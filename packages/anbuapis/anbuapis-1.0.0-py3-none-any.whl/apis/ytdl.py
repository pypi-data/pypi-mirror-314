import requests
from .config import HOST

def ytdl(apikey, url):
    url = f'{HOST}/api/downloader/youtube'
    querystring = {
        'apikey': apikey,
        'url': url
    }

    response = requests.get(url, headers=headers, params=querystring)
    response_json = response.json()
    return response_json