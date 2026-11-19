"""
COCINA DEL OTRO DEPARTAMENTO.

UNA COCINA CALIDA Y ELEGANTE QUE ESCONDE ALGO INQUIETANTE.
LA OTRA MADRE RECIBE A CORALINE CON UNA CENA ESPECIAL.

ELEMENTOS ANIMADOS:
- VAPOR DEL POLLO.
- FLAMA DE LA VELA.
- BRILLO DE LOS OJOS DE BOTON.
- PEQUENAS VARIACIONES DE ILUMINACION.
"""

import math
import pygame

from interfaz.fondos.pintura import ANCHO, ALTO
from interfaz.fondos.pintura import capa_vacia, pegar_con_contorno
from interfaz.fondos.pintura import mezclar, degradado
from interfaz.fondos.pintura import brillo, orillas_oscuras, mostrar

from interfaz.fondos import personajes
from interfaz.fondos import sala_actrices


# --------------------------------------------------
# POSICIONES
# --------------------------------------------------

Y_PISO = 300

X_CORALINE = 436
X_MESA = 508
X_MADRE = 592

VELA = (494, 222)

CAPAS = {}


# --------------------------------------------------
# COLORES
# --------------------------------------------------

COLOR_PARED = (226, 186, 110)
COLOR_PARED_CLARA = (245, 211, 145)
COLOR_PARED_SOMBRA = (170, 120, 70)

COLOR_MUEBLE = (130, 65, 49)
COLOR_MUEBLE_CLARO = (176, 96, 70)
COLOR_MUEBLE_OSCURO = (83, 42, 38)

COLOR_COBRE = (210, 120, 70)
COLOR_COBRE_CLARO = (245, 174, 115)

COLOR_PISO = (170, 70, 60)
COLOR_PISO_CLARO = (236, 220, 196)

COLOR_CONTORNO = (72, 43, 38)


# --------------------------------------------------
# PARED Y PAPEL TAPIZ
# --------------------------------------------------

def dibujar_pared(lienzo):

    """PARED AMARILLA CON PAPEL TAPIZ Y TEXTURA."""

    degradado(
        lienzo,
        pygame.Rect(0, 0, ANCHO, Y_PISO),
        COLOR_PARED_SOMBRA,
        COLOR_PARED,
        18
    )

    # RAYAS DEL PAPEL TAPIZ

    for x in range(0, ANCHO, 12):

        pygame.draw.line(
            lienzo,
            mezclar(COLOR_PARED, (255, 245, 205), 0.25),
            (x, 0),
            (x, Y_PISO),
            2
        )

        pygame.draw.line(
            lienzo,
            mezclar(COLOR_PARED, (125, 83, 52), 0.13),
            (x + 5, 0),
            (x + 5, Y_PISO),
            1
        )

    # PEQUENOS DETALLES DEL PAPEL

    for y in range(12, Y_PISO, 32):

        for x in range(8, ANCHO, 48):

            pygame.draw.circle(
                lienzo,
                (195, 148, 85),
                (x, y),
                1
            )

            pygame.draw.circle(
                lienzo,
                (245, 215, 155),
                (x + 2, y + 2),
                1
            )

    # SOMBRA SUPERIOR DE LA PARED

    pygame.draw.rect(
        lienzo,
        (120, 75, 48),
        (0, 0, ANCHO, 5)
    )

    # ZOCLO INFERIOR

    pygame.draw.rect(
        lienzo,
        (112, 62, 48),
        (0, Y_PISO - 9, ANCHO, 9)
    )

    pygame.draw.line(
        lienzo,
        (225, 160, 105),
        (0, Y_PISO - 9),
        (ANCHO, Y_PISO - 9),
        2
    )


# --------------------------------------------------
# VENTANA
# --------------------------------------------------

def dibujar_ventana(lienzo):

    """VENTANA CON LUZ DE ATARDECER Y CORTINAS."""

    # MARCO EXTERIOR

    pygame.draw.rect(
        lienzo,
        (91, 49, 39),
        (416, 63, 62, 83)
    )

    pygame.draw.rect(
        lienzo,
        (205, 139, 91),
        (420, 67, 54, 75)
    )

    # CIELO

    degradado(
        lienzo,
        pygame.Rect(423, 70, 48, 69),
        (250, 190, 125),
        (204, 92, 79),
        8
    )

    # SILUETA DEL ATARDECER

    pygame.draw.ellipse(
        lienzo,
        (245, 155, 95),
        (431, 100, 25, 25)
    )

    # DIVISIONES DE LA VENTANA

    pygame.draw.line(
        lienzo,
        (112, 62, 43),
        (447, 70),
        (447, 139),
        3
    )

    pygame.draw.line(
        lienzo,
        (112, 62, 43),
        (423, 105),
        (471, 105),
        2
    )

    # CORTINAS

    pygame.draw.polygon(
        lienzo,
        (190, 55, 67),
        [
            (416, 62),
            (439, 62),
            (435, 112),
            (425, 140),
            (416, 146)
        ]
    )

    pygame.draw.polygon(
        lienzo,
        (190, 55, 67),
        [
            (476, 62),
            (453, 62),
            (457, 112),
            (467, 140),
            (476, 146)
        ]
    )

    # PLIEGUES DE LAS CORTINAS

    pygame.draw.line(
        lienzo,
        (130, 39, 52),
        (422, 72),
        (423, 132),
        2
    )

    pygame.draw.line(
        lienzo,
        (130, 39, 52),
        (469, 72),
        (468, 132),
        2
    )

    # REPISA INFERIOR

    pygame.draw.rect(
        lienzo,
        (91, 49, 39),
        (414, 144, 65, 5)
    )

    pygame.draw.line(
        lienzo,
        (235, 169, 112),
        (416, 144),
        (476, 144),
        2
    )


# --------------------------------------------------
# ALACENAS
# --------------------------------------------------

def dibujar_alacenas(lienzo):

    """MUEBLES DE MADERA CON PROFUNDIDAD Y HERRAJES."""

    # ALACENA SUPERIOR

    pygame.draw.rect(
        lienzo,
        COLOR_MUEBLE_OSCURO,
        (540, 36, ANCHO - 540, 62)
    )

    pygame.draw.rect(
        lienzo,
        COLOR_MUEBLE_CLARO,
        (543, 39, ANCHO - 546, 54)
    )

    pygame.draw.rect(
        lienzo,
        (104, 52, 42),
        (540, 92, ANCHO - 540, 6)
    )

    # PUERTAS SUPERIORES

    for x in range(547, ANCHO - 5, 32):

        pygame.draw.rect(
            lienzo,
            (103, 49, 42),
            (x, 42, 27, 45)
        )

        pygame.draw.rect(
            lienzo,
            (158, 79, 58),
            (x + 2, 44, 23, 41)
        )

        pygame.draw.rect(
            lienzo,
            (104, 52, 43),
            (x + 5, 47, 17, 35),
            1
        )

        # MANIJA

        pygame.draw.circle(
            lienzo,
            (220, 167, 103),
            (x + 22, 66),
            2
        )

    # SOMBRA DE LA ENCIMERA

    pygame.draw.rect(
        lienzo,
        (89, 47, 39),
        (536, 218, ANCHO - 536, 12)
    )

    pygame.draw.rect(
        lienzo,
        (236, 226, 206),
        (536, 218, ANCHO - 536, 6)
    )

    pygame.draw.line(
        lienzo,
        (255, 246, 223),
        (536, 218),
        (ANCHO, 218),
        2
    )

    # ALACENA INFERIOR

    pygame.draw.rect(
        lienzo,
        (92, 46, 40),
        (540, 230, ANCHO - 540, Y_PISO - 230)
    )

    pygame.draw.rect(
        lienzo,
        COLOR_MUEBLE_CLARO,
        (543, 233, ANCHO - 546, Y_PISO - 236)
    )

    # PUERTAS INFERIORES

    for x in range(547, ANCHO - 5, 32):

        pygame.draw.rect(
            lienzo,
            (102, 49, 42),
            (x, 236, 27, 57)
        )

        pygame.draw.rect(
            lienzo,
            (157, 79, 59),
            (x + 2, 238, 23, 53)
        )

        pygame.draw.rect(
            lienzo,
            (104, 52, 43),
            (x + 5, 242, 17, 45),
            1
        )

        pygame.draw.circle(
            lienzo,
            (220, 167, 103),
            (x + 22, 265),
            2
        )

    # LATERAL DE LA ALACENA

    pygame.draw.line(
        lienzo,
        (78, 39, 35),
        (540, 36),
        (540, 298),
        3
    )


# --------------------------------------------------
# OLLAS Y UTENSILIOS
# --------------------------------------------------

def dibujar_ollas(lienzo):

    """OLLAS DE COBRE COLGADAS EN LA PARED."""

    # BARRA

    pygame.draw.line(
        lienzo,
        (74, 49, 39),
        (548, 112),
        (636, 112),
        3
    )

    pygame.draw.circle(
        lienzo,
        (180, 130, 82),
        (548, 112),
        3
    )

    pygame.draw.circle(
        lienzo,
        (180, 130, 82),
        (636, 112),
        3
    )

    # OLLAS

    ollas = [
        (560, 10),
        (584, 13),
        (612, 9)
    ]

    for x, tamano in ollas:

        pygame.draw.line(
            lienzo,
            (70, 49, 39),
            (x, 112),
            (x, 118),
            2
        )

        pygame.draw.ellipse(
            lienzo,
            (120, 65, 43),
            (x - tamano - 2, 118, tamano * 2 + 4, tamano * 2)
        )

        pygame.draw.circle(
            lienzo,
            COLOR_COBRE,
            (x, 118 + tamano),
            tamano
        )

        pygame.draw.arc(
            lienzo,
            COLOR_COBRE_CLARO,
            (x - tamano + 2, 119 + tamano // 2,
             tamano * 2 - 4, tamano),
            0.2,
            2.7,
            2
        )

        pygame.draw.circle(
            lienzo,
            (255, 193, 130),
            (x - tamano // 3, 115 + tamano),
            2
        )

    # CUCHARON COLGADO

    pygame.draw.line(
        lienzo,
        (90, 65, 48),
        (630, 113),
        (630, 135),
        2
    )

    pygame.draw.ellipse(
        lienzo,
        (190, 130, 85),
        (625, 133, 10, 7)
    )


# --------------------------------------------------
# PISO
# --------------------------------------------------

def dibujar_piso(lienzo):

    """PISO DE CUADROS ROJOS Y CREMA."""

    for fila in range(6):

        for columna in range(ANCHO // 16 + 1):

            if (fila + columna) % 2 == 0:
                color = COLOR_PISO
            else:
                color = COLOR_PISO_CLARO

            pygame.draw.rect(
                lienzo,
                color,
                (columna * 16, Y_PISO + fila * 10, 16, 10)
            )

            pygame.draw.rect(
                lienzo,
                (90, 55, 48),
                (columna * 16, Y_PISO + fila * 10, 16, 10),
                1
            )

    # SOMBRA DEL ZOCLO SOBRE EL PISO

    pygame.draw.rect(
        lienzo,
        (75, 45, 40),
        (0, Y_PISO, ANCHO, 3)
    )


# --------------------------------------------------
# MESA Y CENA
# --------------------------------------------------

def dibujar_mesa(lienzo):

    """MESA PUESTA CON MANTEL, PLATOS, COPA Y VELA."""

    x = X_MESA

    # PATAS

    pygame.draw.polygon(
        lienzo,
        (112, 64, 48),
        [
            (x - 25, 252),
            (x - 18, 252),
            (x - 20, Y_PISO),
            (x - 29, Y_PISO)
        ]
    )

    pygame.draw.polygon(
        lienzo,
        (112, 64, 48),
        [
            (x + 18, 252),
            (x + 25, 252),
            (x + 29, Y_PISO),
            (x + 20, Y_PISO)
        ]
    )

    # MANTEL

    pygame.draw.polygon(
        lienzo,
        (218, 213, 199),
        [
            (x - 34, 244),
            (x + 34, 244),
            (x + 38, Y_PISO),
            (x - 38, Y_PISO)
        ]
    )

    # RAYAS DEL MANTEL

    for xx in range(x - 34, x + 34, 8):

        pygame.draw.line(
            lienzo,
            (190, 75, 78),
            (xx, 245),
            (xx + 2, Y_PISO),
            2
        )

    # BORDE INFERIOR DEL MANTEL

    pygame.draw.line(
        lienzo,
        (185, 67, 72),
        (x - 37, 292),
        (x + 37, 292),
        2
    )

    # BORDE SUPERIOR

    pygame.draw.ellipse(
        lienzo,
        (170, 105, 80),
        (x - 37, 237, 74, 13)
    )

    pygame.draw.ellipse(
        lienzo,
        (244, 237, 222),
        (x - 36, 237, 72, 11)
    )

    # PLATOS

    for dx in [-20, 16]:

        pygame.draw.ellipse(
            lienzo,
            (195, 190, 180),
            (x + dx - 9, 241, 20, 6)
        )

        pygame.draw.ellipse(
            lienzo,
            (252, 249, 240),
            (x + dx - 8, 240, 18, 5)
        )

        pygame.draw.ellipse(
            lienzo,
            (195, 195, 190),
            (x + dx - 4, 241, 10, 3),
            1
        )

    # COPA

    pygame.draw.polygon(
        lienzo,
        (190, 218, 225),
        [
            (x + 2, 231),
            (x + 9, 231),
            (x + 7, 238),
            (x + 4, 238)
        ]
    )

    pygame.draw.line(
        lienzo,
        (190, 218, 225),
        (x + 5, 238),
        (x + 5, 242),
        1
    )

    pygame.draw.line(
        lienzo,
        (190, 218, 225),
        (x + 1, 242),
        (x + 10, 242),
        1
    )

    # VELA

    pygame.draw.rect(
        lienzo,
        (190, 170, 130),
        (VELA[0] - 3, VELA[1] + 2, 6, 17)
    )

    pygame.draw.rect(
        lienzo,
        (245, 239, 218),
        (VELA[0] - 2, VELA[1] + 2, 4, 16)
    )

    pygame.draw.line(
        lienzo,
        (105, 78, 57),
        (VELA[0], VELA[1] + 1),
        (VELA[0], VELA[1] + 4),
        1
    )

    pygame.draw.ellipse(
        lienzo,
        (190, 150, 90),
        (VELA[0] - 6, VELA[1] + 16, 12, 5)
    )


# --------------------------------------------------
# ILUMINACION FIJA
# --------------------------------------------------

def dibujar_iluminacion(lienzo):

    """LUZ CALIDA DE LA VENTANA Y LA VELA."""

    brillo(
        lienzo,
        (447, 105),
        115,
        (255, 180, 105),
        35
    )

    brillo(
        lienzo,
        VELA,
        65,
        (255, 190, 100),
        35
    )

    # SOMBRA SUAVE DETRAS DE LA OTRA MADRE

    brillo(
        lienzo,
        (X_MADRE, 180),
        75,
        (105, 45, 65),
        14
    )


# --------------------------------------------------
# CONSTRUCCION DEL FONDO FIJO
# --------------------------------------------------

def crear_fijo():

    """CONSTRUYE TODOS LOS ELEMENTOS QUE NO NECESITAN ANIMACION."""

    lienzo = pygame.Surface(
        (ANCHO, ALTO)
    )

    # FONDO

    dibujar_pared(lienzo)
    dibujar_piso(lienzo)

    # ELEMENTOS DE LA COCINA

    dibujar_ventana(lienzo)
    dibujar_alacenas(lienzo)
    dibujar_ollas(lienzo)

    # ILUMINACION

    dibujar_iluminacion(lienzo)

    # OTRA MADRE

    capa = capa_vacia()

    personajes.dibujar_otra_madre(
        capa,
        X_MADRE,
         "normal"
    )

    pegar_con_contorno(
        lienzo,
        capa
    )

    # MESA

    dibujar_mesa(lienzo)

    # CORALINE

    sala_actrices.dibujar_coraline(
        lienzo,
        X_CORALINE
    )

    # OSCURECIMIENTO DE LAS ORILLAS

    orillas_oscuras(
        lienzo
    )

    return lienzo

def dibujar_cajita_botones(lienzo):

    """CAJITA CON LOS DOS BOTONES QUE LA OTRA MADRE LE OFRECE A CORALINE."""

    x = 514
    y = 222

    # SOMBRA DE LA CAJITA

    pygame.draw.ellipse(
        lienzo,
        (80, 45, 38),
        (x - 15, y + 10, 32, 5)
    )

    # BASE DE LA CAJITA

    pygame.draw.rect(
        lienzo,
        (91, 42, 42),
        (x - 14, y, 28, 12)
    )

    pygame.draw.rect(
        lienzo,
        (151, 75, 65),
        (x - 12, y + 2, 24, 8)
    )

    # INTERIOR OSCURO

    pygame.draw.rect(
        lienzo,
        (48, 30, 34),
        (x - 10, y + 3, 20, 6)
    )

    # LOS DOS BOTONES NEGROS

    for dx in [-5, 5]:

        pygame.draw.circle(
            lienzo,
            (8, 7, 12),
            (x + dx, y + 6),
            3
        )

        pygame.draw.circle(
            lienzo,
            (105, 95, 105),
            (x + dx - 1, y + 5),
            1
        )

        # AGUJERITOS DEL BOTON

        pygame.draw.circle(
            lienzo,
            (185, 170, 155),
            (x + dx, y + 5),
            1
        )

    # TAPA ABIERTA DETRAS DE LA CAJITA

    pygame.draw.polygon(
        lienzo,
        (126, 61, 58),
        [
            (x - 14, y),
            (x - 10, y - 9),
            (x + 10, y - 9),
            (x + 14, y)
        ]
    )

    pygame.draw.line(
        lienzo,
        (210, 145, 105),
        (x - 10, y - 8),
        (x + 10, y - 8),
        1
    )

    # AGUJA

    pygame.draw.line(
        lienzo,
        (185, 195, 205),
        (x + 15, y + 1),
        (x + 23, y - 7),
        2
    )

    pygame.draw.circle(
        lienzo,
        (210, 220, 225),
        (x + 23, y - 7),
        2
    )

    # CARRETE DE HILO

    pygame.draw.rect(
        lienzo,
        (190, 130, 95),
        (x - 23, y + 1, 6, 10)
    )

    pygame.draw.line(
        lienzo,
        (245, 195, 145),
        (x - 22, y + 3),
        (x - 18, y + 3),
        2
    )

    pygame.draw.line(
        lienzo,
        (245, 195, 145),
        (x - 22, y + 6),
        (x - 18, y + 6),
        2
    )

    pygame.draw.line(
        lienzo,
        (245, 195, 145),
        (x - 22, y + 9),
        (x - 18, y + 9),
        2
    )

# --------------------------------------------------
# ANIMACIONES
# --------------------------------------------------

def dibujar_flama(lienzo, tiempo):

    """FLAMA DE LA VELA CON MOVIMIENTO SUAVE."""

    x, y = VELA

    baile = int(
        math.sin(tiempo * 9) * 1.5
    )

    altura = int(
        abs(math.sin(tiempo * 7)) * 2
    )

    # RESPLANDOR

    brillo(
        lienzo,
        (x + baile, y - 2),
        20,
        (255, 175, 65),
        22
    )

    # FLAMA EXTERIOR

    pygame.draw.ellipse(
        lienzo,
        (255, 150, 45),
        (
            x - 3 + baile,
            y - 7 - altura,
            7,
            11 + altura
        )
    )

    # FLAMA INTERIOR

    pygame.draw.ellipse(
        lienzo,
        (255, 235, 170),
        (
            x - 1 + baile,
            y - 4 - altura,
            3,
            6 + altura
        )
    )


def dibujar_luz_inquietante(lienzo, tiempo):

    """PEQUENA VARIACION DE LUZ EN LA HABITACION."""

    pulso = abs(
        math.sin(tiempo * 1.5)
    )

    intensidad = int(
        8 + pulso * 8
    )

    brillo(
        lienzo,
        (X_MADRE, 180),
        55,
        (120, 55, 75),
        intensidad
    )


# --------------------------------------------------
# DIBUJO PRINCIPAL
# --------------------------------------------------

def dibujar(ventana):

    """DIBUJA LA COCINA COMPLETA."""

    if "fijo" not in CAPAS:

        CAPAS["fijo"] = crear_fijo()

    tiempo = pygame.time.get_ticks() / 1000

    lienzo = CAPAS["fijo"].copy()

    # LUZ INQUIETANTE

    dibujar_luz_inquietante(
        lienzo,
        tiempo
    )

    dibujar_cajita_botones(lienzo)

    # FLAMA DE LA VELA

    dibujar_flama(
        lienzo,
        tiempo
    )

    # OJOS DE BOTON

    personajes.dibujar_botones(
        lienzo,
        personajes.ojos_otra_madre(X_MADRE),
        tiempo,
        False,
        True
    )

    # MOSTRAR ESCENA

    mostrar(
        ventana,
        lienzo
    )