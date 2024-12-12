import requests
from .config import HOST

def simiteach(apikey, ask, ans, lc):
    url = f'{HOST}/api/v1/simiteach'
    querystring = {
        'apikey': apikey,
        'ask': ask,
        'ans': ans,
        'lc': lc,
    }

    response = requests.get(url, headers=headers, params=querystring)
    response_json = response.json()
    return response_json