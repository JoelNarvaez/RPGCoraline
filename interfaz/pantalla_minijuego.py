"""Pantalla de minijuego. Tiene tres fases:

1. "instrucciones": explica el reto. Clic o Espacio para empezar.
2. "jugando": corre el minijuego del tipo que diga el nodo.
3. "resultado": muestra si ganó o perdió. Clic o Espacio para seguir.

Al terminar, el motor manda al jugador al destino de "exito" o de "fallo".

Responsable: Persona A
"""

import pygame

import config
from juego import motor
from interfaz import dibujo
from interfaz import animaciones
from interfaz import pantalla_juego
from interfaz import piezas
from interfaz.minijuegos import clic
from interfaz.minijuegos import arrastrar
from interfaz.minijuegos import buscar
from interfaz.minijuegos import esquivar
from interfaz.minijuegos import presionar
from interfaz.minijuegos import recorrido
from interfaz.minijuegos import taza_te
from interfaz.minijuegos import llave_puerta
from interfaz.minijuegos import canicas_piedra
from interfaz.minijuegos import escalera_sotano

# Cada tipo de minijuego y el módulo que lo maneja
MODULOS: dict = {
    "clic": clic,
    "arrastrar": arrastrar,
    "buscar": buscar,
    "esquivar": esquivar,
    "presionar": presionar,
    "recorrido": recorrido,
    "taza_te": taza_te,
    "llave_puerta": llave_puerta,
    "canicas_piedra": canicas_piedra,
    "escalera_sotano": escalera_sotano,
}
TITULOS: dict = {
    "clic": "Explora",
    "arrastrar": "Arrastra",
    "buscar": "Busca con la piedra",
    "esquivar": "¡Escapa!",
    "presionar": "¡Rápido!",
    "recorrido": "Recorre la casa",
    "taza_te": "Lee las hojas",
    "llave_puerta": "Abre la puerta",
    "canicas_piedra": "Busca con la piedra",
    "escalera_sotano": "Sube sin que te oiga",
}


def iniciar(contexto: dict) -> None:
    """Se llama desde la pantalla de juego cuando el jugador acepta el reto."""
    nodo: dict = motor.nodo_actual(contexto["estado"], contexto["nodos"])
    contexto["minijuego"] = {
        "datos": nodo["minijuego"],
        "fase": "instrucciones",
        "juego": None,
        "gano": False,
    }


def pidio_continuar(evento: pygame.event.Event) -> bool:
    if evento.type == pygame.MOUSEBUTTONDOWN and evento.button == 1:
        return True
    return evento.type == pygame.KEYDOWN and evento.key in [pygame.K_SPACE, pygame.K_RETURN]


def terminar(contexto: dict) -> str:
    """Manda al jugador al destino del resultado y regresa la siguiente pantalla."""
    mj: dict = contexto["minijuego"]
    motor.resolver_minijuego(mj["datos"], contexto["estado"], mj["gano"])
    pantalla_juego.preparar_nodo(contexto)
    nodo: dict = motor.nodo_actual(contexto["estado"], contexto["nodos"])
    if motor.es_final(nodo):
        return "final"
    return "juego"


def manejar_evento(evento: pygame.event.Event, contexto: dict) -> str:
    mj: dict = contexto["minijuego"]
    modulo = MODULOS[mj["datos"]["tipo"]]

    if mj["fase"] == "instrucciones":
        if pidio_continuar(evento):
            mj["juego"] = modulo.iniciar(mj["datos"])
            mj["fase"] = "jugando"
    elif mj["fase"] == "jugando":
        modulo.manejar_evento(evento, mj["juego"])
    elif mj["fase"] == "resultado":
        if pidio_continuar(evento):
            return terminar(contexto)
    return ""


def actualizar(contexto: dict, dt: float) -> None:
    mj: dict = contexto["minijuego"]
    if mj["fase"] != "jugando":
        return
    modulo = MODULOS[mj["datos"]["tipo"]]
    modulo.actualizar(mj["juego"], dt)
    if mj["juego"]["resultado"] != "":
        mj["gano"] = mj["juego"]["resultado"] == "exito"
        mj["fase"] = "resultado"


def dibujar_barra_tiempo(ventana: pygame.Surface, juego: dict) -> None:
    fraccion: float = max(juego["tiempo_restante"], 0) / juego["tiempo_total"]
    pygame.draw.rect(ventana, config.COLOR_BOTON, (40, 30, config.ANCHO - 80, 14), border_radius=7)
    color: tuple = config.COLOR_ACENTO if fraccion > 0.3 else config.COLOR_FINAL_MALO
    pygame.draw.rect(ventana, color, (40, 30, int((config.ANCHO - 80) * fraccion), 14), border_radius=7)


def dibujar(ventana: pygame.Surface, contexto: dict) -> None:
    mj: dict = contexto["minijuego"]
    datos: dict = mj["datos"]
    fuentes: dict = contexto["fuentes"]
    centro: int = config.ANCHO // 2

    nodo: dict = motor.nodo_actual(contexto["estado"], contexto["nodos"])
    piezas.fondo(ventana, nodo)

    if mj["fase"] == "instrucciones":
        dibujo.dibujar_capa(ventana, (0, 0, 0), 120)
        dibujo.dibujar_texto_centrado(ventana, TITULOS[datos["tipo"]], fuentes["titulo"],
                                      config.COLOR_ACENTO, centro, 200)
        lineas: list = dibujo.dividir_en_lineas(datos["instruccion"], fuentes["texto"], 900)
        y: int = 300
        for linea in lineas:
            dibujo.dibujar_texto_centrado(ventana, linea, fuentes["texto"], config.COLOR_TEXTO, centro, y)
            y = y + 36
        dibujo.dibujar_texto_centrado(ventana, "Tienes " + str(datos["tiempo"]) + " segundos",
                                      fuentes["opcion"], config.COLOR_TENUE, centro, y + 20)
        dibujo.dibujar_texto_centrado(ventana, "Clic o Espacio para empezar", fuentes["pequena"],
                                      config.COLOR_TENUE, centro, config.ALTO - 60)

    elif mj["fase"] == "jugando":
        modulo = MODULOS[datos["tipo"]]
        modulo.dibujar(ventana, mj["juego"], fuentes)
        dibujar_barra_tiempo(ventana, mj["juego"])

    elif mj["fase"] == "resultado":
        modulo = MODULOS[datos["tipo"]]
        modulo.dibujar(ventana, mj["juego"], fuentes)
        dibujo.dibujar_capa(ventana, (0, 0, 0), 170)
        if mj["gano"]:
            titulo: str = "¡Lo lograste!"
            color: tuple = config.COLOR_FINAL_BUENO
        else:
            titulo = "No lo lograste..."
            color = config.COLOR_FINAL_MALO
        dibujo.dibujar_texto_centrado(ventana, titulo, fuentes["titulo"], color, centro, 260)
        dibujo.dibujar_texto_centrado(ventana, "Clic o Espacio para continuar", fuentes["pequena"],
                                      config.COLOR_TENUE, centro, 380)
