import sqlite3
import os.path

class Database:
    def __init__(self, filename):
        preexisted = False
        if Database.exists(filename):
            preexisted = True
        self.filename = filename
        self.con = sqlite3.connect(filename)
        if not preexisted:
            self.createScheme()

    @classmethod
    def exists(cls, filename):
        return os.path.exists(filename)

    def executeUpdate(self, query):
        cur = self.con.cursor()
        res = cur.execute(query)
        self.con.commit()
        return res

    def execute(self, query):
        cur = self.con.cursor()
        res = cur.execute(query)
        return res

    def createScheme(self):
        cur = self.con.cursor()
        cur.execute("CREATE TABLE jugadores (nombre TEXT primary key, fondos INTEGER)")

    def existeJugador(self, nombre):
        query = rf"select fondos from jugadores where nombre = '{nombre}'"
        res = self.execute(query)
        data = res.fetchone()
        if data is None:
            return -1
        else:
            return data[0]

    def insertJugador(self, nombre, fondos):
        query = rf"insert into jugadores values ('{nombre}', {fondos})"
        res = self.executeUpdate(query)

    def updateJugador(self, nombre, fondos):
        if self.existeJugador(nombre):
            query = rf"update jugadores set fondos = {fondos} where nombre = '{nombre}'"
            self.executeUpdate(query)
            return True
        else:
            return False
