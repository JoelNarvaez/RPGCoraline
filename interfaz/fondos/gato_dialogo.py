"""ESCENA DE CONVERSACION CON EL GATO.

CORALINE SE ACERCA AL GATO Y AMBOS SE MIRAN.
SE CONSERVA EL PINK PALACE COMO FONDO,
PERO LOS PERSONAJES PASAN A PRIMER PLANO.

"""

import pygame

from interfaz.fondos import exterior_gato
from interfaz.fondos import personajes

from interfaz.fondos.pintura import ANCHO, ALTO
from interfaz.fondos.pintura import brillo, mostrar


# POSICIONES DE LOS PERSONAJES
# (x ES EL CENTRO DEL SPRITE Y Y ES DONDE PISAN)

X_CORALINE = 420
Y_CORALINE = 300

X_GATO = 520
Y_GATO = 278       # ARRIBA DEL MURO

CAPAS = {}


# --------------------------------------------------
# ILUMINACION DE LA CONVERSACION
# --------------------------------------------------

def dibujar_iluminacion(lienzo):

    """DESTACAMOS A LOS PERSONAJES SIN OCULTAR LA CASA."""

    capa = pygame.Surface(
        (ANCHO, ALTO),
        pygame.SRCALPHA
    )

    capa.fill((8, 9, 20, 45))

    lienzo.blit(
        capa,
        (0, 0)
    )

    # LUZ SUAVE ENTRE LOS DOS PERSONAJES

    brillo(
        lienzo,
        (495, 235),
        115,
        (190, 137, 125),
        35
    )

    brillo(
        lienzo,
        (420, 250),
        65,
        (100, 126, 153),
        22
    )


# --------------------------------------------------
# ESCENA COMPLETA
# --------------------------------------------------

def crear_fijo():

    """PREPARAMOS EL FONDO Y A CORALINE."""

    lienzo = exterior_gato.crear_fijo().copy()

    # OSCURECEMOS UN POCO EL FONDO

    dibujar_iluminacion(lienzo)

    # CORALINE APARECE FRENTE AL GATO

    personajes.dibujar_coraline_chica(
        lienzo,
        X_CORALINE,
        Y_CORALINE,
        True
    )

    return lienzo


def dibujar(ventana):

    """DIBUJAMOS LA CONVERSACION."""

    if "fijo" not in CAPAS:

        CAPAS["fijo"] = crear_fijo()

    tiempo = pygame.time.get_ticks() / 1000

    lienzo = CAPAS["fijo"].copy()

    # LUCES DE LA MARQUESINA

    exterior_gato.dibujar_luces(
        lienzo,
        tiempo
    )

    # GATO EN PRIMER PLANO, MIRANDO A CORALINE (A LA IZQUIERDA)

    personajes.dibujar_gato(
        lienzo,
        X_GATO,
        Y_GATO,
        False,
        tiempo
    )

    mostrar(
        ventana,
        lienzo
    )