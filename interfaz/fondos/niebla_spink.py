"""FONDO DIBUJADO CON CODIGO: MANANA DE NIEBLA CON LA SENORITA SPINK.

Coraline sale al jardin en una manana de niebla espesa y se encuentra con la
senorita Spink paseando a sus dos perritos negros. Atras, la casona rosa
(con su torrecita picuda) casi no se ve entre la niebla. Se usa en cap02_n01.

Coraline es la Coraline chica de personajes.py. La senorita Spink se dibuja con el
mismo estilo que la mama (figuras con luz y sombra): bajita y redonda, pelo
gris en chongo, lentes redondos, abrigo lila y bufanda.

Lo que se mueve: la niebla pasa de lado a lado, los perros mueven la cola y
dan saltitos, y la senorita Spink parpadea.
"""

import pygame

from interfaz.fondos.pintura import ANCHO, ALTO
from interfaz.fondos.pintura import mezclar, degradado, brillo, orillas_oscuras, mostrar
from interfaz.fondos import personajes

Y_PISO = 300

X_CORALINE = 452          # centro de sus pies

X_SPINK = 586             # centro de sus pies

PERROS = [508, 532]       # x de la cola de cada perro

COLOR_NIEBLA = (168, 178, 176)
COLOR_PASTO = (66, 86, 70)

CAPAS = {}


# --------------------------------------------------
# PARTE FIJA: JARDIN CON NIEBLA
# --------------------------------------------------

def dibujar_jardin(lienzo: pygame.Surface) -> None:

    """CIELO BLANCO GRISACEO, LA CASA Y LOS ARBOLES COMO SOMBRAS, Y EL PASTO."""

    degradado(lienzo, pygame.Rect(0, 0, ANCHO, Y_PISO), (196, 202, 198), COLOR_NIEBLA, 20)

    # LA CASONA ROSA A LO LEJOS, DESLAVADA POR LA NIEBLA
    color_casa = mezclar(COLOR_NIEBLA, (226, 150, 172), 0.45)
    color_techo = mezclar(COLOR_NIEBLA, (92, 44, 42), 0.45)
    color_marco = mezclar(COLOR_NIEBLA, (240, 232, 232), 0.5)
    color_vidrio = mezclar(COLOR_NIEBLA, (110, 128, 150), 0.45)

    pygame.draw.rect(lienzo, color_casa, (430, 110, 180, 170))
    pygame.draw.polygon(lienzo, color_techo, [(420, 114), (530, 50), (640, 114)])
    pygame.draw.polygon(lienzo, color_casa, [(450, 110), (530, 66), (610, 110)])

    # TORRECITA PICUDA A LA IZQUIERDA
    pygame.draw.rect(lienzo, color_casa, (412, 100, 26, 180))
    pygame.draw.polygon(lienzo, color_techo, [(406, 104), (425, 34), (444, 104)])

    # PORCHE
    pygame.draw.rect(lienzo, color_techo, (424, 196, 190, 6))

    for x in [434, 486, 600]:
        pygame.draw.rect(lienzo, color_marco, (x, 202, 3, 78))

    for x in [446, 500, 560]:
        for y in [130, 212]:
            pygame.draw.rect(lienzo, color_marco, (x - 2, y - 2, 20, 30))
            pygame.draw.rect(lienzo, color_vidrio, (x, y, 16, 26))

    # UNA VENTANA CON LUZ: ALGUIEN YA ESTA DESPIERTO
    pygame.draw.rect(lienzo, (226, 204, 150), (500, 130, 16, 26))

    # ARBOLES A LOS LADOS, MAS CERCA (UN POCO MAS OSCUROS)
    color_arbol = mezclar(COLOR_NIEBLA, (40, 54, 48), 0.55)

    for x, alto in [(386, 170), (630, 190)]:
        pygame.draw.rect(lienzo, color_arbol, (x - 4, Y_PISO - alto + 60, 8, alto - 60))
        pygame.draw.ellipse(lienzo, color_arbol, (x - 34, Y_PISO - alto, 68, 90))

    # PASTO Y CAMINO DE TIERRA
    degradado(lienzo, pygame.Rect(0, Y_PISO, ANCHO, ALTO - Y_PISO), COLOR_PASTO, (34, 46, 40), 5)

    pygame.draw.polygon(
        lienzo,
        (110, 104, 92),
        [(470, Y_PISO), (560, Y_PISO), (640, ALTO), (420, ALTO)]
    )

    # MATITAS DE PASTO
    for x in range(0, ANCHO, 7):
        y = Y_PISO + 4 + (x * 13) % 50
        pygame.draw.line(lienzo, (88, 112, 90), (x, y), (x + 1, y - 3))

    # VELO DE NIEBLA SOBRE TODO LO DE ATRAS
    velo = pygame.Surface((ANCHO, Y_PISO + 20), pygame.SRCALPHA)
    velo.fill((200, 206, 204, 70))
    lienzo.blit(velo, (0, 0))


# --------------------------------------------------
# PARTE FIJA: CORALINE Y LA SENORITA SPINK
# --------------------------------------------------

def dibujar_sombra_piso(lienzo: pygame.Surface, x: int, ancho: int) -> None:

    """SOMBRA SUAVE EN EL PISO, CENTRADA EN x."""

    sombra = pygame.Surface((ancho, 8), pygame.SRCALPHA)
    pygame.draw.ellipse(sombra, (0, 0, 0, 90), sombra.get_rect())
    lienzo.blit(sombra, (x - ancho // 2, Y_PISO - 4))


def dibujar_coraline(lienzo: pygame.Surface) -> None:

    """CORALINE CHICA (personajes.py) MIRANDO A LA DERECHA."""

    personajes.dibujar_coraline_chica(lienzo, X_CORALINE, Y_PISO, True)


def dibujar_luces(lienzo: pygame.Surface) -> None:

    """LUZ PALIDA DE LA MANANA ARRIBA Y ORILLAS OSCURAS."""

    brillo(lienzo, (520, 90), 160, (255, 250, 230), 40)

    orillas_oscuras(lienzo)


def crear_fijo() -> pygame.Surface:

    lienzo = pygame.Surface((ANCHO, ALTO))

    dibujar_jardin(lienzo)
    dibujar_coraline(lienzo)
    personajes.dibujar_spink(lienzo, X_SPINK, "correas")
    dibujar_luces(lienzo)

    return lienzo


def crear_niebla() -> pygame.Surface:

    """NUBES DE NIEBLA EN UNA FRANJA DEL DOBLE DE ANCHO, PARA HACERLA CORRER."""

    niebla = pygame.Surface((ANCHO * 2, ALTO), pygame.SRCALPHA)

    for i in range(26):

        x = (i * 97) % (ANCHO * 2)
        y = 150 + (i * 53) % 170
        ancho = 120 + (i * 31) % 120

        pygame.draw.ellipse(niebla, (220, 226, 224, 34), (x, y, ancho, 30))

    return niebla


# --------------------------------------------------
# LO QUE SE MUEVE
# --------------------------------------------------

def dibujar_perros(lienzo: pygame.Surface, tiempo: float) -> None:

    """LOS DOS PERROS Y SUS CORREAS HASTA LA MANO DE LA SENORITA SPINK."""

    mano = personajes.mano_spink(X_SPINK, "correas")

    for i in range(len(PERROS)):

        collar = personajes.dibujar_perro(lienzo, PERROS[i], Y_PISO, tiempo, i * 0.7)

        pygame.draw.line(lienzo, personajes.CORREA, mano, collar)


def dibujar_niebla(lienzo: pygame.Surface, tiempo: float) -> None:

    """LA NIEBLA CORRE DESPACIO DE IZQUIERDA A DERECHA Y DA LA VUELTA."""

    if "niebla" not in CAPAS:
        CAPAS["niebla"] = crear_niebla()

    corrimiento = int(tiempo * 8) % (ANCHO * 2)

    lienzo.blit(CAPAS["niebla"], (corrimiento - ANCHO * 2, 0))
    lienzo.blit(CAPAS["niebla"], (corrimiento, 0))


def dibujar(ventana: pygame.Surface) -> None:

    """DIBUJA LA ESCENA COMPLETA EN LA VENTANA DEL JUEGO."""

    if "fijo" not in CAPAS:
        CAPAS["fijo"] = crear_fijo()

    tiempo = pygame.time.get_ticks() / 1000

    lienzo = CAPAS["fijo"].copy()

    dibujar_perros(lienzo, tiempo)
    personajes.dibujar_ojos_spink(lienzo, X_SPINK, tiempo, False)
    dibujar_niebla(lienzo, tiempo)

    mostrar(ventana, lienzo)
