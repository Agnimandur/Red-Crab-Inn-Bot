import discord
from replit import db

def make_embed(title,description):
  #color is dark purple
  return discord.Embed(color=0x71368a,title=title,description=description+"\n[Invite Me](https://discord.com/api/oauth2/authorize?client_id=791162942459478016&permissions=2080894065&scope=bot) | [Join the Discord](https://discord.gg/5bbnUz6J2a) | [Github](https://github.com/Agnimandur/Red-Crab-Inn-Bot) | [Vote on Top.gg](https://top.gg/bot/791162942459478016/vote)").set_author(name='Reaper',url='https://github.com/Agnimandur/Red-Crab-Inn-Bot',icon_url='https://i.ibb.co/tPJM6DP/reaper-logo.png').set_footer(text="Made by Agnimandur#0053",icon_url="https://i.ibb.co/fd2L46j/iron-throne-christmas.jpg")

def reaper_generic():
  return make_embed(title="**Game Commands**",description="Get information about a specific command with help [COMMAND_NAME]. The first row are reaper-admin only commands.").add_field(name="**Begin/End the game**",value = """
  ```
- begin game h=[h] p=[p] rng=[rng]
- begin blitz game s=[s] p=[p] rng=[rng]
- end game```""").add_field(name="**Game parameters**",value = """
  ```
- h=[h]
- s=[s]
- rng=[rng]```""").add_field(name="**Game moderation**",value = """
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
- leaderboard (admin only)```
  """)

def crypto_generic():
  return make_embed(title="**Cryptocurrency Simulator Commands**",description="Buy and sell bitcoin and ethereum at current market rates! Get information about a specific command with help [COMMAND_NAME].").add_field(name="**Make a transaction**",value = """
  ```
- buy btc=[btc] eth=[eth]
- sell btc=[btc] eth=[eth]
- short [cur]=[amt] h=[h]```""").add_field(name="**Simulation**",value = """
  ```
- join
- exchange rate
- leaderboard (admin only)
- rank=[name]
- net worth
- contracts```""")

def main_generic():
  return make_embed(title="Miscellaneous Commands",description="These are commands for setting up the Reaper game, and for other miscellaneous things. All these commands have a **$** prefix. Get information about a specific command with $help [COMMAND_NAME]. For reaper game commands, go to the #reaper channel.").add_field(name="**Reaper Related**",value="""
  ```
- $reaper
- $leave```""").add_field(name="**Miscellaneous Commands**",value="""
  ```
- $quote
- $trump
- $kanye
- $ron
- $what happened in [yr]
- $mathtrivia
- $servers```""")

def main_help(text):
  embed = main_generic()
  if len(text)==5:
    return embed
  try:
    command = text[6:]
    if 'reaper' in command:
      embed=make_embed(title="**Reaper**",description="Initialize the Reaper channels and roles in your server.")
    elif 'leave' in command:
      embed=make_embed(title="**Leave**",description="Remove the Red Crab Inn bot and all associated roles and channels from your server. All history **will be lost**!")
    elif 'quote' in command or 'trump' in command or 'kanye' in command or 'ron' in command:
      embed=make_embed(title="**Fetch a Quote**",description="Fetch a quote from one of several sources.").add_field(name="**Commands**",value="""
- $quote. Get an inspirational quote and its author! [API](https://zenquotes.io)
- $trump. Get some Donald Trump nostalgia. All quotes from before he became president. [API 1](https://tronalddump.io), [API 2](https://api.whatdoestrumpthink.com)
- $kanye. Get a Kanye West quote. [API](https://api.kanye.rest/)
- $ron. Get a Ron Swanson (Parks and Recreation character) quote. [API](http://ron-swanson-quotes.herokuapp.com)""")
    elif 'servers' in command:
      embed=make_embed(title="**Server Statistics**",description="Get the number of servers the bot is in, and the total number of humans in those servers.")
    elif 'mathtrivia' in command:
      embed=make_embed(title="**Math Trivia**",description="Get mathematical trivia about a natural number!")
    elif 'what happened' in command:
      embed=make_embed(title="**What Happened In?**",description="Find out what happened in a certain year. Type this out like: $what happened in 1066?").add_field(name="**Parameters**",value="""
- [yr]. The year you want to find out what happened in. Make this a negative number for BC dates.""")
  except:
    pass
  return embed

def reaper_help(text):
  embed = reaper_generic()
  if len(text)==4:
    return embed
  try:
    command = text[5:]
    if 'blitz' in command:
      embed=make_embed(title="**Begin Blitz Game**",description="Begin a blitz reaper game. These games are short, so expect to play it from beginning to end! At the end, a results graph will be displayed.").add_field(name="**Parameters**",value="""
- [s]. The reap cooldown in seconds. The maximum is 500 seconds, and the minimum is 5 seconds. The default is 10 seconds.
- [p]. The point target to reap in seconds. The maximum is 5000 points, and the minimum is 10 points. The default is 120 points.
- [rng]. Either 0 or 1. If 0, then randomness (score multipliers and free reaps) is turned off.""").add_field(name="**Examples**",value="""
- begin blitz game s=20 p=120 rng=0
- begin blitz game p=500 s=5""")
    elif command.startswith('begin'):
      embed=make_embed(title="**Begin Game**",description="Begin a standard reaper game. These games are long, often taking days or even weeks.").add_field(name="**Parameters**",value="""
- [h]. The reap cooldown in hours (decimals accepted). The maximum is 1000 hours, and the minimum is 0.003 hours. The default is 12 hours.
- [p]. The point target to reap in seconds. The maximum is 10,000,000 points (almost 4 months!), and the minimum is 10 points. The default is 43200 (12 hours) points.
- [rng]. Either 0 or 1. If 0, then randomness (score multipliers and free reaps) is turned off.""").add_field(name="**Examples**",value="""
- begin game h=20 p=640000
- begin game h=13.4 rng=0 p=10000""")
    elif command.startswith('adminify'):
      embed=make_embed(title="**Adminify**",description="Promote new reaper-admins.").add_field(name="**Parameters**",value="""
- [users]. A list of @ed users who you want to promote.""")
    elif command.startswith('demote'):
      embed=make_embed(title="**Demote**",description="A server administrator can use this command to take away the reaper-admin role.").add_field(name="**Parameters**",value="""
- [users]. A list of @ed users who you want to demote.""")
    elif command=='reset':
      embed=make_embed(title="**Reset**",description="Reset someone's score to 0 in a game.").add_field(name="**Parameters**",value="""
- [users]. A list of @ed users whose scores you want to reset.""")
    elif command=='end game':
      embed=make_embed(title="**End game**",description="Manually end an ongoing game.").add_field(name="**Parameters**",value="*None*")
    elif command=='ban':
      embed=make_embed(title="**Ban**",description="Ban someone from the #reaper channels. The ban is permanent until they get unbanned. You cannot ban other reaper-admins.").add_field(name="**Parameters**",value="""
- [users]. A list of @ed users to ban.""")
    elif command=='unban':
      embed=make_embed(title="**Unban**",description="Unban someone from the #reaper channels.").add_field(name="**Parameters**",value="""
- [users]. A list of @ed users to unban.""")
    elif command=='reap':
      embed=make_embed(title="**Reap**",description="When you reap, you gain points equal to the difference between the current time and the time of the last reap! Since there is a cooldown between reaps, you have to strategically decide when the optimal time is to reap.").add_field(name="**Parameters**",value="*None*")
    elif command=='timer':
      embed=make_embed(title="**Timer**",description="Find the current point value of a reap.").add_field(name="**Parameters**",value="*None*")
    elif command.startswith('next'):
      embed=make_embed(title="**Next Reap**",description="Find the amount of time before you can next reap. Alternatively, you can find the next reap time of someone else.").add_field(name="**Parameters**",value="""
- [name]. Optional. The person whose next reap time you want to find. Defaults to yourself.""")
    elif command.startswith('rank'):
      embed=make_embed(title="**Rank**",description="Find your current rank and score in the game. Alternatively, you can find the score of someone else. This is an **expensive** command, meaning that you will be blocked from sending messages for another 20 seconds.").add_field(name="**Parameters**",value="""
- [name]. Optional. The person whose score you want to find (must be at least 4 characters long). Defaults to yourself.""")
    elif command=='leaderboard':
      embed=make_embed(title="**Leaderboard**",description="Diaplay the current top10 of the ongoing game in a leaderboard format. This is an **expensive** command, meaning that you will be blocked from sending messages for another 20 seconds.").add_field(name="**Parameters**",value="*None*")
    elif command.startswith('h'):
      embed=make_embed(title="**Hours**",description="Change the reap cooldown (in hours). This only works for standard games.").add_field(name="**Parameters**",value="""
- [h]. The new cooldown.""")
    elif command.startswith('s'):
      embed=make_embed(title="**Seconds**",description="Change the reap cooldown (in seconds). This only works for blitz games.").add_field(name="**Parameters**",value="""
- [s]. The new cooldown.""")
    elif command.startswith('p'):
      embed=make_embed(title="**Points**",description="Change the points necessary to win. Note that if someone is already at the target, they will still need to reap once to win.").add_field(name="**Parameters**",value="""
- [p]. The new points necessary to win.""")
    elif command.startswith('rng'):
      embed=make_embed(title="**Randomness**",description="Toggle randomness in the game. This will affect reap multipliers and free reaps, but not retroactively.").add_field(name="**Parameters**",value="""
- [rng]. Either 0 or 1, corresponding to whether randomness is off or on.""")
  except:
    pass
  return embed

def crypto_help(text):
  embed = crypto_generic()
  if len(text)==4:
    return embed
  try:
    command = text[5:]
    if command.startswith('buy'):
      embed=make_embed(title="**Buy Cryptocurrency**",description="Buy some amount of cryptocurrency at current exchange rates. The bot will inform you if you don't have enough money. You can use the all keyword to buy as much of one cryptocurrency as possible. Including a dollar sign at the beginning of an input will make the bot automatically convert the US dollar amount into the cryptocurrency in question.").add_field(name="**Parameters**",value="""
- [btc]. The amount of Bitcoin to buy.
- [eth]. The amount of Ethereum to buy.""").add_field(name="**Examples**",value="""
- buy btc=0.1. This would buy ฿0.1.
- buy btc=1 eth=1. This would buy ฿1 and Ξ1.
- buy btc=all. This would buy as much bitcoin as possible.
- buy btc=$35000. This would buy $35000 worth of bitcoin.""")
    elif command.startswith('sell'):
      embed=make_embed(title="**Sell Cryptocurrency**",description="Sell some amount of cryptocurrency at current exchange rates. The bot will inform you if you don't have enough of a given currency. You can use the all keyword to sell all of a given cryptocurrency. Including a dollar sign at the beginning of an input will make the bot automatically convert the US dollar amount into the cryptocurrency in question.").add_field(name="**Parameters**",value="""
- [btc]. The amount of Bitcoin to sell.
- [eth]. The amount of Ethereum to sell.""").add_field(name="**Examples**",value="""
- sell btc=0.1. This would sell ฿0.1.
- sell btc=1 eth=1. This would sell ฿1 and Ξ1.
- sell btc=all eth=5. This would sell all your bitcoin and Ξ5.
- sell btc=$35000. This would sell $35000 worth of bitcoin.""")
    elif command=='leaderboard':
      embed=make_embed(title="**Leaderboard**",description="Diaplay the current top10 richest investors in the ongoing Bitcoin simulation. This is an **expensive** command, meaning that you will be blocked from sending messages for another 20 seconds.").add_field(name="**Parameters**",value="*None*")
    elif command=='join':
      embed=make_embed(title="**Join**",description="Join the bitcoin simulation. You start with a million dollars.").add_field(name="**Parameters**",value="*None*")
    elif command.find('rate') >= 0:
      embed=make_embed(title="**Exchange Rate**",description="Find the current bitcoin and ethereum exchange rate. This is updated every minute or so.").add_field(name="**Parameters**",value="*None*")
    elif command.startswith('rank'):
      embed=make_embed(title="**Rank**",description="Find your current net worth and rank in the simulation. Alternatively, you can find the net worth of someone else. This is an **expensive** command, meaning that you will be blocked from sending messages for another 20 seconds.").add_field(name="**Parameters**",value="""
- [name]. Optional. The person whose net worth you want to find (must be at least 4 characters long). Defaults to yourself.""")
    elif command.startswith('short'):
      embed=make_embed(title="**Short Cryptocurrency (via a CFD)**",description="This command allows you to place a Contract for Difference (a CFD). You agree to pay the difference between the cryptocurrencies price after some number of hours. If the price falls, you make a profit! Note that you lose access to the money in the CFD until the contract ends. If you go bankrupt at the end of a contract, [insert punishment here] will happen!").add_field(name="**Parameters**",value="""
- [cur]. The cryptocurrency you want to short (either btc or eth).
- [amt]. The amount of the cryptocurrency that you want to short.
- [h]. The time, in hours, that the contract will last before collection occurs. The default value is 24 (1 day), although you can make it anywhere from 0.1 (6 minutes) to 10000 (over a year).""")
    elif command.startswith('contract'):
      embed=make_embed(title="**Contracts**",description="Displays a list of your ongoing contracts, and the current profit of each contract. Use the `short` command to place a CFD and sell short on cryptocurrency!").add_field(name="**Parameters**",value="*None*")
    elif command.startswith('net'):
      embed=make_embed(title="**Net Worth**",description="Displays your current simulation assets in an easy to read format.").add_field(name="**Parameters**",value="*None*")
  except:
    pass
  return embed