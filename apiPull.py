import json
import csv
from pandas.io.json import json_normalize
import requests
from requests import Session
from requests.exceptions import ConnectionError, Timeout, TooManyRedirects
import pandas as pd

#Coin Market Cap API CALL
def getCoins():
    url = 'https://pro-api.coinmarketcap.com/v1/cryptocurrency/listings/latest'
    parameters = {
        'limit': '300',
        'convert': 'USD',

    }
    headers = {
        'Accepts': 'application/json',
        'X-CMC_PRO_API_KEY': '',
    }

    session = Session()
    session.headers.update(headers)

    # CSV Writer, calls for ADA BTC AND ETH

    try:
        # get API Response, load data into variable
        response = session.get(url, params=parameters)
        jsonData = json.loads(response.text)
        coinData = pd.json_normalize(jsonData['data'])
        coinData.to_csv('cryptoData.csv')



    except (ConnectionError, Timeout, TooManyRedirects) as e:
        print(e)

