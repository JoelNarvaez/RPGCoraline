"""PARTES COMPARTIDAS: LA SALA DEL DEPARTAMENTO DE LAS ACTRICES.

No es un fondo por si solo: lo usan te_actrices (cap02_n03), hojas_te
(cap02_n04) y piedra_spink (cap02_n05), que pasan en el mismo cuarto.

Una sala vieja y calientita: papel tapiz color vino, fotos y carteles de
teatro con marco dorado, una lampara de flecos, tapete y la mesita del te.
El piso esta en y = 300, igual que en los dibujos de las vecinas
(personajes.py).
"""

import math

import pygame

from interfaz.fondos.pintura import ANCHO, ALTO
from interfaz.fondos.pintura import mezclar, degradado, brillo, tablas_de_madera, COLOR_CONTORNO
from interfaz.fondos import personajes

Y_PISO = 300

LAMPARA = (622, 120)      # centro de la pantalla de la lampara

COLOR_PAPEL = (112, 46, 58)
COLOR_MADERA = (70, 40, 32)
COLOR_DORADO = (196, 156, 72)
COLOR_MANTEL = (206, 150, 160)
COLOR_PORCELANA = (244, 240, 230)
COLOR_LUZ_CALIDA = (255, 190, 120)

# CUADROS EN LA PARED: (x, y, ancho, alto, que tienen adentro)
CUADROS = [
    (416, 70, 34, 44, "retrato"),
    (462, 60, 46, 60, "cartel"),
    (520, 74, 30, 38, "perro"),
    (562, 56, 36, 48, "retrato"),
    (452, 136, 26, 32, "perro"),
    (566, 124, 30, 26, "mascaras"),
]


# --------------------------------------------------
# LA SALA
# --------------------------------------------------

def dibujar_cuadro(lienzo: pygame.Surface, x: int, y: int, ancho: int, alto: int, tipo: str) -> None:

    """MARCO DORADO CON RELIEVE (LUZ ARRIBA, SOMBRA ABAJO) Y UNA FOTO O CARTEL ADENTRO."""

    # SOMBRA DEL CUADRO EN LA PARED
    sombra = pygame.Surface((ancho + 6, alto + 6), pygame.SRCALPHA)
    sombra.fill((20, 6, 10, 90))
    lienzo.blit(sombra, (x, y + 2))

    # MARCO CON RELIEVE
    pygame.draw.rect(lienzo, COLOR_DORADO, (x - 3, y - 3, ancho + 6, alto + 6))
    pygame.draw.line(lienzo, (240, 210, 130), (x - 3, y - 3), (x + ancho + 2, y - 3))
    pygame.draw.line(lienzo, (240, 210, 130), (x - 3, y - 3), (x - 3, y + alto + 2))
    pygame.draw.line(lienzo, (120, 86, 36), (x - 3, y + alto + 2), (x + ancho + 2, y + alto + 2))
    pygame.draw.line(lienzo, (120, 86, 36), (x + ancho + 2, y - 3), (x + ancho + 2, y + alto + 2))
    pygame.draw.rect(lienzo, (120, 86, 36), (x - 1, y - 1, ancho + 2, alto + 2), 1)

    if tipo == "cartel":

        # CARTEL DE TEATRO: FONDO ROJO, TELON Y UNA ESTRELLA
        pygame.draw.rect(lienzo, (150, 40, 44), (x, y, ancho, alto))
        pygame.draw.rect(lienzo, (226, 196, 120), (x + 4, y + 4, ancho - 8, 8))
        pygame.draw.line(lienzo, (150, 40, 44), (x + 8, y + 8), (x + ancho - 8, y + 8))
        pygame.draw.polygon(lienzo, (200, 60, 60), [(x, y + 16), (x + 12, y + 16), (x + 4, y + alto)])
        pygame.draw.polygon(lienzo, (200, 60, 60), [(x + ancho, y + 16), (x + ancho - 12, y + 16), (x + ancho - 4, y + alto)])
        cx = x + ancho // 2
        cy = y + alto // 2 + 6
        pygame.draw.polygon(lienzo, (246, 220, 140), [(cx, cy - 7), (cx + 2, cy - 2), (cx + 7, cy - 2), (cx + 3, cy + 2),
                                                      (cx + 5, cy + 7), (cx, cy + 4), (cx - 5, cy + 7), (cx - 3, cy + 2),
                                                      (cx - 7, cy - 2), (cx - 2, cy - 2)])
        return

    # FOTO EN TONO SEPIA CON LAS ORILLAS MAS OSCURAS
    pygame.draw.rect(lienzo, (190, 166, 128), (x, y, ancho, alto))
    pygame.draw.rect(lienzo, (160, 136, 100), (x, y, ancho, alto), 2)
    color = (110, 86, 62)

    if tipo == "retrato":
        pygame.draw.circle(lienzo, color, (x + ancho // 2, y + alto // 3 + 2), ancho // 5)
        pygame.draw.ellipse(lienzo, color, (x + ancho // 4, y + alto // 2 + 2, ancho // 2, alto // 2))
        pygame.draw.line(lienzo, (150, 120, 90), (x + ancho // 2 - 2, y + alto // 3), (x + ancho // 2 - 2, y + alto // 3))

    elif tipo == "perro":
        pygame.draw.rect(lienzo, color, (x + 6, y + alto // 2, ancho - 12, alto // 4), border_radius=3)
        pygame.draw.rect(lienzo, color, (x + 4, y + alto // 2 - 6, 8, 8))
        pygame.draw.line(lienzo, color, (x + 5, y + alto // 2 - 6), (x + 5, y + alto // 2 - 9))

    elif tipo == "mascaras":
        pygame.draw.circle(lienzo, (240, 230, 210), (x + 10, y + 12), 7)
        pygame.draw.circle(lienzo, (60, 50, 50), (x + 20, y + 14), 7)
        pygame.draw.arc(lienzo, color, (x + 6, y + 12, 8, 6), 3.4, 6.0, 1)


def dibujar_papel_tapiz(lienzo: pygame.Surface) -> None:

    """PAPEL TAPIZ COLOR VINO CON RAYAS FINAS Y UN DIBUJO DE ROMBOS (DAMASCO), Y MOLDURAS."""

    degradado(lienzo, pygame.Rect(0, 0, ANCHO, Y_PISO), (54, 22, 30), COLOR_PAPEL, 16)

    for x in range(0, ANCHO, 22):
        pygame.draw.line(lienzo, mezclar(COLOR_PAPEL, (0, 0, 0), 0.18), (x, 8), (x, 218))

    for y in range(24, 214, 26):
        for x in range(11 + (y // 26 % 2) * 11, ANCHO, 22):
            claro = mezclar(COLOR_PAPEL, (230, 170, 130), 0.22)
            pygame.draw.polygon(lienzo, claro, [(x, y - 5), (x + 4, y), (x, y + 5), (x - 4, y)])
            pygame.draw.polygon(lienzo, mezclar(COLOR_PAPEL, (0, 0, 0), 0.2), [(x, y - 2), (x + 1, y), (x, y + 2), (x - 1, y)])
            lienzo.set_at((x, y - 7), claro)
            lienzo.set_at((x, y + 7), claro)

    # MOLDURA DEL TECHO Y GUARDASILLA
    pygame.draw.rect(lienzo, (66, 36, 28), (0, 0, ANCHO, 8))
    pygame.draw.line(lienzo, (120, 76, 54), (0, 8), (ANCHO, 8))
    pygame.draw.line(lienzo, (30, 14, 12), (0, 10), (ANCHO, 10))


def dibujar_lambrin(lienzo: pygame.Surface) -> None:

    """LAMBRIN DE MADERA CON TABLEROS EN RELIEVE Y ZOCLO OSCURO."""

    pygame.draw.rect(lienzo, COLOR_MADERA, (0, 222, ANCHO, Y_PISO - 222))
    pygame.draw.rect(lienzo, (106, 66, 46), (0, 216, ANCHO, 6))
    pygame.draw.line(lienzo, (150, 104, 74), (0, 216), (ANCHO, 216))
    pygame.draw.line(lienzo, (34, 18, 14), (0, 222), (ANCHO, 222))

    for x in range(10, ANCHO, 44):
        tablero = pygame.Rect(x, 232, 34, 56)
        pygame.draw.rect(lienzo, mezclar(COLOR_MADERA, (255, 255, 255), 0.06), tablero)
        pygame.draw.line(lienzo, (106, 70, 52), tablero.topleft, (tablero.right - 1, tablero.y))
        pygame.draw.line(lienzo, (106, 70, 52), tablero.topleft, (tablero.x, tablero.bottom - 1))
        pygame.draw.line(lienzo, (34, 18, 14), (tablero.x, tablero.bottom - 1), (tablero.right - 1, tablero.bottom - 1))
        pygame.draw.line(lienzo, (34, 18, 14), (tablero.right - 1, tablero.y), (tablero.right - 1, tablero.bottom - 1))

        for i in range(3):
            xx = tablero.x + 8 + i * 9
            pygame.draw.line(lienzo, mezclar(COLOR_MADERA, (0, 0, 0), 0.18), (xx, tablero.y + 6 + i * 4), (xx, tablero.bottom - 8))

    pygame.draw.rect(lienzo, (40, 22, 18), (0, Y_PISO - 6, ANCHO, 6))


def dibujar_tapete(lienzo: pygame.Surface) -> None:

    """TAPETE PERSA: ORILLA OSCURA, FRANJA DORADA CON ROMBOS, CENTRO ROJO, MEDALLON Y FLECOS."""

    rect = pygame.Rect(400, 290, 250, 50)

    for x in range(rect.x + 4, rect.right - 4, 4):
        pygame.draw.line(lienzo, (226, 210, 180), (x, rect.bottom - 4), (x, rect.bottom + 1))

    pygame.draw.ellipse(lienzo, (70, 24, 30), rect)
    pygame.draw.ellipse(lienzo, (170, 120, 70), rect.inflate(-10, -6))
    pygame.draw.ellipse(lienzo, (126, 40, 44), rect.inflate(-24, -12))
    pygame.draw.ellipse(lienzo, (150, 56, 54), rect.inflate(-60, -24))
    pygame.draw.ellipse(lienzo, (210, 170, 100), rect.inflate(-150, -36))

    # ROMBITOS EN LA FRANJA DORADA
    for i in range(18):
        angulo = i / 18 * 2 * math.pi
        x = rect.centerx + int(math.cos(angulo) * (rect.width / 2 - 8))
        y = rect.centery + int(math.sin(angulo) * (rect.height / 2 - 5))
        pygame.draw.polygon(lienzo, (90, 30, 34), [(x, y - 2), (x + 2, y), (x, y + 2), (x - 2, y)])


def dibujar_lampara(lienzo: pygame.Surface) -> None:

    """LAMPARA DE PIE CON PANTALLA DE FLECOS, CON LUZ DE UN LADO Y SOMBRA DEL OTRO."""

    x, y = LAMPARA

    pygame.draw.line(lienzo, (40, 30, 26), (x, y + 14), (x, Y_PISO - 2), 3)
    pygame.draw.line(lienzo, (110, 90, 70), (x - 1, y + 14), (x - 1, Y_PISO - 2))
    pygame.draw.ellipse(lienzo, (40, 30, 26), (x - 10, Y_PISO - 6, 20, 6))

    pygame.draw.polygon(lienzo, (226, 150, 90), [(x - 10, y - 14), (x + 10, y - 14), (x + 18, y + 12), (x - 18, y + 12)])
    pygame.draw.polygon(lienzo, (190, 116, 66), [(x + 2, y - 14), (x + 10, y - 14), (x + 18, y + 12), (x + 6, y + 12)])
    pygame.draw.line(lienzo, (250, 200, 140), (x - 10, y - 14), (x - 18, y + 12))
    pygame.draw.polygon(lienzo, COLOR_CONTORNO, [(x - 10, y - 14), (x + 10, y - 14), (x + 18, y + 12), (x - 18, y + 12)], 1)

    for xx in range(x - 18, x + 19, 3):
        pygame.draw.line(lienzo, (190, 110, 60), (xx, y + 12), (xx, y + 18))


def dibujar_sala(lienzo: pygame.Surface) -> None:

    """LA SALA COMPLETA: PAPEL TAPIZ, LAMBRIN, CUADROS, PISO DE TABLAS, TAPETE Y LAMPARA."""

    dibujar_papel_tapiz(lienzo)
    dibujar_lambrin(lienzo)

    for x, y, ancho, alto, tipo in CUADROS:
        dibujar_cuadro(lienzo, x, y, ancho, alto, tipo)

    tablas_de_madera(lienzo, pygame.Rect(0, Y_PISO, ANCHO, ALTO - Y_PISO), (86, 52, 38), 8)
    dibujar_tapete(lienzo)
    dibujar_lampara(lienzo)


def dibujar_luces(lienzo: pygame.Surface) -> None:

    """LUZ CALIDA DE LA LAMPARA. LAS ORILLAS OSCURAS LAS PONE CADA ESCENA AL FINAL."""

    brillo(lienzo, LAMPARA, 200, COLOR_LUZ_CALIDA, 70)


# --------------------------------------------------
# MESITA DEL TE Y CORALINE
# --------------------------------------------------

def dibujar_mesa(lienzo: pygame.Surface, x: int, con_tetera: bool) -> None:

    """MESITA REDONDA CON MANTEL, TAZAS Y EL PLATO DE GALLETAS DURAS. x ES EL CENTRO."""

    # MANTEL QUE CUELGA HASTA EL PISO
    pygame.draw.polygon(lienzo, COLOR_MANTEL, [(x - 30, 246), (x + 30, 246), (x + 36, Y_PISO), (x - 36, Y_PISO)])
    pygame.draw.polygon(lienzo, mezclar(COLOR_MANTEL, (0, 0, 0), 0.15), [(x + 12, 246), (x + 30, 246), (x + 36, Y_PISO), (x + 16, Y_PISO)])
    pygame.draw.ellipse(lienzo, COLOR_MANTEL, (x - 32, 240, 64, 12))

    for xx in range(x - 34, x + 36, 5):
        pygame.draw.circle(lienzo, (240, 226, 222), (xx, Y_PISO - 1), 2)      # encaje

    # PLATO CON GALLETAS
    pygame.draw.ellipse(lienzo, COLOR_PORCELANA, (x - 26, 240, 20, 6))

    for dx in [-22, -16, -19]:
        pygame.draw.circle(lienzo, (176, 130, 76), (x + dx, 241 - (dx == -19) * 2), 3)

    # DOS TAZAS
    for dx in [2, 16]:
        pygame.draw.ellipse(lienzo, COLOR_PORCELANA, (x + dx - 2, 244, 12, 4))
        pygame.draw.rect(lienzo, COLOR_PORCELANA, (x + dx, 238, 8, 7), border_bottom_left_radius=3,
                         border_bottom_right_radius=3)
        pygame.draw.line(lienzo, (90, 120, 170), (x + dx, 240), (x + dx + 7, 240))

    # TETERA
    if con_tetera:
        pygame.draw.ellipse(lienzo, COLOR_PORCELANA, (x - 4, 222, 22, 20))
        pygame.draw.polygon(lienzo, COLOR_PORCELANA, [(x - 4, 230), (x - 12, 222), (x - 10, 220), (x - 2, 228)])   # pico
        pygame.draw.arc(lienzo, COLOR_PORCELANA, (x + 14, 226, 10, 12), -1.6, 1.6, 2)                             # asa
        pygame.draw.circle(lienzo, (90, 120, 170), (x + 7, 232), 3)
        pygame.draw.circle(lienzo, COLOR_PORCELANA, (x + 7, 221), 2)


def dibujar_vapor(lienzo: pygame.Surface, x: int, y: int, tiempo: float) -> None:

    """TRES HILITOS DE VAPOR QUE SUBEN Y SE BORRAN. (x, y) ES DE DONDE SALEN."""

    capa = pygame.Surface((30, 40), pygame.SRCALPHA)

    for i in range(3):

        fase = (tiempo * 0.6 + i / 3) % 1

        for paso in range(6):

            alto = 36 - int((fase * 20 + paso * 3) % 36)
            dx = 15 + int(math.sin(tiempo * 2 + i * 2 + paso * 0.7) * 4) + (i - 1) * 4
            alfa = int(120 * alto / 36)

            capa.set_at((dx, alto), (250, 246, 240, alfa))
            capa.set_at((dx, alto + 1), (250, 246, 240, alfa // 2))

    lienzo.blit(capa, (x - 15, y - 40))


def dibujar_coraline(lienzo: pygame.Surface, x: int, mira_derecha: bool = True) -> None:

    """CORALINE CHICA (personajes.py) PARADA EN EL PISO DE LA SALA. x ES EL CENTRO DE SUS PIES."""

    personajes.dibujar_coraline_chica(lienzo, x, Y_PISO, mira_derecha)
