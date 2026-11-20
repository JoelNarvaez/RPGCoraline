"""LA PIEDRA CON AGUJERO DE CORALINE (LA QUE LE REGALA LA SENORITA SPINK).

Segun la imagen de referencia de Joel: un triangulo de esquinas muy
redondeadas, verde azulado con vetas oscuras que dan vuelta alrededor del
agujero (como malaquita), brillante como si estuviera pulida, con un agujero
redondo en medio y un cordon negro que pasa por el agujero.

No es un fondo: la usan piedra_spink (cap. 2), beso_fantasma (cap. 7),
caja_juguetes y vista_piedra (cap. 8) y el minijuego canicas_piedra, cada
uno de su tamano.
El agujero queda transparente, asi que por ahi se ve lo que haya detras.
"""

import math

import pygame

from interfaz.fondos.pintura import mezclar
from interfaz.fondos import personajes

# TONOS DE LAS VETAS, DEL MAS OSCURO AL MAS CLARO
VETAS = [(8, 58, 52), (16, 98, 86), (30, 140, 122), (64, 186, 160), (120, 222, 196)]
COLOR_CORDON = (20, 18, 22)

# HACIA DONDE APUNTAN LAS TRES ESQUINAS (EN GRADOS): ARRIBA A LA IZQUIERDA,
# A LA DERECHA Y ABAJO, COMO EN LA FOTO
ESQUINAS = [-150, -20, 100]

SPRITES = {}


def distancia_a_linea(punto: tuple, a: tuple, b: tuple) -> float:

    """QUE TAN LEJOS ESTA UN PUNTO DEL SEGMENTO QUE VA DE a A b."""

    ax = b[0] - a[0]
    ay = b[1] - a[1]
    avance = ((punto[0] - a[0]) * ax + (punto[1] - a[1]) * ay) / (ax * ax + ay * ay)
    avance = max(0.0, min(1.0, avance))

    return math.dist(punto, (a[0] + ax * avance, a[1] + ay * avance))


def forma(tamano: int, radio_agujero: int, borde: int) -> pygame.Surface:

    """LA SILUETA DEL TRIANGULO REDONDEADO, EN BLANCO SOBRE TRANSPARENTE. EL CENTRO ES EL DEL AGUJERO.

    Es un triangulo mas chico "inflado" parejo hacia afuera: un pixel es de la
    piedra si esta dentro de ese triangulo o a menos de "redondeo" de sus lados.
    """

    silueta = pygame.Surface((tamano, tamano), pygame.SRCALPHA)
    centro = tamano // 2

    radio_interno = radio_agujero + borde                   # del centro a la orilla de cada lado
    redondeo = max(2, int(radio_interno * 0.45))
    lejos = (radio_interno - redondeo) * 2                  # del centro a cada esquina del triangulo de adentro

    puntas = []
    for grados in ESQUINAS:
        angulo = math.radians(grados)
        puntas.append((centro + math.cos(angulo) * lejos, centro + math.sin(angulo) * lejos))

    # EL TRIANGULO DE ADENTRO SE PINTA DIRECTO; LO DE ALREDEDOR, PIXEL POR PIXEL
    pygame.draw.polygon(silueta, (255, 255, 255, 255), puntas)

    for y in range(tamano):
        for x in range(tamano):
            for i in range(3):
                if distancia_a_linea((x, y), puntas[i], puntas[(i + 1) % 3]) <= redondeo:
                    silueta.set_at((x, y), (255, 255, 255, 255))
                    break

    return silueta


def sprite_piedra(radio_agujero: int, borde: int) -> pygame.Surface:

    """ARMA (UNA VEZ POR TAMANO) LA PIEDRA CON SUS VETAS, SU BRILLO, EL AGUJERO Y EL CONTORNO.

    radio_agujero: el tamano del agujero. borde: cuanta piedra hay entre el
    agujero y la orilla de cada lado. El sprite queda centrado en el agujero.
    """

    clave = (radio_agujero, borde)

    if clave in SPRITES:
        return SPRITES[clave]

    radio_interno = radio_agujero + borde
    tamano = radio_interno * 4 + 4                       # las esquinas quedan a menos de 2 radios del centro
    centro = tamano // 2

    silueta = forma(tamano, radio_agujero, borde)
    sprite = pygame.Surface((tamano, tamano), pygame.SRCALPHA)

    # VETAS: FRANJAS QUE DAN VUELTA ALREDEDOR DEL AGUJERO, ONDULADAS
    ancho_veta = max(1.5, radio_interno * 0.2)

    for y in range(tamano):
        for x in range(tamano):

            if silueta.get_at((x, y))[3] == 0:
                continue

            dx = x - centro
            dy = y - centro
            distancia = math.sqrt(dx * dx + dy * dy)

            if distancia < radio_agujero:
                continue

            angulo = math.atan2(dy, dx)
            onda = math.sin(distancia / ancho_veta * 2.2 + math.sin(angulo * 2 + 1) * 1.4)
            tono = int((onda + 1) / 2 * (len(VETAS) - 1) + 0.5)

            # MAS OSCURO PEGADO AL AGUJERO (SE VE LA PROFUNDIDAD)
            if distancia < radio_agujero + 1.5:
                tono = 0

            color = VETAS[tono]

            # BRILLO DE PIEDRA PULIDA ARRIBA A LA IZQUIERDA
            if dx < 0 and dy < 0 and radio_agujero + borde * 0.3 < distancia < radio_agujero + borde * 0.8:
                if -2.6 < angulo < -1.8:
                    color = mezclar(color, (255, 255, 255), 0.6)

            sprite.set_at((x, y), color)

    # PUNTITOS DE LUZ (REFLEJOS)
    for grados, que_tan_lejos in [(-70, 0.55), (10, 0.7)]:
        angulo = math.radians(grados)
        distancia = radio_agujero + borde * que_tan_lejos
        punto = (int(centro + math.cos(angulo) * distancia), int(centro + math.sin(angulo) * distancia))
        if silueta.get_at(punto)[3] > 0:
            sprite.set_at(punto, (230, 255, 246))

    sprite = personajes.con_contorno(sprite)
    SPRITES[clave] = sprite

    return sprite


def dibujar_cordon(lienzo: pygame.Surface, x: int, y: int, radio_agujero: int, largo: int) -> None:

    """EL CORDON NEGRO: ENTRA POR EL AGUJERO Y SUBE EN DOS HILOS. (x, y) ES EL CENTRO DEL AGUJERO."""

    grueso = max(1, radio_agujero // 10)
    arriba = y - radio_agujero

    for lado in [-1, 1]:
        inicio = (x + lado * max(1, radio_agujero // 3), arriba)
        fin = (x + lado * max(1, radio_agujero // 6), arriba - largo)
        pygame.draw.line(lienzo, COLOR_CORDON, inicio, fin, grueso)


def dibujar_piedra(lienzo: pygame.Surface, x: int, y: int, radio_agujero: int, borde: int, cordon: int) -> None:

    """PEGA LA PIEDRA CON EL AGUJERO EN (x, y). cordon ES EL LARGO DEL CORDON (0 = SIN CORDON)."""

    sprite = sprite_piedra(radio_agujero, borde)
    lienzo.blit(sprite, (x - sprite.get_width() // 2, y - sprite.get_height() // 2))

    if cordon > 0:
        dibujar_cordon(lienzo, x, y, radio_agujero, cordon)
