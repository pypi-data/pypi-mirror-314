import requests
from .config import HOST

def trace(apikey, url):
    url = f'{HOST}/api/anime/trace'
    querystring = {
        'apikey': apikey,
        'url': url
    }

    response = requests.get(url, headers=headers, params=querystring)
    response_json = response.json()
    return response_json