import discord
from replit import db
from conversion import get_conversion
from conversion import networth
from leaderboard import leaderboard
from leaderboard import leaderboardEmbed
from help import crypto_help

async def crypto(message):
  server = str(message.guild.id)
  key = "CRYPTO " + server + " " + str(message.author.id) #db[key] = (dollars,bitcoins,ethereums)
  text = message.content.lower()
  response = ""

  if text == 'join':
    if key not in db.keys():
      db[key] = (1000000.0,0,0)
      response = "Hi {user}, welcome to the Red Crab Inn's Bitcoin simulator! You start with $1,000,000.".format(user=message.author.mention)
    else:
      response = "Hi {user}, you are already in the simulator!".format(user=message.author.mention)
    return response
  elif text.startswith('help'):
    embed = crypto_help(text)
    await message.channel.send(embed=embed)
    return 200
  
  if key not in db.keys():
    return ""
  
  if text=='exchange rate':
    r = get_conversion()
    response = "The current Bitcoin exchange rate is ${btc}. The current Ethereum exchange rate is ${eth}.".format(btc=r[0],eth=r[1])
  elif text.startswith('buy '):
    params = text[4:].split(' ')
    btc = 0
    eth = 0
    success = True
    r = get_conversion()
    for p in params:
      if p.startswith('btc='):
        try:
          if p=='btc=all':
            btc = db[key][0]/r[0]
          elif p.startswith('btc=$'):
            btc = float(p[5:])/r[0]
          else:
            btc = float(p[4:])
        except:
          success=False
      elif p.startswith('eth='):
        try:
          if p=='eth-all':
            eth = db[key][0]/r[1]
          elif p.startswith('eth=$'):
            eth = float(p[5:])/r[1]
          else:
            eth = float(p[4:])
        except:
          success=False
      else:
        success=False
    if btc < 0 or eth < 0:
      success = False
    if not success:
      return "Invalid use of the `buy` command!"
    
    cost = btc*r[0]+eth*r[1]
    if cost > db[key][0]:
      response = "Hi {user}, you do not have enough money to buy that much cryptocurrency!".format(user=message.author.mention)
    else:
      db[key] = (db[key][0]-cost,db[key][1]+btc,db[key][2]+eth)
      response = "Hi {user}, your transaction was successful! You now have ${cash} and ฿{btc} and Ξ{eth}.".format(user=message.author.mention,cash=db[key][0],btc=db[key][1],eth=db[key][2])
  elif text.startswith('sell '):
    params = text[5:].split(' ')
    btc = 0
    eth = 0
    r = get_conversion()
    success = True
    for p in params:
      if p.startswith('btc='):
        try:
          if p=='btc=all':
            btc = db[key][1]
          elif p.startswith('btc=$'):
            btc = float(p[5:])/r[0]
          else:
            btc = float(p[4:])
        except:
          success = False
      elif p.startswith('eth='):
        try:
          if p=='eth-all':
            eth = db[key][2]
          elif p.startswith('eth=$'):
            eth = float(p[5:])/r[1]
          else:
            eth = float(p[4:])
        except:
          success = False
      else:
        success = False
    if btc < 0 or eth < 0:
      success = False
    if not success:
      return "Invalid use of the `sell` command!"
    profit = btc*r[0]+eth*r[1]
    if btc > db[key][1] or eth > db[key][2]:
      response = "Hi {user}, you do not have enough crpytocurrency to make that sale!".format(user=message.author.mention)
    else:
      db[key] = (db[key][0]+profit,db[key][1]-btc,db[key][2]-eth)
      response = "Hi {user}, your transaction was successful! You now have ${cash} and ฿{btc} and Ξ{eth}.".format(user=message.author.mention,cash=db[key][0],btc=db[key][1],eth=db[key][2])
  elif text=='leaderboard':
    embed = leaderboardEmbed(message.guild,"CRYPTO " + server,'crypto')
    try:
      await message.channel.send(embed=embed)
    except:
      await message.channel.send("The leaderboard is empty!")
    response = 200
  elif text=='rank':
    rankList = [x[1] for x in leaderboard("CRYPTO "+server,'crypto')]
    rank = rankList.index(int(message.author.id))+1
    response = "Hi {user}, you have ${cash} and ฿{btc} and Ξ{eth}. Your current net worth is ${net}. Your current rank in the simulation is {rank} out of {total} players.".format(user=message.author.mention,cash=db[key][0],btc=db[key][1],eth=db[key][2],net=networth(key),rank=str(rank),total=str(len(rankList)))
  elif text.startswith('rank=') and len(text)>8:
    try:
      search = message.content[5:]
      #all members whose names start with "search"
      members = await message.guild.query_members(search,limit=5)
      if len(members)>0:
        for member in members:
          hisInfo = "CRYPTO " + server + " " + str(member.id)
          hisName = member.name if member.nick==None else member.nick
          #check if they're in the game or not
          try:
            response += "{name}'s current net worth is ${net}.\n".format(name=hisName,net=networth(key))
          except:
            response += hisName + " has not entered the simulation yet.\n"
      else:
        response = search+" is not in this server."
    except:
      response = "Invalid use of the rank command. Type in help for documentation."
  return response