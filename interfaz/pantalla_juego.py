"""PANTALLA PRINCIPAL DEL JUEGO CORALINE.

Aqui solo va el flujo: preparar el nodo, recibir clics y teclas, y elegir
opciones. Lo que se ve depende del diseno de cada escena (interfaz/disenos/).
"""

import pygame

import config
from juego import motor
from juego import partida
from interfaz import dibujo
from interfaz import animaciones
from interfaz import pantalla_minijuego
from interfaz import disenos


PREGUNTA_POR_DEFECTO = "¿QUE DECIDES HACER?"

TECLAS_NUMERO = [
    pygame.K_1,
    pygame.K_2,
    pygame.K_3,
    pygame.K_4
]


# --------------------------------------------------
# PREPARAR HISTORIA
# --------------------------------------------------

def lineas_del_nodo(nodo: dict, fuentes: dict) -> list:

    """DIVIDE EL TEXTO DEL NODO EN RENGLONES SEGUN EL ANCHO DE SU DISENO."""

    diseno = disenos.del_nodo(nodo)

    return dibujo.dividir_en_lineas(
        nodo["texto"],
        fuentes["narracion"],
        diseno.ANCHO_TEXTO
    )


def solo_canonicas(opciones: list) -> list:

    """DEJA SOLO LAS OPCIONES DE LA RUTA DEL LIBRO.

    Si ninguna es canonica (no deberia pasar), regresa todas para que el
    jugador no se quede atorado.
    """

    canonicas = []

    for opcion in opciones:

        if opcion.get("canonica", False):
            canonicas.append(opcion)

    if len(canonicas) == 0:
        return opciones

    return canonicas


def preparar_nodo(contexto: dict) -> None:

    """PREPARAMOS EL TEXTO Y LAS OPCIONES DEL NODO."""

    nodo = motor.nodo_actual(
        contexto["estado"],
        contexto["nodos"]
    )

    lineas = lineas_del_nodo(nodo, contexto["fuentes"])

    contexto["lineas"] = lineas

    contexto["total_letras"] = dibujo.contar_letras(lineas)

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

        if config.SOLO_RUTA_CANONICA:

            contexto["opciones"] = solo_canonicas(
                contexto["opciones"]
            )

    contexto["pregunta"] = nodo.get(
        "pregunta",
        PREGUNTA_POR_DEFECTO
    )

    # LOS BOTONES SE CALCULAN AL DIBUJAR LA ESCENA NUEVA
    contexto["rect_opciones"] = []

    animaciones.reiniciar(contexto)


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

        # EL DISENO NOS DICE DONDE QUEDARON LOS BOTONES
        rectangulos = contexto["rect_opciones"]

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
# DIBUJAR PANTALLA
# --------------------------------------------------

def dibujar(
    ventana: pygame.Surface,
    contexto: dict
) -> None:

    """DIBUJAMOS LA ESCENA CON EL DISENO QUE PIDA EL NODO."""

    nodo = motor.nodo_actual(
        contexto["estado"],
        contexto["nodos"]
    )

    diseno = disenos.del_nodo(nodo)

    contexto["rect_opciones"] = diseno.dibujar(
        ventana,
        contexto,
        nodo
    )

    animaciones.dibujar_desvanecer(
        ventana,
        contexto["transparencia"]
    )
