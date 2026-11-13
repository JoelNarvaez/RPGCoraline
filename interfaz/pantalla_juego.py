"""Pantalla principal del juego: imagen de fondo, texto del nodo y opciones.

Controles:
- Clic en una opción, o teclas 1 a 4: elegir.
- Clic o Espacio mientras se escribe el texto: mostrarlo completo.
- G: guardar partida.  I: inventario.  Esc: volver al menú.

Si el nodo tiene "minijuego", en lugar de opciones sale un solo botón
"Aceptar el reto" que abre la pantalla de minijuego.

Responsable: Persona A
"""

import pygame

import config
from juego import motor
from juego import partida
from interfaz import dibujo
from interfaz import animaciones
from interfaz import pantalla_minijuego

# Zona donde va el texto del nodo
MARGEN: int = 80
ANCHO_TEXTO: int = config.ANCHO - 2 * MARGEN
Y_TEXTO: int = 70

# Botones de las opciones
ALTO_BOTON: int = 54
SEPARACION: int = 12
Y_FIN_BOTONES: int = config.ALTO - 70

TECLAS_NUMERO: list = [pygame.K_1, pygame.K_2, pygame.K_3, pygame.K_4]


def preparar_nodo(contexto: dict) -> None:
    """Se llama cada vez que se entra a un nodo (nueva partida, cargar o elegir).

    Parte el texto en renglones y calcula las opciones disponibles una sola vez,
    en lugar de hacerlo 60 veces por segundo dentro de dibujar.
    """
    nodo: dict = motor.nodo_actual(contexto["estado"], contexto["nodos"])
    fuente: pygame.font.Font = contexto["fuentes"]["texto"]
    lineas: list = dibujo.dividir_en_lineas(nodo["texto"], fuente, ANCHO_TEXTO)
    contexto["lineas"] = lineas
    contexto["total_letras"] = dibujo.contar_letras(lineas)
    if motor.es_minijuego(nodo):
        # Un solo botón que abre el minijuego
        contexto["opciones"] = [{"texto": "Aceptar el reto", "abre_minijuego": True}]
    else:
        contexto["opciones"] = motor.opciones_disponibles(nodo, contexto["estado"])
    animaciones.reiniciar(contexto)


def rectangulos_opciones(cantidad: int) -> list:
    """Regresa un pygame.Rect por opción, apilados en la parte de abajo.

    Se usa en dibujar (para pintar los botones) y en manejar_evento
    (para saber a cuál le dieron clic), así los dos usan las mismas posiciones.
    """
    rectangulos: list = []
    alto_total: int = cantidad * ALTO_BOTON + (cantidad - 1) * SEPARACION
    y: int = Y_FIN_BOTONES - alto_total
    for i in range(cantidad):
        rectangulos.append(pygame.Rect(MARGEN, y, ANCHO_TEXTO, ALTO_BOTON))
        y = y + ALTO_BOTON + SEPARACION
    return rectangulos


def elegir(contexto: dict, numero: int) -> str:
    """Elige la opción `numero` (empieza en 0). Regresa "final" si se llegó a un final."""
    opciones: list = contexto["opciones"]
    if numero < 0 or numero >= len(opciones):
        return ""
    if "abre_minijuego" in opciones[numero]:
        pantalla_minijuego.iniciar(contexto)
        return "minijuego"
    motor.elegir_opcion(opciones[numero], contexto["estado"])
    preparar_nodo(contexto)
    nodo: dict = motor.nodo_actual(contexto["estado"], contexto["nodos"])
    if motor.es_final(nodo):
        return "final"
    return ""


def manejar_evento(evento: pygame.event.Event, contexto: dict) -> str:
    """Regresa el nombre de la siguiente pantalla, o "" para quedarse aquí."""
    terminado: bool = animaciones.texto_terminado(contexto, contexto["total_letras"])

    if evento.type == pygame.MOUSEBUTTONDOWN and evento.button == 1:
        # El primer clic solo completa el texto, para no elegir una opción sin querer
        if not terminado:
            animaciones.completar_texto(contexto, contexto["total_letras"])
            return ""
        rectangulos: list = rectangulos_opciones(len(contexto["opciones"]))
        for i in range(len(rectangulos)):
            if rectangulos[i].collidepoint(evento.pos):
                return elegir(contexto, i)

    elif evento.type == pygame.KEYDOWN:
        if evento.key == pygame.K_ESCAPE:
            return "menu"
        if evento.key == pygame.K_i:
            return "inventario"
        if evento.key == pygame.K_g:
            partida.guardar_partida(contexto["estado"], config.RUTA_PARTIDA)
            animaciones.mostrar_mensaje(contexto, "Partida guardada")
            return ""
        if not terminado:
            if evento.key == pygame.K_SPACE:
                animaciones.completar_texto(contexto, contexto["total_letras"])
            return ""
        if evento.key in TECLAS_NUMERO:
            return elegir(contexto, TECLAS_NUMERO.index(evento.key))

    return ""


def actualizar(contexto: dict, dt: float) -> None:
    animaciones.avanzar_maquina_escribir(contexto, dt, contexto["total_letras"])
    animaciones.avanzar_desvanecer(contexto, dt)


def dibujar_fondo(ventana: pygame.Surface, nodo: dict) -> None:
    """Imagen del nodo con una capa oscura encima para que el texto se lea."""
    if "imagen" not in nodo:
        return
    imagen: pygame.Surface = dibujo.cargar_imagen(nodo["imagen"])
    if imagen is not None:
        ventana.blit(imagen, (0, 0))
        dibujo.dibujar_capa(ventana, config.COLOR_FONDO, 110)


def dibujar(ventana: pygame.Surface, contexto: dict) -> None:
    nodo: dict = motor.nodo_actual(contexto["estado"], contexto["nodos"])
    fuentes: dict = contexto["fuentes"]

    dibujar_fondo(ventana, nodo)

    # Texto con máquina de escribir
    visibles: list = dibujo.recortar_lineas(contexto["lineas"], int(contexto["letras_visibles"]))
    dibujo.dibujar_parrafo(ventana, visibles, fuentes["texto"], config.COLOR_TEXTO, MARGEN, Y_TEXTO)

    # Opciones: solo cuando el texto terminó de escribirse
    if animaciones.texto_terminado(contexto, contexto["total_letras"]):
        opciones: list = contexto["opciones"]
        rectangulos: list = rectangulos_opciones(len(opciones))
        posicion_mouse: tuple = pygame.mouse.get_pos()
        for i in range(len(opciones)):
            texto: str = str(i + 1) + ". " + opciones[i]["texto"]
            encima: bool = rectangulos[i].collidepoint(posicion_mouse)
            dibujo.dibujar_boton(ventana, rectangulos[i], texto, fuentes["opcion"], encima, False)
        if len(opciones) == 0:
            dibujo.dibujar_texto(ventana, "(Este nodo no tiene opciones: revisar la historia)",
                                 fuentes["pequena"], config.COLOR_FINAL_MALO, MARGEN, Y_FIN_BOTONES - 30)

    # Ayuda de controles
    dibujo.dibujar_texto(ventana, "G guardar     I inventario     Esc menú",
                         fuentes["pequena"], config.COLOR_TENUE, MARGEN, config.ALTO - 40)

    animaciones.dibujar_desvanecer(ventana, contexto["transparencia"])
