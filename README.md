[<img alt="reaper logo" src="reaper.png">](https://discord.com/api/oauth2/authorize?client_id=791162942459478016&permissions=805825648&scope=bot)
# Red-Crab-Inn-Bot
Code for a discord bot built in python on repl.it. Due to integration with UptimeRobot, this bot will run continuously!
The primary function of the bot is to play the game *Reaper*, a math game created by folks at AOPS. A full explanation of how *Reaper* works can be found **[here](https://artofproblemsolving.com/reaper)**.

To add this bot to your discord server, use **[this link](https://discord.com/api/oauth2/authorize?client_id=791162942459478016&permissions=537390192&scope=bot)**.

#### $reaper
An admin can type $reaper to create a reaper channel in your discord server.
The following commands only work in the #reaper channel.

#### $github
Get a link directly to this Github repository!

## Admin Commands
#### begin game h=[h] p=[p]
An admin starts a new Reaper game. The reap cooldown is [h], and the first to reach [p] points is the winner. Both parameters are optional. The default value of [h] is 12, and the default value of [p] is 42,300,000 (12 hours to reap).

#### h=[h]
An admin changes the reap cooldown to [h].

#### p=[p]
An admin changes the points necessary to win to [p].

#### end game
An admin forcibly ends the ongoing game.


## Player Commands
#### reap
Any player can reap! If this is your first reap, you will automatically join the standings. Your cooldown will also begin.
You may get bonus points, or free reaps!

#### timer
Find the current point value of a reap (in milliseconds).

#### rank
Find out your current point total, and your current rank in the game!

#### leaderboard
Return a top10 current leaderboard of the ongoing game.
