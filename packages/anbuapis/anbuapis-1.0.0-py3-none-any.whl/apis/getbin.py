import requests
from .config import HOST

def getBin(apikey, binNo):
    url = f'{HOST}/api/tools/bin'
    querystring = {
        'apikey': apikey,
        'bin': binNo
    }

    response = requests.get(url, headers=headers, params=querystring)
    response_json = response.json()
    return response_json