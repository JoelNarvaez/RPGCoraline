"""Estado de una partida y guardado/carga en archivo JSON. No usa pygame.

Responsable: Persona A
"""

import json
import os

from juego.estadisticas import ESTADISTICAS_INICIALES

NODO_INICIAL: str = "cap01_n01"


def nuevo_estado() -> dict:
    """Estado de una partida nueva."""
    estado: dict = {
        "nodo_actual": NODO_INICIAL,
        "inventario": [],
        "estadisticas": dict(ESTADISTICAS_INICIALES),
    }
    return estado


def guardar_partida(estado: dict, ruta: str) -> None:
    """Escribe el estado en un archivo JSON (crea la carpeta si no existe)."""
    os.makedirs(os.path.dirname(ruta), exist_ok=True)
    with open(ruta, "w", encoding="utf-8") as archivo:
        json.dump(estado, archivo, ensure_ascii=False, indent=2)


def cargar_partida(ruta: str) -> dict:
    """Regresa el estado guardado, o None si no existe el archivo o está dañado.

    No usa print: la pantalla del menú es la que avisa al jugador.
    """
    if not os.path.exists(ruta):
        return None
    try:
        with open(ruta, "r", encoding="utf-8") as archivo:
            estado: dict = json.load(archivo)
    except json.JSONDecodeError:
        return None
    return estado
