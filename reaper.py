#Scripts for running the AOPS game Reaper.
import discord
from replit import db
import time
from datetime import timedelta
from graph import graph
from help import reaper_help
from help import make_embed
from random import randint

#default parameters
H = 12 #12 hours between reaps
P = 43200 #first to reap 12 hours
BS = 10 #10 seconds between reaps
BP = 120 #first to reap 2 minutes
AGNIMANDUR = 482581806143766529
cache = {} #guild id to a tuple of (reaper-admin role, banned-from-reaper role)

#send the reaper logo
async def sendLogo(channel):
  await channel.send(file=discord.File("reaper.png"))

#build the leaderboard
def leaderboard(guild):
  temp = []
  server = str(guild.id)
  for key in db.keys():
    if key.startswith(server):
      #[score,user id]
      userID = int(key[len(server)+1:])
      temp.append([db[key][1],userID])
  temp.sort(reverse=True)
  return temp
def leaderboardEmbed(guild):
  rankList = leaderboard(guild)
  if len(rankList)==0:
    return None
  ranks = ""
  names = ""
  points = ""
  i = 0
  for person in rankList:
    if i==min(len(rankList),10):
      break
    #skip people who aren't in the server anymore
    member = guild.get_member(person[1])
    if member==None:
      continue
    ranks += "`{pos}.`\n".format(pos=i+1)
    names += "`{name}`\n".format(name=member.nick if member.nick != None else member.name)
    points += "`{points}`\n".format(points=person[0])
    i += 1
  embed = make_embed(title="**Leaderboard**",description="Top 10 reaper leaderboard. The target to win is **{p}** points.".format(p=db["REAPER GAME "+str(guild.id)][2])).add_field(name="**Rank**",value=ranks,inline=True).add_field(name="**Players**",value=names,inline=True).add_field(name="**Points**",value=points,inline=True)
  return embed

#determine the modifier to the score (odds provided by kevinmathz)
def getmodifier(game):
  if db[game][3]==0:
    return 1
  d1000 = randint(1,1000)
  if d1000 <= 100:
    return 2
  elif d1000 <= 150:
    return 3
  elif d1000 <= 180:
    return 4
  elif d1000 <= 199:
    return 5
  elif d1000 <= 200:
    return 8
  else:
    return 1

#is this a free reap?
def getfree(game):
  if db[game][3]==0:
    return False
  return (randint(1,50)==1)

#the begin game message (can be edited later on)
def openingcrawl(game):
  mode = "blitz" if "BLITZ "+game in db.keys() else "standard"
  unit = "seconds" if mode=='blitz' else "hours"
  between = int(3600*db[game][1]) if mode=='blitz' else db[game][1]
  status = "ENABLED" if db[game][3]==1 else "DISABLED"
  return """**The game has begun!**
    - To play, simply type in reap to make your first reap!
    - For the rules and objectives, check out 
    <https://artofproblemsolving.com/reaper>.
    - The time between reaps is {between} {unit}.
    - Reap {delta} ({win} points) to win!
    - This is a {mode} game.
    - Reap modifiers are {status}.
    - Talk to the mods for additional information.
    """.format(between=between,unit=unit,delta=str(timedelta(seconds=db[game][2])),win=db[game][2],mode=mode,status=status)

#End the game
async def endgame(message):
  server = str(message.guild.id)
  game = "REAPER GAME "+server
  blitz = True if "BLITZ "+game in db.keys() else False

  rankList = leaderboard(message.guild)
  embed = leaderboardEmbed(message.guild)
  champion = AGNIMANDUR
  if len(rankList)>0:
    champion = rankList[0][1]

  #clear the database of this game's keys
  for key in db.keys():
    if key.startswith(server):
      del db[key]
  del db[game]

  #create a file for final results
  result = "results/RESULTS"+server+".txt"
  f = open(result,"w+")
  f.write(message.guild.name + " Final Standings: \n")
  for person in rankList:
    member = message.guild.get_member(person[1])
    if member != None:
      f.write(member.name + "#" + member.discriminator + " with " + str(person[0]) + " points\n")
  f.close()

  response = """**The game has ended!**
  - The winner is <@{champion}>!!
  - Final standings are available in the attached file.
  - Talk to the mods for more details.
  """.format(champion=champion)
  
  files = [discord.File(result,filename=message.guild.name + " Final Standings.txt")]

  if blitz:
    events = db["BLITZ "+game]
    del db["BLITZ "+game]
    top = []
    for i in range(0,min(5,len(rankList))):
      top.append(rankList[i][1])
    image = graph(events,message.guild,top)
    files.append(image)

  #send the message and files
  m = await message.channel.send(content=response,files=files,embed=embed)
  try:
    await m.pin()
  except:
    print(m.guild.name + " doesn't have pin privileges")
  
  pinned = await message.channel.pins()
  i = len(pinned)-1
  while i > 30:
    await pinned[i].unpin()
    i -= 1

#The amount of time before you can reap again
def canreap(currentTime,yourID,guild):
  yourInfo = str(guild.id) + " " + str(yourID)
  game = "REAPER GAME " + str(guild.id)
  if yourInfo not in db.keys() or currentTime-db[yourInfo][0] >= db[game][1]*3600000:
    return ""
  else:
    remaining = int(db[game][1]*3600000-(currentTime-db[yourInfo][0]))
    delta = timedelta(seconds=remaining//1000)
    return str(delta)

def find(text,i):
  f = text.find(' ',i)
  if f==-1:
    return None
  else:
    return f

#admin role, banned role
def role_cache(guild):
  if guild.id not in cache:
    admin = None
    banned = None
    for r in guild.roles:
      if r.name=='reaper-admin':
        admin = r
      elif r.name=='banned-from-reaper':
        banned = r
    cache[guild.id] = (admin,banned)
  return cache[guild.id]


#keys are server id + " " + user id
#values are (time,score) tuples
#gamekey is "REAPER GAME "+server and gamevalue is (current time, time between reaps, points to win, begin-game-message-id)
async def reaper(message):
  #senders info
  response=""
  yourID = str(message.author.id)
  author = message.author.name if message.author.nick == None else message.author.nick
  server = str(message.guild.id)
  channel = message.channel.name
  game = "REAPER GAME "+server
  blitz = True if "BLITZ "+game in db.keys() else False
  yourInfo = server + " " + yourID
  roles = role_cache(message.guild)

  #get the time
  currentTime = int(round(time.time() * 1000))

  #check if the user is an admin
  admin = roles[0] in message.author.roles
  #Reaper Test Server Only1
  if message.guild.id==791479138447917076:
    admin = True
  
  #content of the user's message
  text = message.content.lower()

  #begin the game (check parameters)
  if (text.startswith('begin game') or text.startswith('begin blitz game')) and game not in db.keys() and channel=='reaper':
    if not admin:
      return "Hi {author}, you need to be a reaper-admin to begin a game.".format(author=message.author.mention),False
    blitz = True if text.find('blitz') >= 0 else False
    cooldown = H
    towin = P
    random = 1
    if blitz:
      cooldown = BS
      towin = BP
    hi = text.find('h=')
    si = text.find('s=')
    pi = text.find('p=')
    rngi = text.find('rng=')

    try:
      hours = float(text[hi+2:find(text,hi)])
      if not blitz:
        cooldown = min(max(hours,0.003),1000)
    except:
      pass

    try:
      seconds = int(text[si+2:find(text,si)])
      if blitz:
        cooldown = min(max(seconds,5),500)
    except:
      pass
    
    try:
      points = int(text[pi+2:find(text,pi)])
      towin = max(points,10)
      if blitz:
        towin = min(points,5000)
      else:
        towin = min(points,10000000)
    except:
      pass
    
    try:
      random = int(text[rngi+4:find(text,rngi)])
      if 0 <= random <= 1:
        pass
      else:
        error=1//0
    except:
      pass

    if blitz:
      cooldown = cooldown/3600
    db[game] = (currentTime,cooldown,towin,random,0)
    if blitz:
      db["BLITZ "+game] = [currentTime]
    await sendLogo(message.channel)
    return openingcrawl(game),True
  #demote an admin
  elif text.startswith('demote') and (message.author.id==AGNIMANDUR or message.author.guild_permissions.administrator):
    try:
      for member in message.mentions:
        await member.remove_roles(roles[0])
      response = "User{plural} sucessfully demoted!".format(plural='' if len(message.mentions)==1 else 's')
    except:
      response = "There was a failure in demotion 🙁."
  #promote to reaper-admin
  elif text.startswith('adminify') and (admin or message.author.guild_permissions.administrator) and len(message.mentions)>0:
    try:
      for member in message.mentions:
        await member.add_roles(roles[0])
      response = "User{plural} sucessfully promoted to reaper-admin!".format(plural='' if len(message.mentions)==1 else 's')
    except:
      response = "There was a failure in promotion 🙁."
  elif text.startswith('ban') and (admin or message.author.guild_permissions.administrator) and len(message.mentions)>0:
    try:
      x = 0
      for member in message.mentions:
        if roles[0] not in member.roles:
          await member.add_roles(roles[1])
          x += 1
      if x > 0:
        response = "Banning successful. If you'd like to appeal, complain to an admin."
      else:
        response = "You can't ban a reaper-admin!"
    except:
      response = "Banning failed. Do it manually if necessary."
  elif text.startswith('unban') and (admin or message.author.guild_permissions.administrator) and len(message.mentions)>0:
    try:
      for member in message.mentions:
        await member.remove_roles(roles[1])
      response = "Unbanning successful!"
    except:
      response = "Unbanning failed. Do it manually if necessary."
  elif text.startswith('help'):
    embed = reaper_help(text)
    await message.channel.send(embed=embed)
  if game not in db.keys():
    return response,False

  #These commands only work in ongoing games
  #end the game
  if text == 'end game' and admin and channel=='reaper':
    await endgame(message)
  #change the number of hours between reaps or the points needed to win (try/except statements to check valid inputs)
  #update the database (tuples are immutable!)
  elif text.startswith('h=') and admin and channel=='reaper' and not blitz:
    try:
      cooldown = min(max(float(text[2:]),0.003),1000)
      db[game] = (db[game][0],cooldown,db[game][2],db[game][3],db[game][4])
      response = "Reap cooldown updated to {h} hours.".format(h=cooldown)
      beginMessage = await message.channel.fetch_message(db[game][4])
      if beginMessage != None:
        await beginMessage.edit(content=openingcrawl(game))
    except:
      pass
  elif text.startswith('s=') and admin and channel=='reaper' and blitz:
    try:
      cooldown = min(max(int(text[2:]),5),500)
      db[game] = (db[game][0],cooldown/3600,db[game][2],db[game][3],db[game][4])
      response = "Reap cooldown updated to {s} seconds.".format(s=cooldown)
      beginMessage = await message.channel.fetch_message(db[game][4])
      if beginMessage != None:
        await beginMessage.edit(content=openingcrawl(game))
    except:
      pass
  elif text.startswith('p=') and admin and channel=='reaper':
    try:
      towin = max(10,int(text[2:]))
      if blitz:
        towin = min(towin,5000)
      db[game] = (db[game][0],db[game][1],towin,db[game][3],db[game][4])
      response = "Points to win updated to {p} points.".format(p=towin)
      beginMessage = await message.channel.fetch_message(db[game][4])
      if beginMessage != None: 
        await beginMessage.edit(content=openingcrawl(game))
    except:
      pass
  elif text.startswith('rng=') and admin and channel=='reaper':
    try:
      random = int(text[4:])
      if 0 <= random <= 1:
        pass
      else:
        error=1//0
      db[game] = (db[game][0],db[game][1],db[game][2],random,db[game][4])
      response = "Randomness has been {status}.".format(status="ENABLED" if random==1 else "DISABLED")
      beginMessage = await message.channel.fetch_message(db[game][4])
      if beginMessage != None: 
        await beginMessage.edit(content=openingcrawl(game))
    except:
      pass
  elif text.startswith('reset') and admin and len(message.mentions)>0:
    for member in message.mentions:
      hisInfo = server + " " + str(member.id)
      if hisInfo in db.keys():
        db[hisInfo] = (0,0)
    response = "Reset successfully completed!"
  #find your next reap time
  elif text == 'nextreap':
    nextReap = canreap(currentTime,yourID,message.guild)
    if len(nextReap) == 0:
      response = "Hi <@{author}>, your reap is not on cooldown!".format(author=yourID)
    else:
      response = "Hi <@{author}>, you need to wait {delta} before you can next reap.".format(author=yourID,delta=nextReap)
  elif text.startswith('nextreap='):
    try:
      name = str(text[9:])
      members = await message.guild.query_members(name,limit=5)
      for m in members:
        nextReap = canreap(currentTime,m.id,message.guild)
        if len(nextReap) == 0:
          response += "{name}\'s reap is not on cooldown!\n".format(name=m.name)
        else:
          response += "{name} needs to wait {delta} until their next reap.\n".format(name=m.name,delta=nextReap)
    except:
      response = "Invalid use of the nextreap command. Type in help for documentation."
  #reap!
  elif text.startswith('reap') and len(text) <= 6 and channel=='reaper':
    #can't reap
    nextReap = canreap(currentTime,yourID,message.guild)
    if len(nextReap) > 0:
      response="Hi <@{author}>, please wait {delta} before reaping again.".format(author=yourID,delta=nextReap)
    else:
      #get scoring info
      modifier = getmodifier(game)
      free = getfree(game)
      score = (modifier*(currentTime - db[game][0]))//1000
      newScore = score
      if yourInfo in db.keys():
        newScore += db[yourInfo][1]
      newTime = 0 if free else currentTime
      
      #send results
      bonus = ""
      if modifier > 1:
        bonus = "You also got a {mod}x reap".format(mod=modifier)
        if free:
          bonus += " and a free reap!!"
        bonus += "!"
      await message.channel.send("Congratulations <@{author}>, your reap earned {score} points.".format(author=message.author.id,score=score)+bonus)

      #update database with your time and score
      try:
        db[game] = (currentTime,db[game][1],db[game][2],db[game][3],db[game][4])
        db[yourInfo] = (newTime,newScore)
        if blitz:
          events = db["BLITZ "+game]
          events.append([currentTime,newScore,int(yourID)])
          db["BLITZ "+game] = events
        response = ""
        #check for a winner
        if newScore >= db[game][2]:
          await endgame(message)
      except:
        pass
  #get the current reap time
  elif text=='timer':
    points = (currentTime - db[game][0])//1000
    response = "The current reap time is {points} seconds.".format(points=points)
  #print out a top10 current leaderboard
  elif text=='leaderboard':
    rankList = leaderboard(message.guild)
    embed = leaderboardEmbed(message.guild)
    try:
      await message.channel.send(embed=embed)
    except:
      await message.channel.send("The leaderboard is empty!")
  #get your rank
  elif text=='rank':
    if yourInfo not in db.keys():
      response = "Hi <@{author}>, make a reap to join the game!".format(author=yourID)
    else:
      rankList = [x[1] for x in leaderboard(message.guild)]
      rank = rankList.index(int(yourID))+1
      response = "Hi <@{author}>, your current score is {score} points. Your current rank in the game is {rank} out of {total} players.".format(author=yourID,score=db[yourInfo][1],rank=str(rank),total=str(len(rankList)))
  #find the scores of other people
  elif text.startswith('rank=') and len(text)>8:
    try:
      search = message.content[5:]
      #all members whose names start with "search"
      members = await message.guild.query_members(search,limit=5)
      if len(members)>0:
        for member in members:
          hisInfo = server + " " + str(member.id)
          hisName = member.name if member.nick==None else member.nick
          #check if they're in the game or not
          try:
            response += "{name} currently has {score} points.\n".format(name=hisName,score=db[hisInfo][1])
          except:
            response += hisName + " has not reaped in this game yet.\n"
      else:
        response = search+" is not in this server."
    except:
      response = "Invalid use of the rank command. Type in help for documentation."
  return response,False
