"""FONDO DIBUJADO CON CODIGO: CORALINE LE ACARICIA LA CABEZA AL OTRO PADRE.

En el sotano de sotano.py, lo que queda del otro padre esta sentado en el
piso: una masa blanca y blanda que tiembla. Le pide perdon y se le cae uno de
los botones, que rueda por el piso. Coraline, a su lado, le acaricia la
cabeza: el solo es algo que la otra madre hizo y luego tiro. Se usa en
cap09_n04 y en su rama cap09_r04.

Lo que se mueve: el foco que se mece, la masa que tiembla, la mano de
Coraline que lo acaricia, el boton que se cae y rueda (y vuelve a empezar) y
una lagrima blanca que escurre.
"""

import math

import pygame

from interfaz.fondos.pintura import ANCHO, ALTO
from interfaz.fondos.pintura import COLOR_CONTORNO
from interfaz.fondos.pintura import orillas_oscuras, mostrar
from interfaz.fondos import personajes
from interfaz.fondos import sotano

Y_PISO = sotano.Y_PISO

X_PADRE = 458
ALTO_PADRE = 46                          # sentado, medio desparramado
X_CORALINE = 504
CICLO_BOTON = 6.0                        # cada cuanto se vuelve a caer el boton

CAPAS = {}


def crear_fijo() -> pygame.Surface:

    lienzo = pygame.Surface((ANCHO, ALTO))
    sotano.dibujar_sotano(lienzo)
    personajes.dibujar_coraline_chica(lienzo, X_CORALINE, Y_PISO, False)
    orillas_oscuras(lienzo)

    return lienzo


# --------------------------------------------------
# LO QUE SE MUEVE
# --------------------------------------------------

def ojo_que_se_cae(tiempo: float) -> tuple:

    x = X_PADRE + 6 - int(math.sin(tiempo * 7) * 1.5)

    return (x, Y_PISO - ALTO_PADRE - 8)


def dibujar_boton_cayendo(lienzo: pygame.Surface, tiempo: float) -> None:

    """EL BOTON DERECHO SE AFLOJA, SE CAE Y RUEDA POR EL PISO."""

    fase = tiempo % CICLO_BOTON
    ojo = ojo_que_se_cae(tiempo)

    if fase < 1.5:
        # TODAVIA EN SU LUGAR, PERO EL HILO SE ESTA ZAFANDO
        if fase > 0.8:
            pygame.draw.line(lienzo, (40, 36, 40), (ojo[0], ojo[1] + 3), (ojo[0] + 1, ojo[1] + 6))
        return

    if fase < 2.2:
        # CAE
        avance = (fase - 1.5) / 0.7
        x = ojo[0] + int(avance * 6)
        y = ojo[1] + int(avance * avance * (Y_PISO - 4 - ojo[1]))
    else:
        # RUEDA UN POCO Y SE QUEDA EN EL PISO
        avance = min(1.0, (fase - 2.2) / 1.2)
        x = ojo[0] + 6 + int(math.sin(avance * math.pi / 2) * 22)
        y = Y_PISO - 4

    pygame.draw.circle(lienzo, COLOR_CONTORNO, (x, y), 4)
    pygame.draw.circle(lienzo, (14, 12, 16), (x, y), 3)
    for dx, dy in [(-1, -1), (1, -1), (-1, 1), (1, 1)]:
        lienzo.set_at((x + dx, y + dy), (90, 80, 90))

    # EL HILO SUELTO QUE QUEDA COLGANDO DONDE ESTABA EL BOTON
    pygame.draw.line(lienzo, (40, 36, 40), ojo, (ojo[0] + 1, ojo[1] + 6))


def dibujar_lagrima(lienzo: pygame.Surface, tiempo: float) -> None:

    """UNA LAGRIMA BLANCA Y ESPESA QUE ESCURRE POR LA MASA DESDE EL OTRO BOTON."""

    fase = (tiempo * 0.5) % 1
    x = X_PADRE - 6
    y = Y_PISO - ALTO_PADRE - 4 + int(fase * 26)

    pygame.draw.line(lienzo, (240, 238, 232), (x, Y_PISO - ALTO_PADRE - 4), (x, y), 2)
    pygame.draw.circle(lienzo, (250, 250, 246), (x, y + 1), 2)


def dibujar_caricia(lienzo: pygame.Surface, tiempo: float) -> None:

    """EL BRAZO DE CORALINE (MANGA AMARILLA Y GUANTE) ESTIRADO, LA MANO VA Y VIENE SOBRE LA CABEZA."""

    hombro = (X_CORALINE - 6, Y_PISO - 60)
    vaiven = int(math.sin(tiempo * 2) * 4)
    mano = (X_PADRE + 6 + vaiven, Y_PISO - ALTO_PADRE - 22)

    pygame.draw.line(lienzo, COLOR_CONTORNO, hombro, mano, 7)
    pygame.draw.line(lienzo, personajes.AMARILLO, hombro, mano, 5)
    pygame.draw.circle(lienzo, COLOR_CONTORNO, mano, 5)
    pygame.draw.circle(lienzo, personajes.AZUL_OSCURO, mano, 4)
    pygame.draw.line(lienzo, personajes.PIEL_CHIBI, (mano[0] - 4, mano[1] + 2), (mano[0] - 7, mano[1] + 4), 2)


def dibujar(ventana: pygame.Surface) -> None:

    """DIBUJA LA ESCENA COMPLETA EN LA VENTANA DEL JUEGO."""

    if "fijo" not in CAPAS:
        CAPAS["fijo"] = crear_fijo()

    tiempo = pygame.time.get_ticks() / 1000

    lienzo = CAPAS["fijo"].copy()

    sotano.dibujar_foco(lienzo, tiempo)

    # PRIMERO SE SABE CUANTOS BOTONES LE QUEDAN; EL QUE SE CAE SE DIBUJA ENCIMA DE LA MASA
    fase = tiempo % CICLO_BOTON
    botones = 2 if fase < 1.5 else 1
    sotano.dibujar_padre_derretido(lienzo, X_PADRE, Y_PISO, tiempo, ALTO_PADRE, False, botones)
    dibujar_boton_cayendo(lienzo, tiempo)
    dibujar_lagrima(lienzo, tiempo)
    dibujar_caricia(lienzo, tiempo)

    mostrar(ventana, lienzo)
