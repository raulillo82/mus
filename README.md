# Mus
Mus cards game

Mus is a very typical card game in Spain. It's supposed to have its origin in the Basque Country region, however its very well known in most areas of Spain, being some examples Navarra or Madrid. Some people claim numerous university students spend longer in the cafeteria playing this game, than actually attending to lessons. That being true or false, the game has a high component of strategy.

Please read the Wikipedia reference for this game in order to understand it: https://en.wikipedia.org/wiki/Mus_(card_game)

This project was developed in 2015 (and forgotten). Willing to get some more exposure to Python, the project was rescued from some forgotten harddrive directory and uploaded into Github (in order to practice version controlling as well).

The project is very basic, and has some limitations that differ from the original game (check the reference above). Namely:
- It does not consider any possible dicard phase(s). Players always play with the starting cards.
- As the game is played automatically without interaction, no bets are done. Winner of the first two sub-games will simply earn one point, winners of the other two sub-games, will win a point when it applies, together with the value of their given hand.
- Only one single game (up to 40 points) is played. Normally a full game is for the best of 3 or 5.

Technical limitations:
- Depending on the version of python and the Graphical interface used (only tested with KDE-Plasma), buttons might not be seen at first. One would need to click on one of them blindly so that they get loaded (they're located on the top left of the window, in case you hit this bug)
