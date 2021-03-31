import requests
import json
import os
import pyjq
import pandas as pd

path_lila = "/home/lila/Documents/schoolwork/softdes/google-api-key"
api_path = "https://language.googleapis.com/v1/documents:analyzeSentiment?key="

with open(os.path.abspath(path_lila), "r") as f:
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

    response = requests.post(api_path + api_key, data=json.dumps(body))
    return response


def find_sentiment(response):
    """
    Takes Google Cloud response and outputs sentiment and magnitude as list.
    """
    sentiment = pyjq.all(".documentSentiment .score", response.json())[0]
    magnitude = pyjq.all(".documentSentiment .magnitude", response.json())[0]
    return [sentiment, magnitude]


def add_sentiment_and_mag_to_csv(csv_):
    """
    Does not work DO NOT USE
    """
    data_frame = pd.read_csv(csv_)
    print(data_frame.head())
    #data_frame.set_value(0, "Country Name", "changed")
    data_frame.insert(3, "Sentiment", "a")
    data_frame.insert(4, "Magnitude", "b")

def sentiment_to_csv(country_name, index):
    """
    DOES NOT WORK DO NOT USE

    Analyzes a month's headlines and writes sentiment and magnitude to csv.

    WARNING: cvs should already be created and add_sentiment_and_mag_to_csv
    should be run before this function.

    Args:
        country_name: A string representing the name of the country
        index: An integer refering to a row of the country's csv.

    Returns:
        None.
    """
    data_frame = pd.read_csv(f'CountryData/{country_name}_data.csv')
    headlines = data_frame['Month\'s Headlines'][index]
    headline_text = headlines.strip("['']")
    headline_text = headlines.replace("', '", " ")

    sentiment_magnitude = find_sentiment(request_sentiment(headline_text))
    
    data_frame.set_value(index, "Sentiment (-1 to 1)", sentiment_magnitude[0])


    
