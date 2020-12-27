import os
os.environ['MPLCONFIGDIR'] = "C:/Users/Reaper/Pictures/RCI"
import matplotlib.pyplot as plt
import discord

def graph(events,guild):
  startTime = events[0]
  del events[0]
  for i in range(0,len(events)):
    events[i][0] = (events[i][0]-startTime)/1000
  events.sort()

  dx = {}
  dy = {}
  players = []
  for e in events:
    if e[2] not in dx:
      dx[e[2]] = [0]
      dy[e[2]] = [0]
      players.append(e[2])
    dx[e[2]].append(e[0])
    dy[e[2]].append(e[1])

  for p in players:
    member = guild.get_member(p)
    if member != None:
      name = member.name+"#"+member.discriminator
      plt.plot(dx[p],dy[p],label=name)
  plt.xlabel("Time")
  plt.ylabel("Score")
  plt.legend()
  image = "RG"+str(guild.id)+".png"
  plt.savefig(image)
  plt.close()

  return discord.File(image,filename=guild.name + " Results Graph.png")
  