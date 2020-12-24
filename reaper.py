#Scripts for running the AOPS game Reaper.
from replit import db
import time
from datetime import timedelta
import random

def leaderboard(server):
  temp = []
  start = "REAPER SCORE "+server+" "
  for key in db.keys():
    if key.startswith(start):
      temp.append([db[key],key[len(start):]])
  temp.sort(reverse=True)
  return temp

def getmodifier():
  d1000 = random.randint(1,1000)
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

def getfree():
  return random.randint(1,50)==1
  

async def reaper(message):
  response=""
  author = str(message.author.name)
  server = str(message.guild.id)
  game = "REAPER GAME "+server
  reapTime = "REAPER TIME "+server
  yourScore = "REAPER SCORE "+server+" "+author
  yourTime = "REAPER LAST "+server+" "+author
  currentTime = int(round(time.time() * 1000))
  admin = False
  for role in message.author.roles:
    if role.name == 'reaper-admin':
      admin = True
      break
  text = message.content.lower()
  if admin and text=='begin game' and game not in db.keys():
    db[game] = currentTime
    try:
      db[reapTime] = int(message.content[10:])
    except:
      db[reapTime] = 12
    response = """**The game has begun!**
    - To play, simply type in reap to make your first reap!
    - The time between reaps is {between} hours.
    - For the rules and objectives, check out <https://artofproblemsolving.com/reaper>. 
    - Talk to the mods for additional information.
    """.format(between=db[reapTime])
    return response
  elif text == 'help':
    response = """
    ```
Admin:
  begin game [h]     Begin the game of reaper with a reap cooldown of [h] hours.
  end game           End the game manually.
    
Contestant (these only work in the #reaper channel):
  reap               Anyone can Reap and gain points! There is a cooldown.
  timer              The current value of a reap.
  rank               Your current rank in the ongoing game.
  leaderboard        The current top 10 leaderboard.
    ```
    """
  if game not in db.keys():
    return response
  if admin and text == 'end game':
    rankList = leaderboard(server)
    champion = 482581806143766529
    if len(rankList)>0:
      champion = await message.guild.query_members(rankList[0][1])
      champion = champion[0].id

    for key in db.keys():
      if key.startswith("REAPER SCORE "+server+" ") or key.startswith("REAPER LAST "+server+" "):
        del db[key]
    del db[game]
    del db[reapTime]
    response = """**The game is over!**
    - The winner is <@{champion}>!!
    - Final standings are available in the attached file.
    - Talk to the mods for more details.
    """.format(champion=champion)
  elif text == 'reap':
    if yourTime in db.keys() and currentTime-db[yourTime] < db[reapTime]*3600000:
      remaining = db[reapTime]*3600000-(currentTime-db[yourTime])
      delta = timedelta(seconds=remaining//1000)
      response="Hi <@{author}>, please wait {delta} before reaping again.".format(author=message.author.id,delta=str(delta))
    else:
      score = currentTime - db[game]
      modifier = getmodifier()
      free = getfree()
      if yourScore not in db.keys():
        db[yourScore] = 0
      db[yourScore] += modifier*score
      bonus = ""
      if modifier > 1:
        bonus = "You also got a {mod}x reap".format(mod=modifier)
        if free:
          bonus += "and a free reap!!"
        bonus += "!"
      response = "Congratulations <@{author}>, your reap earned {score} points.".format(author=message.author.id,score=score)+bonus
      db[game] = currentTime
      if not free:
        db[yourTime] = currentTime
  elif text=='timer':
    points = currentTime - db[game]
    response = "The current reap time is {points} milliseconds.".format(points=points)
  elif text=='leaderboard':
    rankList = leaderboard(server)
    response = "**Reaper Leaderboard**\n"
    for i in range(0,min(len(rankList),10)):
      add = "{pos}. {name} with {points} points\n".format(pos=i+1,name=rankList[i][1],points=rankList[i][0])
      response += add
  elif text=='rank':
    if yourScore not in db.keys():
      response = "Hi <@{author}>, make a reap to join the game!".format(author=message.author.id)
    else:
      rankList = [x[1] for x in leaderboard(server)]
      rank = rankList.index(author)+1
      response = "Hi <@{author}>, your current score is {score} points. Your current rank in the game is {rank} out of {total} players.".format(author=message.author.id,score=db[yourScore],rank=str(rank),total=str(len(rankList)))
  return response
