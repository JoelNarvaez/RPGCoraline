"""DISENO LIBRETA: LA HOJA DE CUADERNO DONDE CORALINE ANOTA EL RETO DE SU PAPA.

La narracion va sobre renglones azules con margen rojo y espiral arriba, y
las opciones se marcan como con resaltador. Se usa cuando Coraline cuenta
puertas y anota lo azul (cap01_n03 y cap01_m01).
"""

import pygame

from interfaz import piezas
from interfaz import animaciones


X_PANEL = 320
Y_PANEL = 40           # deja lugar arriba para la espiral
ANCHO_PANEL = 920
ALTO_BOTON = 44

ANCHO_TEXTO = ANCHO_PANEL - piezas.MARGEN * 2

X_PERSONAJE = 35
Y_PERSONAJE = 235
ANCHO_PERSONAJE = 245
ALTO_PERSONAJE = 425

COLOR_PAPEL = (250, 246, 232)
COLOR_RENGLON = (176, 199, 228)
COLOR_MARGEN = (222, 128, 128)
COLOR_ESPIRAL = (120, 124, 134)

# EL PAPEL LO DIBUJA ESTE DISENO, POR ESO EL PANEL VA TRANSPARENTE
ESTILO = {
    "panel": (0, 0, 0, 0),
    "borde": (214, 204, 182),
    "texto": (40, 44, 70),
    "texto_secundario": (120, 120, 140),
    "acento": (52, 88, 160),
    "boton": (0, 0, 0, 0),
    "boton_encima": (255, 232, 120, 190),
}


def maximo_lineas(fuentes: dict) -> int:

    """RENGLONES QUE CABEN CON EL MAXIMO DE OPCIONES."""

    return piezas.maximo_lineas(Y_PANEL, ALTO_BOTON, fuentes)


def hoja(
    ventana: pygame.Surface,
    rect: pygame.Rect,
    y_renglones: int,
    alto_renglon: int,
    con_espiral: bool
) -> None:

    """UNA HOJA DE CUADERNO: SOMBRA, PAPEL, RENGLONES, MARGEN Y ESPIRAL."""

    sombra = rect.move(6, 8)

    piezas.rectangulo_con_transparencia(
        ventana,
        sombra,
        (0, 0, 0, 90),
        6
    )

    pygame.draw.rect(
        ventana,
        COLOR_PAPEL,
        rect,
        border_radius=6
    )

    # RENGLONES DESDE y_renglones HASTA EL FINAL DE LA HOJA
    y = y_renglones

    while y < rect.bottom - 8:

        pygame.draw.line(
            ventana,
            COLOR_RENGLON,
            (rect.x + 6, y),
            (rect.right - 6, y),
            1
        )

        y = y + alto_renglon

    # MARGEN ROJO A LA IZQUIERDA DEL TEXTO
    x_margen = rect.x + piezas.MARGEN - 10

    pygame.draw.line(
        ventana,
        COLOR_MARGEN,
        (x_margen, rect.y + 4),
        (x_margen, rect.bottom - 4),
        2
    )

    if not con_espiral:
        return

    # ARILLOS DE LA ESPIRAL SOBRE EL BORDE DE ARRIBA
    x = rect.x + 40

    while x < rect.right - 30:

        pygame.draw.circle(ventana, (60, 58, 66), (x, rect.y + 10), 5)

        pygame.draw.arc(
            ventana,
            COLOR_ESPIRAL,
            (x - 7, rect.y - 16, 14, 30),
            0,
            3.1416,
            3
        )

        x = x + 34


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

    # HOJA DE LA NARRACION: LOS RENGLONES QUEDAN JUSTO DEBAJO DE CADA LINEA
    alto_historia = piezas.alto_panel_historia(
        len(contexto["lineas"]),
        fuentes
    )

    y_primer_renglon = (
        Y_PANEL
        + piezas.MARGEN // 2
        + piezas.alto_encabezado(fuentes)
        + fuentes["narracion"].get_height()
    )

    hoja(
        ventana,
        pygame.Rect(X_PANEL, Y_PANEL, ANCHO_PANEL, alto_historia),
        y_primer_renglon,
        piezas.alto_renglon(fuentes),
        True
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

    # SEGUNDA HOJA PARA LAS OPCIONES, SOLO CUANDO YA SE VEN
    y_opciones = y_final + piezas.SEPARACION_PANELES

    if animaciones.texto_terminado(contexto, contexto["total_letras"]):

        alto_opciones = piezas.alto_panel_opciones(
            len(contexto["opciones"]),
            ALTO_BOTON,
            fuentes
        )

        y_primer_boton = (
            y_opciones
            + piezas.MARGEN // 2
            + fuentes["opcion"].get_height() + 12
        )

        hoja(
            ventana,
            pygame.Rect(X_PANEL, y_opciones, ANCHO_PANEL, alto_opciones),
            y_primer_boton + ALTO_BOTON,
            ALTO_BOTON + piezas.SEPARACION_BOTONES,
            False
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
