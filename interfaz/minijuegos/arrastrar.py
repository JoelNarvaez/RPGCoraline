"""Minijuego de arrastrar: llevar un objeto con el mouse hasta su lugar.

Datos del JSON:
  "objeto": "llave", "mantel" o "gato"
  "zona": "cerradura", "pozo" u "otra_madre"
  "zona_se_mueve": true si el destino se mueve (más difícil)
  "tiempo": segundos

Responsable: Persona B
"""

import math

import pygame

import config
from interfaz import figuras

INICIO: tuple = (260, 480)
DISTANCIA_PARA_AGARRAR: int = 60
DISTANCIA_PARA_SOLTAR: int = 70


def iniciar(datos: dict) -> dict:
    juego: dict = {
        "objeto": datos["objeto"],
        "zona": datos["zona"],
        "zona_se_mueve": datos.get("zona_se_mueve", False),
        "objeto_x": float(INICIO[0]),
        "objeto_y": float(INICIO[1]),
        "zona_x": float(config.ANCHO - 300),
        "zona_y": float(config.ALTO // 2),
        "arrastrando": False,
        "reloj": 0.0,
        "tiempo_total": float(datos["tiempo"]),
        "tiempo_restante": float(datos["tiempo"]),
        "resultado": "",
    }
    return juego


def manejar_evento(evento: pygame.event.Event, juego: dict) -> None:
    if evento.type == pygame.MOUSEBUTTONDOWN and evento.button == 1:
        if math.dist(evento.pos, (juego["objeto_x"], juego["objeto_y"])) < DISTANCIA_PARA_AGARRAR:
            juego["arrastrando"] = True

    elif evento.type == pygame.MOUSEMOTION and juego["arrastrando"]:
        juego["objeto_x"] = float(evento.pos[0])
        juego["objeto_y"] = float(evento.pos[1])

    elif evento.type == pygame.MOUSEBUTTONUP and evento.button == 1 and juego["arrastrando"]:
        juego["arrastrando"] = False
        distancia: float = math.dist((juego["objeto_x"], juego["objeto_y"]), (juego["zona_x"], juego["zona_y"]))
        if distancia < DISTANCIA_PARA_SOLTAR:
            juego["resultado"] = "exito"
        else:
            # Si no lo soltó en el lugar correcto, el objeto regresa al inicio
            juego["objeto_x"] = float(INICIO[0])
            juego["objeto_y"] = float(INICIO[1])


def actualizar(juego: dict, dt: float) -> None:
    juego["reloj"] = juego["reloj"] + dt
    if juego["zona_se_mueve"]:
        # Se mueve de arriba a abajo y de lado a lado, como un 8
        juego["zona_x"] = config.ANCHO - 330 + math.sin(juego["reloj"] * 1.3) * 160
        juego["zona_y"] = config.ALTO // 2 + math.sin(juego["reloj"] * 2.1) * 150
    juego["tiempo_restante"] = juego["tiempo_restante"] - dt
    if juego["tiempo_restante"] <= 0:
        juego["resultado"] = "fallo"


def dibujar_figura(ventana: pygame.Surface, nombre: str, x: int, y: int) -> None:
    if nombre == "cerradura":
        figuras.cerradura(ventana, x, y)
    elif nombre == "pozo":
        figuras.pozo(ventana, x, y)
    elif nombre == "otra_madre":
        figuras.otra_madre(ventana, x, y)
    elif nombre == "llave":
        figuras.llave(ventana, x, y)
    elif nombre == "mantel":
        figuras.mantel(ventana, x, y)
    elif nombre == "gato":
        figuras.gato(ventana, x, y)


def dibujar(ventana: pygame.Surface, juego: dict, fuentes: dict) -> None:
    dibujar_figura(ventana, juego["zona"], int(juego["zona_x"]), int(juego["zona_y"]))
    dibujar_figura(ventana, juego["objeto"], int(juego["objeto_x"]), int(juego["objeto_y"]))
    if not juego["arrastrando"]:
        # Aro que late alrededor del objeto para indicar que se puede agarrar
        radio: int = 50 + int(math.sin(juego["reloj"] * 6) * 6)
        pygame.draw.circle(ventana, config.COLOR_ACENTO, (int(juego["objeto_x"]), int(juego["objeto_y"])), radio, 2)
