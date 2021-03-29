import requests
import json
import pyjq
import csv
import pandas as pd
import time
from os import path
import matplotlib.pyplot as plt
import math

month_days_general = {
    "01": "31",
    "02": "28",
    "03": "31",
    "04": "30",
    "05": "31",
    "06": "30",
    "07": "31",
    "08": "31",
    "09": "30",
    "10": "31",
    "11": "30",
    "12": "31"
}

def days_in_month(year_month):
    """
    Finds number of days in a month with a given year.

    Args:
       year_month: String in format YYYYMM.
    
    Returns:
        A two-character string for the number of days in that month.
    """
    year = year_month[0:4]
    month = year_month[4:]

    if int(year) % 4 == 0 and month == "02":
        return "29"
    return month_days_general[month] 

def next_month(year_month):
    """
    Gives next month.

    Args:
        year_month: String in format YYYYMM.
    
    Returns:
        String in format YYYYMM.
    """
    year = year_month[0:4]
    month = year_month[4:]

    if month == "12":
        return str(int(year) + 1) + "01"
    elif month == "09":
        return year + "10"
    return year + month[0] + str(int(month[1]) + 1)

def request_articles(search_term, begin_date, end_date, api_key):
    """
    Gets NYTimes API response for given search.

    Args:
        search_term: A string to be used as search term.
        begin_date: A string for date in format YYYYMMDD.
        end_date: A string for date in format YYYYMMDD.
        api_key: A string for your NYTimes Developer API key.
    
    Returns:
        A request for this search.
    """
    return requests.get(f"https://api.nytimes.com/svc/search/v2/articlesearch.json?q={search_term}&fq=source:(\"The New York Times\")&begin_date={begin_date}&end_date={end_date}&api-key={api_key}")

def get_hits(request_):
    """
    Finds number of results for request.

    Args:
        request_: A request from NYTimes API.
    
    Returns:
        A positive integer representing number of hits.
    """
    return pyjq.all(".response .meta .hits", request_.json())[0]

def write_data_to_file(country_name, date, num_hits):
    """
    Write collected data to csv file
    
    Args:
        country_name: a string representing the name of the country whos data
        is being collected
        date: a string representing the year and month for which the hits are
        collected
        num_hits: an int representing the number of hits from a nytimes article
        search api for a given country and time period
    Returns:
        No return value
    """
    information = pd.DataFrame([[country_name, date, num_hits]], columns = ['Country Name', 'MM-YYYY', 'Number of Hits'])
    
    filepath = f'CountryData/{country_name}_data.csv'
    
    if path.exists(filepath):
        existing_data = pd.read_csv(filepath)
    
        if existing_data.dropna().empty:
            information.to_csv(filepath, mode = 'w', header = True, index = False)
        else:
            information.to_csv(filepath, mode = 'a', header = False, index = False)
            
    else:
        information.to_csv(filepath, mode = 'w', header = True, index = False)
        
def reset_data_entries(country_name):
    """
    Reset the data in a country's csv file so that the columns contain no data
    
    Args:
        country_name: a string representing the name of the country whos file
        will be reset
    Returns:
        No return value
    """
    new_table = pd.DataFrame([['', '', '']], columns = ['Country Name', 'MM-YYYY', 'Number of Hits'])
    
    new_table.to_csv(f'CountryData/{country_name}_data.csv', mode = 'w', header = True, index = False)

def monthly_hits(search_term, begin_month, end_month, api_key):
    """
    Gives hits per month for a search term in a time period (inclusive).

    Args:
        search_term:
        begin_month: String in the format YYYYMM.
        end_month: String in the format YYYYMM.
        api_key: NYTimes Developer API key.

    Returns:
        List.
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

def write_hits_to_file(search_term, begin_month, end_month, api_key):
    """
    Writes monthly hits to file.

    Args:
        search_term:
        begin_month: String in the format YYYYMM.
        end_month: String in the format YYYYMM.
        api_key: NYTimes Developer API key.

    Returns:
        List.
    """
    search_date_hits = monthly_hits(search_term, begin_month, end_month, api_key)
    
    
    
    for entry in search_date_hits:
        monthyear = entry[1]
        
        date = f'{monthyear[4:]}-{monthyear[0:4]}'
        
        write_data_to_file(entry[0], date, entry[2])
    return search_date_hits

def create_bar_chart(country_name):
    """
    Display a bar chart of hits per month for a country
    
    Args:
        country_name: a string that is the name of the country for which to
        visualize number of hits
    Returns:
        No return value
    """
    country_data = pd.read_csv(f'CountryData/{country_name}_data.csv')
    
    num_entries = len(country_data['MM-YYYY'])
    
    plt.rc('axes', titlesize = 20)
    plt.rc('axes', labelsize = 15)
    plt.rc('xtick', labelsize = 10)
    plt.rc('ytick', labelsize = 10)
    
    plt.figure(figsize = (math.ceil(num_entries / 3), 5))
    plt.bar(country_data['MM-YYYY'], country_data['Number of Hits'])
    
    plt.xticks(rotation = 45)
    
    plt.xlabel('Time Frame (MM-YYYY)')
    plt.ylabel('Number of Hits')
    plt.title(f'Number of Hits in NYTimes Articles per Month for {country_name}')
    
    plt.show()
            