"""FONDO DIBUJADO CON CODIGO: EL OTRO PADRE YA NO PUEDE RESISTIR LA ORDEN.

En el sotano de sotano.py, la masa blanca se levanta y anda a ciegas de un
lado a otro con los brazos estirados, tanteando. Coraline esta a media
escalera, quieta. Se usa en la pantalla de antes del minijuego cap09_m01.

Lo que se mueve: el foco que se mece y la criatura que camina tanteando.
"""

import math

import pygame

from interfaz.fondos.pintura import ANCHO, ALTO
from interfaz.fondos.pintura import orillas_oscuras, mostrar
from interfaz.fondos import personajes
from interfaz.fondos import sotano

AVANCE_CORALINE = 0.35

CAPAS = {}


def crear_fijo() -> pygame.Surface:

    lienzo = pygame.Surface((ANCHO, ALTO))
    sotano.dibujar_sotano(lienzo)

    pie = sotano.punto_escalera(AVANCE_CORALINE)
    personajes.dibujar_coraline_chica(lienzo, pie[0], pie[1], True)

    orillas_oscuras(lienzo)

    return lienzo


def dibujar(ventana: pygame.Surface) -> None:

    """DIBUJA LA ESCENA COMPLETA EN LA VENTANA DEL JUEGO."""

    if "fijo" not in CAPAS:
        CAPAS["fijo"] = crear_fijo()

    tiempo = pygame.time.get_ticks() / 1000

    lienzo = CAPAS["fijo"].copy()

    sotano.dibujar_foco(lienzo, tiempo)
    x = 450 + int(math.sin(tiempo * 0.5) * 50)
    sotano.dibujar_padre_derretido(lienzo, x, sotano.Y_PISO, tiempo, 88, True, 1)

    mostrar(ventana, lienzo)
