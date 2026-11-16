"""FONDO DIBUJADO CON CODIGO: EL TE CON LAS SENORITAS SPINK Y FORCIBLE.

Coraline toma el te en la sala de las actrices: la senorita Forcible detras
de la mesita, la senorita Spink a un lado y un perrito al frente. Se usa en
cap02_n03. La sala, la mesa y Coraline estan en sala_actrices.py; las
vecinas y el perro en personajes.py.

Lo que se mueve: el vapor de la tetera, la cola del perro y los parpadeos.
"""

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
X_PERRO = 600             # cola del perro; esta acostado al frente, sobre el tapete

CAPAS = {}


def crear_fijo() -> pygame.Surface:

    lienzo = pygame.Surface((ANCHO, ALTO))

    sala_actrices.dibujar_sala(lienzo)
    # CADA COSA EN SU CAPA, PARA PEGARLA CON CONTORNO (COMO SPRITE DE RPG)
    capa = capa_vacia()
    personajes.dibujar_spink(capa, X_SPINK, "normal")
    pegar_con_contorno(lienzo, capa)

    capa = capa_vacia()
    personajes.dibujar_forcible(capa, X_FORCIBLE, "normal", False)
    pegar_con_contorno(lienzo, capa)

    capa = capa_vacia()
    sala_actrices.dibujar_mesa(capa, X_MESA, True)
    pegar_con_contorno(lienzo, capa)
    sala_actrices.dibujar_coraline(lienzo, X_CORALINE)
    sala_actrices.dibujar_luces(lienzo)
    orillas_oscuras(lienzo)

    return lienzo


def dibujar(ventana: pygame.Surface) -> None:

    """DIBUJA LA ESCENA COMPLETA EN LA VENTANA DEL JUEGO."""

    if "fijo" not in CAPAS:
        CAPAS["fijo"] = crear_fijo()

    tiempo = pygame.time.get_ticks() / 1000

    lienzo = CAPAS["fijo"].copy()

    sala_actrices.dibujar_vapor(lienzo, X_MESA + 7, 220, tiempo)
    personajes.dibujar_ojos_spink(lienzo, X_SPINK, tiempo, False)
    personajes.dibujar_ojos_forcible(lienzo, X_FORCIBLE, tiempo, "normal", False)
    personajes.dibujar_perro(lienzo, X_PERRO, sala_actrices.Y_PISO + 26, tiempo, 0)

    mostrar(ventana, lienzo)
