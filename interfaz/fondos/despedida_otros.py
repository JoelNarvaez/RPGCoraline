"""FONDO DIBUJADO CON CODIGO: LOS OTROS PADRES DESPIDEN A CORALINE.

Coraline dice que quiere salir a explorar. En la entrada del otro
departamento, los otros padres la despiden con sonrisas identicas, moviendo
la mano despacio y al mismo tiempo. Ella va hacia la puerta, que da a un
afuera muy brillante. Se usa en cap03_n06.

Lo que se mueve: las manos de los dos (iguales, como espejo), el brillo de
sus botones y la luz que entra por la puerta.
"""

import pygame

from interfaz.fondos.pintura import ANCHO, ALTO
from interfaz.fondos.pintura import capa_vacia, pegar_con_contorno
from interfaz.fondos.pintura import mezclar, degradado, brillo, orillas_oscuras, mostrar
from interfaz.fondos import personajes
from interfaz.fondos import sala_actrices

Y_PISO = 300

X_CORALINE = 472
X_MADRE = 556
X_PADRE = 606
PUERTA = pygame.Rect(410, 120, 44, Y_PISO - 120)

COLOR_PARED = (150, 110, 150)

CAPAS = {}


def dibujar_entrada(lienzo: pygame.Surface) -> None:

    """PARED LILA CON MOLDURAS, PERCHERO, ESPEJO Y LA PUERTA ABIERTA AL JARDIN."""

    degradado(lienzo, pygame.Rect(0, 0, ANCHO, Y_PISO), (90, 60, 96), COLOR_PARED, 14)

    for x in range(470, ANCHO, 50):
        pygame.draw.rect(lienzo, mezclar(COLOR_PARED, (255, 255, 255), 0.15), (x, 60, 40, 140), 1)

    pygame.draw.rect(lienzo, (110, 76, 110), (0, 220, ANCHO, 4))

    # PUERTA ABIERTA: AFUERA SE VE EL JARDIN MUY BRILLANTE
    pygame.draw.rect(lienzo, (70, 44, 40), PUERTA.inflate(8, 6).move(0, -3))
    degradado(lienzo, PUERTA, (230, 240, 210), (150, 200, 120), 6)
    pygame.draw.ellipse(lienzo, (110, 170, 90), (PUERTA.x - 6, PUERTA.bottom - 40, 30, 30))
    pygame.draw.polygon(lienzo, (120, 76, 60), [(PUERTA.right, PUERTA.y), (PUERTA.right + 16, PUERTA.y + 8),
                                                (PUERTA.right + 16, Y_PISO + 6), (PUERTA.right, Y_PISO)])

    # PERCHERO CON UN ABRIGO Y UN PARAGUAS
    pygame.draw.line(lienzo, (70, 44, 40), (640 - 8, 70), (640 - 8, Y_PISO), 3)
    pygame.draw.polygon(lienzo, (60, 90, 120), [(626, 80), (640, 80), (640, 150), (622, 150)])

    # ESPEJO REDONDO (NO REFLEJA NADA)
    pygame.draw.ellipse(lienzo, (190, 150, 80), (500, 66, 34, 44))
    pygame.draw.ellipse(lienzo, (60, 66, 80), (503, 69, 28, 38))

    # PISO DE MADERA
    degradado(lienzo, pygame.Rect(0, Y_PISO, ANCHO, ALTO - Y_PISO), (110, 74, 54), (60, 40, 30), 4)

    for x in range(0, ANCHO, 24):
        pygame.draw.line(lienzo, (80, 52, 40), (x, Y_PISO), (x - 8, ALTO))


def crear_fijo() -> pygame.Surface:

    lienzo = pygame.Surface((ANCHO, ALTO))

    dibujar_entrada(lienzo)
    capa = capa_vacia()
    personajes.dibujar_otro_padre(capa, X_PADRE, "despedir")
    pegar_con_contorno(lienzo, capa)

    capa = capa_vacia()
    personajes.dibujar_otra_madre(capa, X_MADRE, "despedir")
    pegar_con_contorno(lienzo, capa)
    sala_actrices.dibujar_coraline(lienzo, X_CORALINE, False)

    brillo(lienzo, PUERTA.center, 100, (240, 250, 220), 60)
    orillas_oscuras(lienzo)

    return lienzo


def dibujar(ventana: pygame.Surface) -> None:

    """DIBUJA LA ESCENA COMPLETA EN LA VENTANA DEL JUEGO."""

    if "fijo" not in CAPAS:
        CAPAS["fijo"] = crear_fijo()

    tiempo = pygame.time.get_ticks() / 1000

    lienzo = CAPAS["fijo"].copy()

    personajes.dibujar_brazo_saludo(lienzo, X_PADRE, "padre", tiempo)
    personajes.dibujar_brazo_saludo(lienzo, X_MADRE, "madre", tiempo)
    personajes.dibujar_botones(lienzo, personajes.ojos_otro_padre(X_PADRE), tiempo, True)
    personajes.dibujar_botones(lienzo, personajes.ojos_otra_madre(X_MADRE), tiempo, False, True)

    mostrar(ventana, lienzo)
