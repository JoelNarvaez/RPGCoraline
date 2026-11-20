"""FONDO DIBUJADO CON CODIGO: LA OTRA MADRE SE COME UN ESCARABAJO Y ABRE EL ESPEJO.

Es el pasillo de espejo_otra_madre.py (cap06_n04), pero la luz se puso rojiza
y oscura porque la otra madre se enojo. Saca un escarabajo de una bolsita de
papel y se lo come. El vidrio del espejo esta abierto como una puerta y atras
hay un hueco negro y frio: ahi va a encerrar a Coraline. Se usa en cap06_n05 y
en su rama cap06_r05.

Lo que se mueve: el escarabajo que patalea y desaparece en la boca (crac),
el aire frio que sale del hueco, la oscuridad de adentro que late y el
brillo de los botones.
"""

import math

import pygame

from interfaz.fondos.pintura import ANCHO, ALTO
from interfaz.fondos.pintura import capa_vacia, pegar_con_contorno
from interfaz.fondos.pintura import brillo, orillas_oscuras, mostrar
from interfaz.fondos import personajes
from interfaz.fondos import sala_actrices
from interfaz.fondos import espejo_otra_madre

Y_PISO = espejo_otra_madre.Y_PISO
ESPEJO = espejo_otra_madre.ESPEJO
VIDRIO = espejo_otra_madre.VIDRIO

X_MADRE = 462
X_CORALINE = 530

CAPAS = {}


# --------------------------------------------------
# PARTE FIJA
# --------------------------------------------------

def oscurecer(lienzo: pygame.Surface) -> None:

    """TINTE ROJIZO Y OSCURO SOBRE TODO EL PASILLO (LA OTRA MADRE ESTA FURIOSA)."""

    tinte = pygame.Surface((ANCHO, ALTO))
    tinte.fill((170, 110, 120))
    lienzo.blit(tinte, (0, 0), special_flags=pygame.BLEND_MULT)


def dibujar_hueco(lienzo: pygame.Surface) -> None:

    """DETRAS DEL VIDRIO HAY UN HUECO NEGRO; EL VIDRIO QUEDA ABIERTO HACIA LA IZQUIERDA."""

    pygame.draw.rect(lienzo, (6, 6, 10), VIDRIO)

    # ORILLAS DEL HUECO QUE SE PIERDEN HACIA ADENTRO
    centro = (VIDRIO.centerx + 4, VIDRIO.centery + 10)
    pygame.draw.polygon(lienzo, (18, 16, 24), [VIDRIO.topleft, (centro[0] - 8, centro[1] - 40),
                                               (centro[0] - 8, centro[1] + 40), VIDRIO.bottomleft])
    pygame.draw.polygon(lienzo, (12, 12, 18), [VIDRIO.topright, (centro[0] + 8, centro[1] - 40),
                                               (centro[0] + 8, centro[1] + 40), VIDRIO.bottomright])


def dibujar_vidrio_abierto(capa: pygame.Surface) -> None:

    """EL VIDRIO, CON SU MARCO DELGADO, GIRADO COMO PUERTA (SE VE ANGOSTO, EN PERSPECTIVA)."""

    bisagra = VIDRIO.x
    puntas = [(bisagra, VIDRIO.y), (bisagra - 20, VIDRIO.y + 10), (bisagra - 20, VIDRIO.bottom - 6), (bisagra, VIDRIO.bottom)]

    pygame.draw.polygon(capa, (120, 84, 50), puntas)
    pygame.draw.polygon(capa, (100, 90, 120), [(bisagra - 2, VIDRIO.y + 4), (bisagra - 18, VIDRIO.y + 12),
                                               (bisagra - 18, VIDRIO.bottom - 8), (bisagra - 2, VIDRIO.bottom - 4)])
    pygame.draw.line(capa, (180, 170, 200), (bisagra - 6, VIDRIO.y + 20), (bisagra - 14, VIDRIO.y + 40))


def crear_fijo() -> pygame.Surface:

    lienzo = pygame.Surface((ANCHO, ALTO))

    espejo_otra_madre.dibujar_pasillo(lienzo)
    espejo_otra_madre.dibujar_marco(lienzo)
    dibujar_hueco(lienzo)
    oscurecer(lienzo)

    capa = capa_vacia()
    dibujar_vidrio_abierto(capa)
    personajes.dibujar_otra_madre(capa, X_MADRE, "escarabajo")
    pegar_con_contorno(lienzo, capa)

    sala_actrices.dibujar_coraline(lienzo, X_CORALINE, False)

    brillo(lienzo, (X_MADRE, 170), 80, (200, 60, 60), 40)
    orillas_oscuras(lienzo)

    return lienzo


# --------------------------------------------------
# LO QUE SE MUEVE
# --------------------------------------------------

def dibujar_escarabajo(lienzo: pygame.Surface, tiempo: float) -> None:

    """EL ESCARABAJO PATALEA ENTRE SUS DEDOS 3 SEGUNDOS; LUEGO SE LO COME Y SALE UN "CRAC"."""

    mano = personajes.mano_escarabajo(X_MADRE)
    fase = tiempo % 4

    if fase > 3:
        # CRAC: RAYITAS QUE SALEN DE LA BOCA
        boca = (X_MADRE, 155)
        for dx, dy in [(-7, -3), (7, -3), (-6, 3), (6, 3)]:
            pygame.draw.line(lienzo, (240, 220, 200), (boca[0] + dx // 2, boca[1] + dy // 2), (boca[0] + dx, boca[1] + dy))
        return

    # SUBE DESPACIO DE LA MANO A LA BOCA
    x = mano[0] - int(fase / 3 * 4)
    y = mano[1] - 6 - int(fase / 3 * 2)
    patas = int(tiempo * 12) % 2

    for lado in [-1, 1]:
        for i in range(3):
            pygame.draw.line(lienzo, (20, 30, 24), (x + lado * 2, y - 1 + i * 2), (x + lado * (4 + patas), y - 2 + i * 2 + patas))

    pygame.draw.ellipse(lienzo, (24, 40, 30), (x - 2, y - 3, 5, 7))
    lienzo.set_at((x, y - 2), (90, 160, 120))                                   # brillo verde del caparazon


def dibujar_aire_frio(lienzo: pygame.Surface, tiempo: float) -> None:

    """HILOS DE AIRE FRIO QUE SALEN DEL HUECO Y SE ARRASTRAN POR EL PISO."""

    capa = pygame.Surface((ANCHO, ALTO), pygame.SRCALPHA)

    for i in range(5):

        fase = (tiempo * 0.4 + i / 5) % 1
        x = VIDRIO.centerx - int(fase * 110)
        y = Y_PISO - 6 - i * 4 + int(math.sin(tiempo * 2 + i) * 2)
        alfa = int(80 * (1 - fase))

        pygame.draw.line(capa, (170, 200, 220, alfa), (x - 10, y), (x + 8, y - 1))

    lienzo.blit(capa, (0, 0))


def dibujar_oscuridad(lienzo: pygame.Surface, tiempo: float) -> None:

    """ADENTRO DEL HUECO LA OSCURIDAD LATE: UN RECTANGULITO QUE CRECE Y SE ENCOGE AL FONDO."""

    tamano = 6 + int((math.sin(tiempo * 1.5) + 1) * 3)
    centro = (VIDRIO.centerx + 4, VIDRIO.centery + 10)

    pygame.draw.rect(lienzo, (0, 0, 0), (centro[0] - tamano // 2, centro[1] - tamano * 2, tamano, tamano * 4))


def dibujar(ventana: pygame.Surface) -> None:

    """DIBUJA LA ESCENA COMPLETA EN LA VENTANA DEL JUEGO."""

    if "fijo" not in CAPAS:
        CAPAS["fijo"] = crear_fijo()

    tiempo = pygame.time.get_ticks() / 1000

    lienzo = CAPAS["fijo"].copy()

    dibujar_oscuridad(lienzo, tiempo)
    dibujar_aire_frio(lienzo, tiempo)
    dibujar_escarabajo(lienzo, tiempo)
    personajes.dibujar_botones(lienzo, personajes.ojos_otra_madre(X_MADRE), tiempo, False, True)

    mostrar(ventana, lienzo)
