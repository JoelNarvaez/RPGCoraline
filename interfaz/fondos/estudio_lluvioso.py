"""FONDO DIBUJADO CON CODIGO: LA SALA EN UNA TARDE DE LLUVIA.

Coraline esta hincada en el banco de la ventana viendo llover, y su papa
trabaja de espaldas frente a la computadora. Se usa en el reto de contar
puertas (cap01_n03 y cap01_m01).

Se dibuja en pixel art sobre un lienzo de 640x360 que se agranda 2 veces.
Casi todo se dibuja una sola vez y se guarda (capa "frente", con la ventana
transparente). En cada vuelta solo se dibuja lo que se mueve: la lluvia, el
parpadeo del monitor y los relampagos.

La escena importante esta a la derecha, porque a la izquierda va el panel
de texto del diseno de exploracion.
"""

import math

import pygame

from interfaz.fondos.pintura import ANCHO, ALTO
from interfaz.fondos.pintura import mezclar, degradado, brillo, orillas_oscuras, mostrar

# VENTANA (LA LLUVIA SE VE A TRAVES DE ELLA)
VENTANA = pygame.Rect(412, 52, 100, 132)

# MONITOR DEL PAPA
PANTALLA = pygame.Rect(571, 183, 34, 26)

Y_PISO = 290

CAPAS = {}


# --------------------------------------------------
# PARTE FIJA: CIELO (DETRAS DE LA VENTANA)
# --------------------------------------------------

def crear_cielo() -> pygame.Surface:

    """CIELO DE TORMENTA CON LOS TECHOS DE LAS CASAS VECINAS."""

    cielo = pygame.Surface((ANCHO, ALTO))

    degradado(cielo, VENTANA, (24, 26, 52), (70, 62, 104), 9)

    # NUBES OSCURAS
    for x, y, r in [(420, 66, 14), (444, 60, 18), (474, 68, 15), (500, 62, 16)]:
        pygame.draw.circle(cielo, (44, 42, 74), (x, y), r)

    # SILUETAS DE ARBOLES Y TECHOS A LO LEJOS
    y_horizonte = VENTANA.bottom - 30

    pygame.draw.rect(
        cielo,
        (22, 26, 40),
        (VENTANA.x, y_horizonte, VENTANA.width, 30)
    )

    for x in range(VENTANA.x, VENTANA.right, 9):
        alto_arbol = 8 + (x * 7) % 11
        pygame.draw.polygon(
            cielo,
            (22, 26, 40),
            [(x - 6, y_horizonte), (x, y_horizonte - alto_arbol), (x + 6, y_horizonte)]
        )

    pygame.draw.polygon(
        cielo,
        (30, 30, 46),
        [(452, y_horizonte + 2), (470, y_horizonte - 14), (488, y_horizonte + 2)]
    )

    pygame.draw.rect(cielo, (30, 30, 46), (456, y_horizonte + 2, 28, 12))
    pygame.draw.rect(cielo, (210, 170, 90), (466, y_horizonte + 6, 4, 4))   # ventanita con luz

    return cielo


# --------------------------------------------------
# PARTE FIJA: LA SALA (CON LA VENTANA TRANSPARENTE)
# --------------------------------------------------

def dibujar_pared(lienzo: pygame.Surface) -> None:

    """PARED CON PAPEL TAPIZ, MOLDURA Y LAMBRIN."""

    degradado(lienzo, pygame.Rect(0, 0, ANCHO, Y_PISO), (26, 28, 46), (52, 56, 84), 12)

    # PAPEL TAPIZ: FLORES PEQUENAS ACOMODADAS EN DIAGONAL
    for y in range(22, 236, 18):

        desfase = 9 if (y // 18) % 2 == 0 else 0

        for x in range(desfase, ANCHO, 18):

            color = mezclar((52, 56, 86), (70, 76, 112), y / 236)

            lienzo.set_at((x, y - 2), color)
            lienzo.set_at((x - 2, y), color)
            lienzo.set_at((x + 2, y), color)
            lienzo.set_at((x, y + 2), color)
            lienzo.set_at((x, y), mezclar(color, (120, 90, 120), 0.4))

    # MOLDURA DEL TECHO
    pygame.draw.rect(lienzo, (16, 16, 28), (0, 0, ANCHO, 12))
    pygame.draw.rect(lienzo, (60, 58, 84), (0, 12, ANCHO, 2))
    pygame.draw.rect(lienzo, (34, 34, 54), (0, 14, ANCHO, 3))

    # LAMBRIN CON TABLEROS
    pygame.draw.rect(lienzo, (34, 38, 58), (0, 238, ANCHO, Y_PISO - 238))
    pygame.draw.rect(lienzo, (74, 76, 104), (0, 236, ANCHO, 2))

    for x in range(6, ANCHO, 40):
        pygame.draw.rect(lienzo, (28, 30, 48), (x, 244, 32, 38), 1)
        pygame.draw.line(lienzo, (50, 54, 78), (x + 1, 281), (x + 31, 281))

    pygame.draw.rect(lienzo, (20, 20, 32), (0, Y_PISO - 4, ANCHO, 4))


def dibujar_piso(lienzo: pygame.Surface) -> None:

    """PISO DE MADERA QUE SE ABRE HACIA ABAJO, Y UNA ALFOMBRA."""

    degradado(lienzo, pygame.Rect(0, Y_PISO, ANCHO, ALTO - Y_PISO), (54, 38, 34), (36, 24, 24), 5)

    y = Y_PISO + 3
    separacion = 5

    while y < ALTO:

        pygame.draw.line(lienzo, (34, 22, 20), (0, y), (ANCHO, y))

        desfase = (y * 13) % 60

        for x in range(desfase, ANCHO, 60):
            pygame.draw.line(lienzo, (34, 22, 20), (x, y), (x, y + separacion))

        y = y + separacion
        separacion = separacion + 2

    # ALFOMBRA ROJIZA CON ORILLA DORADA
    alfombra = pygame.Rect(110, 304, 330, 34)

    pygame.draw.ellipse(lienzo, (86, 36, 50), alfombra)
    pygame.draw.ellipse(lienzo, (150, 110, 70), alfombra.inflate(-12, -8), 1)
    pygame.draw.ellipse(lienzo, (106, 48, 62), alfombra.inflate(-60, -18))


def dibujar_ventana(lienzo: pygame.Surface) -> None:

    """MARCO, VIDRIOS TRANSPARENTES, GOTAS, REPISA Y CORTINAS."""

    pygame.draw.rect(lienzo, (196, 186, 170), VENTANA.inflate(10, 10))
    pygame.draw.rect(lienzo, (150, 140, 130), VENTANA.inflate(10, 10), 1)

    # LOS VIDRIOS SE VACIAN PARA QUE SE VEA EL CIELO DE ATRAS
    lienzo.fill((0, 0, 0, 0), VENTANA)

    # REFLEJO SUAVE EN EL VIDRIO
    reflejo = pygame.Surface((VENTANA.width, VENTANA.height), pygame.SRCALPHA)

    pygame.draw.polygon(
        reflejo,
        (200, 210, 255, 22),
        [(10, 0), (34, 0), (4, 60), (0, 60), (0, 20)]
    )

    lienzo.blit(reflejo, VENTANA.topleft)

    # GOTAS PEGADAS AL VIDRIO
    for i in range(26):

        x = VENTANA.x + 3 + (i * 37) % (VENTANA.width - 6)
        y = VENTANA.y + 3 + (i * 53) % (VENTANA.height - 6)

        lienzo.set_at((x, y), (170, 190, 230, 150))
        lienzo.set_at((x, y + 1), (110, 130, 180, 120))

    # PALILLOS: 2 COLUMNAS Y 3 FILAS
    color_marco = (196, 186, 170)

    pygame.draw.rect(lienzo, color_marco, (VENTANA.centerx - 2, VENTANA.y, 4, VENTANA.height))

    for y in [VENTANA.y + 43, VENTANA.y + 88]:
        pygame.draw.rect(lienzo, color_marco, (VENTANA.x, y, VENTANA.width, 3))

    # REPISA
    pygame.draw.rect(lienzo, (210, 200, 184), (VENTANA.x - 12, VENTANA.bottom + 5, VENTANA.width + 24, 5))
    pygame.draw.rect(lienzo, (120, 110, 104), (VENTANA.x - 12, VENTANA.bottom + 10, VENTANA.width + 24, 2))

    # CORTINAS MORADAS CON PLIEGUES
    pygame.draw.rect(lienzo, (70, 56, 50), (VENTANA.x - 26, 40, VENTANA.width + 52, 3))

    for lado in [-1, 1]:

        if lado == -1:
            x_inicio = VENTANA.x - 22
        else:
            x_inicio = VENTANA.right + 4

        for i in range(6):

            tono = [(92, 54, 86), (112, 66, 104), (80, 46, 76)][i % 3]

            x = x_inicio + i * 3

            # LA CORTINA SE RECOGE UN POCO A LA ALTURA DE LA REPISA
            pygame.draw.rect(lienzo, tono, (x, 43, 3, 154))

        pygame.draw.rect(lienzo, (176, 140, 80), (x_inicio - 1, 128, 20, 3))   # cordon


def dibujar_banco(lienzo: pygame.Surface) -> None:

    """BANCO DEBAJO DE LA VENTANA CON COJIN."""

    pygame.draw.rect(lienzo, (60, 42, 40), (VENTANA.x - 14, 212, VENTANA.width + 28, 26))
    pygame.draw.rect(lienzo, (46, 32, 30), (VENTANA.x - 10, 218, VENTANA.width + 20, 16), 1)
    pygame.draw.rect(lienzo, (118, 76, 96), (VENTANA.x - 16, 205, VENTANA.width + 32, 8), border_radius=3)
    pygame.draw.line(lienzo, (150, 104, 124), (VENTANA.x - 12, 206), (VENTANA.right + 12, 206))


def dibujar_coraline(lienzo: pygame.Surface) -> None:

    """CORALINE HINCADA EN EL BANCO, DE ESPALDAS, CON LA BARBILLA EN LOS BRAZOS."""

    x = 452

    # PIERNAS DOBLADAS SOBRE EL COJIN Y SUELAS DE LAS BOTAS
    pygame.draw.rect(lienzo, (40, 46, 78), (x - 2, 196, 26, 10), border_radius=3)
    pygame.draw.rect(lienzo, (70, 40, 46), (x + 22, 200, 5, 6))
    pygame.draw.rect(lienzo, (70, 40, 46), (x - 6, 200, 5, 6))

    # ESPALDA CON SUETER AMARILLO
    pygame.draw.rect(lienzo, (226, 182, 50), (x, 176, 22, 24), border_radius=4)
    pygame.draw.rect(lienzo, (196, 150, 34), (x, 194, 22, 4))
    pygame.draw.line(lienzo, (246, 210, 90), (x + 2, 180), (x + 2, 192))

    # BRAZOS CRUZADOS SOBRE LA REPISA
    pygame.draw.rect(lienzo, (226, 182, 50), (x - 9, 182, 40, 7), border_radius=3)
    pygame.draw.line(lienzo, (186, 140, 30), (x - 7, 188), (x + 29, 188))
    pygame.draw.rect(lienzo, (236, 200, 172), (x - 11, 183, 3, 5))
    pygame.draw.rect(lienzo, (236, 200, 172), (x + 30, 183, 3, 5))

    # CABEZA: CASI TODO ES PELO AZUL PORQUE ESTA DE ESPALDAS
    pygame.draw.ellipse(lienzo, (34, 58, 170), (x - 1, 160, 24, 24))
    pygame.draw.rect(lienzo, (34, 58, 170), (x - 2, 172, 26, 10))
    pygame.draw.line(lienzo, (70, 100, 214), (x + 4, 164), (x + 14, 162))   # brillo del pelo
    pygame.draw.line(lienzo, (70, 100, 214), (x + 3, 168), (x + 8, 166))
    pygame.draw.rect(lienzo, (236, 200, 172), (x - 3, 174, 3, 5))           # mejilla
    pygame.draw.rect(lienzo, (240, 140, 196), (x + 17, 164, 4, 2))          # pasador

    # LA LUZ DE LA VENTANA LE PINTA EL CONTORNO
    pygame.draw.line(lienzo, (140, 150, 210), (x + 5, 160), (x + 18, 160))


def dibujar_detalles(lienzo: pygame.Surface) -> None:

    """CUADROS, MACETA EN LA REPISA Y LA LUZ QUE ENTRA AL PISO."""

    # CUADRO ARRIBA DEL SILLON
    pygame.draw.rect(lienzo, (150, 116, 60), (176, 146, 46, 34))
    pygame.draw.rect(lienzo, (56, 72, 88), (180, 150, 38, 26))
    pygame.draw.polygon(lienzo, (40, 52, 66), [(180, 176), (196, 158), (210, 170), (218, 162), (218, 176)])
    pygame.draw.circle(lienzo, (210, 200, 160), (208, 156), 3)

    # CUADRO OVALADO JUNTO AL ESCRITORIO
    pygame.draw.ellipse(lienzo, (150, 116, 60), (586, 104, 30, 38))
    pygame.draw.ellipse(lienzo, (96, 70, 80), (590, 108, 22, 30))
    pygame.draw.ellipse(lienzo, (60, 44, 52), (596, 114, 10, 12))

    # RELOJ DE PARED
    pygame.draw.circle(lienzo, (150, 116, 60), (350, 104), 12)
    pygame.draw.circle(lienzo, (224, 214, 190), (350, 104), 9)
    pygame.draw.line(lienzo, (40, 34, 30), (350, 104), (350, 98))
    pygame.draw.line(lienzo, (40, 34, 30), (350, 104), (355, 106))

    # MACETA EN LA REPISA
    pygame.draw.rect(lienzo, (150, 80, 60), (VENTANA.x - 8, VENTANA.bottom - 4, 10, 9))
    for dx, dy in [(-6, -8), (-3, -12), (0, -9), (-9, -5), (2, -5)]:
        pygame.draw.line(lienzo, (70, 110, 70), (VENTANA.x - 3, VENTANA.bottom - 3),
                         (VENTANA.x - 3 + dx, VENTANA.bottom - 3 + dy), 2)

    # LUZ DE LA VENTANA SOBRE EL PISO
    luz = pygame.Surface((ANCHO, ALTO), pygame.SRCALPHA)
    pygame.draw.polygon(
        luz,
        (140, 150, 220, 26),
        [(VENTANA.x + 4, Y_PISO + 2), (VENTANA.right - 4, Y_PISO + 2),
         (VENTANA.right + 40, ALTO), (VENTANA.x + 20, ALTO)]
    )
    lienzo.blit(luz, (0, 0))


def dibujar_papa(lienzo: pygame.Surface) -> None:

    """ESCRITORIO, MONITOR Y EL PAPA DE ESPALDAS, ILUMINADO POR LA PANTALLA."""

    # ESCRITORIO
    pygame.draw.rect(lienzo, (72, 50, 42), (536, 224, 104, 7))
    pygame.draw.rect(lienzo, (52, 36, 32), (540, 231, 96, 52))
    pygame.draw.rect(lienzo, (42, 28, 26), (546, 238, 30, 18), 1)
    pygame.draw.rect(lienzo, (42, 28, 26), (546, 260, 30, 18), 1)
    pygame.draw.rect(lienzo, (176, 140, 80), (559, 246, 4, 2))
    pygame.draw.rect(lienzo, (176, 140, 80), (559, 268, 4, 2))

    # PAPELES Y TAZA
    pygame.draw.rect(lienzo, (210, 206, 196), (614, 219, 18, 5))
    pygame.draw.rect(lienzo, (190, 186, 176), (616, 216, 16, 3))
    pygame.draw.rect(lienzo, (150, 60, 60), (542, 216, 7, 8))
    pygame.draw.rect(lienzo, (150, 60, 60), (549, 218, 2, 4), 1)

    # MONITOR
    pygame.draw.rect(lienzo, (64, 66, 78), (PANTALLA.x - 4, PANTALLA.y - 4, PANTALLA.width + 8, PANTALLA.height + 8),
                     border_radius=2)
    pygame.draw.rect(lienzo, (64, 66, 78), (PANTALLA.centerx - 4, PANTALLA.bottom + 4, 8, 7))
    pygame.draw.rect(lienzo, (64, 66, 78), (PANTALLA.centerx - 10, 220, 20, 4))
    pygame.draw.rect(lienzo, (150, 220, 230), PANTALLA)

    # SILLA
    pygame.draw.rect(lienzo, (30, 26, 40), (566, 228, 40, 40), border_radius=8)
    pygame.draw.rect(lienzo, (30, 26, 40), (584, 268, 4, 16))
    pygame.draw.line(lienzo, (30, 26, 40), (572, 284), (600, 284), 2)

    # PAPA: HOMBROS CON SUETER VERDE Y CABEZA DE PELO CAFE
    pygame.draw.rect(lienzo, (46, 66, 58), (562, 214, 48, 22), border_radius=8)
    pygame.draw.ellipse(lienzo, (70, 48, 36), (574, 192, 24, 26))
    pygame.draw.rect(lienzo, (210, 170, 140), (573, 204, 3, 6))   # oreja

    # LUZ DEL MONITOR EN EL CONTORNO
    pygame.draw.line(lienzo, (150, 220, 230), (578, 192), (594, 192))
    pygame.draw.line(lienzo, (120, 190, 200), (564, 214), (608, 214))


def dibujar_lado_izquierdo(lienzo: pygame.Surface) -> None:

    """LIBRERO, SILLON Y LAMPARA (QUEDAN DETRAS DEL PANEL DE TEXTO)."""

    # LIBRERO
    pygame.draw.rect(lienzo, (58, 40, 36), (26, 108, 88, Y_PISO - 108))

    colores_libros = [(120, 50, 60), (60, 80, 120), (150, 120, 70), (70, 100, 80), (110, 70, 110)]

    for repisa in range(5):

        y = 114 + repisa * 34

        pygame.draw.rect(lienzo, (40, 28, 26), (30, y, 80, 30))

        x = 32

        for i in range(10):

            ancho = 5 + (i * 3 + repisa) % 4
            alto = 20 + (i * 5 + repisa * 3) % 9

            if x + ancho > 108:
                break

            pygame.draw.rect(lienzo, colores_libros[(i + repisa) % 5], (x, y + 30 - alto, ancho, alto))

            x = x + ancho + 1

    # SILLON
    pygame.draw.rect(lienzo, (96, 52, 64), (150, 226, 96, 30), border_radius=8)
    pygame.draw.rect(lienzo, (116, 64, 78), (146, 250, 104, 24), border_radius=4)
    pygame.draw.rect(lienzo, (86, 46, 58), (140, 240, 14, 34), border_radius=4)
    pygame.draw.rect(lienzo, (86, 46, 58), (242, 240, 14, 34), border_radius=4)

    # LAMPARA DE PIE
    pygame.draw.line(lienzo, (30, 26, 28), (286, 186), (286, Y_PISO - 2), 2)
    pygame.draw.rect(lienzo, (30, 26, 28), (278, Y_PISO - 4, 16, 3))
    pygame.draw.polygon(lienzo, (226, 190, 130), [(274, 186), (298, 186), (292, 168), (280, 168)])


def dibujar_luces(lienzo: pygame.Surface) -> None:

    """LUZ CALIDA DE LA LAMPARA, LUZ FRIA DEL MONITOR Y ORILLAS OSCURAS."""

    brillo(lienzo, (286, 186), 100, (255, 190, 110), 120)
    brillo(lienzo, (286, Y_PISO + 8), 50, (255, 190, 110), 50)
    brillo(lienzo, (PANTALLA.centerx, PANTALLA.centery), 80, (120, 210, 230), 90)
    brillo(lienzo, (VENTANA.centerx, VENTANA.centery + 30), 90, (120, 130, 200), 40)

    orillas_oscuras(lienzo)


def crear_frente() -> pygame.Surface:

    """TODA LA SALA EN UNA CAPA CON LA VENTANA TRANSPARENTE."""

    frente = pygame.Surface((ANCHO, ALTO), pygame.SRCALPHA)

    dibujar_pared(frente)
    dibujar_piso(frente)
    dibujar_lado_izquierdo(frente)
    dibujar_ventana(frente)
    dibujar_detalles(frente)
    dibujar_banco(frente)
    dibujar_coraline(frente)
    dibujar_papa(frente)
    dibujar_luces(frente)

    return frente


# --------------------------------------------------
# LO QUE SE MUEVE
# --------------------------------------------------

def dibujar_lluvia(lienzo: pygame.Surface, tiempo: float) -> None:

    """GOTAS QUE CAEN EN DIAGONAL DETRAS DEL VIDRIO."""

    for i in range(40):

        x = VENTANA.x + (i * 23) % VENTANA.width
        y = VENTANA.y + int((tiempo * 140 + i * 31) % VENTANA.height)

        x = x - int((y - VENTANA.y) * 0.15)

        if x < VENTANA.x:
            x = x + VENTANA.width

        fin_y = min(y + 5, VENTANA.bottom - 1)

        pygame.draw.line(lienzo, (130, 150, 200), (x, y), (x - 1, fin_y))


def dibujar_pantalla(lienzo: pygame.Surface, tiempo: float) -> None:

    """LINEAS DE TEXTO EN EL MONITOR Y UN PARPADEO LEVE."""

    for i in range(5):

        largo = 10 + (i * 7 + int(tiempo * 2)) % 18

        pygame.draw.line(
            lienzo,
            (60, 120, 140),
            (PANTALLA.x + 3, PANTALLA.y + 3 + i * 4),
            (PANTALLA.x + 3 + largo, PANTALLA.y + 3 + i * 4)
        )

    # CURSOR QUE PARPADEA
    if int(tiempo * 2) % 2 == 0:
        pygame.draw.rect(lienzo, (40, 90, 110), (PANTALLA.x + 22, PANTALLA.y + 19, 2, 3))


def fuerza_relampago(tiempo: float) -> float:

    """0 CASI SIEMPRE; SUBE UN INSTANTE CADA 9 SEGUNDOS (CON DOBLE DESTELLO)."""

    fase = tiempo % 9

    if fase < 0.08:
        return 1.0

    if 0.16 < fase < 0.26:
        return 0.6

    return 0.0


# --------------------------------------------------
# DIBUJAR
# --------------------------------------------------

def dibujar(ventana: pygame.Surface) -> None:

    """DIBUJA LA SALA COMPLETA EN LA VENTANA DEL JUEGO."""

    if "cielo" not in CAPAS:
        CAPAS["cielo"] = crear_cielo()
        CAPAS["frente"] = crear_frente()

    tiempo = pygame.time.get_ticks() / 1000

    lienzo = CAPAS["cielo"].copy()

    relampago = fuerza_relampago(tiempo)

    if relampago > 0:

        destello = pygame.Surface(VENTANA.size)
        destello.fill((200, 200, 255))
        destello.set_alpha(int(150 * relampago))
        lienzo.blit(destello, VENTANA.topleft)

    dibujar_lluvia(lienzo, tiempo)

    lienzo.blit(CAPAS["frente"], (0, 0))

    dibujar_pantalla(lienzo, tiempo)

    if relampago > 0:

        cuarto = pygame.Surface((ANCHO, ALTO))
        cuarto.fill((150, 160, 230))
        cuarto.set_alpha(int(35 * relampago))
        lienzo.blit(cuarto, (0, 0))

    mostrar(ventana, lienzo)
