"""Valores fijos del juego: ventana, colores, rutas y tamaños de letra.

Archivo compartido: si se cambia algo aquí, avisar al otro.
"""

import os

# Carpeta donde está este archivo. Así las rutas funcionan aunque el juego
# se abra desde otra carpeta.
CARPETA_BASE: str = os.path.dirname(os.path.abspath(__file__))

RUTA_HISTORIA: str = os.path.join(CARPETA_BASE, "historia")
RUTA_PARTIDA: str = os.path.join(CARPETA_BASE, "partidas", "partida.json")
RUTA_IMAGENES: str = os.path.join(CARPETA_BASE, "recursos", "imagenes")
RUTA_FUENTES: str = os.path.join(CARPETA_BASE, "recursos", "fuentes")
RUTA_SONIDOS: str = os.path.join(CARPETA_BASE, "recursos", "sonidos")

# Ventana
TITULO: str = "Coraline"
ANCHO: int = 1280
ALTO: int = 720
FPS: int = 60

# Colores (R, G, B)
COLOR_FONDO: tuple = (18, 16, 32)
COLOR_TEXTO: tuple = (230, 225, 240)
COLOR_BOTON: tuple = (52, 48, 86)
COLOR_BOTON_SOBRE: tuple = (92, 80, 150)
COLOR_ACENTO: tuple = (220, 170, 60)
COLOR_TENUE: tuple = (140, 132, 165)
COLOR_PANEL: tuple = (30, 27, 52)
COLOR_FINAL_BUENO: tuple = (120, 200, 140)
COLOR_FINAL_MALO: tuple = (210, 80, 80)

# Tamaños de letra
TAMANO_TITULO: int = 72
TAMANO_TEXTO: int = 28
TAMANO_OPCION: int = 24
TAMANO_PEQUENO: int = 20

# Animaciones
LETRAS_POR_SEGUNDO: int = 45      # velocidad de la máquina de escribir
DURACION_DESVANECER: float = 0.4  # segundos que dura el fundido entre nodos
DURACION_MENSAJE: float = 2.0     # segundos que se ve un aviso ("Partida guardada")

# Límites para que todo quepa en pantalla (los revisa el verificador)
MAXIMO_OPCIONES: int = 4
MAXIMO_LETRAS_TEXTO: int = 600
