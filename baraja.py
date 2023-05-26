import random

class Baraja:
    palos = ["P","C","T","D"]
    cartas = ["A","2","3","4","5","6","7","8","9","10","J","Q","K"]
    baraja = []

    def __init__(self):
        self.nueva()

    def nueva(self):
        self.baraja = []
        for palo in self.palos:
            for carta in self.cartas:
                self.baraja.append(carta + palo)

    def barajar(self):
        temp = self.baraja
        self.baraja = []

        while len(temp) > 0:
            i = random.randint(0, len(temp)-1)
            self.baraja.append( temp.pop(i) )

    def mostrar(self):
        cartas = ""
        for carta in self.baraja:
            cartas += carta+" "
        print (cartas)

    def darCartas(self, numero):
        dadas = []

        for i in range(numero):
            try:
                dadas.append(self.baraja.pop(0))
            except:
                raise Exception("No hay más cartas")

        return dadas

