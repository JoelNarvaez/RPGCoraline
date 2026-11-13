"""Motor del juego: carga los nodos de historia/ y decide cómo se avanza.

Aquí NO se usa pygame. Este archivo solo maneja la lógica; lo que se ve en
pantalla está en interfaz/. Así el motor se puede probar sin abrir ventana.

Responsable: Persona A
"""

import json
import os

from juego import inventario
from juego import estadisticas


def cargar_archivo(ruta: str) -> dict:
    """Lee un archivo de capítulo y regresa su contenido completo."""
    with open(ruta, "r", encoding="utf-8") as archivo:
        datos: dict = json.load(archivo)
    return datos


def archivos_de_historia(carpeta: str) -> list:
    """Regresa las rutas de todos los .json de la carpeta, en orden."""
    nombres: list = os.listdir(carpeta)
    nombres.sort()
    rutas: list = []
    for nombre in nombres:
        if nombre.endswith(".json"):
            rutas.append(os.path.join(carpeta, nombre))
    return rutas


def cargar_historia(carpeta: str) -> dict:
    """Lee todos los .json de la carpeta y junta sus nodos en un solo diccionario.

    Regresa: {"cap01_n01": {...}, "cap01_n02": {...}, ...}
    """
    nodos: dict = {}
    for ruta in archivos_de_historia(carpeta):
        datos: dict = cargar_archivo(ruta)
        for nombre_nodo in datos["nodos"]:
            nodos[nombre_nodo] = datos["nodos"][nombre_nodo]
    return nodos


def nodo_actual(estado: dict, nodos: dict) -> dict:
    """Regresa el nodo en el que va el jugador."""
    return nodos[estado["nodo_actual"]]


def es_final(nodo: dict) -> bool:
    """True si el nodo es un final (tiene el campo "final")."""
    return "final" in nodo


def cumple_requisitos(opcion: dict, estado: dict) -> bool:
    """True si el jugador cumple todo lo que pide el "requiere" de la opción."""
    if "requiere" not in opcion:
        return True
    requiere: dict = opcion["requiere"]

    if "objetos" in requiere:
        for objeto in requiere["objetos"]:
            if not inventario.tiene_objeto(estado, objeto):
                return False

    if "estadisticas" in requiere:
        for nombre in requiere["estadisticas"]:
            minimo: int = requiere["estadisticas"][nombre]
            if not estadisticas.cumple_requisito(estado, nombre, minimo):
                return False

    return True


def opciones_disponibles(nodo: dict, estado: dict) -> list:
    """Regresa solo las opciones cuyo "requiere" se cumple con el estado actual."""
    disponibles: list = []
    for opcion in nodo["opciones"]:
        if cumple_requisitos(opcion, estado):
            disponibles.append(opcion)
    return disponibles


def aplicar_efectos(opcion: dict, estado: dict) -> None:
    """Aplica los "efectos" de la opción elegida (objetos y estadísticas)."""
    if "efectos" not in opcion:
        return
    efectos: dict = opcion["efectos"]

    if "agregar_objetos" in efectos:
        for objeto in efectos["agregar_objetos"]:
            inventario.agregar_objeto(estado, objeto)

    if "quitar_objetos" in efectos:
        for objeto in efectos["quitar_objetos"]:
            inventario.quitar_objeto(estado, objeto)

    if "estadisticas" in efectos:
        for nombre in efectos["estadisticas"]:
            estadisticas.modificar(estado, nombre, efectos["estadisticas"][nombre])


def elegir_opcion(opcion: dict, estado: dict) -> None:
    """Lo que pasa cuando el jugador elige una opción:
    aplica sus efectos y mueve al jugador al nodo destino."""
    aplicar_efectos(opcion, estado)
    estado["nodo_actual"] = opcion["destino"]


def es_minijuego(nodo: dict) -> bool:
    """True si el nodo tiene un minijuego en lugar de opciones."""
    return "minijuego" in nodo


def resolver_minijuego(minijuego: dict, estado: dict, gano: bool) -> None:
    """Aplica el resultado del minijuego ("exito" o "fallo"): sus efectos y su destino.

    Cada resultado tiene la misma forma que una opción: {"destino": ..., "efectos": ...}
    """
    if gano:
        resultado: dict = minijuego["exito"]
    else:
        resultado = minijuego["fallo"]
    elegir_opcion(resultado, estado)
