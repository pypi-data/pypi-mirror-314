import requests
from .config import HOST

def instadl(apikey, url):
    url = f'{HOST}/api/downloader/instagram'
    querystring = {
        'apikey': apikey,
        'url': url
    }

    response = requests.get(url, headers=headers, params=querystring)
    response_json = response.json()
    return response_json