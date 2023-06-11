from jugador import Jugador
from baraja import Baraja
from juego import Juego
from database import Database
from imagecards import ImageCards
import pdb

class Jugada:
    JUEGO_ESCALERA_COLOR = 0
    JUEGO_POKER = 1
    JUEGO_FULL = 2
    JUEGO_COLOR = 3
    JUEGO_ESCALERA = 4
    JUEGO_TRIO = 5
    JUEGO_DOBLE_PAR = 6
    JUEGO_PAR = 7
    JUEGO_CARTA_ALTA = 8


    jugadas = [["Straight flush","Escalera de color"],["Four of a kind","Poker"],["Full house","Full"],["Flush","Color"],["Straight","Escalera"],["Three of a kind","Trío"],["Two pair","Doble pareja"],["Pair","Par"],["High card","Carta más alta"]]


    card_values = {
        "2": 2,
        "3": 3,
        "4": 4,
        "5": 5,
        "6": 6,
        "7": 7,
        "8": 8,
        "9": 9,
        "10": 10,
        "J": 11,
        "Q": 12,
        "K": 13,
        "A": 14
    }

    valorPalos = {
        "P": 100,
        "T": 200,
        "C": 300,
        "D": 400
    }


    def __init__(self, cantidadInicial = 1000, topeGanador = 5000):
        self.cantidadInicial = cantidadInicial
        self.topeGanador = topeGanador
        self.jugadores = []
        self.baraja = Baraja()
        self.baraja.barajar()
        self.completo = False
        self.lastJuego = -1
        self.lastGanadores = []
        self.lastEmpate = False
        self.bote = 0
        self.ciega = 2
        self.apuestaMinima = 5
        self.lastApuesta = 0
        self.lastBote = 0
        self.rondaApuestas = -1
        self.lastRonda = 1
        self.turno = None
        self.idTurno = 0
        self.finJuego = False
        self.nTurno = 0
        self.subidaMaxima = 0
        self.db = Database("ignorar/jugadores.db")


    def addJugador(self, jugador):
        self.jugadores.append(jugador)


    def addJugadorByNombre(self, nombre, username=""):
        jugador = Jugador(nombre, username=username)
        jugador.setFondos(self.cantidadInicial)
        self.jugadores.append(jugador)
        fondos = self.db.existeJugador(nombre)
        if fondos == -1:
            self.db.insertJugador(nombre, self.cantidadInicial, username)
        else:
            jugador.setFondos(fondos)
        return jugador
    
    def removeJugador(self, jugador):
        self.jugadores.remove(jugador)

    def removeJugadorByNombre(self, nombre):
        j = None
        for index, jugador in enumerate(self.jugadores):
            if jugador.nombre == nombre:
                j = self.jugadores.pop(index)
                break
        return j


    def removeJugadorByUsername(self, nombre):
        j = None
        for index, jugador in enumerate(self.jugadores):
            if jugador.username == username:
                j = self.jugadores.pop(index)
                break
        return j

    def getJugador(self, nombre):
        j = None
        for jugador in self.jugadores:
            if jugador.nombre == nombre:
                j = jugador
                break
        return j

    def getJugadorByUsername(self, username):
        j = None
        for jugador in self.jugadores:
            if jugador.username == username:
                j = jugador
                break
        return j

    def estaJugando(self, nombre):
        nombres = [jugador.nombre for jugador in jugadores]
        return nombre in set(nombres)

    def esCompleto(self):
        return self.completo

    def setCompleto(self, completo):
        self.completo = completo

    def isFinJuego(self):
        return self.finJuego

    def toggleCompleto(self):
        self.completo = not self.completo

    def getSubidaMaxima(self):
        return self.subidaMaxima

    def writeJugadores(self):
        mydb = Database("ignorar/jugadores.db")
        for jugador in self.jugadores:
            mydb.updateJugador(jugador.getNombre(), jugador.getFondos())
        mydb.close()
           
    def setSubidaMaxima(self, cantidad):
        self.subidaMaxima = cantidad

    def repartirCartas(self):
        for jugador in self.jugadores:
            jugador.setCartas(self.baraja.darCartas(5))
       
        self.laCiega()
        self.completo = True

    def nuevaBaraja(self):
        self.baraja = Baraja()
        self.baraja.barajar()

    def servirJugador(self,jugador,ids):
        servicio= jugador.getServicio()
        if servicio + len(ids) > 5:
            served = 5 - servicio
            if served < 0:
                served = 0
            return served
        else:
            jugador.descartarServir(ids,self.baraja.darCartas(len(ids)))
            return len(ids)

    def servirJugadorByNombre(self, nombre, ids):
        jugador = self.getJugador(nombre)
        return self.servirJugador(jugador, ids)

    def laCiega(self):
        self.bote=0
        if len(self.jugadores) == 2:
            # Asignar una ciega grande al jugador
            self.jugadores[0].aumentarApuesta(2)
            self.lastApuesta = 2
            self.bote = 2
            self.idTurno = 1
        else:
            self.jugadores[0].aumentarApuesta(2)
            self.jugadores[1].aumentarApuesta(4)
            self.lastApuesta = 6
            self.bote = 6
            self.idTurno = 2

    def isServida(self):
        servido = True
        for jugador in self.jugadores:
            if not jugador.isServido():
                servido = False
                break
        return servido

    def verApuesta(self, jugador):
        if self.lastApuesta - jugador.getApuesta() > jugador.getFondos():
            return False
        else:
            resto = jugador.verApuesta(self.lastApuesta)
            self.bote += resto
            print(rf"{jugador.getNombre()} ve: montante: {self.lastApuesta} apuesta: {jugador.getApuesta()} cantidad: {resto} bote: {self.bote}")
            return True

    def subirApuesta(self,jugador,cantidad=5):
        cantidadtotal = (self.lastApuesta - jugador.getApuesta()) + cantidad
        if cantidadtotal <= jugador.getFondos():
            self.verApuesta(jugador)
            jugador.aumentarApuesta(cantidad)
            self.lastApuesta += cantidad
            self.bote += cantidad
            print(rf"{jugador.getNombre()} sube: montante: {self.lastApuesta} apuesta: {jugador.getApuesta()} cantidad: {cantidad} bote:{self.bote}")
            return True
        else:
            return False

    def getJugadoresApuestasRestantes(self):
        restantes = []
        print("DEBUG - lastApuesta:",self.lastApuesta)
        if len(self.jugadores) == 0:
                print("DEBUG - ERROR NO HAY JUGADORES")
        for jugador in self.jugadores:
            print("DEBUG - getJugadoresApuestasRestantes",jugador.getNombre(),jugador.getApuesta())
            if not jugador.isNovoy() and jugador.getApuesta() < self.lastApuesta:
                restantes.append(jugador)

        return restantes

    def getTurn(self):
        return self.turno

    def getIdTurn(self):
        return self.idTurno

    def setIdTurn(self, idTurno):
        self.idTurno = idTurno

    def increaseIdTurn(self, jugadores):
        self.idTurno += 1
        if self.idTurno == len(jugadores):
            self.idTurno = 0
        while jugadores[self.idTurno].isNovoy():
            self.idTurno += 1
            if self.idTurno == len(jugadores):
                self.idTurno = 0

    def isFinApuesta(self, jugs):
        finApuesta=True

        if len(jugs) == 1:
            # Todos han abandonado la partida menos uno
            self.finJuego = True
            self.lastGanadores.append(jugs[0])
            return True

        if self.lastApuesta == 0:
            finApuesta=False
        elif self.rondaApuestas == 2 and self.lastRonda != self.rondaApuestas:
            self.lastRonda = self.rondaApuestas
            self.idTurn = 0
            finApuesta=False
        else:
            if self.nTurno == 1:
                return False
            for jugador in jugs:
                print(jugador.getNombre(),jugador.getApuesta())
                if jugador.getApuesta() < self.lastApuesta:
                    finApuesta = False
                    break
        return finApuesta


    def nextTurn(self, noincrement=False):
        turno = None

        jugs = [jugador for jugador in self.jugadores if not jugador.isNovoy()]

        if self.isFinApuesta(jugs):
            turno = None
        else:
            if not noincrement:
                self.nTurno += 1
            turno = jugs[self.getIdTurn()]
            if turno is None:
                self.increaseIdTurn(jugs)
                turno = jugs[self.IdTurn()]
            self.increaseIdTurn(jugs)
        
        self.turno = turno
        return turno

    def repartirBote(self, ganadores):
        n = len(ganadores)
        if n == 1:
            ganadores[0].ganaApuesta(self.bote)
        else:
            parte = bote / n
            for ganador in ganadores:
                ganador.ganaApuesta(parte)
    
        self.lastBote = self.bote
        self.bote = 0

        # Escribimos los jugadores a dico
        self.writeJugadores()


    def establecerGanador(self):

        menorJuego = 9
        cont = 0
        empate = False
        ganadores = []

        for index, jugador in enumerate(self.jugadores):
            juego, carta1, carta2 = Jugada.mejorJugada(jugador.getCartas())

            #Asignar jugada a cada jugador
            jugador.setLastJuego(Juego(juego,carta1,carta2,jugador.getCartas()))
            #jugador.lastJuego = juego
            #jugador.lastCarta1 = carta1
            #jugador.lastCarta2 = carta2

            #Encontrar el mejor juego
            if juego < menorJuego:
                menorJuego = juego
        

        #Encontrar jugadores que tienen el mejor juego
        for index, jugador in enumerate(self.jugadores):
            if jugador.getLastJuego().getJuego() == menorJuego:
                ganadores.append(jugador)

        
        #Tomar nota del resultado
        self.lastJuego = menorJuego
        self.lastGanadores = ganadores
        self.lastEmpate = False

        if len(ganadores) > 1:

            #Resolver el desempate
            mayorJuego = 0
            valoresJuego = [0 for ganador in ganadores]
            desGanadores = []

            for index, ganador in enumerate(ganadores):
                #Almacenar el juego de cada uno
                valoresJuego[index] = Jugada.valorJugada(ganador)
                print("DEBUG - valor",ganador.getNombre(),valoresJuego[index])
                if valoresJuego[index] > mayorJuego:
                    mayorJuego = valoresJuego[index]

            
            for index,valor in enumerate(valoresJuego):
                if valor == mayorJuego:
                    desGanadores.append(ganadores[index])

            self.lastGanadores = desGanadores

            #Sigue habiendo varios ganadores?
            if len(desGanadores) > 1:
                print("DEBUG - ERROR: EMPATE!!!")
                self.lastEmpate = True
                
                #Mirar si es por carta más alta
                if menorJuego == Jugada.JUEGO_CARTA_ALTA:

                    #En ese caso mirar segunda carta más alta
                    desGanadores = self.empateCartaMasAlta(desGanadores)
                    if len(desGanadores) == 1:
                        self.lastEmpate = False

        
            ganadores = desGanadores


        self.repartirBote(ganadores)

        return menorJuego, ganadores

    def empateCartaMasAlta(self, ganadores):
        cartaMayor = 0
        for ganador in ganadores:
            if ganador.getLastJuego().getC2() > cartaMayor:
                cartaMayor = ganador.getLastJuego().getC2()

        desGanadores = []
        for ganador in ganadores:
            if ganador.getLastJuego().getC2() == cartaMayor:
                desGanadores.append(ganador)

        return desGanadores


    def mostrar(self):
        print("Jugadores")
        print("---------")
        for jugador in self.jugadores:
            jugador.mostrar()

        if len(self.lastGanadores) == 1:
            ganador = self.lastGanadores[0]
            print()
            print("Ganador:",ganador.getNombre(),"- Juego:",self.jugadas[self.lastJuego][1])
            #print("Carta1 del juego:",ganador.lastCarta1,"Carta2 del juego:",ganador.lastCarta2)
        else:
            nombres = [ganador.getNombre() for ganador in self.lastGanadores]
            print("Fue un empate a", self.jugadas[self.lastJuego][1],"entre:",nombres)


    def mostrar2(self):
        message = "<b><u>Jugadores</u></b>\n\n"
        #message += "---------------------------------------------------------\n"
        for jugador in self.jugadores:
            message += jugador.mostrar2()

        img_filename = ImageCards.paintJugadores(self.jugadores)


        if len(self.lastGanadores) == 1:
            ganador = self.lastGanadores[0]
            message += "\n"
            message += rf"Ganador: <b>{ganador.getNombre()}</b> - Juego: <b>{self.jugadas[self.lastJuego][1]}</b> Ganancias: <b>{str(ganador.getLastGanado())}</b>"
            #print("Carta1 del juego:",ganador.lastCarta1,"Carta2 del juego:",ganador.lastCarta2)
        else:
            nombres = [ganador.getNombre() for ganador in self.lastGanadores]
            snombres = ', '.join(nombres)
            message += rf"Fue un empate a <b>{self.jugadas[self.lastJuego][1]}</b> entre: <b>{snombres}</b> se reparten <b>{str(self.lastBote)}</b>"

        # Mostrar tabla de ganancias
        message += "\n\n<b><u>Ganancias</u></b>\n\n"
        #message += "---------------\n"
        
        sjugadores = self.jugadores.copy()
        sjugadores.sort(key=lambda jugador: jugador.apuesta)
        for jugador in sjugadores:
            message += rf"<b>{jugador.getNombre()}</b> <b>{jugador.getFondos()}</b>"
            message += "\n"
        message += "\n"


        return img_filename, message
            


# Función para determinar la mejor mano

    @classmethod
    def mejorJugada(cls,hand):
        flush = False
        straight = False
        four_kind = False
        three_kind = False
        pairs = []
        carta = -1

        # Verificar si hay flush
        if len(set([card[-1] for card in hand])) == 1:
            flush = True

        # Verificar si hay straight
        values = sorted([cls.card_values[card[:-1]] for card in hand])
        if values == [2, 3, 4, 5, 14]:
            values = [1, 2, 3, 4, 5]
        if len(set(values)) == 5 and values[4] - values[0] == 4:
            straight = True

        # Verificar si hay four of a kind, three of a kind, y pairs
        for value in set(values):
            count = values.count(value)
            if count == 4:
                carta = value
                four_kind = True
                break
            elif count == 3:
                carta = value
                three_kind = True
            elif count == 2:
                carta = value
                pairs.append(value)

        #print("#DEBUG mejorjugada: ", values)
        # Determinar la mejor mano
        if flush and straight:
            return 0, values[4], -1 #"Straight flush"
        elif four_kind:
            return 1, carta, -1 #"Four of a kind"
        elif three_kind and len(set(pairs)) == 1:
            return 2, carta, pairs[0] #"Full house"
        elif flush:
            return 3, values[4], -1 #"Flush"
        elif straight:
            return 4, values[4], -1 #"Straight"
        elif three_kind:
            return 5, carta, -1 #"Three of a kind"
        elif len(set(pairs)) == 2:
            return 6, pairs[0], pairs[1] #"Two pair"
        elif len(set(pairs)) == 1:
            return 7, carta, -1 #"Pair"
        else:
            return 8, values[4], values[3] #"High card"

    """ 
    Se trata de calcular el valor de una jugada
    teniendo en cuenta el palo. Serirá solo de
    cara al desempate.
    """

    @classmethod
    def valorJugada(cls, jugador):
        match jugador.getLastJuego().getJuego():
            case cls.JUEGO_ESCALERA_COLOR:
                return 1000 + jugador.getLastJuego().getC1()
            case cls.JUEGO_POKER:
                return 900 + jugador.getLastJuego().getC1()
            case cls.JUEGO_FULL:
                return 800 + jugador.getLastJuego().getC1() + jugador.getLastJuego().getC2()
            case cls.JUEGO_COLOR:
                return 700 + jugador.getLastJuego().getC1()
            case cls.JUEGO_ESCALERA:
                return 600 + jugador.getLastJuego().getC1()
            case cls.JUEGO_TRIO:
                return 500 + jugador.getLastJuego().getC1()
            case cls.JUEGO_DOBLE_PAR:
                return 400 + jugador.getLastJuego().getC1() + jugador.getLastJuego().getC2()
            case cls.JUEGO_PAR:
                return 300 + jugador.getLastJuego().getC1()
            case cls.JUEGO_CARTA_ALTA:
                values = sorted([Jugada.card_values[card[:-1]] for card in jugador.getCartas()])
                valor = 0
                for index, value in enumerate(values):
                    valor += value*index

                return valor
		
    
    def evaluarResultado(self):
        juego, ganadores = self.establecerGanador()
        img_filename, mensaje = self.mostrar2()
        return img_filename, mensaje
