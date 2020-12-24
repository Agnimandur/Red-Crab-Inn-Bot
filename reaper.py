#Scripts for running the AOPS game Reaper.
from replit import db
import time
from datetime import timedelta

def leaderboard(server):
  temp = []
  start = "REAPER SCORE "+server+" "
  for key in db.keys():
    if key.startswith(start):
      temp.append([db[key],key[len(start):]])
  temp.sort(reverse=True)
  return temp
  

async def reaper(message):
  response=""
  author = str(message.author.name)
  server = str(message.guild.id)
  game = "REAPER GAME "+server
  reapTime = "REAPER TIME "+server
  yourScore = "REAPER SCORE "+server+" "+author
  yourTime = "REAPER LAST "+server+" "+author
  currentTime = int(round(time.time() * 1000))


  if message.content.startswith("begin game") and game not in db.keys():
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
  if game not in db.keys():
    return response
  if message.content == "end game":
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
  elif message.content == "reap":
    if yourTime in db.keys() and currentTime-db[yourTime] < db[reapTime]*3600000:
      remaining = db[reapTime]*3600000-(currentTime-db[yourTime])
      delta = timedelta(seconds=remaining//1000)
      response="Hi <@{author}>, please wait {delta} before reaping again.".format(author=message.author.id,delta=str(delta))
    else:
      score = currentTime - db[game]
      if yourScore not in db.keys():
        db[yourScore] = 0
      db[yourScore] += score
      response = "Congratulations <@{author}>, your reap earned {score} points.".format(author=message.author.id,score=score)
      db[game] = currentTime
      db[yourTime] = currentTime
  elif message.content == "timer":
    points = currentTime - db[game]
    response = "The current reap time is {points} milliseconds.".format(points=points)
  elif message.content == "leaderboard":
    rankList = leaderboard(server)
    response = "**Reaper Leaderboard**\n"
    for i in range(0,min(len(rankList),10)):
      add = "{pos}. {name} with {points} points\n".format(pos=i+1,name=rankList[i][1],points=rankList[i][0])
      response += add
  elif message.content == "rank":
    if yourScore not in db.keys():
      response = "Hi <@{author}>, make a reap to join the game!".format(author=message.author.id)
    else:
      rankList = [x[1] for x in leaderboard(server)]
      rank = rankList.index(author)+1
      response = "Hi <@{author}>, your current score is {score} points. Your current rank in the game is {rank} out of {total} players.".format(author=message.author.id,score=db[yourScore],rank=str(rank),total=str(len(rankList)))
  elif message.content == "help":
    response = "Type **reap** to reap, and remember, there is a cooldown! Type **timer** to see the value of a reap. Type **rank** to find out your current rank on the leaderboard, and your current point total. Type **leaderboard** to see the top 10!"
  return response