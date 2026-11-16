"""FONDO DIBUJADO CON CODIGO: CORALINE REGRESA A CASA ENTRE LA NIEBLA.

Ya es tarde y la niebla esta mas oscura. Coraline va por el camino hacia la
casona rosa (la misma de la primera escena: techo cafe, torrecita picuda,
ventanas con marco blanco, porche de columnas y escalera de afuera), con la piedra apretada en el puno. Siente que afuera hay
cosas escondidas: en la niebla aparecen y se borran siluetas y ojitos.
Se usa en cap02_n06.

Lo que se mueve: la niebla (la misma de niebla_spink), las cosas escondidas
y el foco de la entrada, que titila.
"""

import math

import pygame

from interfaz.fondos.pintura import ANCHO, ALTO
from interfaz.fondos.pintura import mezclar, degradado, brillo, orillas_oscuras, mostrar
from interfaz.fondos import niebla_spink
from interfaz.fondos import sala_actrices

Y_PISO = 300

X_CORALINE = 476

PUERTA = pygame.Rect(574, 226, 24, Y_PISO - 226 - 6)
FOCO = (564, 212)

COLOR_NIEBLA = (118, 128, 136)
COLOR_ROSA = (226, 150, 172)
COLOR_ROSA_SOMBRA = (190, 116, 140)
COLOR_ROSA_RAYA = (206, 132, 156)
COLOR_TECHO = (92, 44, 42)
COLOR_BLANCO = (240, 232, 232)
COLOR_VIDRIO = (110, 128, 150)

# COSAS ESCONDIDAS EN LA NIEBLA: (x, y, que son, cada cuanto aparecen)
ESCONDIDAS = [
    (420, 200, "ojos", 0.0),
    (512, 170, "silueta", 2.2),
    (440, 250, "ojos", 3.6),
    (470, 150, "ojos", 1.3),
]

CAPAS = {}


def dibujar_paisaje(lienzo: pygame.Surface) -> None:

    """CIELO DE NIEBLA AL ATARDECER, LA CASA CON SU PUERTA Y EL CAMINO."""

    degradado(lienzo, pygame.Rect(0, 0, ANCHO, Y_PISO), (84, 92, 104), COLOR_NIEBLA, 20)

    # ARBOLES MUY BORROSOS
    for x, alto in [(400, 150), (452, 120)]:
        color = mezclar(COLOR_NIEBLA, (40, 48, 52), 0.35)
        pygame.draw.rect(lienzo, color, (x - 3, Y_PISO - alto + 50, 6, alto - 50))
        pygame.draw.ellipse(lienzo, color, (x - 28, Y_PISO - alto, 56, 70))

    dibujar_casa(lienzo)

    # FOCO DE LA ENTRADA (LA LUZ VA APARTE PORQUE TITILA)
    pygame.draw.rect(lienzo, (30, 28, 34), (FOCO[0] - 3, FOCO[1] - 6, 6, 10))

    # PASTO OSCURO Y CAMINO DE TIERRA HACIA LA PUERTA
    degradado(lienzo, pygame.Rect(0, Y_PISO, ANCHO, ALTO - Y_PISO), (44, 58, 52), (22, 30, 30), 5)
    pygame.draw.polygon(lienzo, (86, 82, 76), [(PUERTA.x - 8, Y_PISO), (PUERTA.right + 8, Y_PISO), (600, ALTO), (420, ALTO)])

    # VELO DE NIEBLA ENCIMA DE TODO LO DE ATRAS
    velo = pygame.Surface((ANCHO, Y_PISO + 20), pygame.SRCALPHA)
    velo.fill((150, 160, 170, 60))
    lienzo.blit(velo, (0, 0))


def ventana_blanca(lienzo: pygame.Surface, rect: tuple, encendida: bool) -> None:

    """VENTANA CON MARCO BLANCO Y CRUZ, APAGADA (VIDRIO GRIS) O CON LUZ CALIDA."""

    x, y, ancho, alto = rect

    pygame.draw.rect(lienzo, COLOR_BLANCO, (x - 2, y - 2, ancho + 4, alto + 4))
    pygame.draw.rect(lienzo, (230, 186, 110) if encendida else COLOR_VIDRIO, rect)
    pygame.draw.line(lienzo, COLOR_BLANCO, (x + ancho // 2, y), (x + ancho // 2, y + alto - 1))
    pygame.draw.line(lienzo, COLOR_BLANCO, (x, y + alto // 2), (x + ancho - 1, y + alto // 2))


def dibujar_casa(lienzo: pygame.Surface) -> None:

    """LA CASONA ROSA: TORRECITA A LA IZQUIERDA, TECHO CAFE A DOS AGUAS, PORCHE CON
    COLUMNAS BLANCAS, PUERTA ROJIZA Y LA ESCALERA DE AFUERA A LA DERECHA."""

    # TORRECITA CON TECHO PICUDO
    pygame.draw.rect(lienzo, COLOR_ROSA_SOMBRA, (500, 100, 28, Y_PISO - 100))
    pygame.draw.polygon(lienzo, COLOR_TECHO, [(494, 104), (514, 26), (534, 104)])
    pygame.draw.line(lienzo, COLOR_TECHO, (514, 26), (514, 18))
    ventana_blanca(lienzo, (507, 126, 14, 20), False)
    ventana_blanca(lienzo, (507, 170, 14, 20), False)

    # CUERPO PRINCIPAL CON TABLAS
    pygame.draw.rect(lienzo, COLOR_ROSA, (528, 100, ANCHO - 528, Y_PISO - 100))

    for y in range(104, Y_PISO, 5):
        pygame.draw.line(lienzo, COLOR_ROSA_RAYA, (528, y), (ANCHO, y))

    # TECHO A DOS AGUAS CON SU TRIANGULO ROSA Y LA VENTANITA DE ARRIBA
    pygame.draw.polygon(lienzo, COLOR_TECHO, [(518, 106), (590, 44), (662, 106)])
    pygame.draw.polygon(lienzo, COLOR_ROSA, [(540, 102), (590, 62), (640, 102)])
    pygame.draw.lines(lienzo, COLOR_BLANCO, False, [(540, 102), (590, 62), (640, 102)], 2)
    ventana_blanca(lienzo, (580, 76, 20, 18), False)
    pygame.draw.rect(lienzo, COLOR_TECHO, (518, 102, ANCHO - 518, 5))

    # VENTANAS DEL SEGUNDO PISO (UNA CON LUZ: ALGUIEN ESTA EN CASA)
    ventana_blanca(lienzo, (544, 120, 18, 26), False)
    ventana_blanca(lienzo, (604, 120, 18, 26), True)

    # PORCHE: TECHITO CAFE CON UN PICO SOBRE LA PUERTA
    pygame.draw.rect(lienzo, COLOR_TECHO, (512, 194, ANCHO - 512, 8))
    pygame.draw.polygon(lienzo, COLOR_TECHO, [(554, 198), (586, 174), (618, 198)])
    pygame.draw.polygon(lienzo, COLOR_ROSA, [(564, 196), (586, 180), (608, 196)])

    # SOMBRA DEBAJO DEL PORCHE, VENTANA DE ABAJO Y LA PUERTA ROJIZA
    sombra = pygame.Surface((ANCHO - 512, Y_PISO - 202), pygame.SRCALPHA)
    sombra.fill((40, 20, 40, 60))
    lienzo.blit(sombra, (512, 202))

    ventana_blanca(lienzo, (534, 226, 16, 36), False)

    pygame.draw.rect(lienzo, COLOR_BLANCO, PUERTA.inflate(6, 4).move(0, -2))
    pygame.draw.rect(lienzo, (206, 74, 104), PUERTA)
    pygame.draw.rect(lienzo, (170, 56, 84), PUERTA.inflate(-8, -16).move(0, -2), 1)
    pygame.draw.circle(lienzo, (240, 210, 120), (PUERTA.right - 5, PUERTA.centery), 1)

    # COLUMNAS BLANCAS Y PISO DEL PORCHE
    for x in [516, 556, 616]:
        pygame.draw.rect(lienzo, COLOR_BLANCO, (x, 202, 4, Y_PISO - 208))

    pygame.draw.rect(lienzo, (176, 150, 140), (510, Y_PISO - 8, ANCHO - 510, 8))
    pygame.draw.line(lienzo, COLOR_BLANCO, (510, Y_PISO - 8), (ANCHO, Y_PISO - 8))

    # ESCALONES DE MADERA FRENTE A LA PUERTA
    for i in range(2):
        pygame.draw.rect(lienzo, (130, 88, 64), (PUERTA.x - 6 - i * 5, Y_PISO - 6 + i * 5, PUERTA.width + 12 + i * 10, 5))

    # ESCALERA DE AFUERA, SUBIENDO POR LA ORILLA DERECHA
    for i in range(9):
        x = 620 + i * 3
        y = 190 - i * 9
        pygame.draw.line(lienzo, COLOR_TECHO, (x, y), (x + 10, y), 2)

    pygame.draw.line(lienzo, COLOR_TECHO, (620, 178), (650, 98), 2)
    pygame.draw.line(lienzo, COLOR_TECHO, (628, 194), (658, 114), 2)


def crear_fijo() -> pygame.Surface:

    lienzo = pygame.Surface((ANCHO, ALTO))

    dibujar_paisaje(lienzo)
    sala_actrices.dibujar_coraline(lienzo, X_CORALINE)
    orillas_oscuras(lienzo)

    return lienzo


def crear_luz_foco() -> pygame.Surface:

    capa = pygame.Surface((ANCHO, ALTO), pygame.SRCALPHA)
    brillo(capa, FOCO, 90, (255, 214, 140), 90)

    return capa


# --------------------------------------------------
# LO QUE SE MUEVE
# --------------------------------------------------

def dibujar_escondidas(lienzo: pygame.Surface, tiempo: float) -> None:

    """CADA COSA ESCONDIDA APARECE DESPACIO, SE QUEDA Y SE BORRA (CICLO DE 5 SEGUNDOS)."""

    for x, y, tipo, desfase in ESCONDIDAS:

        fase = (tiempo + desfase) % 5

        if fase > 2:
            continue

        alfa = int(math.sin(fase / 2 * math.pi) * 150)

        capa = pygame.Surface((30, 50), pygame.SRCALPHA)

        if tipo == "ojos":
            pygame.draw.rect(capa, (230, 60, 50, alfa), (9, 20, 3, 2))
            pygame.draw.rect(capa, (230, 60, 50, alfa), (17, 20, 3, 2))
        else:
            pygame.draw.ellipse(capa, (30, 34, 40, alfa // 2), (8, 4, 14, 14))
            pygame.draw.ellipse(capa, (30, 34, 40, alfa // 2), (5, 16, 20, 34))

        lienzo.blit(capa, (x - 15, y - 25))


def dibujar_foco(lienzo: pygame.Surface, tiempo: float) -> None:

    """EL FOCO DE LA ENTRADA TITILA DE VEZ EN CUANDO."""

    if "luz_foco" not in CAPAS:
        CAPAS["luz_foco"] = crear_luz_foco()

    fase = tiempo % 5
    apagado = 3.0 < fase < 3.3 and int(fase * 25) % 2 == 0

    if not apagado:
        lienzo.blit(CAPAS["luz_foco"], (0, 0))
        pygame.draw.circle(lienzo, (255, 236, 180), FOCO, 3)


def dibujar(ventana: pygame.Surface) -> None:

    """DIBUJA LA ESCENA COMPLETA EN LA VENTANA DEL JUEGO."""

    if "fijo" not in CAPAS:
        CAPAS["fijo"] = crear_fijo()

    tiempo = pygame.time.get_ticks() / 1000

    lienzo = CAPAS["fijo"].copy()

    dibujar_escondidas(lienzo, tiempo)
    dibujar_foco(lienzo, tiempo)
    niebla_spink.dibujar_niebla(lienzo, tiempo)

    mostrar(ventana, lienzo)
