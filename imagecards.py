#!/usr/bin/env python3

from PIL import Image, ImageDraw, ImageFont
import tempfile


class ImageCards:
    
    @classmethod
    def convertirCartas(cls, cartas):
        ncartas = []
        for carta in cartas:
            if carta[:-1] == "A":
                numero = "1"
            elif carta[:-1] == "K":
                numero = "13"
            elif carta[:-1] == "Q":
                numero = "12"
            elif carta[:-1] == "J":
                numero = "11"
            else:
                numero = carta[:-1]
            ncartas.append(numero+carta[-1])
        return ncartas

    @classmethod
    def mktemp(cls):
        return tempfile.NamedTemporaryFile(suffix='.png').name

    @classmethod
    def paint(cls, nombre, cartas):
        cartas = cls.convertirCartas(cartas)
        # Cargar la imagen con todas las cartas
        cartas_image = Image.open("pics/cartas-l1.png")
        # print(cartas_image.format, cartas_image.size, cartas_image.mode)

        # Definir el tamaño de cada carta en la imagen original
        carta_width = cartas_image.width // 13  # Suponiendo 13 cartas por palo
        carta_height = cartas_image.height // 5  # Suponiendo 5 filas (4 palos + reverso)
        # print(rf"carta_width: {carta_width} carta_height: {carta_height}")

        # Definir el espacio entre cada carta y alrededor
        espacio_entre_cartas = 20
        espacio_alrededor = 50

        # Crear una nueva imagen para el paño verde
        pano_width = carta_width * 5 + espacio_entre_cartas * 4 + espacio_alrededor * 2
        pano_height = carta_height + espacio_alrededor * 2
        pano_image = Image.new("RGB", (pano_width, pano_height), "green")
        # print(rf"pano_width: {pano_width} pano_height: {pano_height}")


        # Colocar las cartas en el paño verde
        for i, carta in enumerate(cartas):
            # Obtener el número y palo de la carta
            numero = carta[:-1]
            palo = carta[-1]

            # Calcular las coordenadas de la carta en la imagen original
            carta_row = {"T": 0, "C": 1, "P": 2, "D": 3}[palo]
            carta_col = int(numero) - 1
            carta_x = carta_col * carta_width
            carta_y = carta_row * carta_height

            # Recortar la carta de la imagen original
            carta_recortada = cartas_image.crop((carta_x, carta_y, carta_x + carta_width, carta_y + carta_height))

            # Calcular las coordenadas de la carta en el paño verde
            carta_x_pano = i * (carta_width + espacio_entre_cartas) + espacio_alrededor
            carta_y_pano = 50
            # print(rf"carta_x_pano: {carta_x_pano} carta_y_pano: {carta_y_pano}")

            # Pegar la carta recortada en el paño verde
            pano_image.paste(carta_recortada, (carta_x_pano, carta_y_pano))

        # Guardar la imagen resultante
        filename = ImageCards.mktemp()
        pano_image.save(filename)
        return filename



    @classmethod
    def paintJugadores(cls, jugadores):
        # Cargar la imagen con todas las cartas
        cartas_image = Image.open("pics/cartas-l2.png")
        # print(cartas_image.format, cartas_image.size, cartas_image.mode)

        # Definir el tamaño de cada carta en la imagen original
        carta_width = cartas_image.width // 13  # Suponiendo 13 cartas por palo
        carta_height = cartas_image.height // 5  # Suponiendo 5 filas (4 palos + reverso)
        # print(rf"carta_width: {carta_width} carta_height: {carta_height}")

        # Definir el espacio entre cada carta y alrededor
        espacio_entre_cartas = 20
        espacio_alrededor = 50

        # Crear una nueva imagen para el paño verde
        pano_width = carta_width * 5 + espacio_entre_cartas * 4 + espacio_alrededor * 2
        pano_height = len(jugadores) * (carta_height + espacio_alrededor) + espacio_alrededor
        pano_image = Image.new("RGB", (pano_width, pano_height), "green")
        # print(rf"pano_width: {pano_width} pano_height: {pano_height}")
        draw = ImageDraw.Draw(pano_image)
        font = ImageFont.truetype("/usr/share/fonts/truetype/ubuntu-font-family/Ubuntu-R.ttf", 24)
        #font.set_variation_by_name('Bold')


        for idx, jugador in enumerate(jugadores):
            cartas = cls.convertirCartas(jugador.getCartasOrden2())

            # Colocar las cartas en el paño verde
            for i, carta in enumerate(cartas):
                # Obtener el número y palo de la carta
                numero = carta[:-1]
                palo = carta[-1]

                # Calcular las coordenadas de la carta en la imagen original
                carta_row = {"T": 0, "C": 1, "P": 2, "D": 3}[palo]
                carta_col = int(numero) - 1
                carta_x = carta_col * carta_width
                carta_y = carta_row * carta_height

                # Recortar la carta de la imagen original
                carta_recortada = cartas_image.crop((carta_x, carta_y, carta_x + carta_width, carta_y + carta_height))

                # Calcular las coordenadas de la carta en el paño verde
                carta_x_pano = i * (carta_width + espacio_entre_cartas) + espacio_alrededor
                carta_y_pano = 60+idx*(carta_height+60)
                # print(rf"carta_x_pano: {carta_x_pano} carta_y_pano: {carta_y_pano}")

                draw.text((50,60+idx*(carta_height+60)-40),jugador.getNombre(),font=font)

                # Pegar la carta recortada en el paño verde
                pano_image.paste(carta_recortada, (carta_x_pano, carta_y_pano))

        # Guardar la imagen resultante
        filename = ImageCards.mktemp()
        pano_image.save(filename)
        return filename
