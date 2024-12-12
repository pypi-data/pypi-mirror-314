import requests
from .config import HOST

def fbdl(apikey, url):
    url = f'{HOST}/api/downloader/facebook'
    querystring = {
        'apikey': apikey,
        'url': url
    }

    response = requests.get(url, headers=headers, params=querystring)
    response_json = response.json()
    return response_json