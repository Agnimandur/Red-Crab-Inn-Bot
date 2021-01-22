import discord
import math
import time
from replit import db
from conversion import get_conversion
from conversion import networth
from leaderboard import leaderboard
from leaderboard import leaderboardEmbed
from help import crypto_help

def transaction(params,key,kind):
  ret = {'btc':0,'eth':0,'success':True,'h':24}
  r = get_conversion()
  for p in params:
    if p.startswith('btc='):
      try:
        if p=='btc=all':
          ret['btc'] = db[key][0]/r[0] if kind=='buy' else db[key][1]
        elif p.startswith('btc=$'):
          ret['btc'] = float(p[5:])/r[0]
        else:
          ret['btc'] = float(p[4:])
      except:
        ret['success']=False
    elif p.startswith('eth='):
      try:
        if p=='eth=all':
          ret['eth'] = db[key][0]/r[1] if kind=='buy' else db[key][2]
        elif p.startswith('eth=$'):
          ret['eth'] = float(p[5:])/r[1]
        else:
          ret['eth'] = float(p[4:])
      except:
        ret['success']=False
    elif p.startswith('h=') and kind=='short':
      try:
        ret['h'] = float(p[2:])
      except:
        success = False
    else:
      ret['success']=False
  for k in ret.keys():
    if math.isnan(ret[k]) or ret[k] < 0:
      ret['success'] = False
  return ret

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
    r = get_conversion()
    ret = transaction(params,key,'buy')
    if not ret['success']:
      return "Invalid use of the `buy` command!"
    
    cost = ret['btc']*r[0]+ret['eth']*r[1]
    if cost > db[key][0]:
      response = "Hi {user}, you do not have enough money to buy that much cryptocurrency!".format(user=message.author.mention)
    else:
      db[key] = (db[key][0]-cost,db[key][1]+ret['btc'],db[key][2]+ret['eth'])
      response = "Hi {user}, your transaction was successful! You now have ${cash} and ฿{btc} and Ξ{eth}.".format(user=message.author.mention,cash=db[key][0],btc=db[key][1],eth=db[key][2])
  elif text.startswith('sell '):
    params = text[5:].split(' ')
    r = get_conversion()
    ret = transaction(params,key,'sell')
    if not ret['success']:
      return "Invalid use of the `sell` command!"

    profit = ret['btc']*r[0]+ret['eth']*r[1]
    if ret['btc'] > db[key][1] or ret['eth'] > db[key][2]:
      response = "Hi {user}, you do not have enough cryptocurrency to make that sale!".format(user=message.author.mention)
    else:
      db[key] = (db[key][0]+profit,db[key][1]-ret['btc'],db[key][2]-ret['eth'])
      response = "Hi {user}, your transaction was successful! You now have ${cash} and ฿{btc} and Ξ{eth}.".format(user=message.author.mention,cash=db[key][0],btc=db[key][1],eth=db[key][2])
  elif text.startswith('short'):
    params = text[6:].split(' ')
    success = True
    r = get_conversion()
    ret = transaction(params,key,'short')
    if not ret['success'] or (ret['eth'] > 0 and ret['btc'] > 0):
      return "Invalid use of the `short` command!"
    contracts = "CONTRACT "+key
    if ret['btc']*r[0] > db[key][0] or ret['eth']*r[1] > db[key][0]:
      response = "Hi {user}, you do not have enough dollars for this contract!".format(user=message.author.mention)
    elif ret['h'] < 0.1 or ret['h'] > 10000:
      response = "Hi {user}, the duration of the contract must be between 0.1 and 10000 hours.".format(user=message.author.mention)
    elif contracts in db.keys() and len(db[contracts])==5:
      response = "Hi {user}, you can only have a maximum of 5 ongoing contracts at a time! Use the `contracts` command to view them.".format(user=message.author.mention)
    else:
      #place the contract ('short',currency-name ('btc'/'eth'),amt,val at open, end_time)
      endTime = round(time.time())+3600*ret['h']
      if ret['btc'] > 0:
        contract = ('short','btc',ret['btc'],r[0],endTime)
        db[key] = (db[key][0]-ret['btc']*r[0],db[key][1],db[key][2])
      else:
        contract = ('short','eth',ret['eth'],r[1],endTime)
        db[key] = (db[key][0]-ret['eth']*r[1],db[key][1],db[key][2])
      if contracts not in db.keys():
        db[contracts] = []
      temp = db[contracts]
      temp.append(contract)
      db[contracts] = temp
      response = "Hi {user}, your CFD contract for {symbol}{amt} lasting {h} hours was successfully placed! Check back on its status with the `contracts` command!".format(user=message.author.mention,symbol='฿' if contract[1]=='btc' else 'Ξ',amt=contract[2],h=ret['h'])
  elif text=='contracts':
    contracts = "CONTRACT "+key
    if contracts not in db.keys() or len(db[contracts])==0:
      response = "You have no active contracts!"
    else:
      r = get_conversion()
      temp = db[contracts]
      temp2 = []
      response = "Hi {user}, below is a list of your ongoing contracts.\n".format(user=message.author.mention)
      currentTime = round(time.time())
      cash = db[key][0]
      for contract in temp:
        if contract[1]=='btc':
          profit = (contract[3]-r[0])*contract[2]
        else:
          profit = (contract[3]-r[1])*contract[2]
        if contract[4] <= currentTime:
          end = "that has just ended"
          cash += (contract[2]*contract[3]+profit)
        else:
          end = "that will end at {t}".format(t=time.ctime(contract[4]))
          temp2.append(contract)
        response += "1. A CFD for {symbol}{amt} {end} with a profit of ${profit}.\n".format(symbol='฿' if contract[1]=='btc' else 'Ξ',amt=contract[2],end=end,profit=profit)
      db[key] = (cash,db[key][1],db[key][2])
      db[contracts] = temp2
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
            response += "{name}'s current net worth is ${net}.\n".format(name=hisName,net=networth(hisInfo))
          except:
            response += hisName + " has not entered the simulation yet.\n"
      else:
        response = search+" is not in this server."
    except:
      response = "Invalid use of the rank command. Type in help for documentation."
  return response