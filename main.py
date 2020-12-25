import discord
import os
import requests
import json
import random
from replit import db
from keep_alive import keep_alive
from reaper import reaper
client = discord.Client()

#get a random quote from an api
def get_quote():
  response = requests.get("https://zenquotes.io/api/random")
  json_data = json.loads(response.text)
  quote = '"' + json_data[0]['q'] + '"' + " - " + json_data[0]['a']
  return quote

#the bot is online now!
@client.event
async def on_ready():
  print("Successful login as {0.user}".format(client))

@client.event
async def on_message(message):
  #determine the server this message was sent in
  game = "REAPER GAME "+str(message.guild.id)
  if message.author.bot:
    return
  if message.channel.name=='reaper':
    #if this message is a reaper command, let reaper.py handle it.
    response,beginGame = await reaper(message)

    #get the bot's response and send it. If a new game has begun, update the 
    if len(response) > 0:
      botMessage = await message.channel.send(response)
      #begin the game
      if beginGame==True:
        db[game] = (db[game][0],db[game][1],db[game][2],botMessage.id)
        await botMessage.pin()
    return
  #initialize the reaper channel
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
      #if we can't, its because the bot doesn't have enough permissions.
      try:
        await message.guild.create_text_channel(name='reaper',topic="This channel is for playing reaper. Type 'help' to learn how to play.")
        await message.guild.create_role(name='reaper-admin',mentionable=True)
        await message.channel.send("Reaper channel and reaper-admin role created!")
      except:
        response = "Unable to comply. The bot doesn't have the required permission 😭."
        await message.channel.send(response)
  #get a quote
  if message.content == '$quote':
    quote = get_quote()
    await message.channel.send(quote)
  #send a link to the github
  elif message.content == '$github':
    await message.channel.send("https://github.com/Agnimandur/Red-Crab-Inn-Bot")
  #send the help box in markdown
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