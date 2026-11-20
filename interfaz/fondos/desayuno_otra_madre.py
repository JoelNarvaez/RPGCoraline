"""FONDO DIBUJADO CON CODIGO: EL DESAYUNO INCREIBLE DE LA OTRA MADRE.

La otra madre saca a Coraline del espejo y la sienta a desayunar en la misma
cocina amarilla de otra_cocina.py (cap03_n04), ahora de manana: torre de
hot cakes con miel, jugo de naranja, chocolate caliente y fruta. Coraline le
pregunta si le gustan los juegos y a la otra madre le brillan los botones de
emocion. Se usa en cap08_n01 y en su rama cap08_r01.

trato_juego.py (cap08_n02) usa esta misma cocina y esta misma mesa
(dibujar_mesa_desayuno).

Lo que se mueve: el vapor del chocolate, la miel que escurre y destellos de
emocion alrededor de los botones.
"""

import math

import pygame

from interfaz.fondos.pintura import ANCHO, ALTO
from interfaz.fondos.pintura import capa_vacia, pegar_con_contorno
from interfaz.fondos.pintura import brillo, orillas_oscuras, mostrar
from interfaz.fondos import personajes
from interfaz.fondos import sala_actrices
from interfaz.fondos import otra_cocina

Y_PISO = otra_cocina.Y_PISO
X_CORALINE = otra_cocina.X_CORALINE
X_MESA = otra_cocina.X_MESA
X_MADRE = otra_cocina.X_MADRE

HOT_CAKES = (X_MESA - 14, 236)          # el centro de abajo de la torre
CHOCOLATE = (X_MESA + 18, 236)          # la taza

CAPAS = {}


# --------------------------------------------------
# PARTE FIJA (TAMBIEN LA USA trato_juego.py)
# --------------------------------------------------

def dibujar_mesa_desayuno(lienzo: pygame.Surface) -> None:

    """LA MESA DE MANTEL A CUADROS CON EL DESAYUNO ENCIMA."""

    x = X_MESA

    pygame.draw.polygon(lienzo, (236, 230, 220), [(x - 34, 244), (x + 34, 244), (x + 38, Y_PISO), (x - 38, Y_PISO)])

    for xx in range(x - 34, x + 34, 8):
        pygame.draw.line(lienzo, (210, 90, 90), (xx, 244), (xx + 2, Y_PISO), 2)

    pygame.draw.ellipse(lienzo, (236, 230, 220), (x - 36, 238, 72, 12))

    # TORRE DE HOT CAKES CON MANTEQUILLA Y MIEL
    hx, hy = HOT_CAKES
    pygame.draw.ellipse(lienzo, (250, 248, 244), (hx - 12, hy + 1, 24, 6))
    for i in range(5):
        pygame.draw.ellipse(lienzo, (200, 140, 70), (hx - 9, hy - 3 - i * 3, 18, 5))
        pygame.draw.line(lienzo, (236, 186, 110), (hx - 7, hy - 3 - i * 3), (hx + 7, hy - 3 - i * 3))
    pygame.draw.ellipse(lienzo, (176, 100, 40), (hx - 8, hy - 17, 16, 4))                  # miel arriba
    pygame.draw.rect(lienzo, (250, 236, 150), (hx - 2, hy - 19, 4, 3))                      # mantequilla

    # TAZA DE CHOCOLATE
    cx, cy = CHOCOLATE
    pygame.draw.rect(lienzo, (240, 236, 230), (cx - 5, cy - 8, 10, 9))
    pygame.draw.ellipse(lienzo, (110, 60, 40), (cx - 5, cy - 9, 10, 3))
    pygame.draw.arc(lienzo, (240, 236, 230), (cx + 3, cy - 6, 6, 6), -1.6, 1.6, 2)

    # VASO DE JUGO Y PLATITO DE FRESAS
    pygame.draw.rect(lienzo, (250, 170, 50), (x + 30, 228, 6, 11))
    pygame.draw.line(lienzo, (255, 220, 150), (x + 31, 229), (x + 31, 237))
    pygame.draw.ellipse(lienzo, (250, 248, 244), (x - 34, 238, 14, 4))
    for dx in [-31, -27, -24]:
        pygame.draw.circle(lienzo, (220, 50, 60), (x + dx, 237), 2)


def crear_fijo() -> pygame.Surface:

    lienzo = pygame.Surface((ANCHO, ALTO))

    otra_cocina.dibujar_cocina(lienzo)

    capa = capa_vacia()
    personajes.dibujar_otra_madre(capa, X_MADRE, "normal")
    pegar_con_contorno(lienzo, capa)

    dibujar_mesa_desayuno(lienzo)
    sala_actrices.dibujar_coraline(lienzo, X_CORALINE, True)

    brillo(lienzo, (447, 104), 120, (255, 220, 160), 50)
    orillas_oscuras(lienzo)

    return lienzo


# --------------------------------------------------
# LO QUE SE MUEVE (TAMBIEN LO USA trato_juego.py)
# --------------------------------------------------

def dibujar_miel(lienzo: pygame.Surface, tiempo: float) -> None:

    """UNA GOTA DE MIEL QUE ESCURRE POR LA ORILLA DE LA TORRE Y VUELVE A EMPEZAR."""

    hx, hy = HOT_CAKES
    bajada = int((tiempo * 4) % 14)

    pygame.draw.line(lienzo, (176, 100, 40), (hx + 7, hy - 15), (hx + 8, hy - 15 + bajada), 2)


def dibujar_emocion(lienzo: pygame.Surface, tiempo: float) -> None:

    """DESTELLITOS QUE SALTAN ALREDEDOR DE LOS BOTONES: ESTA EMOCIONADA CON EL JUEGO."""

    for i in range(4):

        fase = (tiempo * 1.5 + i / 4) % 1
        angulo = i * 1.6 + 0.4
        distancia = 10 + int(fase * 10)
        x = X_MADRE + int(math.cos(angulo) * distancia)
        y = 146 + int(math.sin(angulo) * distancia * 0.6) - 4

        if fase < 0.7:
            color = (255, 236, 160)
            lienzo.set_at((x, y), color)
            if fase < 0.35:
                for dx, dy in [(-1, 0), (1, 0), (0, -1), (0, 1)]:
                    lienzo.set_at((x + dx, y + dy), color)


def dibujar(ventana: pygame.Surface) -> None:

    """DIBUJA LA ESCENA COMPLETA EN LA VENTANA DEL JUEGO."""

    if "fijo" not in CAPAS:
        CAPAS["fijo"] = crear_fijo()

    tiempo = pygame.time.get_ticks() / 1000

    lienzo = CAPAS["fijo"].copy()

    sala_actrices.dibujar_vapor(lienzo, CHOCOLATE[0], CHOCOLATE[1] - 10, tiempo)
    dibujar_miel(lienzo, tiempo)
    personajes.dibujar_botones(lienzo, personajes.ojos_otra_madre(X_MADRE), tiempo, False, True)
    dibujar_emocion(lienzo, tiempo)

    mostrar(ventana, lienzo)
