[<img alt="reaper logo" src="reaper.png">](https://discord.com/api/oauth2/authorize?client_id=791162942459478016&permissions=537390192&scope=bot)
# Red Crab Inn Discord Bot
Code for a discord bot built in python on repl.it. Due to integration with UptimeRobot, this bot will run continuously!
The primary function of the bot is to play the game *[Reaper](https://artofproblemsolving.com/reaper)*, a math game created by folks at AOPS.

To add this bot to your discord server, use **[this link](https://discord.com/api/oauth2/authorize?client_id=791162942459478016&permissions=537390192&scope=bot)**.

#### $quote
Receive an inspirational quote!

#### $github
Get a link to this github repository.

#### $reaper
An admin can type $reaper to create a reaper channel in your discord server.
The following commands only work in the #reaper channel.

#### begin game h=[h] p=[p]
An admin starts a new Reaper game. The reap cooldown is [h], and the first to reach [p] points is the winner. Both parameters are optional. The default value of [h] is 12, and the default value of [p] is 43200 (12 hours to reap).

#### h=[h]
An admin changes the reap cooldown to [h].

#### p=[p]
An admin changes the points necessary to win to [p].

#### end game
An admin forcibly ends the ongoing game.

#### reap
Any player can reap! If this is your first reap, you will automatically join the standings. Your cooldown will also begin. You may get bonus points, or free reaps!

The number of points you get is the number of seconds between the time of your reap and the time of the last reap. You will need to maximize this time, since you will only get to reap occasionally. Try to avoid getting "sniped", which is when someone reaps a few seconds before you, causing you to waste your reap on very few points. Perfect timing is key to success!

#### timer
Find the current point value of a reap (in milliseconds).

#### rank=[name]
Find out your current point total, and your current rank in the game! If the optional [name] parameter is provided, it finds the score of person [name].
