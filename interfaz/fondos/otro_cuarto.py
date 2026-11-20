"""FONDO DIBUJADO CON CODIGO: EL OTRO CUARTO DE CORALINE.

Un cuarto mucho mas divertido que el suyo: papel tapiz con estrellas, repisas
con juguetes y un baul. Un dinosaurio de cuerda vuela por el cuarto y un
robotito camina solo. El otro padre sonrie desde la puerta y, en los
rincones, unas ratas negras de ojos rojos la vigilan. Se usa en cap03_n05.

Lo que se mueve: el dinosaurio volando, el robot caminando, las ratas que se
asoman y el brillo de los botones del otro padre.
"""

import math

import pygame

from interfaz.fondos.pintura import ANCHO, ALTO
from interfaz.fondos.pintura import capa_vacia, pegar_con_contorno
from interfaz.fondos.pintura import mezclar, degradado, brillo, orillas_oscuras, mostrar
from interfaz.fondos import personajes
from interfaz.fondos import sala_actrices

Y_PISO = 300

X_CORALINE = 440
X_PADRE = 600
PUERTA = pygame.Rect(572, 96, 58, Y_PISO - 96)
BAUL = pygame.Rect(480, 270, 44, 30)

COLOR_PARED = (70, 96, 160)

# RINCONES DONDE SE ASOMAN LAS RATAS: (x, y, mira a la derecha)
RATAS = [(412, Y_PISO - 2, True), (548, 150, False), (530, Y_PISO - 2, False)]

CAPAS = {}


def dibujar_cuarto(lienzo: pygame.Surface, con_baul: bool = True) -> None:

    """PARED AZUL CON ESTRELLAS, REPISAS CON JUGUETES, BAUL, PUERTA Y TAPETE.

    con_baul en False deja el cuarto sin el baul parado (en el cap. 8 esta volteado).
    """

    degradado(lienzo, pygame.Rect(0, 0, ANCHO, Y_PISO), (40, 52, 110), COLOR_PARED, 14)

    # ESTRELLITAS DEL PAPEL TAPIZ
    for y in range(16, 260, 26):
        for x in range(6 + (y // 26 % 2) * 13, ANCHO, 26):
            pygame.draw.line(lienzo, (240, 210, 110), (x - 2, y), (x + 2, y))
            pygame.draw.line(lienzo, (240, 210, 110), (x, y - 2), (x, y + 2))

    # PUERTA ABIERTA CON LUZ DEL PASILLO (ALLI ESTA EL OTRO PADRE)
    pygame.draw.rect(lienzo, (90, 60, 50), PUERTA.inflate(8, 4).move(0, -2))
    degradado(lienzo, PUERTA, (240, 210, 160), (200, 160, 120), 6)

    # REPISAS CON JUGUETES
    for y in [120, 168]:
        pygame.draw.rect(lienzo, (160, 110, 70), (410, y, 150, 5))

    # OSITO, PELOTA, CUBOS, SOLDADITOS, BARCO
    pygame.draw.circle(lienzo, (170, 120, 70), (424, 108), 8)
    pygame.draw.circle(lienzo, (170, 120, 70), (424, 98), 6)
    pygame.draw.circle(lienzo, (170, 120, 70), (419, 93), 2)
    pygame.draw.circle(lienzo, (170, 120, 70), (429, 93), 2)
    pygame.draw.circle(lienzo, (220, 60, 60), (450, 112), 8)
    pygame.draw.line(lienzo, (250, 250, 250), (443, 112), (457, 112), 2)

    for i, color in enumerate([(240, 200, 60), (80, 170, 90), (220, 90, 140)]):
        pygame.draw.rect(lienzo, color, (472 + i * 11, 110, 10, 10))

    for i in range(4):
        pygame.draw.rect(lienzo, (200, 40, 40), (414 + i * 10, 152, 5, 10))
        pygame.draw.rect(lienzo, (30, 30, 50), (414 + i * 10, 148, 5, 4))

    pygame.draw.polygon(lienzo, (230, 230, 220), [(470, 164), (500, 164), (494, 168), (474, 168)])
    pygame.draw.polygon(lienzo, (240, 240, 250), [(484, 140), (484, 162), (498, 160)])
    pygame.draw.line(lienzo, (120, 90, 60), (484, 140), (484, 164))

    # PISO Y TAPETE REDONDO DE COLORES
    pygame.draw.rect(lienzo, (120, 82, 60), (0, Y_PISO, ANCHO, ALTO - Y_PISO))

    for i, color in enumerate([(220, 90, 90), (240, 200, 90), (90, 170, 120), (90, 130, 210)]):
        pygame.draw.ellipse(lienzo, color, (400 + i * 12, 296 + i * 4, 200 - i * 24, 46 - i * 8))

    if not con_baul:
        return

    # BAUL DE JUGUETES ABIERTO
    pygame.draw.rect(lienzo, (150, 70, 50), BAUL)
    pygame.draw.rect(lienzo, (100, 46, 34), BAUL, 1)
    pygame.draw.polygon(lienzo, (170, 84, 60), [(BAUL.x, BAUL.y), (BAUL.right, BAUL.y), (BAUL.right - 4, BAUL.y - 16), (BAUL.x + 4, BAUL.y - 16)])
    pygame.draw.rect(lienzo, (230, 190, 70), (BAUL.centerx - 3, BAUL.y + 6, 6, 6))
    pygame.draw.circle(lienzo, (100, 180, 230), (BAUL.x + 12, BAUL.y - 2), 5)     # cosas asomandose
    pygame.draw.rect(lienzo, (240, 200, 60), (BAUL.x + 24, BAUL.y - 6, 8, 8))


def crear_fijo() -> pygame.Surface:

    lienzo = pygame.Surface((ANCHO, ALTO))

    dibujar_cuarto(lienzo)
    capa = capa_vacia()
    personajes.dibujar_otro_padre(capa, X_PADRE, "normal")
    pegar_con_contorno(lienzo, capa)
    sala_actrices.dibujar_coraline(lienzo, X_CORALINE)

    brillo(lienzo, PUERTA.center, 110, (255, 210, 150), 50)
    orillas_oscuras(lienzo)

    return lienzo


# --------------------------------------------------
# LO QUE SE MUEVE
# --------------------------------------------------

def dibujar_dinosaurio(lienzo: pygame.Surface, tiempo: float) -> None:

    """DINOSAURIO DE CUERDA VERDE CON ALAS, VOLANDO EN OCHOS POR EL CUARTO."""

    x = 500 + int(math.sin(tiempo * 0.8) * 70)
    y = 70 + int(math.sin(tiempo * 1.6) * 20)
    mira_derecha = math.cos(tiempo * 0.8) > 0
    direccion = 1 if mira_derecha else -1

    verde = (90, 180, 90)

    pygame.draw.ellipse(lienzo, verde, (x - 10, y - 5, 20, 10))                           # cuerpo
    pygame.draw.circle(lienzo, verde, (x + direccion * 11, y - 6), 5)                     # cabeza
    lienzo.set_at((x + direccion * 13, y - 7), (20, 20, 20))                              # ojo
    pygame.draw.line(lienzo, verde, (x - direccion * 9, y), (x - direccion * 17, y + 4), 3)   # cola

    for i in range(3):
        pygame.draw.polygon(lienzo, (60, 140, 60), [(x - 6 + i * 5, y - 4), (x - 4 + i * 5, y - 8), (x - 2 + i * 5, y - 4)])

    # ALAS QUE ALETEAN Y LLAVE DE CUERDA QUE GIRA
    aleteo = int(math.sin(tiempo * 16) * 7)
    pygame.draw.polygon(lienzo, (150, 220, 150), [(x - 4, y - 2), (x + 4, y - 2), (x, y - 10 - aleteo)])
    giro = int(math.sin(tiempo * 10) * 3)
    pygame.draw.line(lienzo, (210, 180, 90), (x, y + 4), (x, y + 8))
    pygame.draw.line(lienzo, (210, 180, 90), (x - 3 + giro, y + 8), (x + 3 - giro, y + 8), 2)


def dibujar_robot(lienzo: pygame.Surface, tiempo: float) -> None:

    """ROBOTITO DE LATA QUE CAMINA SOLO DE UN LADO A OTRO EN EL TAPETE."""

    x = 520 + int(math.sin(tiempo * 0.9) * 26)
    y = 318
    paso = int(tiempo * 6) % 2

    pygame.draw.rect(lienzo, (180, 186, 196), (x - 5, y - 16, 10, 10))
    pygame.draw.rect(lienzo, (160, 166, 176), (x - 4, y - 24, 8, 7))
    pygame.draw.rect(lienzo, (230, 60, 60), (x - 2, y - 22, 1, 2))
    pygame.draw.rect(lienzo, (230, 60, 60), (x + 1, y - 22, 1, 2))
    pygame.draw.line(lienzo, (120, 126, 136), (x, y - 24), (x, y - 28))
    pygame.draw.circle(lienzo, (240, 200, 60), (x, y - 29), 1)
    pygame.draw.rect(lienzo, (120, 126, 136), (x - 4, y - 6 - paso, 3, 6))
    pygame.draw.rect(lienzo, (120, 126, 136), (x + 1, y - 6 - (1 - paso), 3, 6))


def dibujar_ratas(lienzo: pygame.Surface, tiempo: float) -> None:

    """RATAS NEGRAS QUE SE ASOMAN UN RATO DESDE LOS RINCONES, CON OJOS ROJOS."""

    for i in range(len(RATAS)):

        x, y, mira_derecha = RATAS[i]
        fase = (tiempo + i * 1.7) % 5

        if fase > 2.5:
            continue

        asomada = min(fase, 2.5 - fase, 0.4) / 0.4
        direccion = 1 if mira_derecha else -1
        x = x + int(direccion * asomada * 6)

        pygame.draw.ellipse(lienzo, (14, 12, 16), (x - 8, y - 7, 14, 7))
        pygame.draw.circle(lienzo, (14, 12, 16), (x + direccion * 7, y - 5), 3)
        pygame.draw.circle(lienzo, (14, 12, 16), (x + direccion * 5, y - 8), 2)                 # oreja
        lienzo.set_at((x + direccion * 8, y - 6), (240, 40, 40))                              # ojo rojo
        pygame.draw.line(lienzo, (40, 30, 34), (x - direccion * 8, y - 2), (x - direccion * 16, y - 1))


def dibujar(ventana: pygame.Surface) -> None:

    """DIBUJA LA ESCENA COMPLETA EN LA VENTANA DEL JUEGO."""

    if "fijo" not in CAPAS:
        CAPAS["fijo"] = crear_fijo()

    tiempo = pygame.time.get_ticks() / 1000

    lienzo = CAPAS["fijo"].copy()

    dibujar_ratas(lienzo, tiempo)
    dibujar_robot(lienzo, tiempo)
    dibujar_dinosaurio(lienzo, tiempo)
    personajes.dibujar_botones(lienzo, personajes.ojos_otro_padre(X_PADRE), tiempo, True)

    mostrar(ventana, lienzo)
