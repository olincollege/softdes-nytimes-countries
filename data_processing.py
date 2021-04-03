"""
This file deals with organizing the collected data and visualizing it.

The functions in this file utilize functions from the helper file to
make sure that the data is in the correct format to be read/written, and
the last several functions deal with creating scatter plots, word clouds,
and bubble charts.
"""
import time
import math
import matplotlib.pyplot as plt
import pandas as pd
from wordcloud import WordCloud, STOPWORDS, ImageColorGenerator
import numpy as np
from PIL import Image
import pyjq
import requests
from data_processing_helpers import (days_in_month, next_month,
                                     request_articles, get_hits,
                                     write_data_to_file,
                                     headline_list_to_string,
                                     all_headlines_in_string)

def monthly_hits(search_term, begin_month, end_month, api_key):
    """
    Gives hits per month for a search term in a time period (inclusive).

    Args:
        search_term: a string representing the search query
        begin_month: String representing the starting month in the format
        YYYYMM.
        end_month: String representing the ending month in the format
        YYYYMM.
        api_key: A string representing a NYTimes Developer API key.

    Returns:
        search_date_hits: a list containing integers representing the monthly
        number of hits for the search term
    """
    search_date_hits = []
    i = 0
    current_month = begin_month
    while current_month != next_month(end_month):
        #Appends "01" to YYYYMM and appends days_in_month(current_month)
        #to get start and end dates
        search_date_hits.append(
            [
                search_term,
                current_month,
                get_hits(request_articles(search_term, current_month + \
                "01", current_month + days_in_month(current_month), api_key))
            ]
        )
        i += 1
        current_month = next_month(current_month)
        time.sleep(6)
    return search_date_hits

def collect_headlines_and_hits(search_query, yyyymm_start, yyyymm_end, api_key):
    """
    Collect the headlines and hits over a period of time for a given search

    Args:
        search_query: a string that represents the search term
        yyyymm_start: a string that represents the start date in the YYYYMM
        format
        yyyymm_end: a string that represents the end date in the YYYYMM
        format
        api_key: a string that represents the user's public api key

    Returns:
        headlines_and_hits: a list containing a list of the following info:
        ['country name', 'month range', 'hits', 'headlines'] for each month
        indicated by the time frame for the inputs
    """
    headlines_and_hits = []
    current_month = yyyymm_start

    while current_month != next_month(yyyymm_end):
        month_all_info = []
        month_headlines = []
        request = request_articles(search_query, current_month + \
                "01", current_month + days_in_month(current_month), api_key)
        num_hits = get_hits(request)
        
        month_all_info += [search_query, current_month, num_hits]
        
        if num_hits == 0:
            month_all_info.append("")
            headlines_and_hits.append(month_all_info)
            current_month = next_month(current_month)
            continue
        
        num_pages = math.ceil(num_hits / 10)
        page_headlines = pyjq.all('.response .docs[] .headline .main',
                                  request.json())

        
        month_headlines += page_headlines

        time.sleep(6)
        if num_pages >= 1:
            for page in range(1, num_pages):
                begin_date = current_month + "01"
                end_date = current_month + days_in_month(current_month)
                request =data_processing_helpers.request_articles(search_query,
                                                                  begin_date,
                                                                  end_date,
                                                                  api_key)
                page_headlines = pyjq.all('.response .docs[] .headline .main',
                                          request.json())
                month_headlines += page_headlines
                time.sleep(6)

            month_all_info.append(month_headlines)

        headlines_and_hits.append(month_all_info)
        current_month = next_month(current_month)

    return headlines_and_hits

def write_hits_and_headlines_to_file(search_term, begin_month, end_month, api_key):
    """
    For a given search term and start/end dates, write the collected data to a
    csv file, with a new row for each month's info

    Args:
        search_term: a string representing the search query
        begin_month: String representing the start date in the format
        YYYYMM.
        end_month: String representing the end date in the format
        YYYYMM.
        api_key: a string representing a NYTimes Developer API key.

    Returns:
        search_date_hits_and_headlines: A list containing the info that was
        written to the csv file
    """
    search_date_hits_and_headlines = collect_headlines_and_hits(search_term,
                                                                begin_month,
                                                                end_month,
                                                                api_key)

    for entry in search_date_hits_and_headlines:
        monthyear = entry[1]

        date = f'{monthyear[4:]}-{monthyear[0:4]}'

        write_data_to_file(entry[0], date, entry[2], entry[3])
    return search_date_hits_and_headlines

def create_scatter_plot(country_name):
    """
    Display a scatter plot of hits per month for a country

    Args:
        country_name: a string that is the name of the country for which to
        visualize number of hits
    Returns:
        No return value
    """
    country_data = pd.read_csv(f'CountryData/{country_name}_data.csv')

    num_entries = len(country_data['MM-YYYY'])

    begin_date = country_data["MM-YYYY"][0]
    end_date = country_data["MM-YYYY"][num_entries - 1]

    plt.rc('axes', titlesize = 20)
    plt.rc('axes', labelsize = 15)
    plt.rc('xtick', labelsize = 10)
    plt.rc('ytick', labelsize = 10)

    plt.figure(figsize = (math.ceil(num_entries / 2), 5))
    plt.scatter(country_data['MM-YYYY'], country_data['Number of Hits'])

    plt.xticks(rotation = 45)

    plt.xlabel('Time Frame (MM-YYYY)')
    plt.ylabel('Number of Hits')
    plt.title(f'Number of Hits in NYTimes Articles per Month for ' \
              f'{country_name} from {begin_date} to {end_date}')

    plt.show()

def create_word_cloud_one_month(country_name, yearmonth):
    """
    Create a wordcloud based on the headlines collected about the country for
    the given month

    Args:
        country_name: a string representing the name of the country for which
        to create the wordcloud
        yearmonth: a string representing the month for which to get headlines,
        in YYYYMM format
    Returns:
        No return value
    """
    text = headline_list_to_string(country_name, yearmonth)
    num_words = len(text.split())

    background_flag_mask = np.array(Image.open(f"CountryFlags/{country_name}_flag.png"))

    wordcloud = WordCloud(mask=background_flag_mask, background_color="white",
                          stopwords = STOPWORDS, max_words = num_words).generate(text)
    colors = ImageColorGenerator(background_flag_mask)

    colored_cloud = wordcloud.recolor(color_func = colors)

    plt.figure(figsize = (20, 20))
    plt.axis('off')
    plt.imshow(colored_cloud)

def create_word_cloud_all(country_name):
    """
    Create a wordcloud based on all the headlines collected about the country

    Args:
        country_name: a string representing the name of the country for which
        to create the wordcloud
    Returns:
        No return value
    """
    text = all_headlines_in_string(country_name)
    num_words = len(text.split())

    background_flag_mask = np.array(Image.open(f"CountryFlags/{country_name}_flag.png"))

    wordcloud = WordCloud(mask=background_flag_mask, background_color="white",
                          stopwords = STOPWORDS, max_words = num_words).generate(text)
    colors = ImageColorGenerator(background_flag_mask)

    colored_cloud = wordcloud.recolor(color_func = colors)

    plt.figure(figsize = (20, 20))
    plt.axis('off')
    plt.imshow(colored_cloud)

def create_bubble_chart(country_name):
    """
    Create a bubble chart for a country based on number of hits and sentiment
    score over time

    Args:
        country_name: a string representing the name of the country for which
        to create a chart
    Returns:
        No return value
    """
    country_data = pd.read_csv(f"CountryData/{country_name}_data.csv")
    num_entries = len(country_data["Country Name"])

    plt.figure(figsize = (math.ceil(num_entries / 2), 5))
    plt.scatter(x = country_data["MM-YYYY"], y = country_data["Sentiment Score (-1 to 1)"],
                s = 10 * country_data["Number of Hits"], alpha = .5, color = 'purple')

    plt.xticks(rotation = 45)
    plt.xlabel("Time Frame (MM-YYYY)", size = 15)
    plt.ylabel("Sentiment Score (-1 to 1)", size = 15)

    begin_date = country_data["MM-YYYY"][0]
    end_date = country_data["MM-YYYY"][num_entries - 1]

    plt.title(f"New York Times Attention and Attitude Towards {country_name} from " \
              f"{begin_date} to {end_date}", size = 20)

    plt.show()
