"""FONDO: CORALINE DESPIERTA EN SU VERDADERO SALON."""

import math
import pygame

from interfaz.fondos.pintura import ANCHO, ALTO, mostrar
from interfaz.fondos import personajes


CAPAS = {}


# --------------------------------------------------
# COLORES
# --------------------------------------------------

PARED = (72, 77, 87)
PARED_CLARA = (91, 94, 103)
PARED_OSCURA = (47, 53, 65)

MADERA = (65, 43, 37)
MADERA_CLARA = (112, 76, 57)

SILLON = (76, 59, 62)
SILLON_CLARO = (112, 83, 79)

PISO = (43, 38, 43)

LUZ = (220, 177, 112)


# --------------------------------------------------
# CREAR FONDO
# --------------------------------------------------

def crear_fijo():

    lienzo = pygame.Surface((ANCHO, ALTO))
    lienzo.fill(PARED)

    # --------------------------------------------------
    # PARED DEL SALON
    # --------------------------------------------------

    pygame.draw.rect(
        lienzo,
        PARED,
        (0, 0, ANCHO, 610)
    )

    # TONALIDAD DE LA PARED
    pygame.draw.rect(
        lienzo,
        PARED_CLARA,
        (0, 0, ANCHO, 8)
    )

    # PAPEL TAPIZ
    for x in range(25, ANCHO, 95):

        pygame.draw.line(
            lienzo,
            PARED_OSCURA,
            (x, 0),
            (x, 610),
            2
        )

        for y in range(65, 570, 115):

            pygame.draw.polygon(
                lienzo,
                (104, 102, 108),
                [
                    (x + 20, y),
                    (x + 29, y + 13),
                    (x + 20, y + 26),
                    (x + 11, y + 13)
                ]
            )

    # --------------------------------------------------
    # VENTANA Y CORTINAS
    # --------------------------------------------------

    pygame.draw.rect(
        lienzo,
        (37, 48, 61),
        (55, 55, 240, 205)
    )

    pygame.draw.rect(
        lienzo,
        (115, 119, 126),
        (65, 65, 220, 185),
        5
    )

    # CRISTALES
    pygame.draw.rect(
        lienzo,
        (65, 85, 103),
        (75, 75, 200, 165)
    )

    pygame.draw.line(
        lienzo,
        (132, 132, 135),
        (175, 75),
        (175, 240),
        5
    )

    pygame.draw.line(
        lienzo,
        (132, 132, 135),
        (75, 155),
        (275, 155),
        5
    )

    # CORTINA IZQUIERDA
    pygame.draw.polygon(
        lienzo,
        (76, 55, 66),
        [
            (42, 40),
            (83, 40),
            (94, 280),
            (65, 300),
            (48, 190)
        ]
    )

    # CORTINA DERECHA
    pygame.draw.polygon(
        lienzo,
        (76, 55, 66),
        [
            (280, 40),
            (320, 40),
            (310, 260),
            (285, 290),
            (295, 160)
        ]
    )

    # PLIEGUES
    pygame.draw.line(
        lienzo,
        (111, 77, 85),
        (58, 55),
        (70, 270),
        3
    )

    pygame.draw.line(
        lienzo,
        (111, 77, 85),
        (300, 55),
        (293, 260),
        3
    )

    # --------------------------------------------------
    # CUADROS DECORATIVOS
    # --------------------------------------------------

    pygame.draw.rect(
        lienzo,
        (39, 31, 32),
        (355, 70, 135, 145)
    )

    pygame.draw.rect(
        lienzo,
        (153, 126, 102),
        (363, 78, 119, 129),
        4
    )

    pygame.draw.rect(
        lienzo,
        (71, 84, 91),
        (373, 88, 99, 109)
    )

    pygame.draw.circle(
        lienzo,
        (177, 157, 124),
        (420, 128),
        23
    )

    pygame.draw.polygon(
        lienzo,
        (49, 59, 65),
        [
            (375, 192),
            (420, 145),
            (477, 192)
        ]
    )

    # SEGUNDO CUADRO
    pygame.draw.rect(
        lienzo,
        (42, 34, 34),
        (535, 85, 115, 125)
    )

    pygame.draw.rect(
        lienzo,
        (143, 113, 89),
        (542, 92, 101, 111),
        4
    )

    pygame.draw.ellipse(
        lienzo,
        (90, 106, 112),
        (557, 107, 72, 78)
    )

    # --------------------------------------------------
    # PUERTA PEQUEÑA Y LADRILLOS
    # --------------------------------------------------

    # PARED DE LA PUERTA
    pygame.draw.rect(
        lienzo,
        (62, 66, 76),
        (830, 80, 420, 500)
    )

    # LADRILLOS
    for fila in range(9):

        y = 90 + fila * 52

        pygame.draw.line(
            lienzo,
            (38, 42, 51),
            (830, y),
            (1250, y),
            4
        )

        desplazamiento = 0

        if fila % 2 == 0:
            desplazamiento = 45

        for x in range(830 + desplazamiento, 1250, 95):

            pygame.draw.line(
                lienzo,
                (38, 42, 51),
                (x, y),
                (x, y + 52),
                4
            )

    # ALGUNOS LADRILLOS MAS CLAROS
    pygame.draw.rect(
        lienzo,
        (105, 94, 91),
        (855, 115, 45, 25)
    )

    pygame.draw.rect(
        lienzo,
        (112, 99, 94),
        (1020, 210, 55, 27)
    )

    pygame.draw.rect(
        lienzo,
        (103, 94, 91),
        (900, 370, 55, 25)
    )

    # MARCO DE LA PUERTA
    pygame.draw.rect(
        lienzo,
        (37, 27, 27),
        (900, 245, 170, 300)
    )

    pygame.draw.rect(
        lienzo,
        MADERA,
        (910, 255, 150, 280),
        7
    )

    # LA PUERTA ESTA ABIERTA Y DEJA VER LOS LADRILLOS
    pygame.draw.rect(
        lienzo,
        (76, 66, 65),
        (920, 265, 130, 260)
    )

    for y in range(275, 520, 40):

        pygame.draw.line(
            lienzo,
            (43, 39, 43),
            (920, y),
            (1050, y),
            3
        )

    # --------------------------------------------------
    # ESTANTERIA
    # --------------------------------------------------

    pygame.draw.rect(
        lienzo,
        (43, 31, 29),
        (690, 90, 105, 365)
    )

    pygame.draw.rect(
        lienzo,
        (102, 68, 49),
        (700, 100, 85, 345)
    )

    for y in [190, 290, 390]:

        pygame.draw.rect(
            lienzo,
            (42, 31, 29),
            (700, y, 85, 8)
        )

    # LIBROS
    libros = [
        (710, 115, 15, 65, (105, 63, 59)),
        (729, 120, 18, 60, (65, 78, 89)),
        (750, 110, 14, 70, (124, 99, 66)),
        (715, 210, 19, 70, (85, 72, 92)),
        (739, 220, 17, 60, (122, 78, 61)),
        (760, 205, 15, 75, (66, 91, 87)),
        (710, 310, 16, 70, (115, 89, 68)),
        (730, 320, 17, 60, (72, 78, 102)),
        (751, 305, 20, 75, (115, 65, 65))
    ]

    for x, y, ancho, alto, color in libros:

        pygame.draw.rect(
            lienzo,
            color,
            (x, y, ancho, alto)
        )

        pygame.draw.line(
            lienzo,
            (160, 137, 111),
            (x + 3, y + 8),
            (x + ancho - 3, y + 8),
            2
        )

    # --------------------------------------------------
    # LAMPARA DE PIE
    # --------------------------------------------------

    pygame.draw.rect(
        lienzo,
        (49, 39, 35),
        (785, 345, 8, 165)
    )

    pygame.draw.polygon(
        lienzo,
        (177, 151, 112),
        [
            (755, 355),
            (823, 355),
            (812, 285),
            (766, 285)
        ]
    )

    pygame.draw.line(
        lienzo,
        (126, 98, 73),
        (789, 355),
        (789, 495),
        5
    )

    pygame.draw.ellipse(
        lienzo,
        (44, 34, 32),
        (765, 495, 55, 14)
    )

    # --------------------------------------------------
    # SILLON
    # --------------------------------------------------

    # SOMBRA
    pygame.draw.ellipse(
        lienzo,
        (23, 22, 29),
        (35, 580, 700, 110)
    )

    # RESPALDO
    pygame.draw.rect(
        lienzo,
        (57, 43, 49),
        (65, 330, 580, 250)
    )

    pygame.draw.rect(
        lienzo,
        SILLON,
        (80, 345, 550, 215)
    )

    # COJINES DEL RESPALDO
    pygame.draw.rect(
        lienzo,
        (67, 53, 60),
        (105, 365, 155, 145)
    )

    pygame.draw.rect(
        lienzo,
        (91, 66, 70),
        (275, 365, 155, 145)
    )

    pygame.draw.rect(
        lienzo,
        (67, 53, 60),
        (445, 365, 155, 145)
    )

    # COSTURAS DE LOS COJINES
    for x in [115, 285, 455]:

        pygame.draw.rect(
            lienzo,
            (123, 91, 87),
            (x, 380, 135, 3)
        )

        pygame.draw.rect(
            lienzo,
            (49, 43, 51),
            (x, 485, 135, 3)
        )

    # ASIENTO
    pygame.draw.polygon(
        lienzo,
        SILLON_CLARO,
        [
            (55, 515),
            (650, 515),
            (720, 625),
            (35, 625)
        ]
    )

    pygame.draw.line(
        lienzo,
        (139, 103, 96),
        (70, 530),
        (640, 530),
        4
    )

    # BRAZOS DEL SILLON
    pygame.draw.rect(
        lienzo,
        (65, 48, 53),
        (25, 470, 85, 160)
    )

    pygame.draw.rect(
        lienzo,
        (65, 48, 53),
        (640, 470, 85, 160)
    )

    pygame.draw.rect(
        lienzo,
        (112, 82, 73),
        (30, 470, 75, 22)
    )

    pygame.draw.rect(
        lienzo,
        (112, 82, 73),
        (645, 470, 75, 22)
    )

    # PATAS DEL SILLON
    pygame.draw.rect(
        lienzo,
        (35, 27, 25),
        (80, 620, 20, 38)
    )

    pygame.draw.rect(
        lienzo,
        (35, 27, 25),
        (660, 620, 20, 38)
    )

    # --------------------------------------------------
    # COJIN CAIDO
    # --------------------------------------------------

    pygame.draw.polygon(
        lienzo,
        (55, 51, 61),
        [
            (720, 570),
            (815, 550),
            (855, 620),
            (750, 650)
        ]
    )

    pygame.draw.line(
        lienzo,
        (119, 99, 103),
        (735, 580),
        (835, 610),
        3
    )

    # --------------------------------------------------
    # MESA DE CENTRO
    # --------------------------------------------------

    pygame.draw.ellipse(
        lienzo,
        (31, 25, 25),
        (390, 625, 400, 45)
    )

    pygame.draw.rect(
        lienzo,
        (67, 44, 36),
        (430, 525, 310, 22)
    )

    pygame.draw.rect(
        lienzo,
        (96, 66, 51),
        (440, 530, 290, 12)
    )

    pygame.draw.rect(
        lienzo,
        (38, 29, 27),
        (455, 545, 15, 95)
    )

    pygame.draw.rect(
        lienzo,
        (38, 29, 27),
        (700, 545, 15, 95)
    )

    # TAZA SOBRE LA MESA
    pygame.draw.rect(
        lienzo,
        (174, 161, 143),
        (560, 490, 35, 28)
    )

    pygame.draw.ellipse(
        lienzo,
        (205, 192, 173),
        (560, 485, 35, 10)
    )

    pygame.draw.circle(
        lienzo,
        (174, 161, 143),
        (598, 503),
        9,
        3
    )

    # --------------------------------------------------
    # ALFOMBRA
    # --------------------------------------------------

    pygame.draw.ellipse(
        lienzo,
        (48, 44, 54),
        (120, 570, 850, 160)
    )

    pygame.draw.ellipse(
        lienzo,
        (110, 87, 82),
        (155, 590, 780, 120),
        3
    )

    pygame.draw.ellipse(
        lienzo,
        (81, 69, 77),
        (290, 620, 500, 55),
        2
    )

    # --------------------------------------------------
    # PISO DE MADERA
    # --------------------------------------------------

    pygame.draw.rect(
        lienzo,
        PISO,
        (0, 635, ANCHO, 85)
    )

    pygame.draw.line(
        lienzo,
        (111, 83, 68),
        (0, 635),
        (ANCHO, 635),
        5
    )

    for x in range(0, ANCHO, 125):

        pygame.draw.line(
            lienzo,
            (69, 54, 50),
            (x, 640),
            (x + 25, ALTO),
            2
        )

    return lienzo


# --------------------------------------------------
# LUZ DE LA LAMPARA
# --------------------------------------------------

def dibujar_luz(lienzo, tiempo):

    brillo = int(
        12 + math.sin(tiempo * 2) * 4
    )

    luz = pygame.Surface(
        (ANCHO, ALTO),
        pygame.SRCALPHA
    )

    pygame.draw.ellipse(
        luz,
        (220, 177, 112, brillo),
        (690, 300, 230, 260)
    )

    lienzo.blit(luz, (0, 0))


# --------------------------------------------------
# CORALINE DESPERTANDO EN EL SALON
# --------------------------------------------------

def dibujar_coraline(lienzo, tiempo):

    # PEQUENO MOVIMIENTO AL INCORPORARSE
    movimiento = int(math.sin(tiempo * 2) * 2)

    # POSICION DE CORALINE
    x_coraline = 1110
    y_piso = 635 - movimiento

    # SOMBRA DEBAJO DEL PERSONAJE
    pygame.draw.ellipse(
        lienzo,
        (20, 20, 26),
        (1075, 625, 70, 14)
    )

    # DIBUJAR CORALINE CON SU RETRATO PIXEL ART
    personajes.dibujar_coraline_con_retrato(
        lienzo,
        x_coraline,
        y_piso
    )

# --------------------------------------------------
# DIBUJO PRINCIPAL
# --------------------------------------------------

def dibujar(ventana):

    if "fijo" not in CAPAS:
        CAPAS["fijo"] = crear_fijo()

    tiempo = pygame.time.get_ticks() / 1000

    lienzo = CAPAS["fijo"].copy()

    # ILUMINACION
    dibujar_luz(lienzo, tiempo)

    # PERSONAJE
    dibujar_coraline(lienzo, tiempo)

    mostrar(ventana, lienzo)