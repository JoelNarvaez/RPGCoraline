"""Minijuego "llave_puerta": meter la llave negra en la cerradura de la puerta pequeña.

Pixel art dibujado con código, con la misma técnica que los fondos de las
escenas (lienzo de 640x360 escalado x2, capa fija + lo que se mueve).
Se ve de cerca la puerta tallada del salón. Coraline está a la izquierda y la
llave en el piso, frente a ella.

Como dice la historia, la llave está helada y pesa más de lo que parece:
- al arrastrarla se queda atrás del mouse (pesa) y se cuelga un poco,
- cerca de la puerta tiembla (frío),
- si se suelta lejos de la cerradura, se cae otra vez al piso.
Gana quien deja la punta de la llave en la cerradura.

En el nodo:
  "tipo": "llave_puerta"
  "instruccion": texto que se muestra antes de empezar
  "tiempo": segundos

Responsable: Persona A
"""

import math
import random

import pygame

import config
from interfaz.fondos.pintura import ANCHO, ALTO
from interfaz.fondos.pintura import mezclar, degradado, brillo, orillas_oscuras, mostrar, tablas_de_madera
from interfaz.fondos import personajes

ESCALA: int = config.ANCHO // ANCHO       # 2

Y_PISO: int = 300
PUERTA: pygame.Rect = pygame.Rect(400, 96, 136, Y_PISO - 96)
CERRADURA: tuple = (512, 206)             # el hoyo de la cerradura
X_CORALINE: int = 120
LLAVE_INICIO: tuple = (176, 292)          # centro de la llave tirada en el piso

LARGO_LLAVE: int = 40                     # del centro del aro a la punta
PESO: float = 5.0                         # entre mas chico, mas lento sigue al mouse
COLGADA: int = 7                          # cuanto se cuelga hacia abajo al cargarla
RADIO_AGARRAR: int = 22
RADIO_CERRADURA: int = 9                  # que tan cerca debe quedar la punta
DISTANCIA_FRIO: int = 70                  # desde aqui empieza a temblar

COLOR_PARED: tuple = (52, 112, 116)
COLOR_PUERTA: tuple = (118, 108, 104)
COLOR_LATON: tuple = (196, 156, 72)
COLOR_LLAVE: tuple = (16, 14, 18)
COLOR_ORILLA_LLAVE: tuple = (176, 168, 196)

CAPAS: dict = {}


# ------------------------------------------------------------ parte fija

def dibujar_pared(lienzo: pygame.Surface) -> None:
    """Pared verde azulada con rayas del papel tapiz, guardasilla y piso de tablas."""
    degradado(lienzo, pygame.Rect(0, 0, ANCHO, Y_PISO), (18, 40, 44), COLOR_PARED, 20)
    for x in range(0, ANCHO, 18):
        pygame.draw.line(lienzo, mezclar(COLOR_PARED, (0, 0, 0), 0.15), (x, 10), (x, 200))
        pygame.draw.line(lienzo, mezclar(COLOR_PARED, (255, 255, 255), 0.06), (x + 9, 10), (x + 9, 200))
    pygame.draw.rect(lienzo, (34, 78, 82), (0, 200, ANCHO, 6))
    pygame.draw.line(lienzo, (80, 140, 142), (0, 200), (ANCHO, 200))
    pygame.draw.rect(lienzo, (40, 88, 92), (0, 206, ANCHO, Y_PISO - 206))
    pygame.draw.rect(lienzo, (22, 50, 54), (0, Y_PISO - 6, ANCHO, 6))
    tablas_de_madera(lienzo, pygame.Rect(0, Y_PISO, ANCHO, ALTO - Y_PISO), (78, 56, 46), 8)


def dibujar_puerta(lienzo: pygame.Surface) -> None:
    """La puerta pequeña tallada: marco, tablero con arcos, perilla y la placa de la cerradura."""
    marco: pygame.Rect = PUERTA.inflate(16, 8).move(0, -4)
    pygame.draw.rect(lienzo, (26, 50, 54), marco)
    pygame.draw.rect(lienzo, (70, 128, 130), marco, 1)

    pygame.draw.rect(lienzo, COLOR_PUERTA, PUERTA)
    pygame.draw.rect(lienzo, mezclar(COLOR_PUERTA, (0, 0, 0), 0.25), (PUERTA.right - 18, PUERTA.y, 18, PUERTA.height))
    for x in range(PUERTA.x + 6, PUERTA.right - 4, 7):
        pygame.draw.line(lienzo, mezclar(COLOR_PUERTA, (0, 0, 0), 0.12), (x, PUERTA.y + 2), (x, PUERTA.bottom - 2))

    # TABLEROS TALLADOS: DOS ARCOS ARRIBA Y DOS RECTANGULOS ABAJO, CON RELIEVE
    for x in [PUERTA.x + 14, PUERTA.x + 72]:
        arco: pygame.Rect = pygame.Rect(x, PUERTA.y + 16, 48, 84)
        pygame.draw.rect(lienzo, mezclar(COLOR_PUERTA, (0, 0, 0), 0.18), arco, border_top_left_radius=24, border_top_right_radius=24)
        pygame.draw.rect(lienzo, mezclar(COLOR_PUERTA, (255, 255, 255), 0.2), arco, 1, border_top_left_radius=24, border_top_right_radius=24)
        abajo: pygame.Rect = pygame.Rect(x, PUERTA.y + 114, 48, 74)
        pygame.draw.rect(lienzo, mezclar(COLOR_PUERTA, (0, 0, 0), 0.18), abajo)
        pygame.draw.line(lienzo, mezclar(COLOR_PUERTA, (255, 255, 255), 0.2), abajo.topleft, abajo.topright)
        pygame.draw.line(lienzo, mezclar(COLOR_PUERTA, (255, 255, 255), 0.2), abajo.topleft, abajo.bottomleft)

    # PLACA DE LATON CON EL HOYO DE LA CERRADURA
    x, y = CERRADURA
    pygame.draw.ellipse(lienzo, COLOR_LATON, (x - 8, y - 14, 16, 30))
    pygame.draw.ellipse(lienzo, (120, 86, 36), (x - 8, y - 14, 16, 30), 1)
    pygame.draw.line(lienzo, (240, 210, 130), (x - 5, y - 10), (x - 5, y + 8))
    pygame.draw.circle(lienzo, (10, 8, 12), (x, y - 2), 3)
    pygame.draw.polygon(lienzo, (10, 8, 12), [(x - 2, y), (x + 2, y), (x + 3, y + 8), (x - 3, y + 8)])

    # PERILLA
    pygame.draw.circle(lienzo, COLOR_LATON, (x, y - 30), 6)
    pygame.draw.circle(lienzo, (240, 210, 130), (x - 2, y - 32), 2)
    pygame.draw.circle(lienzo, (120, 86, 36), (x, y - 30), 6, 1)


def crear_fijo() -> pygame.Surface:
    lienzo: pygame.Surface = pygame.Surface((ANCHO, ALTO))
    dibujar_pared(lienzo)
    dibujar_puerta(lienzo)
    personajes.dibujar_coraline_chica(lienzo, X_CORALINE, Y_PISO, True)
    brillo(lienzo, (300, 60), 220, (200, 230, 230), 40)
    brillo(lienzo, CERRADURA, 60, (150, 210, 230), 40)
    orillas_oscuras(lienzo)
    return lienzo


# ------------------------------------------------------------ el juego

def punta(juego: dict) -> tuple:
    """La punta de la llave (lo que entra en la cerradura): a la derecha del aro."""
    return (juego["x"] + LARGO_LLAVE // 2, juego["y"])


def iniciar(datos: dict) -> dict:
    if "fijo" not in CAPAS:
        CAPAS["fijo"] = crear_fijo()
    return {
        "x": float(LLAVE_INICIO[0]),
        "y": float(LLAVE_INICIO[1]),
        "mouse": LLAVE_INICIO,
        "arrastrando": False,
        "cayendo": False,
        "temblor": (0, 0),
        "reloj": 0.0,
        "tiempo_total": float(datos["tiempo"]),
        "tiempo_restante": float(datos["tiempo"]),
        "resultado": "",
    }


def manejar_evento(evento: pygame.event.Event, juego: dict) -> None:
    if evento.type == pygame.MOUSEBUTTONDOWN and evento.button == 1:
        x: int = evento.pos[0] // ESCALA
        y: int = evento.pos[1] // ESCALA
        if math.dist((x, y), (juego["x"], juego["y"])) < RADIO_AGARRAR:
            juego["arrastrando"] = True
            juego["cayendo"] = False
            juego["mouse"] = (x, y)

    elif evento.type == pygame.MOUSEMOTION and juego["arrastrando"]:
        juego["mouse"] = (evento.pos[0] // ESCALA, evento.pos[1] // ESCALA)

    elif evento.type == pygame.MOUSEBUTTONUP and evento.button == 1 and juego["arrastrando"]:
        juego["arrastrando"] = False
        if math.dist(punta(juego), CERRADURA) < RADIO_CERRADURA:
            # QUEDA METIDA: LA PUNTA JUSTO EN EL HOYO
            juego["x"] = float(CERRADURA[0] - LARGO_LLAVE // 2)
            juego["y"] = float(CERRADURA[1])
            juego["resultado"] = "exito"
        else:
            juego["cayendo"] = True


def actualizar(juego: dict, dt: float) -> None:
    juego["reloj"] = juego["reloj"] + dt

    if juego["arrastrando"]:
        # PESA: VA HACIA EL MOUSE POCO A POCO, Y UN POCO MAS ABAJO (SE CUELGA)
        avance: float = min(1.0, dt * PESO)
        juego["x"] = juego["x"] + (juego["mouse"][0] - juego["x"]) * avance
        juego["y"] = juego["y"] + (juego["mouse"][1] + COLGADA - juego["y"]) * avance

        # HELADA: CERCA DE LA PUERTA TIEMBLA, MAS ENTRE MAS CERCA
        distancia: float = math.dist(punta(juego), CERRADURA)
        if distancia < DISTANCIA_FRIO:
            fuerza: int = 1 + int((DISTANCIA_FRIO - distancia) / 25)
            juego["temblor"] = (random.randint(-fuerza, fuerza), random.randint(-fuerza, fuerza))
        else:
            juego["temblor"] = (0, 0)

    elif juego["cayendo"]:
        # SE CAE AL PISO Y REGRESA A DONDE ESTABA
        juego["temblor"] = (0, 0)
        juego["x"] = juego["x"] + (LLAVE_INICIO[0] - juego["x"]) * min(1.0, dt * 6)
        juego["y"] = juego["y"] + (LLAVE_INICIO[1] - juego["y"]) * min(1.0, dt * 8)
        if math.dist((juego["x"], juego["y"]), LLAVE_INICIO) < 1:
            juego["cayendo"] = False

    juego["tiempo_restante"] = juego["tiempo_restante"] - dt
    if juego["tiempo_restante"] <= 0 and juego["resultado"] == "":
        juego["resultado"] = "fallo"


# ------------------------------------------------------------ lo que se mueve

def dibujar_forma_llave(lienzo: pygame.Surface, color: tuple, x: int, y: int, grueso: int) -> None:
    """Aro a la izquierda, varilla y dientes a la derecha. grueso 1 = orilla clara de atrás."""
    mitad: int = LARGO_LLAVE // 2
    pygame.draw.circle(lienzo, color, (x - mitad + 6, y), 6 + grueso)
    pygame.draw.rect(lienzo, color, (x - mitad + 10 - grueso, y - 2 - grueso, LARGO_LLAVE - 10 + grueso * 2, 4 + grueso * 2))
    pygame.draw.rect(lienzo, color, (x + mitad - 8 - grueso, y + 1 - grueso, 3 + grueso * 2, 6 + grueso * 2))
    pygame.draw.rect(lienzo, color, (x + mitad - 3 - grueso, y + 1 - grueso, 3 + grueso * 2, 8 + grueso * 2))


def dibujar_llave(lienzo: pygame.Surface, juego: dict) -> None:
    x: int = int(juego["x"]) + juego["temblor"][0]
    y: int = int(juego["y"]) + juego["temblor"][1]

    if juego["resultado"] == "exito":
        # METIDA: SOLO SE VE EL ARO Y UN PEDAZO DE VARILLA AFUERA DE LA PLACA
        mitad: int = LARGO_LLAVE // 2
        pygame.draw.rect(lienzo, COLOR_LLAVE, (x - mitad + 10, y - 2, LARGO_LLAVE - 14, 4))
        pygame.draw.circle(lienzo, COLOR_ORILLA_LLAVE, (x - mitad + 6, y), 7)
        pygame.draw.circle(lienzo, COLOR_LLAVE, (x - mitad + 6, y), 6)
        pygame.draw.circle(lienzo, COLOR_PARED, (x - mitad + 6, y), 2)
        return

    # SOMBRITA EN EL PISO CUANDO ESTA ABAJO
    if y > Y_PISO - 20:
        sombra: pygame.Surface = pygame.Surface((LARGO_LLAVE + 6, 5), pygame.SRCALPHA)
        pygame.draw.ellipse(sombra, (0, 0, 0, 110), sombra.get_rect())
        lienzo.blit(sombra, (x - LARGO_LLAVE // 2 - 3, Y_PISO + 4))

    dibujar_forma_llave(lienzo, COLOR_ORILLA_LLAVE, x, y, 1)
    dibujar_forma_llave(lienzo, COLOR_LLAVE, x, y, 0)
    pygame.draw.circle(lienzo, (60, 70, 80), (x - LARGO_LLAVE // 2 + 6, y), 2)          # hueco del aro
    pygame.draw.line(lienzo, (80, 76, 96), (x - 8, y - 1), (x + 12, y - 1))               # brillito

    # ESCARCHA: PUNTITOS BLANCOS QUE APARECEN Y SE VAN
    for i in range(3):
        if (juego["reloj"] * 2 + i * 0.4) % 1.2 < 0.4:
            lienzo.set_at((x - 12 + i * 11, y - 3 + (i % 2) * 5), (230, 244, 255))


def dibujar_aviso(lienzo: pygame.Surface, juego: dict) -> None:
    """Aro que late alrededor de la llave cuando está quieta: se puede agarrar."""
    if juego["arrastrando"] or juego["cayendo"] or juego["resultado"] != "":
        return
    radio: int = 20 + int(math.sin(juego["reloj"] * 6) * 2)
    pygame.draw.circle(lienzo, config.COLOR_ACENTO, (int(juego["x"]), int(juego["y"])), radio, 1)


def dibujar_aire_frio(lienzo: pygame.Surface, tiempo: float) -> None:
    """Hilitos de aire frío que salen del hoyo de la cerradura."""
    capa: pygame.Surface = pygame.Surface((ANCHO, ALTO), pygame.SRCALPHA)
    for i in range(3):
        fase: float = (tiempo * 0.5 + i / 3) % 1
        x: int = CERRADURA[0] - 4 - int(fase * 60)
        y: int = CERRADURA[1] + 2 + int(math.sin(tiempo * 3 + i * 2) * 4) + i * 3
        alfa: int = int(90 * math.sin(fase * math.pi))
        pygame.draw.line(capa, (200, 230, 240, alfa), (x, y), (x + 10, y - 1))
    lienzo.blit(capa, (0, 0))


def dibujar_polvo(lienzo: pygame.Surface, tiempo: float) -> None:
    for i in range(14):
        x: int = 40 + (i * 47 + int(tiempo * 5)) % 560
        y: int = 40 + int(math.sin(tiempo * 0.7 + i) * 16) + (i * 23) % 160
        lienzo.set_at((x, y), (200, 228, 226))


def dibujar(ventana: pygame.Surface, juego: dict, fuentes: dict) -> None:
    lienzo: pygame.Surface = CAPAS["fijo"].copy()
    dibujar_polvo(lienzo, juego["reloj"])
    dibujar_aire_frio(lienzo, juego["reloj"])
    dibujar_aviso(lienzo, juego)
    dibujar_llave(lienzo, juego)
    mostrar(ventana, lienzo)
