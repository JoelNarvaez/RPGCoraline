"""Funciones de ayuda para dibujar. Las usan todas las pantallas.

pygame no hace saltos de línea solo, así que aquí se parte el texto en
renglones que quepan en el ancho indicado.

Responsable: Persona B
"""

import os

import pygame

import config

# Imágenes que ya se cargaron, para no leerlas del disco 60 veces por segundo.
# Llave: nombre del archivo. Valor: la imagen (o None si no existe).
imagenes_cargadas: dict = {}

# Píxeles extra entre renglones para que el texto respire
ESPACIO_ENTRE_RENGLONES: int = 8


def dividir_en_lineas(texto: str, fuente: pygame.font.Font, ancho_maximo: int) -> list:
    """Parte el texto en renglones que no pasen de `ancho_maximo` píxeles.

    Respeta los "\\n" que tenga el texto. Regresa una lista de strings.
    """
    lineas: list = []
    for parrafo in texto.split("\n"):
        renglon: str = ""
        for palabra in parrafo.split(" "):
            if renglon == "":
                prueba: str = palabra
            else:
                prueba = renglon + " " + palabra
            # fuente.size(...) regresa (ancho, alto) en píxeles
            if fuente.size(prueba)[0] <= ancho_maximo or renglon == "":
                renglon = prueba
            else:
                lineas.append(renglon)
                renglon = palabra
        lineas.append(renglon)
    return lineas


def contar_letras(lineas: list) -> int:
    """Cuántas letras hay en total en los renglones."""
    total: int = 0
    for linea in lineas:
        total = total + len(linea)
    return total


def recortar_lineas(lineas: list, letras: int) -> list:
    """Regresa los renglones mostrando solo las primeras `letras` letras.

    Sirve para la máquina de escribir: el texto ya está partido en renglones,
    así las palabras no brincan de renglón mientras se escriben.
    """
    visibles: list = []
    restantes: int = letras
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


def dibujar_texto(ventana: pygame.Surface, texto: str, fuente: pygame.font.Font,
                  color: tuple, x: int, y: int) -> None:
    """Dibuja un solo renglón de texto con su esquina superior izquierda en (x, y)."""
    superficie: pygame.Surface = fuente.render(texto, True, color)
    ventana.blit(superficie, (x, y))


def dibujar_texto_centrado(ventana: pygame.Surface, texto: str, fuente: pygame.font.Font,
                           color: tuple, centro_x: int, y: int) -> None:
    """Dibuja un renglón centrado horizontalmente en `centro_x`."""
    superficie: pygame.Surface = fuente.render(texto, True, color)
    x: int = centro_x - superficie.get_width() // 2
    ventana.blit(superficie, (x, y))


def dibujar_parrafo(ventana: pygame.Surface, lineas: list, fuente: pygame.font.Font,
                    color: tuple, x: int, y: int) -> int:
    """Dibuja varios renglones uno debajo del otro.

    Regresa la `y` donde terminó, para saber dónde dibujar lo siguiente.
    """
    for linea in lineas:
        dibujar_texto(ventana, linea, fuente, color, x, y)
        y = y + fuente.get_linesize() + ESPACIO_ENTRE_RENGLONES
    return y


def dibujar_boton(ventana: pygame.Surface, rectangulo: pygame.Rect, texto: str,
                  fuente: pygame.font.Font, mouse_encima: bool, centrado: bool) -> None:
    """Dibuja un botón. Cambia de color cuando el mouse está encima.

    Si `centrado` es False, el texto va pegado a la izquierda (para opciones largas).
    """
    if mouse_encima:
        color: tuple = config.COLOR_BOTON_SOBRE
    else:
        color = config.COLOR_BOTON
    pygame.draw.rect(ventana, color, rectangulo, border_radius=8)

    superficie: pygame.Surface = fuente.render(texto, True, config.COLOR_TEXTO)
    y: int = rectangulo.centery - superficie.get_height() // 2
    if centrado:
        x: int = rectangulo.centerx - superficie.get_width() // 2
    else:
        x = rectangulo.x + 20
    ventana.blit(superficie, (x, y))


def dibujar_capa(ventana: pygame.Surface, color: tuple, transparencia: int) -> None:
    """Pinta toda la ventana de un color semitransparente (0 = invisible, 255 = sólido)."""
    capa: pygame.Surface = pygame.Surface((config.ANCHO, config.ALTO))
    capa.fill(color)
    capa.set_alpha(transparencia)
    ventana.blit(capa, (0, 0))


def cargar_imagen(nombre: str) -> pygame.Surface:
    """Carga una imagen de recursos/imagenes/ ajustada al tamaño de la ventana.

    Regresa None si no existe, para que el juego siga aunque falte una imagen.
    """
    if nombre in imagenes_cargadas:
        return imagenes_cargadas[nombre]

    ruta: str = os.path.join(config.RUTA_IMAGENES, nombre)
    imagen: pygame.Surface = None
    if os.path.exists(ruta):
        imagen = pygame.image.load(ruta).convert()
        imagen = pygame.transform.smoothscale(imagen, (config.ANCHO, config.ALTO))

    imagenes_cargadas[nombre] = imagen
    return imagen
