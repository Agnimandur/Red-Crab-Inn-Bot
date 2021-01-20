from replit import db
from threading import Timer
import json
import os
import requests

def reset():
  db['BITCOIN'] = 0

def get_conversion():
  if db['BITCOIN'] > 0:
    return db['BITCOIN']
  apikey = os.getenv('BITCOINKEY')
  response = requests.get("https://pro-api.coinmarketcap.com/v1/cryptocurrency/listings/latest?CMC_PRO_API_KEY="+apikey)
  json_data = json.loads(response.text)
  db['BITCOIN'] = json_data['data'][0]['quote']['USD']['price']
  t = Timer(300,reset)
  t.start()
  return db['BITCOIN']