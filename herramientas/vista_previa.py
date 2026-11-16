"""Abre el juego directo en una escena, para probar diseños sin jugar desde el inicio.

Ejecutar con:
    python -m herramientas.vista_previa cap08_n03             (abre la ventana ahí)
    python -m herramientas.vista_previa cap08_n03 --captura   (guarda capturas/cap08_n03.png)

Con --captura no abre ventana: dibuja la escena con el texto completo y las
opciones visibles, y guarda la imagen en la carpeta capturas/.

La partida empieza nueva (inventario vacío, estadísticas iniciales), así que
las opciones con "requiere" pueden no aparecer.
"""

import os
import sys

import pygame

import config
import main as juego_principal
from juego import motor
from juego import partida
from interfaz import animaciones
from interfaz import disenos
from interfaz import pantalla_juego

CARPETA_CAPTURAS: str = os.path.join(config.CARPETA_BASE, "capturas")


def preparar(nombre_nodo: str) -> dict:
    """Crea el contexto del juego parado en la escena pedida."""
    contexto: dict = juego_principal.crear_contexto()
    contexto["estado"] = partida.nuevo_estado()
    contexto["estado"]["nodo_actual"] = nombre_nodo
    contexto["pantalla"] = "juego"
    pantalla_juego.preparar_nodo(contexto)
    return contexto


def guardar_captura(nombre_nodo: str) -> None:
    """Dibuja la escena ya terminada de escribir y la guarda como imagen."""
    os.environ["SDL_VIDEODRIVER"] = "dummy"
    pygame.init()
    ventana: pygame.Surface = pygame.display.set_mode((config.ANCHO, config.ALTO))
    contexto: dict = preparar(nombre_nodo)
    animaciones.completar_texto(contexto, contexto["total_letras"])
    contexto["transparencia"] = 0.0
    pantalla_juego.dibujar(ventana, contexto)

    os.makedirs(CARPETA_CAPTURAS, exist_ok=True)
    ruta: str = os.path.join(CARPETA_CAPTURAS, nombre_nodo + ".png")
    pygame.image.save(ventana, ruta)

    nodo: dict = contexto["nodos"][nombre_nodo]
    diseno = disenos.del_nodo(nodo)
    print("Diseño:   ", nodo.get("diseno", disenos.POR_DEFECTO))
    print("Renglones:", len(contexto["lineas"]), "de", diseno.maximo_lineas(contexto["fuentes"]))
    print("Captura:  ", ruta)
    pygame.quit()


def abrir_ventana(nombre_nodo: str) -> None:
    """Abre el juego normal, pero empezando en la escena pedida."""
    pygame.init()
    ventana: pygame.Surface = pygame.display.set_mode((config.ANCHO, config.ALTO))
    pygame.display.set_caption(config.TITULO + " - " + nombre_nodo)
    reloj: pygame.time.Clock = pygame.time.Clock()
    contexto: dict = preparar(nombre_nodo)

    while not contexto["salir"]:
        dt: float = reloj.tick(config.FPS) / 1000
        for evento in pygame.event.get():
            if evento.type == pygame.QUIT:
                contexto["salir"] = True
            else:
                juego_principal.manejar_evento(evento, contexto)
        juego_principal.actualizar(contexto, dt)
        juego_principal.dibujar(ventana, contexto)

    pygame.quit()


def main() -> None:
    if len(sys.argv) < 2:
        print("Uso: python -m herramientas.vista_previa <nodo> [--captura]")
        return

    nombre_nodo: str = sys.argv[1]
    if nombre_nodo not in motor.cargar_historia(config.RUTA_HISTORIA):
        print("No existe el nodo", nombre_nodo)
        return

    if "--captura" in sys.argv:
        guardar_captura(nombre_nodo)
    else:
        abrir_ventana(nombre_nodo)


if __name__ == "__main__":
    main()
