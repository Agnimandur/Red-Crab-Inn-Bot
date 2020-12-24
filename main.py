import discord
import os
import requests
import json
import random
from replit import db
from keep_alive import keep_alive
from reaper import reaper
client = discord.Client()

def get_quote():
  response = requests.get("https://zenquotes.io/api/random")
  json_data = json.loads(response.text)
  quote = '"' + json_data[0]['q'] + '"' + " - " + json_data[0]['a']
  return quote

@client.event
async def on_ready():
  print("Successful login as {0.user}".format(client))

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
      await message.guild.create_text_channel('reaper')
      await message.guild.create_role(name='reaper-admin')
      await message.channel.send("Reaper channel and reaper-admin role created!")
  if message.content.startswith('$quote'):
    quote = get_quote()
    await message.channel.send(quote)
  elif message.content.lower() == 'help':
    response = """```
Reaper Setup:
  $reaper            Initialize the Reaper channel in a server.
Miscellaneous:
  $quote             Receive an inspirational quote.
    ```"""
    await message.channel.send(response)



#My Discord Bot Token
keep_alive() #it will always be online
client.run(os.getenv('TOKEN'))
