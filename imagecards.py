#!/usr/bin/env python3

from PIL import Image


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
    def paint(cls, nombre, cartas):
        cartas = cls.convertirCartas(cartas)
        # Cargar la imagen con todas las cartas
        cartas_image = Image.open("ignorar/cartas.png")

        # Definir el tamaño de cada carta en la imagen original
        carta_width = cartas_image.width // 13  # Suponiendo 13 cartas por palo
        carta_height = cartas_image.height // 5  # Suponiendo 5 filas (4 palos + reverso)

        # Definir el espacio entre cada carta y alrededor
        espacio_entre_cartas = 20
        espacio_alrededor = 50

        # Crear una nueva imagen para el paño verde
        pano_width = carta_width * 5 + espacio_entre_cartas * 4 + espacio_alrededor * 2
        pano_height = carta_height + espacio_alrededor * 2
        pano_image = Image.new("RGB", (pano_width, pano_height), "green")

        # Calcular el desplazamiento horizontal para el centro de las cartas
        desplazamiento_x = (pano_width - (carta_width + espacio_entre_cartas) * 4) // 2

        # Calcular el desplazamiento vertical para centrar las cartas
        desplazamiento_y = (pano_height - carta_height) // 2

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
            carta_x_pano = desplazamiento_x//5 + i * (carta_width + espacio_entre_cartas) + espacio_alrededor
            carta_y_pano = desplazamiento_y//5 + espacio_alrededor

            # Pegar la carta recortada en el paño verde
            pano_image.paste(carta_recortada, (carta_x_pano, carta_y_pano))

        # Guardar la imagen resultante
        pano_image.save(rf"ignorar/cartas_{nombre}.png")

