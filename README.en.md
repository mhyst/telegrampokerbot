# telegrampokerbot

[![es](https://img.shields.io/badge/lang-es-red.svg)](https://github.com/mhyst/telegrampokerbot/blob/main/README.md)

## Mode of use

* Clone the present repo
* Make a new bot from scratch with @botfather
* Get the bot private token and replace it by the word "TOKEN" in configure.py file
* Execute the bot either with python3 pockerbot.py or with ./pockerbot.py
* Add the bot to a Telegram group
* Play

## Game mechanics

Beforehand, All players must iniciate a private chat with the bot and
click start. If any player should forget this step, the bot will be
unable to send the cards by private message, what will prevent the bot
from working. Then players must join the same group where you added
the bot to.

To start the game, any given player will open the game with */abrir*
command. Then the ones who want to enter the game can join the game
with */entro* command. Once everyone is in, another player can send
the command */cierro* to start the game. The bot will give cards to
all players and first round of bets. The bot will call every user by
turns to make theirs bets, and only in its turn a user will be able to
use the commands */subo* (raise bet) */veo* (see your bet) */paso* (I
pass this turn) and */novoy* (I abandon this game). For now the
command */subo* can only raise the bet by 5. After the first round of
bets, players can drop the cards they don*t want and replace with new
ones from the bot using */sirve* command. This commands allows you to
discard upto five cards all at once or in several steps by giving it
the card ids (starting by 0). For instance */serve 03* will discard
cards 0 and 3 from your hand. Card ids must be written together
without any kind of separator. When all players have discarded five
cards or have called the */servido* command, it will be time for round
number two of bets to start. Once all bets have finished, the bot will
show the result of the game and who the whinner is.

When any given game is finished, the bot returns to a state in which
some more players can join while others can leave (*/salgo* command).
Then the game can be resumed again by using */cierro* command.

There are some things that are still in development. Like a points
table and a target to finish a set of games. It will come when I can
spare some time to it.
