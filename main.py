import discord
import os
import requests
import json
import random
from replit import db
from keep_alive import keep_alive
from reaper import reaper
from help import make_embed

#set up the bot
intents = discord.Intents.default()
intents.members = True
client = discord.Client(intents=intents,activity=discord.Game(name="Reaper"))

#get a random quote from an api
def get_quote():
  response = requests.get("https://zenquotes.io/api/random")
  json_data = json.loads(response.text)
  quote = '"' + json_data[0]['q'] + '"' + " - " + json_data[0]['a']
  return quote

#get a random Donald Trump quote from an api
def get_trump():
  response = requests.get("https://tronalddump.io/random/quote")
  response2 = requests.get("https://api.whatdoestrumpthink.com/api/v1/quotes/random")
  json_data = json.loads(response.text)
  json_data2 = json.loads(response2.text)
  quote = '"'+json_data['value']+'" \n *Date: {date}*'.format(date=json_data['appeared_at'][:10])
  if random.randint(1,2)==1:
    quote = '"'+json_data2['message']+'"'
  return quote

#get a random Kanye West quote from an api
def get_kanye():
  response = requests.get("https://api.kanye.rest/")
  json_data = json.loads(response.text)
  quote = json_data['quote']
  if quote[-1] != '.':
    quote += '.'
  quote = '"'+quote+'"'
  return quote

#8ball function
ballFile = open('8ball.txt','r')
ballList = ballFile.readlines()
ballFile.close()
def ball():
  r = random.randint(0,19)
  return ballList[r].strip('\n')

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
  if message.channel.name == 'reaper' or message.channel.name == 'reaper-discussion':
    #if this message is a reaper command, let reaper.py handle it.
    response,beginGame = await reaper(message)

    #get the bot's response and send it. If a new game has begun, update the 
    if len(response) > 0:
      botMessage = await message.channel.send(response)
      #begin the game
      if beginGame==True:
        db[game] = (db[game][0],db[game][1],db[game][2],db[game][3],botMessage.id)
        try:
          await botMessage.pin()
        except:
          print(message.guild.name + " doesn't have pin privileges")
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
    elif not message.author.guild_permissions.administrator:
      await message.channel.send("Only an admin can do this!")
    else:
      #if we can't, its because the bot doesn't have enough permissions.
      try:
        await message.channel.send("Reaper initialization in progress...")
        category = await message.guild.create_category(name='Reaper')
        await message.guild.create_text_channel(name='reaper',topic="This channel is for playing reaper. Type 'help' to learn how to play.",slowmode_delay=3,category=category)
        await message.guild.create_text_channel(name='reaper-discussion',topic="It is recommended you do leaderboard,rank,timer commands in this channel to avoid clutter.",category=category)
        reaperadmin = await message.guild.create_role(name='reaper-admin',mentionable=True)
        await message.guild.create_role(name='banned-from-reaper',mentionable=False)
        for m in message.guild.members:
          if not m.bot and m.guild_permissions.administrator:
            await m.add_roles(reaperadmin)
        await message.channel.send("Reaper channels and reaper-admin role created! All admins are automatically a {ra}!".format(ra=reaperadmin.mention))
      except:
        response = "Unable to comply. The bot doesn't have the required permission 😭."
        await message.channel.send(response)
  #remove the bot from your server
  if message.content == '$leave':
    if not message.author.guild_permissions.administrator:
      await message.channel.send("Only an admin can do this!")
      return
    g = message.guild
    await message.channel.send("What wonderful times we've shared together! Goodbye, and may the Seven smile upon you.")
    for channel in g.channels:
      if channel.name.lower().find('reaper') >= 0:
        await channel.delete()
    for category in g.categories:
      if category.name.lower().find('reaper') >= 0:
        await category.delete()
    for role in g.roles:
      if role.name.lower().find('reaper') >= 0:
        await role.delete()
    #purge the database
    gid = str(g.id)
    for key in db.keys():
      if key.find(gid) >= 0:
        del db[key]
    await g.leave()
  #get a quote
  if message.content == '$quote':
    quote = get_quote()
    await message.channel.send(quote)
  #get a trump quote
  elif message.content == '$trump':
    quote = get_trump()
    await message.channel.send(quote)
  #get a kanye quote
  elif message.content == '$kanye':
    quote = get_kanye()
    await message.channel.send(quote)
  #the 8ball will answer your query
  elif message.content == '$8ball':
    response = ball()
    await message.channel.send(message.author.mention + " " + response)
  #send a link to the github
  elif message.content == '$github':
    await message.channel.send("https://github.com/Agnimandur/Red-Crab-Inn-Bot")
  #number of servers the bot is in
  elif message.content == '$servers':
    totalPeople = sum([(1 if not x.bot else 0) for x in client.users])
    await message.channel.send("The Red Crab Inn is currently in {s} servers, serving {p} people across Discord!".format(s=len(client.guilds),p=str(totalPeople)))
  #send the help box in markdown
  elif message.content.lower() == 'help':
    embed = make_embed(title="Miscellaneous Commands",description="These are commands for initializing the Reaper game, and for other random things. All these commands have a **$** prefix.").add_field(name="**Reaper Related**",value="""
- $reaper. Initialize the Reaper channels and roles in your server.
- $leave. Remove the Red Crab Inn bot and all associated roles and channels from your server. All history **will be lost**!""").add_field(name="**Random Commands**",value="""
- $quote. Get an inspirational quote!
- $trump. Get a Donald Trump quote.
- $kanye. Get a Kanye West quote.
- $8ball. Ask the 8Ball something!
- $github. Get a link to this bot's public github repository.
- $servers. Find out how many servers the Red Crab Inn is in!""")
    await message.channel.send(embed=embed)



#My Discord Bot Token
keep_alive() #it will always be online
client.run(os.getenv('TOKEN'))