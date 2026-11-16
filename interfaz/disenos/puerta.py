"""DISENO PUERTA: LA PUERTA TALLADA DEL SALON.

Los dos paneles quedan dentro de una puerta de madera con arco, tallado,
manija y cerradura. La narracion va en un pergamino claro para que se lea
bien. Se usa en las escenas de la puerta (cap01_n04 y cap01_n05).

La puerta se dibuja desde el principio con el alto de las opciones, para
que no cambie de tamano cuando estas aparecen.
"""

import pygame

from interfaz import piezas


MARCO = 22             # grosor de la madera alrededor de los paneles
X_PANEL = 330
Y_PANEL = 8 + MARCO    # el arco de la puerta empieza en y = 8
ANCHO_PANEL = 900
ALTO_BOTON = 44

ANCHO_TEXTO = ANCHO_PANEL - piezas.MARGEN * 2

X_PERSONAJE = 35
Y_PERSONAJE = 235
ANCHO_PERSONAJE = 245
ALTO_PERSONAJE = 425

COLOR_MADERA = (78, 47, 29)
COLOR_MADERA_CLARA = (128, 84, 50)
COLOR_LATON = (196, 160, 82)
COLOR_CERRADURA = (25, 16, 12)

ESTILO = {
    "panel": (238, 224, 198, 248),
    "borde": (150, 108, 68),
    "texto": (52, 34, 22),
    "texto_secundario": (120, 92, 66),
    "acento": (128, 58, 34),
    "boton": (222, 204, 170),
    "boton_encima": (230, 196, 120),
}


def maximo_lineas(fuentes: dict) -> int:

    """RENGLONES QUE CABEN CON EL MAXIMO DE OPCIONES.

    La madera ocupa MARCO arriba y MARCO abajo, por eso se le resta ese espacio.
    """

    return piezas.maximo_lineas(Y_PANEL + MARCO, ALTO_BOTON, fuentes)


def dibujar_puerta(
    ventana: pygame.Surface,
    rect: pygame.Rect,
    y_division: int
) -> None:

    """MADERA CON ARCO, TALLADO, MANIJA Y CERRADURA."""

    radio_arco = 80

    # SOMBRA CON LA MISMA FORMA DE ARCO QUE LA PUERTA
    sombra = pygame.Surface((rect.width, rect.height), pygame.SRCALPHA)

    pygame.draw.rect(
        sombra,
        (0, 0, 0, 110),
        sombra.get_rect(),
        border_radius=10,
        border_top_left_radius=radio_arco,
        border_top_right_radius=radio_arco
    )

    ventana.blit(sombra, (rect.x + 8, rect.y + 10))

    # MADERA

    pygame.draw.rect(
        ventana,
        COLOR_MADERA,
        rect,
        border_radius=10,
        border_top_left_radius=radio_arco,
        border_top_right_radius=radio_arco
    )

    # TALLADO: UN MARCO MAS CLARO POR DENTRO
    tallado = rect.inflate(-10, -10)

    pygame.draw.rect(
        ventana,
        COLOR_MADERA_CLARA,
        tallado,
        2,
        border_radius=8,
        border_top_left_radius=radio_arco - 5,
        border_top_right_radius=radio_arco - 5
    )

    # MANIJA Y CERRADURA EN LA MADERA DE LA DERECHA, ENTRE LOS DOS PANELES
    x_manija = rect.right - MARCO // 2

    pygame.draw.circle(ventana, COLOR_LATON, (x_manija, y_division - 14), 8)
    pygame.draw.circle(ventana, COLOR_MADERA, (x_manija, y_division - 14), 3)

    pygame.draw.circle(ventana, COLOR_CERRADURA, (x_manija, y_division + 10), 4)

    pygame.draw.polygon(
        ventana,
        COLOR_CERRADURA,
        [
            (x_manija, y_division + 10),
            (x_manija - 4, y_division + 22),
            (x_manija + 4, y_division + 22)
        ]
    )


def dibujar(
    ventana: pygame.Surface,
    contexto: dict,
    nodo: dict
) -> list:

    """DIBUJA LA ESCENA Y REGRESA LOS RECTANGULOS DE LAS OPCIONES."""

    fuentes = contexto["fuentes"]

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

    # MEDIMOS TODO ANTES PARA DIBUJAR LA PUERTA COMPLETA DESDE EL INICIO
    alto_historia = piezas.alto_panel_historia(
        len(contexto["lineas"]),
        fuentes
    )

    alto_opciones = piezas.alto_panel_opciones(
        len(contexto["opciones"]),
        ALTO_BOTON,
        fuentes
    )

    y_opciones = Y_PANEL + alto_historia + piezas.SEPARACION_PANELES

    puerta = pygame.Rect(
        X_PANEL - MARCO,
        Y_PANEL - MARCO,
        ANCHO_PANEL + MARCO * 2,
        y_opciones + alto_opciones + MARCO - (Y_PANEL - MARCO)
    )

    dibujar_puerta(
        ventana,
        puerta,
        y_opciones - piezas.SEPARACION_PANELES // 2
    )

    piezas.panel_historia(
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
        y_opciones,
        ANCHO_PANEL,
        ALTO_BOTON,
        ESTILO
    )

    piezas.controles(ventana, fuentes)

    return rectangulos
