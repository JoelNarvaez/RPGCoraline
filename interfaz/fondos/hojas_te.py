"""FONDO DIBUJADO CON CODIGO: LA SENORITA FORCIBLE LEE LAS HOJAS DEL TE.

La senorita Forcible levanta la taza y se pone palida: ve un gran peligro.
La senorita Spink, con los brazos cruzados, no esta de acuerdo, y las dos
discuten mientras Coraline las mira. Se usa en cap02_n04. La sala, la mesa
y Coraline estan en sala_actrices.py; las vecinas en personajes.py.

Lo que se mueve: un brillo oscuro que late en la taza, las rayitas de la
discusion que saltan de una cabeza a la otra y los parpadeos.
"""

import math

import pygame

from interfaz.fondos.pintura import ANCHO, ALTO
from interfaz.fondos.pintura import capa_vacia, pegar_con_contorno
from interfaz.fondos.pintura import orillas_oscuras, mostrar
from interfaz.fondos import personajes
from interfaz.fondos import sala_actrices

X_CORALINE = 432
X_MESA = 490
X_FORCIBLE = 522
X_SPINK = 598

COLOR_ENOJO = (255, 226, 120)

CAPAS = {}


def crear_fijo() -> pygame.Surface:

    lienzo = pygame.Surface((ANCHO, ALTO))

    sala_actrices.dibujar_sala(lienzo)
    # CADA COSA EN SU CAPA, PARA PEGARLA CON CONTORNO (COMO SPRITE DE RPG)
    capa = capa_vacia()
    personajes.dibujar_spink(capa, X_SPINK, "brazos_cruzados")
    pegar_con_contorno(lienzo, capa)

    capa = capa_vacia()
    personajes.dibujar_forcible(capa, X_FORCIBLE, "taza", True)
    pegar_con_contorno(lienzo, capa)

    capa = capa_vacia()
    sala_actrices.dibujar_mesa(capa, X_MESA, True)
    pegar_con_contorno(lienzo, capa)
    sala_actrices.dibujar_coraline(lienzo, X_CORALINE)
    sala_actrices.dibujar_luces(lienzo)
    orillas_oscuras(lienzo)

    return lienzo


# --------------------------------------------------
# LO QUE SE MUEVE
# --------------------------------------------------

def dibujar_presagio(lienzo: pygame.Surface, tiempo: float) -> None:

    """BRILLO MORADO OSCURO QUE LATE SOBRE LA TAZA: LO QUE VE LA SENORITA FORCIBLE."""

    x, y = personajes.taza_forcible(X_FORCIBLE)

    fuerza = 0.5 + 0.5 * math.sin(tiempo * 3)
    radio = 10 + int(fuerza * 4)

    capa = pygame.Surface((radio * 2, radio * 2), pygame.SRCALPHA)

    for r in range(radio, 0, -2):
        alfa = int((1 - r / radio) * 90 * (0.5 + fuerza / 2))
        pygame.draw.circle(capa, (90, 40, 120, alfa), (radio, radio), r)

    lienzo.blit(capa, (x - radio, y - 4 - radio))


def dibujar_rayitas(lienzo: pygame.Surface, x: int, y: int) -> None:

    """TRES RAYITAS DE ENOJO SALIENDO DE UNA CABEZA."""

    pygame.draw.line(lienzo, COLOR_ENOJO, (x - 8, y), (x - 12, y - 6), 2)
    pygame.draw.line(lienzo, COLOR_ENOJO, (x, y - 3), (x, y - 10), 2)
    pygame.draw.line(lienzo, COLOR_ENOJO, (x + 8, y), (x + 12, y - 6), 2)


def dibujar_discusion(lienzo: pygame.Surface, tiempo: float) -> None:

    """LAS RAYITAS SALTAN DE UNA VECINA A LA OTRA, COMO SI SE CONTESTARAN."""

    if int(tiempo * 1.5) % 2 == 0:
        dibujar_rayitas(lienzo, X_SPINK + 2, 138)
    else:
        dibujar_rayitas(lienzo, X_FORCIBLE, 122)


def dibujar(ventana: pygame.Surface) -> None:

    """DIBUJA LA ESCENA COMPLETA EN LA VENTANA DEL JUEGO."""

    if "fijo" not in CAPAS:
        CAPAS["fijo"] = crear_fijo()

    tiempo = pygame.time.get_ticks() / 1000

    lienzo = CAPAS["fijo"].copy()

    dibujar_presagio(lienzo, tiempo)
    dibujar_discusion(lienzo, tiempo)
    personajes.dibujar_ojos_spink(lienzo, X_SPINK, tiempo, True)
    personajes.dibujar_ojos_forcible(lienzo, X_FORCIBLE, tiempo, "taza", True)

    mostrar(ventana, lienzo)
