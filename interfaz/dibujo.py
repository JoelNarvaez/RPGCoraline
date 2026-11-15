
"""FUNCIONES DE AYUDA PARA DIBUJAR."""

import os
import pygame
import config

# IMAGENES CARGADAS EN MEMORIA
imagenes_cargadas = {}

# ESPACIO ENTRE RENGLONES
ESPACIO_ENTRE_RENGLONES = 8


def dividir_en_lineas(
    texto: str,
    fuente: pygame.font.Font,
    ancho_maximo: int
) -> list:

    """DIVIDE EL TEXTO EN RENGLONES."""

    lineas = []

    for parrafo in texto.split("\n"):

        renglon = ""

        for palabra in parrafo.split(" "):

            if renglon == "":
                prueba = palabra
            else:
                prueba = renglon + " " + palabra

            if fuente.size(prueba)[0] <= ancho_maximo or renglon == "":
                renglon = prueba
            else:
                lineas.append(renglon)
                renglon = palabra

        lineas.append(renglon)

    return lineas


def contar_letras(lineas: list) -> int:

    """CUENTA LAS LETRAS DE LOS RENGLONES."""

    total = 0

    for linea in lineas:
        total = total + len(linea)

    return total


def recortar_lineas(lineas: list, letras: int) -> list:

    """MUESTRA SOLAMENTE LAS LETRAS INDICADAS."""

    visibles = []
    restantes = letras

    for linea in lineas:

        if restantes <= 0:
            break

        if restantes >= len(linea):
            visibles.append(linea)
            restantes = restantes - len(linea)

        else:
            visibles.append(linea[:restantes])
            restantes = 0

    return visibles


def dibujar_texto(
    ventana: pygame.Surface,
    texto: str,
    fuente: pygame.font.Font,
    color: tuple,
    x: int,
    y: int
) -> None:

    """DIBUJA UN RENGLON DE TEXTO."""

    superficie = fuente.render(
        texto,
        True,
        color
    )

    ventana.blit(
        superficie,
        (x, y)
    )


def dibujar_texto_centrado(
    ventana: pygame.Surface,
    texto: str,
    fuente: pygame.font.Font,
    color: tuple,
    centro_x: int,
    y: int
) -> None:

    """DIBUJA UN TEXTO CENTRADO."""

    superficie = fuente.render(
        texto,
        True,
        color
    )

    x = centro_x - superficie.get_width() // 2

    ventana.blit(
        superficie,
        (x, y)
    )


def dibujar_parrafo(
    ventana: pygame.Surface,
    lineas: list,
    fuente: pygame.font.Font,
    color: tuple,
    x: int,
    y: int,
    espaciado: int = ESPACIO_ENTRE_RENGLONES
) -> int:

    """DIBUJA VARIOS RENGLONES."""

    for linea in lineas:

        dibujar_texto(
            ventana,
            linea,
            fuente,
            color,
            x,
            y
        )

        y = y + fuente.get_height() + espaciado

    return y

def dibujar_boton(
    ventana: pygame.Surface,
    rectangulo: pygame.Rect,
    texto: str,
    fuente: pygame.font.Font,
    mouse_encima: bool,
    centrado: bool
) -> None:

    """DIBUJA UN BOTON."""

    if mouse_encima:
        color = config.COLOR_BOTON_SOBRE
    else:
        color = config.COLOR_BOTON

    pygame.draw.rect(
        ventana,
        color,
        rectangulo,
        border_radius=8
    )

    superficie = fuente.render(
        texto,
        True,
        config.COLOR_TEXTO
    )

    y = rectangulo.centery - superficie.get_height() // 2

    if centrado:
        x = rectangulo.centerx - superficie.get_width() // 2
    else:
        x = rectangulo.x + 20

    ventana.blit(
        superficie,
        (x, y)
    )


def dibujar_capa(
    ventana: pygame.Surface,
    color: tuple,
    transparencia: int
) -> None:

    """DIBUJA UNA CAPA TRANSPARENTE."""

    capa = pygame.Surface(
        (config.ANCHO, config.ALTO)
    )

    capa.fill(color)

    capa.set_alpha(transparencia)

    ventana.blit(
        capa,
        (0, 0)
    )


def cargar_imagen(nombre: str) -> pygame.Surface:

    """CARGA UNA IMAGEN Y LA GUARDA EN MEMORIA."""

    if nombre in imagenes_cargadas:
        return imagenes_cargadas[nombre]

    ruta = os.path.join(
        config.RUTA_IMAGENES,
        nombre
    )

    imagen = None

    if os.path.exists(ruta):

        imagen = pygame.image.load(ruta).convert()

        imagen = pygame.transform.smoothscale(
            imagen,
            (config.ANCHO, config.ALTO)
        )

    imagenes_cargadas[nombre] = imagen

    return imagen