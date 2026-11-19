"""FONDO DIBUJADO CON CODIGO: LAS VECINAS Y SUS RECORTES DE PERIODICO.

Coraline baja a contarle a las senoritas Spink y Forcible que sus papas
desaparecieron, pero ellas apenas la escuchan: acaban de encontrar unos
recortes de periodico de su epoca de teatro. La senorita Forcible tiene un
album abierto en las manos y la senorita Spink le estira un recorte; hay mas
recortes regados en el tapete. La sala, Coraline y las vecinas vienen de
sala_actrices.py y personajes.py (las mismas de cap02). Se usa en cap05_n02.

Lo que se mueve: los parpadeos, la cola del perro, el recorte que tiembla
en la mano de la senorita Spink y la burbuja de Coraline que nadie contesta.
"""

import math

import pygame

from interfaz.fondos.pintura import ANCHO, ALTO
from interfaz.fondos.pintura import capa_vacia, pegar_con_contorno, COLOR_CONTORNO
from interfaz.fondos.pintura import orillas_oscuras, mostrar
from interfaz.fondos import personajes
from interfaz.fondos import sala_actrices

Y_PISO = sala_actrices.Y_PISO

X_CORALINE = 430
X_FORCIBLE = 510
X_SPINK = 596
X_PERRO = 486             # cola del perro; esta acostado al frente, sobre el tapete

PAPEL = (226, 216, 186)
PAPEL_SOMBRA = (186, 174, 146)
TINTA = (70, 64, 60)

# RECORTES REGADOS EN EL PISO: (x, y, ancho, alto)
RECORTES_PISO = [(452, 306, 14, 9), (540, 312, 12, 8), (566, 304, 10, 12), (612, 314, 14, 8)]

CAPAS = {}


# --------------------------------------------------
# PARTE FIJA
# --------------------------------------------------

def dibujar_recorte(lienzo: pygame.Surface, x: int, y: int, ancho: int, alto: int) -> None:

    """UN RECORTE DE PERIODICO AMARILLENTO: FOTITO ARRIBA Y RENGLONES DE LETRA."""

    pygame.draw.rect(lienzo, PAPEL, (x, y, ancho, alto))
    pygame.draw.line(lienzo, PAPEL_SOMBRA, (x, y + alto - 1), (x + ancho - 1, y + alto - 1))

    foto = max(alto // 3, 2)
    pygame.draw.rect(lienzo, (120, 110, 104), (x + 2, y + 1, ancho // 2, foto))

    for yy in range(y + foto + 2, y + alto - 1, 2):
        pygame.draw.line(lienzo, TINTA, (x + 2, yy), (x + ancho - 3, yy))

    pygame.draw.rect(lienzo, COLOR_CONTORNO, (x - 1, y - 1, ancho + 2, alto + 2), 1)


def dibujar_album(lienzo: pygame.Surface) -> None:

    """ALBUM ABIERTO EN LAS MANOS DE LA SENORITA FORCIBLE, LLENO DE RECORTES PEGADOS."""

    x, y = X_FORCIBLE, 216

    pygame.draw.polygon(lienzo, (110, 40, 50), [(x - 18, y), (x + 18, y), (x + 20, y + 14), (x - 20, y + 14)])     # pastas
    pygame.draw.polygon(lienzo, PAPEL, [(x - 17, y - 1), (x - 1, y + 1), (x - 1, y + 13), (x - 18, y + 12)])
    pygame.draw.polygon(lienzo, PAPEL, [(x + 1, y + 1), (x + 17, y - 1), (x + 18, y + 12), (x + 1, y + 13)])
    pygame.draw.line(lienzo, PAPEL_SOMBRA, (x, y + 1), (x, y + 13))

    # FOTITO DE LAS DOS DE JOVENES Y RENGLONES
    pygame.draw.rect(lienzo, (130, 110, 100), (x - 14, y + 2, 7, 6))
    pygame.draw.rect(lienzo, (130, 110, 100), (x + 4, y + 2, 10, 4))

    for yy in [y + 9, y + 11]:
        pygame.draw.line(lienzo, TINTA, (x - 15, yy), (x - 4, yy))
        pygame.draw.line(lienzo, TINTA, (x + 4, yy), (x + 15, yy))

    pygame.draw.circle(lienzo, personajes.FORCIBLE_PIEL, (x - 18, y + 10), 4)                                       # manos
    pygame.draw.circle(lienzo, personajes.FORCIBLE_PIEL, (x + 18, y + 10), 4)


def crear_fijo() -> pygame.Surface:

    lienzo = pygame.Surface((ANCHO, ALTO))

    sala_actrices.dibujar_sala(lienzo)

    for x, y, ancho, alto in RECORTES_PISO:
        dibujar_recorte(lienzo, x, y, ancho, alto)

    # CADA COSA EN SU CAPA, PARA PEGARLA CON CONTORNO (COMO SPRITE DE RPG)
    capa = capa_vacia()
    personajes.dibujar_spink(capa, X_SPINK, "dar")
    pegar_con_contorno(lienzo, capa)

    capa = capa_vacia()
    personajes.dibujar_forcible(capa, X_FORCIBLE, "normal", False)
    dibujar_album(capa)
    pegar_con_contorno(lienzo, capa)

    sala_actrices.dibujar_coraline(lienzo, X_CORALINE)
    sala_actrices.dibujar_luces(lienzo)
    orillas_oscuras(lienzo)

    return lienzo


# --------------------------------------------------
# LO QUE SE MUEVE
# --------------------------------------------------

def dibujar_recorte_en_mano(lienzo: pygame.Surface, tiempo: float) -> None:

    """LA SENORITA SPINK AGITA UN RECORTE, MUY EMOCIONADA."""

    mano = personajes.mano_spink(X_SPINK, "dar")
    dy = int(math.sin(tiempo * 6) * 1.5)

    dibujar_recorte(lienzo, mano[0] - 16, mano[1] - 22 + dy, 14, 18)
    pygame.draw.circle(lienzo, personajes.SPINK_PIEL, (mano[0] - 2, mano[1] - 6 + dy), 3)


def dibujar_burbuja(lienzo: pygame.Surface, tiempo: float) -> None:

    """CORALINE INTENTA HABLAR: UNA BURBUJA CON UN SIGNO DE ADMIRACION QUE NADIE MIRA.
    APARECE 2.5 SEGUNDOS DE CADA 5."""

    if tiempo % 5 > 2.5:
        return

    x, y = X_CORALINE + 10, Y_PISO - 116

    pygame.draw.ellipse(lienzo, COLOR_CONTORNO, (x - 1, y - 1, 22, 18))
    pygame.draw.ellipse(lienzo, (246, 242, 236), (x, y, 20, 16))
    pygame.draw.polygon(lienzo, (246, 242, 236), [(x + 4, y + 13), (x + 9, y + 14), (x + 2, y + 20)])
    pygame.draw.line(lienzo, COLOR_CONTORNO, (x + 2, y + 20), (x + 4, y + 14))

    pygame.draw.rect(lienzo, (190, 50, 60), (x + 9, y + 3, 2, 7))
    pygame.draw.rect(lienzo, (190, 50, 60), (x + 9, y + 11, 2, 2))


def dibujar(ventana: pygame.Surface) -> None:

    """DIBUJA LA ESCENA COMPLETA EN LA VENTANA DEL JUEGO."""

    if "fijo" not in CAPAS:
        CAPAS["fijo"] = crear_fijo()

    tiempo = pygame.time.get_ticks() / 1000

    lienzo = CAPAS["fijo"].copy()

    personajes.dibujar_ojos_spink(lienzo, X_SPINK, tiempo, False)
    personajes.dibujar_ojos_forcible(lienzo, X_FORCIBLE, tiempo, "taza", False)
    dibujar_recorte_en_mano(lienzo, tiempo)
    personajes.dibujar_perro(lienzo, X_PERRO, Y_PISO + 26, tiempo, 0)
    dibujar_burbuja(lienzo, tiempo)

    mostrar(ventana, lienzo)
