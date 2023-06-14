from juego import Juego

class Jugador:
    def __init__(self, nombre, chat_id=-1, cartas=[], username=""):
        self.nombre = nombre
        self.cartas = cartas
        self.apuesta = 0
        self.fondos = 1000
        self.cartera = 0
        self.lastJuego = None
        self.chat_id = chat_id
        self.servicio = 0
        self.servido = False
        self.novoy = False
        self.pasado = False
        self.miTurno = False
        self.lastGanado = 0
        self.username = username
        self.privado = False


    def getNombre(self):
        return self.nombre

    def getUsername(self):
        return self.username

    def setUsername(self, username):
        self.username = username

    def isPrivado(self):
        return self.privado

    def setPrivado(self, privado):
        self.privado = privado

    def getChatId(self):
        return self.chat_id

    def setChatId(self, chat_id):
        self.chat_id = chat_id

    def setCartas(self, cartas):
        self.cartas = cartas

    def getCartas(self):
        return self.cartas

    def getCartasOrden(self):
        cartas = self.cartas

        # Definimos el orden de los valores y palos de las cartas
        valores = {'2': 2, '3': 3, '4': 4, '5': 5, '6': 6, '7': 7, '8': 8, '9': 9, '10': 10, 'J': 11, 'Q': 12, 'K': 13, 'A': 14 }

        # Definimos el orden de los valores y palos de las cartas
        palos = {'T': '♣', 'D': '♦', 'C': '♥', 'P': '♠'}
        
        # Función de ordenamiento personalizada
        def orden_cartas(carta):
            valor = valores[carta[:-1]]
            palo = palos[carta[-1]]
            return (valor, palo)
        
        # Ordenamos las cartas por valor y palo
        cartas_ordenadas = sorted(cartas, key=orden_cartas)
        
        # Construimos las cartas ordenadas con su palo correspondiente
        cartas_ordenadas = [next(k for k, v in valores.items() if v == valor) + palos[carta[-1]] if valor in valores.values() else carta for carta, valor in zip(cartas_ordenadas, map(lambda carta: valores[carta[:-1]], cartas_ordenadas))]
        
        return cartas_ordenadas


    def getCartasOrden2(self):
        cartas = self.cartas

        # Definimos el orden de los valores y palos de las cartas
        valores = {'2': 2, '3': 3, '4': 4, '5': 5, '6': 6, '7': 7, '8': 8, '9': 9, '10': 10, 'J': 11, 'Q': 12, 'K': 13, 'A': 14 }

        # Definimos el orden de los valores y palos de las cartas
        palos = {'T': 'T', 'D': 'D', 'C': 'C', 'P': 'P'}
        
        # Función de ordenamiento personalizada
        def orden_cartas(carta):
            valor = valores[carta[:-1]]
            palo = palos[carta[-1]]
            return (valor, palo)
        
        # Ordenamos las cartas por valor y palo
        cartas_ordenadas = sorted(cartas, key=orden_cartas)
        
        # Construimos las cartas ordenadas con su palo correspondiente
        cartas_ordenadas = [next(k for k, v in valores.items() if v == valor) + palos[carta[-1]] if valor in valores.values() else carta for carta, valor in zip(cartas_ordenadas, map(lambda carta: valores[carta[:-1]], cartas_ordenadas))]
        
        return cartas_ordenadas

    def getCartasBonitas(self):
        cartas = self.cartas

        palos = {'T': '♣', 'D': '♦', 'C': '♥', 'P': '♠'}
        
        cartas_bonitas = [carta[:-1]+palos[carta[-1]] for carta in cartas]

        
        return cartas_bonitas

    def isMiTurno(self):
        return self.miTurno

    def setMiTurno(self, miTurno):
        self.miTurno = miTurno

    def setApuesta(self, cantidad):
        self.apuesta = cantidad

    def getApuesta(self):
        return self.apuesta

    def getFondos(self):
        return self.fondos

    def setFondos(self, fondos):
        self.fondos = fondos

    def addFondos(self, cantidad):
        self.fondos += cantidad

    def getCartera(self):
        return self.cartera

    def setCartera(self, cartera):
        self.cartera = cartera

    def getLastJuego(self):
        return self.lastJuego

    def setLastJuego(self, juego):
        self.lastJuego = juego

    def getLastGanado(self):
        return self.lastGanado

    def isNovoy(self):
        return self.novoy

    def setNovoy(self, novoy):
        self.novoy = novoy

    def isPasado(self):
        return self.pasado

    def setPasado(self, pasado):
        self.pasado = pasado

    def descartar(self, ids=[]):
        #print("DEBUG - jugador.descartar", ids)
        ids = sorted(ids)
        for i in reversed(ids):
            #print("DEBUG - jugador.descartar", i)
            self.cartas.pop(i)

    def servir(self, cartas):
        for carta in cartas:
            self.cartas.append(carta)


    def descartarServir(self, ids=[], cartas=[]):
        self.descartar(ids)
        self.servir(cartas)
        self.servicio += len(ids)
        if self.servicio == 5:
            self.setServido(True)


    def getServicio(self):
        return self.servicio

    def setServicio(self, servicio):
        self.servicio = servicio

    def isServido(self):
        return self.servido

    def setServido(self, servido):
        self.servido = servido

    def getCartasOrdenadas(self):
        return self.cartas.sort()

    def aumentarApuesta(self, cantidad):
        self.apuesta += cantidad
        self.fondos -= cantidad

    def verApuesta(self, cantidad):
        cantidad = cantidad - self.apuesta
        self.apuesta += cantidad
        self.fondos -= cantidad
        return cantidad
    
    def ganaApuesta(self, bote):
        self.fondos += bote
        self.lastGanado = bote

    def setJuego(self, juego, cartas1, cartas2):
        self.lastJuego = juego
        self.lastCartas1 = cartas1
        self.lastCartas2 = cartas2
        self.lastCartas = self.cartas

    def getJuego(self):
        return self.lastJuego, self.lastCartas1, self.lastCartas2, self.lastCartas

    def mostrar(self):
        #print(self.nombre,self.getCartasOrden())
        print(self.nombre, self.cartas, self.getCartasOrden())

    def mostrar2(self):
        #print(self.nombre,self.getCartasOrden())
        cartas = '  '.join(self.getCartasOrden())
        return ""+self.nombre+": "+cartas+"\n"
