"""DISENO PINK PALACE: PANELES CLAROS A LA DERECHA Y CORALINE A LA IZQUIERDA.

Es el diseno por defecto. El nodo puede ocultar a Coraline con
"mostrar_personaje": false.
"""

import pygame

from interfaz import piezas


X_PANEL = 320
Y_PANEL = 25
ANCHO_PANEL = 920
ALTO_BOTON = 44

ANCHO_TEXTO = ANCHO_PANEL - piezas.MARGEN * 2

X_PERSONAJE = 35
Y_PERSONAJE = 235
ANCHO_PERSONAJE = 245
ALTO_PERSONAJE = 425

ESTILO = {
    "panel": (244, 239, 231, 240),
    "borde": (207, 197, 187),
    "texto": (48, 48, 54),
    "texto_secundario": (105, 101, 105),
    "acento": (177, 103, 124),
    "boton": (226, 222, 216),
    "boton_encima": (231, 194, 204),
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

    if nodo.get("mostrar_personaje", True):

        piezas.personaje(
            ventana,
            "coraline_pixel_retrato.png",
            X_PERSONAJE,
            Y_PERSONAJE,
            ANCHO_PERSONAJE,
            ALTO_PERSONAJE
        )

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
