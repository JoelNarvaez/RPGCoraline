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
from interfaz.fondos import exterior_gato
from interfaz.fondos import gato_dialogo
from interfaz.fondos import teatro_vecinas
from interfaz.fondos import teatro_funcion
from interfaz.fondos import cocina_propuesta
from interfaz.fondos import huida_pasillo
from interfaz.fondos import salon_regreso

# CAPITULO 5: UNA FAMILIA DE UNA SOLA PERSONA
from interfaz.fondos import cena_sola
from interfaz.fondos import jardin_noche
from interfaz.fondos import recortes_vecinas
from interfaz.fondos import espejo_pasillo
from interfaz.fondos import espejo_padres
from interfaz.fondos import valentia_gato
from interfaz.fondos import bienvenida_otra_madre

# CAPITULO 6: DETRAS DEL ESPEJO
from interfaz.fondos import cuarto_manana
from interfaz.fondos import fin_del_mundo
from interfaz.fondos import estudio_otro_padre
from interfaz.fondos import espejo_otra_madre
from interfaz.fondos import escarabajo_espejo

# CAPITULO 7: LOS NINOS FANTASMA
from interfaz.fondos import hueco_espejo
from interfaz.fondos import ninos_fantasma
from interfaz.fondos import almas_perdidas
from interfaz.fondos import advertencia_fantasmas
from interfaz.fondos import beso_fantasma

# CAPITULO 8: EL JUEGO
from interfaz.fondos import desayuno_otra_madre
from interfaz.fondos import trato_juego
from interfaz.fondos import caja_juguetes
from interfaz.fondos import vista_piedra
from interfaz.fondos import teatro_abandonado
from interfaz.fondos import telarana_canica
from interfaz.fondos import huida_teatro

# CAPITULO 9: EL SOTANO
from interfaz.fondos import casa_torcida
from interfaz.fondos import pasillo_sotano
from interfaz.fondos import sotano
from interfaz.fondos import padre_derretido
from interfaz.fondos import sotano_cazando
from interfaz.fondos import mundo_gris

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
    "exterior_gato": exterior_gato,
    "gato_dialogo": gato_dialogo,
    "teatro_vecinas": teatro_vecinas,
    "teatro_funcion": teatro_funcion,
    "cocina_propuesta": cocina_propuesta,
    "huida_pasillo": huida_pasillo,
    "salon_regreso": salon_regreso,

    # CAPITULO 5
    "cena_sola": cena_sola,
    "jardin_noche": jardin_noche,
    "recortes_vecinas": recortes_vecinas,
    "espejo_pasillo": espejo_pasillo,
    "espejo_padres": espejo_padres,
    "valentia_gato": valentia_gato,
    "bienvenida_otra_madre": bienvenida_otra_madre,

    # CAPITULO 6
    "cuarto_manana": cuarto_manana,
    "fin_del_mundo": fin_del_mundo,
    "estudio_otro_padre": estudio_otro_padre,
    "espejo_otra_madre": espejo_otra_madre,
    "escarabajo_espejo": escarabajo_espejo,

    # CAPITULO 7
    "hueco_espejo": hueco_espejo,
    "ninos_fantasma": ninos_fantasma,
    "almas_perdidas": almas_perdidas,
    "advertencia_fantasmas": advertencia_fantasmas,
    "beso_fantasma": beso_fantasma,

    # CAPITULO 8
    "desayuno_otra_madre": desayuno_otra_madre,
    "trato_juego": trato_juego,
    "caja_juguetes": caja_juguetes,
    "vista_piedra": vista_piedra,
    "teatro_abandonado": teatro_abandonado,
    "telarana_canica": telarana_canica,
    "huida_teatro": huida_teatro,

    # CAPITULO 9
    "casa_torcida": casa_torcida,
    "pasillo_sotano": pasillo_sotano,
    "sotano": sotano,
    "padre_derretido": padre_derretido,
    "sotano_cazando": sotano_cazando,
    "mundo_gris": mundo_gris,
}
