"""Animaciones del juego.

- Máquina de escribir: el texto del nodo aparece letra por letra.
- Desvanecer: al llegar a un nodo nuevo, la pantalla aparece desde negro.
- Mensaje: un aviso corto abajo de la pantalla ("Partida guardada").

Los valores de cada animación se guardan en el contexto y avanzan con `dt`,
los segundos que pasaron desde la vuelta anterior. Así la animación va
igual de rápido en cualquier computadora.

Responsable: Persona A
"""

import pygame

import config
from interfaz import dibujo


def reiniciar(contexto: dict) -> None:
    """Se llama cada vez que se entra a un nodo nuevo."""
    contexto["letras_visibles"] = 0.0
    contexto["transparencia"] = 255.0


# ------------------------------------------------------------ Máquina de escribir

def avanzar_maquina_escribir(contexto: dict, dt: float, total_letras: int) -> None:
    """Suma letras según LETRAS_POR_SEGUNDO, sin pasarse de `total_letras`."""
    letras: float = contexto["letras_visibles"] + config.LETRAS_POR_SEGUNDO * dt
    if letras > total_letras:
        letras = float(total_letras)
    contexto["letras_visibles"] = letras


def completar_texto(contexto: dict, total_letras: int) -> None:
    """Muestra todo el texto de golpe (cuando el jugador da clic antes de que termine)."""
    contexto["letras_visibles"] = float(total_letras)


def texto_terminado(contexto: dict, total_letras: int) -> bool:
    """True cuando ya se ven todas las letras. Hasta entonces no salen las opciones."""
    return contexto["letras_visibles"] >= total_letras


# ------------------------------------------------------------ Desvanecer

def avanzar_desvanecer(contexto: dict, dt: float) -> None:
    """Baja "transparencia" de 255 a 0 en DURACION_DESVANECER segundos."""
    velocidad: float = 255 / config.DURACION_DESVANECER
    transparencia: float = contexto["transparencia"] - velocidad * dt
    if transparencia < 0:
        transparencia = 0.0
    contexto["transparencia"] = transparencia


def dibujar_desvanecer(ventana: pygame.Surface, transparencia: float) -> None:
    """Dibuja un rectángulo negro encima de todo, con la transparencia indicada."""
    if transparencia > 0:
        dibujo.dibujar_capa(ventana, (0, 0, 0), int(transparencia))


# ------------------------------------------------------------ Mensajes

def mostrar_mensaje(contexto: dict, texto: str) -> None:
    """Muestra un aviso por DURACION_MENSAJE segundos."""
    contexto["mensaje"] = texto
    contexto["tiempo_mensaje"] = config.DURACION_MENSAJE


def avanzar_mensaje(contexto: dict, dt: float) -> None:
    if contexto["tiempo_mensaje"] > 0:
        contexto["tiempo_mensaje"] = contexto["tiempo_mensaje"] - dt


def dibujar_mensaje(ventana: pygame.Surface, contexto: dict) -> None:
    """Dibuja el aviso arriba a la derecha mientras le quede tiempo."""
    if contexto["tiempo_mensaje"] <= 0:
        return
    fuente: pygame.font.Font = contexto["fuentes"]["pequena"]
    superficie: pygame.Surface = fuente.render(contexto["mensaje"], True, config.COLOR_ACENTO)
    x: int = config.ANCHO - superficie.get_width() - 30
    ventana.blit(superficie, (x, 24))
