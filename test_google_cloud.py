import requests
import json
import os

path_lila = "/home/lila/Documents/schoolwork/softdes/google-api-key"
api_path = "https://language.googleapis.com/v1/documents:analyzeSentiment?key="

with open(os.path.abspath(path_lila), "r") as f:
    api_key = f.readline()


def request_sentiment(text):
    document = {
    "type": "PLAIN_TEXT",
    "language": "en-us",
    "content": text
    }

    response = requests.get(api_path + api_key, document)
    return response