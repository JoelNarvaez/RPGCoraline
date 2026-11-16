"""FONDO DIBUJADO CON CODIGO: CORALINE SOLA EN LA COCINA.

La mama salio de compras y el departamento esta en silencio. Coraline mira
hacia arriba: la llave negra cuelga de un clavo, muy alto, junto a la
alacena. Hay una silla a la mano. Se usa en cap03_n02.

Lo que se mueve: el segundero del reloj, el brillo de la llave y el polvo
que flota en la luz de la ventana.
"""

import math

import pygame

from interfaz.fondos.pintura import ANCHO, ALTO
from interfaz.fondos.pintura import mezclar, degradado, brillo, orillas_oscuras, mostrar
from interfaz.fondos import sala_actrices

Y_PISO = 300

X_CORALINE = 470
LLAVE = (606, 92)         # aro de la llave, colgada del clavo
RELOJ = (470, 70)

COLOR_PARED = (176, 168, 140)
COLOR_MUEBLE = (120, 136, 120)
COLOR_MUEBLE_SOMBRA = (90, 104, 92)

CAPAS = {}


def dibujar_cocina(lienzo: pygame.Surface) -> None:

    """PARED CREMA, ALACENA, BARRA CON FREGADERO, VENTANA GRIS, RELOJ Y PISO."""

    degradado(lienzo, pygame.Rect(0, 0, ANCHO, Y_PISO), (130, 124, 104), COLOR_PARED, 14)

    # AZULEJOS DETRAS DE LA BARRA
    for y in range(196, 236, 8):
        for x in range(500, ANCHO, 8):
            pygame.draw.rect(lienzo, mezclar(COLOR_PARED, (255, 255, 255), 0.25), (x, y, 7, 7))

    # VENTANA CON LUZ GRIS DE LA TARDE
    pygame.draw.rect(lienzo, (90, 80, 66), (404, 104, 54, 70))
    degradado(lienzo, pygame.Rect(408, 108, 46, 62), (190, 196, 200), (150, 158, 166), 4)
    pygame.draw.line(lienzo, (90, 80, 66), (431, 108), (431, 170), 2)
    pygame.draw.line(lienzo, (90, 80, 66), (408, 139), (454, 139), 2)

    # ALACENA ALTA
    for x in [504, 546]:
        pygame.draw.rect(lienzo, COLOR_MUEBLE, (x, 40, 40, 62))
        pygame.draw.rect(lienzo, COLOR_MUEBLE_SOMBRA, (x, 40, 40, 62), 1)
        pygame.draw.circle(lienzo, (200, 180, 120), (x + 34, 92), 2)

    # BARRA CON FREGADERO Y CAJONES
    pygame.draw.rect(lienzo, COLOR_MUEBLE, (500, 236, 140, Y_PISO - 236))
    pygame.draw.rect(lienzo, (210, 206, 196), (496, 230, 144, 7))

    for x in [506, 552, 598]:
        pygame.draw.rect(lienzo, COLOR_MUEBLE_SOMBRA, (x, 244, 38, 50), 1)
        pygame.draw.line(lienzo, (200, 180, 120), (x + 14, 252), (x + 24, 252), 2)

    pygame.draw.rect(lienzo, (150, 156, 160), (530, 226, 30, 5))
    pygame.draw.line(lienzo, (150, 156, 160), (545, 226), (545, 212), 2)
    pygame.draw.line(lienzo, (150, 156, 160), (545, 212), (552, 212), 2)

    # MARCO DE LA PUERTA, CON EL CLAVO DE LA LLAVE ARRIBA
    pygame.draw.rect(lienzo, (100, 82, 62), (594, 100, 46, 6))
    pygame.draw.rect(lienzo, (100, 82, 62), (594, 100, 6, 130))
    pygame.draw.rect(lienzo, (60, 50, 44), (LLAVE[0] - 1, LLAVE[1] - 10, 2, 4))      # clavo

    # PISO DE LOSETA
    pygame.draw.rect(lienzo, (150, 140, 120), (0, Y_PISO, ANCHO, ALTO - Y_PISO))

    for x in range(0, ANCHO, 20):
        pygame.draw.line(lienzo, (120, 110, 94), (x, Y_PISO), (x - 10, ALTO))

    for y in range(Y_PISO + 12, ALTO, 14):
        pygame.draw.line(lienzo, (120, 110, 94), (0, y), (ANCHO, y))

    # SILLA DE MADERA JUNTO A CORALINE
    pygame.draw.rect(lienzo, (120, 76, 48), (520, 256, 30, 5))
    pygame.draw.rect(lienzo, (120, 76, 48), (546, 214, 4, 44))
    pygame.draw.rect(lienzo, (120, 76, 48), (546, 216, 4, 4))
    pygame.draw.line(lienzo, (96, 60, 40), (522, 260), (522, Y_PISO), 3)
    pygame.draw.line(lienzo, (96, 60, 40), (548, 260), (548, Y_PISO), 3)

    # RELOJ DE PARED (LAS MANECILLAS VAN APARTE)
    pygame.draw.circle(lienzo, (80, 60, 50), RELOJ, 16)
    pygame.draw.circle(lienzo, (240, 234, 220), RELOJ, 13)

    for i in range(12):
        angulo = i * math.pi / 6
        punto = (RELOJ[0] + int(math.cos(angulo) * 11), RELOJ[1] + int(math.sin(angulo) * 11))
        lienzo.set_at(punto, (60, 50, 50))


def dibujar_llave(lienzo: pygame.Surface) -> None:

    """LA LLAVE NEGRA COLGADA DEL CLAVO, CON LOS DIENTES HACIA ABAJO."""

    x, y = LLAVE

    pygame.draw.circle(lienzo, (16, 14, 18), (x, y - 4), 5)
    pygame.draw.circle(lienzo, COLOR_PARED, (x, y - 4), 2)
    pygame.draw.rect(lienzo, (16, 14, 18), (x - 1, y, 3, 22))
    pygame.draw.rect(lienzo, (16, 14, 18), (x + 2, y + 15, 5, 3))
    pygame.draw.rect(lienzo, (16, 14, 18), (x + 2, y + 19, 4, 3))


def crear_fijo() -> pygame.Surface:

    lienzo = pygame.Surface((ANCHO, ALTO))

    dibujar_cocina(lienzo)
    dibujar_llave(lienzo)
    sala_actrices.dibujar_coraline(lienzo, X_CORALINE)

    brillo(lienzo, (431, 140), 120, (210, 220, 230), 45)
    orillas_oscuras(lienzo)

    return lienzo


# --------------------------------------------------
# LO QUE SE MUEVE
# --------------------------------------------------

def dibujar_reloj(lienzo: pygame.Surface, tiempo: float) -> None:

    """MANECILLAS FIJAS Y UN SEGUNDERO QUE BRINCA CADA SEGUNDO (TIC, TAC)."""

    x, y = RELOJ

    pygame.draw.line(lienzo, (40, 34, 34), (x, y), (x + 6, y - 3), 2)
    pygame.draw.line(lienzo, (40, 34, 34), (x, y), (x - 2, y - 9), 2)

    angulo = int(tiempo) * math.pi / 30 - math.pi / 2
    pygame.draw.line(lienzo, (190, 40, 40), (x, y), (x + int(math.cos(angulo) * 11), y + int(math.sin(angulo) * 11)))


def dibujar_destello_llave(lienzo: pygame.Surface, tiempo: float) -> None:

    """LA LLAVE BRILLA CADA 3 SEGUNDOS: COMO SI LLAMARA A CORALINE."""

    fase = tiempo % 3

    if fase < 0.4:
        tamano = 1 + int((0.2 - abs(fase - 0.2)) * 20)
        x, y = LLAVE[0] + 4, LLAVE[1] - 7
        pygame.draw.line(lienzo, (255, 250, 220), (x - tamano, y), (x + tamano, y))
        pygame.draw.line(lienzo, (255, 250, 220), (x, y - tamano), (x, y + tamano))


def dibujar_polvo(lienzo: pygame.Surface, tiempo: float) -> None:

    """MOTITAS DE POLVO QUE FLOTAN DESPACIO EN LA LUZ DE LA VENTANA."""

    for i in range(12):

        x = 420 + (i * 37 + int(tiempo * 4)) % 90
        y = 120 + int(math.sin(tiempo * 0.7 + i) * 18) + (i * 13) % 80

        lienzo.set_at((x, y), (236, 232, 216))


def dibujar(ventana: pygame.Surface) -> None:

    """DIBUJA LA ESCENA COMPLETA EN LA VENTANA DEL JUEGO."""

    if "fijo" not in CAPAS:
        CAPAS["fijo"] = crear_fijo()

    tiempo = pygame.time.get_ticks() / 1000

    lienzo = CAPAS["fijo"].copy()

    dibujar_reloj(lienzo, tiempo)
    dibujar_destello_llave(lienzo, tiempo)
    dibujar_polvo(lienzo, tiempo)

    mostrar(ventana, lienzo)
