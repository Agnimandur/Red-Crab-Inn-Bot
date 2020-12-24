#Scripts for running the AOPS game Reaper.
from replit import db
import time
from datetime import timedelta
import random

#[score,user id]
def leaderboard(guild):
  temp = []
  server = str(guild.id)
  for key in db.keys():
    if key.startswith(server):
      userID = int(key[len(server)+1:])
      temp.append([db[key][1],userID])
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
  
#keys are server id + " " + user id
#values are (time,score) tuples
#gamekey is "REAPER GAME "+server and gamevalue is (current time, time between reaps)
async def reaper(message):
  response=""
  yourID = str(message.author.id)
  author = str(message.author.name)
  server = str(message.guild.id)
  game = "REAPER GAME "+server
  yourInfo = server + " " + yourID

  currentTime = int(round(time.time() * 1000))
  admin = False
  for role in message.author.roles:
    if role.name == 'reaper-admin':
      admin = True
      break
  text = message.content.lower()
  if admin and (text.startswith('begin game ') or text=='begin game') and game not in db.keys():
    try:
      db[game] = (currentTime,float(message.content[11:]))
    except:
      db[game] = (currentTime,12)

    response = """**The game has begun!**
    - To play, simply type in reap to make your first reap!
    - The time between reaps is {between} hours.
    - For the rules and objectives, check out <https://artofproblemsolving.com/reaper>. 
    - Talk to the mods for additional information.
    """.format(between=db[game][1])
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
    rankList = leaderboard(message.guild)
    champion = 482581806143766529
    if len(rankList)>0:
      champion = rankList[0][1]

    for key in db.keys():
      if key.startswith(server):
        del db[key]
    del db[game]
    response = """**The game is over!**
    - The winner is <@{champion}>!!
    - Final standings are available in the attached file.
    - Talk to the mods for more details.
    """.format(champion=champion)
  elif text == 'reap':
    if yourInfo in db.keys() and currentTime-db[yourInfo][0] < db[game][1]*3600000:
      remaining = int(db[game][1]*3600000-(currentTime-db[yourInfo][0]))
      delta = timedelta(seconds=remaining//1000)
      response="Hi <@{author}>, please wait {delta} before reaping again.".format(author=yourID,delta=str(delta))
    else:
      score = currentTime - db[game][0]
      modifier = getmodifier()
      free = getfree()
      newScore = score*modifier
      if yourInfo in db.keys():
        newScore += db[yourInfo][1]
      newTime = currentTime
      if free:
        newTime = 0

      bonus = ""
      if modifier > 1:
        bonus = "You also got a {mod}x reap".format(mod=modifier)
        if free:
          bonus += "and a free reap!!"
        bonus += "!"
      response = "Congratulations <@{author}>, your reap earned {score} points.".format(author=message.author.id,score=score*modifier)+bonus
      db[game] = (currentTime,db[game][1])
      db[yourInfo] = (newTime,newScore)
  elif text=='timer':
    points = currentTime - db[game][0]
    response = "The current reap time is {points} milliseconds.".format(points=points)
  elif text=='leaderboard':
    rankList = leaderboard(message.guild)
    response = "**Reaper Leaderboard**\n"
    for i in range(0,min(len(rankList),10)):
      member = await message.guild.fetch_member(rankList[i][1])
      add = "{pos}. {name} with {points} points\n".format(pos=i+1,name=member.name,points=rankList[i][0])
      response += add
  elif text=='rank':
    if yourInfo not in db.keys():
      response = "Hi <@{author}>, make a reap to join the game!".format(author=yourID)
    else:
      rankList = [x[1] for x in leaderboard(message.guild)]
      rank = rankList.index(int(yourID))+1
      response = "Hi <@{author}>, your current score is {score} points. Your current rank in the game is {rank} out of {total} players.".format(author=yourID,score=db[yourInfo][1],rank=str(rank),total=str(len(rankList)))
  return response
