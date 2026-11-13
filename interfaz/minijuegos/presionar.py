"""Minijuego de presionar rápido: cerrar la puerta mientras alguien empuja del otro lado.

Cada vez que el jugador presiona Espacio (o da clic), la puerta se cierra un poco.
Mientras tanto, la otra madre empuja cada vez más fuerte.

Datos del JSON:
  "empuje": qué tan fuerte empuja al inicio (puntos por segundo)
  "tiempo": segundos

Responsable: Persona B
"""

import pygame

import config
from interfaz import figuras

FUERZA_POR_GOLPE: float = 5.0
AUMENTO_DE_EMPUJE: float = 2.5   # el empuje crece esta cantidad cada segundo


def iniciar(datos: dict) -> dict:
    juego: dict = {
        "cerrado": 50.0,          # 0 = la otra madre abrió; 100 = puerta cerrada
        "empuje": float(datos.get("empuje", 18)),
        "brillo_golpe": 0.0,
        "tiempo_total": float(datos["tiempo"]),
        "tiempo_restante": float(datos["tiempo"]),
        "resultado": "",
    }
    return juego


def manejar_evento(evento: pygame.event.Event, juego: dict) -> None:
    golpe: bool = False
    if evento.type == pygame.KEYDOWN and evento.key == pygame.K_SPACE:
        golpe = True
    elif evento.type == pygame.MOUSEBUTTONDOWN and evento.button == 1:
        golpe = True
    if golpe:
        juego["cerrado"] = juego["cerrado"] + FUERZA_POR_GOLPE
        juego["brillo_golpe"] = 1.0
        if juego["cerrado"] >= 100:
            juego["resultado"] = "exito"


def actualizar(juego: dict, dt: float) -> None:
    juego["empuje"] = juego["empuje"] + AUMENTO_DE_EMPUJE * dt
    juego["cerrado"] = juego["cerrado"] - juego["empuje"] * dt
    if juego["brillo_golpe"] > 0:
        juego["brillo_golpe"] = juego["brillo_golpe"] - dt * 4
    juego["tiempo_restante"] = juego["tiempo_restante"] - dt
    if juego["cerrado"] <= 0 or juego["tiempo_restante"] <= 0:
        juego["resultado"] = "fallo"


def dibujar(ventana: pygame.Surface, juego: dict, fuentes: dict) -> None:
    centro_x: int = config.ANCHO // 2
    # Marco de la puerta y el hueco oscuro que queda abierto
    marco: pygame.Rect = pygame.Rect(centro_x - 160, 150, 320, 440)
    pygame.draw.rect(ventana, (5, 4, 10), marco)
    abierto: int = int(marco.width * (1 - juego["cerrado"] / 100))
    if abierto > 40:
        figuras.mano(ventana, marco.right - abierto // 2, marco.centery, 16)
    hoja_puerta: pygame.Rect = pygame.Rect(marco.x, marco.y, marco.width - abierto, marco.height)
    pygame.draw.rect(ventana, (110, 70, 40), hoja_puerta)
    pygame.draw.rect(ventana, (70, 42, 22), marco, 6)

    # Barra de qué tan cerrada está
    barra: pygame.Rect = pygame.Rect(centro_x - 250, marco.bottom + 30, 500, 22)
    pygame.draw.rect(ventana, config.COLOR_BOTON, barra, border_radius=10)
    lleno: pygame.Rect = pygame.Rect(barra.x, barra.y, int(barra.width * max(juego["cerrado"], 0) / 100), barra.height)
    color: tuple = config.COLOR_ACENTO if juego["brillo_golpe"] <= 0 else (255, 230, 150)
    pygame.draw.rect(ventana, color, lleno, border_radius=10)

    texto: str = "¡Presiona ESPACIO lo más rápido que puedas!"
    superficie: pygame.Surface = fuentes["opcion"].render(texto, True, config.COLOR_TEXTO)
    ventana.blit(superficie, (centro_x - superficie.get_width() // 2, barra.bottom + 14))
