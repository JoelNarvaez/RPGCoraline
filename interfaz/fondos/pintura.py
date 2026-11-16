"""HERRAMIENTAS DE PINTURA COMPARTIDAS POR LOS FONDOS DIBUJADOS.

Todos los fondos se dibujan en un lienzo de ANCHO x ALTO que luego se agranda
2 veces para llenar la ventana.

Archivo compartido: si se cambia algo aqui, avisar al otro.
"""

import math

import pygame

import config

ANCHO = 640
ALTO = 360


def mezclar(color: tuple, otro: tuple, cuanto: float) -> tuple:

    """COLOR INTERMEDIO ENTRE DOS COLORES."""

    return (
        int(color[0] + (otro[0] - color[0]) * cuanto),
        int(color[1] + (otro[1] - color[1]) * cuanto),
        int(color[2] + (otro[2] - color[2]) * cuanto)
    )


def degradado(
    lienzo: pygame.Surface,
    rect: pygame.Rect,
    arriba: tuple,
    abajo: tuple,
    bandas: int
) -> None:

    """DEGRADADO EN FRANJAS CON PIXELES INTERCALADOS ENTRE ELLAS (TRAMADO)."""

    alto_banda = rect.height / bandas

    for i in range(bandas):

        color = mezclar(arriba, abajo, i / max(bandas - 1, 1))

        y = rect.y + int(i * alto_banda)

        pygame.draw.rect(
            lienzo,
            color,
            (rect.x, y, rect.width, int(alto_banda) + 1)
        )

        # TRAMADO: UNA FILA DE PIXELES SUELTOS CON EL COLOR DE LA BANDA ANTERIOR
        if i > 0:

            anterior = mezclar(arriba, abajo, (i - 1) / max(bandas - 1, 1))

            for x in range(rect.x, rect.right, 2):
                lienzo.set_at((x, y), anterior)

            for x in range(rect.x + 1, rect.right, 4):
                lienzo.set_at((x, y + 1), anterior)


def brillo(
    lienzo: pygame.Surface,
    centro: tuple,
    radio: int,
    color: tuple,
    fuerza: int
) -> None:

    """LUZ REDONDA QUE SE DESVANECE POCO A POCO HACIA LA ORILLA."""

    capa = pygame.Surface((radio * 2, radio * 2), pygame.SRCALPHA)

    for y in range(radio * 2):

        for x in range(radio * 2):

            distancia = math.dist((x, y), (radio, radio)) / radio

            if distancia < 1:

                alfa = int(fuerza * (1 - distancia) ** 2)

                capa.set_at((x, y), (color[0], color[1], color[2], alfa))

    lienzo.blit(capa, (centro[0] - radio, centro[1] - radio))


def orillas_oscuras(lienzo: pygame.Surface) -> None:

    """OSCURECE LAS ORILLAS DE LA ESCENA (SE CALCULA CHICO Y SE AGRANDA)."""

    chica = pygame.Surface((160, 90), pygame.SRCALPHA)

    for y in range(90):

        for x in range(160):

            dx = abs(x - 80) / 80
            dy = abs(y - 45) / 45

            distancia = math.sqrt(dx * dx * 0.7 + dy * dy * 0.5)

            alfa = int(max(0.0, distancia - 0.45) * 220)

            chica.set_at((x, y), (6, 8, 16, min(alfa, 150)))

    lienzo.blit(pygame.transform.smoothscale(chica, (ANCHO, ALTO)), (0, 0))


def armar_sprite(filas: list, colores: dict) -> pygame.Surface:

    """CONVIERTE FILAS DE LETRAS EN UNA IMAGEN. CADA LETRA ES UN COLOR; "." ES TRANSPARENTE."""

    ancho = 0

    for fila in filas:
        ancho = max(ancho, len(fila))

    sprite = pygame.Surface((ancho, len(filas)), pygame.SRCALPHA)

    for y in range(len(filas)):

        for x in range(len(filas[y])):

            letra = filas[y][x]

            if letra in colores:
                sprite.set_at((x, y), colores[letra])

    return sprite


def mostrar(ventana: pygame.Surface, lienzo: pygame.Surface) -> None:

    """AGRANDA EL LIENZO AL TAMANO DE LA VENTANA Y LO DIBUJA."""

    ventana.blit(
        pygame.transform.scale(lienzo, (config.ANCHO, config.ALTO)),
        (0, 0)
    )


# --------------------------------------------------
# PARA QUE SE VEA COMO RPG: CONTORNOS Y TEXTURAS
# --------------------------------------------------

COLOR_CONTORNO = (16, 12, 22)


def capa_vacia() -> pygame.Surface:

    """UNA CAPA TRANSPARENTE DEL TAMANO DEL LIENZO, PARA DIBUJAR ALGO Y LUEGO CONTORNEARLO."""

    return pygame.Surface((ANCHO, ALTO), pygame.SRCALPHA)


def pegar_con_contorno(lienzo: pygame.Surface, capa: pygame.Surface) -> None:

    """PEGA LA CAPA EN EL LIENZO CON UNA ORILLA OSCURA DE 1 PIXEL ALREDEDOR.

    La orilla sale de la silueta de lo que se dibujo en la capa (las sombras
    medio transparentes no cuentan). Asi los personajes y muebles se ven como
    sprites de RPG, igual que Coraline.
    """

    silueta = pygame.mask.from_surface(capa, 127).to_surface(
        setcolor=COLOR_CONTORNO,
        unsetcolor=(0, 0, 0, 0)
    )

    for dx, dy in [(-1, 0), (1, 0), (0, -1), (0, 1)]:
        lienzo.blit(silueta, (dx, dy))

    lienzo.blit(capa, (0, 0))


def tablas_de_madera(lienzo: pygame.Surface, rect: pygame.Rect, color: tuple, alto_tabla: int) -> None:

    """TABLAS HORIZONTALES CON VETAS, UNIONES CHUECAS Y ALGUN NUDO.

    Se ve igual cada vez porque las vetas salen de cuentas fijas, no al azar.
    """

    oscuro = mezclar(color, (0, 0, 0), 0.3)
    claro = mezclar(color, (255, 255, 255), 0.12)

    pygame.draw.rect(lienzo, color, rect)

    fila = 0

    for y in range(rect.y, rect.bottom, alto_tabla):

        # LINEA ENTRE TABLAS Y UN BRILLITO ARRIBA DE CADA UNA
        pygame.draw.line(lienzo, oscuro, (rect.x, y), (rect.right - 1, y))
        pygame.draw.line(lienzo, claro, (rect.x, y + 1), (rect.right - 1, y + 1))

        # UNIONES: CADA FILA EMPIEZA EN OTRO LADO
        for x in range(rect.x + (fila * 37) % 70, rect.right, 70):
            pygame.draw.line(lienzo, oscuro, (x, y), (x, min(y + alto_tabla, rect.bottom) - 1))

        # VETAS CORTAS
        for i in range(rect.width // 9):
            x = rect.x + (i * 29 + fila * 13) % rect.width
            yy = y + 2 + (i * 7 + fila) % max(alto_tabla - 3, 1)
            if yy < rect.bottom:
                pygame.draw.line(lienzo, mezclar(color, (0, 0, 0), 0.15), (x, yy), (min(x + 6, rect.right - 1), yy))

        # UN NUDO DE VEZ EN CUANDO
        if fila % 3 == 1:
            x = rect.x + (fila * 53) % max(rect.width - 6, 1) + 3
            pygame.draw.ellipse(lienzo, oscuro, (x, y + alto_tabla // 2 - 1, 4, 3))

        fila = fila + 1
