import discord
from replit import db

def make_embed(title,description):
  return discord.Embed(color=0x71368a,title=title,description=description+"\n [Invite Me](https://discord.com/api/oauth2/authorize?client_id=791162942459478016&permissions=2080894065&scope=bot) | [Join the Discord](https://discord.gg/5bbnUz6J2a) | [Github](https://github.com/Agnimandur/Red-Crab-Inn-Bot) | [Vote on Top.gg](https://top.gg/bot/791162942459478016/vote)").set_author(name='Reaper',url='https://github.com/Agnimandur/Red-Crab-Inn-Bot',icon_url='https://i.ibb.co/tPJM6DP/reaper-logo.png').set_footer(text="Made by Agnimandur#0053",icon_url="https://i.ibb.co/fd2L46j/iron-throne-christmas.jpg")

def generic():
  #color is dark purple
  return make_embed(title="**Game Commands**",description="Get information about a specific command with help [COMMAND_NAME]. The first row are reaper-admin only commands.").add_field(name="**Begin/End the game**",value = """
  ```
- begin game [h] [p] [rng]
- begin blitz game [s] [p] [rng]
- end game```""").add_field(name="**Game parameters**",value = """
  ```
- h=[h]
- s=[s]
- rng=[rng]
- end game```""").add_field(name="**Game moderation**",value = """
  ```
- adminify [users]
- reset [users]
- ban [users]
- unban [users]
- demote [users]```""").add_field(name="**Reaping**",value="""
  ```
- reap```
  """).add_field(name="**Ingame analysis**",value="""
  ```
- timer
- nextreap=[name]
- rank=[name]
- leaderboard```
  """)

def reaper_help(text):
  if len(text)>4:
    try:
      command = str(text[5:])
      embed=None
      if command.find('blitz') >= 0:
        embed=make_embed(title="**Begin Blitz Game**",description="Begin a blitz reaper game. These games are short, so expect to play it from beginning to end! At the end, a results graph will be displayed.").add_field(name="**Parameters**",value="""
- [s]. The reap cooldown in seconds. The maximum is 500 seconds, and the minimum is 5 seconds. The default is 10 seconds.
- [p]. The point target to reap in seconds. The maximum is 5000 points, and the minimum is 10 points. The default is 120 points.
- [rng]. Either 0 or 1. If 0, then randomness (score multipliers and free reaps) is turned off.""")
      elif command.startswith('begin'):
        embed=make_embed(title="**Begin Game**",description="Begin a standard reaper game. These games are long, often taking days or even weeks.").add_field(name="**Parameters**",value="""
- [h]. The reap cooldown in hours (decimals accepted). The maximum is 1000 hours, and the minimum is 0.003 hours. The default is 12 hours.
- [p]. The point target to reap in seconds. The maximum is 10,000,000 points (almost 4 months!), and the minimum is 10 points. The default is 43200 (12 hours) points.
- [rng]. Either 0 or 1. If 0, then randomness (score multipliers and free reaps) is turned off.""")
      elif command.startswith('adminify'):
        embed=make_embed(title="**Adminify**",description="Use this command to promote new reaper-admins.").add_field(name="**Parameters**",value="""
- [users]. A list of @ed users who you want to promote.""")
      elif command.startswith('demote'):
        embed=make_embed(title="**Demote**",description="A server administrator can use this command to take away the reaper-admin role.").add_field(name="**Parameters**",value="""
- [users]. A list of @ed users who you want to demote.""")
      elif command=='reset':
        embed=make_embed(title="**Reset**",description="Use this command to reset someone's score to 0 in a game.").add_field(name="**Parameters**",value="""
- [users]. A list of @ed users whose scores you want to reset.""")
      elif command=='end game':
        embed=make_embed(title="**End game**",description="Use this command to manually end an ongoing game.").add_field(name="**Parameters**",value="*None*")
      elif command=='ban':
        embed=make_embed(title="**Ban**",description="Use this command to ban someone from the #reaper channels. You cannot ban other reaper-admins.").add_field(name="**Parameters**",value="""
- [users]. A list of @ed users to ban.""")
      elif command=='unban':
        embed=make_embed(title="**Unban**",description="Use this command to un ban someone from the #reaper channels.").add_field(name="**Parameters**",value="""
- [users]. A list of @ed users to unban.""")
      elif command=='reap':
        embed=make_embed(title="**Reap**",description="When you reap, you gain points equal to the difference between the current time and the time of the last reap! Since there is a cooldown between reaps, you have to strategically decide when the optimal time is to reap.").add_field(name="**Parameters**",value="*None*")
      elif command=='timer':
        embed=make_embed(title="**Timer**",description="Use this command to find the current point value of a reap.").add_field(name="**Parameters**",value="*None*")
      elif command.startswith('next'):
        embed=make_embed(title="**Next Reap**",description="Use this command to find the amount of time before you can next reap. Alternatively, you can find the next reap time of someone else.").add_field(name="**Parameters**",value="""
- [name]. Optional. The person whose next reap time you want to find. Defaults to yourself.""")
      elif command.startswith('rank'):
        embed=make_embed(title="**Rank**",description="Use this command to find your current rank and score in the game. Alternatively, you can find the score of someone else.").add_field(name="**Parameters**",value="""
- [name]. Optional. The person whose score you want to find. Defaults to yourself.""")
      elif command=='leaderboard':
        embed=make_embed(title="**Leaderboard**",description="This command displays the current top10 of the ongoing game.").add_field(name="**Parameters**",value="*None*")
      elif command.startswith('h'):
        embed=make_embed(title="**Hours**",description="Use this command to change the reap cooldown (in hours). This only works for standard games.").add_field(name="**Parameters**",value="""
- [h]. The new cooldown.""")
      elif command.startswith('s'):
        embed=make_embed(title="**Seconds**",description="Use this command to change the reap cooldown (in seconds). This only works for blitz games.").add_field(name="**Parameters**",value="""
- [s]. The new cooldown.""")
      elif command.startswith('p'):
        embed=make_embed(title="**Points**",description="Use this command to change the points necessary to win. Note that if someone is already at the target, they will still need to reap once to win.").add_field(name="**Parameters**",value="""
- [p]. The new points necessary to win.""")
      elif command.startswith('rng'):
        embed=make_embed(title="**Randomness**",description="Use this command to toggle randomness in the game. This will affect reap multipliers and free reaps, but not retroactively.").add_field(name="**Parameters**",value="""
- [rng]. Either 0 or 1, corresponding to no randomness or yes randomness.""")
      else:
        embed = generic()
    except:
      pass
    return embed

  return generic()
