import discord
import math
import time
from datetime import timedelta
from replit import db
from conversion import get_conversion
from conversion import networth
from leaderboard import leaderboard
from leaderboard import leaderboardEmbed
from help import crypto_help
from help import make_embed
AGNIMANDUR = 482581806143766529

async def transaction(params,key,kind):
  ret = {'btc':0,'eth':0,'success':True,'h':24}
  r = await get_conversion()
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
      response = "Hi {user}, welcome to the Red Crab Inn's cryptocurrency simulator, where you can trade Bitcoin and Ethereum! You start with $1,000,000.".format(user=message.author.mention)
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
    r = await get_conversion()
    response = "The current Bitcoin exchange rate is ${btc}. The current Ethereum exchange rate is ${eth}.".format(btc=round(r[0]),eth=round(r[1]))
  elif text.startswith('buy '):
    params = text[4:].split(' ')
    r = await get_conversion()
    ret = await transaction(params,key,'buy')
    if not ret['success']:
      return "Invalid use of the `buy` command!"
    
    cost = ret['btc']*r[0]+ret['eth']*r[1]
    if cost > db[key][0]:
      response = "Hi {user}, you do not have enough money to buy that much cryptocurrency!".format(user=message.author.mention)
    else:
      db[key] = (db[key][0]-cost,db[key][1]+ret['btc'],db[key][2]+ret['eth'])
      response = "Hi {user}, your transaction was successful! You now have ${cash} and ฿{btc} and Ξ{eth}.".format(user=message.author.mention,cash=round(db[key][0]),btc=db[key][1],eth=db[key][2])
  elif text.startswith('sell '):
    params = text[5:].split(' ')
    r = await get_conversion()
    ret = await transaction(params,key,'sell')
    if not ret['success']:
      return "Invalid use of the `sell` command!"

    profit = ret['btc']*r[0]+ret['eth']*r[1]
    if ret['btc'] > db[key][1] or ret['eth'] > db[key][2]:
      response = "Hi {user}, you do not have enough cryptocurrency to make that sale!".format(user=message.author.mention)
    else:
      db[key] = (db[key][0]+profit,db[key][1]-ret['btc'],db[key][2]-ret['eth'])
      response = "Hi {user}, your transaction was successful! You now have ${cash} and ฿{btc} and Ξ{eth}.".format(user=message.author.mention,cash=round(db[key][0]),btc=db[key][1],eth=db[key][2])
  elif text.startswith('short'):
    params = text[6:].split(' ')
    success = True
    r = await get_conversion()
    ret = await transaction(params,key,'short')
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
      r = await get_conversion()
      temp = db[contracts]
      temp2 = []
      currentTime = round(time.time())
      cash = db[key][0]
      amts = ""
      ends = ""
      profits = ""
      for contract in temp:
        if contract[1]=='btc':
          profit = (contract[3]-r[0])*contract[2]
        else:
          profit = (contract[3]-r[1])*contract[2]
        if contract[4] <= currentTime:
          end = "none"
          cash += (contract[2]*contract[3]+profit)
        else:
          end = str(timedelta(seconds=contract[4]-currentTime))
          temp2.append(contract)
        amts += "`{symbol}{amt}`\n".format(symbol='฿' if contract[1]=='btc' else 'Ξ',amt=contract[2])
        ends += "`{end}`\n".format(end=end)
        profits += "`${profit}`\n".format(profit=round(profit))
      db[key] = (cash,db[key][1],db[key][2])
      db[contracts] = temp2

      embed = make_embed(title="**{user}'s Contracts**".format(user=message.author.name),description="A list of your ongoing contracts.").add_field(name="**Amount**",value=amts,inline=True).add_field(name="**Time Until End**",value=ends[:-1],inline=True).add_field(name="**Projected Profit**",value=profits[:-1],inline=True)
      await message.channel.send(embed=embed)
      response = 200
  elif text=='leaderboard':
    if message.author.id==AGNIMANDUR:
      embed = await leaderboardEmbed(message.guild,"CRYPTO " + server,'crypto')
      try:
        await message.channel.send(embed=embed)
      except:
        await message.channel.send("The leaderboard is empty!")
      wait = "WAIT "+str(message.author.id)
      db[wait] = round(time.time())
      response = 200
    else:
      response = "This command is temporarily unavailable."
  elif text=='net worth':
    embed = make_embed(title="**{user}'s Net Worth**".format(user=message.author.name),description="A list of your liquid assets. Use `contracts` to view your current contracts.").add_field(name="**US Dollars**",value='$'+str(round(db[key][0])),inline=True).add_field(name="**Bitcoin**",value='฿'+str(db[key][1]),inline=True).add_field(name="**Ethereum**",value='Ξ'+str(db[key][2]),inline=True)
    await message.channel.send(embed=embed)
    response = 200
  elif text=='rank':
    #board = await leaderboard("CRYPTO "+server,'crypto')
    #rankList = [x[1] for x in board]
    #rank = rankList.index(int(message.author.id))+1
    #wait = "WAIT "+str(message.author.id)
    #db[wait] = round(time.time())
    #response = "Hi {user}, you have ${cash} and ฿{btc} and Ξ{eth}. Your current net worth is ${net}. Your rank in the simulation is {r} out of {t} investors.".format(user=message.author.mention,cash=round(db[key][0]),btc=db[key][1],eth=db[key][2],net=round(nw),r=rank,t=len(rankList))
    nw = await networth(key)
    response = "Hi {user}, you have ${cash} and ฿{btc} and Ξ{eth}. Your current net worth is ${net}.".format(user=message.author.mention,cash=round(db[key][0]),btc=db[key][1],eth=db[key][2],net=round(nw))
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
            nw = await networth(hisInfo)
            response += f"{hisName}'s current net worth is ${round(nw)}.\n"
          except:
            response += hisName + " has not entered the simulation yet.\n"
      else:
        response = search+" is not in this server."
    except:
      response = "Invalid use of the rank command. Type in help for documentation."
  return response