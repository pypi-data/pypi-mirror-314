import requests
from .config import HOST

def imei(apikey, imei):
    url = f'{HOST}/api/tools/imei'
    querystring = {
        'apikey': apikey,
        'imei': imei
    }

    response = requests.get(url, headers=headers, params=querystring)
    response_json = response.json()
    return response_json