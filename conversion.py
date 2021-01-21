from replit import db
from threading import Timer
from random import randint
import json
import os
import requests

def reset():
  db['BITCOIN'] = 0
  db['ETHEREUM'] = 0

def get_conversion():
  if db['BITCOIN'] > 0 and db['ETHEREUM'] > 0:
    return (db['BITCOIN'],db['ETHEREUM'])
  x = randint(1,7) #select a random api key
  apikey = os.getenv('CRYPTOKEY'+str(x))
  response = requests.get("https://pro-api.coinmarketcap.com/v1/cryptocurrency/listings/latest?CMC_PRO_API_KEY="+apikey)
  json_data = json.loads(response.text)
  db['BITCOIN'] = json_data['data'][0]['quote']['USD']['price']
  db['ETHEREUM'] = json_data['data'][1]['quote']['USD']['price']
  t = Timer(55,reset)
  t.start()
  return (db['BITCOIN'],db['ETHEREUM'])

def networth(key):
  r = get_conversion()
  return db[key][0]+r[0]*db[key][1]+r[1]*db[key][2]