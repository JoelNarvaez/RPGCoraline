"""DISENO EXPLORACION: PANELES OSCUROS A LA IZQUIERDA Y EL ESCENARIO LIBRE.

Pensado para fondos donde la imagen ya muestra a Coraline o el lugar
importa, por eso no dibuja al personaje.
"""

import pygame

from interfaz import piezas


X_PANEL = 45
Y_PANEL = 30
ANCHO_PANEL = 760
ALTO_BOTON = 40

ANCHO_TEXTO = ANCHO_PANEL - piezas.MARGEN * 2

ESTILO = {
    "panel": (25, 30, 43, 225),
    "borde": (155, 135, 143),
    "texto": (244, 237, 232),
    "texto_secundario": (205, 194, 194),
    "acento": (221, 157, 174),
    "boton": (38, 46, 62, 235),
    "boton_encima": (115, 69, 88, 245),
}


def maximo_lineas(fuentes: dict) -> int:

    """RENGLONES QUE CABEN CON EL MAXIMO DE OPCIONES."""

    return piezas.maximo_lineas(Y_PANEL, ALTO_BOTON, fuentes)


def dibujar(
    ventana: pygame.Surface,
    contexto: dict,
    nodo: dict
) -> list:

    """DIBUJA LA ESCENA Y REGRESA LOS RECTANGULOS DE LAS OPCIONES."""

    piezas.fondo(ventana, nodo)

    y_final = piezas.panel_historia(
        ventana,
        contexto,
        nodo,
        X_PANEL,
        Y_PANEL,
        ANCHO_PANEL,
        ESTILO
    )

    rectangulos = piezas.panel_opciones(
        ventana,
        contexto,
        X_PANEL,
        y_final + piezas.SEPARACION_PANELES,
        ANCHO_PANEL,
        ALTO_BOTON,
        ESTILO
    )

    piezas.controles(ventana, contexto["fuentes"])

    return rectangulos
