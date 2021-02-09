from replit import db
from threading import Timer
from random import randint
import json
import os
import aiohttp

def reset():
  db['BITCOIN'] = 0
  db['ETHEREUM'] = 0

async def request():
  x = randint(1,7) #select a random api key
  apikey = os.getenv('CRYPTOKEY'+str(x))
  url = "https://pro-api.coinmarketcap.com/v1/cryptocurrency/listings/latest?CMC_PRO_API_KEY="+apikey
  
  async with aiohttp.ClientSession() as session:
    async with session.get(url) as r:
      json_data = await r.json()
      return json_data

async def get_conversion():
  if db['BITCOIN'] > 0 and db['ETHEREUM'] > 0:
    return (db['BITCOIN'],db['ETHEREUM'])
  
  json_data = await request()
  db['BITCOIN'] = json_data['data'][0]['quote']['USD']['price']
  db['ETHEREUM'] = json_data['data'][1]['quote']['USD']['price']
  t = Timer(55,reset)
  t.start()
  return (db['BITCOIN'],db['ETHEREUM'])

async def networth(key):
  r = await get_conversion()
  usd = db[key][0]+r[0]*db[key][1]+r[1]*db[key][2]
  return usd