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
  game = "REAPER GAME "+str(message.guild.id)
  if message.author.bot:
    return
  if message.channel.name=='reaper':
    response = await reaper(message)
    if len(response) > 0:
      botMessage = await message.channel.send(response)
      if (botMessage.content.startswith("**The game has begun!**")):
        db[game] = (db[game][0],db[game][1],db[game][2],botMessage.id)
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
      try:
        await message.guild.create_text_channel('reaper')
        await message.guild.create_role(name='reaper-admin')
        await message.channel.send("Reaper channel and reaper-admin role created!")
      except:
        await message.channel.send("Unable to comply. The bot doesn't have the required permission.")
  if message.content == '$quote':
    quote = get_quote()
    await message.channel.send(quote)
  elif message.content == '$github':
    await message.channel.send("https://github.com/Agnimandur/Red-Crab-Inn-Bot")
  elif message.content.lower() == 'help':
    response = """```
Reaper Setup:
  $reaper            Initialize the Reaper channel in a server.

  All Reaper related commands can only be done in the #reaper channel.

Miscellaneous:
  $quote             Receive an inspirational quote.
  
  $github            Get a link to the bot's github page.
    ```"""
    await message.channel.send(response)



#My Discord Bot Token
keep_alive() #it will always be online
client.run(os.getenv('TOKEN'))
