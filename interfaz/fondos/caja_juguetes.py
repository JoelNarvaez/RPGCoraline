"""FONDO DIBUJADO CON CODIGO: CORALINE VOLTEA LA CAJA DE JUGUETES.

El otro cuarto de otro_cuarto.py (cap03_n05), pero con el baul de juguetes
volteado de lado y todo regado sobre el tapete: cubos, soldaditos, una
pelota, un trompo y muchas canicas. Coraline esta junto a la caja con la
piedra con agujero colgando de su cordon. Una de las canicas guarda un alma,
pero a simple vista todas se ven iguales. Se usa en la pantalla de antes del
minijuego cap08_m01.

vista_piedra.py (cap08_n03) usa estos mismos juguetes regados
(dibujar_juguetes_regados, CANICAS y BRASA).

Lo que se mueve: canicas que siguen saliendo rodando de la caja, la piedra
que se mece colgada de su cordon, las ratas y el dinosaurio de cuerda.
"""

import math

import pygame

from interfaz.fondos.pintura import ANCHO, ALTO
from interfaz.fondos.pintura import capa_vacia, pegar_con_contorno, COLOR_CONTORNO
from interfaz.fondos.pintura import brillo, orillas_oscuras, mostrar
from interfaz.fondos import sala_actrices
from interfaz.fondos import otro_cuarto
from interfaz.fondos import piedra

Y_PISO = otro_cuarto.Y_PISO

X_CORALINE = 446
MANO = (X_CORALINE + 11, Y_PISO - 40)          # la mano de adelante, de donde cuelga el cordon
LARGO_CORDON = 16

CAJA = pygame.Rect(480, 276, 50, 26)           # el baul acostado, con la boca hacia la derecha
BOCA = (CAJA.right + 2, CAJA.bottom - 6)       # por aqui salen rodando las canicas

BRASA = (548, 322)                             # la canica que guarda un alma (gris)
CANICAS = [(470, 312), (496, 326), (512, 306), (586, 314), (566, 334), (524, 338), (602, 328)]
COLORES_CANICA = [(110, 170, 230), (230, 120, 160), (240, 200, 80), (120, 200, 140),
                  (200, 140, 230), (90, 200, 210), (240, 150, 90)]

CAPAS = {}


# --------------------------------------------------
# PARTE FIJA (TAMBIEN LA USA vista_piedra.py)
# --------------------------------------------------

def dibujar_canica(lienzo: pygame.Surface, x: int, y: int, color: tuple) -> None:

    """CANICA DE VIDRIO CON SU REMOLINO Y UN BRILLITO."""

    pygame.draw.circle(lienzo, COLOR_CONTORNO, (x, y), 4)
    pygame.draw.circle(lienzo, (226, 232, 240), (x, y), 3)
    pygame.draw.line(lienzo, color, (x - 2, y + 1), (x + 2, y - 1), 2)
    lienzo.set_at((x - 1, y - 2), (255, 255, 255))


def dibujar_caja_volteada(capa: pygame.Surface) -> None:

    """EL BAUL ACOSTADO: SE VE EL FONDO OSCURO POR LA BOCA Y LA TAPA ABIERTA EN EL PISO."""

    pygame.draw.rect(capa, (150, 70, 50), CAJA)
    pygame.draw.rect(capa, (60, 28, 22), (CAJA.right - 12, CAJA.y + 3, 10, CAJA.height - 6))      # la boca
    pygame.draw.rect(capa, (230, 190, 70), (CAJA.x + 14, CAJA.y + 10, 6, 6))                      # chapa
    pygame.draw.line(capa, (110, 50, 36), (CAJA.x, CAJA.centery), (CAJA.right - 12, CAJA.centery))
    pygame.draw.polygon(capa, (170, 84, 60), [(CAJA.right, CAJA.y), (CAJA.right + 18, CAJA.y + 12),
                                              (CAJA.right + 18, CAJA.bottom + 2), (CAJA.right, CAJA.bottom)])


def dibujar_juguetes_regados(lienzo: pygame.Surface) -> None:

    """CUBOS, SOLDADITOS, PELOTA, TROMPO Y CANICAS REGADOS SOBRE EL TAPETE."""

    for x, y, color in [(482, 334, (240, 200, 60)), (494, 338, (80, 170, 90)), (576, 302, (220, 90, 140))]:
        pygame.draw.rect(lienzo, color, (x, y - 8, 8, 8))
        pygame.draw.rect(lienzo, COLOR_CONTORNO, (x, y - 8, 8, 8), 1)

    for x, y in [(530, 312), (538, 330), (610, 320)]:
        pygame.draw.rect(lienzo, (200, 40, 40), (x, y - 2, 9, 3))
        pygame.draw.rect(lienzo, (30, 30, 50), (x - 3, y - 2, 3, 3))

    pygame.draw.circle(lienzo, (220, 60, 60), (452, 330), 7)
    pygame.draw.line(lienzo, (250, 250, 250), (446, 330), (458, 330), 2)
    pygame.draw.polygon(lienzo, (90, 130, 210), [(616, 302), (628, 302), (622, 312)])

    for i in range(len(CANICAS)):
        x, y = CANICAS[i]
        dibujar_canica(lienzo, x, y, COLORES_CANICA[i])

    # LA CANICA DEL ALMA: GRIS Y ABURRIDA
    pygame.draw.circle(lienzo, COLOR_CONTORNO, BRASA, 4)
    pygame.draw.circle(lienzo, (140, 140, 146), BRASA, 3)
    lienzo.set_at((BRASA[0] - 1, BRASA[1] - 1), (176, 176, 182))


def crear_fijo() -> pygame.Surface:

    lienzo = pygame.Surface((ANCHO, ALTO))

    otro_cuarto.dibujar_cuarto(lienzo, False)
    dibujar_juguetes_regados(lienzo)

    capa = capa_vacia()
    dibujar_caja_volteada(capa)
    pegar_con_contorno(lienzo, capa)

    sala_actrices.dibujar_coraline(lienzo, X_CORALINE, True)

    brillo(lienzo, otro_cuarto.PUERTA.center, 110, (255, 210, 150), 40)
    orillas_oscuras(lienzo)

    return lienzo


# --------------------------------------------------
# LO QUE SE MUEVE
# --------------------------------------------------

def dibujar_canicas_rodando(lienzo: pygame.Surface, tiempo: float) -> None:

    """TRES CANICAS SALEN DE LA BOCA DE LA CAJA, RODANDO Y DANDO BRINQUITOS CADA VEZ MAS CHICOS."""

    for i in range(3):

        fase = (tiempo * 0.35 + i / 3) % 1
        x = BOCA[0] + int(fase * (90 + i * 12))
        rebote = abs(math.sin(fase * math.pi * 4)) * (1 - fase) * 6
        y = BOCA[1] + int(fase * (14 + i * 10)) - int(rebote)

        dibujar_canica(lienzo, x, y, COLORES_CANICA[(i * 2) % len(COLORES_CANICA)])


def dibujar_piedra_colgando(lienzo: pygame.Surface, tiempo: float) -> None:

    """LA PIEDRA CUELGA DE SU CORDON DESDE LA MANO DE CORALINE Y SE MECE COMO PENDULO."""

    angulo = math.sin(tiempo * 2.2) * 0.4
    x = MANO[0] + int(math.sin(angulo) * LARGO_CORDON)
    y = MANO[1] + int(math.cos(angulo) * LARGO_CORDON)

    pygame.draw.line(lienzo, piedra.COLOR_CORDON, MANO, (x, y - 3))
    piedra.dibujar_piedra(lienzo, x, y + 2, 2, 3, 0)


def dibujar(ventana: pygame.Surface) -> None:

    """DIBUJA LA ESCENA COMPLETA EN LA VENTANA DEL JUEGO."""

    if "fijo" not in CAPAS:
        CAPAS["fijo"] = crear_fijo()

    tiempo = pygame.time.get_ticks() / 1000

    lienzo = CAPAS["fijo"].copy()

    otro_cuarto.dibujar_ratas(lienzo, tiempo)
    otro_cuarto.dibujar_dinosaurio(lienzo, tiempo)
    dibujar_canicas_rodando(lienzo, tiempo)
    dibujar_piedra_colgando(lienzo, tiempo)

    mostrar(ventana, lienzo)
