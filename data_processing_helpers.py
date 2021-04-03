"""
This file contains helper functions for data collecting and data processing.

The functions in this file deal with constructing NYTimes article search API
requests and writing the data collected from the responses into csv files.
"""

from os import path
import pyjq
import pandas as pd
import requests

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
       year_month: String representing target month in format YYYYMM.

    Returns:
        A two-character string for the number of days in that month in format
        DD.
    """
    year = year_month[0:4]
    month = year_month[4:]

    if int(year) % 4 == 0 and month == "02":
        return "29"
    return month_days_general[month]

def next_month(year_month):
    """
    Give the month following the input month.

    Args:
        year_month: String representing the month in format YYYYMM.

    Returns:
        A string representing the following month in format YYYYMM.
    """
    year = year_month[0:4]
    month = year_month[4:]

    if month == "12":
        return str(int(year) + 1) + "01"
    if month == "09":
        return year + "10"
    return year + month[0] + str(int(month[1]) + 1)

def request_articles(search_term, begin_date, end_date, api_key, page=1):
    """
    Gets NYTimes Article Search API response for given search term, date range,
    and API key. Can also provide a page of search results, but one is default.

    Args:
        search_term: A string representing the search term.
        begin_date: A string representing the start date in format YYYYMMDD.
        end_date: A string representing the end date in format YYYYMMDD.
        api_key: A string representing a NYTimes Developer API key.

    Returns:
        A Response for this request in NYTimes Article Search API.
    """
    return requests.get(f"https://api.nytimes.com/svc/search/v2/" \
                        f"articlesearch.json?q={search_term}&fq=" \
                        f"source:(\"The New York Times\")&begin_" \
                        f"date={begin_date}&end_date={end_date}&" \
                        f"page={page}&api-key={api_key}")

def get_hits(response_):
    """
    Finds number of results for a NYTimes API request.

    Args:
        response_: A Response from the NYTimes article search API.

    Returns:
        A positive integer representing number of hits, as indicated by the
        API response.
    """
    return pyjq.all(".response .meta .hits", response_.json())[0]

def write_data_to_file(country_name, date, num_hits, headlines):
    """
    Write collected data to csv file for one month.

    Args:
        country_name: a string representing the name of the country whose data
        is being collected
        date: a string representing the year and month for which the hits are
        collected
        num_hits: an int representing the number of hits from a NYTimes article
        search api for a given country and time period
        headlines: a list containing all of the headlines for the month
    Returns:
        None.
    """
    information = pd.DataFrame([[country_name, date, num_hits, headlines]],
                               columns = ['Country Name', 'MM-YYYY',
                                          'Number of Hits',
                                          'Month\'s Headlines'])

    filepath = f'CountryData/{country_name}_data.csv'

    if path.exists(filepath):
        existing_data = pd.read_csv(filepath)

        if existing_data["Country Name"].dropna().empty:
            information.to_csv(filepath, mode = 'w', header = True, index = False)
        else:
            information.to_csv(filepath, mode = 'a', header = False, index = False)

    else:
        information.to_csv(filepath, mode = 'w', header = True, index = False)

def reset_data_entries(country_name):
    """
    Reset the data in a country's csv file so that the columns contain no data

    Args:
        country_name: a string representing the name of the country whose file
        will be reset
    Returns:
        No return value
    """
    new_table = pd.DataFrame([['', '', '', '', '', '']],
                             columns = ['Country Name', 'MM-YYYY',
                                        'Number of Hits',
                                        'Sentiment Score (-1 to 1)',
                                        'Magnitude', 'Month\'s Headlines'])

    new_table.to_csv(f'CountryData/{country_name}_data.csv', mode = 'w',
                     header = True, index = False)

def headline_list_to_string(country_name, year_month):
    """
    Create one long string out of a list of strings, where the list of strings
    is one month's headlines.

    Accesses csv to take one month's headlines and remove quotes, commas, and
    other list artifacts.

    Args:
        country_name: A string representing the name of the country.
        year_month: A string representing the month, in YYYYMM format.

    Returns:
        headline_text: A string that contains one month's headlines.
    """
    data_frame = pd.read_csv(f'CountryData/{country_name}_data.csv')

    date = f'{year_month[4:]}-{year_month[0:4]}'

    location = data_frame.index[data_frame['MM-YYYY'] == date][0]

    headlines = data_frame['Month\'s Headlines'][location]

    headline_text = headlines.strip("['']")
    headline_text = headline_text.replace("', '", " ")
    headline_text = headline_text.replace(chr(8217)+"s", "")#
    headline_text = headline_text.replace("'s", "")#

    return headline_text

def all_headlines_in_string(country_name):
    """
    Create one long string out of all the headlines collected for a country
    over the entire time frame.

    Accesses csv file's Headlines column to get one string of all headlines
    in all rows.

    Args:
        country_name: A string representing the name of the country.
    Returns:
        all_text: A string that contains all the headlines merged in one string.
    """
    country_data = pd.read_csv(f'CountryData/{country_name}_data.csv')

    month_headline_strings = []

    for item in country_data['MM-YYYY']:
        year = item[3:]
        month = item[0:2]

        month_headline_strings.append(headline_list_to_string(country_name, year + month))

    all_text = " ".join(month_headline_strings)

    return all_text
