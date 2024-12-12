import requests
from .config import HOST

def neko(apikey):
    url = f'{HOST}/api/anime/neko'
    querystring = {
        'apikey': apikey,
    }

    response = requests.get(url, headers=headers, params=querystring)
    response_json = response.json()
    return response_json