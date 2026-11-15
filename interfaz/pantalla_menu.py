"""Menu principal del juego."""

import os
import math
import random
import pygame

import config
from juego import motor
from juego import partida
from interfaz import dibujo
from interfaz import animaciones
from interfaz import pantalla_juego


OPCIONES_MENU: list = ["NUEVA PARTIDA", "CONTINUAR", "SALIR"]

TECLAS_NUMERO: list = [
    pygame.K_1,
    pygame.K_2,
    pygame.K_3
]

ANCHO_BOTON: int = int(config.ANCHO * 0.65)
ALTO_BOTON: int = 86
SEPARACION: int = 14
Y_PRIMER_BOTON: int = 330

def calcular_opacidad(tiempo, inicio, duracion=0.8):
    # CALCULAMOS LA APARICION SUAVE DE CADA ELEMENTO
    progreso = (tiempo - inicio) / duracion

    progreso = max(0, min(progreso, 1))

    return int(progreso * 255)

def crear_particulas(contexto):
    # CREAMOS LAS PARTICULAS DEL FONDO
    if "particulas_menu" not in contexto:

        particulas = []

        for i in range(45):
            particulas.append({
                "x": random.randint(0, config.ANCHO),
                "y": random.randint(0, config.ALTO),
                "velocidad": random.uniform(3, 8),
                "tamano": random.randint(2, 3),
                "fase": random.uniform(0, 6.28),
                "brillo": random.randint(120, 190),
                "color": random.choice([
                    (100, 160, 210),
                    (235, 200, 110)
                ])
            })

        contexto["particulas_menu"] = particulas

def actualizar_particulas(contexto, dt):
    # MOVEMOS LAS PARTICULAS LENTAMENTE
    for particula in contexto["particulas_menu"]:

        particula["y"] -= particula["velocidad"] * dt

        particula["x"] += math.sin(
            contexto["tiempo_menu"] * 0.4 + particula["fase"]
        ) * 3 * dt

        if particula["y"] < 0:
            particula["y"] = config.ALTO + 5
            particula["x"] = random.randint(0, config.ANCHO)


def dibujar_particulas(ventana, contexto):
    # CREAMOS UNA CAPA TRANSPARENTE
    capa = pygame.Surface(
        (config.ANCHO, config.ALTO),
        pygame.SRCALPHA
    )

    tiempo = contexto["tiempo_menu"]

    for particula in contexto["particulas_menu"]:

        # HACEMOS QUE EL BRILLO CAMBIE SUAVEMENTE
        brillo = math.sin(
            tiempo * 1.5 + particula["fase"]
        )

        transparencia = int(
            particula["brillo"] + brillo * 35
        )

        transparencia = max(80, min(220, transparencia))

        x = int(particula["x"])
        y = int(particula["y"])
        tamano = particula["tamano"]

        # PEQUENO RESPLANDOR
        pygame.draw.circle(
            capa,
            (*particula["color"], 35),
            (x, y),
            tamano + 4
        )

        # PARTICULA PRINCIPAL
        pygame.draw.circle(
            capa,
            (*particula["color"], transparencia),
            (x, y),
            tamano
        )

    ventana.blit(capa, (0, 0))

def rectangulos_menu() -> list:
    # CREAMOS LOS RECTANGULOS DE LOS BOTONES
    rectangulos: list = []

    x: int = 24
    y: int = Y_PRIMER_BOTON

    for i in range(len(OPCIONES_MENU)):

        rectangulos.append(
            pygame.Rect(
                x,
                y,
                ANCHO_BOTON,
                ALTO_BOTON
            )
        )

        y = y + ALTO_BOTON + SEPARACION

    return rectangulos


def dibujar_boton_decorativo(ventana, x, y, radio, color):
    # DIBUJAMOS EL CIRCULO EXTERIOR
    pygame.draw.circle(
        ventana,
        color,
        (x, y),
        radio,
        2
    )

    # DIBUJAMOS EL CENTRO DEL CIRCULO
    pygame.draw.circle(
        ventana,
        color,
        (x, y),
        radio - 4
    )


def dibujar_imagen_redondeada(ventana, imagen, posicion, radio=22):
    # OBTENEMOS EL TAMANO DE LA IMAGEN
    ancho, alto = imagen.get_size()

    # CREAMOS UNA CAPA PARA REDONDEAR LAS ESQUINAS
    mascara = pygame.Surface(
        (ancho, alto),
        pygame.SRCALPHA
    )

    pygame.draw.rect(
        mascara,
        (255, 255, 255, 255),
        (0, 0, ancho, alto),
        border_radius=radio
    )

    # APLICAMOS LA MASCARA
    imagen_redondeada = imagen.copy()

    imagen_redondeada.blit(
        mascara,
        (0, 0),
        special_flags=pygame.BLEND_RGBA_MULT
    )

    # DIBUJAMOS LA SOMBRA
    sombra = pygame.Surface(
        (ancho + 12, alto + 12),
        pygame.SRCALPHA
    )

    pygame.draw.rect(
        sombra,
        (0, 0, 0, 100),
        (5, 5, ancho, alto),
        border_radius=radio
    )

    ventana.blit(
        sombra,
        (posicion[0] - 5, posicion[1] - 2)
    )

    # MOSTRAMOS LA IMAGEN
    ventana.blit(
        imagen_redondeada,
        posicion
    )

    # AGREGAMOS UN BORDE DORADO
    pygame.draw.rect(
        ventana,
        (155, 127, 70),
        (posicion[0], posicion[1], ancho, alto),
        1,
        border_radius=radio
    )


def entrar_a_partida(contexto: dict) -> str:
    pantalla_juego.preparar_nodo(contexto)

    nodo: dict = motor.nodo_actual(
        contexto["estado"],
        contexto["nodos"]
    )

    if motor.es_final(nodo):
        return "final"

    return "juego"


def continuar(contexto: dict) -> str:

    if contexto["estado"] is not None:
        return entrar_a_partida(contexto)

    estado: dict = partida.cargar_partida(
        config.RUTA_PARTIDA
    )

    if estado is None:
        animaciones.mostrar_mensaje(
            contexto,
            "No hay partida guardada"
        )
        return ""

    if estado["nodo_actual"] not in contexto["nodos"]:
        animaciones.mostrar_mensaje(
            contexto,
            "La partida guardada ya no coincide con la historia"
        )
        return ""

    contexto["estado"] = estado

    return entrar_a_partida(contexto)


def ejecutar(numero: int, contexto: dict) -> str:

    if numero == 0:
        contexto["estado"] = partida.nuevo_estado()
        return entrar_a_partida(contexto)

    if numero == 1:
        return continuar(contexto)

    if numero == 2:
        return "salir"

    return ""


def manejar_evento(
    evento: pygame.event.Event,
    contexto: dict
) -> str:

    # DETECTAMOS LOS CLICS DEL MOUSE
    if evento.type == pygame.MOUSEBUTTONDOWN and evento.button == 1:

        rectangulos: list = rectangulos_menu()

        for i in range(len(rectangulos)):

            if rectangulos[i].collidepoint(evento.pos):
                return ejecutar(i, contexto)

    # DETECTAMOS LAS TECLAS NUMERICAS
    elif evento.type == pygame.KEYDOWN:

        if evento.key in TECLAS_NUMERO:

            numero = TECLAS_NUMERO.index(evento.key)

            return ejecutar(numero, contexto)

    return ""


def actualizar(contexto: dict, dt: float) -> None:

    contexto["tiempo_menu"] += dt

    # CREAMOS Y ACTUALIZAMOS LAS PARTICULAS
    crear_particulas(contexto)
    actualizar_particulas(contexto, dt)


def dibujar(ventana: pygame.Surface, contexto: dict) -> None:

    fuentes: dict = contexto["fuentes"]
    centro: int = config.ANCHO // 2
    tiempo: float = contexto["tiempo_menu"]
    # CALCULAMOS LA APARICION DEL MENU
    opacidad_general = calcular_opacidad(tiempo, 0, 1.2)

    # FONDO AZUL OSCURO
    ventana.fill((8, 13, 26))

    # MOSTRAMOS LAS PARTICULAS DEL AMBIENTE
    if "particulas_menu" in contexto:
        dibujar_particulas(ventana, contexto)

    # TITULO PRINCIPAL
    brillo = (math.sin(tiempo * 1.5) + 1) / 2

    color_titulo = (
        int(225 + brillo * 20),
        int(210 + brillo * 15),
        int(165 + brillo * 20)
    )

    titulo = fuentes["titulo_intro"].render(
        "Coraline",
        True,
        color_titulo
    )

    # AJUSTAMOS EL TAMANO DEL TITULO
    alto_titulo = 55

    escala = alto_titulo / titulo.get_height()

    nuevo_ancho = int(titulo.get_width() * escala)

    titulo = pygame.transform.smoothscale(
        titulo,
        (nuevo_ancho, alto_titulo)
    )

    ventana.blit(titulo, (24, 65))

    # SUBTITULO
    subtitulo = fuentes["pequena"].render(
        "Y LA PUERTA SECRETA",
        True,
        (195, 175, 115)
    )

    ventana.blit(
        subtitulo,
        (24, 135)
    )

     # FRASE MISTERIOSA DEL JUEGO
    dibujo.dibujar_texto_centrado(
        ventana,
        "NO TODAS LAS PUERTAS DEBERIAN ABRIRSE...",
        fuentes["pequena"],
        (145, 151, 170),
        centro,
        235
    )

    # CARGAMOS LA IMAGEN DE CORALINE
    if "imagen_menu" not in contexto:

        ruta = os.path.join(
            config.RUTA_IMAGENES,
            "coraline_menu.jpg"
        )

        if os.path.exists(ruta):
            imagen = pygame.image.load(ruta).convert_alpha()
            contexto["imagen_menu"] = imagen
        else:
            contexto["imagen_menu"] = None

    imagen_coraline = contexto["imagen_menu"]

    # MOSTRAMOS LA IMAGEN
    if imagen_coraline is not None:

        ancho_original, alto_original = imagen_coraline.get_size()

        # EVITAMOS DEFORMAR LA IMAGEN
        escala = min(
            330 / ancho_original,
            500 / alto_original
        )

        nuevo_ancho = int(ancho_original * escala)
        nuevo_alto = int(alto_original * escala)

        imagen_coraline = pygame.transform.smoothscale(
            imagen_coraline,
            (nuevo_ancho, nuevo_alto)
        )

        imagen_x = config.ANCHO - nuevo_ancho - 24
        imagen_y = 15

        # MOSTRAMOS A CORALINE CON ESQUINAS REDONDEADAS
        dibujar_imagen_redondeada(
            ventana,
            imagen_coraline,
            (imagen_x, imagen_y),
            22
        )

    # LINEA DIVISORIA
    pygame.draw.line(
        ventana,
        (145, 119, 65),
        (24, 300),
        (config.ANCHO - 24, 300),
        1
    )

    # DIBUJAMOS LOS BOTONES
    rectangulos: list = rectangulos_menu()

    posicion_mouse = pygame.mouse.get_pos()

        # DIBUJAMOS LOS BOTONES CON APARICION ESCALONADA
    rectangulos: list = rectangulos_menu()
    posicion_mouse = pygame.mouse.get_pos()

    for i in range(len(OPCIONES_MENU)):

        rect = rectangulos[i]

        # CADA BOTON APARECE UN POQUITO DESPUES DEL ANTERIOR
        opacidad_boton = calcular_opacidad(
            tiempo,
            1.0 + i * 0.3,
            0.6
        )

        # SI TODAVIA NO APARECE, NO LO DIBUJAMOS
        if opacidad_boton <= 0:
            continue

        encima = rect.collidepoint(posicion_mouse)

        # COLORES DEL BOTON
        if encima:
            color_fondo = (65, 57, 38, 210)
            color_borde = (245, 210, 115)
            color_boton = (245, 205, 100)
            color_texto = (255, 235, 185)
        else:
            color_fondo = (35, 39, 54, 170)
            color_borde = (145, 119, 65)
            color_boton = (215, 185, 105)
            color_texto = (225, 220, 205)

        # CREAMOS UNA CAPA PARA TODO EL BOTON
        capa_boton = pygame.Surface(
            (rect.width, rect.height),
            pygame.SRCALPHA
        )

        # FONDO DEL BOTON
        pygame.draw.rect(
            capa_boton,
            color_fondo,
            (0, 0, rect.width, rect.height),
            border_radius=16
        )

        # BORDE DEL BOTON
        pygame.draw.rect(
            capa_boton,
            (*color_borde, 230),
            (0, 0, rect.width, rect.height),
            1,
            border_radius=16
        )

        # DIBUJAMOS EL ICONO CIRCULAR
        dibujar_boton_decorativo(
            capa_boton,
            34,
            rect.height // 2,
            10,
            color_boton
        )

        # TEXTO DEL BOTON
        texto = fuentes["opcion"].render(
            OPCIONES_MENU[i],
            True,
            color_texto
        )

        capa_boton.blit(
            texto,
            (
                62,
                rect.height // 2 - texto.get_height() // 2
            )
        )

        # APLICAMOS LA TRANSPARENCIA
        capa_boton.set_alpha(opacidad_boton)

        # MOSTRAMOS EL BOTON
        ventana.blit(
            capa_boton,
            rect.topleft
        )

     # EFECTO DE APARICION DEL MENU
    if opacidad_general < 255:

        capa_oscura = pygame.Surface(
            (config.ANCHO, config.ALTO)
        )

        capa_oscura.fill((0, 0, 0))
        capa_oscura.set_alpha(255 - opacidad_general)

        ventana.blit(capa_oscura, (0, 0))

    # INDICACIONES DEL TECLADO
    dibujo.dibujar_texto_centrado(
        ventana,
        "1  NUEVA PARTIDA · 2  CONTINUAR · 3  SALIR",
        fuentes["pequena"],
        (165, 160, 150),
        centro,
        config.ALTO - 25
    )