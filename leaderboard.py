from replit import db
import discord
from conversion import get_conversion
from conversion import networth
from help import make_embed

#build the leaderboard
def leaderboard(prefix,game):
  temp = []
  r = get_conversion()
  for key in db.keys():
    if key.startswith(prefix):
      #[score,user id]
      score = db[key][1] if game=='reaper' else networth(key)
      userID = int(key[len(prefix)+1:])
      temp.append([score,userID])
  temp.sort(reverse=True)
  return temp

def leaderboardEmbed(guild,prefix,game):
  rankList = leaderboard(prefix,game)
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
  description = "Top 10 reaper leaderboard. The target to win is **{p}** points.".format(p=db["REAPER GAME "+prefix][2]) if game=='reaper' else "Top 10 cryptocurrency investors leaderboard."
  denoteNames = "**Players**" if game=='reaper' else "**Investors**"
  denotePoints = "**Points**" if game=='reaper' else "**Total Money**"

  embed = make_embed(title="**Leaderboard**",description=description).add_field(name="**Rank**",value=ranks,inline=True).add_field(name=denoteNames,value=names,inline=True).add_field(name=denotePoints,value=points,inline=True)
  return embed