"""FONDO DIBUJADO CON CODIGO: EL TEATRO DE LAS VECINAS, ABANDONADO.

Es el teatro de teatro_vecinas.py (cap04, de Wendy), pero oscuro, frio y
lleno de telaranas. Una telarana enorme cruza el escenario y tiene pegada la
segunda canica. En el escenario se mueve algo enorme y palido, hecho de dos
cuerpos pegados (lo que queda de las otras Spink y Forcible). Los perros del
publico estan quietos y solo les brillan los ojos. Coraline mira desde el
pasillo. Se usa en cap08_n04 y en su rama cap08_r04.

huida_teatro.py (cap08_n05) usa este mismo teatro (crear_base,
dibujar_perros_quietos, criatura y las posiciones).

Lo que se mueve: la criatura que respira, un brillo que recorre la telarana,
la canica pegada que destella, los ojos de los perros y el polvo.
"""

import math

import pygame

from interfaz.fondos.pintura import ANCHO, ALTO
from interfaz.fondos.pintura import capa_vacia, pegar_con_contorno, COLOR_CONTORNO
from interfaz.fondos.pintura import brillo, orillas_oscuras, mostrar
from interfaz.fondos import personajes
from interfaz.fondos import teatro_vecinas

X_CORALINE = 405
Y_CORALINE = 355                                  # donde pisa, en el pasillo (igual que en el cap. 4)

TELARANA = (466, 140)                             # centro de la telarana grande
RADIO_TELARANA = 74
CANICA = (446, 124)                               # la segunda canica, pegada en la telarana
X_CRIATURA = 570
Y_ESCENARIO = 240

# LOS PERROS EN LAS MISMAS BUTACAS QUE EN EL CAP. 4: (x, y_piso)
PERROS = [(95, 300), (205, 300), (315, 300), (535, 300), (85, 350), (195, 350), (305, 350), (555, 350)]

COLOR_PALIDO = (206, 202, 196)
COLOR_PALIDO_SOMBRA = (150, 146, 146)
COLOR_TELARANA = (196, 200, 210)

CAPAS = {}


# --------------------------------------------------
# PARTE FIJA (TAMBIEN LA USA huida_teatro.py)
# --------------------------------------------------

def dibujar_telarana(lienzo: pygame.Surface, centro: tuple, radio: int, desde: float, hasta: float) -> None:

    """TELARANA: RAYOS QUE SALEN DEL CENTRO Y VUELTAS QUE LOS UNEN (ENTRE LOS ANGULOS desde Y hasta)."""

    capa = pygame.Surface((ANCHO, ALTO), pygame.SRCALPHA)
    color = (*COLOR_TELARANA, 110)
    rayos = 12
    angulos = []

    for i in range(rayos + 1):
        angulos.append(desde + (hasta - desde) * i / rayos)

    for angulo in angulos:
        punta = (centro[0] + int(math.cos(angulo) * radio), centro[1] + int(math.sin(angulo) * radio))
        pygame.draw.line(capa, color, centro, punta)

    for vuelta in range(1, 6):
        distancia = radio * vuelta / 6
        puntos = []
        for angulo in angulos:
            puntos.append((centro[0] + int(math.cos(angulo) * distancia), centro[1] + int(math.sin(angulo) * distancia)))
        pygame.draw.lines(capa, color, False, puntos)

    lienzo.blit(capa, (0, 0))


def crear_criatura() -> pygame.Surface:

    """LA COSA DEL ESCENARIO: DOS CUERPOS PALIDOS PEGADOS, CON DOS CABEZAS Y MUCHOS BRAZOS."""

    capa = capa_vacia()
    x, y = X_CRIATURA, Y_ESCENARIO

    # CUERPO GRANDE Y BLANDO, CON PATAS CORTAS
    for dx in [-24, -12, 6, 20]:
        pygame.draw.rect(capa, COLOR_PALIDO_SOMBRA, (x + dx, y - 12, 5, 12))
    pygame.draw.ellipse(capa, COLOR_PALIDO, (x - 34, y - 62, 68, 54))
    pygame.draw.ellipse(capa, COLOR_PALIDO_SOMBRA, (x - 2, y - 56, 32, 46))
    pygame.draw.line(capa, COLOR_PALIDO_SOMBRA, (x - 2, y - 58), (x - 6, y - 12))         # la costura

    # CUATRO BRAZOS FLACOS
    for inicio, codo, mano in [((x - 30, y - 46), (x - 46, y - 40), (x - 50, y - 22)),
                               ((x - 26, y - 34), (x - 40, y - 20), (x - 34, y - 6)),
                               ((x + 28, y - 48), (x + 44, y - 50), (x + 50, y - 32)),
                               ((x + 26, y - 30), (x + 42, y - 18), (x + 40, y - 4))]:
        pygame.draw.line(capa, COLOR_PALIDO, inicio, codo, 3)
        pygame.draw.line(capa, COLOR_PALIDO, codo, mano, 3)

    # DOS CABEZAS: UNA CON CHONGO (SPINK) Y OTRA CON RIZOS (FORCIBLE), SIN COLOR
    for cx, cy, chongo in [(x - 14, y - 70, True), (x + 14, y - 74, False)]:
        pygame.draw.circle(capa, COLOR_PALIDO, (cx, cy), 10)
        if chongo:
            pygame.draw.circle(capa, COLOR_PALIDO_SOMBRA, (cx, cy - 11), 5)
        else:
            for rx in [-8, -3, 3, 8]:
                pygame.draw.circle(capa, COLOR_PALIDO_SOMBRA, (cx + rx, cy - 8), 4)
        pygame.draw.rect(capa, (40, 36, 44), (cx - 5, cy - 1, 3, 3))                        # ojos hundidos
        pygame.draw.rect(capa, (40, 36, 44), (cx + 2, cy - 1, 3, 3))
        pygame.draw.line(capa, (90, 70, 74), (cx - 3, cy + 5), (cx + 3, cy + 5))

    criatura = capa_vacia()
    pegar_con_contorno(criatura, capa)

    return criatura


def dibujar_perros_quietos(lienzo: pygame.Surface) -> None:

    """LOS PERROS DEL PUBLICO, SIN SALTAR NI MOVER LA COLA."""

    for x, y in PERROS:
        personajes.dibujar_perro(lienzo, x, y, 0, 0)


def crear_base() -> pygame.Surface:

    """EL TEATRO DE WENDY, OSCURO Y FRIO, CON TELARANAS (SIN PERSONAJES)."""

    lienzo = pygame.Surface((ANCHO, ALTO))

    teatro_vecinas.dibujar_pared(lienzo)
    teatro_vecinas.dibujar_arco(lienzo)
    teatro_vecinas.dibujar_escenario(lienzo)
    teatro_vecinas.dibujar_cortinas(lienzo)
    teatro_vecinas.dibujar_tarima(lienzo)

    # FOCOS DEL ARCO APAGADOS
    for i in range(12):
        pygame.draw.circle(lienzo, (45, 26, 37), (250 + i * 31, 49), 5)
        pygame.draw.circle(lienzo, (70, 56, 60), (250 + i * 31, 49), 3)

    dibujar_telarana(lienzo, TELARANA, RADIO_TELARANA, 0, math.pi * 2)
    dibujar_telarana(lienzo, (226, 22), 60, 0, math.pi / 2)                      # esquinas del arco
    dibujar_telarana(lienzo, (624, 22), 60, math.pi / 2, math.pi)

    teatro_vecinas.dibujar_butacas(lienzo)
    dibujar_telarana(lienzo, (130, 268), 30, math.pi, math.pi * 2)               # entre las butacas
    dibujar_telarana(lienzo, (470, 268), 26, math.pi, math.pi * 2)

    # TODO SE ENFRIA Y SE OSCURECE
    tinte = pygame.Surface((ANCHO, ALTO))
    tinte.fill((104, 104, 128))
    lienzo.blit(tinte, (0, 0), special_flags=pygame.BLEND_MULT)

    return lienzo


def crear_fijo() -> pygame.Surface:

    lienzo = crear_base()

    dibujar_perros_quietos(lienzo)
    personajes.dibujar_coraline_chica(lienzo, X_CORALINE, Y_CORALINE, True)

    brillo(lienzo, (X_CRIATURA, 180), 90, (190, 196, 220), 30)
    orillas_oscuras(lienzo)

    return lienzo


# --------------------------------------------------
# LO QUE SE MUEVE (TAMBIEN LO USA huida_teatro.py)
# --------------------------------------------------

def dibujar_criatura(lienzo: pygame.Surface, tiempo: float, avance: int) -> None:

    """LA CRIATURA RESPIRA (SUBE Y BAJA UN PIXEL). avance LA MUEVE HACIA LA IZQUIERDA."""

    if "criatura" not in CAPAS:
        CAPAS["criatura"] = crear_criatura()

    respira = 1 if math.sin(tiempo * 1.7) > 0 else 0
    lienzo.blit(CAPAS["criatura"], (-avance, -respira))


def dibujar_ojos_perros(lienzo: pygame.Surface, tiempo: float, color: tuple) -> None:

    """LOS OJOS DE LOS PERROS BRILLAN Y CADA UNO PARPADEA A SU TIEMPO."""

    for i in range(len(PERROS)):
        x, y = PERROS[i]
        if (tiempo * 0.4 + i * 0.29) % 1 < 0.05:
            continue
        pygame.draw.rect(lienzo, color, (x - 36, y - 21, 3, 2))


def dibujar_brillo_telarana(lienzo: pygame.Surface, tiempo: float) -> None:

    """UN PUNTITO DE LUZ RECORRE UNO DE LOS RAYOS DE LA TELARANA, DEL CENTRO HACIA AFUERA."""

    rayo = int(tiempo / 2) % 12
    angulo = rayo / 12 * math.pi * 2
    distancia = (tiempo % 2) / 2 * RADIO_TELARANA

    x = TELARANA[0] + int(math.cos(angulo) * distancia)
    y = TELARANA[1] + int(math.sin(angulo) * distancia)

    lienzo.set_at((x, y), (240, 244, 255))
    lienzo.set_at((x + 1, y), (200, 206, 220))


def dibujar_canica_pegada(lienzo: pygame.Surface, tiempo: float) -> None:

    """LA SEGUNDA CANICA, ENVUELTA EN HILOS, CON UN DESTELLO DE VEZ EN CUANDO."""

    x, y = CANICA
    pygame.draw.circle(lienzo, COLOR_CONTORNO, (x, y), 4)
    pygame.draw.circle(lienzo, (190, 200, 220), (x, y), 3)
    pygame.draw.line(lienzo, (230, 150, 200), (x - 2, y + 1), (x + 2, y - 1))
    pygame.draw.line(lienzo, COLOR_TELARANA, (x - 5, y - 2), (x + 5, y + 3))

    if tiempo % 2.5 < 0.3:
        for dx, dy in [(-1, 0), (1, 0), (0, -1), (0, 1)]:
            pygame.draw.line(lienzo, (255, 255, 240), (x + dx * 5, y + dy * 5), (x + dx * 8, y + dy * 8))


def dibujar_polvo(lienzo: pygame.Surface, tiempo: float) -> None:

    """POLVO QUE CAE DESPACIO FRENTE AL ESCENARIO."""

    for i in range(16):
        x = 240 + (i * 37) % 380 + int(math.sin(tiempo + i) * 3)
        y = int((tiempo * 6 + i * 23) % 230) + 20
        lienzo.set_at((x, y), (170, 170, 190))


def dibujar(ventana: pygame.Surface) -> None:

    """DIBUJA LA ESCENA COMPLETA EN LA VENTANA DEL JUEGO."""

    if "fijo" not in CAPAS:
        CAPAS["fijo"] = crear_fijo()

    tiempo = pygame.time.get_ticks() / 1000

    lienzo = CAPAS["fijo"].copy()

    dibujar_brillo_telarana(lienzo, tiempo)
    dibujar_canica_pegada(lienzo, tiempo)
    dibujar_criatura(lienzo, tiempo, 0)
    dibujar_ojos_perros(lienzo, tiempo, (220, 220, 160))
    dibujar_polvo(lienzo, tiempo)

    mostrar(ventana, lienzo)
