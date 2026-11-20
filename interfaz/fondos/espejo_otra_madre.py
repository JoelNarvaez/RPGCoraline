"""FONDO DIBUJADO CON CODIGO: LA OTRA MADRE ENCUENTRA A CORALINE FRENTE AL ESPEJO.

El pasillo lila del otro departamento (como la entrada de despedida_otros.py)
con un espejo de cuerpo entero. Coraline esta de espaldas al espejo, que la
refleja azulada. La otra madre le propone jugar a lo que quiera: en una
burbuja van pasando el avion (rayuela), un rompecabezas y una pelota. Se usa
en cap06_n04 y en su rama cap06_r04.

escarabajo_espejo.py (cap06_n05) usa este mismo pasillo y este mismo espejo
(dibujar_pasillo, dibujar_marco, ESPEJO y VIDRIO).

Lo que se mueve: los juegos que cambian en la burbuja, el reflejo de luz que
cruza el vidrio y el brillo de los botones.
"""

import math

import pygame

from interfaz.fondos.pintura import ANCHO, ALTO
from interfaz.fondos.pintura import capa_vacia, pegar_con_contorno, COLOR_CONTORNO
from interfaz.fondos.pintura import mezclar, degradado, brillo, orillas_oscuras, mostrar
from interfaz.fondos import personajes
from interfaz.fondos import sala_actrices

Y_PISO = 300

X_MADRE = 452
X_CORALINE = 520

ESPEJO = pygame.Rect(560, 60, 72, Y_PISO - 60)
VIDRIO = pygame.Rect(ESPEJO.x + 7, ESPEJO.y + 18, ESPEJO.width - 14, ESPEJO.height - 26)

COLOR_PARED = (150, 110, 150)
COLOR_MARCO = (120, 84, 50)
COLOR_MARCO_LUZ = (196, 156, 90)

BURBUJA = pygame.Rect(470, 70, 46, 34)
JUEGOS = ["avion", "rompecabezas", "pelota"]

CAPAS = {}


# --------------------------------------------------
# PARTE FIJA (TAMBIEN LA USA escarabajo_espejo.py)
# --------------------------------------------------

def dibujar_pasillo(lienzo: pygame.Surface) -> None:

    """PARED LILA CON MOLDURAS, UN CUADRO DE FLORES, UNA LAMPARA DE PARED Y PISO DE MADERA."""

    degradado(lienzo, pygame.Rect(0, 0, ANCHO, Y_PISO), (90, 60, 96), COLOR_PARED, 14)

    for x in range(410, ESPEJO.x - 30, 50):
        pygame.draw.rect(lienzo, mezclar(COLOR_PARED, (255, 255, 255), 0.15), (x, 60, 40, 140), 1)

    pygame.draw.rect(lienzo, (110, 76, 110), (0, 220, ANCHO, 4))

    # LAMPARA DE PARED ENTRE EL ESPEJO Y LA PARED
    pygame.draw.rect(lienzo, (170, 130, 70), (536, 110, 4, 12))
    pygame.draw.polygon(lienzo, (250, 220, 170), [(530, 100), (546, 100), (542, 112), (534, 112)])

    degradado(lienzo, pygame.Rect(0, Y_PISO, ANCHO, ALTO - Y_PISO), (110, 74, 54), (60, 40, 30), 4)

    for x in range(0, ANCHO, 24):
        pygame.draw.line(lienzo, (80, 52, 40), (x, Y_PISO), (x - 8, ALTO))


def dibujar_marco(lienzo: pygame.Surface) -> None:

    """MARCO DORADO CON CRESTA REDONDA Y SOMBRA EN EL PISO."""

    sombra = pygame.Surface((ESPEJO.width + 10, 8), pygame.SRCALPHA)
    pygame.draw.ellipse(sombra, (0, 0, 0, 100), sombra.get_rect())
    lienzo.blit(sombra, (ESPEJO.x - 5, Y_PISO - 4))

    pygame.draw.rect(lienzo, COLOR_MARCO, ESPEJO.inflate(0, -12).move(0, 6), border_radius=4)
    pygame.draw.rect(lienzo, COLOR_MARCO_LUZ, ESPEJO.inflate(-4, -16).move(0, 6), 1, border_radius=3)
    pygame.draw.ellipse(lienzo, COLOR_MARCO, (ESPEJO.x + 12, ESPEJO.y - 6, ESPEJO.width - 24, 26))
    pygame.draw.arc(lienzo, COLOR_MARCO_LUZ, (ESPEJO.x + 16, ESPEJO.y - 2, ESPEJO.width - 32, 18), 0.4, 2.7, 1)
    pygame.draw.circle(lienzo, COLOR_MARCO_LUZ, (ESPEJO.centerx, ESPEJO.y + 2), 3)

    pygame.draw.rect(lienzo, COLOR_CONTORNO, ESPEJO.inflate(2, -10).move(0, 6), 1, border_radius=4)
    pygame.draw.rect(lienzo, COLOR_CONTORNO, VIDRIO.inflate(2, 2), 1)


def dibujar_vidrio(lienzo: pygame.Surface) -> None:

    """EL VIDRIO REFLEJA EL PASILLO LILA Y A CORALINE, MAS OSCURO Y AZULADO."""

    degradado(lienzo, VIDRIO, (120, 104, 140), (70, 60, 90), 8)
    pygame.draw.rect(lienzo, (74, 56, 60), (VIDRIO.x, VIDRIO.bottom - 18, VIDRIO.width, 18))

    # EL REFLEJO DE CORALINE: MIRA AL LADO CONTRARIO Y SOLO SE VE LO QUE CABE EN EL VIDRIO
    reflejo = capa_vacia()
    personajes.dibujar_coraline_chica(reflejo, VIDRIO.x + 16, VIDRIO.bottom - 4, True)
    reflejo.fill((110, 120, 170, 150), special_flags=pygame.BLEND_RGBA_MULT)

    vieja = lienzo.get_clip()
    lienzo.set_clip(VIDRIO)
    lienzo.blit(reflejo, (0, 0))
    lienzo.set_clip(vieja)

    for i in range(3):
        pygame.draw.line(lienzo, (190, 180, 210), (VIDRIO.x + 4 + i * 4, VIDRIO.y + 26), (VIDRIO.x + 18 + i * 4, VIDRIO.y + 4))


def crear_fijo() -> pygame.Surface:

    lienzo = pygame.Surface((ANCHO, ALTO))

    dibujar_pasillo(lienzo)
    dibujar_marco(lienzo)
    dibujar_vidrio(lienzo)

    capa = capa_vacia()
    personajes.dibujar_otra_madre(capa, X_MADRE, "normal")
    pegar_con_contorno(lienzo, capa)

    sala_actrices.dibujar_coraline(lienzo, X_CORALINE, False)

    brillo(lienzo, (538, 106), 70, (255, 220, 170), 50)
    orillas_oscuras(lienzo)

    return lienzo


# --------------------------------------------------
# LO QUE SE MUEVE
# --------------------------------------------------

def dibujar_destello(lienzo: pygame.Surface, tiempo: float) -> None:

    """UNA FRANJA DE LUZ CRUZA EL VIDRIO EN DIAGONAL CADA 5 SEGUNDOS."""

    fase = tiempo % 5

    if fase > 1.2:
        return

    capa = pygame.Surface(VIDRIO.size, pygame.SRCALPHA)
    x = int(-40 + fase / 1.2 * (VIDRIO.width + 80))

    pygame.draw.polygon(capa, (255, 255, 255, 60), [(x, 0), (x + 12, 0), (x - 28, VIDRIO.height), (x - 40, VIDRIO.height)])

    lienzo.blit(capa, VIDRIO.topleft)


def dibujar_juego(lienzo: pygame.Surface, juego: str, x: int, y: int) -> None:

    """DIBUJITO DE UN JUEGO DENTRO DE LA BURBUJA. (x, y) ES EL CENTRO."""

    if juego == "avion":
        # RAYUELA: CUADROS EN COLUMNA, CON DOS LADO A LADO EN MEDIO
        for dx, dy in [(-3, 8), (-3, 2), (-6, -4), (0, -4), (-3, -10)]:
            pygame.draw.rect(lienzo, (240, 236, 230), (x + dx, y + dy, 6, 6))
            pygame.draw.rect(lienzo, (90, 70, 100), (x + dx, y + dy, 6, 6), 1)
        pygame.draw.circle(lienzo, (220, 70, 80), (x + 9, y + 10), 2)

    elif juego == "rompecabezas":
        pygame.draw.rect(lienzo, (90, 150, 220), (x - 8, y - 6, 12, 12))
        pygame.draw.circle(lienzo, (90, 150, 220), (x + 5, y), 3)
        pygame.draw.circle(lienzo, (90, 150, 220), (x - 2, y - 7), 3)
        pygame.draw.rect(lienzo, (240, 200, 80), (x + 2, y + 2, 8, 8))
        pygame.draw.circle(lienzo, (240, 200, 80), (x + 6, y + 1), 2)

    else:
        pygame.draw.circle(lienzo, (230, 80, 80), (x, y), 8)
        pygame.draw.line(lienzo, (250, 250, 240), (x - 8, y), (x + 8, y), 2)
        pygame.draw.circle(lienzo, (250, 250, 240), (x - 3, y - 3), 1)


def dibujar_burbuja(lienzo: pygame.Surface, tiempo: float) -> None:

    """LA OTRA MADRE OFRECE JUEGOS: CADA 1.5 SEGUNDOS CAMBIA EL DIBUJO DE LA BURBUJA."""

    juego = JUEGOS[int(tiempo / 1.5) % len(JUEGOS)]
    salto = int(abs(math.sin(tiempo * 4)) * 2)
    rect = BURBUJA.move(0, -salto)

    pygame.draw.ellipse(lienzo, COLOR_CONTORNO, rect.inflate(2, 2))
    pygame.draw.ellipse(lienzo, (246, 238, 240), rect)

    # PUNTITOS QUE BAJAN HACIA LA CABEZA DE LA OTRA MADRE
    for dx, dy, r in [(-10, 6, 3), (-18, 16, 2)]:
        centro = (rect.x + 4 + dx, rect.bottom + dy)
        pygame.draw.circle(lienzo, COLOR_CONTORNO, centro, r + 1)
        pygame.draw.circle(lienzo, (246, 238, 240), centro, r)

    dibujar_juego(lienzo, juego, rect.centerx, rect.centery)


def dibujar(ventana: pygame.Surface) -> None:

    """DIBUJA LA ESCENA COMPLETA EN LA VENTANA DEL JUEGO."""

    if "fijo" not in CAPAS:
        CAPAS["fijo"] = crear_fijo()

    tiempo = pygame.time.get_ticks() / 1000

    lienzo = CAPAS["fijo"].copy()

    dibujar_destello(lienzo, tiempo)
    personajes.dibujar_botones(lienzo, personajes.ojos_otra_madre(X_MADRE), tiempo, False, True)
    dibujar_burbuja(lienzo, tiempo)

    mostrar(ventana, lienzo)
