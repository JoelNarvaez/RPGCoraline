"""Minijuego "escalera_sotano": subir la escalera del sótano sin que te oiga el otro padre.

Pixel art dibujado con código, con la misma técnica que los fondos de las
escenas (lienzo de 640x360 escalado x2, capa fija + lo que se mueve).
Es el sótano de sotano.py. Lo que queda del otro padre anda a ciegas por el
piso: no ve, pero oye. Como en el libro, Coraline tiene que quedarse muy
quieta cuando la busca y subir cuando no la escucha.

- Mantener presionado Espacio (o el clic) = Coraline sube la escalera.
- La criatura camina tanteando, de pronto se detiene (aviso) y se pone a
  escuchar (salen ondas de su cabeza). Si Coraline se mueve mientras
  escucha, la oye: se lanza contra la escalera, Coraline resbala unos
  escalones y pierde una vida.
- Gana al llegar a la puerta de arriba. Pierde sin vidas o sin tiempo.

En el nodo:
  "tipo": "escalera_sotano"
  "instruccion": texto que se muestra antes de empezar
  "tiempo": segundos

Responsable: Persona A
"""

import math
import random

import pygame

import config
from interfaz.fondos.pintura import ANCHO, ALTO
from interfaz.fondos.pintura import orillas_oscuras, mostrar
from interfaz.fondos import personajes
from interfaz.fondos import sotano

VIDAS: int = 3
VELOCIDAD_SUBIR: float = 0.2              # parte de la escalera por segundo (5 s presionando)
RESBALON: float = 0.25                    # cuanto baja cuando la atrapan
VELOCIDAD_CRIATURA: float = 70.0          # pixeles del lienzo por segundo
ORILLAS_CRIATURA: tuple = (180, 500)      # de donde a donde camina

# CUANTO DURA CADA COSA QUE HACE LA CRIATURA (MINIMO, MAXIMO) EN SEGUNDOS
DURACION_BUSCA: tuple = (1.4, 2.6)
DURACION_AVISO: float = 0.6
DURACION_ESCUCHA: tuple = (1.2, 2.0)
DURACION_LANZA: float = 0.9

ALTOS: dict = {"busca": 80, "aviso": 86, "escucha": 94, "lanza": 98}

CAPAS: dict = {}


# ------------------------------------------------------------ parte fija

def crear_fijo() -> pygame.Surface:
    lienzo: pygame.Surface = pygame.Surface((ANCHO, ALTO))
    sotano.dibujar_sotano(lienzo)
    orillas_oscuras(lienzo)
    return lienzo


# ------------------------------------------------------------ el juego

def cambiar_estado(juego: dict, estado: str) -> None:
    """La criatura pasa a otro estado y se sortea cuánto va a durar."""
    juego["estado"] = estado
    juego["reloj_estado"] = 0.0
    if estado == "busca":
        juego["duracion"] = random.uniform(DURACION_BUSCA[0], DURACION_BUSCA[1])
    elif estado == "aviso":
        juego["duracion"] = DURACION_AVISO
    elif estado == "escucha":
        juego["duracion"] = random.uniform(DURACION_ESCUCHA[0], DURACION_ESCUCHA[1])
    else:
        juego["duracion"] = DURACION_LANZA


def iniciar(datos: dict) -> dict:
    if "fijo" not in CAPAS:
        CAPAS["fijo"] = crear_fijo()
    juego: dict = {
        "avance": 0.0,
        "subiendo": False,
        "vidas": VIDAS,
        "x_criatura": float(ORILLAS_CRIATURA[0]),
        "direccion": 1,
        "x_lanza": 0.0,                     # desde donde se lanzó
        "estado": "busca",
        "reloj_estado": 0.0,
        "duracion": 0.0,
        "reloj": 0.0,
        "tiempo_total": float(datos["tiempo"]),
        "tiempo_restante": float(datos["tiempo"]),
        "resultado": "",
    }
    cambiar_estado(juego, "busca")
    return juego


def manejar_evento(evento: pygame.event.Event, juego: dict) -> None:
    if evento.type == pygame.KEYDOWN and evento.key == pygame.K_SPACE:
        juego["subiendo"] = True
    elif evento.type == pygame.KEYUP and evento.key == pygame.K_SPACE:
        juego["subiendo"] = False
    elif evento.type == pygame.MOUSEBUTTONDOWN and evento.button == 1:
        juego["subiendo"] = True
    elif evento.type == pygame.MOUSEBUTTONUP and evento.button == 1:
        juego["subiendo"] = False


def actualizar(juego: dict, dt: float) -> None:
    juego["reloj"] = juego["reloj"] + dt
    juego["reloj_estado"] = juego["reloj_estado"] + dt
    estado: str = juego["estado"]

    # CORALINE SUBE MIENTRAS SE PRESIONE (MENOS CUANDO LA ESTAN ATRAPANDO)
    if juego["subiendo"] and estado != "lanza":
        juego["avance"] = min(1.0, juego["avance"] + VELOCIDAD_SUBIR * dt)

    if estado == "busca":
        juego["x_criatura"] = juego["x_criatura"] + juego["direccion"] * VELOCIDAD_CRIATURA * dt
        if juego["x_criatura"] < ORILLAS_CRIATURA[0] or juego["x_criatura"] > ORILLAS_CRIATURA[1]:
            juego["direccion"] = -juego["direccion"]
        if juego["reloj_estado"] > juego["duracion"]:
            cambiar_estado(juego, "aviso")

    elif estado == "aviso":
        if juego["reloj_estado"] > juego["duracion"]:
            cambiar_estado(juego, "escucha")

    elif estado == "escucha":
        if juego["subiendo"]:
            # LA OYO: SE LANZA, CORALINE RESBALA Y PIERDE UNA VIDA
            juego["vidas"] = juego["vidas"] - 1
            juego["avance"] = max(0.0, juego["avance"] - RESBALON)
            juego["x_lanza"] = juego["x_criatura"]
            cambiar_estado(juego, "lanza")
        elif juego["reloj_estado"] > juego["duracion"]:
            cambiar_estado(juego, "busca")

    elif estado == "lanza":
        # VA HACIA LA ESCALERA Y LUEGO SE REGRESA
        ida: float = math.sin(min(1.0, juego["reloj_estado"] / juego["duracion"]) * math.pi)
        destino: float = sotano.ESCALERA_ABAJO[0] - 30
        juego["x_criatura"] = juego["x_lanza"] + (destino - juego["x_lanza"]) * ida
        if juego["reloj_estado"] > juego["duracion"]:
            juego["x_criatura"] = juego["x_lanza"]
            cambiar_estado(juego, "busca")

    juego["tiempo_restante"] = juego["tiempo_restante"] - dt

    if juego["resultado"] == "":
        if juego["avance"] >= 1.0:
            juego["resultado"] = "exito"
        elif juego["vidas"] <= 0 or juego["tiempo_restante"] <= 0:
            juego["resultado"] = "fallo"


# ------------------------------------------------------------ lo que se mueve

def dibujar_ondas(lienzo: pygame.Surface, juego: dict) -> None:
    """Cuando escucha, salen ondas de su cabeza (como si oyera todo el sótano)."""
    cabeza: tuple = (int(juego["x_criatura"]), sotano.Y_PISO - ALTOS["escucha"] - 10)
    for i in range(3):
        radio: int = 8 + int(((juego["reloj"] * 1.5 + i / 3) % 1) * 40)
        alfa: int = int(200 * (1 - (radio - 8) / 40))
        capa: pygame.Surface = pygame.Surface((radio * 2 + 2, radio * 2 + 2), pygame.SRCALPHA)
        pygame.draw.circle(capa, (220, 220, 240, alfa), (radio + 1, radio + 1), radio, 1)
        lienzo.blit(capa, (cabeza[0] - radio - 1, cabeza[1] - radio - 1))


def dibujar_aviso(lienzo: pygame.Surface, juego: dict) -> None:
    """Un signo de interrogación sobre su cabeza: se detiene, va a escuchar."""
    x: int = int(juego["x_criatura"])
    y: int = sotano.Y_PISO - ALTOS["aviso"] - 34
    pygame.draw.arc(lienzo, (240, 230, 200), (x - 4, y, 8, 8), -0.5, 3.4, 2)
    pygame.draw.line(lienzo, (240, 230, 200), (x + 2, y + 6), (x, y + 10), 2)
    pygame.draw.rect(lienzo, (240, 230, 200), (x - 1, y + 13, 2, 2))


def dibujar_coraline(lienzo: pygame.Surface, juego: dict) -> None:
    """Coraline en su escalón. Al subir da saltitos y el escalón cruje (rayitas)."""
    pie: tuple = sotano.punto_escalera(juego["avance"])
    moviendose: bool = juego["subiendo"] and juego["estado"] != "lanza"
    salto: int = int(abs(math.sin(juego["reloj"] * 10)) * 2) if moviendose else 0

    personajes.dibujar_coraline_chica(lienzo, pie[0], pie[1] - salto, True)

    if moviendose and int(juego["reloj"] * 6) % 2 == 0:
        for dx in [-14, 14]:
            pygame.draw.line(lienzo, (200, 190, 170), (pie[0] + dx, pie[1] - 2), (pie[0] + dx + (dx // 7), pie[1] - 6))


def dibujar_vidas(ventana: pygame.Surface, juego: dict) -> None:
    """Las vidas como botoncitos blancos arriba a la izquierda (los perdidos, apagados)."""
    for i in range(VIDAS):
        centro: tuple = (60 + i * 34, 76)
        color: tuple = (236, 232, 222) if i < juego["vidas"] else (70, 64, 70)
        pygame.draw.circle(ventana, (16, 12, 22), centro, 13)
        pygame.draw.circle(ventana, color, centro, 11)
        for dx, dy in [(-3, -3), (3, -3), (-3, 3), (3, 3)]:
            pygame.draw.circle(ventana, (16, 12, 22), (centro[0] + dx, centro[1] + dy), 2)


def dibujar(ventana: pygame.Surface, juego: dict, fuentes: dict) -> None:
    lienzo: pygame.Surface = CAPAS["fijo"].copy()
    tiempo: float = juego["reloj"]
    estado: str = juego["estado"]

    sotano.dibujar_foco(lienzo, tiempo)
    sotano.dibujar_padre_derretido(lienzo, int(juego["x_criatura"]), sotano.Y_PISO, tiempo, ALTOS[estado], True, 1)

    if estado == "aviso":
        dibujar_aviso(lienzo, juego)
    elif estado == "escucha":
        dibujar_ondas(lienzo, juego)

    dibujar_coraline(lienzo, juego)

    # CUANDO ESCUCHA, TODO SE PONE UN POCO AZUL Y FRIO
    if estado == "escucha":
        frio: pygame.Surface = pygame.Surface((ANCHO, ALTO), pygame.SRCALPHA)
        frio.fill((40, 60, 120, 50))
        lienzo.blit(frio, (0, 0))
    elif estado == "lanza" and juego["reloj_estado"] < 0.15:
        lienzo.fill((120, 30, 30), special_flags=pygame.BLEND_ADD)

    mostrar(ventana, lienzo)
    dibujar_vidas(ventana, juego)

    # AVISO EN TEXTO, ARRIBA AL CENTRO
    if estado == "escucha":
        texto, color = "¡QUIETA! Está escuchando...", config.COLOR_FINAL_MALO
    elif estado == "lanza":
        texto, color = "¡Te oyó!", config.COLOR_FINAL_MALO
    else:
        texto, color = "Mantén Espacio para subir", config.COLOR_TENUE
    imagen: pygame.Surface = fuentes["opcion"].render(texto, True, color)
    ventana.blit(imagen, (config.ANCHO // 2 - imagen.get_width() // 2, 62))
