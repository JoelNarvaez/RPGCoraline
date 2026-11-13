"""Panel de inventario y estadísticas. Se dibuja encima de la pantalla de juego.

Se abre y se cierra con la tecla I (Esc también lo cierra).

Responsable: Persona B
"""

import pygame

import config
from juego import inventario
from juego import estadisticas
from interfaz import dibujo

ANCHO_PANEL: int = 760
ALTO_PANEL: int = 460
ANCHO_BARRA: int = 260
ALTO_BARRA: int = 16


def manejar_evento(evento: pygame.event.Event, contexto: dict) -> str:
    """Regresa "juego" para cerrar el panel, o "" para quedarse aquí."""
    if evento.type == pygame.KEYDOWN:
        if evento.key == pygame.K_i or evento.key == pygame.K_ESCAPE:
            return "juego"
    return ""


def actualizar(contexto: dict, dt: float) -> None:
    pass


def dibujar_barra(ventana: pygame.Surface, x: int, y: int, valor: int) -> None:
    """Barra de estadística: el fondo es el máximo y lo dorado es el valor actual."""
    fondo: pygame.Rect = pygame.Rect(x, y, ANCHO_BARRA, ALTO_BARRA)
    pygame.draw.rect(ventana, config.COLOR_BOTON, fondo, border_radius=6)
    ancho_valor: int = ANCHO_BARRA * valor // estadisticas.VALOR_MAXIMO
    if ancho_valor > 0:
        lleno: pygame.Rect = pygame.Rect(x, y, ancho_valor, ALTO_BARRA)
        pygame.draw.rect(ventana, config.COLOR_ACENTO, lleno, border_radius=6)


def dibujar(ventana: pygame.Surface, contexto: dict) -> None:
    estado: dict = contexto["estado"]
    fuentes: dict = contexto["fuentes"]

    dibujo.dibujar_capa(ventana, (0, 0, 0), 170)
    panel: pygame.Rect = pygame.Rect(0, 0, ANCHO_PANEL, ALTO_PANEL)
    panel.center = (config.ANCHO // 2, config.ALTO // 2)
    pygame.draw.rect(ventana, config.COLOR_PANEL, panel, border_radius=14)

    # Columna izquierda: objetos
    x: int = panel.x + 40
    y: int = panel.y + 36
    dibujo.dibujar_texto(ventana, "Objetos", fuentes["texto"], config.COLOR_ACENTO, x, y)
    y = y + 50
    if len(estado["inventario"]) == 0:
        dibujo.dibujar_texto(ventana, "(vacío)", fuentes["opcion"], config.COLOR_TENUE, x, y)
    for objeto in estado["inventario"]:
        nombre: str = "• " + inventario.nombre_para_mostrar(objeto)
        dibujo.dibujar_texto(ventana, nombre, fuentes["opcion"], config.COLOR_TEXTO, x, y)
        y = y + 34

    # Columna derecha: estadísticas
    x = panel.x + 400
    y = panel.y + 36
    dibujo.dibujar_texto(ventana, "Estadísticas", fuentes["texto"], config.COLOR_ACENTO, x, y)
    y = y + 50
    for nombre_estadistica in estado["estadisticas"]:
        valor: int = estado["estadisticas"][nombre_estadistica]
        etiqueta: str = inventario.nombre_para_mostrar(nombre_estadistica) + ": " + str(valor)
        dibujo.dibujar_texto(ventana, etiqueta, fuentes["opcion"], config.COLOR_TEXTO, x, y)
        dibujar_barra(ventana, x, y + 30, valor)
        y = y + 70

    dibujo.dibujar_texto_centrado(ventana, "I o Esc para cerrar", fuentes["pequena"],
                                  config.COLOR_TENUE, panel.centerx, panel.bottom - 40)
