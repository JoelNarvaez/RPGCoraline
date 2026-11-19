"""FONDO DIBUJADO CON CODIGO: CORALINE CENA SOLA EN LA CASA VACIA.

Sus papas no han vuelto. Es de noche y Coraline, en pijama, cena pan tostado
y pizza congelada en la barra de la cocina, con todas las luces prendidas.
Es la misma cocina de cocina_sola.py (cap03_n02), pero de noche y sin la
llave en el clavo (Coraline ya la tiene). La pijama es la de pasillo_noche.py.
Se usa en cap05_n01.

Lo que se mueve: el segundero del reloj, el foco que titila de vez en cuando
y el vapor de la pizza recien calentada.
"""

import math

import pygame

from interfaz.fondos.pintura import ANCHO, ALTO
from interfaz.fondos.pintura import mezclar, degradado, brillo, orillas_oscuras, mostrar
from interfaz.fondos import cocina_sola
from interfaz.fondos import pasillo_noche

Y_PISO = cocina_sola.Y_PISO

X_CORALINE = 470
VENTANA = pygame.Rect(408, 108, 46, 62)       # el vidrio de la ventana de cocina_sola
FOCO = (575, 34)                               # foco del techo, encima de la barra
PLATO = (586, 228)                             # centro del plato sobre la barra

CAPAS = {}


# --------------------------------------------------
# PARTE FIJA
# --------------------------------------------------

def dibujar_ventana_noche(lienzo: pygame.Surface) -> None:

    """EL VIDRIO DE LA VENTANA AHORA ES NOCHE: CIELO AZUL OSCURO, LUNA Y ESTRELLAS."""

    degradado(lienzo, VENTANA, (10, 14, 34), (30, 36, 70), 5)

    pygame.draw.circle(lienzo, (236, 232, 206), (VENTANA.x + 33, VENTANA.y + 12), 5)
    pygame.draw.circle(lienzo, (30, 36, 70), (VENTANA.x + 35, VENTANA.y + 10), 4)       # luna menguante

    for dx, dy in [(6, 8), (14, 22), (38, 36), (8, 48), (28, 52), (20, 6)]:
        lienzo.set_at((VENTANA.x + dx, VENTANA.y + dy), (220, 220, 250))

    # EL MARCO Y LA CRUZ DE LA VENTANA SE VUELVEN A PINTAR ENCIMA
    pygame.draw.line(lienzo, (90, 80, 66), (431, 108), (431, 170), 2)
    pygame.draw.line(lienzo, (90, 80, 66), (408, 139), (454, 139), 2)


def oscurecer(lienzo: pygame.Surface) -> None:

    """TINTE AZUL DE NOCHE SOBRE TODA LA COCINA (LA LUZ DEL FOCO SE PONE DESPUES)."""

    capa = pygame.Surface((ANCHO, ALTO), pygame.SRCALPHA)
    capa.fill((10, 14, 44, 150))
    lienzo.blit(capa, (0, 0))


def dibujar_lampara(lienzo: pygame.Surface) -> None:

    """LAMPARA DE TECHO COLGADA DE UN CABLE, CON SU PANTALLA DE LAMINA."""

    x, y = FOCO

    pygame.draw.line(lienzo, (40, 36, 40), (x, 0), (x, y - 8))
    pygame.draw.polygon(lienzo, (70, 90, 84), [(x - 6, y - 9), (x + 6, y - 9), (x + 14, y + 1), (x - 14, y + 1)])
    pygame.draw.line(lienzo, (110, 130, 120), (x - 5, y - 8), (x - 12, y))
    pygame.draw.ellipse(lienzo, (255, 236, 180), (x - 5, y - 1, 10, 6))


def dibujar_cena(lienzo: pygame.Surface) -> None:

    """SOBRE LA BARRA: PLATO CON UNA REBANADA DE PIZZA, PAN TOSTADO Y UN VASO DE LECHE."""

    x, y = PLATO

    pygame.draw.ellipse(lienzo, (236, 234, 226), (x - 16, y - 1, 32, 7))
    pygame.draw.ellipse(lienzo, (200, 198, 190), (x - 12, y, 24, 4))

    # REBANADA DE PIZZA (TRIANGULO CON ORILLA DORADA Y PEPERONI)
    pygame.draw.polygon(lienzo, (236, 190, 90), [(x - 12, y - 1), (x + 2, y - 1), (x - 6, y - 6)])
    pygame.draw.line(lienzo, (190, 120, 50), (x - 12, y - 1), (x + 2, y - 1), 2)
    lienzo.set_at((x - 6, y - 3), (190, 50, 40))
    lienzo.set_at((x - 3, y - 2), (190, 50, 40))

    # PAN TOSTADO
    pygame.draw.rect(lienzo, (176, 112, 54), (x + 4, y - 6, 9, 7), border_top_left_radius=3, border_top_right_radius=3)
    pygame.draw.rect(lienzo, (222, 170, 96), (x + 5, y - 5, 7, 5))

    # VASO DE LECHE
    pygame.draw.rect(lienzo, (230, 236, 240), (x + 20, y - 10, 7, 12))
    pygame.draw.rect(lienzo, (250, 250, 246), (x + 21, y - 6, 5, 7))
    pygame.draw.line(lienzo, (255, 255, 255), (x + 21, y - 9), (x + 21, y - 7))


def dibujar_coraline(lienzo: pygame.Surface) -> None:

    """CORALINE EN PIJAMA, PARADA FRENTE A LA BARRA, MIRANDO SU CENA."""

    sprite = pasillo_noche.sprite_pijama()

    sombra = pygame.Surface((sprite.get_width() + 6, 6), pygame.SRCALPHA)
    pygame.draw.ellipse(sombra, (0, 0, 0, 120), sombra.get_rect())
    lienzo.blit(sombra, (X_CORALINE - sombra.get_width() // 2, Y_PISO - 4))

    lienzo.blit(sprite, (X_CORALINE - sprite.get_width() // 2, Y_PISO - sprite.get_height()))


def crear_fijo() -> pygame.Surface:

    lienzo = pygame.Surface((ANCHO, ALTO))

    cocina_sola.dibujar_cocina(lienzo)
    dibujar_ventana_noche(lienzo)
    oscurecer(lienzo)

    # LA VENTANA BRILLA UN POCO CON LA LUNA, POR ENCIMA DEL TINTE
    brillo(lienzo, VENTANA.center, 40, (150, 170, 230), 40)

    dibujar_lampara(lienzo)
    dibujar_cena(lienzo)
    dibujar_coraline(lienzo)

    orillas_oscuras(lienzo)

    return lienzo


def crear_luz() -> pygame.Surface:

    """CONO DE LUZ CALIDA DEL FOCO (SE GUARDA PORQUE SE DIBUJA EN CADA CUADRO)."""

    capa = pygame.Surface((ANCHO, ALTO), pygame.SRCALPHA)
    brillo(capa, (FOCO[0], FOCO[1] + 70), 180, (255, 206, 140), 95)
    brillo(capa, (FOCO[0], FOCO[1] + 4), 40, (255, 240, 200), 120)

    cono = pygame.Surface((ANCHO, ALTO), pygame.SRCALPHA)
    x, y = FOCO
    pygame.draw.polygon(cono, (255, 226, 170, 44), [(x - 12, y + 2), (x + 12, y + 2), (x + 70, Y_PISO), (x - 70, Y_PISO)])
    capa.blit(cono, (0, 0))

    return capa


# --------------------------------------------------
# LO QUE SE MUEVE
# --------------------------------------------------

def foco_encendido(tiempo: float) -> bool:

    """EL FOCO TITILA DOS VECES CADA 7 SEGUNDOS, COMO SI LA CASA SUSPIRARA."""

    fase = tiempo % 7

    return not (5.0 < fase < 5.08 or 5.2 < fase < 5.26)


def dibujar_vapor(lienzo: pygame.Surface, tiempo: float) -> None:

    """DOS HILITOS DE VAPOR QUE SUBEN DE LA PIZZA Y SE DESHACEN."""

    for i in range(2):

        fase = (tiempo * 0.5 + i * 0.5) % 1
        x0 = PLATO[0] - 8 + i * 4

        for paso in range(5):
            y = PLATO[1] - 8 - int(fase * 18) - paso * 3
            x = x0 + int(math.sin(tiempo * 2 + paso * 0.8 + i) * 2)
            if y > PLATO[1] - 30:
                lienzo.set_at((x, y), mezclar((236, 232, 220), (120, 120, 130), fase))


def dibujar(ventana: pygame.Surface) -> None:

    """DIBUJA LA ESCENA COMPLETA EN LA VENTANA DEL JUEGO."""

    if "fijo" not in CAPAS:
        CAPAS["fijo"] = crear_fijo()
        CAPAS["luz"] = crear_luz()

    tiempo = pygame.time.get_ticks() / 1000

    lienzo = CAPAS["fijo"].copy()

    if foco_encendido(tiempo):
        lienzo.blit(CAPAS["luz"], (0, 0))

    cocina_sola.dibujar_reloj(lienzo, tiempo)
    dibujar_vapor(lienzo, tiempo)

    mostrar(ventana, lienzo)
