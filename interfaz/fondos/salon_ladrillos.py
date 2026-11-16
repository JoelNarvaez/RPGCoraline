"""FONDO DIBUJADO CON CODIGO: LA PUERTA ABIERTA Y LA PARED DE LADRILLOS.

Es el mismo salon de salon_puerta.py, pero la mama ya abrio la puerta
pequena: detras solo hay ladrillos rojos. Ella tiene la llave negra en la
mano (en el marco de la cocina solo queda el clavo) y Coraline mira desde
atras. Se usa en cap01_n05.
"""

import pygame

from interfaz.fondos.pintura import ANCHO, ALTO
from interfaz.fondos.pintura import mezclar, brillo, orillas_oscuras, armar_sprite, mostrar
from interfaz.fondos import salon_puerta
from interfaz.minijuegos import recorrido

PUERTA = salon_puerta.PUERTA
Y_PISO = salon_puerta.Y_PISO

X_MAMA = 404
X_CORALINE = 336

CAPAS = {}

COLORES_MAMA = {
    "O": (24, 20, 30),      # contorno
    "C": (32, 26, 36),      # pelo negro
    "c": (20, 16, 24),      # pelo en sombra
    "d": (78, 70, 92),      # brillo del pelo
    "S": (240, 204, 178),   # piel
    "s": (210, 166, 142),   # piel en sombra
    "E": (30, 26, 40),      # ojo
    "G": (166, 80, 46),     # abrigo color oxido
    "g": (122, 56, 34),     # abrigo en sombra
    "T": (228, 208, 172),   # pantalon crema
    "t": (192, 172, 140),   # pantalon en sombra
    "Z": (104, 46, 34),     # zapatos cafes
    "K": (16, 14, 18),      # llave negra
}

# LA MAMA MIRA A LA DERECHA (HACIA LA PUERTA) CON LA LLAVE EN LA MANO
MAMA = [
    ".......OOOOOO...........",
    ".....OOCCCCCCOO.........",
    "....OCCddCCCCCCO........",
    "...OCCdCCCCCCCCCO.......",
    "...OCCCCCCCCCCCCO.......",
    "..OcCCCCCCCcSSSSO.......",
    "..OcCCCCCCcSSSSSSO......",
    "..OcCCCCCcSSSSESSO......",
    "..OcCCCCCcSSSSESSSO.....",
    "..OcCCCCCcsSSSSSSO......",
    "..OcCCCCCCcsSSSsSO......",
    "..OccCCCCCOcsSSSO.......",
    "...OccCCCO.OssO.........",
    "....OOOOO..OssO.........",
    "....OGGGGGGGGGGO........",
    "...OGGGGGGGGGGGGO.......",
    "..OGgGGGGGGGGGGGGO......",
    "..OGgGGGGGGGGGGGGO......",
    "..OGgGGGGGGGGGGGGGO.....",
    "..OGgGGGGGGGGGOOSSSO....",
    "..OGgGGGGGGGGGOSSKKKKO..",
    "..OGgGGGGGGGGGGOSKOOKO..",
    "..OGgGGGGGGGGGGOOK..OO..",
    "..OGgGGGGGGGGGGGO.......",
    "..OggGGGGGGGGGGGO.......",
    "..OggGGGGGGGGGGGO.......",
    "..OggGGGGGGGGGGGO.......",
    "..OOgggggggggggOO.......",
    "...OTTTTTTTTTTTO........",
] + ["...OTTTtTTOTTTTTO......."] * 11 + [
    "...OZZZZZZOZZZZZO.......",
    "..OZZZZZZZOZZZZZZO......",
    "..OOOOOOOOOOOOOOOO......",
]


# --------------------------------------------------
# PARTE FIJA
# --------------------------------------------------

def dibujar_ladrillos(lienzo: pygame.Surface) -> None:

    """EL HUECO DE LA PUERTA TAPADO CON LADRILLOS ROJOS."""

    pygame.draw.rect(lienzo, (18, 38, 42), PUERTA.inflate(8, 6).move(0, -3))
    pygame.draw.rect(lienzo, (66, 56, 54), PUERTA)   # mezcla entre ladrillos

    tonos = [(150, 58, 48), (132, 48, 40), (166, 70, 54), (122, 46, 42)]

    alto_ladrillo = 6
    ancho_ladrillo = 14

    fila = 0

    for y in range(PUERTA.y, PUERTA.bottom, alto_ladrillo):

        desfase = 0 if fila % 2 == 0 else -ancho_ladrillo // 2

        columna = 0

        for x in range(PUERTA.x + desfase, PUERTA.right, ancho_ladrillo):

            ladrillo = pygame.Rect(x + 1, y + 1, ancho_ladrillo - 2, alto_ladrillo - 2).clip(PUERTA)

            if ladrillo.width > 0:

                tono = tonos[(fila * 3 + columna) % 4]

                pygame.draw.rect(lienzo, tono, ladrillo)
                pygame.draw.line(lienzo, mezclar(tono, (255, 220, 200), 0.2), ladrillo.topleft,
                                 (ladrillo.right - 1, ladrillo.y))

            columna = columna + 1

        fila = fila + 1

    # SOMBRA ARRIBA DEL HUECO: LA PARED TIENE GROSOR
    sombra = pygame.Surface((PUERTA.width, 10), pygame.SRCALPHA)

    for i in range(10):
        pygame.draw.line(sombra, (0, 0, 0, 120 - i * 12), (0, i), (PUERTA.width, i))

    lienzo.blit(sombra, PUERTA.topleft)


def dibujar_hoja_abierta(lienzo: pygame.Surface) -> None:

    """LA HOJA DE LA PUERTA ABIERTA HACIA EL FRENTE, VISTA DE LADO (BISAGRA A LA DERECHA)."""

    madera = (86, 76, 74)
    clara = (112, 100, 96)
    oscura = (50, 44, 44)

    x = PUERTA.right
    arriba = PUERTA.y
    abajo = PUERTA.bottom
    abre = 26   # que tanto sale hacia el frente

    hoja = [(x, arriba), (x + abre, arriba + 8), (x + abre, abajo + 8), (x, abajo)]

    pygame.draw.polygon(lienzo, madera, hoja)
    pygame.draw.polygon(lienzo, oscura, hoja, 1)

    # TABLERO EN ARCO APLASTADO POR LA PERSPECTIVA
    pygame.draw.polygon(
        lienzo,
        clara,
        [(x + 6, arriba + 16), (x + abre - 6, arriba + 20), (x + abre - 6, abajo - 4), (x + 6, abajo - 8)],
        1
    )

    # CANTO DE LA PUERTA Y MANIJA DEL OTRO LADO
    pygame.draw.line(lienzo, clara, (x + abre, arriba + 8), (x + abre, abajo + 8), 2)
    pygame.draw.circle(lienzo, (150, 130, 90), (x + abre - 4, (arriba + abajo) // 2 + 6), 2)

    # SOMBRA DE LA HOJA EN EL PISO
    sombra = pygame.Surface((ANCHO, ALTO), pygame.SRCALPHA)
    pygame.draw.polygon(sombra, (0, 0, 0, 80), [(x, abajo), (x + abre, abajo + 8), (x + abre + 18, abajo + 8),
                                                 (x + 10, abajo)])
    lienzo.blit(sombra, (0, 0))


def dibujar_personaje(lienzo: pygame.Surface, sprite: pygame.Surface, x: int) -> None:

    """DIBUJA UN SPRITE AL DOBLE DE TAMANO, PARADO EN EL PISO, CON SOMBRA."""

    grande = pygame.transform.scale(sprite, (sprite.get_width() * 2, sprite.get_height() * 2))

    y_pies = Y_PISO + 16

    sombra = pygame.Surface((grande.get_width() - 4, 8), pygame.SRCALPHA)
    pygame.draw.ellipse(sombra, (0, 0, 0, 110), sombra.get_rect())
    lienzo.blit(sombra, (x + 2, y_pies - 4))

    lienzo.blit(grande, (x, y_pies - grande.get_height()))


def crear_fijo() -> pygame.Surface:

    lienzo = pygame.Surface((ANCHO, ALTO))

    salon_puerta.dibujar_pared(lienzo)
    salon_puerta.dibujar_piso(lienzo)
    salon_puerta.dibujar_cocina(lienzo, False)
    dibujar_ladrillos(lienzo)
    dibujar_hoja_abierta(lienzo)

    dibujar_personaje(lienzo, recorrido.sprite_coraline("quieta", True), X_CORALINE)
    dibujar_personaje(lienzo, armar_sprite(MAMA, COLORES_MAMA), X_MAMA)

    # LUZ CALIDA DE LA COCINA Y UNA LUZ FRIA SOBRE LOS LADRILLOS
    luz = pygame.Surface((ANCHO, ALTO), pygame.SRCALPHA)
    pygame.draw.polygon(
        luz,
        (255, 196, 120, 34),
        [(salon_puerta.COCINA.x, Y_PISO), (ANCHO, Y_PISO), (ANCHO, ALTO), (salon_puerta.COCINA.x - 130, ALTO)]
    )
    lienzo.blit(luz, (0, 0))

    brillo(lienzo, (salon_puerta.COCINA.x - 10, salon_puerta.COCINA.centery + 40), 130, (255, 196, 120), 95)
    brillo(lienzo, PUERTA.center, 80, (150, 225, 225), 70)

    orillas_oscuras(lienzo)

    return lienzo


# --------------------------------------------------
# LO QUE SE MUEVE
# --------------------------------------------------

def dibujar_destello_llave(lienzo: pygame.Surface, tiempo: float) -> None:

    """LA LLAVE EN LA MANO DE LA MAMA BRILLA CADA 3 SEGUNDOS."""

    if tiempo % 3 < 0.4:

        # POSICION DE LA LLAVE DENTRO DEL SPRITE (COLUMNA 20, FILA 20), AL DOBLE
        x = X_MAMA + 20 * 2
        y = Y_PISO + 16 - len(MAMA) * 2 + 20 * 2

        pygame.draw.line(lienzo, (255, 250, 220), (x - 3, y), (x + 3, y))
        pygame.draw.line(lienzo, (255, 250, 220), (x, y - 3), (x, y + 3))


def dibujar(ventana: pygame.Surface) -> None:

    """DIBUJA LA ESCENA COMPLETA EN LA VENTANA DEL JUEGO."""

    if "fijo" not in CAPAS:
        CAPAS["fijo"] = crear_fijo()

    tiempo = pygame.time.get_ticks() / 1000

    lienzo = CAPAS["fijo"].copy()

    salon_puerta.dibujar_polvo(lienzo, tiempo)
    dibujar_destello_llave(lienzo, tiempo)

    mostrar(ventana, lienzo)
