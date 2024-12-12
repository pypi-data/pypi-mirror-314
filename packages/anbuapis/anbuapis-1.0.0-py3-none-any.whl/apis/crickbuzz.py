import requests
from .config import HOST

def matches(apikey):
    url = f'{HOST}/api/sports/match'
    querystring = {
        'apikey': apikey,
    }

    response = requests.get(url, headers=headers, params=querystring)
    response_json = response.json()
    return response_json

def score(apikey, url):
    url = f'{HOST}/api/sports/score'
    querystring = {
        'apikey': apikey,
        'url': url
    }

    response = requests.get(url, headers=headers, params=querystring)
    response_json = response.json()
    return response_json