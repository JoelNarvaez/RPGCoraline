"""FONDO DIBUJADO CON CODIGO: LA OTRA MADRE RECIBE A CORALINE CON LOS BRAZOS ABIERTOS.

Coraline abre la puerta con la llave negra y cruza otra vez. Del otro lado
la espera la otra madre, con los brazos abiertos y su sonrisa de botones.
Coraline trae la llave negra en la mano. El gato, sentado en un rincon junto
a la puerta por donde entro, le susurra que la desafie. Es la misma entrada
lila del otro departamento de despedida_otros.py (cap03_n06), pero ahora la
puerta da al pasillo oscuro y frio por el que llego. Se usa en cap05_n06 y
en su rama cap05_r05.

Lo que se mueve: los botones de la otra madre brillan, sus dedos tamborilean,
el aire frio sale del pasillo, el gato parpadea y su susurro aparece en una
burbujita.
"""

import math

import pygame

from interfaz.fondos.pintura import ANCHO, ALTO
from interfaz.fondos.pintura import capa_vacia, pegar_con_contorno, COLOR_CONTORNO
from interfaz.fondos.pintura import degradado, brillo, orillas_oscuras, mostrar
from interfaz.fondos import personajes
from interfaz.fondos import despedida_otros
from interfaz.fondos import sala_actrices

Y_PISO = despedida_otros.Y_PISO
PUERTA = despedida_otros.PUERTA

X_GATO = PUERTA.x - 4             # en el rincon, junto a la puerta
X_CORALINE = 484
X_MADRE = 576

CAPAS = {}


# --------------------------------------------------
# PARTE FIJA
# --------------------------------------------------

def dibujar_pasillo_oscuro(lienzo: pygame.Surface) -> None:

    """LA PUERTA YA NO DA AL JARDIN: SE VE EL PASILLO FRIO CON UNA LUZ AL FONDO."""

    degradado(lienzo, PUERTA, (10, 14, 22), (26, 40, 46), 6)

    # PAREDES DEL PASILLO QUE SE PIERDEN A LO LEJOS
    centro = (PUERTA.centerx, PUERTA.centery + 10)
    pygame.draw.polygon(lienzo, (20, 34, 38), [PUERTA.topleft, (centro[0] - 6, centro[1] - 14),
                                               (centro[0] - 6, centro[1] + 14), PUERTA.bottomleft])
    pygame.draw.polygon(lienzo, (14, 24, 28), [PUERTA.topright, (centro[0] + 6, centro[1] - 14),
                                               (centro[0] + 6, centro[1] + 14), PUERTA.bottomright])

    # LUCECITA DEL OTRO LADO (LA CASA DE VERDAD)
    pygame.draw.rect(lienzo, (200, 190, 140), (centro[0] - 3, centro[1] - 5, 6, 9))


def dibujar_llave(lienzo: pygame.Surface) -> None:

    """LA LLAVE NEGRA EN LA MANO DE ADELANTE DE CORALINE."""

    x, y = X_CORALINE + 13, Y_PISO - 30

    pygame.draw.circle(lienzo, (16, 14, 18), (x, y - 3), 3)
    pygame.draw.circle(lienzo, (150, 110, 150), (x, y - 3), 1)
    pygame.draw.rect(lienzo, (16, 14, 18), (x - 1, y, 2, 12))
    pygame.draw.rect(lienzo, (16, 14, 18), (x + 1, y + 8, 3, 2))
    pygame.draw.rect(lienzo, (16, 14, 18), (x + 1, y + 11, 2, 1))


def crear_fijo() -> pygame.Surface:

    lienzo = pygame.Surface((ANCHO, ALTO))

    despedida_otros.dibujar_entrada(lienzo)
    dibujar_pasillo_oscuro(lienzo)

    # LA OTRA MADRE CON LOS BRAZOS ABIERTOS (CONTORNO COMO SPRITE DE RPG)
    capa = capa_vacia()
    personajes.dibujar_otra_madre(capa, X_MADRE, "brazos_abiertos")
    pegar_con_contorno(lienzo, capa)

    sala_actrices.dibujar_coraline(lienzo, X_CORALINE, True)
    dibujar_llave(lienzo)

    brillo(lienzo, (X_MADRE, 200), 120, (255, 200, 150), 40)
    orillas_oscuras(lienzo)

    return lienzo


# --------------------------------------------------
# LO QUE SE MUEVE
# --------------------------------------------------

def dibujar_aire_frio(lienzo: pygame.Surface, tiempo: float) -> None:

    """HILOS DE AIRE FRIO QUE SALEN DEL PASILLO A RAS DEL PISO."""

    capa = pygame.Surface((ANCHO, ALTO), pygame.SRCALPHA)

    for i in range(4):

        fase = (tiempo * 0.35 + i / 4) % 1
        x = PUERTA.centerx + int(fase * 90)
        y = Y_PISO - 6 - i * 5 + int(math.sin(tiempo * 2 + i) * 2)
        alfa = int(70 * (1 - fase))

        pygame.draw.line(capa, (190, 220, 230, alfa), (x - 10, y), (x + 8, y - 1))

    lienzo.blit(capa, (0, 0))


def dibujar_dedos(lienzo: pygame.Surface, tiempo: float) -> None:

    """LOS DEDOS LARGOS DE LA OTRA MADRE TAMBORILEAN EN EL AIRE, IMPACIENTES."""

    for lado in [-1, 1]:

        mano = (X_MADRE + lado * 38, 182)

        for i in range(3):
            sube = int((math.sin(tiempo * 9 + i * 1.3 + lado) + 1) * 1.2)
            punta = (mano[0] + lado * 7, mano[1] - 5 + i * 2 - sube)
            pygame.draw.line(lienzo, personajes.OTRA_PIEL, (mano[0] + lado * 2, mano[1] - 2 + i * 2), punta)


def dibujar_susurro(lienzo: pygame.Surface, tiempo: float) -> None:

    """BURBUJITA DEL GATO CON TRES PUNTITOS QUE APARECEN UNO A UNO (LE SUSURRA)."""

    fase = tiempo % 6

    if fase > 3.5:
        return

    x, y = X_GATO + 8, Y_PISO - 104

    pygame.draw.ellipse(lienzo, COLOR_CONTORNO, (x - 1, y - 1, 26, 14))
    pygame.draw.ellipse(lienzo, (236, 230, 240), (x, y, 24, 12))
    pygame.draw.polygon(lienzo, (236, 230, 240), [(x + 4, y + 9), (x + 9, y + 10), (x + 2, y + 16)])
    pygame.draw.line(lienzo, COLOR_CONTORNO, (x + 2, y + 16), (x + 4, y + 10))

    for i in range(min(int(fase / 0.5), 3)):
        pygame.draw.rect(lienzo, (60, 50, 70), (x + 6 + i * 5, y + 5, 2, 2))


def dibujar(ventana: pygame.Surface) -> None:

    """DIBUJA LA ESCENA COMPLETA EN LA VENTANA DEL JUEGO."""

    if "fijo" not in CAPAS:
        CAPAS["fijo"] = crear_fijo()

    tiempo = pygame.time.get_ticks() / 1000

    lienzo = CAPAS["fijo"].copy()

    dibujar_aire_frio(lienzo, tiempo)
    dibujar_dedos(lienzo, tiempo)
    personajes.dibujar_botones(lienzo, personajes.ojos_otra_madre(X_MADRE), tiempo, False, True)
    personajes.dibujar_gato(lienzo, X_GATO, Y_PISO + 2, True, tiempo)
    dibujar_susurro(lienzo, tiempo)

    mostrar(ventana, lienzo)
