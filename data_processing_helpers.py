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

def write_data_to_file(country_name, date, num_hits, headlines):
    """
    Write collected data to csv file
    
    Args:
        country_name: a string representing the name of the country whos data
        is being collected
        date: a string representing the year and month for which the hits are
        collected
        num_hits: an int representing the number of hits from a nytimes article
        search api for a given country and time period
        headlines: a list containing all of the headlines for the month
    Returns:
        No return value
    """
    information = pd.DataFrame([[country_name, date, num_hits, headlines]], columns = ['Country Name', 'MM-YYYY', 'Number of Hits', 'Month\'s Headlines'])
    
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
    new_table = pd.DataFrame([['', '', '', '']], columns = ['Country Name', 'MM-YYYY', 'Number of Hits', 'Month\'s Headlines'])
    
    new_table.to_csv(f'CountryData/{country_name}_data.csv', mode = 'w', header = True, index = False)
    
def headline_list_to_string(country_name, yearmonth):
    """
    Create one long string out of a list of strings, where the list of strings
    is one month's headlines
    
    Args:
        country_name: a string representing the name of the country
        yearmonth: a string representing the month of interest, in YYYYMM format
        
    Returns:
        headline_text: a string that is all of the headlines merged into one string
    """
    data_frame = pd.read_csv(f'CountryData/{country_name}_data.csv')
    
    date = f'{yearmonth[4:]}-{yearmonth[0:4]}'
    
    location = data_frame.index[data_frame['MM-YYYY'] == date][0]
    
    headlines = data_frame['Month\'s Headlines'][location]
    
    headline_text = headlines.strip("['']")
    headline_text = headline_text.replace("', '", " ")
    headline_text = headline_text.replace(chr(8217)+"s", "")
    headline_text = headline_text.replace("'s", "")
    
    return headline_text

def all_headlines_in_string(country_name):
    """
    Create one long string out of all the headlines collected for a country
    over the entire time frame
    
    Args:
        country_name: a string representing the name of the country
    Returns:
        all_text: a string that contains all the headlines merged in one string
    """
    country_data = pd.read_csv(f'CountryData/{country_name}_data.csv')
    
    month_headline_strings = []
    
    for item in country_data['MM-YYYY']:
        year = item[3:]
        month = item[0:2]
        
        month_headline_strings.append(headline_list_to_string(country_name, year + month))
        
    all_text = " ".join(month_headline_strings)
    
    return all_text