"""FONDO DIBUJADO CON CODIGO: EL SALON Y LA PUERTA CERRADA.

Coraline, con su libreta, mira la puerta pequena que acaba de encontrar. A la
derecha se asoma la entrada de la cocina con luz calida, y en lo alto del
marco cuelga la llave negra con un brillo. Se usa en cap01_n04.

Los colores siguen la ultima escena del recorrido de puertas (verde azulado
y penumbra) para que se sienta el mismo lugar.
"""

import math

import pygame

from interfaz.fondos.pintura import ANCHO, ALTO
from interfaz.fondos.pintura import mezclar, degradado, brillo, orillas_oscuras, mostrar
from interfaz.fondos import personajes

Y_PISO = 290

PUERTA = pygame.Rect(468, 212, 54, 78)
COCINA = pygame.Rect(584, 120, 56, Y_PISO - 120)   # hueco de la puerta de la cocina
LLAVE = (600, 100)                                  # donde cuelga la llave

COLOR_PARED = (52, 112, 116)
COLOR_LUZ_CALIDA = (255, 196, 120)

CAPAS = {}


# --------------------------------------------------
# PARTE FIJA
# --------------------------------------------------

def dibujar_pared(lienzo: pygame.Surface) -> None:

    """PARED LISA EN DEGRADADO, MOLDURA Y ZOCLO."""

    degradado(
        lienzo,
        pygame.Rect(0, 0, ANCHO, Y_PISO),
        mezclar(COLOR_PARED, (0, 0, 0), 0.6),
        COLOR_PARED,
        28
    )

    pygame.draw.rect(lienzo, (12, 26, 30), (0, 0, ANCHO, 10))
    pygame.draw.rect(lienzo, (40, 80, 84), (0, 10, ANCHO, 2))

    pygame.draw.rect(lienzo, (34, 78, 82), (0, Y_PISO - 8, ANCHO, 8))
    pygame.draw.line(lienzo, (70, 128, 130), (0, Y_PISO - 9), (ANCHO, Y_PISO - 9))

    # MARCOS VACIOS DE CUADROS VIEJOS (QUEDAN DETRAS DEL PANEL)
    for x, y, ancho, alto in [(120, 120, 60, 44), (210, 110, 40, 56)]:
        pygame.draw.rect(lienzo, (30, 64, 68), (x, y, ancho, alto), 2)


def dibujar_piso(lienzo: pygame.Surface) -> None:

    """PISO OSCURO VERDE AZULADO CON TABLAS QUE SE ABREN HACIA ABAJO."""

    degradado(lienzo, pygame.Rect(0, Y_PISO, ANCHO, ALTO - Y_PISO), (30, 58, 64), (10, 22, 28), 6)

    y = Y_PISO + 4
    separacion = 6

    while y < ALTO:

        pygame.draw.line(lienzo, (20, 40, 46), (0, y), (ANCHO, y))

        desfase = (y * 17) % 70

        for x in range(desfase, ANCHO, 70):
            pygame.draw.line(lienzo, (20, 40, 46), (x, y), (x, y + separacion))

        y = y + separacion
        separacion = separacion + 2


def dibujar_puerta(lienzo: pygame.Surface) -> None:

    """LA PUERTA PEQUENA: MADERA GRIS OSCURA, TABLERO EN ARCO Y CERRADURA."""

    madera = (86, 76, 74)
    clara = (112, 100, 96)
    oscura = (50, 44, 44)

    # MARCO HUNDIDO Y SOMBRA EN EL PISO
    pygame.draw.rect(lienzo, (18, 38, 42), PUERTA.inflate(8, 6).move(0, -3))
    pygame.draw.rect(lienzo, (10, 22, 26), (PUERTA.x - 4, PUERTA.bottom, PUERTA.width + 14, 4))

    pygame.draw.rect(lienzo, madera, PUERTA)
    pygame.draw.line(lienzo, clara, (PUERTA.x + 1, PUERTA.y + 1), (PUERTA.x + 1, PUERTA.bottom - 2))
    pygame.draw.line(lienzo, oscura, (PUERTA.right - 2, PUERTA.y + 1), (PUERTA.right - 2, PUERTA.bottom - 1))

    # VETAS DE LA MADERA
    for x in range(PUERTA.x + 6, PUERTA.right - 4, 7):
        pygame.draw.line(lienzo, mezclar(madera, oscura, 0.3), (x, PUERTA.y + 3), (x, PUERTA.bottom - 3))

    # TABLERO EN ARCO, CON DOBLE LINEA PARA QUE PAREZCA TALLADO
    tablero = pygame.Rect(PUERTA.x + 12, PUERTA.y + 9, PUERTA.width - 24, PUERTA.height - 20)

    pygame.draw.rect(lienzo, mezclar(madera, oscura, 0.2), tablero, border_top_left_radius=13,
                     border_top_right_radius=13)
    pygame.draw.rect(lienzo, oscura, tablero, 1, border_top_left_radius=13, border_top_right_radius=13)
    pygame.draw.rect(lienzo, clara, tablero.inflate(-6, -6), 1, border_top_left_radius=10,
                     border_top_right_radius=10)

    # MANIJA Y CERRADURA A LA IZQUIERDA
    pygame.draw.circle(lienzo, (34, 30, 30), (PUERTA.x + 6, PUERTA.centery), 3)
    pygame.draw.circle(lienzo, (150, 130, 90), (PUERTA.x + 6, PUERTA.centery), 2)
    pygame.draw.rect(lienzo, (10, 8, 8), (PUERTA.x + 5, PUERTA.centery + 6, 2, 5))
    pygame.draw.circle(lienzo, (10, 8, 8), (PUERTA.x + 6, PUERTA.centery + 6), 2)


def dibujar_cocina(lienzo: pygame.Surface, con_llave: bool) -> None:

    """ENTRADA DE LA COCINA CON LUZ CALIDA Y EL CLAVO DE LA LLAVE.

    Con con_llave = False solo se dibuja el clavo (la llave la tiene la mama).
    """

    # MARCO
    pygame.draw.rect(lienzo, (176, 168, 150), (COCINA.x - 10, COCINA.y - 12, COCINA.width + 20, COCINA.height + 12))
    pygame.draw.rect(lienzo, (130, 122, 110), (COCINA.x - 10, COCINA.y - 12, COCINA.width + 20, 4))

    # INTERIOR ILUMINADO
    degradado(lienzo, COCINA, (236, 184, 116), (150, 100, 66), 8)

    # PISO DE MOSAICO DENTRO DE LA COCINA
    for fila in range(4):
        y = COCINA.bottom - 28 + fila * 7
        for columna in range(10):
            x = COCINA.x + columna * 7 - fila * 2
            if (fila + columna) % 2 == 0:
                color = (214, 184, 140)
            else:
                color = (160, 116, 84)
            pygame.draw.rect(lienzo, color, (x, y, 7, 7))

    # GROSOR DE LA PARED: SOMBRA EN LA ORILLA IZQUIERDA Y ARRIBA DEL HUECO
    pygame.draw.rect(lienzo, (96, 70, 52), (COCINA.x, COCINA.y, 5, COCINA.height))
    pygame.draw.rect(lienzo, (120, 86, 60), (COCINA.x, COCINA.y, COCINA.width, 4))

    # ALACENA Y BARRA DENTRO DE LA COCINA
    pygame.draw.rect(lienzo, (120, 80, 56), (COCINA.x + 18, COCINA.y + 26, 38, 30))
    pygame.draw.rect(lienzo, (96, 62, 44), (COCINA.x + 18, COCINA.y + 26, 38, 30), 1)
    pygame.draw.rect(lienzo, (110, 72, 50), (COCINA.x + 24, COCINA.bottom - 58, 32, 30))
    pygame.draw.rect(lienzo, (210, 196, 170), (COCINA.x + 22, COCINA.bottom - 62, 34, 5))
    pygame.draw.rect(lienzo, (90, 58, 40), (COCINA.x + 28, COCINA.bottom - 52, 12, 18), 1)

    # CLAVO Y LLAVE NEGRA EN LO ALTO DEL MARCO
    x, y = LLAVE

    pygame.draw.rect(lienzo, (90, 86, 80), (x, y - 4, 2, 3))

    if not con_llave:
        return

    pygame.draw.circle(lienzo, (16, 14, 18), (x + 1, y + 3), 4)
    pygame.draw.circle(lienzo, (176, 168, 150), (x + 1, y + 3), 2)
    pygame.draw.rect(lienzo, (16, 14, 18), (x, y + 6, 2, 12))
    pygame.draw.rect(lienzo, (16, 14, 18), (x + 2, y + 14, 3, 2))
    pygame.draw.rect(lienzo, (16, 14, 18), (x + 2, y + 17, 2, 2))


def dibujar_coraline(lienzo: pygame.Surface) -> None:

    """CORALINE CHICA (personajes.py) VIENDO LA PUERTA."""

    personajes.dibujar_coraline_chica(lienzo, 412, Y_PISO + 16, True)


def dibujar_luces(lienzo: pygame.Surface) -> None:

    """LUZ CALIDA QUE SALE DE LA COCINA Y UNA LUZ FRIA SOBRE LA PUERTA."""

    luz = pygame.Surface((ANCHO, ALTO), pygame.SRCALPHA)

    pygame.draw.polygon(
        luz,
        (COLOR_LUZ_CALIDA[0], COLOR_LUZ_CALIDA[1], COLOR_LUZ_CALIDA[2], 34),
        [(COCINA.x, Y_PISO), (ANCHO, Y_PISO), (ANCHO, ALTO), (COCINA.x - 130, ALTO)]
    )

    lienzo.blit(luz, (0, 0))

    brillo(lienzo, (COCINA.x - 10, COCINA.centery + 40), 130, COLOR_LUZ_CALIDA, 95)
    brillo(lienzo, PUERTA.center, 80, (150, 225, 225), 85)

    orillas_oscuras(lienzo)


def crear_fijo() -> pygame.Surface:

    lienzo = pygame.Surface((ANCHO, ALTO))

    dibujar_pared(lienzo)
    dibujar_piso(lienzo)
    dibujar_cocina(lienzo, True)
    dibujar_puerta(lienzo)
    dibujar_coraline(lienzo)
    dibujar_luces(lienzo)

    return lienzo


# --------------------------------------------------
# LO QUE SE MUEVE
# --------------------------------------------------

def dibujar_polvo(lienzo: pygame.Surface, tiempo: float) -> None:

    """MOTAS DE POLVO FLOTANDO EN LA LUZ DE LA COCINA."""

    for i in range(14):

        x = COCINA.x - 40 + (i * 37) % 90 + int(math.sin(tiempo * 0.7 + i) * 6)
        y = COCINA.bottom - int((tiempo * 6 + i * 23) % 150)

        brillo_mota = 150 + int(math.sin(tiempo * 2 + i) * 60)

        lienzo.set_at((x, y), (brillo_mota, brillo_mota - 30, brillo_mota - 70))


def dibujar_destello_llave(lienzo: pygame.Surface, tiempo: float) -> None:

    """UN BRILLO QUE APARECE EN LA LLAVE CADA 3 SEGUNDOS."""

    fase = tiempo % 3

    if fase < 0.5:

        tamano = 3 if fase < 0.25 else 2

        x = LLAVE[0] + 4
        y = LLAVE[1] + 1

        pygame.draw.line(lienzo, (255, 250, 220), (x - tamano, y), (x + tamano, y))
        pygame.draw.line(lienzo, (255, 250, 220), (x, y - tamano), (x, y + tamano))


# --------------------------------------------------
# DIBUJAR
# --------------------------------------------------

def dibujar(ventana: pygame.Surface) -> None:

    """DIBUJA EL SALON COMPLETO EN LA VENTANA DEL JUEGO."""

    if "fijo" not in CAPAS:
        CAPAS["fijo"] = crear_fijo()

    tiempo = pygame.time.get_ticks() / 1000

    lienzo = CAPAS["fijo"].copy()

    dibujar_polvo(lienzo, tiempo)
    dibujar_destello_llave(lienzo, tiempo)

    mostrar(ventana, lienzo)
