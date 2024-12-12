import requests
from .config import HOST

def device(apikey, search):
    url = f'{HOST}/api/tools/device'
    querystring = {
        'apikey': apikey,
        'search': search
    }

    response = requests.get(url, headers=headers, params=querystring)
    response_json = response.json()
    return response_json