# Ludum Date 34 Entry
Basic concept: A very basic side scrolling game, like Gemotry Dash, with the added
mechanic that you grow slowly over time. Pressing another button will reduce your size
making it easier to complete levels. The larger you are the more points you get though.

## Gampeplay
* Auto running to the right
* Collide with any objects other than landing on top of safe blocks will kill the player
** Colliding with the side of any object will result in death
** Colliding with the top or bottom of safe objects is OK
* The player slowly grows in size over time
* Pressing one button will cause the player to jump
* Pressing another button will cause the player to shrink
* Score accumulates based on distance and size, the larger you are the more points per distance unit

## Technical Stuff
* Using Python and PyGame for the engine and code
* Using Tiled from mapeditor.com for creating maps
* Using PyTMX for loading the .tmx map files