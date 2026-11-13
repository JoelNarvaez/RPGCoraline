"""Inventario de Coraline: los objetos se guardan como una lista de nombres.

Ejemplo: ["piedra_con_agujero", "llave_negra"]

No usa pygame: el panel que dibuja el inventario está en interfaz/pantalla_inventario.py

Responsable: Persona B
"""


def tiene_objeto(estado: dict, objeto: str) -> bool:
    return objeto in estado["inventario"]


def agregar_objeto(estado: dict, objeto: str) -> None:
    """Agrega el objeto, sin repetirlo si ya lo tiene."""
    if not tiene_objeto(estado, objeto):
        estado["inventario"].append(objeto)


def quitar_objeto(estado: dict, objeto: str) -> None:
    """Quita el objeto si lo tiene; si no, no hace nada."""
    if tiene_objeto(estado, objeto):
        estado["inventario"].remove(objeto)


def nombre_para_mostrar(objeto: str) -> str:
    """Convierte el nombre interno en texto para la pantalla.

    Ejemplo: "piedra_con_agujero" -> "Piedra con agujero"
    """
    texto: str = objeto.replace("_", " ")
    return texto.capitalize()
