"""FONDO DIBUJADO CON CODIGO: CORALINE Y LA OTRA MADRE HACEN EL TRATO DEL JUEGO.

En la cocina del desayuno (desayuno_otra_madre.py), la otra madre levanta la
mano para jurar. Arriba se ve el trato en una nube, como una balanza: de un
lado lo que Coraline gana (sus papas y las tres almas, que son canicas) y del
otro lo que pierde (dos botones negros, una aguja y un hilo). Se usa en
cap08_n02 y en su rama cap08_r02.

Lo que se mueve: la balanza que se mece sin decidirse, el brillo de la aguja
y el de los botones de la otra madre.
"""

import math

import pygame

from interfaz.fondos.pintura import ANCHO, ALTO
from interfaz.fondos.pintura import capa_vacia, pegar_con_contorno, COLOR_CONTORNO
from interfaz.fondos.pintura import brillo, orillas_oscuras, mostrar
from interfaz.fondos import personajes
from interfaz.fondos import sala_actrices
from interfaz.fondos import otra_cocina
from interfaz.fondos import desayuno_otra_madre

X_CORALINE = desayuno_otra_madre.X_CORALINE
X_MADRE = desayuno_otra_madre.X_MADRE

NUBE = pygame.Rect(436, 20, 150, 84)
CENTRO_BALANZA = (NUBE.centerx, NUBE.y + 30)
LARGO_BRAZO = 42

COLOR_NUBE = (246, 236, 214)

CAPAS = {}


# --------------------------------------------------
# PARTE FIJA
# --------------------------------------------------

def dibujar_nube(lienzo: pygame.Surface) -> None:

    """NUBE DEL TRATO CON BOLITAS QUE BAJAN HACIA LA OTRA MADRE."""

    capa = capa_vacia()

    for cx, cy, r in [(NUBE.x + 26, NUBE.centery + 4, 26), (NUBE.centerx, NUBE.centery - 6, 40),
                      (NUBE.right - 26, NUBE.centery + 4, 26), (NUBE.x + 50, NUBE.bottom - 16, 22),
                      (NUBE.right - 50, NUBE.bottom - 16, 22)]:
        pygame.draw.circle(capa, COLOR_NUBE, (cx, cy), r)

    for cx, cy, r in [(NUBE.right - 10, NUBE.bottom + 10, 6), (NUBE.right - 2, NUBE.bottom + 24, 4)]:
        pygame.draw.circle(capa, COLOR_NUBE, (cx, cy), r)

    pegar_con_contorno(lienzo, capa)

    # EL POSTE DE LA BALANZA
    x, y = CENTRO_BALANZA
    pygame.draw.line(lienzo, (150, 110, 60), (x, y), (x, NUBE.bottom - 14), 2)
    pygame.draw.line(lienzo, (150, 110, 60), (x - 10, NUBE.bottom - 14), (x + 10, NUBE.bottom - 14), 2)


def crear_fijo() -> pygame.Surface:

    lienzo = pygame.Surface((ANCHO, ALTO))

    otra_cocina.dibujar_cocina(lienzo)

    # LA OTRA MADRE JURA CON LA MANO EN ALTO (EL BRAZO DE DESPEDIRSE, QUIETO Y DERECHO)
    capa = capa_vacia()
    personajes.dibujar_otra_madre(capa, X_MADRE, "despedir")
    pegar_con_contorno(lienzo, capa)
    personajes.dibujar_brazo_saludo(lienzo, X_MADRE, "madre", 0)

    desayuno_otra_madre.dibujar_mesa_desayuno(lienzo)
    sala_actrices.dibujar_coraline(lienzo, X_CORALINE, True)

    brillo(lienzo, (447, 104), 120, (255, 220, 160), 50)
    orillas_oscuras(lienzo)

    # LA NUBE VA DESPUES DE LAS ORILLAS PARA QUE NO SE OSCUREZCA
    dibujar_nube(lienzo)

    return lienzo


# --------------------------------------------------
# LO QUE SE MUEVE
# --------------------------------------------------

def dibujar_platillo_gana(lienzo: pygame.Surface, x: int, y: int) -> None:

    """LO QUE GANA CORALINE: SUS PAPAS (DOS FIGURITAS) Y TRES CANICAS."""

    pygame.draw.circle(lienzo, (60, 40, 30), (x - 6, y - 14), 3)                    # mama
    pygame.draw.rect(lienzo, (226, 214, 190), (x - 8, y - 11, 5, 8))
    pygame.draw.circle(lienzo, (130, 80, 50), (x + 1, y - 15), 3)                   # papa
    pygame.draw.rect(lienzo, (90, 120, 100), (x - 1, y - 12, 5, 9))

    for i, color in enumerate([(120, 200, 230), (230, 150, 200), (160, 220, 150)]):
        pygame.draw.circle(lienzo, color, (x + 9 + (i % 2) * 4, y - 4 - (i // 2) * 4), 2)


def dibujar_platillo_pierde(lienzo: pygame.Surface, x: int, y: int, tiempo: float) -> None:

    """LO QUE PIERDE: DOS BOTONES NEGROS, UNA AGUJA Y UN HILO."""

    for dx in [-6, 3]:
        pygame.draw.circle(lienzo, (14, 12, 16), (x + dx, y - 6), 4)
        for hx, hy in [(-1, -1), (1, -1), (-1, 1), (1, 1)]:
            lienzo.set_at((x + dx + hx, y - 6 + hy), (90, 80, 90))

    pygame.draw.line(lienzo, (190, 196, 204), (x + 9, y - 2), (x + 15, y - 16))                # aguja
    pygame.draw.arc(lienzo, (196, 34, 46), (x + 6, y - 18, 12, 14), 0.5, 3.5)                  # hilo rojo

    if tiempo % 2 < 0.25:
        lienzo.set_at((x + 15, y - 17), (255, 255, 255))
        lienzo.set_at((x + 16, y - 16), (255, 255, 255))


def dibujar_balanza(lienzo: pygame.Surface, tiempo: float) -> None:

    """EL BRAZO DE LA BALANZA SE MECE: TODAVIA NADIE SABE QUIEN VA A GANAR."""

    x, y = CENTRO_BALANZA
    angulo = math.sin(tiempo * 1.2) * 0.18
    dx = int(math.cos(angulo) * LARGO_BRAZO)
    dy = int(math.sin(angulo) * LARGO_BRAZO)

    izquierda = (x - dx, y - dy)
    derecha = (x + dx, y + dy)

    pygame.draw.line(lienzo, (150, 110, 60), izquierda, derecha, 2)
    pygame.draw.circle(lienzo, (196, 156, 72), (x, y), 3)

    for punta in [izquierda, derecha]:
        plato = (punta[0], punta[1] + 22)
        pygame.draw.line(lienzo, (150, 110, 60), punta, (plato[0] - 10, plato[1]))
        pygame.draw.line(lienzo, (150, 110, 60), punta, (plato[0] + 10, plato[1]))
        pygame.draw.ellipse(lienzo, COLOR_CONTORNO, (plato[0] - 13, plato[1] - 1, 26, 6))
        pygame.draw.ellipse(lienzo, (196, 156, 72), (plato[0] - 12, plato[1], 24, 4))

    dibujar_platillo_gana(lienzo, izquierda[0] - 2, izquierda[1] + 22)
    dibujar_platillo_pierde(lienzo, derecha[0] - 2, derecha[1] + 22, tiempo)


def dibujar(ventana: pygame.Surface) -> None:

    """DIBUJA LA ESCENA COMPLETA EN LA VENTANA DEL JUEGO."""

    if "fijo" not in CAPAS:
        CAPAS["fijo"] = crear_fijo()

    tiempo = pygame.time.get_ticks() / 1000

    lienzo = CAPAS["fijo"].copy()

    sala_actrices.dibujar_vapor(lienzo, desayuno_otra_madre.CHOCOLATE[0], desayuno_otra_madre.CHOCOLATE[1] - 10, tiempo)
    personajes.dibujar_botones(lienzo, personajes.ojos_otra_madre(X_MADRE), tiempo, False, True)
    dibujar_balanza(lienzo, tiempo)

    mostrar(ventana, lienzo)
