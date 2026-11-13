"""Punto de entrada del juego. Ejecutar con: python main.py

Abre la ventana y corre el ciclo principal de pygame. En cada vuelta:
1. Revisa los eventos (teclado, mouse, cerrar ventana).
2. Actualiza la pantalla actual (animaciones).
3. Dibuja la pantalla actual.

Cada pantalla vive en interfaz/ y tiene las mismas tres funciones:
manejar_evento, actualizar y dibujar. Son cinco: menu, juego, inventario,
final y minijuego.

Responsable: Persona A
"""

import pygame

import config
from juego import motor
from interfaz import pantalla_menu
from interfaz import pantalla_juego
from interfaz import pantalla_inventario
from interfaz import pantalla_final
from interfaz import pantalla_minijuego
from interfaz import animaciones


def crear_contexto() -> dict:
    """Todo lo que las pantallas necesitan compartir.

    "estado" es la partida (lo único que se guarda en el archivo).
    Lo demás es temporal y solo sirve mientras el juego está abierto.
    """
    contexto: dict = {
        "nodos": motor.cargar_historia(config.RUTA_HISTORIA),
        "estado": None,
        "pantalla": "menu",
        "salir": False,
        "fuentes": {
            "titulo": pygame.font.Font(None, config.TAMANO_TITULO),
            "texto": pygame.font.Font(None, config.TAMANO_TEXTO),
            "opcion": pygame.font.Font(None, config.TAMANO_OPCION),
            "pequena": pygame.font.Font(None, config.TAMANO_PEQUENO),
        },
        # Nodo actual ya preparado para dibujar (lo llena pantalla_juego.preparar_nodo)
        "lineas": [],
        "total_letras": 0,
        "opciones": [],
        "minijuego": None,     # datos del minijuego en curso (pantalla_minijuego)
        # Datos de las animaciones
        "letras_visibles": 0.0,
        "transparencia": 0.0,
        "tiempo_menu": 0.0,
        "mensaje": "",
        "tiempo_mensaje": 0.0,
    }
    return contexto


def manejar_evento(evento: pygame.event.Event, contexto: dict) -> None:
    """Le pasa el evento a la pantalla actual. Si regresa el nombre de otra
    pantalla, se cambia a esa."""
    pantalla: str = contexto["pantalla"]
    siguiente: str = ""
    if pantalla == "menu":
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
    """`dt` son los segundos que pasaron desde la vuelta anterior."""
    pantalla: str = contexto["pantalla"]
    if pantalla == "menu":
        pantalla_menu.actualizar(contexto, dt)
    elif pantalla == "juego":
        pantalla_juego.actualizar(contexto, dt)
    elif pantalla == "inventario":
        pantalla_inventario.actualizar(contexto, dt)
    elif pantalla == "final":
        pantalla_final.actualizar(contexto, dt)
    elif pantalla == "minijuego":
        pantalla_minijuego.actualizar(contexto, dt)
    animaciones.avanzar_mensaje(contexto, dt)


def dibujar(ventana: pygame.Surface, contexto: dict) -> None:
    ventana.fill(config.COLOR_FONDO)
    pantalla: str = contexto["pantalla"]
    if pantalla == "menu":
        pantalla_menu.dibujar(ventana, contexto)
    elif pantalla == "juego":
        pantalla_juego.dibujar(ventana, contexto)
    elif pantalla == "inventario":
        # El inventario se dibuja encima del juego, como un panel
        pantalla_juego.dibujar(ventana, contexto)
        pantalla_inventario.dibujar(ventana, contexto)
    elif pantalla == "final":
        pantalla_final.dibujar(ventana, contexto)
    elif pantalla == "minijuego":
        pantalla_minijuego.dibujar(ventana, contexto)
    # Los avisos ("Partida guardada") van encima de cualquier pantalla
    animaciones.dibujar_mensaje(ventana, contexto)
    pygame.display.flip()


def main() -> None:
    pygame.init()
    ventana: pygame.Surface = pygame.display.set_mode((config.ANCHO, config.ALTO))
    pygame.display.set_caption(config.TITULO)
    reloj: pygame.time.Clock = pygame.time.Clock()

    contexto: dict = crear_contexto()

    while not contexto["salir"]:
        # tick() espera lo necesario para no pasar de FPS y regresa milisegundos
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
