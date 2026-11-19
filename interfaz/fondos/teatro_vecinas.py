"""TEATRO DEL OTRO MUNDO.

LAS SENORITAS SPINK Y FORCIBLE PRESENTAN UNA FUNCION
ANTE UN PUBLICO FORMADO POR PERRITOS NEGROS.
"""

import math
import pygame

from interfaz.fondos.pintura import ANCHO, ALTO
from interfaz.fondos.pintura import degradado, brillo, orillas_oscuras, mostrar
from interfaz.fondos import personajes


CAPAS = {}


# --------------------------------------------------
# COLORES
# --------------------------------------------------

VINO = (83, 24, 39)
VINO_CLARO = (137, 43, 57)
ROJO = (157, 49, 59)
DORADO = (205, 158, 83)
DORADO_CLARO = (244, 205, 132)
NEGRO = (22, 18, 28)


# --------------------------------------------------
# PAREDES DEL TEATRO
# --------------------------------------------------

def dibujar_pared(lienzo):

    """PAREDES OSCURAS CON DETALLES DORADOS."""

    degradado(
        lienzo,
        pygame.Rect(0, 0, ANCHO, ALTO),
        (37, 25, 43),
        (86, 39, 52),
        18
    )

    # PANELES LATERALES

    for x in range(0, ANCHO, 55):

        pygame.draw.rect(
            lienzo,
            (58, 31, 45),
            (x, 0, 5, 245)
        )

        pygame.draw.line(
            lienzo,
            (112, 61, 65),
            (x + 7, 15),
            (x + 7, 230),
            1
        )

    # MOLDURA SUPERIOR

    pygame.draw.rect(
        lienzo,
        (47, 27, 38),
        (0, 0, ANCHO, 13)
    )

    pygame.draw.line(
        lienzo,
        DORADO,
        (0, 13),
        (ANCHO, 13),
        2
    )

    # CUADROS DECORATIVOS

    for x in [30, 95, 160, 540, 600]:

        pygame.draw.rect(
            lienzo,
            (48, 27, 38),
            (x, 35, 30, 45)
        )

        pygame.draw.rect(
            lienzo,
            DORADO,
            (x, 35, 30, 45),
            2
        )

        pygame.draw.circle(
            lienzo,
            (160, 112, 91),
            (x + 15, 55),
            7
        )


# --------------------------------------------------
# ARCO DEL ESCENARIO
# --------------------------------------------------

def dibujar_arco(lienzo):

    """MARCO GRANDE DEL ESCENARIO TEATRAL."""

    # ESTRUCTURA EXTERIOR

    pygame.draw.rect(
        lienzo,
        (36, 22, 32),
        (220, 30, 420, 225)
    )

    pygame.draw.rect(
        lienzo,
        DORADO,
        (225, 35, 410, 215),
        4
    )

    pygame.draw.rect(
        lienzo,
        (109, 42, 55),
        (235, 45, 390, 195)
    )

    # FONDO DEL ESCENARIO

    degradado(
        lienzo,
        pygame.Rect(245, 55, 370, 175),
        (57, 29, 49),
        (104, 42, 55),
        12
    )

    # DECORACION DEL FONDO

    for x in range(275, 615, 35):

        pygame.draw.circle(
            lienzo,
            (134, 67, 70),
            (x, 88),
            3
        )

    # LINEAS DEL ARCO

    pygame.draw.rect(
        lienzo,
        (174, 119, 70),
        (230, 40, 400, 7)
    )

    pygame.draw.rect(
        lienzo,
        (174, 119, 70),
        (230, 40, 7, 205)
    )

    pygame.draw.rect(
        lienzo,
        (174, 119, 70),
        (623, 40, 7, 205)
    )

    # ADORNOS DORADOS

    for x in range(245, 620, 30):

        pygame.draw.circle(
            lienzo,
            DORADO_CLARO,
            (x, 42),
            3
        )


# --------------------------------------------------
# CORTINAS
# --------------------------------------------------

def dibujar_cortinas(lienzo):

    """CORTINAS ROJAS CON PLIEGUES Y BORDE DORADO."""

    # CORTINA IZQUIERDA

    pygame.draw.polygon(
        lienzo,
        VINO,
        [
            (230, 42),
            (315, 42),
            (300, 85),
            (282, 135),
            (275, 235),
            (230, 245)
        ]
    )

    pygame.draw.polygon(
        lienzo,
        ROJO,
        [
            (230, 42),
            (268, 42),
            (258, 120),
            (263, 245),
            (230, 245)
        ]
    )

    pygame.draw.polygon(
        lienzo,
        VINO_CLARO,
        [
            (268, 42),
            (315, 42),
            (295, 120),
            (282, 235),
            (263, 245)
        ]
    )

    # CORTINA DERECHA

    pygame.draw.polygon(
        lienzo,
        VINO,
        [
            (545, 42),
            (630, 42),
            (630, 245),
            (585, 245),
            (582, 130),
            (560, 85)
        ]
    )

    pygame.draw.polygon(
        lienzo,
        ROJO,
        [
            (592, 42),
            (630, 42),
            (630, 245),
            (603, 245),
            (610, 130)
        ]
    )

    pygame.draw.polygon(
        lienzo,
        VINO_CLARO,
        [
            (545, 42),
            (592, 42),
            (610, 130),
            (603, 245),
            (585, 245),
            (582, 130)
        ]
    )

    # PLIEGUES

    for puntos in [
        [(248, 50), (250, 145), (242, 230)],
        [(270, 48), (267, 145), (274, 232)],
        [(289, 48), (281, 145), (280, 230)],
        [(575, 48), (586, 145), (590, 230)],
        [(605, 48), (610, 145), (615, 230)]
    ]:

        pygame.draw.lines(
            lienzo,
            (65, 23, 39),
            False,
            puntos,
            3
        )

    # CENEFA SUPERIOR

    pygame.draw.polygon(
        lienzo,
        (124, 39, 53),
        [
            (230, 40),
            (630, 40),
            (615, 68),
            (590, 59),
            (565, 68),
            (540, 59),
            (515, 68),
            (490, 59),
            (465, 68),
            (440, 59),
            (415, 68),
            (390, 59),
            (365, 68),
            (340, 59),
            (315, 68),
            (290, 59),
            (265, 68),
            (245, 59)
        ]
    )

    pygame.draw.line(
        lienzo,
        DORADO,
        (230, 42),
        (630, 42),
        3
    )


# --------------------------------------------------
# ESCENARIO Y PISO
# --------------------------------------------------

def dibujar_tarima(lienzo):

    """PISO DE MADERA Y LUCES DEL ESCENARIO."""

    pygame.draw.rect(
        lienzo,
        (43, 27, 35),
        (235, 230, 390, 25)
    )

    pygame.draw.rect(
        lienzo,
        (116, 68, 57),
        (240, 231, 380, 5)
    )

    pygame.draw.rect(
        lienzo,
        (74, 44, 45),
        (235, 245, 390, 10)
    )

    # TABLAS

    for x in range(250, 620, 45):

        pygame.draw.line(
            lienzo,
            (112, 72, 62),
            (x, 236),
            (x - 5, 251),
            1
        )

    # LUCES DEL BORDE DEL ESCENARIO

    for x in range(260, 615, 24):

        pygame.draw.circle(
            lienzo,
            DORADO,
            (x, 229),
            3
        )


def dibujar_escenario(lienzo):

    """ELEMENTOS DECORATIVOS DETRAS DE LAS ACTRICES."""

    # TELON DEL FONDO

    pygame.draw.rect(
        lienzo,
        (74, 33, 49),
        (320, 82, 225, 135)
    )

    # CORTINA CENTRAL

    pygame.draw.polygon(
        lienzo,
        (105, 39, 55),
        [
            (320, 82),
            (430, 82),
            (420, 215),
            (320, 215)
        ]
    )

    pygame.draw.polygon(
        lienzo,
        (137, 49, 62),
        [
            (430, 82),
            (545, 82),
            (545, 215),
            (420, 215)
        ]
    )

    # ESTRELLAS DECORATIVAS

    for x, y in [
        (355, 115),
        (510, 125),
        (390, 170),
        (485, 175)
    ]:

        pygame.draw.polygon(
            lienzo,
            DORADO_CLARO,
            [
                (x, y - 5),
                (x + 2, y - 2),
                (x + 5, y),
                (x + 2, y + 2),
                (x, y + 5),
                (x - 2, y + 2),
                (x - 5, y),
                (x - 2, y - 2)
            ]
        )

def dibujar_actrices(lienzo, tiempo):

    """LAS DOS ARTISTAS PRESENTAN SU FUNCION."""

    personajes.dibujar_spink_joven(
        lienzo,
        450,
        240
    )

    personajes.dibujar_forcible_joven(
        lienzo,
        560,
        240
    )


# --------------------------------------------------
# PUBLICO DE PERRITOS
# --------------------------------------------------

def dibujar_butacas(lienzo):

    """FILAS DE BUTACAS ROJAS FRENTE AL ESCENARIO."""

    # FILA TRASERA

    for x in range(25, 640, 65):

        pygame.draw.rect(
            lienzo,
            (47, 25, 38),
            (x, 267, 49, 44),
            border_radius=5
        )

        pygame.draw.rect(
            lienzo,
            (113, 42, 56),
            (x + 4, 271, 41, 35),
            border_radius=4
        )

        pygame.draw.line(
            lienzo,
            (169, 83, 78),
            (x + 8, 275),
            (x + 38, 275),
            2
        )

        pygame.draw.rect(
            lienzo,
            (45, 27, 39),
            (x + 2, 306, 45, 7)
        )

    # FILA DELANTERA

    for x in range(0, 640, 80):

        pygame.draw.rect(
            lienzo,
            (40, 22, 35),
            (x, 315, 59, 42),
            border_radius=5
        )

        pygame.draw.rect(
            lienzo,
            (91, 34, 50),
            (x + 4, 319, 51, 34),
            border_radius=4
        )


def dibujar_perritos(lienzo, tiempo):

    """PERRITOS SENTADOS EN LAS BUTACAS."""

    # FILA TRASERA

    perros_atras = [95, 205, 315, 535]

    for i in range(len(perros_atras)):

        personajes.dibujar_perro(
            lienzo,
            perros_atras[i],
            300,
            tiempo,
            i * 0.8
        )

    # FILA DELANTERA

    perros_delante = [85, 195, 305, 555]

    for i in range(len(perros_delante)):

        personajes.dibujar_perro(
            lienzo,
            perros_delante[i],
            350,
            tiempo,
            i * 0.9 + 1
        )


# --------------------------------------------------
# CORALINE
# --------------------------------------------------

def dibujar_coraline(lienzo):

    """CORALINE OBSERVA LA FUNCION DESDE EL PASILLO."""

    personajes.dibujar_coraline_chica(
        lienzo,
        405,
        355,
        True
    )


# --------------------------------------------------
# ILUMINACION
# --------------------------------------------------

def dibujar_luces_fijas(lienzo):

    """REFLECTORES CALIDOS SOBRE EL ESCENARIO."""

    brillo(
        lienzo,
        (465, 150),
        100,
        (255, 177, 104),
        45
    )

    brillo(
        lienzo,
        (560, 150),
        95,
        (255, 188, 116),
        40
    )


def dibujar_focos(lienzo, tiempo):

    """LUCES QUE PARPADEAN SOBRE EL ARCO."""

    for i in range(12):

        x = 250 + i * 31

        fase = math.sin(tiempo * 3 + i * 1.2)

        if fase > 0:

            color = (255, 210, 135)

        else:

            color = (133, 81, 76)

        pygame.draw.circle(
            lienzo,
            (45, 26, 37),
            (x, 49),
            5
        )

        pygame.draw.circle(
            lienzo,
            color,
            (x, 49),
            3
        )


# --------------------------------------------------
# FONDO COMPLETO
# --------------------------------------------------

def crear_fijo():

    """CONSTRUIMOS TODA LA SALA DEL TEATRO."""

    lienzo = pygame.Surface(
        (ANCHO, ALTO)
    )

    dibujar_pared(lienzo)
    dibujar_arco(lienzo)
    dibujar_escenario(lienzo)
    dibujar_cortinas(lienzo)
    dibujar_tarima(lienzo)
    dibujar_butacas(lienzo)
    dibujar_luces_fijas(lienzo)

    orillas_oscuras(lienzo)

    return lienzo


def dibujar(ventana):

    """DIBUJAMOS EL TEATRO Y SUS PERSONAJES ANIMADOS."""

    if "fijo" not in CAPAS:

        CAPAS["fijo"] = crear_fijo()

    tiempo = pygame.time.get_ticks() / 1000

    lienzo = CAPAS["fijo"].copy()

    dibujar_focos(
        lienzo,
        tiempo
    )

    dibujar_actrices(
        lienzo,
        tiempo
    )

    dibujar_perritos(
        lienzo,
        tiempo
    )

    dibujar_coraline(lienzo)

    mostrar(
        ventana,
        lienzo
    )