"""FONDO DIBUJADO CON CODIGO: CORALINE LE CUENTA AL GATO LO DE LAS AVISPAS.

El policia no le creyo. Esa noche, en su cuarto, Coraline le cuenta al gato
la vez que su papa se quedo quieto mientras lo picaban las avispas, para que
ella pudiera escapar. El recuerdo sale en una nube de pensamiento: el papa
quieto, rodeado de avispas, y Coraline chiquita corriendo. En el buro esta el
telefono con el que llamo a la policia. Coraline va en pijama (la de
pasillo_noche.py) y el gato esta echado en la cama. Se usa en cap05_n05.

Lo que se mueve: las avispas zumban alrededor del papa del recuerdo, la
Coraline del recuerdo corre, el gato parpadea y una nube tapa la luna.
"""

import math

import pygame

from interfaz.fondos.pintura import ANCHO, ALTO
from interfaz.fondos.pintura import mezclar, degradado, brillo, orillas_oscuras, mostrar
from interfaz.fondos.pintura import capa_vacia, pegar_con_contorno, tablas_de_madera, COLOR_CONTORNO
from interfaz.fondos import personajes
from interfaz.fondos import pasillo_noche

Y_PISO = 300

X_CORALINE = 486
X_GATO = 574
Y_CAMA = 254                                   # donde se apoya el gato (arriba del colchon)

VENTANA = pygame.Rect(418, 50, 52, 70)
BURO = pygame.Rect(404, 262, 34, Y_PISO - 262)
NUBE = pygame.Rect(498, 16, 136, 104)          # la nube del recuerdo
ESCENA = NUBE.inflate(-30, -30)                # el dibujito dentro de la nube

COLOR_PARED = (40, 46, 84)
COLOR_RECUERDO = (236, 222, 186)

CAPAS = {}


# --------------------------------------------------
# PARTE FIJA
# --------------------------------------------------

def dibujar_cuarto(lienzo: pygame.Surface) -> None:

    """PARED AZUL DE NOCHE CON ESTRELLITAS, VENTANA CON CORTINAS, PISO DE TABLAS."""

    degradado(lienzo, pygame.Rect(0, 0, ANCHO, Y_PISO), (20, 24, 50), COLOR_PARED, 12)

    for y in range(14, 250, 22):
        for x in range((y // 22 % 2) * 11, ANCHO, 22):
            lienzo.set_at((x, y), mezclar(COLOR_PARED, (255, 255, 255), 0.2))
            lienzo.set_at((x + 1, y), mezclar(COLOR_PARED, (255, 255, 255), 0.12))

    pygame.draw.rect(lienzo, (30, 34, 62), (0, 280, ANCHO, Y_PISO - 280))                     # zoclo

    # VENTANA: CIELO, LUNA, MARCO Y CORTINAS
    degradado(lienzo, VENTANA, (8, 10, 30), (26, 34, 70), 5)
    pygame.draw.circle(lienzo, (236, 232, 206), (VENTANA.x + 36, VENTANA.y + 16), 7)

    for dx, dy in [(8, 10), (20, 36), (42, 50), (12, 58), (30, 6)]:
        lienzo.set_at((VENTANA.x + dx, VENTANA.y + dy), (220, 220, 250))

    pygame.draw.rect(lienzo, (70, 60, 70), VENTANA.inflate(6, 6), 3)
    pygame.draw.line(lienzo, (70, 60, 70), (VENTANA.centerx, VENTANA.y), (VENTANA.centerx, VENTANA.bottom), 2)
    pygame.draw.line(lienzo, (70, 60, 70), (VENTANA.x, VENTANA.centery), (VENTANA.right, VENTANA.centery), 2)

    for x, lado in [(VENTANA.x - 10, 1), (VENTANA.right + 2, -1)]:
        pygame.draw.polygon(lienzo, (120, 70, 90), [(x, VENTANA.y - 8), (x + 10, VENTANA.y - 8),
                                                    (x + 10 - lado * 4, VENTANA.bottom + 14), (x - lado * 2, VENTANA.bottom + 14)])

    pygame.draw.line(lienzo, (90, 70, 60), (VENTANA.x - 14, VENTANA.y - 9), (VENTANA.right + 14, VENTANA.y - 9), 2)

    tablas_de_madera(lienzo, pygame.Rect(0, Y_PISO, ANCHO, ALTO - Y_PISO), (70, 54, 52), 8)


def dibujar_luz_de_luna(lienzo: pygame.Surface) -> None:

    """LA LUZ DE LA VENTANA CAE EN EL PISO COMO UN RECTANGULO CHUECO."""

    capa = pygame.Surface((ANCHO, ALTO), pygame.SRCALPHA)
    pygame.draw.polygon(capa, (170, 190, 240, 36), [(VENTANA.x, VENTANA.bottom), (VENTANA.right, VENTANA.bottom),
                                                    (VENTANA.right + 60, Y_PISO + 30), (VENTANA.x + 30, Y_PISO + 30)])
    lienzo.blit(capa, (0, 0))


def dibujar_cama(lienzo: pygame.Surface) -> None:

    """CAMA CON CABECERA DE BARROTES, COLCHA DE PARCHES Y ALMOHADA."""

    # CABECERA
    pygame.draw.rect(lienzo, (96, 70, 60), (618, 196, 8, Y_PISO - 196))
    pygame.draw.rect(lienzo, (96, 70, 60), (604, 196, 36, 6))

    for x in range(606, 640, 7):
        pygame.draw.line(lienzo, (80, 58, 50), (x, 202), (x, Y_PISO - 30), 2)

    # COLCHON Y COLCHA
    pygame.draw.rect(lienzo, (96, 70, 60), (528, Y_PISO - 20, 112, 20))                         # base de madera
    pygame.draw.rect(lienzo, (210, 200, 190), (530, Y_CAMA, 110, 12))                           # sabana

    colores = [(150, 80, 96), (90, 110, 150), (190, 150, 80), (110, 140, 100)]

    for i, x in enumerate(range(530, 640, 14)):
        for j, y in enumerate(range(Y_CAMA + 4, Y_PISO - 18, 10)):
            pygame.draw.rect(lienzo, colores[(i + j) % 4], (x, y, 14, 10))
            pygame.draw.rect(lienzo, mezclar(colores[(i + j) % 4], (0, 0, 0), 0.25), (x, y, 14, 10), 1)

    pygame.draw.polygon(lienzo, (150, 80, 96), [(530, Y_CAMA + 4), (524, Y_PISO - 14), (530, Y_PISO - 14)])  # cae la colcha

    # ALMOHADA
    pygame.draw.ellipse(lienzo, (230, 226, 216), (596, Y_CAMA - 8, 24, 14))
    pygame.draw.arc(lienzo, (190, 186, 176), (596, Y_CAMA - 8, 24, 14), 3.4, 6.0, 1)


def dibujar_buro(lienzo: pygame.Surface) -> None:

    """BURO CON EL TELEFONO ROJO DE DISCO (CON EL QUE LLAMO A LA POLICIA)."""

    pygame.draw.rect(lienzo, (96, 70, 60), BURO)
    pygame.draw.rect(lienzo, (70, 50, 44), BURO.inflate(-8, -12).move(0, 2), 1)
    pygame.draw.circle(lienzo, (190, 160, 100), (BURO.centerx, BURO.centery + 2), 1)
    pygame.draw.rect(lienzo, (120, 90, 76), (BURO.x - 2, BURO.y - 3, BURO.width + 4, 4))

    # TELEFONO
    x, y = BURO.centerx, BURO.y - 3
    pygame.draw.polygon(lienzo, (170, 40, 46), [(x - 9, y), (x + 9, y), (x + 6, y - 8), (x - 6, y - 8)])
    pygame.draw.circle(lienzo, (230, 220, 210), (x, y - 4), 3)
    pygame.draw.circle(lienzo, (170, 40, 46), (x, y - 4), 1)
    pygame.draw.rect(lienzo, (140, 30, 36), (x - 10, y - 12, 20, 4), border_radius=2)          # bocina colgada
    pygame.draw.rect(lienzo, COLOR_CONTORNO, (x - 11, y - 13, 22, 14), 1)

    # CABLE ENROSCADO QUE BAJA AL PISO
    for i in range(6):
        pygame.draw.circle(lienzo, (120, 30, 36), (BURO.right + 2, y + 6 + i * 5), 2, 1)


def dibujar_coraline(lienzo: pygame.Surface) -> None:

    """CORALINE EN PIJAMA, PARADA JUNTO A LA CAMA, PLATICANDO CON EL GATO."""

    sprite = pasillo_noche.sprite_pijama()

    sombra = pygame.Surface((sprite.get_width() + 6, 6), pygame.SRCALPHA)
    pygame.draw.ellipse(sombra, (0, 0, 0, 120), sombra.get_rect())
    lienzo.blit(sombra, (X_CORALINE - sombra.get_width() // 2, Y_PISO - 4))

    lienzo.blit(sprite, (X_CORALINE - sprite.get_width() // 2, Y_PISO - sprite.get_height()))


def dibujar_nube(lienzo: pygame.Surface) -> None:

    """NUBE DE PENSAMIENTO CON BOLITAS QUE SALEN DE LA CABEZA DE CORALINE."""

    capa = capa_vacia()

    for cx, cy, r in [(NUBE.x + 24, NUBE.y + 30, 22), (NUBE.x + 62, NUBE.y + 20, 26), (NUBE.x + 104, NUBE.y + 28, 24),
                      (NUBE.x + 116, NUBE.y + 62, 20), (NUBE.x + 84, NUBE.y + 80, 24), (NUBE.x + 40, NUBE.y + 80, 22),
                      (NUBE.x + 18, NUBE.y + 58, 18), (NUBE.centerx, NUBE.centery, 40)]:
        pygame.draw.circle(capa, COLOR_RECUERDO, (cx, cy), r)

    # BOLITAS HACIA LA CABEZA DE CORALINE
    for cx, cy, r in [(NUBE.x + 22, NUBE.bottom + 8, 6), (NUBE.x + 10, NUBE.bottom + 26, 4), (NUBE.x + 2, NUBE.bottom + 40, 3)]:
        pygame.draw.circle(capa, COLOR_RECUERDO, (cx, cy), r)

    pegar_con_contorno(lienzo, capa)


def dibujar_recuerdo_fijo(lienzo: pygame.Surface) -> None:

    """DENTRO DE LA NUBE, EN TONOS SEPIA: EL PASTO, UN ARBUSTO Y EL PAPA QUIETO.
    LAS AVISPAS Y LA CORALINE CHIQUITA SE MUEVEN Y VAN APARTE."""

    piso = ESCENA.bottom - 6
    sepia = (150, 120, 84)

    pygame.draw.line(lienzo, sepia, (ESCENA.x, piso), (ESCENA.right, piso), 2)

    for x in range(ESCENA.x + 2, ESCENA.right, 5):
        lienzo.set_at((x, piso - 1 - (x % 3)), sepia)

    # ARBUSTO DONDE ESTABA EL NIDO
    pygame.draw.ellipse(lienzo, (170, 150, 100), (ESCENA.right - 22, piso - 14, 22, 15))
    pygame.draw.ellipse(lienzo, (120, 96, 66), (ESCENA.right - 14, piso - 20, 8, 9))           # nido

    # EL PAPA, MUY DERECHITO Y QUIETO, CON LOS OJOS CERRADOS
    x = ESCENA.centerx + 10
    pygame.draw.rect(lienzo, (110, 100, 80), (x - 3, piso - 10, 2, 10))                        # piernas
    pygame.draw.rect(lienzo, (110, 100, 80), (x + 1, piso - 10, 2, 10))
    pygame.draw.rect(lienzo, (96, 120, 100), (x - 5, piso - 24, 10, 15), border_radius=2)       # sueter
    pygame.draw.rect(lienzo, (96, 120, 100), (x - 7, piso - 23, 2, 11))                         # brazos pegados
    pygame.draw.rect(lienzo, (96, 120, 100), (x + 5, piso - 23, 2, 11))
    pygame.draw.circle(lienzo, (220, 186, 150), (x, piso - 29), 5)                              # cabeza
    pygame.draw.arc(lienzo, (110, 80, 60), (x - 5, piso - 35, 10, 8), 0.2, 2.9, 2)              # pelo
    pygame.draw.line(lienzo, (80, 60, 50), (x - 3, piso - 29), (x - 1, piso - 29))              # ojos cerrados
    pygame.draw.line(lienzo, (80, 60, 50), (x + 1, piso - 29), (x + 3, piso - 29))


def crear_fijo() -> pygame.Surface:

    lienzo = pygame.Surface((ANCHO, ALTO))

    dibujar_cuarto(lienzo)
    dibujar_luz_de_luna(lienzo)
    dibujar_cama(lienzo)
    dibujar_buro(lienzo)
    dibujar_coraline(lienzo)

    brillo(lienzo, VENTANA.center, 70, (170, 190, 240), 45)
    orillas_oscuras(lienzo)

    # LA NUBE VA DESPUES DE LAS ORILLAS PARA QUE NO SE OSCUREZCA
    dibujar_nube(lienzo)
    dibujar_recuerdo_fijo(lienzo)

    return lienzo


# --------------------------------------------------
# LO QUE SE MUEVE
# --------------------------------------------------

def dibujar_avispas(lienzo: pygame.Surface, tiempo: float) -> None:

    """SIETE AVISPAS QUE DAN VUELTAS ALREDEDOR DEL PAPA DEL RECUERDO, A SACUDIDAS."""

    centro_x = ESCENA.centerx + 10
    centro_y = ESCENA.bottom - 24

    for i in range(7):

        angulo = tiempo * (2.4 + i * 0.3) + i * 0.9
        radio_x = 12 + (i % 3) * 4
        radio_y = 8 + (i % 2) * 5

        x = centro_x + int(math.cos(angulo) * radio_x + math.sin(tiempo * 23 + i) * 1.2)
        y = centro_y + int(math.sin(angulo) * radio_y + math.cos(tiempo * 19 + i) * 1.2)

        lienzo.set_at((x, y), (40, 30, 20))
        lienzo.set_at((x + 1, y), (220, 170, 40))
        lienzo.set_at((x + 2, y), (40, 30, 20))

        if int(tiempo * 12 + i) % 2 == 0:
            lienzo.set_at((x + 1, y - 1), (250, 250, 250))                                     # alitas


def dibujar_coraline_recuerdo(lienzo: pygame.Surface, tiempo: float) -> None:

    """LA CORALINE CHIQUITA DEL RECUERDO CORRE HACIA LA IZQUIERDA Y VUELVE A EMPEZAR."""

    piso = ESCENA.bottom - 6
    fase = (tiempo % 4) / 4

    x = int(ESCENA.centerx - 4 - fase * (ESCENA.width // 2 - 4))
    paso = int(tiempo * 10) % 2

    pygame.draw.circle(lienzo, (70, 80, 150), (x, piso - 13), 4)                               # pelo azul
    pygame.draw.circle(lienzo, (224, 190, 156), (x - 1, piso - 12), 2)                         # carita
    pygame.draw.rect(lienzo, (216, 176, 70), (x - 3, piso - 9, 6, 5))                          # impermeable
    pygame.draw.line(lienzo, (150, 110, 90), (x - 2, piso - 4), (x - 3 - paso * 2, piso - 1))   # piernitas
    pygame.draw.line(lienzo, (150, 110, 90), (x + 1, piso - 4), (x + 2 + paso * 2, piso - 1))


def dibujar_nube_luna(lienzo: pygame.Surface, tiempo: float) -> None:

    """UNA NUBE PASA FRENTE A LA LUNA CADA 12 SEGUNDOS."""

    fase = tiempo % 12

    if fase > 3:
        return

    x = int(-30 + fase / 3 * (VENTANA.width + 50))

    nube = pygame.Surface(VENTANA.size, pygame.SRCALPHA)
    pygame.draw.ellipse(nube, (30, 36, 64, 220), (x, 8, 32, 14))
    pygame.draw.ellipse(nube, (30, 36, 64, 220), (x + 10, 4, 28, 14))
    lienzo.blit(nube, VENTANA.topleft)

    # LA CRUZ DE LA VENTANA QUEDA ENCIMA DE LA NUBE
    pygame.draw.line(lienzo, (70, 60, 70), (VENTANA.centerx, VENTANA.y), (VENTANA.centerx, VENTANA.bottom), 2)
    pygame.draw.line(lienzo, (70, 60, 70), (VENTANA.x, VENTANA.centery), (VENTANA.right, VENTANA.centery), 2)


def dibujar(ventana: pygame.Surface) -> None:

    """DIBUJA LA ESCENA COMPLETA EN LA VENTANA DEL JUEGO."""

    if "fijo" not in CAPAS:
        CAPAS["fijo"] = crear_fijo()

    tiempo = pygame.time.get_ticks() / 1000

    lienzo = CAPAS["fijo"].copy()

    dibujar_nube_luna(lienzo, tiempo)
    personajes.dibujar_gato(lienzo, X_GATO, Y_CAMA + 4, False, tiempo)
    dibujar_coraline_recuerdo(lienzo, tiempo)
    dibujar_avispas(lienzo, tiempo)

    mostrar(ventana, lienzo)
