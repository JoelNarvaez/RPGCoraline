"""FONDO DIBUJADO CON CODIGO: AFUERA DE LA CASA, DE NOCHE Y CON VIENTO.

Coraline sale de noche a buscar a sus papas, pero afuera solo hay oscuridad
y el viento entre los arboles. La casona rosa es la de regreso_niebla.py,
ahora de noche: casi todas las ventanas apagadas, menos las del departamento
de Coraline, que dejo todas las luces prendidas. Se usa en cap05_r01.

Lo que se mueve: los arboles se mecen con el viento, vuelan hojas y la luz
de la puerta titila.
"""

import math

import pygame

from interfaz.fondos.pintura import ANCHO, ALTO
from interfaz.fondos.pintura import mezclar, degradado, brillo, orillas_oscuras, mostrar
from interfaz.fondos import regreso_niebla
from interfaz.fondos import sala_actrices

Y_PISO = regreso_niebla.Y_PISO

X_CORALINE = 470
PUERTA = regreso_niebla.PUERTA
FOCO = regreso_niebla.FOCO

# ARBOLES DEL FONDO: (x del tronco, alto, ancho de la copa)
ARBOLES = [(420, 120, 70), (468, 96, 56), (360, 140, 80)]

CAPAS = {}


# --------------------------------------------------
# PARTE FIJA
# --------------------------------------------------

def dibujar_cielo(lienzo: pygame.Surface) -> None:

    """CIELO DE NOCHE, ESTRELLAS Y PASTO OSCURO."""

    degradado(lienzo, pygame.Rect(0, 0, ANCHO, Y_PISO), (6, 8, 24), (34, 40, 72), 12)

    for i in range(40):
        x = (i * 97) % ANCHO
        y = (i * 53) % 180
        lienzo.set_at((x, y), (200, 206, 240) if i % 3 else (150, 156, 200))

    pygame.draw.circle(lienzo, (230, 226, 200), (300, 46), 12)
    pygame.draw.circle(lienzo, (10, 12, 30), (306, 42), 11)                 # luna delgadita

    # PASTO Y CAMINO
    degradado(lienzo, pygame.Rect(0, Y_PISO, ANCHO, ALTO - Y_PISO), (24, 36, 30), (10, 16, 16), 4)

    for x in range(0, ANCHO, 6):
        alto = 3 + (x * 7) % 5
        pygame.draw.line(lienzo, (34, 52, 40), (x, Y_PISO), (x + 1, Y_PISO - alto))


def apagar_casa(lienzo: pygame.Surface) -> None:

    """LA CASA DE NOCHE: SE OSCURECE Y SE PRENDEN SOLO LAS VENTANAS DE CORALINE."""

    capa = pygame.Surface((ANCHO, ALTO), pygame.SRCALPHA)
    pygame.draw.rect(capa, (8, 10, 34, 150), (490, 0, ANCHO - 490, Y_PISO))
    lienzo.blit(capa, (0, 0))

    # EL DEPARTAMENTO DE CORALINE CON TODAS LAS LUCES PRENDIDAS
    for rect in [(544, 120, 18, 26), (604, 120, 18, 26), (534, 226, 16, 36)]:
        regreso_niebla.ventana_blanca(lienzo, rect, True)


def crear_fijo() -> pygame.Surface:

    lienzo = pygame.Surface((ANCHO, ALTO))

    dibujar_cielo(lienzo)
    regreso_niebla.dibujar_casa(lienzo)
    apagar_casa(lienzo)

    for rect in [(544, 120, 18, 26), (604, 120, 18, 26), (534, 226, 16, 36)]:
        brillo(lienzo, (rect[0] + rect[2] // 2, rect[1] + rect[3] // 2), 30, (255, 210, 130), 50)

    return lienzo


# --------------------------------------------------
# LO QUE SE MUEVE
# --------------------------------------------------

def dibujar_arboles(lienzo: pygame.Surface, tiempo: float) -> None:

    """SILUETAS DE ARBOLES QUE SE INCLINAN CON LAS RAFAGAS DE VIENTO."""

    rafaga = math.sin(tiempo * 1.3) * 0.6 + math.sin(tiempo * 3.1) * 0.25

    for x, alto, ancho in ARBOLES:

        punta = Y_PISO - alto
        inclinacion = int(rafaga * 6 * alto / 120)
        color = mezclar((10, 14, 22), (20, 26, 40), (x % 3) / 3)

        pygame.draw.polygon(lienzo, color, [(x - 4, Y_PISO), (x + 4, Y_PISO), (x + 2 + inclinacion // 2, punta + 30),
                                            (x - 2 + inclinacion // 2, punta + 30)])

        for i in range(4):
            cx = x + inclinacion + (i - 1) * ancho // 5
            cy = punta + 10 + (i % 2) * 18
            pygame.draw.ellipse(lienzo, color, (cx - ancho // 3, cy - 16, ancho * 2 // 3, 40))


def dibujar_hojas(lienzo: pygame.Surface, tiempo: float) -> None:

    """HOJITAS QUE EL VIENTO ARRASTRA DE IZQUIERDA A DERECHA."""

    for i in range(9):

        x = int((tiempo * (60 + i * 7) + i * 83) % (ANCHO + 40)) - 20
        y = 150 + (i * 31) % 140 + int(math.sin(tiempo * 4 + i) * 6)
        color = (120, 90, 50) if i % 2 else (90, 110, 60)

        pygame.draw.line(lienzo, color, (x, y), (x + 2, y + (1 if i % 3 else -1)))


def dibujar_foco(lienzo: pygame.Surface, tiempo: float) -> None:

    """EL FOCO DE LA PUERTA TITILA CON EL VIENTO."""

    fuerza = 50 + int(math.sin(tiempo * 7) * 10 + math.sin(tiempo * 17) * 6)

    brillo(lienzo, FOCO, 26, (255, 220, 150), fuerza)
    pygame.draw.circle(lienzo, (255, 236, 180), FOCO, 2)


def dibujar(ventana: pygame.Surface) -> None:

    """DIBUJA LA ESCENA COMPLETA EN LA VENTANA DEL JUEGO."""

    if "fijo" not in CAPAS:
        CAPAS["fijo"] = crear_fijo()
        CAPAS["orillas"] = pygame.Surface((ANCHO, ALTO), pygame.SRCALPHA)
        orillas_oscuras(CAPAS["orillas"])

    tiempo = pygame.time.get_ticks() / 1000

    lienzo = CAPAS["fijo"].copy()

    dibujar_arboles(lienzo, tiempo)
    dibujar_foco(lienzo, tiempo)
    sala_actrices.dibujar_coraline(lienzo, X_CORALINE, True)
    dibujar_hojas(lienzo, tiempo)
    lienzo.blit(CAPAS["orillas"], (0, 0))

    mostrar(ventana, lienzo)
