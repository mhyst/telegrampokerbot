# telegrampokerbot
## Modo de uso
* Clonar el repositorio
* Crear un bot nuevo con @botfather
* Obtener el token y reemplazarlo por la palabra TOKEN del archivo configure.py
* Ejecutar pokerbot.py
* Meter el bot en un grupo
* Jugar

## Mecánica de juego

Todos los jugadores deben iniciar un privado previamente con el bot y pulsar
el botón inicio (/start). Si algún jugador no ha cumplido ese paso el bot no
podrá enviarle las cartas por privado, lo que impedirá el juego. Luego
tendrán que unirse, si no lo están ya, al grupo donde tendrá lugar la
partida.

Para empezar a jugar, un jugador abrirá el juego con el comando
/abrir. Entonces podrán unirse todos los que quieran jugar con el
comando /entro. Una vez se hayan unido todos los que vayan a jugar,
otro jugador cerrará el juego con /cerrar. Enseguida se repartirán las
cartas que le llegarán a cada jugador por privado y se iniciará la
primera ronda de apuestas. El bot irá llamando por turno a cada
jugador y solo este podrá hacer su apuesta con los comandos /subo /veo
/paso /novoy. El comando /subo por ahora solo añade 5 fichas a la
apuesta. Próximamente se podrá introducir una cantidad concreta o ir
con todo. Tras la primera ronda llega el momento de los descartes.
Estos se podrán hacer en cualquier orden con el comando /sirve seguido
de un espacio y los números de las cartas de los que queremos
deshacernos (empezando en 0). Por ejemplo, con /sirve 03 nos
descartaremos de la carta 0 y 3 (1 y 4). Los números deben ir juntos
sin ningún tipo de separación, solo separados del comando /sirve por
un espacio. Cuando todos los jugadores se hayan descartado de 5 cartas
o hayan invocado el comando /servido, se iniciará la segunda y última
ronda de apuestas, que se desarrollará igual que la anterior. Al
finalizar, el bot mostrará el resultado de la partida.

Una vez terminada la partida, el bot queda en el estado en el que de
nuevo acepta participantes. Nuevos jugadores pueden unirse con /entro
o abandonar el juego con /salgo. Después puede cerrarse de nuevo el
juego con /cerrar podemos pasar a la siguiente partida.

Todavía no hay un sistema de puntos ni puntos objetivo. Eso es algo
que se implementará próximamente.


