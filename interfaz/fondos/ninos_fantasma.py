"""FONDO DIBUJADO CON CODIGO: APARECEN LOS TRES NINOS FANTASMA.

En el hueco detras del espejo (hueco_espejo.py) la oscuridad se llena con la
luz palida de tres ninos fantasma: el de capa y peluca blanca, la nina de
cofia y el mas pequeno. Flotan alrededor de Coraline; con su luz el hueco
parece no tener orillas. Se usa en cap07_n02 y en su rama cap07_r02.

Lo que se mueve: los fantasmas flotan subiendo y bajando, cada uno a su
ritmo, y su luz late despacio.
"""

import math

import pygame

from interfaz.fondos.pintura import ANCHO, ALTO
from interfaz.fondos.pintura import brillo, orillas_oscuras, mostrar
from interfaz.fondos import sala_actrices
from interfaz.fondos import hueco_espejo

X_CORALINE = 476

# (QUIEN, x DEL CENTRO, y DONDE EMPIEZA LA CABEZA)
FANTASMAS = [("pequeno", 436, 196), ("capa", 560, 184), ("cofia", 606, 194)]

CAPAS = {}


def crear_fijo() -> pygame.Surface:

    lienzo = pygame.Surface((ANCHO, ALTO))

    hueco_espejo.dibujar_hueco(lienzo, 0.35)

    for quien, x, y in FANTASMAS:
        brillo(lienzo, (x, y + 34), 50, (190, 206, 246), 45)

    sala_actrices.dibujar_coraline(lienzo, X_CORALINE, True)
    orillas_oscuras(lienzo)

    return lienzo


def dibujar(ventana: pygame.Surface) -> None:

    """DIBUJA LA ESCENA COMPLETA EN LA VENTANA DEL JUEGO."""

    if "fijo" not in CAPAS:
        CAPAS["fijo"] = crear_fijo()

    tiempo = pygame.time.get_ticks() / 1000

    lienzo = CAPAS["fijo"].copy()

    for i in range(len(FANTASMAS)):
        quien, x, y = FANTASMAS[i]
        alfa = 150 + int(math.sin(tiempo * 1.1 + i * 2) * 30)
        hueco_espejo.dibujar_fantasma(lienzo, quien, x, y, tiempo, alfa)

    mostrar(ventana, lienzo)
