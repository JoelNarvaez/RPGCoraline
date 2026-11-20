"""FONDO DIBUJADO CON CODIGO: AFUERA, EL MUNDO ESTA GRIS Y VACIO.

Coraline sube del sotano y cierra la puerta. Afuera ya no queda casi nada del
jardin bonito del otro mundo: todo es gris, el pasto es una mancha lisa y los
arboles parecen recortes de papel que se doblan con el aire. Coraline se queda
sola en medio y se dice que es valiente: en su pecho late una lucecita calida,
lo unico con color en toda la escena. Se usa en cap09_n05 y en su rama
cap09_r05.

Lo que se mueve: los arboles de papel que se doblan, pedacitos grises que caen
como ceniza, la niebla y la lucecita de valor que crece y se encoge.
"""

import math

import pygame

from interfaz.fondos.pintura import ANCHO, ALTO
from interfaz.fondos.pintura import COLOR_CONTORNO
from interfaz.fondos.pintura import mezclar, degradado, orillas_oscuras, mostrar
from interfaz.fondos import personajes

Y_PISO = 300
X_CORALINE = 482
PECHO = (X_CORALINE + 2, Y_PISO - 50)

# ARBOLES DE PAPEL: (x, alto, que tan gris)
ARBOLES = [(424, 110, 0.2), (560, 128, 0.0), (612, 96, 0.4)]

CAPAS = {}


def crear_fijo() -> pygame.Surface:

    lienzo = pygame.Surface((ANCHO, ALTO))

    degradado(lienzo, pygame.Rect(0, 0, ANCHO, Y_PISO), (150, 150, 154), (196, 196, 198), 10)
    degradado(lienzo, pygame.Rect(0, Y_PISO - 10, ANCHO, ALTO - Y_PISO + 10), (128, 128, 130), (96, 96, 100), 4)

    # LA CASA A LO LEJOS, YA SOLO UNA SILUETA GRIS
    pygame.draw.rect(lienzo, (132, 130, 136), (300, 200, 90, Y_PISO - 200))
    pygame.draw.polygon(lienzo, (120, 118, 124), [(292, 202), (345, 168), (398, 202)])

    personajes.dibujar_coraline_chica(lienzo, X_CORALINE, Y_PISO, True)

    # TODO EN GRIS, INCLUSO CORALINE (LA LUCECITA DE VALOR SE DIBUJA APARTE, CON COLOR)
    lienzo = pygame.transform.grayscale(lienzo)
    orillas_oscuras(lienzo)

    return lienzo


# --------------------------------------------------
# LO QUE SE MUEVE
# --------------------------------------------------

def dibujar_arbol_de_papel(lienzo: pygame.Surface, x: int, alto: int, gris: float, tiempo: float) -> None:

    """UN ARBOL PLANO COMO RECORTE DE PAPEL: SE DOBLA HACIA UN LADO Y SE LE VE LA ORILLA BLANCA."""

    doblez = math.sin(tiempo * 1.3 + x) * 0.5 + 0.5             # 0 = derecho, 1 = doblado
    ancho = 40 - int(doblez * 22)                                 # al doblarse se ve mas angosto
    copa = pygame.Rect(x - ancho // 2, Y_PISO - alto, ancho, 54)

    color = mezclar((150, 150, 152), (190, 190, 192), gris)
    pygame.draw.rect(lienzo, color, (x - 2, copa.bottom - 6, 4, Y_PISO - copa.bottom + 6))
    pygame.draw.ellipse(lienzo, color, copa)
    pygame.draw.ellipse(lienzo, COLOR_CONTORNO, copa, 1)

    # LA ORILLA DEL PAPEL (BLANCA) SE VE CUANDO SE DOBLA
    if doblez > 0.3:
        pygame.draw.line(lienzo, (236, 236, 236), (copa.right, copa.y + 8), (copa.right, copa.bottom - 8), 2)


def dibujar_ceniza(lienzo: pygame.Surface, tiempo: float) -> None:

    """PEDACITOS GRISES QUE CAEN DESPACIO, COMO SI EL MUNDO SE ESTUVIERA DESHACIENDO."""

    for i in range(20):
        x = 400 + (i * 37) % 240 + int(math.sin(tiempo + i) * 6)
        y = int((tiempo * 14 + i * 29) % 300)
        pygame.draw.rect(lienzo, (210, 210, 212) if i % 2 else (110, 110, 114), (x, y, 2, 1))


def dibujar_valor(lienzo: pygame.Surface, tiempo: float) -> None:

    """LA LUCECITA CALIDA EN SU PECHO: LATE, Y CADA TANTO CRECE COMO SI SE CONVENCIERA DE QUE ES VALIENTE."""

    convencida = (math.sin(tiempo * 0.6) + 1) / 2
    late = (math.sin(tiempo * 5) + 1) / 2
    radio = 4 + int(convencida * 10 + late * 2)

    # LA LUZ SE SUMA A LO QUE HAY DEBAJO (BLEND_ADD): ASI ILUMINA EN VEZ DE MANCHAR DE CAFE
    capa = pygame.Surface((80, 80))
    pygame.draw.circle(capa, (40, 26, 6), (40, 40), radio + 10)
    pygame.draw.circle(capa, (90, 60, 16), (40, 40), radio)
    pygame.draw.circle(capa, (150, 110, 50), (40, 40), radio // 2 + 1)
    lienzo.blit(capa, (PECHO[0] - 40, PECHO[1] - 40), special_flags=pygame.BLEND_ADD)
    pygame.draw.circle(lienzo, (255, 236, 170), PECHO, 1 + int(late * 2))

    # CHISPITAS QUE SALEN CUANDO ESTA MAS CONVENCIDA
    if convencida > 0.6:
        for i in range(4):
            angulo = i * 1.57 + tiempo * 2
            distancia = radio + 4 + int(late * 4)
            lienzo.set_at((PECHO[0] + int(math.cos(angulo) * distancia), PECHO[1] + int(math.sin(angulo) * distancia)),
                          (255, 220, 140))


def dibujar(ventana: pygame.Surface) -> None:

    """DIBUJA LA ESCENA COMPLETA EN LA VENTANA DEL JUEGO."""

    if "fijo" not in CAPAS:
        CAPAS["fijo"] = crear_fijo()

    tiempo = pygame.time.get_ticks() / 1000

    lienzo = CAPAS["fijo"].copy()

    for x, alto, gris in ARBOLES:
        dibujar_arbol_de_papel(lienzo, x, alto, gris, tiempo)

    dibujar_ceniza(lienzo, tiempo)
    dibujar_valor(lienzo, tiempo)

    mostrar(ventana, lienzo)
