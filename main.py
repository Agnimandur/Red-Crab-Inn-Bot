import discord
import os
import requests
import json
import random
from replit import db
from keep_alive import keep_alive
from reaper import reaper
client = discord.Client()

authors = []
with open('authors.txt') as fp:
  for author in fp:
    authors.append(str(author))

drinks = []
with open('drinks.txt') as fp:
  for drink in fp:
    drinks.append(str(drink))

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
  if message.channel.name=='reaper':
    response = await reaper(message)
    if len(response) > 0:
      botMessage = await message.channel.send(response)
      if (botMessage.content.startswith("**The game has begun!**")):
        await botMessage.pin()
    return
  if message.content == '$reaper':
    reaperID = 0
    allChannels = await message.guild.fetch_channels()
    for c in allChannels:
      if c.name=='reaper':
        reaperID = c.id
        break
    if reaperID != 0:
      await message.channel.send("Reaper channel already exists. Go to <#{reaperID}>.".format(reaperID=reaperID))
    else:
      channel = await message.guild.create_text_channel('reaper')
      await message.channel.send("Reaper Channel Created!")
  if message.content.startswith("$wait"):
    await message.channel.send("A guy in a black cloak makes secret hand signals in your direction.")
  elif message.content.startswith("$drink"):
    await message.channel.send("Maxene gives you a " + get_random(drinks))
  elif message.content.startswith("$quote"):
    quote = get_quote()
    await message.channel.send(quote)
  elif message.content.startswith("$money"):
    add = 0
    if len(message.content) > 7:
      try:
        add = int(message.content[7:])
      except:
        add = 0
    author = message.author.name
    server = str(message.guild.id)
    key = author+server
    if key in db.keys():
      db[key] = db[key]+add
    else:
      db[key] = add
    
    await message.channel.send("Hello {name} your current balance is {value} gold!".format(name=author,value=db[key]))



#My Discord Bot Token
keep_alive() #it will always be online
client.run(os.getenv('TOKEN'))
