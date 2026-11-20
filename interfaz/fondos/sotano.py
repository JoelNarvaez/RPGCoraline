"""FONDO DIBUJADO CON CODIGO: EL SOTANO Y LO QUE QUEDA DEL OTRO PADRE.

Un sotano bajito de piedra humeda, con vigas, un estante de botellas rotas
(huele a vino agrio), un pan con moho y un foco que cuelga de su cable. La
escalera baja desde la puerta, arriba a la derecha. En medio hay un monton de
cortinas viejas y debajo asoma un pie palido. Coraline acaba de bajar y lo
mira desde el ultimo escalon. Se usa en cap09_n03 y en su rama cap09_r03.

Tambien son las partes de padre_derretido.py (cap09_n04), sotano_cazando.py
(cap09_m01) y del minijuego escalera_sotano: el cuarto (dibujar_sotano), la
escalera (punto_escalera) y la criatura (dibujar_padre_derretido), que es
el otro padre convertido en una masa blanca y blanda con dos botones.

Lo que se mueve: el foco que se mece y mueve la luz, el monton de cortinas
que respira, el pie que tiembla, las moscas del pan y una gota que cae.
"""

import math

import pygame

from interfaz.fondos.pintura import ANCHO, ALTO
from interfaz.fondos.pintura import capa_vacia, pegar_con_contorno
from interfaz.fondos.pintura import mezclar, degradado, brillo, orillas_oscuras, mostrar
from interfaz.fondos import personajes

Y_PISO = 300

ESCALERA_ABAJO = (540, Y_PISO)          # donde termina la escalera (en el piso)
ESCALERA_ARRIBA = (622, 124)            # el escalon de hasta arriba, junto a la puerta
ESCALONES = 9
PUERTA = pygame.Rect(606, 66, 30, 58)

FOCO = (486, 40)                        # de donde cuelga el cable del foco
LARGO_CABLE = 46
X_CORTINAS = 456
GOTA = (430, 74)

COLOR_PIEDRA = (52, 46, 44)
COLOR_MADERA = (70, 50, 40)
COLOR_MASA = (226, 222, 214)
COLOR_MASA_SOMBRA = (176, 172, 168)

X_CORALINE = 548

CAPAS = {}


# --------------------------------------------------
# PARTES (TAMBIEN LAS USAN LAS DEMAS ESCENAS DEL SOTANO Y EL MINIJUEGO)
# --------------------------------------------------

def punto_escalera(avance: float) -> tuple:

    """DONDE PISA ALGUIEN QUE VA EN avance DE LA ESCALERA (0 = ABAJO, 1 = ARRIBA), SOBRE UN ESCALON."""

    escalon = min(ESCALONES, int(avance * ESCALONES + 0.5))
    x = ESCALERA_ABAJO[0] + (ESCALERA_ARRIBA[0] - ESCALERA_ABAJO[0]) * avance
    y = ESCALERA_ABAJO[1] + (ESCALERA_ARRIBA[1] - ESCALERA_ABAJO[1]) * escalon / ESCALONES

    return (int(x), int(y))


def dibujar_sotano(lienzo: pygame.Surface) -> None:

    """PAREDES DE PIEDRA CON HUMEDAD, VIGAS, ESTANTE DE BOTELLAS, PAN CON MOHO, ESCALERA Y PUERTA."""

    degradado(lienzo, pygame.Rect(0, 0, ANCHO, Y_PISO), (24, 22, 24), COLOR_PIEDRA, 10)

    # PIEDRAS DE LA PARED, CADA FILA CORRIDA
    for fila, y in enumerate(range(30, Y_PISO, 18)):
        pygame.draw.line(lienzo, (34, 30, 30), (0, y), (ANCHO, y))
        for x in range((fila % 2) * 16, ANCHO, 32):
            pygame.draw.line(lienzo, (34, 30, 30), (x, y), (x, y + 18))
            pygame.draw.line(lienzo, (66, 60, 56), (x + 2, y + 2), (x + 10, y + 2))

    # MANCHAS DE HUMEDAD VERDOSAS QUE ESCURREN
    for x, largo in [(412, 120), (446, 60), (598, 150), (520, 80)]:
        for i in range(3):
            pygame.draw.line(lienzo, (46, 62, 48), (x + i * 3, 30), (x + i * 4, 30 + largo - i * 20), 2)

    # VIGAS DEL TECHO
    pygame.draw.rect(lienzo, (30, 22, 20), (0, 0, ANCHO, 30))
    for x in range(380, ANCHO, 70):
        pygame.draw.rect(lienzo, COLOR_MADERA, (x, 22, 16, 12))

    # ESTANTE CON BOTELLAS (ALGUNAS ROTAS) Y EL PAN CON MOHO
    pygame.draw.rect(lienzo, COLOR_MADERA, (404, 150, 70, 4))
    pygame.draw.rect(lienzo, COLOR_MADERA, (404, 196, 70, 4))
    for i, rota in enumerate([False, True, False, False, True]):
        x = 410 + i * 13
        alto = 10 if rota else 22
        pygame.draw.rect(lienzo, (40, 70, 50), (x, 150 - alto, 7, alto))
        if rota:
            pygame.draw.polygon(lienzo, (60, 90, 70), [(x, 140), (x + 3, 136), (x + 7, 140)])     # pico roto
        else:
            pygame.draw.rect(lienzo, (40, 70, 50), (x + 2, 150 - alto - 5, 3, 5))                 # cuello
        lienzo.set_at((x + 1, 150 - alto + 2), (120, 160, 130))
    pygame.draw.ellipse(lienzo, (150, 110, 70), (426, 184, 30, 13))
    for x, y in [(432, 188), (440, 186), (448, 190), (436, 192)]:
        pygame.draw.circle(lienzo, (90, 130, 80), (x, y), 2)
    pygame.draw.ellipse(lienzo, (90, 30, 50), (406, 196, 24, 5))                     # vino derramado

    # PISO DE TIERRA APISONADA
    degradado(lienzo, pygame.Rect(0, Y_PISO, ANCHO, ALTO - Y_PISO), (44, 36, 32), (24, 20, 20), 4)
    pygame.draw.ellipse(lienzo, (30, 34, 40), (GOTA[0] - 14, Y_PISO + 4, 28, 6))     # charco

    # LA PUERTA DE ARRIBA (POR LA RENDIJA ENTRA LUZ) Y LA ESCALERA
    pygame.draw.rect(lienzo, COLOR_MADERA, PUERTA.inflate(6, 4))
    pygame.draw.rect(lienzo, (96, 70, 54), PUERTA)
    pygame.draw.line(lienzo, (230, 210, 170), (PUERTA.x, PUERTA.bottom), (PUERTA.right, PUERTA.bottom))

    capa = capa_vacia()
    for i in range(ESCALONES + 1):
        x, y = punto_escalera(i / ESCALONES)
        pygame.draw.rect(capa, (96, 68, 52), (x - 16, y, 32, 4))
        pygame.draw.rect(capa, (66, 46, 36), (x - 16, y + 4, 32, 2))
    pygame.draw.line(capa, COLOR_MADERA, (ESCALERA_ABAJO[0] - 18, Y_PISO), (ESCALERA_ARRIBA[0] - 18, ESCALERA_ARRIBA[1]), 3)
    pygame.draw.line(capa, COLOR_MADERA, (ESCALERA_ABAJO[0] + 18, Y_PISO), (ESCALERA_ARRIBA[0] + 18, ESCALERA_ARRIBA[1]), 3)
    pegar_con_contorno(lienzo, capa)


def posicion_foco(tiempo: float) -> tuple:

    """EL FOCO SE MECE COLGADO DE SU CABLE."""

    angulo = math.sin(tiempo * 1.1) * 0.35

    return (FOCO[0] + int(math.sin(angulo) * LARGO_CABLE), FOCO[1] + int(math.cos(angulo) * LARGO_CABLE))


def dibujar_foco(lienzo: pygame.Surface, tiempo: float) -> None:

    """EL FOCO, SU CABLE Y LA LUZ AMARILLENTA QUE SE MUEVE CON EL (LA LUZ SE CALCULA UNA VEZ)."""

    if "luz" not in CAPAS:
        luz = pygame.Surface((300, 300), pygame.SRCALPHA)
        brillo(luz, (150, 150), 150, (255, 210, 140), 70)
        CAPAS["luz"] = luz

    x, y = posicion_foco(tiempo)
    lienzo.blit(CAPAS["luz"], (x - 150, y - 130))

    pygame.draw.line(lienzo, (20, 18, 20), FOCO, (x, y - 4))
    pygame.draw.rect(lienzo, (60, 60, 60), (x - 2, y - 5, 5, 4))
    pygame.draw.circle(lienzo, (255, 236, 180), (x, y + 1), 4)


def dibujar_padre_derretido(lienzo: pygame.Surface, x: int, y_piso: int, tiempo: float,
                             alto: int, brazos: bool, botones: int) -> None:

    """LO QUE QUEDA DEL OTRO PADRE: UNA MASA BLANCA Y BLANDA QUE TIEMBLA, CON BOTONES POR OJOS.

    alto: que tan levantado esta (20 = echado, 90 = de pie). brazos: si estira dos
    brazos blandos tanteando. botones: cuantos botones le quedan (2 o 1).
    """

    capa = capa_vacia()
    tiembla = math.sin(tiempo * 7) * 1.5

    # LA MASA: VARIOS BULTOS ENCIMADOS QUE SE ESTIRAN SEGUN EL ALTO
    ancho = 54 - alto // 5
    pygame.draw.ellipse(capa, COLOR_MASA_SOMBRA, (x - ancho // 2 - 6, y_piso - 18, ancho + 12, 20))
    pygame.draw.ellipse(capa, COLOR_MASA, (x - ancho // 2 + tiembla, y_piso - alto - 10, ancho, alto + 18))
    pygame.draw.ellipse(capa, COLOR_MASA, (x - 14 - tiembla, y_piso - alto - 22, 28, 30))           # la "cabeza"
    pygame.draw.ellipse(capa, COLOR_MASA_SOMBRA, (x + 2, y_piso - alto + 6, ancho // 2 - 2, alto - 4))

    # GOTERONES QUE ESCURREN
    for dx in [-ancho // 3, ancho // 4]:
        largo = 6 + int((math.sin(tiempo * 2 + dx) + 1) * 3)
        pygame.draw.line(capa, COLOR_MASA, (x + dx, y_piso - 14), (x + dx, y_piso - 14 + largo), 3)

    # RESTOS DE LA BATA NARANJA PEGADOS
    pygame.draw.polygon(capa, mezclar(personajes.PADRE_BATA, COLOR_MASA, 0.4),
                        [(x - 10, y_piso - alto + 14), (x + 6, y_piso - alto + 18), (x + 2, y_piso - alto + 30)])

    if brazos:
        for lado in [-1, 1]:
            mano = (x + lado * (34 + int(math.sin(tiempo * 3 + lado) * 6)), y_piso - alto + 8 + int(math.cos(tiempo * 2.4 + lado) * 6))
            pygame.draw.line(capa, COLOR_MASA, (x + lado * 10, y_piso - alto + 16), mano, 6)
            for i in range(3):
                pygame.draw.line(capa, COLOR_MASA, mano, (mano[0] + lado * 6, mano[1] - 4 + i * 4), 2)

    pegar_con_contorno(lienzo, capa)

    # LOS BOTONES (UNO SE PUEDE HABER CAIDO)
    ojos = [(x - 6 - int(tiembla), y_piso - alto - 8), (x + 6 - int(tiembla), y_piso - alto - 8)]
    personajes.dibujar_botones(lienzo, ojos[:botones], tiempo, True)


# --------------------------------------------------
# ESTA ESCENA (cap09_n03)
# --------------------------------------------------

def dibujar_cortinas(capa: pygame.Surface, respira: int) -> None:

    """EL MONTON DE CORTINAS VIEJAS (VERDE Y VINO) CON EL PIE PALIDO ASOMANDO."""

    x, y = X_CORTINAS, Y_PISO
    pygame.draw.polygon(capa, (70, 90, 70), [(x - 46, y), (x - 34, y - 26 - respira), (x - 6, y - 36 - respira), (x + 20, y - 24), (x + 44, y)])
    pygame.draw.polygon(capa, (100, 40, 50), [(x - 30, y), (x - 10, y - 22 - respira), (x + 16, y - 16), (x + 30, y)])
    for dx in [-24, -4, 14]:
        pygame.draw.line(capa, (50, 64, 50), (x + dx, y - 4), (x + dx + 6, y - 22 - respira))


def crear_fijo() -> pygame.Surface:

    lienzo = pygame.Surface((ANCHO, ALTO))
    dibujar_sotano(lienzo)

    pie = punto_escalera(0)
    personajes.dibujar_coraline_chica(lienzo, X_CORALINE, pie[1], False)

    orillas_oscuras(lienzo)

    return lienzo


def dibujar_monton(lienzo: pygame.Surface, tiempo: float) -> None:

    """EL MONTON DE CORTINAS SUBE Y BAJA (ALGO RESPIRA DEBAJO) Y EL PIE TIEMBLA DE VEZ EN CUANDO."""

    respira = 1 if math.sin(tiempo * 1.3) > 0 else 0
    capa = capa_vacia()
    dibujar_cortinas(capa, respira)

    # EL PIE: BLANCO, BLANDO, CON DEDOS COMO MASA
    tiembla = 1 if tiempo % 4 < 0.3 and int(tiempo * 20) % 2 == 0 else 0
    pie = (X_CORTINAS + 40 + tiembla, Y_PISO - 6)
    pygame.draw.ellipse(capa, COLOR_MASA, (pie[0] - 6, pie[1] - 4, 20, 10))
    for i in range(4):
        pygame.draw.circle(capa, COLOR_MASA, (pie[0] + 14, pie[1] - 3 + i * 2), 2)

    pegar_con_contorno(lienzo, capa)


def dibujar_moscas(lienzo: pygame.Surface, tiempo: float) -> None:

    """TRES MOSCAS DANDO VUELTAS SOBRE EL PAN CON MOHO."""

    for i in range(3):
        angulo = tiempo * (4 + i) + i * 2
        x = 441 + int(math.cos(angulo) * (8 + i * 3))
        y = 178 + int(math.sin(angulo * 1.3) * 5)
        lienzo.set_at((x, y), (10, 10, 10))
        lienzo.set_at((x + 1, y), (10, 10, 10))


def dibujar_gota(lienzo: pygame.Surface, tiempo: float) -> None:

    """UNA GOTA QUE CAE DEL TECHO AL CHARCO CADA 2 SEGUNDOS."""

    fase = tiempo % 2
    y = GOTA[1] + int(fase * fase * 120)

    if y < Y_PISO + 6:
        pygame.draw.rect(lienzo, (150, 170, 190), (GOTA[0], y, 1, 3))
    else:
        pygame.draw.ellipse(lienzo, (110, 130, 150), (GOTA[0] - 5, Y_PISO + 5, 10, 3), 1)


def dibujar(ventana: pygame.Surface) -> None:

    """DIBUJA LA ESCENA COMPLETA EN LA VENTANA DEL JUEGO."""

    if "fijo" not in CAPAS:
        CAPAS["fijo"] = crear_fijo()

    tiempo = pygame.time.get_ticks() / 1000

    lienzo = CAPAS["fijo"].copy()

    dibujar_foco(lienzo, tiempo)
    dibujar_monton(lienzo, tiempo)
    dibujar_moscas(lienzo, tiempo)
    dibujar_gota(lienzo, tiempo)

    mostrar(ventana, lienzo)
