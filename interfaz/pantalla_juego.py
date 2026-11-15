"""PANTALLA PRINCIPAL DEL JUEGO CORALINE."""

import os
import pygame

import config
from juego import motor
from juego import partida
from interfaz import dibujo
from interfaz import animaciones
from interfaz import pantalla_minijuego


# --------------------------------------------------
# POSICIONES Y TAMANOS
# --------------------------------------------------

X_PERSONAJE = 35
Y_PERSONAJE = 235
ANCHO_PERSONAJE = 245
ALTO_PERSONAJE = 425

X_CONTENIDO = 320
ANCHO_CONTENIDO = 920

# PANEL DE HISTORIA
X_PANEL = 320
Y_PANEL_HISTORIA = 25
ANCHO_PANEL = 920
ALTO_PANEL_HISTORIA = 325

# MEDIDAS INTERNAS DE LA HISTORIA
X_DIARIO = X_PANEL
Y_DIARIO = 125
ANCHO_DIARIO = ANCHO_PANEL
ALTO_DIARIO = 250
MARGEN_TEXTO = 32

# PANEL DE DECISIONES
Y_PANEL_OPCIONES = 365
ALTO_PANEL_OPCIONES = 285

# POSICIONES DE LAS OPCIONES
X_OPCIONES = X_PANEL + 25
ANCHO_OPCIONES = ANCHO_PANEL - 50

# CONTENEDOR PRINCIPAL
X_PANEL = 320
Y_PANEL = 25
ANCHO_PANEL = 920
ALTO_PANEL = 530

# ENCABEZADO
Y_ENCABEZADO = 43

# NARRACION
Y_DIARIO = 125
ALTO_DIARIO = 250

# OPCIONES
Y_TITULO_OPCIONES = 380
Y_OPCIONES = 415
ALTO_BOTON = 44
SEPARACION = 8

# CONTROLES
Y_CONTROLES = 683

TECLAS_NUMERO = [
    pygame.K_1,
    pygame.K_2,
    pygame.K_3,
    pygame.K_4
]

# MEDIDAS DEL DISENO DE EXPLORACION

X_EXPLORACION = 45
Y_EXPLORACION = 55

ANCHO_HISTORIA_EXPLORACION = 650
ALTO_HISTORIA_EXPLORACION = 245

Y_OPCIONES_EXPLORACION = 440
ALTO_BOTON_EXPLORACION = 48
SEPARACION_EXPLORACION = 9

# MEDIDAS INTERNAS DEL DISENO DE EXPLORACION

X_TEXTO_EXPLORACION = X_EXPLORACION + 30
Y_TEXTO_EXPLORACION = Y_EXPLORACION + 130

Y_TITULO_OPCIONES_EXPLORACION = 445
X_OPCIONES_EXPLORACION = X_EXPLORACION + 20

ANCHO_OPCIONES_EXPLORACION = ANCHO_HISTORIA_EXPLORACION - 40

ALTO_BOTON_EXPLORACION = 40
Y_BOTONES_EXPLORACION = 480

# --------------------------------------------------
# COLORES
# --------------------------------------------------

COLOR_TEXTO = (48, 48, 54)
COLOR_TEXTO_SECUNDARIO = (105, 101, 105)

COLOR_PANEL = (244, 239, 231, 240)
COLOR_PANEL_BOTON = (226, 222, 216)
COLOR_PANEL_SELECCION = (231, 194, 204)

COLOR_BORDE = (207, 197, 187)
COLOR_ACENTO = (177, 103, 124)

COLOR_FONDO_CONTROLES = (35, 39, 50, 235)

# COLORES DEL DISENO DE EXPLORACION

COLOR_PANEL_EXPLORACION = (25, 30, 43, 225)
COLOR_BORDE_EXPLORACION = (155, 135, 143)
COLOR_TEXTO_EXPLORACION = (244, 237, 232)
COLOR_TEXTO_SECUNDARIO_EXPLORACION = (205, 194, 194)
COLOR_BOTON_EXPLORACION = (38, 46, 62, 235)
COLOR_BOTON_SELECCION_EXPLORACION = (115, 69, 88, 245)
COLOR_ACENTO_EXPLORACION = (221, 157, 174)

FONDO_CACHE = {}

# --------------------------------------------------
# PREPARAR HISTORIA
# --------------------------------------------------

def preparar_nodo(contexto: dict) -> None:

    """PREPARAMOS EL TEXTO Y LAS OPCIONES DEL NODO."""

    nodo = motor.nodo_actual(
        contexto["estado"],
        contexto["nodos"]
    )

    fuente = contexto["fuentes"]["narracion"]

    if nodo.get("diseno") == "exploracion":

        ancho_texto = ANCHO_HISTORIA_EXPLORACION - 60

    else:

        ancho_texto = ANCHO_DIARIO - MARGEN_TEXTO * 2

    lineas = dibujo.dividir_en_lineas(
        nodo["texto"],
        fuente,
        ancho_texto
    )

    contexto["lineas"] = lineas

    contexto["total_letras"] = dibujo.contar_letras(
        lineas
    )

    if motor.es_minijuego(nodo):

        contexto["opciones"] = [
            {
                "texto": "Aceptar el reto",
                "abre_minijuego": True
            }
        ]

    else:

        contexto["opciones"] = motor.opciones_disponibles(
            nodo,
            contexto["estado"]
        )

    animaciones.reiniciar(contexto)


def rectangulos_opciones(cantidad: int) -> list:

    """CREAMOS LAS AREAS CLICABLES DE LAS OPCIONES."""

    rectangulos = []

    y = Y_OPCIONES

    for i in range(cantidad):

        rect = pygame.Rect(
            X_OPCIONES,
            y,
            ANCHO_OPCIONES,
            ALTO_BOTON
        )

        rectangulos.append(rect)

        y += ALTO_BOTON + SEPARACION

    return rectangulos

def rectangulos_opciones_exploracion(cantidad: int) -> list:

    """CREAMOS LAS AREAS CLICABLES DEL DISENO DE EXPLORACION."""

    rectangulos = []

    y = Y_BOTONES_EXPLORACION

    for i in range(cantidad):

        rect = pygame.Rect(
            X_OPCIONES_EXPLORACION,
            y,
            ANCHO_OPCIONES_EXPLORACION,
            ALTO_BOTON_EXPLORACION
        )

        rectangulos.append(rect)

        y += ALTO_BOTON_EXPLORACION + SEPARACION_EXPLORACION

    return rectangulos

# --------------------------------------------------
# SELECCIONAR OPCIONES
# --------------------------------------------------

def elegir(contexto: dict, numero: int) -> str:

    """PROCESAMOS LA OPCION ELEGIDA."""

    opciones = contexto["opciones"]

    if numero < 0 or numero >= len(opciones):
        return ""

    if "abre_minijuego" in opciones[numero]:

        pantalla_minijuego.iniciar(contexto)

        return "minijuego"

    motor.elegir_opcion(
        opciones[numero],
        contexto["estado"]
    )

    preparar_nodo(contexto)

    nodo = motor.nodo_actual(
        contexto["estado"],
        contexto["nodos"]
    )

    if motor.es_final(nodo):
        return "final"

    return ""


def manejar_evento(
    evento: pygame.event.Event,
    contexto: dict
) -> str:

    """RECIBIMOS LAS ACCIONES DEL JUGADOR."""

    terminado = animaciones.texto_terminado(
        contexto,
        contexto["total_letras"]
    )

    if evento.type == pygame.MOUSEBUTTONDOWN and evento.button == 1:

        if not terminado:

            animaciones.completar_texto(
                contexto,
                contexto["total_letras"]
            )

            return ""

        nodo = motor.nodo_actual(
    contexto["estado"],
            contexto["nodos"]
        )

        if nodo.get("diseno") == "exploracion":

            rectangulos = rectangulos_opciones_exploracion(
                len(contexto["opciones"])
            )

        else:

            rectangulos = rectangulos_opciones(
                len(contexto["opciones"])
            )

        for i in range(len(rectangulos)):

            if rectangulos[i].collidepoint(evento.pos):
                return elegir(contexto, i)

    elif evento.type == pygame.KEYDOWN:

        if evento.key == pygame.K_ESCAPE:
            return "menu"

        if evento.key == pygame.K_i:
            return "inventario"

        if evento.key == pygame.K_g:

            partida.guardar_partida(
                contexto["estado"],
                config.RUTA_PARTIDA
            )

            animaciones.mostrar_mensaje(
                contexto,
                "Partida guardada"
            )

            return ""

        if not terminado:

            if evento.key == pygame.K_SPACE:

                animaciones.completar_texto(
                    contexto,
                    contexto["total_letras"]
                )

            return ""

        if evento.key in TECLAS_NUMERO:

            numero = TECLAS_NUMERO.index(evento.key)

            return elegir(contexto, numero)

    return ""


def actualizar(contexto: dict, dt: float) -> None:

    """ACTUALIZAMOS LAS ANIMACIONES."""

    animaciones.avanzar_maquina_escribir(
        contexto,
        dt,
        contexto["total_letras"]
    )

    animaciones.avanzar_desvanecer(
        contexto,
        dt
    )


# --------------------------------------------------
# FONDO
# --------------------------------------------------

def crear_fondo(nombre_imagen: str) -> pygame.Surface:

    """CARGAMOS Y AJUSTAMOS LA IMAGEN DEL ESCENARIO."""

    ruta = os.path.join(
        config.RUTA_IMAGENES,
        nombre_imagen
    )

    imagen = pygame.image.load(ruta).convert()

    ancho_original, alto_original = imagen.get_size()

    escala = max(
        config.ANCHO / ancho_original,
        config.ALTO / alto_original
    )

    nuevo_ancho = int(ancho_original * escala)
    nuevo_alto = int(alto_original * escala)

    imagen = pygame.transform.scale(
        imagen,
        (nuevo_ancho, nuevo_alto)
    )

    x_recorte = (nuevo_ancho - config.ANCHO) // 2
    y_recorte = (nuevo_alto - config.ALTO) // 2

    imagen = imagen.subsurface(
        (
            x_recorte,
            y_recorte,
            config.ANCHO,
            config.ALTO
        )
    ).copy()

    return imagen


def dibujar_fondo(
    ventana: pygame.Surface,
    nodo: dict
) -> None:

    """MOSTRAMOS EL FONDO CORRESPONDIENTE A CADA ESCENA."""

    global FONDO_CACHE

    nombre_imagen = nodo.get(
        "imagen",
        "casarosa.webp"
    )

    if nombre_imagen not in FONDO_CACHE:

        FONDO_CACHE[nombre_imagen] = crear_fondo(
            nombre_imagen
        )

    ventana.blit(
        FONDO_CACHE[nombre_imagen],
        (0, 0)
    )


def dibujar_contenedor(
    ventana: pygame.Surface,
    cantidad_opciones: int
) -> None:

    """DIBUJAMOS LOS PANELES DE HISTORIA Y DECISIONES."""

    panel_historia = pygame.Rect(
        X_PANEL,
        Y_PANEL_HISTORIA,
        ANCHO_PANEL,
        ALTO_PANEL_HISTORIA
    )

    # CALCULAMOS LA ALTURA SEGUN LAS OPCIONES
    alto_opciones = (
        Y_OPCIONES
        + (cantidad_opciones - 1) * (ALTO_BOTON + SEPARACION)
        + ALTO_BOTON
        + 20
        - Y_PANEL_OPCIONES
    )

    panel_opciones = pygame.Rect(
        X_PANEL,
        Y_PANEL_OPCIONES,
        ANCHO_PANEL,
        alto_opciones
    )

    for rect in [panel_historia, panel_opciones]:

        capa = pygame.Surface(
            (rect.width, rect.height),
            pygame.SRCALPHA
        )

        pygame.draw.rect(
            capa,
            COLOR_PANEL,
            capa.get_rect(),
            border_radius=12
        )

        ventana.blit(
            capa,
            rect.topleft
        )

        pygame.draw.rect(
            ventana,
            COLOR_BORDE,
            rect,
            1,
            border_radius=12
        )

# --------------------------------------------------
# PERSONAJE
# --------------------------------------------------

def preparar_personaje(contexto: dict) -> None:

    """CARGAMOS Y ESCALAMOS A CORALINE."""

    ruta = os.path.join(
        config.RUTA_IMAGENES,
        "coraline_pixel_retrato.png"
    )

    if not os.path.exists(ruta):

        contexto["personaje_listo"] = None

        return

    imagen = pygame.image.load(ruta).convert_alpha()

    ancho_original, alto_original = imagen.get_size()

    escala = min(
        ANCHO_PERSONAJE / ancho_original,
        ALTO_PERSONAJE / alto_original
    )

    nuevo_ancho = int(ancho_original * escala)
    nuevo_alto = int(alto_original * escala)

    imagen = pygame.transform.scale(
        imagen,
        (nuevo_ancho, nuevo_alto)
    )

    contexto["personaje_listo"] = imagen


def dibujar_personaje(
    ventana: pygame.Surface,
    contexto: dict
) -> None:

    """MOSTRAMOS A CORALINE EN EL LADO IZQUIERDO."""

    if "personaje_listo" not in contexto:
        preparar_personaje(contexto)

    imagen = contexto["personaje_listo"]

    if imagen is None:
        return

    ancho, alto = imagen.get_size()

    x = X_PERSONAJE + (ANCHO_PERSONAJE - ancho) // 2

    y = Y_PERSONAJE + (ALTO_PERSONAJE - alto)

    # SOMBRA SUAVE DEBAJO DEL PERSONAJE
    sombra = pygame.Surface(
        (ANCHO_PERSONAJE, 22),
        pygame.SRCALPHA
    )

    pygame.draw.ellipse(
        sombra,
        (10, 14, 22, 100),
        (10, 3, ANCHO_PERSONAJE - 20, 15)
    )

    ventana.blit(
        sombra,
        (X_PERSONAJE, Y_PERSONAJE + ALTO_PERSONAJE - 5)
    )

    ventana.blit(
        imagen,
        (x, y)
    )


# --------------------------------------------------
# ENCABEZADO
# --------------------------------------------------

def dibujar_encabezado(
    ventana: pygame.Surface,
    fuentes: dict
) -> None:

    """MOSTRAMOS EL NOMBRE DEL ESCENARIO."""

    titulo = fuentes["titulo_palace"].render(
    "Pink Palace",
    True,
    COLOR_ACENTO
    )

    # DETALLE DECORATIVO DEL TITULO
    pygame.draw.line(
        ventana,
        COLOR_ACENTO,
        (X_CONTENIDO + 30, 112),
        (X_CONTENIDO + 125, 112),
        3
    )

    subtitulo = fuentes["pequena"].render(
        "EL JARDIN  |  DIA 01",
        True,
        COLOR_TEXTO_SECUNDARIO
    )

    ventana.blit(
        titulo,
        (X_CONTENIDO + 30, 43)
    )

    ventana.blit(
        subtitulo,
        (X_CONTENIDO + 30, 94)
    )

    pygame.draw.line(
        ventana,
        COLOR_BORDE,
        (X_CONTENIDO + 25, 112),
        (X_CONTENIDO + ANCHO_CONTENIDO - 25, 112),
        1
    )

# --------------------------------------------------
# NARRACION
# --------------------------------------------------

def dibujar_diario(
    ventana: pygame.Surface,
    contexto: dict,
    fuentes: dict
) -> None:

    """MOSTRAMOS EL TEXTO DE LA HISTORIA."""

    titulo = fuentes["pequena"].render(
        "HISTORIA",
        True,
        COLOR_ACENTO
    )

    ventana.blit(
        titulo,
        (X_DIARIO + MARGEN_TEXTO, Y_DIARIO)
    )

    visibles = dibujo.recortar_lineas(
        contexto["lineas"],
        int(contexto["letras_visibles"])
    )

    dibujo.dibujar_parrafo(
    ventana,
    visibles,
    fuentes["narracion"],
    COLOR_TEXTO,
    X_DIARIO + MARGEN_TEXTO,
    Y_DIARIO + 42,
    espaciado=5
    )

    terminado = animaciones.texto_terminado(
        contexto,
        contexto["total_letras"]
    )

    if not terminado:

        pista = fuentes["pequena"].render(
            "ESPACIO PARA CONTINUAR",
            True,
            COLOR_TEXTO_SECUNDARIO
        )

        ventana.blit(
            pista,
            (
                X_DIARIO + ANCHO_DIARIO - pista.get_width() - 30,
                Y_DIARIO + ALTO_DIARIO - pista.get_height() - 12
            )
        )

# --------------------------------------------------
# DECISIONES
# --------------------------------------------------

def dibujar_opcion(
    ventana: pygame.Surface,
    rect: pygame.Rect,
    indice: int,
    texto: str,
    encima: bool,
    fuentes: dict
) -> None:

    """DIBUJAMOS UNA OPCION."""

    color = (
        COLOR_PANEL_SELECCION
        if encima
        else COLOR_PANEL_BOTON
    )

    pygame.draw.rect(
        ventana,
        color,
        rect,
        border_radius=6
    )

    if encima:

        pygame.draw.rect(
            ventana,
            COLOR_ACENTO,
            (rect.x, rect.y + 5, 4, rect.height - 10)
        )

    numero = fuentes["pequena"].render(
        str(indice + 1),
        True,
        COLOR_ACENTO
    )

    ventana.blit(
        numero,
        (
            rect.x + 18,
            rect.centery - numero.get_height() // 2
        )
    )

    texto_opcion = fuentes["pequena"].render(
        texto,
        True,
        COLOR_TEXTO
    )

    ventana.blit(
        texto_opcion,
        (
            rect.x + 55,
            rect.centery - texto_opcion.get_height() // 2
        )
    )


def dibujar_opciones(
    ventana: pygame.Surface,
    contexto: dict,
    fuentes: dict
) -> None:

    """MOSTRAMOS LAS DECISIONES DEL JUGADOR."""

    opciones = contexto["opciones"]

    rectangulos = rectangulos_opciones(
        len(opciones)
    )

    posicion_mouse = pygame.mouse.get_pos()

    terminado = animaciones.texto_terminado(
        contexto,
        contexto["total_letras"]
    )

    titulo = fuentes["opcion"].render(
        "¿QUE DECIDES HACER?",
        True,
        COLOR_TEXTO
    )

    ventana.blit(
        titulo,
        (X_OPCIONES, Y_TITULO_OPCIONES)
    )

    if not terminado:
        return

    for i in range(len(opciones)):

        dibujar_opcion(
            ventana,
            rectangulos[i],
            i,
            opciones[i]["texto"],
            rectangulos[i].collidepoint(posicion_mouse),
            fuentes
        )

# --------------------------------------------------
# CONTROLES
# --------------------------------------------------

def dibujar_controles(
    ventana: pygame.Surface,
    fuentes: dict
) -> None:

    """MOSTRAMOS LOS CONTROLES EN LA PARTE INFERIOR."""

    # FRANJA INFERIOR
    franja = pygame.Surface(
        (config.ANCHO, 47),
        pygame.SRCALPHA
    )

    franja.fill((28, 34, 46, 225))

    ventana.blit(
        franja,
        (0, 673)
    )

    controles = [
        ("G", "GUARDAR"),
        ("I", "INVENTARIO"),
        ("ESC", "MENU")
    ]

    x = 40
    y = 684

    for tecla, nombre in controles:

        ancho_tecla = 42 if len(tecla) == 1 else 48

        rect = pygame.Rect(
            x,
            y,
            ancho_tecla,
            25
        )

        pygame.draw.rect(
            ventana,
            (62, 72, 91),
            rect,
            border_radius=4
        )

        texto_tecla = fuentes["pequena"].render(
            tecla,
            True,
            (255, 255, 255)
        )

        ventana.blit(
            texto_tecla,
            (
                rect.centerx - texto_tecla.get_width() // 2,
                rect.centery - texto_tecla.get_height() // 2
            )
        )

        texto_nombre = fuentes["pequena"].render(
            nombre,
            True,
            (240, 240, 240)
        )

        ventana.blit(
            texto_nombre,
            (
                rect.right + 9,
                y + 2
            )
        )

        x = rect.right + texto_nombre.get_width() + 35


# --------------------------------------------------
# SEGUNDO DISENO: EXPLORACION
# --------------------------------------------------

def dibujar_panel_exploracion(
    ventana: pygame.Surface,
    rect: pygame.Rect
) -> None:

    """DIBUJAMOS UN PANEL OSCURO TRANSLUCIDO."""

    capa = pygame.Surface(
        (rect.width, rect.height),
        pygame.SRCALPHA
    )

    pygame.draw.rect(
        capa,
        COLOR_PANEL_EXPLORACION,
        capa.get_rect(),
        border_radius=12
    )

    ventana.blit(
        capa,
        rect.topleft
    )

    pygame.draw.rect(
        ventana,
        COLOR_BORDE_EXPLORACION,
        rect,
        1,
        border_radius=12
    )


def dibujar_encabezado_exploracion(
    ventana: pygame.Surface,
    nodo: dict,
    fuentes: dict
) -> None:

    """MOSTRAMOS EL NOMBRE DEL ESCENARIO."""

    nombre = nodo.get(
        "titulo_escena",
        "EXPLORACION"
    )

    titulo = fuentes["titulo_palace"].render(
        nombre,
        True,
        COLOR_ACENTO_EXPLORACION
    )

    subtitulo = fuentes["pequena"].render(
        "CAPITULO 01  |  EXPLORACION",
        True,
        COLOR_TEXTO_SECUNDARIO_EXPLORACION
    )

    ventana.blit(
        titulo,
        (X_EXPLORACION + 30, Y_EXPLORACION + 12)
    )

    ventana.blit(
        subtitulo,
        (X_EXPLORACION + 32, Y_EXPLORACION + 62)
    )

    pygame.draw.line(
        ventana,
        COLOR_BORDE_EXPLORACION,
        (
            X_EXPLORACION + 25,
            Y_EXPLORACION + 87
        ),
        (
            X_EXPLORACION + ANCHO_HISTORIA_EXPLORACION - 25,
            Y_EXPLORACION + 87
        ),
        1
    )


def dibujar_diario_exploracion(
    ventana: pygame.Surface,
    contexto: dict,
    fuentes: dict
) -> None:

    """MOSTRAMOS LA NARRACION DEL ESCENARIO."""

    titulo = fuentes["pequena"].render(
        "LO QUE OCURRE",
        True,
        COLOR_ACENTO_EXPLORACION
    )

    ventana.blit(
        titulo,
        (X_TEXTO_EXPLORACION, Y_EXPLORACION + 105)
    )

    visibles = dibujo.recortar_lineas(
        contexto["lineas"],
        int(contexto["letras_visibles"])
    )

    dibujo.dibujar_parrafo(
        ventana,
        visibles,
        fuentes["narracion"],
        COLOR_TEXTO_EXPLORACION,
        X_TEXTO_EXPLORACION,
        Y_TEXTO_EXPLORACION,
        espaciado=4
    )

    terminado = animaciones.texto_terminado(
        contexto,
        contexto["total_letras"]
    )

    if not terminado:

        pista = fuentes["pequena"].render(
            "ESPACIO PARA CONTINUAR",
            True,
            COLOR_TEXTO_SECUNDARIO_EXPLORACION
        )

        ventana.blit(
            pista,
            (
                X_EXPLORACION + ANCHO_HISTORIA_EXPLORACION
                - pista.get_width() - 25,
                Y_EXPLORACION + ALTO_HISTORIA_EXPLORACION
                - pista.get_height() - 12
            )
        )


def dibujar_opcion_exploracion(
    ventana: pygame.Surface,
    rect: pygame.Rect,
    indice: int,
    texto: str,
    encima: bool,
    fuentes: dict
) -> None:

    """DIBUJAMOS UNA DECISION DEL DISENO DE EXPLORACION."""

    color = (
        COLOR_BOTON_SELECCION_EXPLORACION
        if encima
        else COLOR_BOTON_EXPLORACION
    )

    capa = pygame.Surface(
        (rect.width, rect.height),
        pygame.SRCALPHA
    )

    pygame.draw.rect(
        capa,
        color,
        capa.get_rect(),
        border_radius=6
    )

    ventana.blit(
        capa,
        rect.topleft
    )

    if encima:

        pygame.draw.rect(
            ventana,
            COLOR_ACENTO_EXPLORACION,
            (
                rect.x,
                rect.y + 5,
                4,
                rect.height - 10
            )
        )

    numero = fuentes["pequena"].render(
        str(indice + 1),
        True,
        COLOR_ACENTO_EXPLORACION
    )

    texto_opcion = fuentes["pequena"].render(
        texto,
        True,
        COLOR_TEXTO_EXPLORACION
    )

    ventana.blit(
        numero,
        (
            rect.x + 15,
            rect.centery - numero.get_height() // 2
        )
    )

    ventana.blit(
        texto_opcion,
        (
            rect.x + 48,
            rect.centery - texto_opcion.get_height() // 2
        )
    )


def dibujar_opciones_exploracion(
    ventana: pygame.Surface,
    contexto: dict,
    fuentes: dict
) -> None:

    """MOSTRAMOS LAS DECISIONES DEL ESCENARIO."""

    opciones = contexto["opciones"]

    rectangulos = rectangulos_opciones_exploracion(
        len(opciones)
    )

    titulo = fuentes["opcion"].render(
        "¿QUE DECIDES HACER?",
        True,
        COLOR_TEXTO_EXPLORACION
    )

    ventana.blit(
        titulo,
        (
            X_OPCIONES_EXPLORACION,
            Y_TITULO_OPCIONES_EXPLORACION
        )
    )

    terminado = animaciones.texto_terminado(
        contexto,
        contexto["total_letras"]
    )

    if not terminado:
        return

    posicion_mouse = pygame.mouse.get_pos()

    for i in range(len(opciones)):

        dibujar_opcion_exploracion(
            ventana,
            rectangulos[i],
            i,
            opciones[i]["texto"],
            rectangulos[i].collidepoint(posicion_mouse),
            fuentes
        )


def dibujar_diseno_exploracion(
    ventana: pygame.Surface,
    contexto: dict,
    nodo: dict,
    fuentes: dict
) -> None:

    """DIBUJAMOS LA NUEVA VENTANA DE EXPLORACION."""

    cantidad_opciones = len(contexto["opciones"])

    alto_opciones = (
        Y_BOTONES_EXPLORACION
        + cantidad_opciones * ALTO_BOTON_EXPLORACION
        + max(0, cantidad_opciones - 1) * SEPARACION_EXPLORACION
        + 15
        - 425
    )

    panel_historia = pygame.Rect(
        X_EXPLORACION,
        Y_EXPLORACION,
        ANCHO_HISTORIA_EXPLORACION,
        ALTO_HISTORIA_EXPLORACION
    )

    panel_opciones = pygame.Rect(
        X_EXPLORACION,
        425,
        ANCHO_HISTORIA_EXPLORACION,
        alto_opciones
    )

    dibujar_panel_exploracion(
        ventana,
        panel_historia
    )

    dibujar_panel_exploracion(
        ventana,
        panel_opciones
    )

    dibujar_encabezado_exploracion(
        ventana,
        nodo,
        fuentes
    )

    dibujar_diario_exploracion(
        ventana,
        contexto,
        fuentes
    )

    dibujar_opciones_exploracion(
        ventana,
        contexto,
        fuentes
    )

    dibujar_controles(
        ventana,
        fuentes
    )


# --------------------------------------------------
# PRIMER DISENO: PINK PALACE
# --------------------------------------------------

def dibujar_diseno_pink_palace(
    ventana: pygame.Surface,
    contexto: dict,
    nodo: dict,
    fuentes: dict
) -> None:

    """CONSERVAMOS EL DISENO ORIGINAL DE PINK PALACE."""

    dibujar_contenedor(
        ventana,
        len(contexto["opciones"])
    )

    dibujar_encabezado(
        ventana,
        fuentes
    )

    if nodo.get("mostrar_personaje", True):

        dibujar_personaje(
            ventana,
            contexto
        )

    dibujar_diario(
        ventana,
        contexto,
        fuentes
    )

    dibujar_opciones(
        ventana,
        contexto,
        fuentes
    )

    dibujar_controles(
        ventana,
        fuentes
    )

# --------------------------------------------------
# DIBUJAR PANTALLA
# --------------------------------------------------
def dibujar(
    ventana: pygame.Surface,
    contexto: dict
) -> None:

    """DIBUJAMOS EL DISEÑO CORRESPONDIENTE A CADA ESCENA."""

    nodo = motor.nodo_actual(
        contexto["estado"],
        contexto["nodos"]
    )

    fuentes = contexto["fuentes"]

    dibujar_fondo(ventana, nodo)

    if nodo.get("diseno") == "exploracion":

        dibujar_diseno_exploracion(
            ventana,
            contexto,
            nodo,
            fuentes
        )

    else:

        dibujar_diseno_pink_palace(
            ventana,
            contexto,
            nodo,
            fuentes
        )

    animaciones.dibujar_desvanecer(
        ventana,
        contexto["transparencia"]
    )