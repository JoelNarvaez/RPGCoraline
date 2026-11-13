"""Menú principal: Nueva partida, Continuar y Salir.

"Continuar" regresa a la partida que está abierta; si no hay ninguna,
carga la que está guardada en el archivo.

Responsable: Persona B
"""

import math

import pygame

import config
from juego import motor
from juego import partida
from interfaz import dibujo
from interfaz import animaciones
from interfaz import pantalla_juego

OPCIONES_MENU: list = ["Nueva partida", "Continuar", "Salir"]
TECLAS_NUMERO: list = [pygame.K_1, pygame.K_2, pygame.K_3]

ANCHO_BOTON: int = 340
ALTO_BOTON: int = 56
SEPARACION: int = 16
Y_PRIMER_BOTON: int = 340


def rectangulos_menu() -> list:
    """Un pygame.Rect por opción del menú, centrados en la ventana."""
    rectangulos: list = []
    x: int = config.ANCHO // 2 - ANCHO_BOTON // 2
    y: int = Y_PRIMER_BOTON
    for i in range(len(OPCIONES_MENU)):
        rectangulos.append(pygame.Rect(x, y, ANCHO_BOTON, ALTO_BOTON))
        y = y + ALTO_BOTON + SEPARACION
    return rectangulos


def entrar_a_partida(contexto: dict) -> str:
    """Prepara el nodo actual y regresa a qué pantalla hay que ir."""
    pantalla_juego.preparar_nodo(contexto)
    nodo: dict = motor.nodo_actual(contexto["estado"], contexto["nodos"])
    if motor.es_final(nodo):
        return "final"
    return "juego"


def continuar(contexto: dict) -> str:
    # Si hay una partida abierta (se salió con Esc), se regresa a ella
    if contexto["estado"] is not None:
        return entrar_a_partida(contexto)

    estado: dict = partida.cargar_partida(config.RUTA_PARTIDA)
    if estado is None:
        animaciones.mostrar_mensaje(contexto, "No hay partida guardada")
        return ""
    # Si la historia cambió después de guardar, el nodo puede ya no existir
    if estado["nodo_actual"] not in contexto["nodos"]:
        animaciones.mostrar_mensaje(contexto, "La partida guardada ya no coincide con la historia")
        return ""
    contexto["estado"] = estado
    return entrar_a_partida(contexto)


def ejecutar(numero: int, contexto: dict) -> str:
    """Hace lo que dice la opción `numero` del menú (empieza en 0)."""
    if numero == 0:
        contexto["estado"] = partida.nuevo_estado()
        return entrar_a_partida(contexto)
    if numero == 1:
        return continuar(contexto)
    if numero == 2:
        return "salir"
    return ""


def manejar_evento(evento: pygame.event.Event, contexto: dict) -> str:
    """Regresa el nombre de la siguiente pantalla, o "" para quedarse aquí."""
    if evento.type == pygame.MOUSEBUTTONDOWN and evento.button == 1:
        rectangulos: list = rectangulos_menu()
        for i in range(len(rectangulos)):
            if rectangulos[i].collidepoint(evento.pos):
                return ejecutar(i, contexto)
    elif evento.type == pygame.KEYDOWN:
        if evento.key in TECLAS_NUMERO:
            return ejecutar(TECLAS_NUMERO.index(evento.key), contexto)
    return ""


def actualizar(contexto: dict, dt: float) -> None:
    contexto["tiempo_menu"] = contexto["tiempo_menu"] + dt


def dibujar(ventana: pygame.Surface, contexto: dict) -> None:
    fuentes: dict = contexto["fuentes"]
    centro: int = config.ANCHO // 2

    # Título que "respira": su brillo sube y baja con una onda seno
    brillo: float = (math.sin(contexto["tiempo_menu"] * 2) + 1) / 2   # entre 0 y 1
    color_titulo: tuple = (
        int(config.COLOR_TENUE[0] + (config.COLOR_ACENTO[0] - config.COLOR_TENUE[0]) * brillo),
        int(config.COLOR_TENUE[1] + (config.COLOR_ACENTO[1] - config.COLOR_TENUE[1]) * brillo),
        int(config.COLOR_TENUE[2] + (config.COLOR_ACENTO[2] - config.COLOR_TENUE[2]) * brillo),
    )
    dibujo.dibujar_texto_centrado(ventana, "C O R A L I N E", fuentes["titulo"], color_titulo, centro, 150)
    dibujo.dibujar_texto_centrado(ventana, "Un juego de decisiones basado en la novela de Neil Gaiman",
                                  fuentes["pequena"], config.COLOR_TENUE, centro, 235)

    rectangulos: list = rectangulos_menu()
    posicion_mouse: tuple = pygame.mouse.get_pos()
    for i in range(len(OPCIONES_MENU)):
        encima: bool = rectangulos[i].collidepoint(posicion_mouse)
        dibujo.dibujar_boton(ventana, rectangulos[i], OPCIONES_MENU[i], fuentes["opcion"], encima, True)

    dibujo.dibujar_texto_centrado(ventana, "Proyecto escolar sin fines de lucro. Coraline es obra de Neil Gaiman.",
                                  fuentes["pequena"], config.COLOR_TENUE, centro, config.ALTO - 40)
