import discord
import os
import requests
import json
import random
from replit import db
from keep_alive import keep_alive
client = discord.Client()

authors = []
with open('authors.txt') as fp:
  for author in fp:
    authors.append(str(author))

def get_random(arr):
  return arr[random.randint(0,len(arr)-1)]

def get_quote():
  response = requests.get("https://zenquotes.io/api/random")
  json_data = json.loads(response.text)
  quote = '"' + json_data[0]['q'] + '"' + " - " + get_random(authors)
  return quote

@client.event
async def on_ready():
  print("We have logged in as {0.user}".format(client))

@client.event
async def on_message(message):
  if message.author == client.user:
    return
  if message.content.startswith("$wait"):
    await message.channel.send("A guy in a black cloak makes secret hand signals in your direction.")
  elif message.content.startswith("$drink"):
    await message.channel.send("Maxene gives you a Dragonbreath Ale")
  elif message.content.startswith("$quote"):
    quote = get_quote()
    await message.channel.send(quote)
  elif message.content.startswith("$money"):
    add = 0
    if len(message.content) > 7:
      add = int(message.content[7:])
    author = message.author.name
    if author in db.keys():
      db[author] = db[author]+add
    else:
      db[author] = add
    
    await message.channel.send("Hello {name} your current balance is {value} gold!".format(name=author,value=db[author]))



#My Discord Bot Token
keep_alive() #it will always be online
client.run(os.getenv('TOKEN'))