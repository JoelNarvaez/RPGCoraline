"""FONDO DIBUJADO CON CODIGO: DETRAS DE LA CASA, EL MUNDO SE ACABA.

Coraline y el gato salen por atras de la casa rosa. Al principio el jardin
es normal, pero mientras mas se alejan los arboles se ven como dibujos a
medio hacer: primero sin color, despues unas cuantas rayas y al final nada.
Mas alla solo hay una blancura sin forma. Coraline camina con el gato, que va
adelante. Se usa en cap06_n02 y en su rama cap06_r02.

Lo que se mueve: motitas de pasto que se deshacen en la orilla blanca, la
blancura que "respira" y el gato que parpadea.
"""

import math

import pygame

from interfaz.fondos.pintura import ANCHO, ALTO
from interfaz.fondos.pintura import capa_vacia, pegar_con_contorno
from interfaz.fondos.pintura import mezclar, degradado, brillo, orillas_oscuras, mostrar
from interfaz.fondos import personajes
from interfaz.fondos import sala_actrices

Y_PISO = 300

X_CORALINE = 456
X_GATO = 506

INICIO_BLANCO = 360           # desde aqui el mundo empieza a borrarse
COLOR_BLANCO = (238, 238, 234)
COLOR_PASTO = (92, 140, 84)
COLOR_CASA = (226, 150, 170)

CAPAS = {}


# --------------------------------------------------
# PARTE FIJA
# --------------------------------------------------

def dibujar_cielo_y_pasto(lienzo: pygame.Surface) -> None:

    """CIELO DE DIA MEDIO GRIS Y PASTO CON FLORECITAS (EN LA PARTE QUE TODAVIA EXISTE)."""

    degradado(lienzo, pygame.Rect(0, 0, ANCHO, Y_PISO), (150, 176, 206), (214, 222, 226), 12)
    degradado(lienzo, pygame.Rect(0, Y_PISO - 14, ANCHO, ALTO - Y_PISO + 14), COLOR_PASTO, (62, 100, 60), 5)

    for i in range(70):
        x = (i * 37) % 420
        y = Y_PISO - 10 + (i * 13) % 60
        pygame.draw.line(lienzo, (120, 170, 100), (x, y), (x + 1, y - 3))

        if i % 7 == 0:
            pygame.draw.rect(lienzo, [(240, 220, 90), (236, 130, 160), (250, 250, 240)][i % 3], (x + 3, y - 2, 2, 2))


def dibujar_casa(capa: pygame.Surface) -> None:

    """LA PARTE DE ATRAS DE LA CASA ROSA, CORTADA POR LA ORILLA IZQUIERDA."""

    pygame.draw.rect(capa, COLOR_CASA, (0, 150, 120, Y_PISO - 136))
    pygame.draw.rect(capa, mezclar(COLOR_CASA, (0, 0, 0), 0.2), (108, 150, 12, Y_PISO - 136))
    pygame.draw.polygon(capa, (120, 60, 56), [(0, 120), (90, 120), (130, 152), (0, 152)])

    # PUERTA DE ATRAS Y UNA VENTANA
    pygame.draw.rect(capa, (150, 60, 90), (54, 236, 28, Y_PISO - 222))
    pygame.draw.circle(capa, (240, 200, 80), (76, 262), 2)
    pygame.draw.rect(capa, (100, 90, 110), (12, 184, 26, 30))
    pygame.draw.line(capa, (210, 220, 230), (25, 184), (25, 214))


def dibujar_arbol(lienzo: pygame.Surface, x: int, alto: int, que_tanto: float) -> None:

    """UN ARBOL QUE SE VA BORRANDO: que_tanto 0 = NORMAL, 0.5 = SOLO CONTORNO, 1 = UNAS RAYITAS."""

    copa = pygame.Rect(x - 26, Y_PISO - alto, 52, 50)

    if que_tanto < 0.4:
        pygame.draw.rect(lienzo, (96, 70, 52), (x - 4, copa.bottom - 10, 8, Y_PISO - copa.bottom + 10))
        pygame.draw.ellipse(lienzo, (64, 112, 70), copa)
        pygame.draw.ellipse(lienzo, (84, 136, 84), copa.inflate(-16, -18).move(-4, -6))
        return

    gris = mezclar((120, 126, 120), COLOR_BLANCO, (que_tanto - 0.4) * 1.2)

    if que_tanto < 0.8:
        # COMO DIBUJO A LAPIZ: SOLO LA ORILLA Y EL TRONCO
        pygame.draw.ellipse(lienzo, gris, copa, 1)
        pygame.draw.line(lienzo, gris, (x - 3, copa.bottom - 2), (x - 3, Y_PISO))
        pygame.draw.line(lienzo, gris, (x + 3, copa.bottom - 2), (x + 3, Y_PISO))
        return

    # CASI NADA: TRES RAYAS SUELTAS
    pygame.draw.arc(lienzo, gris, copa, 0.6, 2.2, 1)
    pygame.draw.line(lienzo, gris, (x, copa.bottom + 6), (x, copa.bottom + 22))


def borrar_el_mundo(lienzo: pygame.Surface) -> None:

    """TAPA TODO CON BLANCO, CADA VEZ MAS FUERTE HACIA LA DERECHA (NO HAY HORIZONTE)."""

    capa = pygame.Surface((ANCHO, ALTO), pygame.SRCALPHA)

    for x in range(INICIO_BLANCO, ANCHO):
        avance = min((x - INICIO_BLANCO) / 190, 1)
        pygame.draw.line(capa, (*COLOR_BLANCO, int(255 * avance ** 0.8)), (x, 0), (x, ALTO))

    lienzo.blit(capa, (0, 0))


def crear_fijo() -> pygame.Surface:

    lienzo = pygame.Surface((ANCHO, ALTO))

    dibujar_cielo_y_pasto(lienzo)

    capa = capa_vacia()
    dibujar_casa(capa)
    pegar_con_contorno(lienzo, capa)

    capa = capa_vacia()
    dibujar_arbol(capa, 180, 118, 0)
    dibujar_arbol(capa, 300, 104, 0.2)
    pegar_con_contorno(lienzo, capa)

    borrar_el_mundo(lienzo)

    # LOS ARBOLES DE MAS LEJOS YA SON SOLO DIBUJOS, ENCIMA DE LA BLANCURA
    dibujar_arbol(lienzo, 410, 110, 0.5)
    dibujar_arbol(lienzo, 560, 96, 0.9)

    # CORALINE VA DETRAS DEL GATO, YA METIDA EN LA BLANCURA
    sala_actrices.dibujar_coraline(lienzo, X_CORALINE, True)

    brillo(lienzo, (600, 180), 140, (255, 255, 255), 70)
    orillas_oscuras(lienzo)

    return lienzo


# --------------------------------------------------
# LO QUE SE MUEVE
# --------------------------------------------------

def dibujar_respiro(lienzo: pygame.Surface, tiempo: float) -> None:

    """LA BLANCURA AVANZA Y SE RETIRA UN POQUITO, COMO SI RESPIRARA."""

    # UNA FRANJA SUAVE, MAS CLARA EN MEDIO Y TRANSPARENTE EN LAS DOS ORILLAS (SIN CORTES QUE SE NOTEN)
    capa = pygame.Surface((80, ALTO), pygame.SRCALPHA)

    for x in range(80):
        pygame.draw.line(capa, (*COLOR_BLANCO, int(math.sin(x / 80 * math.pi) * 40)), (x, 0), (x, ALTO))

    avance = int((math.sin(tiempo * 0.8) + 1) * 14)
    lienzo.blit(capa, (INICIO_BLANCO + 20 - avance, 0))


def dibujar_deshacerse(lienzo: pygame.Surface, tiempo: float) -> None:

    """PEDACITOS DE PASTO QUE SE DESPEGAN DEL PISO Y SE VUELVEN BLANCO MIENTRAS FLOTAN A LA DERECHA."""

    for i in range(18):

        fase = (tiempo * 0.3 + i / 18) % 1
        x = INICIO_BLANCO + 20 + (i * 23) % 90 + int(fase * 110)
        y = Y_PISO + 4 + (i * 11) % 40 - int(fase * 40) + int(math.sin(tiempo * 2 + i) * 2)

        color = mezclar((110, 160, 96), COLOR_BLANCO, fase)

        lienzo.set_at((x, y), color)

        if fase < 0.5:
            lienzo.set_at((x + 1, y), color)


def dibujar(ventana: pygame.Surface) -> None:

    """DIBUJA LA ESCENA COMPLETA EN LA VENTANA DEL JUEGO."""

    if "fijo" not in CAPAS:
        CAPAS["fijo"] = crear_fijo()

    tiempo = pygame.time.get_ticks() / 1000

    lienzo = CAPAS["fijo"].copy()

    dibujar_respiro(lienzo, tiempo)
    dibujar_deshacerse(lienzo, tiempo)
    personajes.dibujar_gato(lienzo, X_GATO, Y_PISO + 2, True, tiempo)

    mostrar(ventana, lienzo)
