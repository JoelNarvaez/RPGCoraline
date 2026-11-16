"""PIEZAS COMPARTIDAS PARA ARMAR LOS DISENOS DE ESCENA.

Cada diseno de interfaz/disenos/ se arma con estas funciones. Los paneles se
ajustan solos al texto y a las opciones, asi que nada se sale de la pantalla.

Archivo compartido: si se cambia algo aqui, avisar al otro.

Un "estilo" es un diccionario con los colores de un diseno:
    panel, borde, texto, texto_secundario, acento, boton, boton_encima
Los colores pueden llevar transparencia (R, G, B, A).
"""

import os
import pygame

import config
from interfaz import dibujo
from interfaz import animaciones
from interfaz import fondos


# MEDIDAS COMUNES A TODOS LOS DISENOS
MARGEN = 30             # espacio entre el borde del panel y su contenido
ESPACIADO_TEXTO = 5     # espacio extra entre renglones de la narracion
SEPARACION_PANELES = 15
ALTO_BOTON = 44
SEPARACION_BOTONES = 8
Y_CONTROLES = 673       # donde empieza la franja de controles de abajo

FONDOS_CARGADOS = {}
PERSONAJE_CARGADO = {}


# --------------------------------------------------
# MEDIDAS
# --------------------------------------------------

def alto_renglon(fuentes: dict) -> int:

    """ALTO DE UN RENGLON DE NARRACION, CONTANDO EL ESPACIADO."""

    return fuentes["narracion"].get_height() + ESPACIADO_TEXTO


def alto_encabezado(fuentes: dict) -> int:

    """ALTO DEL TITULO DE LA ESCENA MAS SU LINEA SEPARADORA."""

    return fuentes["titulo_palace"].get_height() + 22


def alto_panel_historia(cantidad_lineas: int, fuentes: dict) -> int:

    """ALTO QUE NECESITA EL PANEL DE HISTORIA PARA ESE NUMERO DE RENGLONES."""

    alto_pista = fuentes["pequena"].get_height() + 8

    return (
        MARGEN // 2
        + alto_encabezado(fuentes)
        + cantidad_lineas * alto_renglon(fuentes)
        + alto_pista
        + MARGEN // 2
    )


def alto_panel_opciones(
    cantidad_opciones: int,
    alto_boton: int,
    fuentes: dict
) -> int:

    """ALTO QUE NECESITA EL PANEL DE OPCIONES."""

    alto_botones = (
        cantidad_opciones * alto_boton
        + max(0, cantidad_opciones - 1) * SEPARACION_BOTONES
    )

    return (
        MARGEN // 2
        + fuentes["opcion"].get_height() + 12
        + alto_botones
        + MARGEN // 2
    )


def maximo_lineas(
    y_panel: int,
    alto_boton: int,
    fuentes: dict
) -> int:

    """CUANTOS RENGLONES CABEN SI LA ESCENA TIENE EL MAXIMO DE OPCIONES.

    Lo usa el verificador para avisar si un texto no cabe en su diseno.
    """

    espacio = (
        Y_CONTROLES - 10
        - y_panel
        - SEPARACION_PANELES
        - alto_panel_opciones(config.MAXIMO_OPCIONES, alto_boton, fuentes)
        - alto_panel_historia(0, fuentes)
    )

    return espacio // alto_renglon(fuentes)


# --------------------------------------------------
# FONDO
# --------------------------------------------------

def crear_fondo(nombre_imagen: str) -> pygame.Surface:

    """CARGAMOS LA IMAGEN Y LA RECORTAMOS AL TAMANO DE LA VENTANA."""

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

    return imagen.subsurface(
        (x_recorte, y_recorte, config.ANCHO, config.ALTO)
    ).copy()


def fondo(
    ventana: pygame.Surface,
    nodo: dict
) -> None:

    """MOSTRAMOS LA IMAGEN DE LA ESCENA, O SU FONDO DIBUJADO CON CODIGO."""

    if "fondo" in nodo:
        fondos.FONDOS[nodo["fondo"]].dibujar(ventana)
        return

    nombre_imagen = nodo.get(
        "imagen",
        "casarosa.webp"
    )

    if nombre_imagen not in FONDOS_CARGADOS:
        FONDOS_CARGADOS[nombre_imagen] = crear_fondo(nombre_imagen)

    ventana.blit(
        FONDOS_CARGADOS[nombre_imagen],
        (0, 0)
    )


# --------------------------------------------------
# PANELES
# --------------------------------------------------

def rectangulo_con_transparencia(
    ventana: pygame.Surface,
    rect: pygame.Rect,
    color: tuple,
    radio: int
) -> None:

    """DIBUJA UN RECTANGULO QUE PUEDE SER TRANSLUCIDO."""

    capa = pygame.Surface(
        (rect.width, rect.height),
        pygame.SRCALPHA
    )

    pygame.draw.rect(
        capa,
        color,
        capa.get_rect(),
        border_radius=radio
    )

    ventana.blit(
        capa,
        rect.topleft
    )


def panel(
    ventana: pygame.Surface,
    rect: pygame.Rect,
    estilo: dict
) -> None:

    """PANEL CON ESQUINAS REDONDAS Y BORDE DELGADO."""

    rectangulo_con_transparencia(
        ventana,
        rect,
        estilo["panel"],
        12
    )

    pygame.draw.rect(
        ventana,
        estilo["borde"],
        rect,
        1,
        border_radius=12
    )


def titulo_de_escena(
    contexto: dict,
    nodo: dict
) -> list:

    """REGRESA [TITULO, SUBTITULO] DE LA ESCENA.

    El titulo es "titulo_escena" del nodo o, si no tiene, el del capitulo.
    """

    clave_capitulo = contexto["estado"]["nodo_actual"][:5]

    capitulo = contexto["capitulos"].get(
        clave_capitulo,
        {"numero": 0, "titulo": ""}
    )

    titulo = nodo.get(
        "titulo_escena",
        capitulo["titulo"]
    )

    subtitulo = ""

    if capitulo["numero"] > 0:
        subtitulo = "CAPITULO " + str(capitulo["numero"])

    return [titulo, subtitulo]


def panel_historia(
    ventana: pygame.Surface,
    contexto: dict,
    nodo: dict,
    x: int,
    y: int,
    ancho: int,
    estilo: dict
) -> int:

    """PANEL CON EL TITULO DE LA ESCENA Y LA NARRACION.

    Su alto depende de cuantos renglones tenga el texto completo, asi el
    panel no cambia de tamano mientras se escribe. Regresa la y donde termina.
    """

    fuentes = contexto["fuentes"]

    alto = alto_panel_historia(
        len(contexto["lineas"]),
        fuentes
    )

    rect = pygame.Rect(x, y, ancho, alto)

    panel(ventana, rect, estilo)

    # ENCABEZADO: TITULO A LA IZQUIERDA, CAPITULO A LA DERECHA
    titulo, subtitulo = titulo_de_escena(contexto, nodo)

    imagen_titulo = fuentes["titulo_palace"].render(
        titulo,
        True,
        estilo["acento"]
    )

    y_titulo = y + MARGEN // 2

    ventana.blit(
        imagen_titulo,
        (x + MARGEN, y_titulo)
    )

    imagen_subtitulo = fuentes["pequena"].render(
        subtitulo,
        True,
        estilo["texto_secundario"]
    )

    y_linea = y_titulo + fuentes["titulo_palace"].get_height() + 4

    ventana.blit(
        imagen_subtitulo,
        (
            x + ancho - MARGEN - imagen_subtitulo.get_width(),
            y_linea - imagen_subtitulo.get_height() - 8
        )
    )

    pygame.draw.line(
        ventana,
        estilo["borde"],
        (x + MARGEN - 5, y_linea),
        (x + ancho - MARGEN + 5, y_linea),
        1
    )

    # NARRACION CON MAQUINA DE ESCRIBIR
    visibles = dibujo.recortar_lineas(
        contexto["lineas"],
        int(contexto["letras_visibles"])
    )

    dibujo.dibujar_parrafo(
        ventana,
        visibles,
        fuentes["narracion"],
        estilo["texto"],
        x + MARGEN,
        y + MARGEN // 2 + alto_encabezado(fuentes),
        espaciado=ESPACIADO_TEXTO
    )

    # PISTA DENTRO DEL PANEL MIENTRAS SE ESCRIBE
    if not animaciones.texto_terminado(contexto, contexto["total_letras"]):

        pista = fuentes["pequena"].render(
            "ESPACIO PARA CONTINUAR",
            True,
            estilo["texto_secundario"]
        )

        ventana.blit(
            pista,
            (
                x + ancho - MARGEN - pista.get_width(),
                y + alto - MARGEN // 2 - pista.get_height()
            )
        )

    return y + alto


def boton(
    ventana: pygame.Surface,
    rect: pygame.Rect,
    numero: int,
    texto: str,
    encima: bool,
    fuentes: dict,
    estilo: dict
) -> None:

    """UNA OPCION: NUMERO A LA IZQUIERDA Y TEXTO."""

    color = estilo["boton_encima"] if encima else estilo["boton"]

    rectangulo_con_transparencia(
        ventana,
        rect,
        color,
        6
    )

    if encima:

        pygame.draw.rect(
            ventana,
            estilo["acento"],
            (rect.x, rect.y + 5, 4, rect.height - 10)
        )

    imagen_numero = fuentes["pequena"].render(
        str(numero),
        True,
        estilo["acento"]
    )

    ventana.blit(
        imagen_numero,
        (rect.x + 18, rect.centery - imagen_numero.get_height() // 2)
    )

    imagen_texto = fuentes["pequena"].render(
        texto,
        True,
        estilo["texto"]
    )

    ventana.blit(
        imagen_texto,
        (rect.x + 50, rect.centery - imagen_texto.get_height() // 2)
    )


def panel_opciones(
    ventana: pygame.Surface,
    contexto: dict,
    x: int,
    y: int,
    ancho: int,
    alto_boton: int,
    estilo: dict
) -> list:

    """PANEL CON LAS DECISIONES. SOLO APARECE CUANDO TERMINA EL TEXTO.

    Regresa los rectangulos de los botones, en orden, para saber donde dio
    clic el jugador. Si todavia no aparecen, regresa una lista vacia.
    """

    if not animaciones.texto_terminado(contexto, contexto["total_letras"]):
        return []

    fuentes = contexto["fuentes"]
    opciones = contexto["opciones"]

    alto = alto_panel_opciones(
        len(opciones),
        alto_boton,
        fuentes
    )

    panel(ventana, pygame.Rect(x, y, ancho, alto), estilo)

    titulo = fuentes["opcion"].render(
        contexto["pregunta"],
        True,
        estilo["texto"]
    )

    ventana.blit(
        titulo,
        (x + MARGEN - 5, y + MARGEN // 2)
    )

    rectangulos = []

    y_boton = y + MARGEN // 2 + fuentes["opcion"].get_height() + 12

    posicion_mouse = pygame.mouse.get_pos()

    for i in range(len(opciones)):

        rect = pygame.Rect(
            x + MARGEN - 10,
            y_boton,
            ancho - (MARGEN - 10) * 2,
            alto_boton
        )

        boton(
            ventana,
            rect,
            i + 1,
            opciones[i]["texto"],
            rect.collidepoint(posicion_mouse),
            fuentes,
            estilo
        )

        rectangulos.append(rect)

        y_boton = y_boton + alto_boton + SEPARACION_BOTONES

    return rectangulos


# --------------------------------------------------
# PERSONAJE
# --------------------------------------------------

def personaje(
    ventana: pygame.Surface,
    nombre_imagen: str,
    x: int,
    y: int,
    ancho: int,
    alto: int
) -> None:

    """DIBUJA UN PERSONAJE PARADO SOBRE EL BORDE DE ABAJO DEL AREA DADA."""

    clave = nombre_imagen + str(ancho) + "x" + str(alto)

    if clave not in PERSONAJE_CARGADO:

        ruta = os.path.join(config.RUTA_IMAGENES, nombre_imagen)

        imagen = None

        if os.path.exists(ruta):

            imagen = pygame.image.load(ruta).convert_alpha()

            ancho_original, alto_original = imagen.get_size()

            escala = min(
                ancho / ancho_original,
                alto / alto_original
            )

            imagen = pygame.transform.scale(
                imagen,
                (int(ancho_original * escala), int(alto_original * escala))
            )

        PERSONAJE_CARGADO[clave] = imagen

    imagen = PERSONAJE_CARGADO[clave]

    if imagen is None:
        return

    # SOMBRA SUAVE DEBAJO DEL PERSONAJE
    sombra = pygame.Surface((ancho, 22), pygame.SRCALPHA)

    pygame.draw.ellipse(
        sombra,
        (10, 14, 22, 100),
        (10, 3, ancho - 20, 15)
    )

    ventana.blit(sombra, (x, y + alto - 5))

    ventana.blit(
        imagen,
        (
            x + (ancho - imagen.get_width()) // 2,
            y + alto - imagen.get_height()
        )
    )


# --------------------------------------------------
# CONTROLES
# --------------------------------------------------

def controles(
    ventana: pygame.Surface,
    fuentes: dict
) -> None:

    """FRANJA DE ABAJO CON LAS TECLAS DEL JUEGO."""

    franja = pygame.Surface(
        (config.ANCHO, config.ALTO - Y_CONTROLES),
        pygame.SRCALPHA
    )

    franja.fill((28, 34, 46, 225))

    ventana.blit(franja, (0, Y_CONTROLES))

    lista = [
        ("G", "GUARDAR"),
        ("I", "INVENTARIO"),
        ("ESC", "MENU")
    ]

    x = 40
    y = Y_CONTROLES + 11

    for tecla, nombre in lista:

        ancho_tecla = 42 if len(tecla) == 1 else 48

        rect = pygame.Rect(x, y, ancho_tecla, 25)

        pygame.draw.rect(
            ventana,
            (62, 72, 91),
            rect,
            border_radius=4
        )

        texto_tecla = fuentes["pequena"].render(tecla, True, (255, 255, 255))

        ventana.blit(
            texto_tecla,
            (
                rect.centerx - texto_tecla.get_width() // 2,
                rect.centery - texto_tecla.get_height() // 2
            )
        )

        texto_nombre = fuentes["pequena"].render(nombre, True, (240, 240, 240))

        ventana.blit(texto_nombre, (rect.right + 9, y + 2))

        x = rect.right + texto_nombre.get_width() + 35

