class Juego:

    def __init__(self, juego, c1, c2, cartas):
        self.juego = juego
        self.c1 = c1
        self.c2 = c2
        self.cartas = cartas

    def getJuego(self):
        return self.juego

    def getJuegoStr(self):
        return Jugada.jugadas[self.juego][1]

    def setJuego(self, juego):
        self.juego = juego

    def getC1(self):
        return self.c1

    def setC1(self, c1):
        self.c1 = c1

    def getC2(self):
        return self.c2

    def setC2(self, c2):
        self.c2 = c2

    def getCartas(self):
        return self.cartas

    def setCartas(self, cartas):
        self.cartas = cartas
