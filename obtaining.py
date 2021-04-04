import math
import pyjq
import pandas as pd
import requests
import time

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
                request = request_articles(search_query, begin_date, end_date,
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