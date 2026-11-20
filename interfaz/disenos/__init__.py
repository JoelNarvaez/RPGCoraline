"""DISENOS DE ESCENA.

Cada escena elige su diseno en el JSON con "diseno": "nombre". Si no pone
nada, usa POR_DEFECTO.

Para crear un diseno nuevo:
1. Copiar pink_palace.py con otro nombre (por ejemplo sotano.py).
2. Cambiar sus medidas, colores y lo que dibuja. Todo se arma con las
   funciones de interfaz/piezas.py.
3. Agregarlo a DISENOS aqui abajo.
4. Probarlo con: python -m herramientas.vista_previa <nodo>

Todo diseno tiene lo mismo:
- ANCHO_TEXTO: ancho en pixeles de los renglones de la narracion.
- maximo_lineas(fuentes): cuantos renglones caben (lo revisa el verificador).
- dibujar(ventana, contexto, nodo): dibuja la escena y regresa los
  rectangulos de las opciones, en orden, para saber donde dio clic el jugador.
"""

from interfaz.disenos import pink_palace
from interfaz.disenos import exploracion
from interfaz.disenos import libreta
from interfaz.disenos import puerta
from interfaz.disenos import exploracion_derecha

DISENOS = {
    "pink_palace": pink_palace,
    "exploracion": exploracion,
    "exploracion_derecha": exploracion_derecha,
    "libreta": libreta,
    "puerta": puerta,
}

POR_DEFECTO = "pink_palace"


def del_nodo(nodo: dict):

    """REGRESA EL MODULO DEL DISENO QUE USA ESTE NODO."""

    nombre = nodo.get("diseno", POR_DEFECTO)

    return DISENOS[nombre]
