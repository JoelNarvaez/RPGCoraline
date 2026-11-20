"""FONDO DIBUJADO CON CODIGO: CORALINE ENCERRADA DETRAS DEL ESPEJO.

Un hueco diminuto, apenas mas alto que Coraline, en medio de la oscuridad.
La pared derecha es el vidrio frio del espejo: del otro lado se adivina,
muy oscuro, el pasillo lila de espejo_otra_madre.py. No hay puerta ni manija.
Desde la pared de la izquierda sale una mano palida y helada que le roza la
mano. Se usa en cap07_n01 y en su rama cap07_r01.

Tambien son las partes del resto del capitulo 7 (ninos_fantasma,
almas_perdidas, advertencia_fantasmas y beso_fantasma): el hueco
(dibujar_hueco) y los tres ninos fantasma (dibujar_fantasma), que son: el
nino de capa y peluca blanca, la nina de cofia y el mas pequeno, que ya casi
no tiene forma.

Lo que se mueve: la mano palida que se acerca y se retira, la sombra de la
otra madre que pasa del otro lado del vidrio y motitas de polvo en la luz.
"""

import math

import pygame

from interfaz.fondos.pintura import ANCHO, ALTO
from interfaz.fondos.pintura import mezclar, brillo, orillas_oscuras, mostrar
from interfaz.fondos import sala_actrices

Y_PISO = 300

HUECO = pygame.Rect(420, 196, 104, Y_PISO - 196)              # el espacio donde cabe Coraline
VIDRIO = pygame.Rect(HUECO.right, HUECO.y, 8, HUECO.height)   # la pared de vidrio (atras del espejo)
PASILLO = pygame.Rect(VIDRIO.right, HUECO.y - 20, ANCHO - VIDRIO.right, HUECO.height + 20)

X_CORALINE = 484

COLOR_NEGRO = (8, 6, 12)
COLOR_PARED = (30, 24, 30)
COLOR_FANTASMA = (226, 234, 248)
COLOR_FANTASMA_SOMBRA = (168, 184, 214)
COLOR_FANTASMA_OJOS = (54, 62, 96)

CAPAS = {}
SPRITES_FANTASMA = {}


# --------------------------------------------------
# EL HUECO (TAMBIEN LO USAN LAS DEMAS ESCENAS DEL CAPITULO 7)
# --------------------------------------------------

def dibujar_hueco(lienzo: pygame.Surface, paredes: float) -> None:

    """TODO NEGRO, EL HUECO CON PAREDES DE TABLAS Y EL VIDRIO A LA DERECHA.

    paredes: que tanto se ven las tablas (1 = como en cap07_n01; menos cuando
    los fantasmas llenan la oscuridad y el hueco parece no tener orillas).
    """

    lienzo.fill(COLOR_NEGRO)

    # DEL OTRO LADO DEL VIDRIO, EL PASILLO LILA APENAS SE ADIVINA (CON MENOS paredes, CASI NADA,
    # PARA QUE LOS FANTASMAS FLOTEN EN LA OSCURIDAD Y NO PAREZCA QUE ESTAN EN EL PASILLO)
    lila = mezclar(COLOR_NEGRO, (54, 38, 60), paredes ** 2)

    for x in range(PASILLO.x, PASILLO.right):
        lejos = (x - PASILLO.x) / PASILLO.width
        color = mezclar(lila, COLOR_NEGRO, lejos)
        pygame.draw.line(lienzo, color, (x, PASILLO.y), (x, PASILLO.bottom))

    # LA ORILLA DE ARRIBA SE FUNDE CON LO NEGRO
    for i in range(24):
        pygame.draw.line(lienzo, mezclar(COLOR_NEGRO, lila, i / 24 * 0.5), (PASILLO.x, PASILLO.y + i), (PASILLO.right, PASILLO.y + i))

    pygame.draw.rect(lienzo, mezclar(COLOR_NEGRO, (46, 32, 30), paredes * 0.7), (PASILLO.x, Y_PISO - 4, PASILLO.width, 4))

    # TABLAS DE LAS PAREDES, EL TECHO Y EL PISO DEL HUECO
    tabla = mezclar(COLOR_NEGRO, COLOR_PARED, paredes)
    junta = mezclar(COLOR_NEGRO, (18, 14, 18), paredes)

    pygame.draw.rect(lienzo, tabla, HUECO)

    for y in range(HUECO.y + 10, HUECO.bottom, 13):
        pygame.draw.line(lienzo, junta, (HUECO.x, y), (HUECO.right - 1, y))
        x = HUECO.x + (y * 7) % 60 + 10
        pygame.draw.line(lienzo, junta, (x, y), (x, min(y + 13, HUECO.bottom - 1)))

    orilla = mezclar(COLOR_NEGRO, (52, 42, 48), paredes)
    pygame.draw.rect(lienzo, orilla, HUECO.inflate(6, 6), 3)

    # EL VIDRIO: FRIO, AZULADO, CON UN BRILLO DIAGONAL
    pygame.draw.rect(lienzo, (70, 84, 110), VIDRIO)
    pygame.draw.line(lienzo, (150, 170, 200), (VIDRIO.x + 2, VIDRIO.y + 30), (VIDRIO.x + 5, VIDRIO.y + 10))
    pygame.draw.line(lienzo, (150, 170, 200), (VIDRIO.x + 2, VIDRIO.y + 70), (VIDRIO.x + 5, VIDRIO.y + 56))
    pygame.draw.line(lienzo, (110, 126, 160), (VIDRIO.x, VIDRIO.y), (VIDRIO.x, VIDRIO.bottom - 1))


def luz_del_vidrio(lienzo: pygame.Surface) -> None:

    """LA POQUITA LUZ QUE ENTRA POR EL VIDRIO, FRIA Y AZULADA."""

    brillo(lienzo, (VIDRIO.x, VIDRIO.centery), 70, (110, 130, 180), 40)


# --------------------------------------------------
# LOS TRES NINOS FANTASMA
# --------------------------------------------------

def desvanecer_abajo(sprite: pygame.Surface, desde: float) -> None:

    """LA PARTE DE ABAJO DEL FANTASMA SE VA HACIENDO TRANSPARENTE (NO TIENEN PIES)."""

    alto = sprite.get_height()
    mascara = pygame.Surface(sprite.get_size(), pygame.SRCALPHA)

    for y in range(alto):
        avance = y / alto
        alfa = 255 if avance < desde else int(255 * max(0.0, 1 - (avance - desde) / (1 - desde)))
        pygame.draw.line(mascara, (255, 255, 255, alfa), (0, y), (sprite.get_width(), y))

    sprite.blit(mascara, (0, 0), special_flags=pygame.BLEND_RGBA_MULT)


def cara_triste(sprite: pygame.Surface, x: int, y: int) -> None:

    """OJOS HUNDIDOS Y BOCA CHIQUITA HACIA ABAJO. (x, y) ES EL CENTRO DE LA CARA."""

    pygame.draw.rect(sprite, COLOR_FANTASMA_OJOS, (x - 5, y - 2, 2, 3))
    pygame.draw.rect(sprite, COLOR_FANTASMA_OJOS, (x + 3, y - 2, 2, 3))
    pygame.draw.line(sprite, COLOR_FANTASMA_OJOS, (x - 1, y + 5), (x + 1, y + 5))
    sprite.set_at((x - 2, y + 6), COLOR_FANTASMA_OJOS)
    sprite.set_at((x + 2, y + 6), COLOR_FANTASMA_OJOS)


def sprite_fantasma(quien: str) -> pygame.Surface:

    """ARMA (UNA SOLA VEZ) EL DIBUJO DE UN FANTASMA: "capa", "cofia" O "pequeno"."""

    if quien in SPRITES_FANTASMA:
        return SPRITES_FANTASMA[quien]

    sprite = pygame.Surface((40, 90), pygame.SRCALPHA)
    blanco = (246, 248, 252)

    if quien == "capa":
        # CAPA ANCHA, CASACA, CUELLO DE ENCAJE Y PELUCA BLANCA CON RIZOS Y COLETA
        pygame.draw.polygon(sprite, COLOR_FANTASMA_SOMBRA, [(8, 26), (32, 26), (39, 88), (1, 88)])
        pygame.draw.polygon(sprite, COLOR_FANTASMA, [(13, 26), (27, 26), (29, 88), (11, 88)])
        pygame.draw.polygon(sprite, blanco, [(15, 26), (25, 26), (20, 36)])
        pygame.draw.line(sprite, COLOR_FANTASMA_SOMBRA, (20, 38), (20, 80))
        pygame.draw.ellipse(sprite, COLOR_FANTASMA, (12, 6, 16, 20))
        pygame.draw.ellipse(sprite, blanco, (10, 1, 20, 9))
        for y in [10, 16, 22]:
            pygame.draw.circle(sprite, blanco, (10, y), 3)
            pygame.draw.circle(sprite, blanco, (30, y), 3)
        pygame.draw.rect(sprite, COLOR_FANTASMA_OJOS, (18, 2, 4, 2))           # monito de la coleta
        cara_triste(sprite, 20, 15)
        desvanecer_abajo(sprite, 0.55)

    elif quien == "cofia":
        # VESTIDO LARGO CON DELANTAL Y UNA COFIA REDONDA CON OLANES ALREDEDOR DE LA CARA
        pygame.draw.polygon(sprite, COLOR_FANTASMA_SOMBRA, [(11, 28), (29, 28), (37, 88), (3, 88)])
        pygame.draw.rect(sprite, COLOR_FANTASMA, (14, 34, 12, 46))
        pygame.draw.ellipse(sprite, COLOR_FANTASMA, (6, 26, 8, 10))            # mangas abombadas
        pygame.draw.ellipse(sprite, COLOR_FANTASMA, (26, 26, 8, 10))
        pygame.draw.ellipse(sprite, blanco, (6, 0, 28, 28))
        for i in range(10):
            angulo = i / 10 * math.pi * 2
            sprite.set_at((20 + int(math.cos(angulo) * 13), 14 + int(math.sin(angulo) * 13)), COLOR_FANTASMA_SOMBRA)
        pygame.draw.ellipse(sprite, COLOR_FANTASMA, (13, 7, 14, 17))
        pygame.draw.line(sprite, COLOR_FANTASMA_SOMBRA, (14, 24), (18, 30))     # cintas de la cofia
        pygame.draw.line(sprite, COLOR_FANTASMA_SOMBRA, (26, 24), (22, 30))
        cara_triste(sprite, 20, 15)
        desvanecer_abajo(sprite, 0.5)

    else:
        # EL MAS PEQUENO: CASI NO TIENE FORMA, SOLO UNA CABECITA Y UN CUERPO DE NIEBLA
        pygame.draw.ellipse(sprite, COLOR_FANTASMA_SOMBRA, (10, 46, 20, 40))
        pygame.draw.circle(sprite, COLOR_FANTASMA, (20, 40), 8)
        cara_triste(sprite, 20, 40)
        desvanecer_abajo(sprite, 0.6)

    SPRITES_FANTASMA[quien] = sprite

    return sprite


def dibujar_fantasma(lienzo: pygame.Surface, quien: str, x: int, y: int, tiempo: float, alfa: int) -> None:

    """PEGA UN FANTASMA QUE FLOTA SUBIENDO Y BAJANDO. x ES EL CENTRO Y y DONDE EMPIEZA SU CABEZA."""

    sprite = sprite_fantasma(quien).copy()
    sprite.set_alpha(alfa)

    flota = int(math.sin(tiempo * 1.4 + x * 0.05) * 3)

    lienzo.blit(sprite, (x - sprite.get_width() // 2, y + flota))


# --------------------------------------------------
# ESTA ESCENA (cap07_n01)
# --------------------------------------------------

def crear_fijo() -> pygame.Surface:

    lienzo = pygame.Surface((ANCHO, ALTO))

    dibujar_hueco(lienzo, 1)
    luz_del_vidrio(lienzo)
    sala_actrices.dibujar_coraline(lienzo, X_CORALINE, False)
    orillas_oscuras(lienzo)

    return lienzo


def dibujar_mano_palida(lienzo: pygame.Surface, tiempo: float) -> None:

    """UNA MANO PALIDA SALE DE LA PARED IZQUIERDA, ROZA LA MANO DE CORALINE Y SE RETIRA."""

    avance = (math.sin(tiempo * 0.9) + 1) / 2                      # 0 = metida en la pared, 1 = tocandola
    x = HUECO.x + int(avance * 40)
    y = 252

    capa = pygame.Surface((ANCHO, ALTO), pygame.SRCALPHA)
    color = (*COLOR_FANTASMA, 170)

    pygame.draw.line(capa, (*COLOR_FANTASMA_SOMBRA, 120), (HUECO.x, y + 2), (x - 4, y + 1), 4)   # brazo
    pygame.draw.ellipse(capa, color, (x - 6, y - 3, 9, 8))

    for i in range(4):                                                                       # dedos largos
        pygame.draw.line(capa, color, (x + 2, y - 2 + i * 2), (x + 8 + (i % 2), y - 3 + i * 2))

    lienzo.blit(capa, (0, 0))


def dibujar_sombra_pasillo(lienzo: pygame.Surface, tiempo: float) -> None:

    """CADA 9 SEGUNDOS, LA SILUETA DE LA OTRA MADRE PASA DEL OTRO LADO DEL VIDRIO."""

    fase = tiempo % 9

    if fase > 3:
        return

    x = PASILLO.right + 10 - int(fase / 3 * (PASILLO.width + 40))
    sombra = (20, 14, 22)

    # SOLO SE VE DEL OTRO LADO DEL VIDRIO
    vieja = lienzo.get_clip()
    lienzo.set_clip(PASILLO)

    pygame.draw.circle(lienzo, sombra, (x, PASILLO.y + 40), 9)                               # cabeza con melena
    pygame.draw.rect(lienzo, sombra, (x - 2, PASILLO.y + 48, 4, 8))                         # cuello largo
    pygame.draw.polygon(lienzo, sombra, [(x - 8, PASILLO.y + 56), (x + 8, PASILLO.y + 56),
                                         (x + 16, Y_PISO - 6), (x - 16, Y_PISO - 6)])

    lienzo.set_clip(vieja)


def dibujar_polvo(lienzo: pygame.Surface, tiempo: float) -> None:

    """MOTITAS DE POLVO QUE FLOTAN EN LA LUZ DEL VIDRIO."""

    for i in range(8):

        x = VIDRIO.x - 6 - (i * 11 + int(tiempo * 2)) % 50
        y = HUECO.y + 10 + (i * 17) % 80 + int(math.sin(tiempo * 0.8 + i) * 4)

        lienzo.set_at((x, y), (120, 136, 170))


def dibujar(ventana: pygame.Surface) -> None:

    """DIBUJA LA ESCENA COMPLETA EN LA VENTANA DEL JUEGO."""

    if "fijo" not in CAPAS:
        CAPAS["fijo"] = crear_fijo()

    tiempo = pygame.time.get_ticks() / 1000

    lienzo = CAPAS["fijo"].copy()

    dibujar_sombra_pasillo(lienzo, tiempo)
    dibujar_polvo(lienzo, tiempo)
    dibujar_mano_palida(lienzo, tiempo)

    mostrar(ventana, lienzo)
