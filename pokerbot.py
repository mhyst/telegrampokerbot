#!/usr/bin/env python3
# pylint: disable=unused-argument, wrong-import-position
# This program is dedicated to the public domain under the CC0 license.

"""
Bot de Telegram para jugar al poker


Bot de Telegram que permite jugar al poker entre 2 y 5 jugadores.

Agradecimientos:

Utilicé el ejemplo echobot de la biblioteca python telegram bot como punto
de partida para este bot. La URL original es la que sigue:

https://github.com/python-telegram-bot/python-telegram-bot/blob/master/examples/echobot.py

Los documentos de ayuda de la bibliteca Python Telegram Bot me ayudaron a dar los primeros
pasos, en un ambiente al que nunca me había asomado, y a rellenar los huecos 

Un algoritmo básico que determinaba el juego de un jugador, proporcionado por CgatGPT.

Este algoritmo, ligeramente alterado puede encontrarse en Jugada.mejorJugada.

Fueron de gran ayuda las ideas de algunos compañeros del grupo Teóricos de la Conspiración 
(https://t.me/TeoricosDeLaConspiracion) como Cejas Pobladas, Dr.Psychoblack, GAR y otros.

Por último, la inestimable ayuda de decenas de inestimables usuarios a lo largo de 
Internet de cuyas respuestas y publicaciones obtuve información vital para la escritura
de este código.

"""

import logging

from telegram import __version__ as TG_VER
from telegram import Chat, ChatMember, ChatMemberUpdated, Update, ForceReply
from telegram.constants import ParseMode


try:
    from telegram import __version_info__
except ImportError:
    __version_info__ = (0, 0, 0, 0, 0)  # type: ignore[assignment]

if __version_info__ < (20, 0, 0, "alpha", 1):
    raise RuntimeError(
        f"This example is not compatible with your current PTB version {TG_VER}. To view the "
        f"{TG_VER} version of this example, "
        f"visit https://docs.python-telegram-bot.org/en/v{TG_VER}/examples.html"
    )
from telegram.ext import Application, CommandHandler, ContextTypes, MessageHandler, filters

# Importamos objetos del juego
from jugador import Jugador
from baraja import Baraja
from jugada import Jugada

# Importamos la configuración
from configure import token

# Enable logging
# Aunque no lo uso, por el momento se queda.
logging.basicConfig(
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s", level=logging.INFO
)
logger = logging.getLogger(__name__)


# Inicialización
# Objetos juego y variables globales
jugada = None
ABRIR, PARTICIPAR, APUESTAS1, DESCARTES, APUESTAS2, RESULTADO = range(6)
estado = ABRIR
chat_id=-1


# Manejador: Punto de entrada
# Todos los jugadores tienen que enviar este comando por privado al bot
# antes de poder jugar, para que el bot pueda enviarles mensajes
# privados.
#
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Send a message when the command /start is issued."""
    user = update.effective_user
    await update.message.reply_html(
        rf"!Hola{user.mention_html()}!",
        reply_markup=ForceReply(selective=True),
    )


# Manejador: Ayuda del juego
# ---------------
# Aún por desarrollar
#
async def help_command(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Send a message when the command /help is issued."""
    await update.message.reply_html("El puto <b>mhyst</b> aún no ha tenido tiempo de escribir la ayuda")


# Función de soporte: Comandos en este estado
# -------------------------------------------
# Permite informar al usuario cuales son los comandos que puede
# invocar en el estado actual.
#
def comandosEstado():
    global estado

# ABRIR, PARTICIPAR, APUESTAS1, DESCARTES, APUESTAS2, RESULTADO = range(6)

    if estado == ABRIR:
        res = "/abrir, /ayuda"
        s = "ABRIR"
    elif estado == PARTICIPAR:
        res = "/entro, /salgo, /cerrar, /terminar"
        s = "PARTICIPAR"
    elif estado == APUESTAS1:
        res = "/subo, /veo, /paso, /novoy"
        s = "APUESTAS1"
    elif estado == APUESTAS2:
        res = "/subo, /veo, /paso, /novoy"
        s = "APUESTAS2"
    elif estado == DESCARTES:
        res = "/sirve, /servido"
        s = "DESCARTES"
    elif estado == RESULTADO:
        res = "/evaluar"
        s = "RESULTADO"
    else:
        res = "¿?"
        s = "ERROR"

    return rf"Comandos disponibles estado: {s} - {res}"


# Función de soporte: Enviar Mensaje al Grupo
# -------------------------------------------
# En el caso de que algunos jugadores estén jugando desde sus ventanas de chat privadas
# esta función permite suministrar al grupo la información que sea imprescindible.
#
async def sendToGroup(nombre, context, mensaje):
    global chat

    await context.bot.send_message(chat_id=chat_id, text=nombre+": "+mensaje, parse_mode=ParseMode.HTML)



# Función de soporte: Enviar
# --------------------------
# Todos los manejadores llaman a esta función para enviar mensajes al usuario o al grupo.
# Determina si estamos en un chat privado o en un grupo y en caso de ser lo primero
# envía el mensaje también al grupo.
#
async def send(update: Update, context, mensaje):
    if update.effective_chat.type == Chat.PRIVATE:
        await update.message.reply_html(mensaje)
        await sendToGroup(update.effective_user.first_name, context, mensaje)
    else:
        await update.message.reply_html(mensaje)


# Manejador: Abrir juego nuevo
# ----------------------------
# Abre un juego nuevo
#
async def open_command(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    global estado, jugada, chat_id
    if estado != ABRIR:
        comandos = comandosEstado()
        await send(update, context, "El juego ya fue abierto * "+comandos)
        return

    """Abrir juego"""
    mensaje = ""
    if jugada:
        mensaje = "El juego ya estaba abierto"
    elif update.effective_chat.type == Chat.PRIVATE:
        mensaje = "El juego no puede abrirse desde un mensaje privado"
    else:
        jugada = Jugada()
        mensaje = "Juego abierto"
        chat_id = update.effective_chat.id
        estado = PARTICIPAR

    await send(update, context, mensaje)


# Manejador: Unirse al juego
# --------------------------
# Un jugador se une al juego
#
async def join_command(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    if estado != PARTICIPAR:
        comandos = comandosEstado()
        await update.message.reply_html("Comando no válido en este estado * "+comandos)
        return

    global jugada
    mensaje = ""
    if not jugada:
        mensaje = "Aún no se ha abierto el juego. <i>Usa el comando open</i>"
    else:
        if jugada.esCompleto() or len(jugada.jugadores) == 5:
            mensaje = "El juego esta completo. Espera al próximo juego"
        else:
            user = update.effective_user.first_name
            if jugada.getJugador(user):
                mensaje = "Ya estabas en el juego"
            else:
                jugador = jugada.addJugadorByNombre(user)
                jugador.setChatId(update.effective_user.id)
                mensaje = rf"<b>{user}</b> se ha unido al juego"

    await send(update, context, mensaje)


# Manejador: Abandonar el juego
# -----------------------------
# Un jugador abandona el juego
#
async def part_command(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    global jugada, estado

    if estado != PARTICIPAR:
        comandos = comandosEstado()
        await send(update, context, "Comando no válido en este estado * "+comandos)
        return

    mensaje = ""
    if not jugada:
        mensaje = "Aún no se ha abierto el juego. <i>Usa el comando open</i>"
    else:
        user = update.effective_user.first_name
        jugador = jugada.removeJugadorByNombre(user)
        if jugador:
            mensaje = rf"<b>{user}</b> ha salido del juego"
        else:
            mensaje = "No estabas jugando"

    await send(update, context, mensaje)


# Manejador: Lista de jugadores
# -----------------------------
# Muestra los jugadores que están en el juego
#
async def jugadores_command(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    global jugada
    mensaje = ""
    if not jugada:
        mensaje = "Aún no se ha abierto el juego. <i>Usa el comando open</i>"
    else:
        if len(jugada.jugadores) == 0:
            mensaje = "Aún no se ha unido ningún jugador"
        else:
            mensaje = "<u><b>Lista de Jugadores</b></u>"
            mensaje += "\n\n"
            for jugador in jugada.jugadores:
                mensaje += rf"<b>{jugador.getNombre()}</b>"
                mensaje += "\n"

    await send(update, context, mensaje)



# Manejador: Tabla de ganancias
# -----------------------------
# Muestra los fondos de cada jugador
#
async def ganancias_command(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    global jugada
    mensaje = ""
    if not jugada:
        mensaje = "Aún no se ha abierto el juego. <i>Usa el comando open</i>"
    else:
        if len(jugada.jugadores) == 0:
            mensaje = "Aún no se ha unido ningún jugador"
        else:
            mensaje = "<u><b>Tabla Ganancias</b></u>\n\n"
            for jugador in jugada.jugadores:
                mensaje += rf"<b>{jugador.getNombre()}</b> <b>{jugador.getFondos()}</b>"
                mensaje += "\n"

    await send(update, context, mensaje)


# Manejador: Cerrar juego
# -----------------------
# El juego comienza, se reparten las cartas, hagan sus apuestas
#
async def close_command(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    global estado, jugada

    if estado != PARTICIPAR:
        comandos = comandosEstado()
        await send(update, context, "Comando no válido en este estado * "+comandos)
        return

    """Cerramos el juego para que no puedan entrar otros jugadores."""
    mensaje = ""
    if jugada == None:
        mensaje = "Aún no se ha abierto el juego. <i>Usa el comando open</i>"
    else:
        if jugada.esCompleto():
            mensaje = "El juego ya esta completo."
        else:
            if len(jugada.jugadores) == 0:
                mensaje = "Para jugar necesitamos algunos jugadores. <i>Únete con /join</i>"
            else:
                if len(jugada.jugadores) == 1:
                    pukito = jugada.addJugadorByNombre("pukit")
                    pukito.setServido(True)
                
                jugada.nuevaBaraja()
                jugada.repartirCartas()
                jugada.setCompleto(True)
                for jugador in jugada.jugadores:
                    if jugador.getNombre() != "pukit":
                        tusCartas = '  '.join(jugador.getCartasBonitas())
                        await context.bot.send_message(chat_id=jugador.getChatId(), text=tusCartas)
                mensaje = "El juego está completo * "

                turno = jugada.nextTurn()
                mensaje += rf"Primera ronda de apuestas. Turno de <b>{turno.getNombre()}</b>"
                jugada.rondaApuestas = 1
                estado = APUESTAS1

    await send(update, context, mensaje)


# Manejador: Servir cartas
# ------------------------
# Un jugador pide un descarte al bot
#
async def serve_command(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    global estado, jugada

    if estado != DESCARTES:
        comandos = comandosEstado()
        await send(update, context, "Comando no válido en este estado * "+comandos)
        return

    """Servimos cartas al jugador que las pide si aún no ha consumido sus 5 cartas de descarte"""
    mensaje = ""
    if jugada == None:
        mensaje = "Aún no se ha abierto el juego. Usa el comando open"
    else:
        if not jugada.esCompleto():
            mensaje = "El juego aún no esta completo. Esperando que se unan más jugadores."
        else:
            if len(jugada.jugadores) == 0:
                mensaje = "Error. No se añadió ningún jugador."
            else:
                user = update.effective_user.first_name
                message = update.message.text
                jugador = jugada.getJugador(user)
                if not jugador:
                    mensaje = rf"Error: El jugador <b>{user}</b> no está jugando."
                else:
                    print(message)
                    cmds = message.split(' ')
                    cmds.pop(0)

                    if len(cmds) == 0:
                        mensaje = "Debes indicar los índices de las cartas de las que desea descartarse (0 al 4)"
                    else:
                        error = False
                        ids = []
                        try:
                            ids = [int(i) for i in cmds[0]]
                        except:
                            error = True

                        if error:
                            mensaje = "Debes indicar números enteros del 0 al 4"
                        else:
                            servido = jugada.servirJugador(jugador,ids)
                            if servido == len(ids):
                                tusCartas = '  '.join(jugador.getCartasBonitas())
                                await context.bot.send_message(chat_id=jugador.getChatId(), text=tusCartas)
                                if jugador.getServicio() == 5:
                                    mensaje = "Se te ha servido. Vuelve a mirar tus cartas * "
                                    mensaje += rf"<b>{user}</b> está servido"
                                else:
                                    mensaje = "Se te ha servido. Vuelve a mirar tus cartas"
                            elif servido > 0:
                                mensaje = "No se te ha servido. Solo puedes descartarte de "+str(servido)
                            else:
                                mensaje = "No te quedan descartes"

    await send(update, context, mensaje)
    if jugada.isServida():

        jugada.setIdTurn(0)
        jugada.rondaApuestas = 2
        jugada.nTurno = 0
        turno = jugada.nextTurn()

        mensaje += "\n"
        mensaje += rf"Ronda 2 de apuestas: turno de <b>{turno.getNombre()}</b>"
        await send(update, context, mensaje)
        estado = APUESTAS2


# Manejador: Jugador Servido
# ------------------
# Un jugador se declara servido
#
async def served_command(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    global estado, jugada

    if estado != DESCARTES:
        comandos = comandosEstado()
        await send(update, context, "Comando no válido en este estado * "+comandos)
        return

    """El jugador se da por servido."""
    mensaje = ""
    if jugada == None:
        mensaje = "Aún no se ha abierto el juego. <i>Usa el comando open</i>"
    else:
        if not jugada.esCompleto():
            mensaje = "El juego aún no esta completo. Esperando que se unan más jugadores."
        else:
            if len(jugada.jugadores) == 0:
                mensaje = "Error. No se añadió ningún jugador."
            else:
                user = update.effective_user.first_name
                message = update.message.text
                jugador = jugada.getJugador(user)
                if not jugador:
                    mensaje = rf"Error: El jugador <b>{user}</b> no está jugando."
                else:
                    jugador.setServido(True)
                    mensaje = rf"<b>{user}</b> está servido"

    await send(update, context, mensaje)
    if jugada.isServida():
        print("DEBUG - served: estan todos servidos")
        jugada.setIdTurn(0)
        jugada.rondaApuestas = 2
        jugada.nTurno = 0
        turno = jugada.nextTurn()
        mensaje += "\n"
        mensaje += rf"Ronda 2 de apuestas: turno de <b>{turno.getNombre()}</b>"
        await send(update, context, mensaje)
        estado = APUESTAS2


# Manejador: Ver Apuesta
# ----------------------
# El jugador ve la apuesta
#
async def veo_command(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    global jugada, estado

    if estado != APUESTAS1 and estado != APUESTAS2:
        comandos = comandosEstado()
        await send(update, context, "Comando no válido en este estado * "+comandos)
        return

    mensaje = ""
    if jugada == None:
        mensaje = "Aún no se ha abierto el juego. <i>Usa el comando open</i>"
    else:
        if not jugada.esCompleto():
            mensaje = "El juego aún no esta completo. Esperando que se unan más jugadores."
        else:
            if len(jugada.jugadores) == 0:
                mensaje = "Error. No se añadió ningún jugador."
            else:
                user = update.effective_user.first_name
                message = update.message.text
                jugador = jugada.getJugador(user)
                if not jugador:
                    mensaje = rf"Error: El jugador <b>{user}</b> no está jugando."
                else:
                    turno = jugada.getTurn()
                    if jugador != turno:
                        mensaje = rf"No es tu turno, sino el de <b>{turno.getNombre()}</b>"
                    else:
                        lastApuesta = jugada.lastApuesta
                        if lastApuesta == 0 or jugada.nTurno == 1:
                            mensaje = "Aún no hay apuesta inicial"
                        else:
                            jugada.verApuesta(jugador)
                            mensaje = rf"<b>{user}</b> ve la apuesta"
                            mensaje += "\n"
                            turno = jugada.nextTurn()

                            if turno is None:
                                if jugada.isFinJuego():
                                    estado = RESULTADO
                                    mensaje = evaluar()
                                else:
                                    mensaje = "Las apuestas han concluído"
                                    mensaje += "\n"
                                    if jugada.rondaApuestas == 1:
                                        mensaje += "Se inician los descartes (<i>/sirve /servido</i>)"
                                        estado = DESCARTES
                                    elif jugada.rondaApuestas == 2:
                                        estado = RESULTADO
                                        mensaje = evaluar()
                            else:
                                mensaje += rf"Ronda {str(jugada.rondaApuestas)}: Turno de apostar de <b>{turno.getNombre()}</b>"
                                mensaje += "\n"
                                mensaje += rf"Montante: {str(jugada.lastApuesta)} - Tu apuesta: {str(turno.getApuesta())}"

    await send(update, context, mensaje)


# Manejador: Subir Apuesta
# ------------------------
# El jugador sube la apuesta
#
async def subo_command(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    global jugada, estado

    if estado != APUESTAS1 and estado != APUESTAS2:
        comandos = comandosEstado()
        await send(update, context, "Comando no válido en este estado * "+comandos)
        return

    """Evaluamos el juego a ver quién ha ganado"""
    mensaje = ""
    if jugada == None:
        mensaje = "Aún no se ha abierto el juego. <i>Usa el comando open</i>"
    else:
        if not jugada.esCompleto():
            mensaje = "El juego aún no esta completo. Esperando que se unan más jugadores."
        else:
            if len(jugada.jugadores) == 0:
                mensaje = "Error. No se añadió ningún jugador."
            else:
                user = update.effective_user.first_name
                message = update.message.text
                jugador = jugada.getJugador(user)
                if not jugador:
                    mensaje = rf"Error: El jugador <b>{user}</b> no está jugando."
                else:
                    turno = jugada.getTurn()
                    if jugador != turno:
                        mensaje = rf"No es tu turno, sino el de <b>{turno.getNombre()}</b>"
                    else:
                        error = False
                        comando = message.split(" ")
                        if len(comando) < 2:
                            cantidad = jugada.apuestaMinima
                        else:
                            try:
                                cantidad = int(comando[1])
                            except:
                                error = True

                        if error:
                            mensaje = "Necesitas indicar un número entero para subir la apuesta\n"
                            mensaje += rf"Inténtalo de nuevo {user}"
                        else:
                            if jugada.subirApuesta(jugador, cantidad):
                                mensaje = rf"<b>{user}</b> sube la apuesta en {str(cantidad)}"
                                mensaje += "\n"
                                turno = jugada.nextTurn()

                                if turno is None:
                                    if jugada.isFinJuego():
                                        estado = RESULTADO
                                        mensaje = evaluar()
                                    else:
                                        mensaje = "las apuestas han concluído"
                                        mensaje += "\n"
                                        if jugada.rondaApuestas == 1:
                                            mensaje += "Se inician los descartes (<i>/sirve /servido</i>)"
                                            estado = DESCARTES
                                        elif jugada.rondaApuestas == 2:
                                            estado = RESULTADO
                                            mensaje = evaluar()
                                else:                    
                                    mensaje += rf"Ronda {str(jugada.rondaApuestas)}: Turno de apostar de <b>{turno.getNombre()}</b>"
                                    mensaje += "\n"
                                    mensaje += rf"Montante: {str(jugada.lastApuesta)} - Tu apuesta: <b>{str(turno.getApuesta())}</b>"
                            else:
                                mensaje = rf"<b>{user}, no tienes suficientes fondos para cubrir esa apuesta.</b>"

    await send(update, context, mensaje)


# Manejador: Jugador Pasa
# -----------------------
# El jugador pasa este turno
#
async def paso_command(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    global jugada, estado

    if estado != APUESTAS1 and estado != APUESTAS2:
        comandos = comandosEstado()
        await send(update, context, "Comando no válido en este estado * "+comandos)
        return

    """Evaluamos el juego a ver quién ha ganado"""
    mensaje = ""
    if jugada == None:
        mensaje = "Aún no se ha abierto el juego. Usa el comando open"
    else:
        if not jugada.esCompleto():
            mensaje = "El juego aún no esta completo. Esperando que se unan más jugadores."
        else:
            if len(jugada.jugadores) == 0:
                mensaje = "Error. No se añadió ningún jugador."
            else:
                user = update.effective_user.first_name
                message = update.message.text
                jugador = jugada.getJugador(user)
                if not jugador:
                    mensaje = rf"Error: El jugador <b>{user}</b> no está jugando."
                else:
                    turno = jugada.getTurn()

                    if jugador != turno:
                        mensaje = rf"No es tu turno, sino el de <b>{turno.getNombre()}</b>"
                    else:
                        if jugada.rondaApuestas == 1:
                            jugador.setPasado(True)
                            mensaje = rf"<b>{user}</b> ha pasado"
                            mensaje += "\n"

                            turno = jugada.nextTurn(True)


                            if turno is None:
                                if jugada.isFinJuego():
                                    estado = RESULTADO
                                    mensaje = evaluar()
                                else:
                                    mensaje = "las apuestas han concluído"
                                    mensaje += "\n"
                                    if jugada.rondaApuestas == 1:
                                        mensaje += "Se inician los descartes (/sirve /servido)"
                                        estado = DESCARTES
                                    elif jugada.rondaApuestas == 2:
                                        estado = RESULTADO
                                        mensaje = evaluar()
                            else:
                                mensaje += rf"Ronda {str(jugada.rondaApuestas)}: Turno de apostar de <b>{turno.getNombre()}</b>"
                                mensaje += "\n"
                                mensaje += rf"Montante: {str(jugada.lastApuesta)} - Tu apuesta: {str(turno.getApuesta())}"


                        else:
                            mensaje = "No puedes pasar en la segunda ronda de apuestas * "
                            mensaje += "<b>{user}</b>Sigue siendo tu turno"

    await send(update, context, mensaje)


# Manejador: Jugador No Va
# ------------------------
# El jugador se retira de esta ronda de juego
#
async def novoy_command(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    global jugada, estado

    if estado != APUESTAS1 and estado != APUESTAS2:
        comandos = comandosEstado()
        await send(update, context, "Comando no válido en este estado * "+comandos)
        return

    """Evaluamos el juego a ver quién ha ganado"""
    mensaje = ""
    if jugada == None:
        mensaje = "Aún no se ha abierto el juego. Usa el comando open"
    else:
        if not jugada.esCompleto():
            mensaje = "El juego aún no esta completo. Esperando que se unan más jugadores."
        else:
            if len(jugada.jugadores) == 0:
                mensaje = "Error. No se añadió ningún jugador."
            else:
                user = update.effective_user.first_name
                message = update.message.text
                jugador = jugada.getJugador(user)
                if not jugador:
                    mensaje = rf"Error: El jugador <b>{user}</b> no está jugando."
                else:
                    turno = jugada.getTurn()
                    if jugador != turno:
                        mensaje = rf"No es tu turno, sino el de {turno.getNombre()}"
                    else:
                        user = update.effective_user.first_name
                        message = update.message.text
                        jugador = jugada.getJugador(user)

                        jugador.setNovoy(True)
                        jugador.setServido(True)
                        mensaje = rf"<b>{user}</b> se retira"
                        mensaje += "\n"
                        turno = jugada.nextTurn(True)

                        if turno is None:
                            if jugada.isFinJuego():
                                estado = RESULTADO
                                mensaje = evaluar()
                            else:
                                mensaje = "las apuestas han concluído"
                                mensaje += "\n"
                                if jugada.rondaApuestas == 1:
                                    mensaje += "Se inician los descartes (<i>/sirve /servido</i>)"
                                    estado = DESCARTES
                                elif jugada.rondaApuestas == 2:
                                    estado = RESULTADO
                                    mensaje = evaluar()
                        else:
                            mensaje += rf"Ronda {str(jugada.rondaApuestas)}: Turno de apostar de <b>{turno.getNombre()}</b>"
                            mensaje += "\n"
                            mensaje += rf"Montante: {str(jugada.lastApuesta)} - Tu apuesta: {str(turno.getApuesta())}"


    await send(update, context, mensaje)


# Función de Soporte: Evaluar Juego
# ---------------------------------
# Realiza comprobaciones para ver quién ha ganado y lo muestra en el grupo
#
def evaluar():
    global jugada, estado

    # Evaluamos el resultado de la jugada
    if jugada.isFinJuego():
        mensaje = rf"Gana <b>{jugada.lastGanadores[0].getNombre()}</b> por abandono. Gana {str(jugada.bote)}"
        jugada.repartirBote(jugada.lastGanadores)
        #jugada.lastBote = jugada.bote
        #mensaje += jugada.mostrar2()
    else:
        mensaje = jugada.evaluarResultado()

    # Preparamos la siguiente jugada

    # El primero pasa a ser el último
    jugadores = jugada.jugadores.copy()
    ultimo = jugadores.pop(0)
    jugadores.append(ultimo)

    #Empezamos con jugada y baraja nueva
    jugada = Jugada()
    for jugador in jugadores:
        j = jugada.addJugadorByNombre(jugador.getNombre())
        j.setChatId(jugador.getChatId())
        j.setFondos(jugador.getFondos())
    jugada.setCompleto(False)

    #Pasamos al estado de participar para que puedan unirse otros jugadores
    estado = PARTICIPAR

    #Devolvemos la cadena con el ganador
    return mensaje


# Manejador: Evaluar Juego - En deshuso
# -------------------------------------
# Manejador en deshuso
# Servía para responder al comando evaluate o evaluar y mostrar el resultado
# del juego.
#
# Ahora el resultado se muestra automáticamente al terminar la segunda ronda
# de apuestas.
#
async def evaluate_command(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    global estado, jugada

    if estado != RESULTADO:
        comandos = comandosEstado()
        await send(update, context, "Comando no válido en este estado * "+comandos)
        return

    """Evaluamos el juego a ver quién ha ganado"""
    mensaje = ""
    if jugada == None:
        mensaje = "Aún no se ha abierto el juego. <i>Usa el comando open</i>"
    else:
        if not jugada.esCompleto():
            mensaje = "El juego aún no esta completo. Esperando que se unan más jugadores."
        else:
            if len(jugada.jugadores) == 0:
                mensaje = "Error. No se añadió ningún jugador."
            else:
                mensaje = evaluar()
                # juego, ganadores = jugada.establecerGanador()
                # mensaje = jugada.mostrar2()
                # jugadores = jugada.jugadores.copy()
                # jugada = Jugada()
                # jugada.jugadores = jugadores
                # jugada.setCompleto(False)
                # estado = PARTICIPAR

    await send(update, context, mensaje)


# Manejador: Fin del Juego
# ------------------------
# Permite finalizar las operaciones del bot y volver al estado inicial
# de ABRIR, lo que a su vez permitirá que se vuelva a iniciar el juego
# y se vuelvan a unir los jugadores.
#
async def end_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    global estado, jugada

    if estado != PARTICIPAR:
        comandos = comandosEstado()
        await send(update, context, "Comando no válido en este estado * "+comandos)
        return

    jugada = None
    mensaje = "Juego cerrado"
    estado = ABRIR
    await send(update, context, "Juego finalizado")


# Manejador: Pukit -  En deshuso
# ------------------------------
# Había previsto una especie de consola del administrador que se quedó
# sólo en el comienzo. Se conserva por si considero añadirla.
#
async def pukit_commands(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    # Solo responder a mhyst
    user = update.effective_user.username
    mensaje = "Nada que objetar"
    if user == "mhyst":
        print(user, update.message.text)
        # Obtén el mensaje del usuario
        message = update.message.text
        # Si el mensaje contiene "pbt"
        if message.startswith("pukit"):
            comando = message.split(".")
            if len(comando) == 1:
                mensaje = "Espero órdenes"
            else:
                parms = comando[1].split(" ")
                match parms[0]:
                    case "addFondos":
                        if len(parms) < 3:
                            mensaje = "Necesita indicar el nombre del jugador y la cantidad a añadir"
                        else:
                            jugador = jugada.getJugador(parms[1])
                            if jugador is None:
                                mensaje = "Ese jugador no existe"
                            else:
                                error = False
                                try:
                                    cantidad = int(parms[2])
                                except:
                                    error = True
                                if error:
                                    mensaje = "La cantidad debe ser un número entero"
                                else:
                                    jugador.addFondos(cantidad)
                                    mensaje = rf"La cantidad de {cantidad} fue añadida a los fondos de <b>{parms[1]}</b> que ahora cuenta con {jugador.getFondos()}"
                    case "resetFondos":
                        if len(parms) > 1:
                            error = False
                            try:
                                cantidad = int(parms[1])
                            except:
                                error = True
                            if error:
                                mensaje = "La cantidad debe ser un número entero"
                            else:
                                for jugador in jugada.jugadores:
                                    jugador.setFondos(cantidad)
                                mensaje = rf"Todos los jugadores tienen {cantidad}"
                        elif len(parms) == 1:
                            for jugador in jugada.jugadores:
                                jugador.setFondos(1000)
                            mensaje = "Todos los jugadores tienen 100"

            # Envía una respuesta al usuario
            await update.message.reply_html(mensaje)
            #await context.bot.send_message(chat_id=update.effective_chat.id, text=message)


# Manejador: Comando Desconocido
# ------------------------------
# Responde todos aquellos comandos para los cuales no existe un manejador.
#
async def unknown(update: Update, context: ContextTypes.DEFAULT_TYPE):
    comando = comandosEstado()
    await update.message.reply_html("Lo siento, no entiendo ese comando * "+comando)
    #await context.bot.send_message(chat_id=update.effective_chat.id, html="Lo siento, no entiendo ese comando * "+comando)


# Programa Principal
def main() -> None:
    """Start the bot."""
    # Create the Application and pass it your bot's token.
    application = Application.builder().token(token).build()


    # on different commands - answer in Telegram
    application.add_handler(CommandHandler("start", start))
    application.add_handler(CommandHandler("ayuda", help_command))

    # Crea un manejador de mensajes que responda a los mensajes de texto que contengan "pbt"
    application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, pukit_commands))


    application.add_handler(CommandHandler("abrir", open_command))

    application.add_handler(CommandHandler("entro", join_command))
    application.add_handler(CommandHandler("salgo", part_command))

    application.add_handler(CommandHandler("cerrar", close_command))

    application.add_handler(CommandHandler("jugadores", jugadores_command))
    application.add_handler(CommandHandler("ganancias", ganancias_command))

    application.add_handler(CommandHandler("sirve", serve_command))
    application.add_handler(CommandHandler("servido", served_command))

    application.add_handler(CommandHandler("subo", subo_command))
    application.add_handler(CommandHandler("paso", paso_command))
    application.add_handler(CommandHandler("veo", veo_command))
    application.add_handler(CommandHandler("novoy", novoy_command))

    application.add_handler(CommandHandler("terminar", end_command))

    application.add_handler(MessageHandler(filters.COMMAND, unknown))


    # Run the bot until the user presses Ctrl-C
    application.run_polling()


if __name__ == "__main__":
    main()
