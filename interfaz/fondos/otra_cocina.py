"""FONDO DIBUJADO CON CODIGO: LA COCINA DEL OTRO DEPARTAMENTO.

Es igual a la cocina de Coraline, pero mas bonita y calientita: papel tapiz
amarillo, ollas de cobre, una mesa puesta con velas. La otra madre (como la
mama, pero mas alta, palida y con ojos de boton) trae el pollo asado.
Se usa en cap03_n04.

Lo que se mueve: el vapor del pollo, la flama de la vela y el brillo de los
botones.
"""

import math

import pygame

from interfaz.fondos.pintura import ANCHO, ALTO
from interfaz.fondos.pintura import capa_vacia, pegar_con_contorno
from interfaz.fondos.pintura import mezclar, degradado, brillo, orillas_oscuras, mostrar
from interfaz.fondos import personajes
from interfaz.fondos import sala_actrices

Y_PISO = 300

X_CORALINE = 436
X_MESA = 508
X_MADRE = 592
VELA = (494, 222)         # punta de la vela (donde va la flama)

COLOR_PARED = (226, 186, 110)
COLOR_MUEBLE = (176, 96, 70)
COLOR_COBRE = (210, 120, 70)

CAPAS = {}


def dibujar_cocina(lienzo: pygame.Surface) -> None:

    """PAPEL TAPIZ AMARILLO A RAYAS, ALACENA ROJIZA, OLLAS DE COBRE, VENTANA AL ATARDECER."""

    degradado(lienzo, pygame.Rect(0, 0, ANCHO, Y_PISO), (170, 120, 70), COLOR_PARED, 14)

    for x in range(0, ANCHO, 12):
        pygame.draw.line(lienzo, mezclar(COLOR_PARED, (255, 255, 255), 0.2), (x, 0), (x, Y_PISO), 2)

    # VENTANA CON EL CIELO NARANJA DEL ATARDECER
    pygame.draw.rect(lienzo, (110, 60, 44), (420, 70, 54, 70))
    degradado(lienzo, pygame.Rect(424, 74, 46, 62), (250, 170, 110), (230, 110, 90), 5)
    pygame.draw.line(lienzo, (110, 60, 44), (447, 74), (447, 136), 2)
    pygame.draw.polygon(lienzo, (210, 70, 80), [(418, 66), (440, 66), (430, 120), (418, 140)])       # cortinas
    pygame.draw.polygon(lienzo, (210, 70, 80), [(476, 66), (454, 66), (464, 120), (476, 140)])

    # ALACENA ALTA Y BARRA
    pygame.draw.rect(lienzo, COLOR_MUEBLE, (540, 36, ANCHO - 540, 60))
    pygame.draw.rect(lienzo, COLOR_MUEBLE, (540, 226, ANCHO - 540, Y_PISO - 226))
    pygame.draw.rect(lienzo, (236, 226, 206), (536, 220, ANCHO - 536, 7))

    for x in range(546, ANCHO, 32):
        pygame.draw.rect(lienzo, mezclar(COLOR_MUEBLE, (0, 0, 0), 0.25), (x, 42, 28, 48), 1)
        pygame.draw.rect(lienzo, mezclar(COLOR_MUEBLE, (0, 0, 0), 0.25), (x, 234, 28, 58), 1)

    # OLLAS DE COBRE COLGADAS
    pygame.draw.line(lienzo, (80, 60, 50), (548, 112), (636, 112), 2)

    for x, tamano in [(560, 10), (584, 13), (612, 9)]:
        pygame.draw.line(lienzo, (80, 60, 50), (x, 112), (x, 118))
        pygame.draw.circle(lienzo, COLOR_COBRE, (x, 118 + tamano), tamano)
        pygame.draw.circle(lienzo, (250, 180, 120), (x - tamano // 3, 115 + tamano), 2)

    # PISO DE CUADROS ROJOS Y CREMA
    for fila in range(6):
        for columna in range(ANCHO // 16 + 1):
            color = (170, 70, 60) if (fila + columna) % 2 == 0 else (236, 220, 196)
            pygame.draw.rect(lienzo, color, (columna * 16, Y_PISO + fila * 10, 16, 10))


def dibujar_mesa(lienzo: pygame.Surface) -> None:

    """MESA CON MANTEL DE CUADROS, PLATOS, COPAS Y UNA VELA."""

    x = X_MESA

    pygame.draw.polygon(lienzo, (236, 230, 220), [(x - 34, 244), (x + 34, 244), (x + 38, Y_PISO), (x - 38, Y_PISO)])

    for xx in range(x - 34, x + 34, 8):
        pygame.draw.line(lienzo, (210, 90, 90), (xx, 244), (xx + 2, Y_PISO), 2)

    pygame.draw.ellipse(lienzo, (236, 230, 220), (x - 36, 238, 72, 12))

    # PLATOS Y COPAS
    for dx in [-20, 16]:
        pygame.draw.ellipse(lienzo, (250, 248, 244), (x + dx - 8, 240, 18, 5))
        pygame.draw.ellipse(lienzo, (200, 200, 210), (x + dx - 4, 241, 10, 3), 1)

    pygame.draw.polygon(lienzo, (210, 230, 240), [(x + 2, 232), (x + 8, 232), (x + 6, 238), (x + 4, 238)])
    pygame.draw.line(lienzo, (210, 230, 240), (x + 5, 238), (x + 5, 242))

    # VELA (LA FLAMA VA APARTE)
    pygame.draw.rect(lienzo, (240, 236, 220), (VELA[0] - 2, VELA[1] + 2, 4, 16))
    pygame.draw.ellipse(lienzo, (200, 170, 90), (VELA[0] - 5, VELA[1] + 16, 10, 4))


def crear_fijo() -> pygame.Surface:

    lienzo = pygame.Surface((ANCHO, ALTO))

    dibujar_cocina(lienzo)
    capa = capa_vacia()
    personajes.dibujar_otra_madre(capa, X_MADRE, "charola")
    pegar_con_contorno(lienzo, capa)
    dibujar_mesa(lienzo)
    sala_actrices.dibujar_coraline(lienzo, X_CORALINE)

    brillo(lienzo, (447, 104), 120, (255, 190, 120), 50)
    brillo(lienzo, VELA, 70, (255, 200, 120), 50)
    orillas_oscuras(lienzo)

    return lienzo


# --------------------------------------------------
# LO QUE SE MUEVE
# --------------------------------------------------

def dibujar_flama(lienzo: pygame.Surface, tiempo: float) -> None:

    """FLAMA DE LA VELA QUE BAILA UN POCO."""

    x, y = VELA
    baile = int(math.sin(tiempo * 9) * 1.5)

    pygame.draw.ellipse(lienzo, (255, 170, 60), (x - 2 + baile, y - 6, 5, 9))
    pygame.draw.ellipse(lienzo, (255, 240, 180), (x - 1 + baile, y - 3, 3, 5))


def dibujar(ventana: pygame.Surface) -> None:

    """DIBUJA LA ESCENA COMPLETA EN LA VENTANA DEL JUEGO."""

    if "fijo" not in CAPAS:
        CAPAS["fijo"] = crear_fijo()

    tiempo = pygame.time.get_ticks() / 1000

    lienzo = CAPAS["fijo"].copy()

    pollo = personajes.charola_otra_madre(X_MADRE)
    sala_actrices.dibujar_vapor(lienzo, pollo[0], pollo[1] - 8, tiempo)
    dibujar_flama(lienzo, tiempo)
    personajes.dibujar_botones(lienzo, personajes.ojos_otra_madre(X_MADRE), tiempo, False, True)

    mostrar(ventana, lienzo)
