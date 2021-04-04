"""
This file deals with processing the collected data.

These functions access the csv file to get headlines and use Google Cloud
Natural Language API to get sentiment analysis.
"""
import json
import os
import pandas as pd
import pyjq
import requests

PATH_LILA = "api-keys/google-api-key-lila"
PATH_ALEX = "/home/softdes/Desktop/google-api-key"
API_PATH = "https://language.googleapis.com/v1/documents:analyzeSentiment?key="

with open(os.path.abspath(PATH_LILA), "r") as f:
    api_key = f.readline()

#Headline to String Functions
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
    
    if data_frame["Number of Hits"][location] == 0:
        return ""

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


#Google Natural Language API Functions
def request_sentiment(text):
    """
    Sends HTTP post to Google Cloud and receives Response.

    Args:
        text: A string to have its context 
    """
    body = {
        "document": {
            "type": "PLAIN_TEXT",
            "language": "en-us",
            "content": text
        },
    "encodingType": "UTF32"
    }

    response = requests.post(API_PATH + api_key, data=json.dumps(body))
    return response

def find_sentiment(response):
    """
    Takes Google Cloud response and outputs sentiment and magnitude as list.
    """
    sentiment = pyjq.all(".documentSentiment .score", response.json())[0]
    magnitude = pyjq.all(".documentSentiment .magnitude", response.json())[0]
    return [sentiment, magnitude]

def sentiment_and_magnitude_to_csv(country_name):
    """
    Conduct sentiment analysis on monthly headlines for a given country and
    update the country's data file with the corresponding scores

    Args:
        country_name: a string representing the name of the country whose
        headlines will be analyzed
    Return:
        No return value
    """
    country_dataframe = pd.read_csv(f'CountryData/{country_name}_data.csv')

    sentiment_scores = []
    magnitudes = []

    for item in country_dataframe["MM-YYYY"]:
        year = item[3:]
        month = item[0:2]
        text = data_processing_helpers.headline_list_to_string(country_name, year + month)
        analysis = find_sentiment(request_sentiment(text))

        sentiment_scores.append(analysis[0])
        magnitudes.append(analysis[1])

    country_dataframe["Sentiment Score (-1 to 1)"] = sentiment_scores
    country_dataframe["Magnitude"] = magnitudes

    updated_dataframe = country_dataframe

    updated_dataframe.to_csv(f'CountryData/{country_name}_data.csv', index = False)
