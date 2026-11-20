"""FONDO DIBUJADO CON CODIGO: CORALINE HUYE DEL TEATRO CON DOS ALMAS.

El teatro abandonado de teatro_abandonado.py. Coraline ya tiene las dos
canicas, que le brillan en la mano, y corre por el pasillo hacia la salida.
Todos los perros del publico la miran con ojos rojos, sin moverse, y la
criatura del escenario avanza un poco hacia la orilla. La voz de la nina
fantasma le grita que huya: una burbuja palida con un signo de admiracion.
Se usa en cap08_n05 y en su rama cap08_r05.

Lo que se mueve: Coraline que da saltitos al correr, las rayitas de
velocidad, las canicas que brillan, la criatura que avanza y se regresa, los
ojos rojos de los perros y la burbuja del grito que late.
"""

import math

import pygame

from interfaz.fondos.pintura import ANCHO, ALTO
from interfaz.fondos.pintura import COLOR_CONTORNO
from interfaz.fondos.pintura import brillo, orillas_oscuras, mostrar
from interfaz.fondos import personajes
from interfaz.fondos import hueco_espejo
from interfaz.fondos import teatro_abandonado

X_CORALINE = 300
Y_CORALINE = teatro_abandonado.Y_CORALINE
MANO = (X_CORALINE - 10, Y_CORALINE - 42)           # donde lleva las canicas
GRITO = pygame.Rect(X_CORALINE + 18, 226, 26, 22)

CAPAS = {}


def crear_fijo() -> pygame.Surface:

    lienzo = teatro_abandonado.crear_base()
    teatro_abandonado.dibujar_perros_quietos(lienzo)

    brillo(lienzo, (teatro_abandonado.X_CRIATURA, 180), 90, (190, 196, 220), 30)
    brillo(lienzo, MANO, 40, (200, 220, 255), 40)
    orillas_oscuras(lienzo)

    return lienzo


# --------------------------------------------------
# LO QUE SE MUEVE
# --------------------------------------------------

def dibujar_coraline(lienzo: pygame.Surface, tiempo: float) -> None:

    """CORALINE CORRIENDO HACIA LA IZQUIERDA, CON SALTITOS Y RAYAS DE VELOCIDAD DETRAS."""

    salto = int(abs(math.sin(tiempo * 9)) * 3)
    personajes.dibujar_coraline_chica(lienzo, X_CORALINE, Y_CORALINE - salto, False)

    for i in range(3):
        largo = 10 + ((int(tiempo * 10) + i) % 3) * 4
        y = Y_CORALINE - 70 + i * 18 - salto
        pygame.draw.line(lienzo, (200, 196, 210), (X_CORALINE + 22, y), (X_CORALINE + 22 + largo, y))


def dibujar_canicas(lienzo: pygame.Surface, tiempo: float) -> None:

    """LAS DOS CANICAS EN SU MANO, CON UN BRILLO QUE LATE."""

    luz = (math.sin(tiempo * 4) + 1) / 2
    salto = int(abs(math.sin(tiempo * 9)) * 3)

    capa = pygame.Surface((30, 30), pygame.SRCALPHA)
    pygame.draw.circle(capa, (255, 250, 220, int(20 + luz * 40)), (15, 15), 8)
    pygame.draw.circle(capa, (255, 255, 240, int(40 + luz * 60)), (15, 15), 5)
    lienzo.blit(capa, (MANO[0] - 15, MANO[1] - 15 - salto))

    for dx, color in [(-3, (120, 200, 230)), (3, (230, 150, 200))]:
        x, y = MANO[0] + dx, MANO[1] - salto
        pygame.draw.circle(lienzo, COLOR_CONTORNO, (x, y), 3)
        pygame.draw.circle(lienzo, (226, 232, 240), (x, y), 2)
        lienzo.set_at((x, y), color)


def dibujar_grito(lienzo: pygame.Surface, tiempo: float) -> None:

    """BURBUJA PALIDA (LA VOZ DE LA NINA FANTASMA) CON UN SIGNO DE ADMIRACION QUE LATE."""

    crece = 1 if math.sin(tiempo * 8) > 0 else 0
    burbuja = GRITO.inflate(crece * 2, crece * 2)

    pygame.draw.ellipse(lienzo, COLOR_CONTORNO, burbuja.inflate(2, 2))
    pygame.draw.ellipse(lienzo, hueco_espejo.COLOR_FANTASMA, burbuja)
    pygame.draw.polygon(lienzo, hueco_espejo.COLOR_FANTASMA, [(GRITO.x + 4, GRITO.bottom - 5),
                                                              (GRITO.x + 10, GRITO.bottom - 2),
                                                              (GRITO.x - 4, GRITO.bottom + 8)])

    pygame.draw.rect(lienzo, (180, 40, 60), (GRITO.centerx - 1, GRITO.y + 4, 3, 9))
    pygame.draw.rect(lienzo, (180, 40, 60), (GRITO.centerx - 1, GRITO.y + 15, 3, 3))


def dibujar(ventana: pygame.Surface) -> None:

    """DIBUJA LA ESCENA COMPLETA EN LA VENTANA DEL JUEGO."""

    if "fijo" not in CAPAS:
        CAPAS["fijo"] = crear_fijo()

    tiempo = pygame.time.get_ticks() / 1000

    lienzo = CAPAS["fijo"].copy()

    avance = int((math.sin(tiempo * 0.6) + 1) * 8)
    teatro_abandonado.dibujar_criatura(lienzo, tiempo, avance)
    teatro_abandonado.dibujar_ojos_perros(lienzo, tiempo, (230, 50, 50))
    teatro_abandonado.dibujar_polvo(lienzo, tiempo)
    dibujar_coraline(lienzo, tiempo)
    dibujar_canicas(lienzo, tiempo)
    dibujar_grito(lienzo, tiempo)

    mostrar(ventana, lienzo)
