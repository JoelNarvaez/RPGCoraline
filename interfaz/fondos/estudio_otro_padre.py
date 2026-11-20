"""FONDO DIBUJADO CON CODIGO: EL OTRO PADRE SENTADO EN SU ESTUDIO SIN HACER NADA.

Al volver a la casa, Coraline se asoma al estudio. El otro padre esta sentado
detras de un escritorio vacio, con los brazos colgando y sin sonreir. Los
libros del librero no tienen titulo y por la ventana solo se ve blanco (afuera
no hay nada, como en fin_del_mundo.py). Le susurra que no puede platicar con
ella cuando la otra madre no esta. Se usa en cap06_n03 y en su rama cap06_r03.

Lo que se mueve: la lamparita que titila, el brillo de los botones, el
susurro en una burbujita y motitas de polvo.
"""

import math

import pygame

from interfaz.fondos.pintura import ANCHO, ALTO
from interfaz.fondos.pintura import capa_vacia, pegar_con_contorno, COLOR_CONTORNO
from interfaz.fondos.pintura import mezclar, degradado, brillo, orillas_oscuras, mostrar
from interfaz.fondos.pintura import tablas_de_madera
from interfaz.fondos import personajes
from interfaz.fondos import sala_actrices

Y_PISO = 300

X_CORALINE = 452
X_PADRE = 584
ESCRITORIO = pygame.Rect(520, 222, 120, Y_PISO - 222)
VENTANA = pygame.Rect(552, 62, 66, 70)
LIBRERO = pygame.Rect(406, 96, 56, Y_PISO - 96)
LAMPARA = (628, 204)

COLOR_PARED = (110, 104, 74)
COLOR_MADERA = (96, 62, 44)
COLOR_MADERA_LUZ = (130, 88, 60)

CAPAS = {}


# --------------------------------------------------
# PARTE FIJA
# --------------------------------------------------

def dibujar_cuarto(lienzo: pygame.Surface) -> None:

    """PARED VERDE MOSTAZA APAGADA, LAMBRIN, PISO DE TABLAS Y LA VENTANA QUE SOLO MUESTRA BLANCO."""

    degradado(lienzo, pygame.Rect(0, 0, ANCHO, Y_PISO), (60, 58, 46), COLOR_PARED, 12)

    for x in range(0, ANCHO, 16):
        pygame.draw.line(lienzo, mezclar(COLOR_PARED, (0, 0, 0), 0.1), (x, 0), (x, 230))

    pygame.draw.rect(lienzo, (70, 52, 40), (0, 230, ANCHO, Y_PISO - 230))
    pygame.draw.rect(lienzo, COLOR_MADERA_LUZ, (0, 228, ANCHO, 3))

    tablas_de_madera(lienzo, pygame.Rect(0, Y_PISO, ANCHO, ALTO - Y_PISO), (84, 58, 44), 8)

    # VENTANA: AFUERA NO HAY NADA, SOLO BLANCO
    pygame.draw.rect(lienzo, COLOR_MADERA, VENTANA.inflate(8, 8))
    degradado(lienzo, VENTANA, (236, 236, 232), (218, 220, 216), 4)
    pygame.draw.line(lienzo, COLOR_MADERA, (VENTANA.centerx, VENTANA.y), (VENTANA.centerx, VENTANA.bottom), 3)
    pygame.draw.line(lienzo, COLOR_MADERA, (VENTANA.x, VENTANA.centery), (VENTANA.right, VENTANA.centery), 3)


def dibujar_librero(capa: pygame.Surface) -> None:

    """LIBRERO CON LIBROS DE COLORES APAGADOS Y LOMOS SIN TITULO."""

    pygame.draw.rect(capa, COLOR_MADERA, LIBRERO)
    pygame.draw.rect(capa, (50, 34, 28), LIBRERO.inflate(-8, -8))

    colores = [(120, 70, 60), (70, 90, 110), (110, 104, 70), (90, 70, 96), (130, 120, 100)]

    for fila in range(4):
        y = LIBRERO.y + 6 + fila * 48
        pygame.draw.rect(capa, COLOR_MADERA_LUZ, (LIBRERO.x + 4, y + 40, LIBRERO.width - 8, 4))

        x = LIBRERO.x + 6
        i = fila

        while x < LIBRERO.right - 10:
            ancho = 4 + (i * 3) % 4
            alto = 28 + (i * 7) % 10
            pygame.draw.rect(capa, colores[i % len(colores)], (x, y + 40 - alto, ancho, alto))
            pygame.draw.line(capa, mezclar(colores[i % len(colores)], (0, 0, 0), 0.3), (x, y + 40 - alto), (x, y + 39))
            x = x + ancho + 1
            i = i + 1


def dibujar_silla(capa: pygame.Surface) -> None:

    """RESPALDO ALTO DE LA SILLA, QUE SE VE DETRAS DEL OTRO PADRE."""

    pygame.draw.rect(capa, (70, 40, 34), (X_PADRE - 24, 156, 48, 70), border_radius=6)
    pygame.draw.rect(capa, (110, 56, 46), (X_PADRE - 18, 162, 36, 58), border_radius=4)


def dibujar_escritorio(capa: pygame.Surface) -> None:

    """ESCRITORIO VACIO: NI PAPELES, NI PLUMAS, SOLO UNA LAMPARITA."""

    pygame.draw.rect(capa, COLOR_MADERA_LUZ, (ESCRITORIO.x - 4, ESCRITORIO.y, ESCRITORIO.width + 4, 6))
    pygame.draw.rect(capa, COLOR_MADERA, (ESCRITORIO.x, ESCRITORIO.y + 6, ESCRITORIO.width, ESCRITORIO.height - 6))

    for y in [236, 262]:
        pygame.draw.rect(capa, mezclar(COLOR_MADERA, (0, 0, 0), 0.25), (ESCRITORIO.x + 8, y, 40, 20), 1)
        pygame.draw.rect(capa, (200, 170, 90), (ESCRITORIO.x + 26, y + 9, 4, 2))

    # LAMPARITA DE PANTALLA VERDE
    pygame.draw.rect(capa, (60, 50, 40), (LAMPARA[0] - 1, LAMPARA[1], 2, ESCRITORIO.y - LAMPARA[1]))
    pygame.draw.rect(capa, (60, 50, 40), (LAMPARA[0] - 5, ESCRITORIO.y - 2, 10, 2))
    pygame.draw.polygon(capa, (50, 110, 80), [(LAMPARA[0] - 9, LAMPARA[1]), (LAMPARA[0] + 3, LAMPARA[1]),
                                             (LAMPARA[0] + 1, LAMPARA[1] - 7), (LAMPARA[0] - 7, LAMPARA[1] - 7)])


def crear_fijo() -> pygame.Surface:

    lienzo = pygame.Surface((ANCHO, ALTO))

    dibujar_cuarto(lienzo)

    capa = capa_vacia()
    dibujar_librero(capa)
    pegar_con_contorno(lienzo, capa)

    # SILLA, OTRO PADRE Y ESCRITORIO ENCIMA (ASI SOLO SE VE DE LA CINTURA PARA ARRIBA)
    capa = capa_vacia()
    dibujar_silla(capa)
    personajes.dibujar_otro_padre(capa, X_PADRE, "quieto")
    dibujar_escritorio(capa)
    pegar_con_contorno(lienzo, capa)

    sala_actrices.dibujar_coraline(lienzo, X_CORALINE, True)

    brillo(lienzo, VENTANA.center, 90, (240, 240, 236), 40)
    orillas_oscuras(lienzo)

    return lienzo


# --------------------------------------------------
# LO QUE SE MUEVE
# --------------------------------------------------

def dibujar_lampara(lienzo: pygame.Surface, tiempo: float) -> None:

    """EL FOCO DE LA LAMPARITA TITILA, COMO SI LE FALTARA FUERZA."""

    falla = math.sin(tiempo * 13) + math.sin(tiempo * 5.3) > 1.3

    if falla:
        return

    capa = pygame.Surface((40, 30), pygame.SRCALPHA)
    pygame.draw.polygon(capa, (255, 230, 150, 50), [(16, 0), (24, 0), (40, 30), (0, 30)])
    lienzo.blit(capa, (LAMPARA[0] - 23, LAMPARA[1] - 8))
    pygame.draw.rect(lienzo, (255, 236, 170), (LAMPARA[0] - 4, LAMPARA[1], 4, 2))


def dibujar_susurro(lienzo: pygame.Surface, tiempo: float) -> None:

    """BURBUJITA CHICA JUNTO A SU BOCA: SUSURRA (TRES PUNTITOS QUE SALEN UNO A UNO)."""

    fase = tiempo % 5

    if fase > 3:
        return

    x, y = X_PADRE - 50, 118

    pygame.draw.ellipse(lienzo, COLOR_CONTORNO, (x - 1, y - 1, 26, 14))
    pygame.draw.ellipse(lienzo, (236, 230, 220), (x, y, 24, 12))
    pygame.draw.polygon(lienzo, (236, 230, 220), [(x + 18, y + 9), (x + 22, y + 9), (x + 28, y + 18)])
    pygame.draw.line(lienzo, COLOR_CONTORNO, (x + 28, y + 18), (x + 22, y + 10))

    for i in range(min(int(fase / 0.5), 3)):
        pygame.draw.rect(lienzo, (70, 60, 50), (x + 6 + i * 5, y + 5, 2, 2))


def dibujar_polvo(lienzo: pygame.Surface, tiempo: float) -> None:

    """MOTITAS DE POLVO EN LA LUZ BLANCA DE LA VENTANA."""

    for i in range(10):

        x = VENTANA.x - 20 + (i * 19 + int(tiempo * 2)) % 100
        y = VENTANA.bottom + 4 + (i * 13) % 70 + int(math.sin(tiempo * 0.7 + i) * 5)

        lienzo.set_at((x, y), (220, 220, 210))


def dibujar(ventana: pygame.Surface) -> None:

    """DIBUJA LA ESCENA COMPLETA EN LA VENTANA DEL JUEGO."""

    if "fijo" not in CAPAS:
        CAPAS["fijo"] = crear_fijo()

    tiempo = pygame.time.get_ticks() / 1000

    lienzo = CAPAS["fijo"].copy()

    dibujar_polvo(lienzo, tiempo)
    dibujar_lampara(lienzo, tiempo)
    personajes.dibujar_botones(lienzo, personajes.ojos_otro_padre(X_PADRE), tiempo, True)
    dibujar_susurro(lienzo, tiempo)

    mostrar(ventana, lienzo)
