"""
This module deals with visalizing the data that is stored in the country csv
files.

The three main visualizations created in this module are scatterplot,
wordcloud, and bubblechart. There are some variations of the wordcloud creation
so that wordclouds can be created for all the csv data, or just some of it.
"""
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
from wordcloud import WordCloud, STOPWORDS, ImageColorGenerator
from PIL import Image
from processing import all_headlines_in_string, headline_list_to_string

def create_scatter_plot(country_name):
    """
    Display a scatter plot of hits per month for a country using matplotlib.

    Args:
        country_name: A string that is the name of the country for which to
        visualize number of hits
    Returns:
        None.
    """

    country_data = pd.read_csv(f'CountryData/{country_name}_data.csv')

    num_entries = len(country_data['MM-YYYY'])

    begin_date = country_data["MM-YYYY"][0]
    end_date = country_data["MM-YYYY"][num_entries - 1]

    _, axis = plt.subplots(figsize = (20, 10))
    axis.scatter(country_data['MM-YYYY'], country_data['Number of Hits'])

    axis.set_xlabel('Time Frame (MM-YYYY)', fontsize = 20)
    axis.set_ylabel('Number of Hits', fontsize = 20)
    axis.set_title(f'Number of Hits in NYTimes Articles per Month for ' \
              f'{country_name} from {begin_date} to {end_date}', fontsize = 25)

    axis.xaxis.set_major_locator(plt.MaxNLocator(30))
    axis.xaxis.labelpad = 30
    axis.yaxis.labelpad = 30

    plt.xticks(rotation = 45)

def create_word_cloud_one_month(country_name, yearmonth):
    """
    Create a wordcloud based on the headlines collected about the country for
    the given month.

    Args:
        country_name: A string representing the name of the country for which
        to create the wordcloud.
        yearmonth: A string representing the month for which to get headlines,
        in YYYYMM format.
    Returns:
        None.
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

def create_word_cloud_certain_months(country_name, start_month, end_month):
    """
    Create a wordcloud based on the headlines collected about a country for
    a set range of months.

    Args:
        country_name: A string representing the name of the country for which
        to create the wordcloud.
        start_month: A string representing the start month of headlines in
        YYYYMM format.
        end_month: A string representing the end month of headliens in YYYYMM
        format.
    Returns:
        None.
    """

    country_dataframe = pd.read_csv(f"CountryData/{country_name}_data.csv")

    begin_index = country_dataframe.index[
        country_dataframe['MM-YYYY'] == f"{start_month[4:]}-{start_month[0:4]}"
        ][0]
    end_index = country_dataframe.index[
        country_dataframe["MM-YYYY"] == f"{end_month[4:]}-{end_month[0:4]}"
        ][0]

    text = ""
    for index in range(begin_index, end_index + 1):
        month = country_dataframe["MM-YYYY"][index][0:2]
        year = country_dataframe["MM-YYYY"][index][3:]
        text += headline_list_to_string(country_name, year + month)
        text += " "

    background_flag_mask = np.array(Image.open(f"CountryFlags/{country_name}_flag.png"))

    wordcloud = WordCloud(mask=background_flag_mask, background_color="white",
                          stopwords = STOPWORDS,
                          max_words = len(text.split())).generate(text)
    colors = ImageColorGenerator(background_flag_mask)

    colored_cloud = wordcloud.recolor(color_func = colors)

    plt.figure(figsize = (20, 20))
    plt.axis('off')
    plt.imshow(colored_cloud)

def create_word_cloud_all(country_name):
    """
    Create a wordcloud based on all the headlines collected about the country.

    Args:
        country_name: A string representing the name of the country for which
        to create the wordcloud.
    Returns:
        None.
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
    score over time.

    Args:
        country_name: A string representing the name of the country for which
        to create a chart.
    Returns:
        None.
    """

    if country_name[-7 :] == "_subset":
        name = country_name[: -7]
    else:
        name = country_name

    country_data = pd.read_csv(f"CountryData/{country_name}_data.csv")
    num_entries = len(country_data["Country Name"])

    begin_date = country_data["MM-YYYY"][0]
    end_date = country_data["MM-YYYY"][num_entries - 1]

    _, axis = plt.subplots(figsize = (20, 10))
    scatterplot = axis.scatter(country_data['MM-YYYY'], country_data["Sentiment Score (-1 to 1)"],
              s = 10 * country_data["Number of Hits"], alpha = .5, color = 'purple')

    axis.set_xlabel('Time Frame (MM-YYYY)', fontsize = 20)
    axis.set_ylabel('Sentiment Score (-1 to 1)', fontsize = 20)
    axis.set_title(f"New York Times Mentions and Sentiment for {name} from " \
              f"{begin_date} to {end_date}", fontsize = 20)

    handles, labels = scatterplot.legend_elements(prop = "sizes",
    alpha = 0.5, color = "purple", num = 4)
    axis.legend(handles, labels, title = "Number of Hits Times Ten",
    labelspacing = 3, handletextpad = 5, borderpad = 3, bbox_to_anchor = (1, 1))

    axis.xaxis.set_major_locator(plt.MaxNLocator(30))
    axis.xaxis.labelpad = 30
    axis.yaxis.labelpad = 30

    plt.xticks(rotation = 45)
