import requests
import json
import os 
path_lila = "/home/lila/Documents/schoolwork/softdes/google-api-key"
api_path = "https://language.googleapis.com/v1/documents:analyzeSentiment?key="

with open(os.path.abspath(path_lila), "r") as f:
    api_key = f.readline()


def request_sentiment(text):
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