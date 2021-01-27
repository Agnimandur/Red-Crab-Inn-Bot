import discord
import os
import requests
import json
import random
from replit import db
from keep_alive import keep_alive
from reaper import reaper
from reaper import cache
from help import main_help
from crypto import crypto
from threading import Timer
import time

#set up the bot
AGNIMANDUR = 482581806143766529
intents = discord.Intents.default()
intents.members = True
client = discord.Client(intents=intents,activity=discord.Game(name="Reaper"))
delay = set()

def get_quote():
  response = requests.get("https://zenquotes.io/api/random")
  json_data = json.loads(response.text)
  quote = '"' + json_data[0]['q'] + '"' + " - " + json_data[0]['a']
  return quote

def get_trump():
  response = requests.get("https://tronalddump.io/random/quote")
  response2 = requests.get("https://api.whatdoestrumpthink.com/api/v1/quotes/random")
  json_data = json.loads(response.text)
  json_data2 = json.loads(response2.text)
  quote = '"'+json_data['value']+'" \n *Date: {date}*'.format(date=json_data['appeared_at'][:10])
  if random.randint(1,2)==1:
    quote = '"'+json_data2['message']+'"'
  return quote

def get_kanye():
  response = requests.get("https://api.kanye.rest/")
  json_data = json.loads(response.text)
  quote = json_data['quote']
  if quote[-1] != '.':
    quote += '.'
  quote = '"'+quote+'"'
  return quote

def get_ron():
  response = requests.get("http://ron-swanson-quotes.herokuapp.com/v2/quotes")
  json_data = json.loads(response.text)
  quote = '"'+json_data[0]+'"'
  return quote

def get_year(yr):
  response = requests.get("http://numbersapi.com/{yr}/year?json".format(yr=yr))
  json_data = json.loads(response.text)
  quote = json_data['text']
  return quote

def get_math_trivia():
  response = requests.get("http://numbersapi.com/random/math?json")
  json_data = json.loads(response.text)
  quote = json_data['text']
  return quote

#the bot is online now!
@client.event
async def on_ready():
  db['BITCOIN'] = 0
  db['ETHEREUM'] = 0
  print("Successful login as {name}".format(name=str(client.user)))

def reset(ID):
  delay.remove(ID)

def begin(ID):
  delay.add(ID)
  t = Timer(5,reset,[ID])
  t.start()

@client.event
async def on_message(message):
  if message.author.bot or not type(message.channel)==discord.TextChannel or message.author.id in delay:
    return
  wait = "WAIT "+str(message.author.id)
  if wait in db.keys() and round(time.time())-db[wait] < 20:
    return

  #determine the server this message was sent in
  try:
    game = "REAPER GAME "+str(message.guild.id)
  except:
    print(message)
    return
  
  if message.channel.name == 'reaper-crypto':
    response = await crypto(message)
    if response == 200 or len(response) > 0:
      begin(message.author.id)
      if response == 200:
        return
      await message.channel.send(response)
      return

  if message.channel.name == 'reaper' or message.channel.name == 'reaper-discussion':
    #if this message is a reaper command, let reaper.py handle it.
    response,beginGame = await reaper(message)
    #get the bot's response and send it.
    if response == 200 or len(response) > 0:
      begin(message.author.id)
      if response == 200:
        return
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
  skip = False
  if message.content == '$reaper':
    reaperID = 0
    for c in message.guild.channels:
      try:
        if c.name=='reaper':
          reaperID = c.id
          break
      except:
        pass
    if reaperID != 0:
      await message.channel.send("Reaper channel already exists. Go to <#{reaperID}>.".format(reaperID=reaperID))
    elif not message.author.guild_permissions.administrator:
      await message.channel.send("Only an admin can do this!")
    else:
      #if we can't, its because the bot doesn't have enough permissions.
      try:
        await message.channel.send("Reaper initialization in progress...")
        reaperadmin = await message.guild.create_role(name='reaper-admin',mentionable=True)
        banned = await message.guild.create_role(name='banned-from-reaper',mentionable=False)
        category = await message.guild.create_category(name='Reaper')
        re = await message.guild.create_text_channel(name='reaper',topic="This channel is for playing reaper. Type 'help' to learn how to play.",slowmode_delay=1,category=category)
        await re.set_permissions(banned,read_messages=True,send_messages=False)
        rd = await message.guild.create_text_channel(name='reaper-discussion',topic="It is recommended you do leaderboard,rank,timer commands in this channel to avoid clutter.",category=category)
        await rd.set_permissions(banned,read_messages=True,send_messages=False)
        rc = await message.guild.create_text_channel(name='reaper-crypto',topic="Buy and sell cryptocurrency in this channel! Type join to enter!",slowmode_delay=2,category=category)
        await rc.set_permissions(banned,read_messages=True,send_messages=False)
        for m in message.guild.members:
          if not m.bot and m.guild_permissions.administrator:
            await m.add_roles(reaperadmin)
        cache[message.guild.id] = (reaperadmin,banned)
        await message.channel.send("Reaper channels and reaper-admin role created! All admins are automatically a reaper-admin! Type in $help for more information.")
      except:
        response = "Unable to comply. The bot doesn't have the required permission 😭."
        await message.channel.send(response)
  #remove the bot from your server
  if message.content == '$leave':
    if not message.author.guild_permissions.administrator:
      await message.channel.send("Only an admin can do this!")
      return
    g = message.guild

    await message.channel.send("Are you sure you want to remove the Red Crab Inn from your server? (yes/no)")
    def check(m):
      return m.author==message.author and m.channel==message.channel
    abort = True
    try:
      conf = await client.wait_for('message',timeout=5.0,check=check)
      if conf.content.lower()=='yes':
        abort = False
    except:
      pass
    if abort:
      await message.channel.send("Leaving cancelled!")
      return
    
    await message.channel.send("What wonderful times we've shared together! Goodbye, and may the Seven smile upon you.")
    for channel in g.channels:
      if 'reaper' in channel.name:
        await channel.delete()
    for category in g.categories:
      if category.name=='Reaper':
        await category.delete()
    for role in g.roles:
      if 'reaper' in role.name:
        await role.delete()
    #purge the database (if it exists)
    if g.id in cache:
      del cache[g.id]
      for key in db.keys():
        if str(g.id) in key:
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
  #random math trivia
  elif message.content == '$mathtrivia':
    quote = get_math_trivia()
    await message.channel.send(quote)
  #get a year based piece of trivia
  elif message.content.startswith('$what happened in '):
    try:
      end = len(message.content)
      if '?' in message.content:
        end = message.content.find('?')
      yr = int(message.content[18:end])
      quote = get_year(yr)
      await message.channel.send(quote)
    except:
      pass
  #get a kanye quote
  elif message.content == '$kanye':
    quote = get_kanye()
    await message.channel.send(quote)
  #get a ron swanson (parks and recreation character) quote
  elif message.content == '$ron':
    quote = get_ron()
    await message.channel.send(quote)
  #number of servers the bot is in
  elif message.content == '$servers':
    totalPeople = sum([(1 if not x.bot else 0) for x in client.users])
    await message.channel.send("The Red Crab Inn is currently in {s} servers, serving {p} people across Discord!".format(s=len(client.guilds),p=str(totalPeople)))
  #send the help box in markdown
  elif message.content.lower().startswith('$help'):
    embed = main_help(message.content.lower())
    await message.channel.send(embed=embed)
  else:
    skip = True

#My Discord Bot Token
keep_alive() #it will always be online
client.run(os.getenv('TOKEN'))
