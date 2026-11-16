"""FONDO DIBUJADO CON CODIGO: LA SENORITA SPINK LE REGALA LA PIEDRA.

La senorita Spink saco de su comoda una piedra con un agujero en medio y se
la da a Coraline. Atras queda la comoda con el cajon abierto. Se usa en
cap02_n05. La sala y Coraline estan en sala_actrices.py; la senorita Spink
en personajes.py.

Lo que se mueve: la piedra brilla de vez en cuando y la senorita Spink parpadea.
"""

import pygame

from interfaz.fondos.pintura import ANCHO, ALTO
from interfaz.fondos.pintura import capa_vacia, pegar_con_contorno
from interfaz.fondos.pintura import mezclar, orillas_oscuras, mostrar
from interfaz.fondos import personajes
from interfaz.fondos import sala_actrices

X_CORALINE = 432
X_SPINK = 522

COMODA = pygame.Rect(570, 214, 64, 86)

COLOR_MADERA = (104, 62, 40)
COLOR_PIEDRA = (150, 150, 140)

CAPAS = {}


def dibujar_comoda(lienzo: pygame.Surface) -> None:

    """COMODA DE MADERA CON EL CAJON DE ARRIBA ABIERTO Y COSAS ADENTRO."""

    pygame.draw.rect(lienzo, COLOR_MADERA, COMODA)
    pygame.draw.rect(lienzo, mezclar(COLOR_MADERA, (0, 0, 0), 0.35), COMODA, 2)

    # CAJONES DE ABAJO CERRADOS
    for y in [COMODA.y + 32, COMODA.y + 58]:
        pygame.draw.rect(lienzo, mezclar(COLOR_MADERA, (0, 0, 0), 0.2), (COMODA.x + 4, y, COMODA.width - 8, 22), 1)
        pygame.draw.circle(lienzo, (210, 170, 90), (COMODA.centerx, y + 11), 2)

    # CAJON DE ARRIBA SALIDO HACIA EL FRENTE, CON ESTAMBRES, UN LISTON Y BOTONES
    cajon = pygame.Rect(COMODA.x - 6, COMODA.y + 6, COMODA.width + 2, 22)
    pygame.draw.rect(lienzo, (60, 34, 24), (cajon.x, cajon.y - 6, cajon.width, 8))
    pygame.draw.circle(lienzo, (200, 80, 90), (cajon.x + 12, cajon.y - 4), 5)
    pygame.draw.circle(lienzo, (120, 150, 200), (cajon.x + 26, cajon.y - 3), 4)
    pygame.draw.line(lienzo, (230, 200, 90), (cajon.x + 34, cajon.y - 4), (cajon.x + 52, cajon.y - 2), 2)
    pygame.draw.rect(lienzo, mezclar(COLOR_MADERA, (255, 255, 255), 0.1), cajon)
    pygame.draw.rect(lienzo, mezclar(COLOR_MADERA, (0, 0, 0), 0.35), cajon, 1)
    pygame.draw.circle(lienzo, (210, 170, 90), cajon.center, 2)

    # FOTO CON MARCO Y FLORERO ENCIMA
    pygame.draw.rect(lienzo, sala_actrices.COLOR_DORADO, (COMODA.x + 6, COMODA.y - 18, 14, 18))
    pygame.draw.rect(lienzo, (190, 166, 128), (COMODA.x + 8, COMODA.y - 16, 10, 14))
    pygame.draw.rect(lienzo, (70, 110, 120), (COMODA.x + 42, COMODA.y - 14, 10, 14), border_radius=3)
    pygame.draw.circle(lienzo, (220, 110, 130), (COMODA.x + 44, COMODA.y - 18), 4)
    pygame.draw.circle(lienzo, (240, 200, 120), (COMODA.x + 50, COMODA.y - 20), 4)


def piedra() -> tuple:

    """DONDE ESTA LA PIEDRA: EN LA MANO ESTIRADA DE LA SENORITA SPINK, UN POCO ARRIBA."""

    mano = personajes.mano_spink(X_SPINK, "dar")

    return (mano[0], mano[1] - 7)


def dibujar_piedra(lienzo: pygame.Surface) -> None:

    """PIEDRA GRIS REDONDEADA CON EL AGUJERO EN MEDIO."""

    x, y = piedra()

    pygame.draw.ellipse(lienzo, COLOR_PIEDRA, (x - 6, y - 5, 13, 10))
    pygame.draw.ellipse(lienzo, mezclar(COLOR_PIEDRA, (0, 0, 0), 0.3), (x - 6, y - 5, 13, 10), 1)
    pygame.draw.circle(lienzo, (40, 30, 34), (x, y), 2)
    pygame.draw.line(lienzo, (200, 200, 190), (x - 4, y - 3), (x - 1, y - 4))


def crear_fijo() -> pygame.Surface:

    lienzo = pygame.Surface((ANCHO, ALTO))

    sala_actrices.dibujar_sala(lienzo)
    # CADA COSA EN SU CAPA, PARA PEGARLA CON CONTORNO (COMO SPRITE DE RPG)
    capa = capa_vacia()
    dibujar_comoda(capa)
    pegar_con_contorno(lienzo, capa)

    capa = capa_vacia()
    personajes.dibujar_spink(capa, X_SPINK, "dar")
    dibujar_piedra(capa)
    pegar_con_contorno(lienzo, capa)
    sala_actrices.dibujar_coraline(lienzo, X_CORALINE)
    sala_actrices.dibujar_luces(lienzo)
    orillas_oscuras(lienzo)

    return lienzo


def dibujar_destello(lienzo: pygame.Surface, tiempo: float) -> None:

    """UNA ESTRELLITA QUE APARECE EN LA PIEDRA CADA 2.5 SEGUNDOS."""

    fase = tiempo % 2.5

    if fase < 0.5:

        x, y = piedra()
        tamano = 2 + int((0.25 - abs(fase - 0.25)) * 16)

        pygame.draw.line(lienzo, (255, 252, 220), (x + 4 - tamano, y - 5), (x + 4 + tamano, y - 5))
        pygame.draw.line(lienzo, (255, 252, 220), (x + 4, y - 5 - tamano), (x + 4, y - 5 + tamano))


def dibujar(ventana: pygame.Surface) -> None:

    """DIBUJA LA ESCENA COMPLETA EN LA VENTANA DEL JUEGO."""

    if "fijo" not in CAPAS:
        CAPAS["fijo"] = crear_fijo()

    tiempo = pygame.time.get_ticks() / 1000

    lienzo = CAPAS["fijo"].copy()

    dibujar_destello(lienzo, tiempo)
    personajes.dibujar_ojos_spink(lienzo, X_SPINK, tiempo, False)

    mostrar(ventana, lienzo)
