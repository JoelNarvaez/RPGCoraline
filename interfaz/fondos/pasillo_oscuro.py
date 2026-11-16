"""FONDO DIBUJADO CON CODIGO: LA PUERTA ABIERTA Y EL PASILLO OSCURO.

Coraline abre otra vez la puerta del salon, pero ya no hay ladrillos: hay un
pasillo oscuro y humedo que se pierde a lo lejos, con una luz debil al
fondo. Ella esta en la entrada, a punto de cruzar. Se usa en cap03_n03.

Lo que se mueve: la luz del fondo late, sale aire frio por la puerta y cae
una gota del techo del pasillo.
"""

import math

import pygame

from interfaz.fondos.pintura import ANCHO, ALTO
from interfaz.fondos.pintura import mezclar, degradado, brillo, orillas_oscuras, mostrar
from interfaz.fondos import sala_actrices

Y_PISO = 300

X_CORALINE = 450

HUECO = pygame.Rect(500, 150, 92, Y_PISO - 150)        # la puerta abierta
FONDO_PASILLO = pygame.Rect(538, 206, 16, 24)          # la lucecita del final

COLOR_PARED = (52, 112, 116)

CAPAS = {}


def dibujar_salon(lienzo: pygame.Surface) -> None:

    """LA PARED VERDE AZULADA DEL SALON Y EL PISO, COMO EN LAS ESCENAS DEL CAPITULO 1."""

    degradado(lienzo, pygame.Rect(0, 0, ANCHO, Y_PISO), (18, 40, 44), COLOR_PARED, 24)

    for x in range(0, ANCHO, 18):
        pygame.draw.line(lienzo, mezclar(COLOR_PARED, (0, 0, 0), 0.15), (x, 40), (x, Y_PISO))

    pygame.draw.rect(lienzo, (34, 78, 82), (0, Y_PISO - 6, ANCHO, 6))
    degradado(lienzo, pygame.Rect(0, Y_PISO, ANCHO, ALTO - Y_PISO), (30, 58, 64), (12, 24, 30), 4)


def dibujar_pasillo(lienzo: pygame.Surface) -> None:

    """EL HUECO DE LA PUERTA CON UN PASILLO QUE SE ENCOGE HACIA EL FONDO."""

    pygame.draw.rect(lienzo, (16, 30, 34), HUECO.inflate(12, 6).move(0, -3))

    # MARCOS QUE SE VAN HACIENDO CHICOS Y OSCUROS: DAN PROFUNDIDAD
    pasos = 10

    for i in range(pasos):

        avance = i / pasos
        rect = pygame.Rect(
            int(HUECO.x + (FONDO_PASILLO.x - HUECO.x) * avance),
            int(HUECO.y + (FONDO_PASILLO.y - HUECO.y) * avance),
            int(HUECO.width + (FONDO_PASILLO.width - HUECO.width) * avance),
            int(HUECO.height + (FONDO_PASILLO.height - HUECO.height) * avance)
        )

        color = mezclar((40, 36, 40), (6, 6, 10), avance)
        pygame.draw.rect(lienzo, color, rect)
        pygame.draw.rect(lienzo, mezclar(color, (0, 0, 0), 0.4), rect, 1)

    # PIEDRAS SUELTAS EN LAS PAREDES DEL PASILLO
    for i in range(8):
        x = HUECO.x + 6 + (i * 23) % (HUECO.width - 12)
        y = HUECO.y + 10 + (i * 37) % (HUECO.height - 30)
        pygame.draw.rect(lienzo, (54, 50, 54), (x, y, 6, 3))

    # HOJA DE LA PUERTA ABIERTA HACIA EL FRENTE
    x = HUECO.right + 6
    hoja = [(x, HUECO.y - 3), (x + 30, HUECO.y + 10), (x + 30, Y_PISO + 12), (x, Y_PISO)]
    pygame.draw.polygon(lienzo, (86, 76, 74), hoja)
    pygame.draw.polygon(lienzo, (50, 44, 44), hoja, 1)
    pygame.draw.circle(lienzo, (16, 14, 18), (x + 24, 230), 3)                 # cerradura con la llave
    pygame.draw.line(lienzo, (16, 14, 18), (x + 24, 230), (x + 24, 240), 2)


def crear_fijo() -> pygame.Surface:

    lienzo = pygame.Surface((ANCHO, ALTO))

    dibujar_salon(lienzo)
    dibujar_pasillo(lienzo)
    sala_actrices.dibujar_coraline(lienzo, X_CORALINE)

    orillas_oscuras(lienzo)

    return lienzo


def crear_luz() -> pygame.Surface:

    capa = pygame.Surface((ANCHO, ALTO), pygame.SRCALPHA)
    brillo(capa, FONDO_PASILLO.center, 40, (210, 200, 170), 140)

    return capa


# --------------------------------------------------
# LO QUE SE MUEVE
# --------------------------------------------------

def dibujar_luz(lienzo: pygame.Surface, tiempo: float) -> None:

    """LA LUCECITA DEL FONDO SE PRENDE Y SE APAGA DESPACIO, COMO SI LLAMARA."""

    if "luz" not in CAPAS:
        CAPAS["luz"] = crear_luz()

    capa = CAPAS["luz"].copy()
    capa.set_alpha(int(170 + math.sin(tiempo * 1.5) * 80))
    lienzo.blit(capa, (0, 0))

    pygame.draw.rect(lienzo, (200, 190, 160), FONDO_PASILLO.inflate(-10, -12))


def dibujar_aire_frio(lienzo: pygame.Surface, tiempo: float) -> None:

    """HILOS DE AIRE FRIO QUE SALEN DEL PASILLO HACIA CORALINE."""

    capa = pygame.Surface((ANCHO, ALTO), pygame.SRCALPHA)

    for i in range(4):

        fase = (tiempo * 0.4 + i / 4) % 1
        x = int(HUECO.x + 10 - fase * 90)
        y = 200 + i * 22 + int(math.sin(tiempo * 2 + i) * 4)
        alfa = int(70 * math.sin(fase * math.pi))

        pygame.draw.line(capa, (190, 220, 230, alfa), (x, y), (x + 24, y - 2))

    lienzo.blit(capa, (0, 0))


def dibujar_gota(lienzo: pygame.Surface, tiempo: float) -> None:

    """UNA GOTA CAE DEL TECHO DEL PASILLO CADA 2 SEGUNDOS."""

    fase = tiempo % 2

    if fase < 0.8:
        y = HUECO.y + 14 + int(fase * fase * 120)
        pygame.draw.rect(lienzo, (150, 180, 190), (HUECO.x + 30, y, 1, 3))


def dibujar(ventana: pygame.Surface) -> None:

    """DIBUJA LA ESCENA COMPLETA EN LA VENTANA DEL JUEGO."""

    if "fijo" not in CAPAS:
        CAPAS["fijo"] = crear_fijo()

    tiempo = pygame.time.get_ticks() / 1000

    lienzo = CAPAS["fijo"].copy()

    dibujar_luz(lienzo, tiempo)
    dibujar_gota(lienzo, tiempo)
    dibujar_aire_frio(lienzo, tiempo)

    mostrar(ventana, lienzo)
