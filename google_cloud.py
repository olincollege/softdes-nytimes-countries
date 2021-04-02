"""
This file deals with analyzing the collected article headlines using Google
Cloud's Natural Language API

The functions in this file access the data that is already collected in the
csv data files, namely the headlines, and constructing the data so that it can
be sent to Google's language analysis API, rewriting it to the csv files after
analysis is completed.
"""
import json
import os
import pyjq
import pandas as pd
import requests
import data_processing_helpers

#PATH_LILA = "/home/lila/Documents/schoolwork/softdes/google-api-key"
PATH_ALEX = "/home/softdes/Desktop/google-api-key"
API_PATH = "https://language.googleapis.com/v1/documents:analyzeSentiment?key="

with open(os.path.abspath(PATH_ALEX), "r") as f:
    api_key = f.readline()


def request_sentiment(text):
    """
    Sends HTTP post to Google Cloud and receives result.
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
