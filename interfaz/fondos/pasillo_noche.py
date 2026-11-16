"""FONDO DIBUJADO CON CODIGO: EL PASILLO DE NOCHE Y LA SOMBRA.

Coraline no puede dormir. Se asoma desde la puerta de su cuarto en pijama
(es la Coraline chica de personajes.py con otros colores: la pijama sale del
impermeable, el pantalon de las medias y las pantuflas de las botas) y ve una sombra cruzar el pasillo y meterse al salon. En lo oscuro del salon
parpadean ojitos rojos (el sueno de las criaturas). Se usa en cap01_n06.

Lo que se mueve: la sombra cruza el piso, los ojitos rojos parpadean y las
nubes tapan la luna de vez en cuando.
"""

import math

import pygame

from interfaz.fondos.pintura import ANCHO, ALTO
from interfaz.fondos.pintura import mezclar, degradado, brillo, orillas_oscuras, mostrar, armar_sprite
from interfaz.fondos import personajes

Y_PISO = 330

CUARTO = pygame.Rect(404, 150, 66, Y_PISO - 150)      # puerta abierta del cuarto de Coraline
SALON = pygame.Rect(566, 146, 62, Y_PISO - 146)       # entrada oscura del salon
VENTANA = pygame.Rect(492, 52, 44, 64)                # ventana alta con la luna

X_CORALINE = 443          # centro de sus pies
# PIJAMA: EN CADA PARTE DEL CUERPO, QUE LETRA DEL SPRITE SE CAMBIA POR CUAL.
# LAS LETRAS NUEVAS (MINUSCULAS) SON LOS COLORES DE LA PIJAMA.
FILA_CUERPO = 33          # de aqui para abajo ya no es la cabeza
FILA_PIERNAS = 68
FILA_PIES = 79

CAMBIOS_PIJAMA = {"B": "b", "C": "c", "T": "t", "W": "t", "H": "t", "J": "j", "R": "j", "U": "u"}
CAMBIOS_PANTALON = {"I": "i", "K": "k", "S": "k", "E": "e"}
CAMBIOS_PANTUFLAS = {"B": "p", "C": "q", "H": "r", "J": "r", "U": "u", "F": "u"}

COLORES_PIJAMA = {
    "b": (196, 212, 236),   # pijama azul cielo
    "c": (156, 176, 216),   # pijama en sombra
    "t": (120, 140, 190),   # pliegues
    "j": (96, 112, 166),    # pliegues oscuros
    "u": (236, 242, 252),   # brillos
    "i": (120, 140, 190),   # pantalon: raya oscura
    "k": (210, 222, 242),   # pantalon: raya clara
    "e": (80, 100, 160),    # pantalon: raya azul
    "p": (236, 176, 196),   # pantuflas rosas
    "q": (210, 146, 170),
    "r": (170, 104, 130),
}



# OJITOS ROJOS DENTRO DEL SALON: (x, y, desfase del parpadeo)
OJITOS = [(580, 236, 0.0), (604, 262, 1.3), (590, 296, 2.1), (614, 218, 3.4)]

CAPAS = {}


# --------------------------------------------------
# PARTE FIJA
# --------------------------------------------------

def dibujar_pasillo(lienzo: pygame.Surface) -> None:

    """PARED AZUL OSCURO CON LAMBRIN, PISO DE MADERA Y MOLDURA."""

    degradado(lienzo, pygame.Rect(0, 0, ANCHO, Y_PISO), (8, 10, 22), (30, 36, 62), 26)

    pygame.draw.rect(lienzo, (6, 6, 14), (0, 0, ANCHO, 12))
    pygame.draw.rect(lienzo, (26, 30, 50), (0, 12, ANCHO, 2))

    # LAMBRIN
    pygame.draw.rect(lienzo, (20, 24, 42), (0, 270, ANCHO, Y_PISO - 270))
    pygame.draw.line(lienzo, (44, 50, 80), (0, 269), (ANCHO, 269))

    for x in range(8, ANCHO, 44):
        pygame.draw.rect(lienzo, (14, 16, 30), (x, 276, 36, 46), 1)

    # PISO DE MADERA OSCURA
    degradado(lienzo, pygame.Rect(0, Y_PISO, ANCHO, ALTO - Y_PISO), (26, 22, 30), (10, 8, 14), 4)

    for y in [Y_PISO + 6, Y_PISO + 14, Y_PISO + 24]:
        pygame.draw.line(lienzo, (16, 12, 20), (0, y), (ANCHO, y))

    # CUADRO EN LA PARED (CASI NO SE VE EN LA OSCURIDAD)
    pygame.draw.rect(lienzo, (40, 36, 44), (520, 150, 28, 36), 2)


def dibujar_ventana(lienzo: pygame.Surface) -> None:

    """VENTANA ALTA CON CIELO DE NOCHE, LUNA Y PALILLOS."""

    pygame.draw.rect(lienzo, (60, 64, 90), VENTANA.inflate(8, 8))
    degradado(lienzo, VENTANA, (16, 22, 52), (40, 52, 96), 6)

    pygame.draw.circle(lienzo, (226, 230, 240), (VENTANA.x + 30, VENTANA.y + 18), 8)
    pygame.draw.circle(lienzo, (190, 196, 214), (VENTANA.x + 27, VENTANA.y + 16), 2)

    pygame.draw.line(lienzo, (60, 64, 90), (VENTANA.centerx, VENTANA.y), (VENTANA.centerx, VENTANA.bottom), 2)
    pygame.draw.line(lienzo, (60, 64, 90), (VENTANA.x, VENTANA.centery), (VENTANA.right, VENTANA.centery), 2)


def dibujar_luz_de_luna(lienzo: pygame.Surface) -> None:

    """LA LUZ DE LA LUNA BAJA EN DIAGONAL Y CAE SOBRE EL PISO."""

    luz = pygame.Surface((ANCHO, ALTO), pygame.SRCALPHA)

    pygame.draw.polygon(
        luz,
        (150, 170, 230, 22),
        [(VENTANA.x, VENTANA.bottom), (VENTANA.right, VENTANA.bottom), (VENTANA.right + 40, Y_PISO + 20),
         (VENTANA.x + 4, Y_PISO + 20)]
    )

    pygame.draw.polygon(
        luz,
        (170, 190, 240, 40),
        [(VENTANA.x + 6, Y_PISO + 2), (VENTANA.right + 34, Y_PISO + 2), (VENTANA.right + 48, ALTO),
         (VENTANA.x + 10, ALTO)]
    )

    lienzo.blit(luz, (0, 0))


def dibujar_puertas(lienzo: pygame.Surface) -> None:

    """PUERTA DEL CUARTO CON LUZ DE LAMPARITA Y ENTRADA NEGRA DEL SALON."""

    # CUARTO DE CORALINE: MARCO Y LUZ CALIDA MUY TENUE ADENTRO
    pygame.draw.rect(lienzo, (44, 46, 70), CUARTO.inflate(10, 6).move(0, -3))
    degradado(lienzo, CUARTO, (40, 30, 40), (78, 56, 54), 8)

    # HOJA DE LA PUERTA ABIERTA HACIA ADENTRO (SE VE DE LADO A LA IZQUIERDA)
    pygame.draw.polygon(lienzo, (34, 30, 40), [(CUARTO.x, CUARTO.y), (CUARTO.x + 14, CUARTO.y + 8),
                                               (CUARTO.x + 14, CUARTO.bottom - 6), (CUARTO.x, CUARTO.bottom)])

    # SALON: MARCO Y OSCURIDAD TOTAL
    pygame.draw.rect(lienzo, (40, 42, 64), SALON.inflate(10, 6).move(0, -3))
    pygame.draw.rect(lienzo, (2, 2, 6), SALON)


def cambiar_letras(fila: str, cambios: dict) -> str:

    """REGRESA LA FILA CON LAS LETRAS CAMBIADAS SEGUN EL DICCIONARIO."""

    nueva = ""

    for letra in fila:
        nueva = nueva + cambios.get(letra, letra)

    return nueva


def sprite_pijama() -> pygame.Surface:

    """LA CORALINE CHICA CON LA PIJAMA: MISMA CABEZA, OTROS COLORES DEL CUELLO PARA ABAJO."""

    filas = []

    for i in range(len(personajes.CORALINE_FILAS)):

        fila = personajes.CORALINE_FILAS[i]

        if i >= FILA_PIES:
            fila = cambiar_letras(fila, CAMBIOS_PANTUFLAS)
        elif i >= FILA_PIERNAS:
            fila = cambiar_letras(fila, CAMBIOS_PANTALON)
        elif i >= FILA_CUERPO:
            fila = cambiar_letras(fila, CAMBIOS_PIJAMA)

        filas.append(fila)

    colores = dict(personajes.CORALINE_COLORES)
    colores.update(COLORES_PIJAMA)

    return armar_sprite(filas, colores)


def dibujar_coraline(lienzo: pygame.Surface) -> None:

    """CORALINE EN PIJAMA PARADA EN LA PUERTA, MIRANDO HACIA EL SALON."""

    sprite = sprite_pijama()

    sombra = pygame.Surface((sprite.get_width() + 6, 6), pygame.SRCALPHA)
    pygame.draw.ellipse(sombra, (0, 0, 0, 120), sombra.get_rect())
    lienzo.blit(sombra, (X_CORALINE - sombra.get_width() // 2, Y_PISO - 4))

    lienzo.blit(sprite, (X_CORALINE - sprite.get_width() // 2, Y_PISO - sprite.get_height()))


def crear_fijo() -> pygame.Surface:

    lienzo = pygame.Surface((ANCHO, ALTO))

    dibujar_pasillo(lienzo)
    dibujar_ventana(lienzo)
    dibujar_puertas(lienzo)
    dibujar_luz_de_luna(lienzo)
    dibujar_coraline(lienzo)

    brillo(lienzo, (CUARTO.centerx, CUARTO.centery + 20), 70, (255, 180, 120), 40)
    brillo(lienzo, (VENTANA.centerx, VENTANA.centery), 70, (170, 190, 240), 50)

    orillas_oscuras(lienzo)

    return lienzo


# --------------------------------------------------
# LO QUE SE MUEVE
# --------------------------------------------------

def dibujar_sombra(lienzo: pygame.Surface, tiempo: float) -> None:

    """LA SOMBRA CRUZA EL PISO Y SE METE AL SALON. TARDA 4 SEGUNDOS Y ESPERA 3."""

    fase = tiempo % 7

    if fase > 4:
        return

    avance = fase / 4
    x = int(480 + (SALON.centerx - 480) * avance)
    y = Y_PISO - 6 + int(math.sin(tiempo * 9) * 2)

    capa = pygame.Surface((ANCHO, ALTO), pygame.SRCALPHA)

    # CUERPO DE LA SOMBRA: VARIAS MANCHAS QUE SE ESTIRAN AL CORRER
    for i in range(5):
        dx = i * 7 - 14
        alto = 14 - abs(dx) // 3
        pygame.draw.ellipse(capa, (0, 0, 4, 190), (x + dx - 8, y - alto, 18, alto + 4))

    # COLITA Y PATITAS
    pygame.draw.line(capa, (0, 0, 4, 180), (x - 20, y - 2), (x - 34, y - 8 + int(math.sin(tiempo * 12) * 3)), 2)

    lienzo.blit(capa, (0, 0))

    # DOS PUNTITOS ROJOS AL FRENTE
    lienzo.set_at((x + 12, y - 9), (230, 40, 40))
    lienzo.set_at((x + 15, y - 9), (230, 40, 40))


def dibujar_ojitos(lienzo: pygame.Surface, tiempo: float) -> None:

    """OJITOS ROJOS QUE SE ABREN Y CIERRAN EN LO OSCURO DEL SALON."""

    for x, y, desfase in OJITOS:

        if (tiempo + desfase) % 5 < 2.2:
            pygame.draw.rect(lienzo, (200, 30, 36), (x, y, 2, 2))
            pygame.draw.rect(lienzo, (200, 30, 36), (x + 5, y, 2, 2))


def dibujar_nubes(lienzo: pygame.Surface, tiempo: float) -> None:

    """UNA NUBE PASA FRENTE A LA LUNA CADA 10 SEGUNDOS Y OSCURECE TODO UN POCO."""

    fase = tiempo % 10

    if fase > 3:
        return

    x = VENTANA.x - 20 + int(fase / 3 * (VENTANA.width + 40))

    nube = pygame.Surface(VENTANA.size, pygame.SRCALPHA)
    pygame.draw.ellipse(nube, (30, 36, 60, 230), (x - VENTANA.x - 16, 8, 34, 18))
    pygame.draw.ellipse(nube, (30, 36, 60, 230), (x - VENTANA.x - 4, 4, 30, 18))
    lienzo.blit(nube, VENTANA.topleft)

    if 0.8 < fase < 2.2:
        oscuro = pygame.Surface((ANCHO, ALTO), pygame.SRCALPHA)
        oscuro.fill((0, 0, 8, 50))
        lienzo.blit(oscuro, (0, 0))


def dibujar(ventana: pygame.Surface) -> None:

    """DIBUJA EL PASILLO COMPLETO EN LA VENTANA DEL JUEGO."""

    if "fijo" not in CAPAS:
        CAPAS["fijo"] = crear_fijo()

    tiempo = pygame.time.get_ticks() / 1000

    lienzo = CAPAS["fijo"].copy()

    dibujar_ojitos(lienzo, tiempo)
    dibujar_sombra(lienzo, tiempo)
    dibujar_nubes(lienzo, tiempo)

    mostrar(ventana, lienzo)
