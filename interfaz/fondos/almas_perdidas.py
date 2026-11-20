"""FONDO DIBUJADO CON CODIGO: LOS FANTASMAS LE CUENTAN QUE LES QUITARON EL ALMA.

Los tres ninos fantasma de hueco_espejo.py se acercan a Coraline. El de capa
piensa en sus almas: en una nube palida aparecen tres canicas de vidrio, las
almas que la otra madre escondio en algun lugar de la casa (Coraline las va
a encontrar en los capitulos 8 y 10). Se usa en cap07_n03 y en su rama
cap07_r03.

Lo que se mueve: los fantasmas flotan, las canicas brillan una por una y el
remolino de color dentro de cada canica da vueltas.
"""

import math

import pygame

from interfaz.fondos.pintura import ANCHO, ALTO
from interfaz.fondos.pintura import capa_vacia, pegar_con_contorno
from interfaz.fondos.pintura import brillo, orillas_oscuras, mostrar
from interfaz.fondos import sala_actrices
from interfaz.fondos import hueco_espejo

X_CORALINE = 486

FANTASMAS = [("cofia", 440, 192), ("pequeno", 552, 210), ("capa", 600, 184)]

NUBE = pygame.Rect(484, 40, 128, 62)
CANICAS = [(514, 72), (548, 66), (582, 72)]
COLORES_CANICA = [(120, 200, 230), (230, 150, 200), (160, 220, 150)]

CAPAS = {}


def dibujar_nube(lienzo: pygame.Surface) -> None:

    """NUBE DE PENSAMIENTO PALIDA, CON BOLITAS QUE BAJAN HACIA LA CABEZA DEL FANTASMA DE CAPA."""

    capa = capa_vacia()
    color = (214, 224, 244)

    for cx, cy, r in [(NUBE.x + 20, NUBE.centery, 22), (NUBE.centerx, NUBE.centery - 6, 30),
                      (NUBE.right - 22, NUBE.centery, 22), (NUBE.x + 44, NUBE.bottom - 14, 18),
                      (NUBE.right - 44, NUBE.bottom - 14, 18), (NUBE.centerx, NUBE.bottom - 10, 20)]:
        pygame.draw.circle(capa, color, (cx, cy), r)

    for cx, cy, r in [(596, 136, 6), (600, 154, 4), (602, 168, 3)]:
        pygame.draw.circle(capa, color, (cx, cy), r)

    pegar_con_contorno(lienzo, capa)


def crear_fijo() -> pygame.Surface:

    lienzo = pygame.Surface((ANCHO, ALTO))

    hueco_espejo.dibujar_hueco(lienzo, 0.35)

    for quien, x, y in FANTASMAS:
        brillo(lienzo, (x, y + 34), 50, (190, 206, 246), 45)

    sala_actrices.dibujar_coraline(lienzo, X_CORALINE, True)
    orillas_oscuras(lienzo)

    # LA NUBE VA DESPUES DE LAS ORILLAS PARA QUE NO SE OSCUREZCA
    dibujar_nube(lienzo)

    return lienzo


def dibujar_canicas(lienzo: pygame.Surface, tiempo: float) -> None:

    """TRES CANICAS CON UN REMOLINO DE COLOR ADENTRO; CADA SEGUNDO BRILLA UNA."""

    for i in range(len(CANICAS)):

        x, y = CANICAS[i]
        color = COLORES_CANICA[i]

        pygame.draw.circle(lienzo, (60, 70, 96), (x, y), 9)
        pygame.draw.circle(lienzo, (236, 242, 250), (x, y), 8)

        # REMOLINO: TRES PUNTOS QUE DAN VUELTAS
        for j in range(3):
            angulo = tiempo * 2 + j * 2.1 + i
            pygame.draw.circle(lienzo, color, (x + int(math.cos(angulo) * 4), y + int(math.sin(angulo) * 4)), 2)

        pygame.draw.circle(lienzo, color, (x, y), 2)
        lienzo.set_at((x - 3, y - 4), (255, 255, 255))

        # DESTELLO EN CRUZ SOBRE LA CANICA QUE LE TOCA
        if int(tiempo) % 3 == i:
            for dx, dy in [(-1, 0), (1, 0), (0, -1), (0, 1)]:
                pygame.draw.line(lienzo, (255, 255, 240), (x + dx * 10, y + dy * 10), (x + dx * 13, y + dy * 13))


def dibujar(ventana: pygame.Surface) -> None:

    """DIBUJA LA ESCENA COMPLETA EN LA VENTANA DEL JUEGO."""

    if "fijo" not in CAPAS:
        CAPAS["fijo"] = crear_fijo()

    tiempo = pygame.time.get_ticks() / 1000

    lienzo = CAPAS["fijo"].copy()

    for i in range(len(FANTASMAS)):
        quien, x, y = FANTASMAS[i]
        hueco_espejo.dibujar_fantasma(lienzo, quien, x, y, tiempo, 170)

    dibujar_canicas(lienzo, tiempo)

    mostrar(ventana, lienzo)
