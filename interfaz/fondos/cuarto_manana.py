"""FONDO DIBUJADO CON CODIGO: CORALINE DESPIERTA EN EL OTRO CUARTO.

Es el mismo cuarto azul con estrellas de otro_cuarto.py (cap03_n05), pero de
manana: el sol entra por la ventana y cae sobre la cama deshecha. El armario
esta abierto y tiene la ropa maravillosa: pantalones de terciopelo negro, un
sueter gris con estrellitas y unas botas naranjas brillantes. Coraline, en
pijama (la de pasillo_noche.py), se queda mirandolas. Se usa en cap06_n01 y
en su rama cap06_r01.

Lo que se mueve: polvo en los rayos de sol, las estrellitas del sueter que
brillan, el destello de las botas y el dinosaurio de cuerda de otro_cuarto.py.
"""

import math

import pygame

from interfaz.fondos.pintura import ANCHO, ALTO
from interfaz.fondos.pintura import capa_vacia, pegar_con_contorno
from interfaz.fondos.pintura import mezclar, degradado, brillo, orillas_oscuras, mostrar
from interfaz.fondos import otro_cuarto
from interfaz.fondos import pasillo_noche

Y_PISO = 300

X_CORALINE = 514
VENTANA = pygame.Rect(418, 64, 56, 78)
CAMA = pygame.Rect(410, 258, 84, 42)
ARMARIO = pygame.Rect(548, 92, 78, Y_PISO - 92)

COLOR_PARED = (96, 124, 190)
COLOR_MUEBLE = (150, 96, 64)
COLOR_MUEBLE_SOMBRA = (104, 64, 46)
COLOR_SOL = (255, 236, 170)

# ESTRELLITAS DEL SUETER (x, y DENTRO DEL ARMARIO)
ESTRELLAS_SUETER = [(588, 126), (600, 132), (594, 142), (606, 146), (584, 150), (612, 128)]
BOTAS = [(574, 284), (594, 284)]

CAPAS = {}


# --------------------------------------------------
# PARTE FIJA
# --------------------------------------------------

def dibujar_pared(lienzo: pygame.Surface) -> None:

    """PARED AZUL CLARO DE MANANA CON EL MISMO PAPEL DE ESTRELLAS Y EL PISO DE MADERA."""

    degradado(lienzo, pygame.Rect(0, 0, ANCHO, Y_PISO), (66, 84, 150), COLOR_PARED, 14)

    for y in range(16, 260, 26):
        for x in range(6 + (y // 26 % 2) * 13, ANCHO, 26):
            pygame.draw.line(lienzo, (244, 220, 130), (x - 2, y), (x + 2, y))
            pygame.draw.line(lienzo, (244, 220, 130), (x, y - 2), (x, y + 2))

    degradado(lienzo, pygame.Rect(0, Y_PISO, ANCHO, ALTO - Y_PISO), (140, 98, 70), (96, 66, 50), 4)

    for x in range(0, ANCHO, 24):
        pygame.draw.line(lienzo, (110, 76, 56), (x, Y_PISO), (x - 8, ALTO))


def dibujar_ventana(lienzo: pygame.Surface) -> None:

    """VENTANA CON CIELO DE MANANA, CORTINAS AMARILLAS RECOGIDAS Y EL RAYO DE SOL HASTA EL PISO."""

    pygame.draw.rect(lienzo, COLOR_MUEBLE, VENTANA.inflate(8, 8))
    degradado(lienzo, VENTANA, (170, 214, 250), (236, 240, 220), 5)
    pygame.draw.circle(lienzo, (255, 246, 200), (VENTANA.right - 14, VENTANA.y + 16), 8)
    pygame.draw.line(lienzo, COLOR_MUEBLE, (VENTANA.centerx, VENTANA.y), (VENTANA.centerx, VENTANA.bottom), 3)
    pygame.draw.line(lienzo, COLOR_MUEBLE, (VENTANA.x, VENTANA.centery), (VENTANA.right, VENTANA.centery), 3)

    for lado in [-1, 1]:
        x = VENTANA.x - 10 if lado < 0 else VENTANA.right + 2
        pygame.draw.polygon(lienzo, (236, 196, 90), [(x, VENTANA.y - 6), (x + 8, VENTANA.y - 6),
                                                     (x + 4 - lado * 2, VENTANA.bottom + 14), (x + 2, VENTANA.bottom + 14)])
        pygame.draw.line(lienzo, (196, 150, 60), (x + 4, VENTANA.y - 4), (x + 3, VENTANA.bottom + 12))

    pygame.draw.rect(lienzo, COLOR_MUEBLE_SOMBRA, (VENTANA.x - 12, VENTANA.y - 8, VENTANA.width + 24, 3))

    # EL RAYO DE SOL: UNA FRANJA CLARA QUE BAJA EN DIAGONAL HASTA LA CAMA Y EL PISO
    capa = pygame.Surface((ANCHO, ALTO), pygame.SRCALPHA)
    pygame.draw.polygon(capa, (*COLOR_SOL, 46), [VENTANA.topleft, VENTANA.topright,
                                                (VENTANA.right + 80, Y_PISO + 20), (VENTANA.x + 30, Y_PISO + 20)])
    lienzo.blit(capa, (0, 0))


def dibujar_cama(capa: pygame.Surface) -> None:

    """CAMA DESHECHA CON COLCHA DE CUADROS DE COLORES Y LA ALMOHADA AL REVES."""

    # CABECERA Y PATAS
    pygame.draw.rect(capa, COLOR_MUEBLE, (CAMA.x, CAMA.y - 30, 8, CAMA.height + 30))
    pygame.draw.circle(capa, COLOR_MUEBLE, (CAMA.x + 4, CAMA.y - 32), 5)
    pygame.draw.rect(capa, COLOR_MUEBLE, (CAMA.right - 6, CAMA.y - 8, 6, CAMA.height + 8))

    # COLCHON Y ALMOHADA
    pygame.draw.rect(capa, (236, 232, 222), (CAMA.x + 8, CAMA.y, CAMA.width - 14, 16))
    pygame.draw.ellipse(capa, (250, 248, 240), (CAMA.x + 10, CAMA.y - 10, 26, 14))

    # COLCHA DE CUADROS, ARRUGADA Y CAYENDO DE UN LADO
    colores = [(220, 90, 90), (240, 200, 90), (90, 170, 120), (90, 130, 210)]

    for i in range(6):
        for j in range(2):
            color = colores[(i + j) % 4]
            pygame.draw.rect(capa, color, (CAMA.x + 30 + i * 9, CAMA.y + 2 + j * 9 + (i % 2), 9, 9))

    pygame.draw.polygon(capa, (220, 90, 90), [(CAMA.right - 10, CAMA.y + 12), (CAMA.right + 4, CAMA.y + 14),
                                              (CAMA.right + 2, CAMA.bottom - 6), (CAMA.right - 8, CAMA.bottom - 8)])


def dibujar_armario(capa: pygame.Surface) -> None:

    """ARMARIO CON LAS PUERTAS ABIERTAS Y LA ROPA NUEVA COLGADA (LO QUE BRILLA VA APARTE)."""

    pygame.draw.rect(capa, COLOR_MUEBLE, ARMARIO)
    pygame.draw.rect(capa, (44, 30, 36), ARMARIO.inflate(-10, -16).move(0, 2))            # adentro oscuro
    pygame.draw.rect(capa, COLOR_MUEBLE_SOMBRA, (ARMARIO.x - 4, ARMARIO.y - 6, ARMARIO.width + 8, 8))

    # PUERTAS ABIERTAS EN PERSPECTIVA, CON SU ESPEJITO Y SU PERILLA
    pygame.draw.polygon(capa, COLOR_MUEBLE_SOMBRA, [(ARMARIO.x, ARMARIO.y + 2), (ARMARIO.x - 16, ARMARIO.y + 12),
                                                    (ARMARIO.x - 16, ARMARIO.bottom - 6), (ARMARIO.x, ARMARIO.bottom)])
    pygame.draw.circle(capa, (230, 190, 70), (ARMARIO.x - 12, ARMARIO.centery), 2)
    pygame.draw.polygon(capa, COLOR_MUEBLE_SOMBRA, [(ARMARIO.right, ARMARIO.y + 2), (ARMARIO.right + 12, ARMARIO.y + 10),
                                                    (ARMARIO.right + 12, ARMARIO.bottom - 4), (ARMARIO.right, ARMARIO.bottom)])

    # TUBO Y GANCHOS
    pygame.draw.line(capa, (180, 170, 160), (ARMARIO.x + 6, 116), (ARMARIO.right - 6, 116), 2)

    for x in [565, 598]:
        pygame.draw.arc(capa, (190, 190, 196), (x - 3, 110, 6, 6), 0, 3.14, 1)
        pygame.draw.line(capa, (190, 190, 196), (x - 8, 121), (x + 8, 121))

    # PANTALONES DE TERCIOPELO NEGRO (CON BRILLITO DE TELA SUAVE)
    pygame.draw.polygon(capa, (22, 20, 28), [(557, 121), (573, 121), (575, 196), (567, 196), (565, 140), (563, 196), (555, 196)])
    pygame.draw.line(capa, (70, 66, 86), (558, 126), (557, 192))
    pygame.draw.line(capa, (70, 66, 86), (570, 126), (572, 192))

    # SUETER GRIS CON MANGAS
    pygame.draw.polygon(capa, (150, 152, 160), [(586, 121), (610, 121), (614, 160), (582, 160)])
    pygame.draw.polygon(capa, (130, 132, 140), [(586, 122), (579, 150), (583, 152), (589, 132)])
    pygame.draw.polygon(capa, (130, 132, 140), [(610, 122), (617, 150), (613, 152), (607, 132)])
    pygame.draw.line(capa, (120, 122, 130), (583, 158), (613, 158), 2)

    # BOTAS NARANJAS EN EL PISO DEL ARMARIO
    for x, y in BOTAS:
        pygame.draw.rect(capa, (240, 120, 30), (x - 5, y - 16, 10, 16))
        pygame.draw.rect(capa, (240, 120, 30), (x - 5, y - 4, 14, 6))
        pygame.draw.line(capa, (190, 80, 20), (x - 5, y + 1), (x + 8, y + 1))
        pygame.draw.line(capa, (255, 176, 90), (x - 3, y - 14), (x - 3, y - 4))


def dibujar_coraline(lienzo: pygame.Surface) -> None:

    """CORALINE EN PIJAMA, RECIEN LEVANTADA, MIRANDO EL ARMARIO."""

    sprite = pasillo_noche.sprite_pijama()

    sombra = pygame.Surface((sprite.get_width() + 6, 6), pygame.SRCALPHA)
    pygame.draw.ellipse(sombra, (0, 0, 0, 110), sombra.get_rect())
    lienzo.blit(sombra, (X_CORALINE - sombra.get_width() // 2, Y_PISO - 4))

    lienzo.blit(sprite, (X_CORALINE - sprite.get_width() // 2, Y_PISO - sprite.get_height()))


def crear_fijo() -> pygame.Surface:

    lienzo = pygame.Surface((ANCHO, ALTO))

    dibujar_pared(lienzo)
    dibujar_ventana(lienzo)

    capa = capa_vacia()
    dibujar_cama(capa)
    dibujar_armario(capa)
    pegar_con_contorno(lienzo, capa)

    dibujar_coraline(lienzo)

    brillo(lienzo, (VENTANA.centerx + 30, 200), 120, COLOR_SOL, 40)
    brillo(lienzo, (ARMARIO.centerx, 150), 50, (255, 220, 160), 30)
    orillas_oscuras(lienzo)

    return lienzo


# --------------------------------------------------
# LO QUE SE MUEVE
# --------------------------------------------------

def dibujar_polvo(lienzo: pygame.Surface, tiempo: float) -> None:

    """MOTITAS DE POLVO QUE FLOTAN DENTRO DEL RAYO DE SOL."""

    for i in range(14):

        bajada = (tiempo * 4 + i * 17) % 150
        x = VENTANA.x + 10 + int(bajada * 0.45) + (i * 13) % 40 + int(math.sin(tiempo + i) * 3)
        y = VENTANA.bottom + int(bajada)

        lienzo.set_at((x, y), mezclar(COLOR_SOL, (255, 255, 255), 0.5))


def dibujar_estrellitas(lienzo: pygame.Surface, tiempo: float) -> None:

    """LAS ESTRELLITAS DEL SUETER SE PRENDEN Y SE APAGAN UNA POR UNA."""

    for i in range(len(ESTRELLAS_SUETER)):

        x, y = ESTRELLAS_SUETER[i]
        luz = (math.sin(tiempo * 3 + i * 1.4) + 1) / 2
        color = mezclar((200, 190, 140), (255, 250, 200), luz)

        lienzo.set_at((x, y), color)

        if luz > 0.6:
            for dx, dy in [(-1, 0), (1, 0), (0, -1), (0, 1)]:
                lienzo.set_at((x + dx, y + dy), color)

        if luz > 0.9:
            for dx, dy in [(-2, 0), (2, 0), (0, -2), (0, 2)]:
                lienzo.set_at((x + dx, y + dy), (255, 255, 240))


def dibujar_destello_botas(lienzo: pygame.Surface, tiempo: float) -> None:

    """UN DESTELLO CRUZA LAS BOTAS NARANJAS CADA 3 SEGUNDOS, COMO SI FUERAN NUEVAS DE VERDAD."""

    fase = tiempo % 3

    if fase > 0.6:
        return

    for i in range(len(BOTAS)):
        x, y = BOTAS[i]
        alto = int(fase / 0.6 * 16)
        pygame.draw.line(lienzo, (255, 230, 190), (x + 1, y - 2 - alto), (x + 3, y - 4 - alto))


def dibujar(ventana: pygame.Surface) -> None:

    """DIBUJA LA ESCENA COMPLETA EN LA VENTANA DEL JUEGO."""

    if "fijo" not in CAPAS:
        CAPAS["fijo"] = crear_fijo()

    tiempo = pygame.time.get_ticks() / 1000

    lienzo = CAPAS["fijo"].copy()

    dibujar_polvo(lienzo, tiempo)
    dibujar_estrellitas(lienzo, tiempo)
    dibujar_destello_botas(lienzo, tiempo)
    otro_cuarto.dibujar_dinosaurio(lienzo, tiempo)

    mostrar(ventana, lienzo)
