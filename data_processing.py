import requests
import json
import pyjq
import csv
import pandas as pd
import time
from os import path
import matplotlib.pyplot as plt
import math
from data_processing_helpers import *

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
        num_pages = math.ceil(num_hits / 10)
        page_headlines = pyjq.all('.response .docs[] .headline .main', request.json())
        
        month_all_info += [search_query, current_month, num_hits]
        month_headlines += page_headlines
        
        time.sleep(6)
        if num_pages >= 1:
            for page in range(1, num_pages):
                begin_date = current_month + "01"
                end_date = current_month + days_in_month(current_month)
                request = requests.get(f"https://api.nytimes.com/svc/search/v2/articlesearch.json?q={search_query}&fq=source:(\"The New York Times\")&begin_date={begin_date}&end_date={end_date}&page={page}&api-key={api_key}")
        
                page_headlines = pyjq.all('.response .docs[] .headline .main', request.json())
                month_headlines += page_headlines
                time.sleep(6)
                
            month_all_info.append(month_headlines)
            
        headlines_and_hits.append(month_all_info)
        current_month = next_month(current_month)
        
    return headlines_and_hits

def write_hits_and_headlines_to_file(search_term, begin_month, end_month, api_key):
    """
    Writes monthly hits and headlines to file.

    Args:
        search_term:
        begin_month: String in the format YYYYMM.
        end_month: String in the format YYYYMM.
        api_key: NYTimes Developer API key.

    Returns:
        List.
    """
    search_date_hits_and_headlines = collect_headlines_and_hits(search_term, begin_month, end_month, api_key)
    
    for entry in search_date_hits_and_headlines:
        monthyear = entry[1]
        
        date = f'{monthyear[4:]}-{monthyear[0:4]}'
        
        write_data_to_file(entry[0], date, entry[2], entry[3])
    return search_date_hits_and_headlines

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

