import discord
from replit import db
from conversion import get_conversion
from leaderboard import leaderboard
from leaderboard import leaderboardEmbed
from help import bitcoin_help

def amount(text):
  r = get_conversion()
  try:
    btc = float(text[text.index('btc=')+4:])
    return (r*btc,btc)
  except:
    try:
      usd = float(text[text.index('usd=')+4:])
      return (usd,usd/r)
    except:
      try:
        usd = float(text)
        return (usd,usd/r)
      except:
        return (0,0)

async def bitcoin(message):
  server = str(message.guild.id)
  key = "BITCOIN " + server + " " + str(message.author.id) #db[key] = (dollars,bitcoins)
  text = message.content.lower()
  response = ""

  if text == 'join':
    if key not in db.keys():
      db[key] = (1000000.0,0)
      response = "Hi {user}, welcome to the Red Crab Inn's Bitcoin simulator! You start with $1,000,000.".format(user=message.author.mention)
    else:
      response = "Hi {user}, you are already in the simulator! You have ${cash} and ฿{bitcoin}.".format(user=message.author.mention,cash=db[key][0],bitcoin=db[key][1])
    return response
  elif text.startswith('help'):
    embed = bitcoin_help(text)
    await message.channel.send(embed=embed)
    return 200
  
  if key not in db.keys():
    return "Hi {user}, please type in join to enter the Bitcoin Simulator!".format(user=message.author.mention)
  
  if text=='exchange rate':
    response = "The current Bitcoin exchange rate is ${cash}".format(cash=get_conversion())
  elif text.startswith('buy '):
    val = amount(text[4:])
    if text=='buy all':
      val = (db[key][0],db[key][0]/get_conversion())
    if val[0] <= 0:
      return ""
    if val[0] > db[key][0]:
      response = "Hi {user}, you do not have enough money to buy that much bitcoin!".format(user=message.author.mention)
    else:
      db[key] = (db[key][0]-val[0],db[key][1]+val[1])
      response = "Hi {user}, your transaction was successful! You now have ${cash} and ฿{bitcoin}.".format(user=message.author.mention,cash=db[key][0],bitcoin=db[key][1])
  elif text.startswith('sell '):
    val = amount(text[5:])
    if text=='sell all':
      val = (db[key][1]*get_conversion(),db[key][1])
    if val[1] <= 0:
      return ""
    if val[1] > db[key][1]:
      response = "Hi {user}, you do not have enough bitcoin to sell that much!".format(user=message.author.mention)
    else:
      db[key] = (db[key][0]+val[0],db[key][1]-val[1])
      response = "Hi {user}, your transaction was successful! You now have ${cash} and ฿{bitcoin}.".format(user=message.author.mention,cash=db[key][0],bitcoin=db[key][1])
  elif text=='leaderboard':
    embed = leaderboardEmbed(message.guild,"BITCOIN " + server,'bitcoin')
    try:
      await message.channel.send(embed=embed)
    except:
      await message.channel.send("The leaderboard is empty!")
    response = 200
  elif text=='net worth':
    response = "Hi {user}, you have ${cash} and ฿{bitcoin}. Your current net worth is ${net}.".format(user=message.author.mention,cash=db[key][0],bitcoin=db[key][1],net=db[key][0]+db[key][1]*get_conversion())
  elif text=='rank':
    rankList = [x[1] for x in leaderboard("BITCOIN "+server,'bitcoin')]
    rank = rankList.index(int(message.author.id))+1
    response = "Hi {user}, you have ${cash} and ฿{bitcoin}. Your current net worth is ${net}. Your current rank in the simulation is {rank} out of {total} players.".format(user=message.author.mention,cash=db[key][0],bitcoin=db[key][1],net=db[key][0]+db[key][1]*get_conversion(),rank=str(rank),total=str(len(rankList)))
  elif text.startswith('rank=') and len(text)>8:
    try:
      search = message.content[5:]
      #all members whose names start with "search"
      members = await message.guild.query_members(search,limit=5)
      if len(members)>0:
        for member in members:
          hisInfo = "BITCOIN " + server + " " + str(member.id)
          hisName = member.name if member.nick==None else member.nick
          #check if they're in the game or not
          try:
            response += "{name}'s current net worth is ${net}.\n".format(name=hisName,net=db[hisInfo][0]+db[hisInfo][1]*get_conversion())
          except:
            response += hisName + " has not entered the simulation yet.\n"
      else:
        response = search+" is not in this server."
    except:
      response = "Invalid use of the rank command. Type in help for documentation."
  return response