import requests
from .config import HOST

def simitalk(apikey, ask, lc):
    url = f'{HOST}/api/v1/simitalk'
    querystring = {
        'apikey': apikey,
        'ask': ask,
        'lc': lc,
    }

    response = requests.get(url, headers=headers, params=querystring)
    response_json = response.json()
    return response_json