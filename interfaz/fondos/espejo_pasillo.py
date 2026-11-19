"""FONDO DIBUJADO CON CODIGO: EL GATO SE SIENTA FRENTE AL ESPEJO DEL PASILLO.

El gato negro entra a la casa y se sienta frente al espejo de cuerpo entero
del pasillo, como si quisiera que Coraline mirara ahi. Es el pasillo de su
casa de verdad, de dia y con luz gris (de noche se ve en pasillo_noche.py).
Coraline viene del lado de la cocina. El gato es el de personajes.py. Se usa
en cap05_n03 y en sus ramas cap05_r03 y cap05_r04.

espejo_padres.py usa este mismo pasillo y este mismo espejo (dibujar_pasillo,
dibujar_marco, ESPEJO y VIDRIO) para cuando aparecen los papas.

Lo que se mueve: un reflejo de luz cruza el vidrio, el gato parpadea despacio
y flotan motitas de polvo.
"""

import math

import pygame

from interfaz.fondos.pintura import ANCHO, ALTO
from interfaz.fondos.pintura import mezclar, degradado, brillo, orillas_oscuras, mostrar
from interfaz.fondos.pintura import tablas_de_madera, COLOR_CONTORNO
from interfaz.fondos import personajes
from interfaz.fondos import sala_actrices

Y_PISO = 300

X_CORALINE = 452
X_GATO = 552

ESPEJO = pygame.Rect(508, 64, 112, 230)                      # el marco completo
VIDRIO = pygame.Rect(ESPEJO.x + 9, ESPEJO.y + 20, ESPEJO.width - 18, ESPEJO.height - 34)
PUERTA_COCINA = pygame.Rect(404, 120, 56, Y_PISO - 120)      # de ahi viene la luz gris

COLOR_PARED = (104, 112, 106)
COLOR_MARCO = (78, 50, 36)
COLOR_MARCO_LUZ = (128, 90, 60)
COLOR_VIDRIO_ARRIBA = (118, 132, 140)
COLOR_VIDRIO_ABAJO = (70, 80, 92)

CAPAS = {}


# --------------------------------------------------
# PARTE FIJA
# --------------------------------------------------

def dibujar_pasillo(lienzo: pygame.Surface) -> None:

    """PARED VERDE GRISACEA CON RAYAS, LAMBRIN, LA PUERTA DE LA COCINA Y PISO DE TABLAS."""

    degradado(lienzo, pygame.Rect(0, 0, ANCHO, Y_PISO), (70, 78, 76), COLOR_PARED, 12)

    # PAPEL TAPIZ DE RAYAS FINAS
    for x in range(0, ANCHO, 12):
        pygame.draw.line(lienzo, mezclar(COLOR_PARED, (0, 0, 0), 0.12), (x, 0), (x, 220))
        pygame.draw.line(lienzo, mezclar(COLOR_PARED, (255, 255, 255), 0.06), (x + 6, 0), (x + 6, 220))

    # LAMBRIN DE MADERA
    pygame.draw.rect(lienzo, (74, 60, 52), (0, 220, ANCHO, Y_PISO - 220))
    pygame.draw.rect(lienzo, (96, 78, 64), (0, 218, ANCHO, 4))

    for x in range(6, ANCHO, 40):
        pygame.draw.rect(lienzo, (62, 50, 44), (x, 230, 32, Y_PISO - 240), 1)

    # PUERTA DE LA COCINA (ABIERTA, SALE LUZ GRIS DE LA TARDE)
    pygame.draw.rect(lienzo, (96, 80, 62), PUERTA_COCINA.inflate(8, 6).move(0, -3))
    degradado(lienzo, PUERTA_COCINA, (176, 178, 168), (130, 132, 124), 6)
    pygame.draw.rect(lienzo, (150, 140, 120), (PUERTA_COCINA.x, Y_PISO - 14, PUERTA_COCINA.width, 14))

    # UN CUADRITO TORCIDO Y UN PERCHERO VACIO (NADIE HA COLGADO SU ABRIGO)
    pygame.draw.polygon(lienzo, (60, 46, 40), [(470, 80), (494, 78), (496, 100), (472, 102)])
    pygame.draw.polygon(lienzo, (150, 160, 150), [(473, 83), (491, 81), (493, 97), (475, 99)])
    pygame.draw.line(lienzo, (60, 46, 40), (480, 84), (486, 96))

    pygame.draw.rect(lienzo, (70, 54, 44), (628, 110, 12, 4))
    for x in [630, 636]:
        pygame.draw.line(lienzo, (70, 54, 44), (x, 114), (x, 120), 2)

    # PISO DE TABLAS
    tablas_de_madera(lienzo, pygame.Rect(0, Y_PISO, ANCHO, ALTO - Y_PISO), (92, 66, 50), 8)


def dibujar_marco(lienzo: pygame.Surface) -> None:

    """MARCO DE MADERA OSCURA CON CRESTA TALLADA ARRIBA Y PATAS SOBRE EL PISO."""

    # PATAS Y SOMBRA EN EL PISO
    sombra = pygame.Surface((ESPEJO.width + 10, 8), pygame.SRCALPHA)
    pygame.draw.ellipse(sombra, (0, 0, 0, 100), sombra.get_rect())
    lienzo.blit(sombra, (ESPEJO.x - 5, Y_PISO - 4))

    for x in [ESPEJO.x + 8, ESPEJO.right - 14]:
        pygame.draw.rect(lienzo, COLOR_MARCO, (x, ESPEJO.bottom - 4, 6, Y_PISO - ESPEJO.bottom + 4))

    # MARCO
    pygame.draw.rect(lienzo, COLOR_MARCO, ESPEJO.inflate(0, -14).move(0, 7), border_radius=4)
    pygame.draw.rect(lienzo, COLOR_MARCO_LUZ, ESPEJO.inflate(-6, -20).move(0, 7), 1, border_radius=3)

    # CRESTA TALLADA: UN ARCO CON VOLUTAS A LOS LADOS
    pygame.draw.ellipse(lienzo, COLOR_MARCO, (ESPEJO.x + 18, ESPEJO.y - 6, ESPEJO.width - 36, 30))
    pygame.draw.arc(lienzo, COLOR_MARCO_LUZ, (ESPEJO.x + 22, ESPEJO.y - 2, ESPEJO.width - 44, 22), 0.4, 2.7, 1)

    for lado in [-1, 1]:
        cx = ESPEJO.centerx + lado * (ESPEJO.width // 2 - 14)
        pygame.draw.circle(lienzo, COLOR_MARCO, (cx, ESPEJO.y + 12), 7)
        pygame.draw.circle(lienzo, COLOR_MARCO_LUZ, (cx, ESPEJO.y + 12), 3, 1)

    pygame.draw.circle(lienzo, (170, 130, 70), (ESPEJO.centerx, ESPEJO.y + 4), 3)                  # botoncito de laton

    # ORILLA OSCURA DEL MARCO Y DEL HUECO DEL VIDRIO PARA QUE SE VEA COMO SPRITE
    pygame.draw.rect(lienzo, COLOR_CONTORNO, ESPEJO.inflate(2, -12).move(0, 7), 1, border_radius=4)
    pygame.draw.rect(lienzo, COLOR_CONTORNO, VIDRIO.inflate(2, 2), 1)


def dibujar_vidrio(lienzo: pygame.Surface) -> None:

    """EL VIDRIO REFLEJA EL PASILLO, MAS OSCURO Y AZULADO."""

    degradado(lienzo, VIDRIO, COLOR_VIDRIO_ARRIBA, COLOR_VIDRIO_ABAJO, 8)

    for x in range(VIDRIO.x + 4, VIDRIO.right, 12):
        pygame.draw.line(lienzo, mezclar(COLOR_VIDRIO_ARRIBA, (0, 0, 0), 0.12), (x, VIDRIO.y), (x, VIDRIO.y + 130))

    pygame.draw.rect(lienzo, mezclar(COLOR_VIDRIO_ABAJO, (60, 40, 30), 0.4), (VIDRIO.x, VIDRIO.y + 130, VIDRIO.width, VIDRIO.height - 130))

    # BRILLO DIAGONAL FIJO EN UNA ESQUINA
    for i in range(3):
        pygame.draw.line(lienzo, mezclar(COLOR_VIDRIO_ARRIBA, (255, 255, 255), 0.35),
                         (VIDRIO.x + 6 + i * 4, VIDRIO.y + 30), (VIDRIO.x + 22 + i * 4, VIDRIO.y + 6))


def crear_fijo() -> pygame.Surface:

    lienzo = pygame.Surface((ANCHO, ALTO))

    dibujar_pasillo(lienzo)
    dibujar_marco(lienzo)
    dibujar_vidrio(lienzo)

    brillo(lienzo, PUERTA_COCINA.center, 90, (210, 214, 200), 40)
    sala_actrices.dibujar_coraline(lienzo, X_CORALINE, True)
    orillas_oscuras(lienzo)

    return lienzo


# --------------------------------------------------
# LO QUE SE MUEVE (TAMBIEN LO USA espejo_padres.py)
# --------------------------------------------------

def dibujar_destello(lienzo: pygame.Surface, tiempo: float) -> None:

    """UNA FRANJA DE LUZ CRUZA EL VIDRIO EN DIAGONAL CADA 5 SEGUNDOS."""

    fase = tiempo % 5

    if fase > 1.2:
        return

    capa = pygame.Surface(VIDRIO.size, pygame.SRCALPHA)
    x = int(-40 + fase / 1.2 * (VIDRIO.width + 80))

    pygame.draw.polygon(capa, (255, 255, 255, 60), [(x, 0), (x + 14, 0), (x - 26, VIDRIO.height), (x - 40, VIDRIO.height)])
    pygame.draw.polygon(capa, (255, 255, 255, 40), [(x + 20, 0), (x + 24, 0), (x - 16, VIDRIO.height), (x - 20, VIDRIO.height)])

    lienzo.blit(capa, VIDRIO.topleft)


def dibujar_polvo(lienzo: pygame.Surface, tiempo: float) -> None:

    """MOTITAS DE POLVO EN LA LUZ QUE SALE DE LA COCINA."""

    for i in range(10):

        x = PUERTA_COCINA.x + (i * 23 + int(tiempo * 3)) % 90
        y = 140 + int(math.sin(tiempo * 0.6 + i) * 14) + (i * 17) % 110

        lienzo.set_at((x, y), (214, 214, 200))


def dibujar(ventana: pygame.Surface) -> None:

    """DIBUJA LA ESCENA COMPLETA EN LA VENTANA DEL JUEGO."""

    if "fijo" not in CAPAS:
        CAPAS["fijo"] = crear_fijo()

    tiempo = pygame.time.get_ticks() / 1000

    lienzo = CAPAS["fijo"].copy()

    dibujar_destello(lienzo, tiempo)
    personajes.dibujar_gato(lienzo, X_GATO, Y_PISO + 2, False, tiempo)
    dibujar_polvo(lienzo, tiempo)

    mostrar(ventana, lienzo)
