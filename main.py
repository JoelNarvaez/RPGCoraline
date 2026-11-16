
"""Punto de entrada del juego. Ejecutar con: python main.py

Abre la ventana y corre el ciclo principal de pygame.
En cada vuelta:
1. Revisa los eventos.
2. Actualiza la pantalla actual.
3. Dibuja la pantalla actual.

Cada pantalla vive en interfaz/ y tiene las mismas tres funciones:
manejar_evento, actualizar y dibujar.

Responsable: Persona A
"""

import os
import pygame

import config
from juego import motor
from interfaz import pantalla_menu
from interfaz import pantalla_intro
from interfaz import pantalla_juego
from interfaz import pantalla_inventario
from interfaz import pantalla_final
from interfaz import pantalla_minijuego
from interfaz import animaciones


def crear_contexto() -> dict:
    """Todo lo que las pantallas necesitan compartir."""

    # CARGAMOS LA TIPOGRAFIA ESPECIAL PARA EL TITULO
    fuente_coraline = pygame.font.Font(
        os.path.join(
            config.RUTA_FUENTES,
            "BerkshireSwash-Regular.ttf"
        ),
        88
    )

    # CARGAMOS LA TIPOGRAFIA PARA LA FRASE DE INTRO
    fuente_frase = pygame.font.Font(
        os.path.join(
            config.RUTA_FUENTES,
            "BerkshireSwash-Regular.ttf"
        ),
        34
    )

    # CARGAMOS LA TIPOGRAFIA PARA EL TITULO DEL MENU
    fuente_menu = pygame.font.Font(
        os.path.join(
            config.RUTA_FUENTES,
            "BerkshireSwash-Regular.ttf"
        ),
        76
    )

    # FUENTE PARA EL TITULO PINK PALACE
    fuente_palace = pygame.font.Font(
        os.path.join(
            config.RUTA_FUENTES,
            "BerkshireSwash-Regular.ttf"
        ),
        34
    )

    # FUENTE DE MAQUINA DE ESCRIBIR PARA LA NARRACION
    fuente_maquina = pygame.font.Font(
        os.path.join(
            config.RUTA_FUENTES,
            "SpecialElite-Regular.ttf"
        ),
        20
    )

    contexto: dict = {
        "nodos": motor.cargar_historia(config.RUTA_HISTORIA),
        "capitulos": motor.cargar_capitulos(config.RUTA_HISTORIA),
        "estado": None,
        "pantalla": "intro",
        "salir": False,

        "fuentes": {
            "titulo": pygame.font.Font(
                None,
                config.TAMANO_TITULO
            ),
            "titulo_intro": fuente_coraline,
            "frase_intro": fuente_frase,
            "titulo_menu": fuente_menu,
            "titulo_palace": fuente_palace,
            "narracion": fuente_maquina,
            "texto": pygame.font.Font(
                None,
                config.TAMANO_TEXTO
            ),
            "opcion": pygame.font.Font(
                None,
                config.TAMANO_OPCION
            ),
            "pequena": pygame.font.Font(
                None,
                config.TAMANO_PEQUENO
            ),
        },

        # DATOS DEL JUEGO
        "lineas": [],
        "total_letras": 0,
        "opciones": [],
        "rect_opciones": [],
        "pregunta": "",
        "minijuego": None,

        # DATOS DE LAS ANIMACIONES
        "letras_visibles": 0.0,
        "transparencia": 0.0,
        "tiempo_menu": 0.0,
        "tiempo_intro": 0.0,
        "mensaje": "",
        "tiempo_mensaje": 0.0,
    }

    return contexto


def manejar_evento(evento: pygame.event.Event, contexto: dict) -> None:
    """Le pasa el evento a la pantalla actual."""

    pantalla: str = contexto["pantalla"]
    siguiente: str = ""

    if pantalla == "intro":
        siguiente = pantalla_intro.manejar_evento(evento, contexto)

    elif pantalla == "menu":
        siguiente = pantalla_menu.manejar_evento(evento, contexto)

    elif pantalla == "juego":
        siguiente = pantalla_juego.manejar_evento(evento, contexto)

    elif pantalla == "inventario":
        siguiente = pantalla_inventario.manejar_evento(evento, contexto)

    elif pantalla == "final":
        siguiente = pantalla_final.manejar_evento(evento, contexto)

    elif pantalla == "minijuego":
        siguiente = pantalla_minijuego.manejar_evento(evento, contexto)

    if siguiente == "salir":
        contexto["salir"] = True

    elif siguiente != "":
        contexto["pantalla"] = siguiente


def actualizar(contexto: dict, dt: float) -> None:
    """Actualiza la pantalla y sus animaciones."""

    pantalla: str = contexto["pantalla"]

    if pantalla == "intro":
        pantalla_intro.actualizar(contexto, dt)

        if contexto["tiempo_intro"] >= pantalla_intro.DURACION_INTRO:
            contexto["pantalla"] = "menu"

    elif pantalla == "menu":
        pantalla_menu.actualizar(contexto, dt)

    elif pantalla == "juego":
        pantalla_juego.actualizar(contexto, dt)

    elif pantalla == "final":
        pantalla_final.actualizar(contexto, dt)

    elif pantalla == "minijuego":
        pantalla_minijuego.actualizar(contexto, dt)

    animaciones.avanzar_mensaje(contexto, dt)


def dibujar(ventana: pygame.Surface, contexto: dict) -> None:
    """Dibuja la pantalla actual."""

    ventana.fill(config.COLOR_FONDO)

    pantalla: str = contexto["pantalla"]

    if pantalla == "intro":
        pantalla_intro.dibujar(ventana, contexto)

    elif pantalla == "menu":
        pantalla_menu.dibujar(ventana, contexto)

    elif pantalla == "juego":
        pantalla_juego.dibujar(ventana, contexto)

    elif pantalla == "inventario":
        # EL INVENTARIO SE DIBUJA ENCIMA DEL JUEGO
        pantalla_juego.dibujar(ventana, contexto)
        pantalla_inventario.dibujar(ventana, contexto)

    elif pantalla == "final":
        pantalla_final.dibujar(ventana, contexto)

    elif pantalla == "minijuego":
        pantalla_minijuego.dibujar(ventana, contexto)

    # MOSTRAMOS LOS AVISOS DEL JUEGO
    animaciones.dibujar_mensaje(ventana, contexto)

    pygame.display.flip()


def main() -> None:
    """INICIA EL VIDEOJUEGO."""

    pygame.init()

    ventana: pygame.Surface = pygame.display.set_mode(
        (config.ANCHO, config.ALTO)
    )

    pygame.display.set_caption(config.TITULO)

    reloj: pygame.time.Clock = pygame.time.Clock()

    contexto: dict = crear_contexto()

    while not contexto["salir"]:

        dt: float = reloj.tick(config.FPS) / 1000

        for evento in pygame.event.get():

            if evento.type == pygame.QUIT:
                contexto["salir"] = True

            else:
                manejar_evento(evento, contexto)

        actualizar(contexto, dt)
        dibujar(ventana, contexto)

    pygame.quit()


if __name__ == "__main__":
    main()