"""Pantalla de final: muestra el texto del final y su tipo (canónico, bueno o malo).

Usa las mismas animaciones que la pantalla de juego: aparece desde negro y el
texto se escribe letra por letra.

Responsable: Persona B
"""

import pygame

import config
from juego import motor
from interfaz import dibujo
from interfaz import animaciones
from interfaz import pantalla_juego

MARGEN: int = 120
Y_TEXTO: int = 220

TITULOS: dict = {
    "canonico": "FINAL CANÓNICO",
    "bueno": "FINAL BUENO",
    "malo": "FINAL MALO",
}
COLORES: dict = {
    "canonico": config.COLOR_ACENTO,
    "bueno": config.COLOR_FINAL_BUENO,
    "malo": config.COLOR_FINAL_MALO,
}


def manejar_evento(evento: pygame.event.Event, contexto: dict) -> str:
    """Regresa "menu" cuando el jugador presiona Enter o da clic."""
    presiono: bool = False
    if evento.type == pygame.MOUSEBUTTONDOWN and evento.button == 1:
        presiono = True
    elif evento.type == pygame.KEYDOWN and evento.key in [pygame.K_RETURN, pygame.K_SPACE]:
        presiono = True

    if not presiono:
        return ""
    if not animaciones.texto_terminado(contexto, contexto["total_letras"]):
        animaciones.completar_texto(contexto, contexto["total_letras"])
        return ""
    # La partida terminó: "Continuar" en el menú ya no debe regresar aquí
    contexto["estado"] = None
    return "menu"


def actualizar(contexto: dict, dt: float) -> None:
    animaciones.avanzar_maquina_escribir(contexto, dt, contexto["total_letras"])
    animaciones.avanzar_desvanecer(contexto, dt)


def dibujar(ventana: pygame.Surface, contexto: dict) -> None:
    nodo: dict = motor.nodo_actual(contexto["estado"], contexto["nodos"])
    fuentes: dict = contexto["fuentes"]
    tipo: str = nodo["final"]
    centro: int = config.ANCHO // 2

    pantalla_juego.dibujar_fondo(ventana, nodo)
    dibujo.dibujar_texto_centrado(ventana, TITULOS.get(tipo, "FINAL"), fuentes["titulo"],
                                  COLORES.get(tipo, config.COLOR_TEXTO), centro, 100)

    visibles: list = dibujo.recortar_lineas(contexto["lineas"], int(contexto["letras_visibles"]))
    dibujo.dibujar_parrafo(ventana, visibles, fuentes["texto"], config.COLOR_TEXTO, MARGEN, Y_TEXTO)

    if animaciones.texto_terminado(contexto, contexto["total_letras"]):
        dibujo.dibujar_texto_centrado(ventana, "Presiona Enter para volver al menú", fuentes["pequena"],
                                      config.COLOR_TENUE, centro, config.ALTO - 60)

    animaciones.dibujar_desvanecer(ventana, contexto["transparencia"])
