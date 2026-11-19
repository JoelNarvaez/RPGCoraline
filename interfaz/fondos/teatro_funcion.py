"""
SEGUNDA PARTE DE LA FUNCION DEL TEATRO.

UN PERRITO LE OFRECE CHOCOLATES A CORALINE.
MIENTRAS TANTO, EL TRUCO DE LAS ACTRICES SALE MAL.
"""

import math
import pygame

from interfaz.fondos.pintura import ANCHO, ALTO, brillo, mostrar
from interfaz.fondos import teatro_vecinas
from interfaz.fondos import personajes


CAPAS = {}


# --------------------------------------------------
# AMBIENTE DE LA SEGUNDA FUNCION
# --------------------------------------------------

def dibujar_ambiente_inquietante(lienzo):

    """CAMBIA LA ILUMINACION CALIDA POR UNA TONALIDAD EXTRAÑA."""

    ambiente = pygame.Surface(
        (ANCHO, ALTO),
        pygame.SRCALPHA
    )

    # TONO OSCURO GENERAL

    ambiente.fill((25, 8, 35, 32))

    # REFLEJO ROJIZO SOBRE EL ESCENARIO

    pygame.draw.rect(
        ambiente,
        (105, 20, 55, 28),
        (245, 65, 390, 210)
    )

    lienzo.blit(
        ambiente,
        (0, 0)
    )


# --------------------------------------------------
# TRUCO DE MAGIA
# --------------------------------------------------

def dibujar_aura_magica(lienzo, tiempo):

    """ILUMINACION EXTRAÑA ANTES DEL ACCIDENTE."""

    pulso = abs(math.sin(tiempo * 3))

    intensidad = int(35 + pulso * 25)

    brillo(
        lienzo,
        (505, 160),
        125,
        (155, 45, 145),
        intensidad
    )

    brillo(
        lienzo,
        (505, 150),
        65,
        (230, 65, 105),
        28
    )


def dibujar_truco_fallido(lienzo, tiempo):

    """HUMO Y DESTELLOS DEL TRUCO QUE SALE TERRIBLEMENTE MAL."""

    centro_x = 505
    centro_y = 145

    pulso = int(abs(math.sin(tiempo * 4)) * 8)

    # HUMO DEL TRUCO

    humo = pygame.Surface(
        (210, 145),
        pygame.SRCALPHA
    )

    pygame.draw.ellipse(
        humo,
        (45, 15, 58, 75),
        (25, 50 + pulso, 155, 65)
    )

    pygame.draw.ellipse(
        humo,
        (82, 24, 88, 85),
        (48, 25 + pulso, 120, 75)
    )

    pygame.draw.circle(
        humo,
        (120, 42, 105, 65),
        (105, 65 + pulso),
        35
    )

    pygame.draw.circle(
        humo,
        (65, 20, 75, 70),
        (145, 75 + pulso),
        28
    )

    lienzo.blit(
        humo,
        (centro_x - 105, centro_y - 65)
    )

    # DESTELLOS ALREDEDOR DEL HUMO

    for i in range(12):

        angulo = tiempo * 2 + i * 0.75

        distancia = 38 + abs(
            math.sin(tiempo * 3 + i)
        ) * 42

        x = int(
            centro_x + math.cos(angulo) * distancia
        )

        y = int(
            centro_y + math.sin(angulo) * distancia
        )

        radio = 2 + int(
            abs(math.sin(tiempo * 5 + i)) * 3
        )

        pygame.draw.circle(
            lienzo,
            (225, 105, 195),
            (x, y),
            radio
        )

        pygame.draw.circle(
            lienzo,
            (255, 215, 240),
            (x, y),
            1
        )

    # CHISPAS ROJIZAS

    for i in range(7):

        x = centro_x - 42 + i * 14

        desplazamiento = int(
            math.sin(tiempo * 5 + i) * 12
        )

        y = centro_y + desplazamiento

        pygame.draw.line(
            lienzo,
            (235, 75, 110),
            (x - 5, y - 5),
            (x + 5, y + 5),
            2
        )

        pygame.draw.line(
            lienzo,
            (255, 190, 215),
            (x + 5, y - 5),
            (x - 5, y + 5),
            2
        )

    # FRAGMENTOS DE LUZ QUE SALEN DESPEDIDOS

    for i in range(5):

        angulo = tiempo * 1.5 + i * 1.25

        distancia = 55 + i * 8

        x = int(
            centro_x + math.cos(angulo) * distancia
        )

        y = int(
            centro_y + math.sin(angulo) * distancia
        )

        pygame.draw.line(
            lienzo,
            (255, 165, 205),
            (x - 3, y - 6),
            (x + 3, y + 6),
            2
        )


# --------------------------------------------------
# PERRITO QUE OFRECE CHOCOLATES
# --------------------------------------------------

def dibujar_bolsita(lienzo, tiempo):

    """BOLSITA DE CHOCOLATES QUE EL PERRITO LE OFRECE A CORALINE."""

    movimiento = int(
        math.sin(tiempo * 3) * 2
    )

    x = 442
    y = 329 + movimiento

    # SOMBRA

    pygame.draw.ellipse(
        lienzo,
        (15, 10, 20),
        (x - 2, y + 20, 31, 7)
    )

    # CUERPO DE LA BOLSITA

    pygame.draw.polygon(
        lienzo,
        (105, 57, 39),
        [
            (x, y),
            (x + 27, y),
            (x + 25, y + 22),
            (x + 3, y + 22)
        ]
    )

    pygame.draw.polygon(
        lienzo,
        (165, 105, 65),
        [
            (x + 3, y + 2),
            (x + 24, y + 2),
            (x + 21, y + 19),
            (x + 5, y + 19)
        ]
    )

    # PARTE SUPERIOR ABIERTA

    pygame.draw.polygon(
        lienzo,
        (205, 157, 100),
        [
            (x, y),
            (x + 7, y - 6),
            (x + 15, y - 2),
            (x + 22, y - 6),
            (x + 27, y)
        ]
    )

    # CHOCOLATES VISIBLES

    pygame.draw.ellipse(
        lienzo,
        (55, 25, 30),
        (x + 4, y - 5, 8, 8)
    )

    pygame.draw.ellipse(
        lienzo,
        (75, 34, 36),
        (x + 13, y - 7, 9, 8)
    )

    pygame.draw.circle(
        lienzo,
        (145, 76, 60),
        (x + 8, y - 3),
        2
    )

    pygame.draw.circle(
        lienzo,
        (155, 83, 65),
        (x + 18, y - 5),
        2
    )

    # CINTA DE LA BOLSITA

    pygame.draw.line(
        lienzo,
        (145, 45, 70),
        (x + 5, y + 11),
        (x + 23, y + 11),
        2
    )

    pygame.draw.circle(
        lienzo,
        (210, 95, 115),
        (x + 14, y + 11),
        3
    )

    # PEQUENO REFLEJO

    pygame.draw.line(
        lienzo,
        (235, 190, 140),
        (x + 5, y + 5),
        (x + 7, y + 15),
        1
    )


def dibujar_perrito_chocolates(lienzo, tiempo):

    """PERRITO EN PRIMER PLANO, FRENTE A CORALINE."""

    # EL PERRO MIRA HACIA LA IZQUIERDA

    personajes.dibujar_perro(
        lienzo,
        510,
        350,
        tiempo,
        0.5
    )

    # LA BOLSITA QUEDA ENTRE EL PERRO Y CORALINE

    dibujar_bolsita(
        lienzo,
        tiempo
    )

    # BRILLO SUAVE SOBRE LOS CHOCOLATES

    pulso = abs(math.sin(tiempo * 2))

    intensidad = int(15 + pulso * 12)

    brillo(
        lienzo,
        (456, 331),
        25,
        (220, 145, 90),
        intensidad
    )


# --------------------------------------------------
# APLAUSOS DEL PUBLICO
# --------------------------------------------------

def dibujar_aplausos(lienzo, tiempo):

    """PEQUENAS MARCAS DE MOVIMIENTO SOBRE LOS PERRITOS."""

    posiciones = [
        (63, 264),
        (173, 264),
        (283, 264),
        (503, 264),
        (53, 314),
        (163, 314),
        (273, 314),
        (523, 314)
    ]

    for i in range(len(posiciones)):

        x = posiciones[i][0]
        y = posiciones[i][1]

        movimiento = abs(
            math.sin(tiempo * 7 + i)
        )

        if movimiento > 0.45:

            pygame.draw.arc(
                lienzo,
                (205, 155, 125),
                (x - 7, y - 9, 12, 12),
                0.3,
                2.4,
                2
            )

            pygame.draw.arc(
                lienzo,
                (205, 155, 125),
                (x + 2, y - 9, 12, 12),
                0.7,
                2.8,
                2
            )


# --------------------------------------------------
# FONDO FIJO
# --------------------------------------------------

def crear_fijo():

    """REUTILIZAMOS EL TEATRO ORIGINAL."""

    return teatro_vecinas.crear_fijo()


# --------------------------------------------------
# DIBUJO PRINCIPAL
# --------------------------------------------------

def dibujar(ventana):

    """COMPONE LA SEGUNDA PARTE DE LA FUNCION."""

    if "fijo" not in CAPAS:

        CAPAS["fijo"] = crear_fijo()

    tiempo = pygame.time.get_ticks() / 1000

    lienzo = CAPAS["fijo"].copy()

    # CAMBIO DE AMBIENTE

    dibujar_ambiente_inquietante(
        lienzo
    )

    # LUCES DEL TEATRO

    teatro_vecinas.dibujar_focos(
        lienzo,
        tiempo
    )

    # RESPLANDOR DETRAS DE LAS ACTRICES

    dibujar_aura_magica(
        lienzo,
        tiempo
    )

    # ACTRICES

    teatro_vecinas.dibujar_actrices(
        lienzo,
        tiempo
    )

    # PUBLICO

    teatro_vecinas.dibujar_perritos(
        lienzo,
        tiempo
    )

    dibujar_aplausos(
        lienzo,
        tiempo
    )

    # CORALINE

    teatro_vecinas.dibujar_coraline(
        lienzo
    )

    # PERRITO Y CHOCOLATES EN PRIMER PLANO

    dibujar_perrito_chocolates(
        lienzo,
        tiempo
    )

    # ACCIDENTE MAGICO

    dibujar_truco_fallido(
        lienzo,
        tiempo
    )

    # MOSTRAR ESCENA

    mostrar(
        ventana,
        lienzo
    )