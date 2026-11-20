"""FONDO DIBUJADO CON CODIGO: LOS FANTASMAS LE ADVIERTEN QUE LA OTRA MADRE SIEMPRE GANA.

En el hueco detras del espejo (hueco_espejo.py) los tres fantasmas se ven mas
debiles y parpadean, como si se fueran a apagar. A Coraline se le encoge el
estomago, pero se acuerda de su papa y las avispas: el recuerdo sale en la
misma nube de valentia_gato.py (cap05_n05). Se usa en cap07_n04 y en su rama
cap07_r04.

Lo que se mueve: los fantasmas que se apagan y se prenden, las avispas que
zumban alrededor del papa del recuerdo y la Coraline chiquita que corre.
"""

import math

import pygame

from interfaz.fondos.pintura import ANCHO, ALTO
from interfaz.fondos.pintura import brillo, orillas_oscuras, mostrar
from interfaz.fondos import sala_actrices
from interfaz.fondos import hueco_espejo
from interfaz.fondos import valentia_gato

X_CORALINE = valentia_gato.X_CORALINE      # debajo de las bolitas de la nube

FANTASMAS = [("cofia", 438, 194), ("pequeno", 556, 214), ("capa", 604, 190)]

CAPAS = {}


def crear_fijo() -> pygame.Surface:

    lienzo = pygame.Surface((ANCHO, ALTO))

    hueco_espejo.dibujar_hueco(lienzo, 0.5)

    for quien, x, y in FANTASMAS:
        brillo(lienzo, (x, y + 34), 44, (170, 186, 230), 30)

    sala_actrices.dibujar_coraline(lienzo, X_CORALINE, True)
    orillas_oscuras(lienzo)

    valentia_gato.dibujar_nube(lienzo)
    valentia_gato.dibujar_recuerdo_fijo(lienzo)

    return lienzo


def dibujar(ventana: pygame.Surface) -> None:

    """DIBUJA LA ESCENA COMPLETA EN LA VENTANA DEL JUEGO."""

    if "fijo" not in CAPAS:
        CAPAS["fijo"] = crear_fijo()

    tiempo = pygame.time.get_ticks() / 1000

    lienzo = CAPAS["fijo"].copy()

    # SE APAGAN Y SE PRENDEN, COMO VELAS A PUNTO DE ACABARSE
    for i in range(len(FANTASMAS)):
        quien, x, y = FANTASMAS[i]
        alfa = 90 + int(math.sin(tiempo * 2.3 + i * 1.7) * 40 + math.sin(tiempo * 7 + i) * 15)
        hueco_espejo.dibujar_fantasma(lienzo, quien, x, y, tiempo, max(alfa, 20))

    valentia_gato.dibujar_avispas(lienzo, tiempo)
    valentia_gato.dibujar_coraline_recuerdo(lienzo, tiempo)

    mostrar(ventana, lienzo)
