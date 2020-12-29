import os
os.environ['MPLCONFIGDIR'] = "C:/Users/Reaper/Pictures/RCI"
import matplotlib.pyplot as plt
import discord

def graph(events,guild,top):
  startTime = events[0]
  del events[0]
  for i in range(0,len(events)):
    events[i][0] = (events[i][0]-startTime)/1000
  events.sort()
  dx = [[0] for i in range(0,len(top))]
  dy = [[0] for i in range(0,len(top))]
  for e in events:
    i = top.index(e[2])
    dx[i].append(e[0])
    dy[i].append(e[1])

  for p in top:
    member = guild.get_member(p)
    if member != None:
      name = member.name+"#"+member.discriminator
      i = top.index(p)
      plt.plot(dx[i],dy[i],label=name)
  plt.xlabel("Time")
  plt.ylabel("Score")
  if len(top)>0:
    plt.legend()
  image = "RG"+str(guild.id)+".png"
  plt.savefig(image)
  plt.close()

  return discord.File(image,filename=guild.name + " Results Graph.png")
  