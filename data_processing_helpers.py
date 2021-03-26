import requests
import json
import pyjq

month_days_general = {
    "01": "31",
    "02": "28",
    "3": "31",
    "4": "30",
    "5": "31",
    "6": "30",
    "7": "31",
    "8": "31",
    "9": "30",
    "10": "31",
    "11": "30",
    "12": "31"
}
def days_in_month(month, year):
    """
    Finds number of days in a month with a given year.

    Args:
        month: Two-character string representing month in digits.
        year: Four-character string representing year in digits.
    
    Returns:
        A two-character string for the number of days in that month.
    """

    if int(year) % 4 == 0 and "month" == "02":
        return "29"
    return month_days_general[month] 

def request_articles(search_term, begin_date, end_date, api_key):
    """
    Gets NYTimes API response for given search.
    WARNING: I think this search currently returns more than just NYTimes articles.
    DOES NOT WORK AT THE MOMENT

    Args:
        search_term: A string to be used as search term.
        begin_date: A string for date in format YYYYMMDD.
        end_date: A string for date in format YYYYMMDD.
        api_key: A string for your NYTimes Developer API key.
    
    Returns:
        A request for this search.
    """
    return requests.get(f"https://api.nytimes.com/svc/search/v2/articlesearch.json?fq={search_term}&begin_date={begin_date}&end_date={end_date}&api-key={api_key}")
    #return requests.get(f"https://api.nytimes.com/svc/search/v2/articlesearch \
    #       .json?fq={search_term}&begin_date={begin_date}&end_date={end_date} \
    #       &api-key={api_key}")

def get_hits(request_):
    """
    Finds number of results for request.

    Args:
        request_: A request from NYTimes API.
    
    Returns:
        A positive integer representing number of hits.
    """
    return pyjq.all(".response .meta .hits", request_.json())[0]

