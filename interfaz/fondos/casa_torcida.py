"""FONDO DIBUJADO CON CODIGO: LA OTRA CASA, COMO UNA IMITACION TORCIDA DE SI MISMA.

Es la casa rosa de exterior_gato.py (cap. 4, de Wendy), pero se le esta
acabando el truco: los colores estan medio apagados y toda la casa ondula
como si fuera un dibujo en el agua. La otra madre espera en el pasto con los
brazos cruzados y le ofrece "una pequena pista" con voz melosa: de su burbuja
salen corazoncitos y una flechita. Coraline la mira desde el camino. Se usa
en cap09_n01 y en su rama cap09_r01.

Lo que se mueve: la casa que ondula, los corazoncitos que suben y se
deshacen, la burbuja de la pista y los botones de la otra madre.
"""

import math

import pygame

from interfaz.fondos.pintura import ANCHO, ALTO
from interfaz.fondos.pintura import capa_vacia, pegar_con_contorno, COLOR_CONTORNO
from interfaz.fondos.pintura import mezclar, orillas_oscuras, mostrar
from interfaz.fondos import personajes
from interfaz.fondos import exterior_gato

X_CORALINE = 466
X_MADRE = 566
BURBUJA = pygame.Rect(588, 92, 40, 28)

CAPAS = {}


# --------------------------------------------------
# PARTE FIJA
# --------------------------------------------------

def crear_capas() -> None:

    """LA CASA SIN EL MURO, MEDIO DESTENIDA (SE ONDULA CADA CUADRO), Y LAS ORILLAS OSCURAS APARTE."""

    casa = pygame.Surface((ANCHO, ALTO))
    exterior_gato.dibujar_cielo(casa)
    exterior_gato.dibujar_arboles(casa)
    exterior_gato.dibujar_terreno(casa)
    exterior_gato.dibujar_casa(casa)
    exterior_gato.dibujar_marquesina(casa)

    # SE LE VA EL COLOR: MITAD COLOR, MITAD GRIS
    gris = pygame.transform.grayscale(casa)
    gris.set_alpha(120)
    casa.blit(gris, (0, 0))
    CAPAS["casa"] = casa

    orillas = pygame.Surface((ANCHO, ALTO), pygame.SRCALPHA)
    orillas_oscuras(orillas)
    CAPAS["orillas"] = orillas

    # LOS PERSONAJES NO SE ONDULAN: VAN EN SU PROPIA CAPA
    capa = capa_vacia()
    personajes.dibujar_otra_madre(capa, X_MADRE, "brazos_cruzados")
    figuras = capa_vacia()
    pegar_con_contorno(figuras, capa)
    personajes.dibujar_coraline_chica(figuras, X_CORALINE, 300, True)
    CAPAS["figuras"] = figuras


# --------------------------------------------------
# LO QUE SE MUEVE
# --------------------------------------------------

def dibujar_casa_ondulada(lienzo: pygame.Surface, tiempo: float) -> None:

    """PEGA LA CASA EN TIRAS DE 2 PIXELES, CADA UNA UN POCO MAS ARRIBA O ABAJO (ONDULA COMO EN EL AGUA)."""

    casa = CAPAS["casa"]

    for x in range(0, ANCHO, 2):
        sube = int(math.sin(x * 0.035 + tiempo * 1.4) * 3 + math.sin(x * 0.011 - tiempo * 0.7) * 2)
        lienzo.blit(casa, (x, sube), (x, 0, 2, ALTO))


def dibujar_corazones(lienzo: pygame.Surface, tiempo: float) -> None:

    """CORAZONCITOS ROSAS QUE SUBEN DE LA OTRA MADRE (LA VOZ MELOSA) Y SE PONEN GRISES AL DESHACERSE."""

    for i in range(5):

        fase = (tiempo * 0.4 + i / 5) % 1
        x = X_MADRE - 26 + (i * 13) % 50 + int(math.sin(tiempo * 2 + i) * 4)
        y = 150 - int(fase * 90)
        color = mezclar((240, 120, 170), (120, 120, 126), fase)

        if fase > 0.85:
            lienzo.set_at((x, y), color)                                    # ya casi no queda nada
            continue

        pygame.draw.circle(lienzo, color, (x - 2, y), 2)
        pygame.draw.circle(lienzo, color, (x + 2, y), 2)
        pygame.draw.polygon(lienzo, color, [(x - 4, y + 1), (x + 4, y + 1), (x, y + 5)])


def dibujar_burbuja(lienzo: pygame.Surface, tiempo: float) -> None:

    """BURBUJA ROSA CON UNA FLECHITA QUE APUNTA A UN LADO Y A OTRO: "TE DOY UNA PISTA"."""

    pygame.draw.ellipse(lienzo, COLOR_CONTORNO, BURBUJA.inflate(2, 2))
    pygame.draw.ellipse(lienzo, (250, 222, 234), BURBUJA)
    pygame.draw.polygon(lienzo, (250, 222, 234), [(BURBUJA.x + 4, BURBUJA.bottom - 6),
                                                  (BURBUJA.x + 12, BURBUJA.bottom - 3),
                                                  (BURBUJA.x - 6, BURBUJA.bottom + 10)])

    # LA FLECHITA GIRA DESPACIO: LA PISTA NO LLEVA A NINGUN LADO
    angulo = tiempo * 1.5
    x, y = BURBUJA.center
    punta = (x + int(math.cos(angulo) * 9), y + int(math.sin(angulo) * 7))
    cola = (x - int(math.cos(angulo) * 9), y - int(math.sin(angulo) * 7))

    pygame.draw.line(lienzo, (190, 60, 110), cola, punta, 2)
    pygame.draw.circle(lienzo, (190, 60, 110), punta, 2)
    pygame.draw.circle(lienzo, (250, 222, 234), cola, 1)


def dibujar(ventana: pygame.Surface) -> None:

    """DIBUJA LA ESCENA COMPLETA EN LA VENTANA DEL JUEGO."""

    if "casa" not in CAPAS:
        crear_capas()

    tiempo = pygame.time.get_ticks() / 1000

    lienzo = pygame.Surface((ANCHO, ALTO))
    lienzo.fill((40, 30, 50))
    dibujar_casa_ondulada(lienzo, tiempo)
    lienzo.blit(CAPAS["orillas"], (0, 0))
    lienzo.blit(CAPAS["figuras"], (0, 0))

    personajes.dibujar_botones(lienzo, personajes.ojos_otra_madre(X_MADRE), tiempo, False, True)
    dibujar_corazones(lienzo, tiempo)
    dibujar_burbuja(lienzo, tiempo)

    mostrar(ventana, lienzo)
