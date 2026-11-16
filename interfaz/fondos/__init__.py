"""FONDOS DIBUJADOS CON CODIGO.

Un nodo puede usar "fondo": "nombre" en lugar de "imagen". Cada fondo es un
archivo de esta carpeta con una funcion dibujar(ventana) que llena toda la
pantalla, y puede tener animacion (lluvia, luces...).

Las herramientas comunes (degradado, luces, orillas oscuras) estan en
pintura.py.

Para crear uno nuevo: copiar estudio_lluvioso.py, cambiar lo que dibuja y
agregarlo a FONDOS aqui abajo.
"""

from interfaz.fondos import estudio_lluvioso
from interfaz.fondos import salon_puerta
from interfaz.fondos import salon_ladrillos
from interfaz.fondos import mama_llave
from interfaz.fondos import pasillo_noche
from interfaz.fondos import niebla_spink
from interfaz.fondos import atico_ratones
from interfaz.fondos import te_actrices
from interfaz.fondos import hojas_te
from interfaz.fondos import piedra_spink
from interfaz.fondos import regreso_niebla
from interfaz.fondos import tienda_ropa
from interfaz.fondos import cocina_sola
from interfaz.fondos import pasillo_oscuro
from interfaz.fondos import otra_cocina
from interfaz.fondos import otro_cuarto
from interfaz.fondos import despedida_otros

FONDOS = {
    "estudio_lluvioso": estudio_lluvioso,
    "salon_puerta": salon_puerta,
    "salon_ladrillos": salon_ladrillos,
    "mama_llave": mama_llave,
    "pasillo_noche": pasillo_noche,
    "niebla_spink": niebla_spink,
    "atico_ratones": atico_ratones,
    "te_actrices": te_actrices,
    "hojas_te": hojas_te,
    "piedra_spink": piedra_spink,
    "regreso_niebla": regreso_niebla,
    "tienda_ropa": tienda_ropa,
    "cocina_sola": cocina_sola,
    "pasillo_oscuro": pasillo_oscuro,
    "otra_cocina": otra_cocina,
    "otro_cuarto": otro_cuarto,
    "despedida_otros": despedida_otros,
}
