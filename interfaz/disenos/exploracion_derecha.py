"""DISENO EXPLORACION_DERECHA: IGUAL QUE EXPLORACION, PERO CON LOS PANELES A LA DERECHA.

Para que no todas las escenas tengan la accion del mismo lado. Se usa junto
con "espejo": true en el nodo, que voltea el fondo dibujado: asi lo importante
de la escena queda a la izquierda y el texto a la derecha.
"""

import pygame

import config
from interfaz import piezas
from interfaz.disenos import exploracion

ANCHO_PANEL = exploracion.ANCHO_PANEL
X_PANEL = config.ANCHO - exploracion.X_PANEL - ANCHO_PANEL
Y_PANEL = exploracion.Y_PANEL
ALTO_BOTON = exploracion.ALTO_BOTON

ANCHO_TEXTO = exploracion.ANCHO_TEXTO
ESTILO = exploracion.ESTILO


def maximo_lineas(fuentes: dict) -> int:

    """RENGLONES QUE CABEN CON EL MAXIMO DE OPCIONES (LOS MISMOS QUE EN EXPLORACION)."""

    return exploracion.maximo_lineas(fuentes)


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
