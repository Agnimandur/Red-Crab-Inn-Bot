[<img alt="reaper logo" src="reaper.png">](https://discord.com/api/oauth2/authorize?client_id=791162942459478016&permissions=2080894065&scope=bot)
# Red Crab Inn Discord Bot
The primary function of the bot is to play the game *[Reaper](https://artofproblemsolving.com/reaper)*, a math game created by folks at AOPS. Reaper is a game of strategy and patience, and anywhere from 2 to over a thousand players can play! Depending on the type of game you want, a Reaper game might last as little as 2 minutes to as much as several months! This bot is hosted on Repl.it, and continuously run due to UptimeRobot.

To add this bot to your discord server, use **[this link](https://discord.com/api/oauth2/authorize?client_id=791162942459478016&permissions=2080894065&scope=bot)**. A list of Reaper specific commands are at the bottom of this README. Click here to join the **[Public Reaper Server](https://discord.gg/5bbnUz6J2a)**

#### $quote
Receive an inspirational quote!

#### $trump
Receive a Donald Trump quote!

#### $kanye
Receive a Kanye West quote!

#### $8ball
The Magic 8 Ball will answer your query.

#### $github
Get a link to this github repository.

#### $servers
Find the number of servers and people that this bot has reached.

#### $reaper
An admin can type $reaper to create a reaper channel in your discord server.
The following commands only work in the #reaper or #reaper-discussion channel.

<br/>

## Reaper Game Commands

#### begin game h=[h] p=[p] rng=[rng]
An admin starts a new Reaper game. The reap cooldown is [h] hours, and the first to reach [p] points wins. If [rng] is 0, then there will be no random reap multipliers or free reaps! All parameters are optional. The default value of [h] is 12, [p] is 43200 (12 hours to reap), and [rng] is 1 (enabled).

#### begin blitz game s=[s] p=[p] rng=[rng]
An admin starts a new **Blitz** Reaper game. The reap cooldown is [s] seconds, and the first to reach [p] points wins. The difference between blitz and standard games is that in blitz, players play continuously from the beginning to the end of the game. Blitz games usually last from 2 minutes to an hour. In blitz reaper, keeping track of your opponent's timers is critical! The default value of [s] is 10, [p] is 120 (2 minutes to reap), and [rng] is 1 (enabled).

#### h=[h] or s=[s]
An admin changes the reap cooldown to [h] hours (standard games only) or [s] seconds (blitz games only).

#### p=[p]
An admin changes the point target to [p]. If a player is already at [p] points, he still needs to reap once to win!

#### rng=[rng]
If [rng]=0, then randomness is disabled. If [rng]=1, then randomness is enabled.

#### end game
An admin forcibly ends the ongoing game.

#### reset [users]
An admin can type "reset" along with @ing a list of [users] to manually reset all their scores to 0.

<br />

#### reap
Any player can reap! If this is your first reap, you will automatically join the standings. Your cooldown will also begin. You may get bonus points, or free reaps!

The number of points you get is the number of seconds between the time of your reap and the time of the last reap. You will need to maximize this time, since you will only get to reap occasionally. Try to avoid getting "sniped", which is when someone reaps a few seconds before you, causing you to waste your reap on very few points. Perfect timing is key to success!

#### timer
Find the current point value of a reap (in milliseconds).

#### nextreap
Find the time remaining before you can reap again.

#### rank=[name]
Find out your current point total, and your current rank in the game! If the optional [name] parameter is provided, it finds the score of person [name].
