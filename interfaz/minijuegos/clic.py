"""Minijuego de explorar y hacer clic: encontrar todas las figuras antes de que se acabe el tiempo.

Datos del JSON:
  "figura": "puerta" u "hoja"
  "cantidad": cuántas hay que encontrar
  "tiempo": segundos

Responsable: Persona B
"""

import math
import random

import pygame

import config
from interfaz import figuras

DISTANCIA_MINIMA: int = 90    # para que las figuras no queden encimadas
RADIO_CLIC: int = 36


def posicion_libre(objetivos: list) -> tuple:
    """Busca un lugar al azar que no esté encima de otra figura."""
    for intento in range(200):
        x: int = random.randint(100, config.ANCHO - 100)
        y: int = random.randint(150, config.ALTO - 80)
        libre: bool = True
        for objetivo in objetivos:
            if math.dist((x, y), (objetivo["x"], objetivo["y"])) < DISTANCIA_MINIMA:
                libre = False
        if libre:
            return (x, y)
    return (x, y)


def iniciar(datos: dict) -> dict:
    objetivos: list = []
    for i in range(datos["cantidad"]):
        x, y = posicion_libre(objetivos)
        objetivos.append({"x": x, "y": y, "encontrado": False})
    juego: dict = {
        "figura": datos["figura"],
        "objetivos": objetivos,
        "encontrados": 0,
        "tiempo_total": float(datos["tiempo"]),
        "tiempo_restante": float(datos["tiempo"]),
        "resultado": "",
    }
    return juego


def manejar_evento(evento: pygame.event.Event, juego: dict) -> None:
    if evento.type != pygame.MOUSEBUTTONDOWN or evento.button != 1:
        return
    for objetivo in juego["objetivos"]:
        if not objetivo["encontrado"]:
            if math.dist(evento.pos, (objetivo["x"], objetivo["y"])) < RADIO_CLIC:
                objetivo["encontrado"] = True
                juego["encontrados"] = juego["encontrados"] + 1
                break
    if juego["encontrados"] == len(juego["objetivos"]):
        juego["resultado"] = "exito"


def actualizar(juego: dict, dt: float) -> None:
    juego["tiempo_restante"] = juego["tiempo_restante"] - dt
    if juego["tiempo_restante"] <= 0:
        juego["resultado"] = "fallo"


def dibujar(ventana: pygame.Surface, juego: dict, fuentes: dict) -> None:
    for objetivo in juego["objetivos"]:
        if juego["figura"] == "puerta":
            figuras.puerta(ventana, objetivo["x"], objetivo["y"], objetivo["encontrado"])
        else:
            figuras.hoja(ventana, objetivo["x"], objetivo["y"], objetivo["encontrado"])
    texto: str = "Encontradas: " + str(juego["encontrados"]) + " / " + str(len(juego["objetivos"]))
    superficie: pygame.Surface = fuentes["texto"].render(texto, True, config.COLOR_ACENTO)
    ventana.blit(superficie, (40, config.ALTO - 50))
