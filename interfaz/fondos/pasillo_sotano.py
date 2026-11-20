"""FONDO DIBUJADO CON CODIGO: EL PASILLO VACIO Y LA PUERTA DEL SOTANO.

El pasillo lila del otro departamento (el de espejo_otra_madre.py, cap. 6),
pero ya no hay nadie: la puerta del bano esta abierta y adentro solo hay
oscuridad. Coraline silba para darse valor y las notitas le salen chuecas. Al
fondo, la puerta del sotano esta entreabierta: se ven los primeros escalones
bajando a lo negro y sale aire frio. Se usa en cap09_n02 y en su rama
cap09_r02.

Lo que se mueve: las notitas del silbido que suben temblando, la lampara que
falla, la puerta del sotano que rechina un poquito, el aire frio y, de vez en
cuando, dos botoncitos que brillan en la oscuridad de abajo.
"""

import math

import pygame

from interfaz.fondos.pintura import ANCHO, ALTO
from interfaz.fondos.pintura import capa_vacia, pegar_con_contorno, COLOR_CONTORNO
from interfaz.fondos.pintura import mezclar, degradado, brillo, orillas_oscuras, mostrar
from interfaz.fondos import sala_actrices
from interfaz.fondos import espejo_otra_madre

Y_PISO = espejo_otra_madre.Y_PISO

X_CORALINE = 444
BANO = pygame.Rect(470, 150, 40, Y_PISO - 150)
SOTANO = pygame.Rect(572, 136, 46, Y_PISO - 136)       # el hueco de la puerta del sotano
LAMPARA = (538, 106)

COLOR_MADERA = (90, 60, 50)

CAPAS = {}


# --------------------------------------------------
# PARTE FIJA
# --------------------------------------------------

def dibujar_bano(lienzo: pygame.Surface) -> None:

    """LA PUERTA DEL BANO ABIERTA: ADENTRO OSCURO, CON LA ORILLA DE UNA TINA VACIA."""

    pygame.draw.rect(lienzo, COLOR_MADERA, BANO.inflate(6, 4).move(0, -2))
    degradado(lienzo, BANO, (20, 18, 26), (36, 34, 44), 4)
    pygame.draw.rect(lienzo, (70, 70, 80), (BANO.x + 4, Y_PISO - 26, BANO.width - 8, 4))           # orilla de la tina
    pygame.draw.polygon(lienzo, (120, 84, 70), [(BANO.right, BANO.y), (BANO.right + 10, BANO.y + 6),
                                                (BANO.right + 10, Y_PISO + 4), (BANO.right, Y_PISO)])


def dibujar_escalera(lienzo: pygame.Surface) -> None:

    """POR EL HUECO DE LA PUERTA SE VEN LOS PRIMEROS ESCALONES BAJANDO A LO NEGRO."""

    degradado(lienzo, SOTANO, (6, 6, 10), (16, 14, 20), 5)

    for i in range(5):
        ancho = SOTANO.width - 8 - i * 6
        color = mezclar((70, 54, 44), (8, 8, 12), i / 5)
        pygame.draw.rect(lienzo, color, (SOTANO.x + 4 + i * 3, Y_PISO - 40 + i * 9, ancho, 3))


def dibujar_marco_sotano(capa: pygame.Surface) -> None:

    """EL MARCO Y LA PUERTA DEL SOTANO (LA HOJA SE DIBUJA APARTE PORQUE SE MUEVE)."""

    pygame.draw.rect(capa, COLOR_MADERA, (SOTANO.x - 4, SOTANO.y - 6, 4, SOTANO.height + 6))
    pygame.draw.rect(capa, COLOR_MADERA, (SOTANO.right, SOTANO.y - 6, 4, SOTANO.height + 6))
    pygame.draw.rect(capa, COLOR_MADERA, (SOTANO.x - 4, SOTANO.y - 6, SOTANO.width + 8, 6))


def crear_fijo() -> pygame.Surface:

    lienzo = pygame.Surface((ANCHO, ALTO))

    espejo_otra_madre.dibujar_pasillo(lienzo)

    # TODO MAS APAGADO QUE EN EL CAP. 6: YA NO HAY NADIE
    tinte = pygame.Surface((ANCHO, ALTO))
    tinte.fill((150, 140, 160))
    lienzo.blit(tinte, (0, 0), special_flags=pygame.BLEND_MULT)

    dibujar_bano(lienzo)
    dibujar_escalera(lienzo)

    capa = capa_vacia()
    dibujar_marco_sotano(capa)
    pegar_con_contorno(lienzo, capa)

    sala_actrices.dibujar_coraline(lienzo, X_CORALINE, True)

    orillas_oscuras(lienzo)

    return lienzo


# --------------------------------------------------
# LO QUE SE MUEVE
# --------------------------------------------------

def dibujar_luz(lienzo: pygame.Surface, tiempo: float) -> None:

    """LA LAMPARA DE PARED FALLA: A VECES SE APAGA UN INSTANTE."""

    falla = math.sin(tiempo * 11) + math.sin(tiempo * 4.3) > 1.5

    if falla:
        return

    if "luz" not in CAPAS:
        luz = pygame.Surface((ANCHO, ALTO), pygame.SRCALPHA)
        brillo(luz, LAMPARA, 80, (255, 220, 170), 60)
        CAPAS["luz"] = luz

    lienzo.blit(CAPAS["luz"], (0, 0))
    pygame.draw.polygon(lienzo, (255, 236, 190), [(LAMPARA[0] - 8, 100), (LAMPARA[0] + 8, 100),
                                                  (LAMPARA[0] + 4, 112), (LAMPARA[0] - 4, 112)])


def dibujar_puerta(lienzo: pygame.Surface, tiempo: float) -> None:

    """LA HOJA DE LA PUERTA DEL SOTANO, ENTREABIERTA HACIA EL PASILLO; SE MECE TANTITO (RECHINA)."""

    abre = 18 + int(math.sin(tiempo * 0.9) * 3)
    bisagra = SOTANO.x - 1

    puntas = [(bisagra, SOTANO.y), (bisagra - abre, SOTANO.y + 6), (bisagra - abre, SOTANO.bottom + 2), (bisagra, SOTANO.bottom)]
    pygame.draw.polygon(lienzo, COLOR_CONTORNO, [(px - 1, py) for px, py in puntas])
    pygame.draw.polygon(lienzo, (110, 76, 60), puntas)
    pygame.draw.line(lienzo, (80, 54, 44), (bisagra - abre // 2, SOTANO.y + 10), (bisagra - abre // 2, SOTANO.bottom - 6))
    pygame.draw.circle(lienzo, (200, 170, 90), (bisagra - abre + 3, SOTANO.centery + 10), 2)


def dibujar_notas(lienzo: pygame.Surface, tiempo: float) -> None:

    """NOTITAS DEL SILBIDO: SALEN DE CORALINE, SUBEN TEMBLANDO Y SE APAGAN ANTES DE LLEGAR AL SOTANO."""

    for i in range(4):

        fase = (tiempo * 0.45 + i / 4) % 1
        x = X_CORALINE + 14 + int(fase * 60)
        y = Y_PISO - 74 - int(fase * 40) + int(math.sin(tiempo * 9 + i * 2) * 2)
        color = mezclar((250, 240, 200), (60, 50, 70), fase)

        pygame.draw.line(lienzo, color, (x + 3, y - 7), (x + 3, y))
        pygame.draw.ellipse(lienzo, color, (x, y - 1, 4, 3))
        if i % 2 == 0:
            pygame.draw.line(lienzo, color, (x + 3, y - 7), (x + 6, y - 5))


def dibujar_aire_y_botones(lienzo: pygame.Surface, tiempo: float) -> None:

    """AIRE FRIO QUE SALE DEL SOTANO Y, CADA 7 SEGUNDOS, DOS BOTONCITOS QUE BRILLAN ALLA ABAJO."""

    capa = pygame.Surface((ANCHO, ALTO), pygame.SRCALPHA)

    for i in range(4):
        fase = (tiempo * 0.3 + i / 4) % 1
        x = SOTANO.x - int(fase * 80)
        y = Y_PISO - 4 - i * 4 + int(math.sin(tiempo * 2 + i) * 2)
        pygame.draw.line(capa, (180, 200, 220, int(70 * (1 - fase))), (x - 8, y), (x + 8, y - 1))

    lienzo.blit(capa, (0, 0))

    if tiempo % 7 < 0.6:
        for dx in [-3, 3]:
            lienzo.set_at((SOTANO.centerx + dx + 4, Y_PISO - 8), (230, 230, 240))


def dibujar(ventana: pygame.Surface) -> None:

    """DIBUJA LA ESCENA COMPLETA EN LA VENTANA DEL JUEGO."""

    if "fijo" not in CAPAS:
        CAPAS["fijo"] = crear_fijo()

    tiempo = pygame.time.get_ticks() / 1000

    lienzo = CAPAS["fijo"].copy()

    dibujar_luz(lienzo, tiempo)
    dibujar_aire_y_botones(lienzo, tiempo)
    dibujar_puerta(lienzo, tiempo)
    dibujar_notas(lienzo, tiempo)

    mostrar(ventana, lienzo)
