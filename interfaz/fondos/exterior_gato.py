"""FONDO DEL EXTERIOR DE LA OTRA CASA.

CASA ROSA INSPIRADA EN EL PINK PALACE,
CON JARDIN, CAMINO DE PIEDRA Y EL GATO NEGRO.
"""

import math
import pygame

from interfaz.fondos.pintura import ANCHO, ALTO
from interfaz.fondos.pintura import degradado, brillo
from interfaz.fondos.pintura import armar_sprite, pegar_con_contorno
from interfaz.fondos.pintura import orillas_oscuras, mostrar
from interfaz.fondos import personajes


CAPAS = {}


# --------------------------------------------------
# CIELO Y JARDIN
# --------------------------------------------------

def dibujar_cielo(lienzo):

    """CIELO DEL OTRO MUNDO."""

    degradado(
        lienzo,
        pygame.Rect(0, 0, ANCHO, ALTO),
        (35, 39, 68),
        (111, 78, 100),
        18
    )

    # LUNA

    pygame.draw.circle(
        lienzo,
        (210, 202, 180),
        (555, 65),
        24
    )

    pygame.draw.circle(
        lienzo,
        (55, 47, 73),
        (565, 56),
        22
    )

    # ESTRELLAS

    for i in range(25):

        x = (i * 53 + 17) % ANCHO
        y = (i * 31 + 12) % 145

        pygame.draw.rect(
            lienzo,
            (190, 173, 172),
            (x, y, 2, 2)
        )


def dibujar_arboles(lienzo):

    """ARBOLES OSCUROS ALREDEDOR DE LA CASA."""

    color_tronco = (48, 43, 53)
    color_hojas = (39, 48, 55)
    color_hojas2 = (52, 58, 62)

    # ARBOL IZQUIERDO

    pygame.draw.polygon(
        lienzo,
        color_tronco,
        [
            (0, 120),
            (35, 120),
            (53, 300),
            (0, 300)
        ]
    )

    for x, y, radio in [
        (10, 105, 38),
        (50, 135, 35),
        (5, 170, 40),
        (75, 185, 30),
        (25, 220, 34)
    ]:

        pygame.draw.circle(
            lienzo,
            color_hojas,
            (x, y),
            radio
        )

    # ARBOL DERECHO

    pygame.draw.polygon(
        lienzo,
        color_tronco,
        [
            (590, 100),
            (620, 100),
            (640, 300),
            (570, 300)
        ]
    )

    for x, y, radio in [
        (595, 115, 32),
        (630, 155, 40),
        (580, 185, 35),
        (635, 220, 36)
    ]:

        pygame.draw.circle(
            lienzo,
            color_hojas2,
            (x, y),
            radio
        )


def dibujar_terreno(lienzo):

    """JARDIN COMPLETO PARA EVITAR ESPACIOS NEGROS."""

    pygame.draw.rect(
        lienzo,
        (59, 72, 57),
        (0, 255, ANCHO, 105)
    )

    pygame.draw.rect(
        lienzo,
        (73, 84, 60),
        (0, 260, ANCHO, 100)
    )

    # PEQUENOS MONTICULOS DE PASTO

    for x, y, ancho, alto in [
        (0, 270, 120, 35),
        (95, 280, 110, 35),
        (440, 278, 110, 35),
        (555, 265, 85, 40)
    ]:

        pygame.draw.ellipse(
            lienzo,
            (81, 93, 61),
            (x, y, ancho, alto)
        )

    # CAMINO DE PIEDRA

    pygame.draw.polygon(
        lienzo,
        (75, 69, 83),
        [
            (260, 360),
            (400, 360),
            (368, 280),
            (335, 260),
            (305, 280)
        ]
    )

    pygame.draw.polygon(
        lienzo,
        (112, 92, 91),
        [
            (270, 360),
            (285, 360),
            (320, 285),
            (310, 282)
        ]
    )

    # DIVISIONES DEL CAMINO

    for y in [300, 320, 340]:

        pygame.draw.line(
            lienzo,
            (45, 43, 59),
            (300 - (y - 300), y),
            (365 + (y - 300), y),
            2
        )

    # PIEDRAS DEL JARDIN

    for x, y in [
        (35, 300),
        (105, 327),
        (180, 295),
        (455, 320),
        (555, 300),
        (610, 330)
    ]:

        pygame.draw.ellipse(
            lienzo,
            (111, 100, 88),
            (x, y, 13, 6)
        )


# --------------------------------------------------
# CASA ROSA
# --------------------------------------------------

def dibujar_casa(lienzo):

    """FACHADA INSPIRADA EN LA CASA PINK PALACE."""

    # CUERPO PRINCIPAL

    pygame.draw.rect(
        lienzo,
        (194, 119, 131),
        (145, 145, 465, 145)
    )

    pygame.draw.rect(
        lienzo,
        (230, 151, 163),
        (155, 155, 445, 125)
    )

    # PARED LATERAL

    pygame.draw.polygon(
        lienzo,
        (158, 91, 108),
        [
            (600, 150),
            (630, 170),
            (630, 290),
            (600, 280)
        ]
    )

    # TECHO PRINCIPAL

    pygame.draw.polygon(
        lienzo,
        (72, 36, 42),
        [
            (125, 155),
            (350, 42),
            (615, 155),
            (600, 176),
            (350, 76),
            (145, 176)
        ]
    )

    pygame.draw.polygon(
        lienzo,
        (119, 57, 47),
        [
            (145, 155),
            (350, 55),
            (575, 155),
            (510, 155),
            (350, 90),
            (190, 155)
        ]
    )

    # SOMBRAS DEL TECHO

    pygame.draw.polygon(
        lienzo,
        (61, 29, 39),
        [
            (350, 55),
            (615, 155),
            (600, 176),
            (350, 76)
        ]
    )

    # CHIMENEA IZQUIERDA

    pygame.draw.rect(
        lienzo,
        (102, 49, 45),
        (205, 48, 25, 94)
    )

    pygame.draw.rect(
        lienzo,
        (64, 31, 39),
        (200, 45, 35, 13)
    )

    pygame.draw.rect(
        lienzo,
        (133, 65, 51),
        (209, 65, 9, 65)
    )

    # CHIMENEA DERECHA

    pygame.draw.rect(
        lienzo,
        (91, 42, 43),
        (500, 95, 22, 52)
    )

    pygame.draw.rect(
        lienzo,
        (55, 31, 40),
        (495, 91, 32, 9)
    )

    # GABLETE ROSA SUPERIOR

    pygame.draw.polygon(
        lienzo,
        (247, 170, 184),
        [
            (285, 157),
            (350, 85),
            (425, 157)
        ]
    )

    pygame.draw.polygon(
        lienzo,
        (255, 201, 205),
        [
            (310, 153),
            (350, 101),
            (405, 153)
        ]
    )

    # VENTANAS DEL GABLETE

    for x in [340, 365]:

        pygame.draw.rect(
            lienzo,
            (88, 69, 77),
            (x, 111, 18, 22)
        )

        pygame.draw.rect(
            lienzo,
            (128, 149, 150),
            (x + 2, 113, 14, 18)
        )

        pygame.draw.line(
            lienzo,
            (82, 68, 78),
            (x + 9, 113),
            (x + 9, 131),
            2
        )

        pygame.draw.line(
            lienzo,
            (82, 68, 78),
            (x + 2, 122),
            (x + 16, 122),
            2
        )

    # MARCO DE LA FACHADA

    pygame.draw.rect(
        lienzo,
        (173, 91, 111),
        (145, 153, 465, 9)
    )

    pygame.draw.line(
        lienzo,
        (250, 182, 183),
        (150, 164),
        (600, 164),
        2
    )

    # VENTANAS PRINCIPALES

    ventanas = [
        (178, 183),
        (235, 183),
        (430, 183),
        (510, 183)
    ]

    for x, y in ventanas:

        pygame.draw.rect(
            lienzo,
            (77, 52, 68),
            (x - 4, y - 4, 31, 49)
        )

        pygame.draw.rect(
            lienzo,
            (135, 151, 155),
            (x, y, 23, 41)
        )

        pygame.draw.rect(
            lienzo,
            (61, 48, 67),
            (x + 10, y, 3, 41)
        )

        pygame.draw.line(
            lienzo,
            (61, 48, 67),
            (x, y + 20),
            (x + 23, y + 20),
            3
        )

        pygame.draw.rect(
            lienzo,
            (235, 179, 179),
            (x - 4, y - 4, 31, 3)
        )

    # PUERTA PRINCIPAL

    pygame.draw.rect(
        lienzo,
        (88, 43, 64),
        (300, 213, 54, 77)
    )

    pygame.draw.rect(
        lienzo,
        (209, 78, 119),
        (305, 218, 44, 72)
    )

    pygame.draw.rect(
        lienzo,
        (237, 120, 151),
        (311, 224, 32, 66)
    )

    pygame.draw.rect(
        lienzo,
        (154, 49, 88),
        (315, 229, 23, 56)
    )

    pygame.draw.circle(
        lienzo,
        (246, 199, 102),
        (338, 258),
        3
    )

    # PORCHE

    pygame.draw.rect(
        lienzo,
        (247, 207, 196),
        (277, 204, 101, 8)
    )

    pygame.draw.rect(
        lienzo,
        (124, 66, 79),
        (280, 211, 8, 79)
    )

    pygame.draw.rect(
        lienzo,
        (124, 66, 79),
        (368, 211, 8, 79)
    )

    # ESCALONES

    pygame.draw.rect(
        lienzo,
        (105, 85, 91),
        (291, 290, 75, 7)
    )

    pygame.draw.rect(
        lienzo,
        (142, 110, 106),
        (282, 297, 93, 7)
    )


# --------------------------------------------------
# DEPARTAMENTO DE LAS VECINAS
# --------------------------------------------------

def dibujar_marquesina(lienzo):

    """LETRERO DE FOCOS INTEGRADO A LA FACHADA."""

    # PEQUENO LETRERO LATERAL

    pygame.draw.rect(
        lienzo,
        (65, 34, 49),
        (450, 145, 112, 25)
    )

    pygame.draw.rect(
        lienzo,
        (166, 91, 75),
        (454, 149, 104, 17)
    )

    pygame.draw.rect(
        lienzo,
        (78, 40, 48),
        (458, 153, 96, 9)
    )

    # FOCOS

    for x in range(460, 556, 12):

        pygame.draw.rect(
            lienzo,
            (245, 194, 130),
            (x, 148, 4, 3)
        )

        pygame.draw.rect(
            lienzo,
            (245, 194, 130),
            (x, 164, 4, 3)
        )


def dibujar_luces(lienzo, tiempo):

    """ANIMACION DE LOS FOCOS DE LA MARQUESINA."""

    for i in range(8):

        x = 462 + i * 12

        parpadeo = math.sin(tiempo * 3 + i * 1.4)

        if parpadeo > -0.1:

            color = (255, 216, 143)

        else:

            color = (143, 88, 75)

        brillo(
            lienzo,
            (x + 2, 158),
            10,
            (255, 177, 104),
            35 if parpadeo > 0.5 else 12
        )

        pygame.draw.rect(
            lienzo,
            color,
            (x, 156, 4, 4)
        )


# --------------------------------------------------
# MURO
# --------------------------------------------------

def dibujar_muro(lienzo):

    """MURO DE PIEDRA DEL JARDIN."""

    pygame.draw.rect(
        lienzo,
        (55, 47, 59),
        (465, 278, 175, 82)
    )

    pygame.draw.rect(
        lienzo,
        (104, 86, 91),
        (465, 278, 175, 7)
    )

    pygame.draw.line(
        lienzo,
        (154, 123, 112),
        (465, 278),
        (640, 278),
        2
    )

    for fila in range(3):

        y = 290 + fila * 22

        for columna in range(6):

            x = 468 + columna * 31

            if fila % 2 == 1:
                x = x - 14

            pygame.draw.rect(
                lienzo,
                (77, 65, 76),
                (x, y, 28, 18)
            )

            pygame.draw.line(
                lienzo,
                (115, 96, 96),
                (x + 2, y + 2),
                (x + 24, y + 2),
                1
            )


# --------------------------------------------------
# ESCENARIO COMPLETO
# --------------------------------------------------

def crear_fijo():

    """CONSTRUIMOS TODA LA ESCENA."""

    lienzo = pygame.Surface(
        (ANCHO, ALTO)
    )

    dibujar_cielo(lienzo)
    dibujar_arboles(lienzo)
    dibujar_terreno(lienzo)
    dibujar_casa(lienzo)
    dibujar_marquesina(lienzo)
    dibujar_muro(lienzo)

    # SOMBRAS Y PROFUNDIDAD

    orillas_oscuras(lienzo)

    return lienzo


def dibujar(ventana):

    """DIBUJAMOS EL ESCENARIO Y SUS ANIMACIONES."""

    if "fijo" not in CAPAS:

        CAPAS["fijo"] = crear_fijo()

    tiempo = pygame.time.get_ticks() / 1000

    lienzo = CAPAS["fijo"].copy()

    # LUCES DE LA MARQUESINA

    dibujar_luces(
        lienzo,
        tiempo
    )

    # GATO SOBRE EL MURO

    personajes.dibujar_gato(
        lienzo,
        530,
        278,
        False,
        tiempo
    )

    mostrar(
        ventana,
        lienzo
    )