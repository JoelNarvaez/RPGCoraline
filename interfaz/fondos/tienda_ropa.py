"""FONDO DIBUJADO CON CODIGO: LA TIENDA DE ROPA DEL CENTRO.

La mama lleva a Coraline a comprar ropa para la escuela. Coraline se queda
viendo unos guantes verdes fosforescentes en un exhibidor, mientras su mama
ya trae en los brazos las camisas grises. Atras hay repisas con pilas de ropa
(casi toda gris) y un perchero. Se usa en cap03_n01.

Coraline es la chica de sala_actrices.py; la mama esta en personajes.py.

Lo que se mueve: los guantes brillan como si latieran, una lampara del techo
parpadea.
"""

import math

import pygame

from interfaz.fondos.pintura import ANCHO, ALTO
from interfaz.fondos.pintura import mezclar, degradado, brillo, orillas_oscuras, mostrar
from interfaz.fondos import personajes
from interfaz.fondos import sala_actrices

Y_PISO = 300

X_CORALINE = 436
X_MAMA = 598
EXHIBIDOR = pygame.Rect(484, 252, 40, Y_PISO - 252)
GUANTES = (504, 238)      # centro de los guantes, arriba del exhibidor

COLOR_PARED = (176, 186, 178)
COLOR_REPISA = (150, 112, 76)
COLOR_VERDE = (130, 255, 90)

# PILAS DE ROPA EN LAS REPISAS: (x, y de la repisa, color)
PILAS = [
    (420, 96, (140, 142, 148)), (446, 96, (150, 152, 156)), (472, 96, (130, 132, 138)),
    (498, 96, (196, 90, 90)), (524, 96, (146, 148, 152)), (550, 96, (136, 138, 144)),
    (420, 150, (150, 152, 156)), (446, 150, (90, 120, 180)), (472, 150, (144, 146, 152)),
    (498, 150, (138, 140, 146)), (524, 150, (152, 154, 158)), (550, 150, (220, 190, 80)),
]

LAMPARAS = [440, 540, 630]

CAPAS = {}


def dibujar_tienda(lienzo: pygame.Surface) -> None:

    """PARED VERDE GRISACEA, REPISAS CON ROPA, PERCHERO, LAMPARAS Y PISO DE CUADROS."""

    degradado(lienzo, pygame.Rect(0, 0, ANCHO, Y_PISO), (150, 160, 154), COLOR_PARED, 12)

    # TECHO Y LAMPARAS LARGAS (LA LUZ VA APARTE)
    pygame.draw.rect(lienzo, (120, 128, 124), (0, 0, ANCHO, 14))

    for x in LAMPARAS:
        pygame.draw.rect(lienzo, (90, 96, 94), (x - 22, 14, 44, 5))
        pygame.draw.rect(lienzo, (250, 252, 236), (x - 20, 19, 40, 2))

    # REPISAS CON PILAS DE ROPA DOBLADA
    for y in [96, 150]:
        pygame.draw.rect(lienzo, COLOR_REPISA, (408, y, 172, 5))
        pygame.draw.rect(lienzo, mezclar(COLOR_REPISA, (0, 0, 0), 0.3), (408, y + 5, 172, 2))

    for x, y, color in PILAS:
        for i in range(4):
            pygame.draw.rect(lienzo, color, (x, y - 8 - i * 7, 22, 7))
            pygame.draw.line(lienzo, mezclar(color, (0, 0, 0), 0.25), (x, y - 2 - i * 7), (x + 21, y - 2 - i * 7))

    # PERCHERO CON CAMISAS GRISES COLGADAS
    pygame.draw.line(lienzo, (90, 90, 96), (548, 176), (636, 176), 2)
    pygame.draw.line(lienzo, (90, 90, 96), (552, 176), (552, Y_PISO), 2)
    pygame.draw.line(lienzo, (90, 90, 96), (632, 176), (632, Y_PISO), 2)

    for x in range(558, 628, 14):
        pygame.draw.arc(lienzo, (70, 70, 76), (x, 172, 8, 8), 0, math.pi, 1)
        pygame.draw.polygon(lienzo, personajes.CAMISA_GRIS, [(x - 2, 180), (x + 10, 180), (x + 12, 214), (x - 4, 214)])
        pygame.draw.line(lienzo, personajes.CAMISA_GRIS_SOMBRA, (x + 10, 180), (x + 12, 214))

    # PISO DE CUADROS BLANCOS Y NEGROS
    pygame.draw.rect(lienzo, (210, 210, 204), (0, Y_PISO, ANCHO, ALTO - Y_PISO))

    for fila in range(6):
        for columna in range(ANCHO // 16 + 1):
            if (fila + columna) % 2 == 0:
                pygame.draw.rect(lienzo, (70, 72, 78), (columna * 16, Y_PISO + fila * 10, 16, 10))

    pygame.draw.rect(lienzo, (110, 116, 112), (0, Y_PISO - 4, ANCHO, 4))


def dibujar_exhibidor(lienzo: pygame.Surface) -> None:

    """EXHIBIDOR BLANCO CON LOS GUANTES VERDES FOSFORESCENTES ENCIMA."""

    pygame.draw.rect(lienzo, (236, 236, 230), EXHIBIDOR)
    pygame.draw.rect(lienzo, (180, 180, 176), EXHIBIDOR, 1)
    pygame.draw.rect(lienzo, (200, 200, 196), (EXHIBIDOR.x - 3, EXHIBIDOR.y - 3, EXHIBIDOR.width + 6, 4))

    # DOS GUANTES: PALMA Y CUATRO DEDOS CADA UNO, UN POCO DE LADO
    for dx in [-9, 7]:

        x = GUANTES[0] + dx
        y = GUANTES[1]

        pygame.draw.rect(lienzo, COLOR_VERDE, (x - 5, y, 10, 12), border_radius=2)

        for i in range(4):
            pygame.draw.rect(lienzo, COLOR_VERDE, (x - 5 + i * 3, y - 6 + abs(i - 1), 2, 7))

        pygame.draw.rect(lienzo, (60, 170, 50), (x - 5, y + 9, 10, 3))       # punos


def crear_fijo() -> pygame.Surface:

    lienzo = pygame.Surface((ANCHO, ALTO))

    dibujar_tienda(lienzo)
    personajes.dibujar_mama(lienzo, X_MAMA, Y_PISO, False, 1)
    personajes.dibujar_camisas(lienzo, personajes.manos_mama(X_MAMA, Y_PISO, False, 1))
    dibujar_exhibidor(lienzo)
    sala_actrices.dibujar_coraline(lienzo, X_CORALINE)

    for x in LAMPARAS:
        brillo(lienzo, (x, 30), 90, (250, 252, 240), 30)

    orillas_oscuras(lienzo)

    return lienzo


def crear_brillo_guantes() -> pygame.Surface:

    capa = pygame.Surface((80, 80), pygame.SRCALPHA)
    brillo(capa, (40, 40), 40, COLOR_VERDE, 120)

    return capa


# --------------------------------------------------
# LO QUE SE MUEVE
# --------------------------------------------------

def dibujar_brillo_guantes(lienzo: pygame.Surface, tiempo: float) -> None:

    """EL BRILLO VERDE DE LOS GUANTES LATE DESPACIO: A CORALINE LE ENCANTAN."""

    if "brillo" not in CAPAS:
        CAPAS["brillo"] = crear_brillo_guantes()

    capa = CAPAS["brillo"].copy()
    capa.set_alpha(int(150 + math.sin(tiempo * 3) * 100))

    lienzo.blit(capa, (GUANTES[0] - 40, GUANTES[1] - 36))


def dibujar_lampara_fallando(lienzo: pygame.Surface, tiempo: float) -> None:

    """LA LAMPARA DE EN MEDIO SE APAGA UN INSTANTE DE VEZ EN CUANDO."""

    fase = tiempo % 7

    if 5.0 < fase < 5.25 and int(fase * 30) % 2 == 0:
        sombra = pygame.Surface((90, 60), pygame.SRCALPHA)
        sombra.fill((0, 0, 0, 40))
        lienzo.blit(sombra, (LAMPARAS[1] - 45, 14))
        pygame.draw.rect(lienzo, (110, 112, 108), (LAMPARAS[1] - 20, 19, 40, 2))


def dibujar(ventana: pygame.Surface) -> None:

    """DIBUJA LA ESCENA COMPLETA EN LA VENTANA DEL JUEGO."""

    if "fijo" not in CAPAS:
        CAPAS["fijo"] = crear_fijo()

    tiempo = pygame.time.get_ticks() / 1000

    lienzo = CAPAS["fijo"].copy()

    dibujar_brillo_guantes(lienzo, tiempo)
    dibujar_lampara_fallando(lienzo, tiempo)

    mostrar(ventana, lienzo)
