"""Estadísticas de Coraline. Abren o bloquean opciones según su valor.

No usa pygame: las barras que se ven en pantalla están en interfaz/pantalla_inventario.py

Responsable: Persona B
"""

# Valores con los que empieza una partida nueva.
# PENDIENTE: confirmar entre los dos qué estadísticas se usan.
ESTADISTICAS_INICIALES: dict = {
    "valentia": 0,
    "cordura": 10,
    "confianza_gato": 0,
}

# Rango de cada estadística (propuesta: confirmar entre los dos).
VALOR_MINIMO: int = 0
VALOR_MAXIMO: int = 10


def cumple_requisito(estado: dict, nombre: str, minimo: int) -> bool:
    """True si la estadística `nombre` es mayor o igual a `minimo`."""
    if nombre not in estado["estadisticas"]:
        return False
    return estado["estadisticas"][nombre] >= minimo


def modificar(estado: dict, nombre: str, cantidad: int) -> None:
    """Suma `cantidad` (puede ser negativa) a la estadística,
    sin salirse de VALOR_MINIMO y VALOR_MAXIMO."""
    valor: int = estado["estadisticas"].get(nombre, 0) + cantidad
    if valor < VALOR_MINIMO:
        valor = VALOR_MINIMO
    if valor > VALOR_MAXIMO:
        valor = VALOR_MAXIMO
    estado["estadisticas"][nombre] = valor
