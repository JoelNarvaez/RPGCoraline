"""FONDO: HUIDA POR EL PASILLO DEL OTRO MUNDO."""

import math
import os
import pygame
import config

from interfaz.fondos.pintura import ANCHO, ALTO, mostrar
from interfaz.fondos import personajes


CAPAS = {}


# --------------------------------------------------
# COLORES
# --------------------------------------------------

AZUL_PARED = (17, 43, 53)
AZUL_OSCURO = (7, 19, 30)
AZUL_MEDIO = (24, 62, 72)
AZUL_LUZ = (55, 112, 119)

MADERA = (20, 29, 35)
MADERA_CLARA = (34, 48, 52)

NEGRO = (3, 7, 15)
BLANCO = (170, 190, 180)


# --------------------------------------------------
# FONDO PRINCIPAL
# --------------------------------------------------

def crear_fijo():

    lienzo = pygame.Surface((ANCHO, ALTO))
    lienzo.fill(AZUL_OSCURO)

    # PARED DEL PASILLO
    pygame.draw.rect(
        lienzo,
        AZUL_PARED,
        (0, 0, ANCHO, 610)
    )

    # PARED DEL FONDO
    pygame.draw.polygon(
        lienzo,
        (9, 27, 38),
        [
            (780, 0),
            (ANCHO, 0),
            (ANCHO, 610),
            (780, 610)
        ]
    )

    # --------------------------------------------------
    # PAPEL TAPIZ
    # --------------------------------------------------

    for x in range(25, 800, 100):

        pygame.draw.rect(
            lienzo,
            AZUL_MEDIO,
            (x, 0, 3, 610)
        )

        pygame.draw.rect(
            lienzo,
            (10, 32, 43),
            (x + 7, 0, 2, 610)
        )

        # PEQUENOS DETALLES DEL PAPEL TAPIZ
        for y in range(70, 570, 115):

            pygame.draw.polygon(
                lienzo,
                (28, 72, 79),
                [
                    (x + 35, y),
                    (x + 45, y + 15),
                    (x + 35, y + 30),
                    (x + 25, y + 15)
                ]
            )

    # --------------------------------------------------
    # MARCOS DE LA PARED
    # --------------------------------------------------

    pygame.draw.rect(
        lienzo,
        (6, 18, 29),
        (55, 95, 170, 220),
        8
    )

    pygame.draw.rect(
        lienzo,
        (56, 76, 76),
        (65, 105, 150, 200),
        3
    )

    pygame.draw.rect(
        lienzo,
        (6, 18, 29),
        (390, 70, 175, 235),
        8
    )

    pygame.draw.rect(
        lienzo,
        (56, 76, 76),
        (400, 80, 155, 215),
        3
    )

    # SILUETAS OSCURAS DENTRO DE LOS MARCOS
    pygame.draw.ellipse(
        lienzo,
        (5, 13, 23),
        (105, 145, 65, 90)
    )

    pygame.draw.ellipse(
        lienzo,
        (5, 13, 23),
        (445, 125, 65, 100)
    )

    # --------------------------------------------------
    # PUERTA DEL FONDO
    # --------------------------------------------------

    pygame.draw.rect(
        lienzo,
        (3, 12, 22),
        (870, 80, 300, 530)
    )

    pygame.draw.rect(
        lienzo,
        (29, 56, 65),
        (890, 100, 260, 490),
        5
    )

    pygame.draw.rect(
        lienzo,
        (4, 12, 21),
        (920, 125, 200, 465)
    )

    # LUZ DETRAS DE LA PUERTA
    pygame.draw.rect(
        lienzo,
        (27, 67, 77),
        (970, 155, 100, 390)
    )

    pygame.draw.rect(
        lienzo,
        (42, 93, 101),
        (1000, 180, 45, 330)
    )

    # MANIJA
    pygame.draw.circle(
        lienzo,
        (118, 110, 77),
        (1090, 355),
        7
    )

    # --------------------------------------------------
    # PISO DE MADERA
    # --------------------------------------------------

    pygame.draw.polygon(
        lienzo,
        MADERA,
        [
            (0, 500),
            (ANCHO, 500),
            (ANCHO, ALTO),
            (0, ALTO)
        ]
    )

    pygame.draw.line(
        lienzo,
        (39, 72, 76),
        (0, 500),
        (ANCHO, 500),
        5
    )

    # TABLAS EN PERSPECTIVA
    for x in range(-300, ANCHO + 300, 130):

        pygame.draw.line(
            lienzo,
            MADERA_CLARA,
            (640, 500),
            (x, ALTO),
            2
        )

    # LINEAS HORIZONTALES
    for y in [555, 615, 680]:

        pygame.draw.line(
            lienzo,
            (27, 43, 49),
            (0, y),
            (ANCHO, y),
            2
        )

    # RODAPIE
    pygame.draw.line(
        lienzo,
        (46, 76, 78),
        (0, 505),
        (ANCHO, 505),
        5
    )

    return lienzo


# --------------------------------------------------
# CARGAR IMAGEN DE CORALINE
# --------------------------------------------------

def cargar_rostro():

    ruta = os.path.join(
        config.RUTA_IMAGENES,
        "cora.png"
    )

    if not os.path.exists(ruta):

        print("NO SE ENCONTRO cora.png:", ruta)
        return None

    imagen = pygame.image.load(ruta).convert_alpha()

    # TAMANO DEL RETRATO
    ancho = 190
    alto = 210

    imagen = pygame.transform.smoothscale(
        imagen,
        (ancho, alto)
    )

    return imagen


# --------------------------------------------------
# APARICION DE CORALINE
# --------------------------------------------------

def dibujar_retrato(lienzo, tiempo):

    if "retrato" not in CAPAS:

        CAPAS["retrato"] = cargar_rostro()

    imagen = CAPAS["retrato"]

    if imagen is None:
        return

    # POSICION EN LA PARED DERECHA
    x = ANCHO - 215
    y = 155

    # MARCO OSCURO
    pygame.draw.rect(
        lienzo,
        (4, 12, 23),
        (x - 12, y - 12, 214, 234)
    )

    pygame.draw.rect(
        lienzo,
        (48, 82, 88),
        (x - 7, y - 7, 204, 224),
        3
    )

    # LIGERO MOVIMIENTO
    movimiento = int(math.sin(tiempo * 1.5) * 3)

    lienzo.blit(
        imagen,
        (x, y + movimiento)
    )


# --------------------------------------------------
# SOMBRAS QUE SALEN DE LAS PAREDES
# --------------------------------------------------

def dibujar_sombras(lienzo, tiempo):

    movimiento = int(math.sin(tiempo * 2.5) * 14)

    # SOMBRA IZQUIERDA
    pygame.draw.polygon(
        lienzo,
        NEGRO,
        [
            (0, 330),
            (110, 315),
            (210, 350),
            (290 + movimiento, 420),
            (200, 405),
            (110, 390),
            (0, 420)
        ]
    )

    # SOMBRA DERECHA
    pygame.draw.polygon(
        lienzo,
        NEGRO,
        [
            (ANCHO, 300),
            (1190, 320),
            (1110, 380),
            (1040 - movimiento, 445),
            (1160, 420),
            (ANCHO, 440)
        ]
    )

    # DEDOS ALARGADOS
    for i in range(4):

        avance = int(math.sin(tiempo * 3 + i) * 12)

        pygame.draw.line(
            lienzo,
            NEGRO,
            (0, 350 + i * 25),
            (230 + avance, 430 + i * 20),
            7
        )

        pygame.draw.line(
            lienzo,
            NEGRO,
            (ANCHO, 330 + i * 25),
            (ANCHO - 220 - avance, 420 + i * 20),
            7
        )


# --------------------------------------------------
# OJOS ESCONDIDOS
# --------------------------------------------------

def dibujar_ojos(lienzo, tiempo):

    posiciones = [
        (320, 390),
        (700, 230),
        (780, 430),
        (ANCHO - 70, 440)
    ]

    for i, posicion in enumerate(posiciones):

        x, y = posicion

        movimiento = int(
            math.sin(tiempo * 2 + i) * 3
        )

        pygame.draw.ellipse(
            lienzo,
            (2, 5, 12),
            (x - 19, y - 10, 40, 21)
        )

        pygame.draw.circle(
            lienzo,
            BLANCO,
            (x - 8 + movimiento, y),
            5
        )

        pygame.draw.circle(
            lienzo,
            BLANCO,
            (x + 8 + movimiento, y),
            5
        )


# --------------------------------------------------
# PARTICULAS DEL PASILLO
# --------------------------------------------------

def dibujar_particulas(lienzo, tiempo):

    for i in range(18):

        x = (i * 83 + int(tiempo * 9)) % ANCHO
        y = (i * 47 + int(tiempo * 5)) % 570

        pygame.draw.circle(
            lienzo,
            (58, 105, 111),
            (x, y),
            2
        )


# --------------------------------------------------
# CORALINE EN PRIMER PLANO
# --------------------------------------------------

def dibujar_coraline_corriendo(lienzo, tiempo):

    movimiento = math.sin(tiempo * 9)

    # RASTROS DE MOVIMIENTO
    for i in range(4):

        x = 790 - i * 24
        y = 555 + i * 13 + int(movimiento * 3)

        pygame.draw.line(
            lienzo,
            (65, 104, 112),
            (x, y),
            (x - 15, y),
            2
        )

    # PEQUENO SALTO
    salto = abs(math.sin(tiempo * 9)) * 5

    x_coraline = 870 + int(math.sin(tiempo * 1.5) * 7)
    y_piso = 630 - int(salto)

    personajes.dibujar_coraline_chica(
        lienzo,
        x_coraline,
        y_piso,
        True
    )


# --------------------------------------------------
# DIBUJO PRINCIPAL
# --------------------------------------------------

def dibujar(ventana):

    if "fijo" not in CAPAS:
        CAPAS["fijo"] = crear_fijo()

    tiempo = pygame.time.get_ticks() / 1000

    lienzo = CAPAS["fijo"].copy()

    # SOMBRAS
    dibujar_sombras(lienzo, tiempo)

    # OJOS ESCONDIDOS
    dibujar_ojos(lienzo, tiempo)

    # PARTICULAS
    dibujar_particulas(lienzo, tiempo)

    # RETRATO DE CORALINE
    dibujar_retrato(lienzo, tiempo)

    # CORALINE EN PRIMER PLANO
    dibujar_coraline_corriendo(lienzo, tiempo)

    mostrar(ventana, lienzo)