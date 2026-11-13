"""Minijuego de esquivar: Coraline sigue al mouse y tiene que aguantar sin que la
toquen hasta que se acabe el tiempo. Tiene 3 vidas.

Datos del JSON:
  "enemigo": "sombra", "mano" o "otro_padre"
  "cantidad": cuántos enemigos
  "persiguen": true si los enemigos van hacia Coraline
  "tiempo": segundos que hay que aguantar

Responsable: Persona B
"""

import math
import random

import pygame

import config
from interfaz import figuras

VELOCIDAD_CORALINE: float = 380.0
VIDAS: int = 3
SEGUNDOS_INVENCIBLE: float = 1.0
RADIOS: dict = {"sombra": 26, "mano": 18, "otro_padre": 48}
VELOCIDADES: dict = {"sombra": 170.0, "mano": 260.0, "otro_padre": 110.0}


def iniciar(datos: dict) -> dict:
    tipo: str = datos["enemigo"]
    enemigos: list = []
    for i in range(datos["cantidad"]):
        angulo: float = random.uniform(0, 2 * math.pi)
        enemigos.append({
            # Aparecen en la parte derecha para no caer encima de Coraline
            "x": float(random.randint(config.ANCHO // 2, config.ANCHO - 60)),
            "y": float(random.randint(120, config.ALTO - 60)),
            "vx": math.cos(angulo) * VELOCIDADES[tipo],
            "vy": math.sin(angulo) * VELOCIDADES[tipo],
        })
    juego: dict = {
        "enemigo": tipo,
        "persiguen": datos.get("persiguen", False),
        "enemigos": enemigos,
        "x": 160.0,
        "y": float(config.ALTO // 2),
        "vidas": VIDAS,
        "invencible": 0.0,
        "tiempo_total": float(datos["tiempo"]),
        "tiempo_restante": float(datos["tiempo"]),
        "resultado": "",
    }
    return juego


def manejar_evento(evento: pygame.event.Event, juego: dict) -> None:
    pass   # Coraline sigue al mouse; no hace falta revisar eventos


def mover_coraline(juego: dict, dt: float) -> None:
    """Coraline camina hacia el mouse sin pasar de su velocidad máxima."""
    raton: tuple = pygame.mouse.get_pos()
    dx: float = raton[0] - juego["x"]
    dy: float = raton[1] - juego["y"]
    distancia: float = math.hypot(dx, dy)
    paso: float = VELOCIDAD_CORALINE * dt
    if distancia <= paso:
        juego["x"] = float(raton[0])
        juego["y"] = float(raton[1])
    else:
        juego["x"] = juego["x"] + dx / distancia * paso
        juego["y"] = juego["y"] + dy / distancia * paso


def mover_enemigo(enemigo: dict, juego: dict, dt: float) -> None:
    if juego["persiguen"]:
        dx: float = juego["x"] - enemigo["x"]
        dy: float = juego["y"] - enemigo["y"]
        distancia: float = math.hypot(dx, dy)
        if distancia > 0:
            velocidad: float = VELOCIDADES[juego["enemigo"]]
            enemigo["vx"] = dx / distancia * velocidad
            enemigo["vy"] = dy / distancia * velocidad
    enemigo["x"] = enemigo["x"] + enemigo["vx"] * dt
    enemigo["y"] = enemigo["y"] + enemigo["vy"] * dt
    # Rebotan en las orillas
    if enemigo["x"] < 30 or enemigo["x"] > config.ANCHO - 30:
        enemigo["vx"] = -enemigo["vx"]
    if enemigo["y"] < 100 or enemigo["y"] > config.ALTO - 30:
        enemigo["vy"] = -enemigo["vy"]


def actualizar(juego: dict, dt: float) -> None:
    mover_coraline(juego, dt)
    if juego["invencible"] > 0:
        juego["invencible"] = juego["invencible"] - dt

    radio: int = RADIOS[juego["enemigo"]]
    for enemigo in juego["enemigos"]:
        mover_enemigo(enemigo, juego, dt)
        tocada: bool = math.dist((juego["x"], juego["y"]), (enemigo["x"], enemigo["y"])) < radio + 14
        if tocada and juego["invencible"] <= 0:
            juego["vidas"] = juego["vidas"] - 1
            juego["invencible"] = SEGUNDOS_INVENCIBLE

    juego["tiempo_restante"] = juego["tiempo_restante"] - dt
    if juego["vidas"] <= 0:
        juego["resultado"] = "fallo"
    elif juego["tiempo_restante"] <= 0:
        juego["resultado"] = "exito"


def dibujar(ventana: pygame.Surface, juego: dict, fuentes: dict) -> None:
    for enemigo in juego["enemigos"]:
        x: int = int(enemigo["x"])
        y: int = int(enemigo["y"])
        if juego["enemigo"] == "mano":
            figuras.mano(ventana, x, y, RADIOS["mano"])
        elif juego["enemigo"] == "otro_padre":
            pygame.draw.circle(ventana, (220, 215, 205), (x, y), RADIOS["otro_padre"])
            figuras.boton_ojo(ventana, x - 16, y - 10, 9)
        else:
            figuras.sombra(ventana, x, y, RADIOS["sombra"])
    figuras.coraline(ventana, int(juego["x"]), int(juego["y"]), juego["invencible"] > 0)

    texto: str = "Vidas: " + str(juego["vidas"])
    superficie: pygame.Surface = fuentes["texto"].render(texto, True, config.COLOR_FINAL_MALO)
    ventana.blit(superficie, (40, config.ALTO - 50))
