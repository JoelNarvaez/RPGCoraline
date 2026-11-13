"""Minijuego de buscar con la piedra: la pantalla está a oscuras y el mouse es la
piedra con agujero. Solo a través de ella se ve cuál canica brilla.

Datos del JSON:
  "se_mueve": true si la canica la lleva una rata que corre
  "senuelos": cuántas canicas falsas hay
  "tiempo": segundos

Clic en la canica que brilla = éxito. Clic en una falsa = pierdes 3 segundos.

Responsable: Persona B
"""

import math
import random

import pygame

import config
from interfaz import figuras

RADIO_PIEDRA: int = 85
CASTIGO_SEGUNDOS: float = 3.0
VELOCIDAD_RATA: float = 230.0


def iniciar(datos: dict) -> dict:
    senuelos: list = []
    for i in range(datos.get("senuelos", 6)):
        senuelos.append((random.randint(80, config.ANCHO - 80), random.randint(140, config.ALTO - 80)))
    juego: dict = {
        "se_mueve": datos.get("se_mueve", False),
        "real_x": float(random.randint(150, config.ANCHO - 150)),
        "real_y": float(random.randint(180, config.ALTO - 120)),
        "velocidad_x": VELOCIDAD_RATA,
        "velocidad_y": VELOCIDAD_RATA * 0.6,
        "senuelos": senuelos,
        "tiempo_total": float(datos["tiempo"]),
        "tiempo_restante": float(datos["tiempo"]),
        "resultado": "",
    }
    return juego


def manejar_evento(evento: pygame.event.Event, juego: dict) -> None:
    if evento.type != pygame.MOUSEBUTTONDOWN or evento.button != 1:
        return
    if math.dist(evento.pos, (juego["real_x"], juego["real_y"])) < 32:
        juego["resultado"] = "exito"
        return
    for (x, y) in juego["senuelos"]:
        if math.dist(evento.pos, (x, y)) < 20:
            juego["tiempo_restante"] = juego["tiempo_restante"] - CASTIGO_SEGUNDOS


def actualizar(juego: dict, dt: float) -> None:
    if juego["se_mueve"]:
        juego["real_x"] = juego["real_x"] + juego["velocidad_x"] * dt
        juego["real_y"] = juego["real_y"] + juego["velocidad_y"] * dt
        # Rebota en las orillas
        if juego["real_x"] < 80 or juego["real_x"] > config.ANCHO - 80:
            juego["velocidad_x"] = -juego["velocidad_x"]
        if juego["real_y"] < 140 or juego["real_y"] > config.ALTO - 80:
            juego["velocidad_y"] = -juego["velocidad_y"]
    juego["tiempo_restante"] = juego["tiempo_restante"] - dt
    if juego["tiempo_restante"] <= 0:
        juego["resultado"] = "fallo"


def dibujar(ventana: pygame.Surface, juego: dict, fuentes: dict) -> None:
    for (x, y) in juego["senuelos"]:
        figuras.canica(ventana, x, y, False)
    x_real: int = int(juego["real_x"])
    y_real: int = int(juego["real_y"])
    if juego["se_mueve"]:
        figuras.rata(ventana, x_real - 10, y_real + 8, juego["velocidad_x"] > 0)
    figuras.canica(ventana, x_real, y_real, True)

    # Oscuridad con un agujero donde está el mouse (la piedra)
    oscuridad: pygame.Surface = pygame.Surface((config.ANCHO, config.ALTO), pygame.SRCALPHA)
    oscuridad.fill((5, 4, 10, 250))
    raton: tuple = pygame.mouse.get_pos()
    pygame.draw.circle(oscuridad, (0, 0, 0, 0), raton, RADIO_PIEDRA)
    ventana.blit(oscuridad, (0, 0))
    pygame.draw.circle(ventana, (120, 115, 125), raton, RADIO_PIEDRA + 10, 12)
