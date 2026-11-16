"""Minijuego "taza_te": encontrar los grumos de hojas de té en el fondo de la taza.

La taza se ve desde arriba, en pixel art dibujado con código (lienzo de
640x360 escalado x2, igual que los fondos de las escenas).
El té da vueltas y los grumos giran con él; además cada grumo se mece por
su cuenta, así que hay que atinarle. Al encontrar uno se queda quieto. Hay motitas sueltas
que NO cuentan, para que haya que fijarse. Al encontrar los 9 grumos se unen
con líneas y forman la figura que ve la señorita Forcible: una mano de dedos
largos (el peligro que viene).

En el nodo:
  "tipo": "taza_te"
  "instruccion": texto que se muestra antes de empezar
  "tiempo": segundos

Responsable: Persona A
"""

import math
import random

import pygame

import config
from interfaz.fondos.pintura import ANCHO, ALTO
from interfaz.fondos.pintura import mezclar, degradado, brillo, orillas_oscuras, mostrar

ESCALA: int = config.ANCHO // ANCHO       # 2

CENTRO: tuple = (320, 176)                # centro de la taza en el lienzo
RADIO_TAZA: int = 120
RADIO_TE: int = 106
RADIO_CLIC: int = 13                      # que tan cerca hay que dar el clic (en el lienzo)
VUELTA: float = 0.8                       # que tan rapido gira el te (radianes por segundo)
BAMBOLEO: int = 10                        # cuanto se mece cada grumo por su cuenta (en el lienzo)

# GRUMOS DE HOJAS: FORMAN UNA MANO (4 EN LA PALMA, 5 PUNTAS DE DEDO).
# POSICIONES RELATIVAS AL CENTRO DE LA TAZA.
GRUMOS: list = [
    (-8, 34), (18, 32), (-4, 58), (20, 56),                     # palma
    (-58, -26), (-30, -62), (2, -76), (32, -62), (56, 14),      # puntas de los dedos
]
NUDILLOS: list = [(-8, 32), (1, 31), (10, 31), (18, 31), (20, 44)]   # de donde sale cada dedo (el ultimo es el pulgar)

COLOR_MANTEL: tuple = (206, 150, 160)
COLOR_PORCELANA: tuple = (244, 240, 230)
COLOR_TE: tuple = (190, 128, 70)
COLOR_GRUMO: tuple = (60, 36, 22)
COLOR_ENCONTRADO: tuple = (240, 200, 90)
COLOR_FIGURA: tuple = (176, 110, 226)
COLOR_FIGURA_OSCURO: tuple = (60, 20, 80)

CAPAS: dict = {}


# ------------------------------------------------------------ parte fija

def dibujar_mesa(lienzo: pygame.Surface) -> None:
    """Mantel rosa con florecitas, el plato de galletas y la tetera vistos desde arriba."""
    lienzo.fill(COLOR_MANTEL)
    for y in range(10, ALTO, 24):
        for x in range(8 + (y // 24 % 2) * 12, ANCHO, 24):
            pygame.draw.circle(lienzo, mezclar(COLOR_MANTEL, (255, 255, 255), 0.35), (x, y), 2)

    # PLATO CON GALLETAS DURAS (ABAJO A LA IZQUIERDA)
    pygame.draw.circle(lienzo, COLOR_PORCELANA, (96, 290), 52)
    pygame.draw.circle(lienzo, (210, 206, 196), (96, 290), 52, 2)
    for x, y in [(80, 280), (106, 272), (100, 302), (74, 304)]:
        pygame.draw.circle(lienzo, (176, 130, 76), (x, y), 12)
        pygame.draw.circle(lienzo, (150, 108, 60), (x, y), 12, 1)

    # TETERA (ARRIBA A LA DERECHA)
    pygame.draw.circle(lienzo, COLOR_PORCELANA, (560, 70), 56)
    pygame.draw.circle(lienzo, (90, 120, 170), (560, 70), 40, 3)
    pygame.draw.circle(lienzo, (230, 226, 216), (560, 70), 14)
    pygame.draw.polygon(lienzo, COLOR_PORCELANA, [(506, 84), (470, 104), (474, 112), (512, 98)])


def dibujar_taza(lienzo: pygame.Surface) -> None:
    """Platito, taza, asa y el té."""
    x, y = CENTRO

    # SOMBRA, PLATITO Y TAZA
    sombra = pygame.Surface((ANCHO, ALTO), pygame.SRCALPHA)
    pygame.draw.circle(sombra, (0, 0, 0, 60), (x + 10, y + 12), RADIO_TAZA + 34)
    lienzo.blit(sombra, (0, 0))
    pygame.draw.circle(lienzo, COLOR_PORCELANA, (x, y), RADIO_TAZA + 30)
    pygame.draw.circle(lienzo, (90, 120, 170), (x, y), RADIO_TAZA + 22, 2)

    pygame.draw.circle(lienzo, (226, 222, 212), (x + RADIO_TAZA + 4, y), 22, 9)     # asa
    pygame.draw.circle(lienzo, COLOR_PORCELANA, (x, y), RADIO_TAZA)
    pygame.draw.circle(lienzo, (90, 120, 170), (x, y), RADIO_TAZA - 4, 2)            # filito azul

    # PARED DE ADENTRO CON SOMBRA DE UN LADO
    pygame.draw.circle(lienzo, (214, 208, 196), (x, y), RADIO_TE + 6)
    pygame.draw.circle(lienzo, (232, 228, 218), (x - 4, y - 4), RADIO_TE + 3)

    # TE CLARO (YA CASI SE LO TOMARON): MAS CLARO EN EL CENTRO
    for r in range(RADIO_TE, 0, -6):
        avance = 1 - r / RADIO_TE
        pygame.draw.circle(lienzo, mezclar(COLOR_TE, (226, 176, 116), avance), (x, y), r)


def crear_fijo() -> pygame.Surface:
    lienzo = pygame.Surface((ANCHO, ALTO))
    dibujar_mesa(lienzo)
    dibujar_taza(lienzo)
    brillo(lienzo, (200, 60), 220, (255, 220, 170), 40)
    orillas_oscuras(lienzo)
    return lienzo


# ------------------------------------------------------------ el juego

def giro(tiempo: float) -> float:
    """Cuánto ha girado el té: da vueltas sin parar, a ratos más rápido."""
    return tiempo * VUELTA + math.sin(tiempo * 0.9) * 0.5


def posicion(grumo: dict, tiempo: float) -> tuple:
    """Dónde está el grumo ahorita: gira con el té y, si bambolea, además se
    mece a su propio ritmo (cada uno distinto)."""
    x: float = grumo["dx"]
    y: float = grumo["dy"]

    if grumo["bambolea"]:
        x = x + math.sin(tiempo * grumo["ritmo"] + grumo["fase"]) * BAMBOLEO
        y = y + math.cos(tiempo * grumo["ritmo"] * 0.8 + grumo["fase"]) * BAMBOLEO

    angulo: float = giro(tiempo)
    dx: float = x * math.cos(angulo) - y * math.sin(angulo)
    dy: float = x * math.sin(angulo) + y * math.cos(angulo)
    return (CENTRO[0] + int(dx), CENTRO[1] + int(dy))


def nuevo_punto(dx: int, dy: int, bambolea: bool) -> dict:
    """Un grumo o motita en el té, con su propio ritmo para mecerse."""
    return {
        "dx": dx,
        "dy": dy,
        "bambolea": bambolea,
        "ritmo": random.uniform(2.2, 3.8),
        "fase": random.uniform(0, 2 * math.pi),
    }


def iniciar(datos: dict) -> dict:
    grumos: list = []
    for dx, dy in GRUMOS:
        grumo: dict = nuevo_punto(dx, dy, True)
        grumo["encontrado"] = False
        grumo["forma"] = random.randint(0, 2)
        grumos.append(grumo)

    # MOTITAS AL AZAR DENTRO DEL TE, LEJOS DE LOS GRUMOS. ALGUNAS SON DE 2 O 3
    # PUNTITOS PARA QUE PAREZCAN GRUMOS CHIQUITOS (Y HAYA QUE FIJARSE BIEN)
    motitas: list = []
    while len(motitas) < 55:
        angulo: float = random.uniform(0, 2 * math.pi)
        distancia: float = random.uniform(0, RADIO_TE - 6 - BAMBOLEO)
        mx: int = int(math.cos(angulo) * distancia)
        my: int = int(math.sin(angulo) * distancia)
        lejos: bool = True
        for dx, dy in GRUMOS:
            if math.dist((mx, my), (dx, dy)) < 14:
                lejos = False
        if lejos:
            motita: dict = nuevo_punto(mx, my, True)
            motita["puntos"] = random.choice([1, 1, 2, 3])
            motitas.append(motita)

    if "fijo" not in CAPAS:
        CAPAS["fijo"] = crear_fijo()

    return {
        "grumos": grumos,
        "motitas": motitas,
        "encontrados": 0,
        "tiempo": 0.0,
        "tiempo_total": float(datos["tiempo"]),
        "tiempo_restante": float(datos["tiempo"]),
        "ondas": [],          # circulitos donde se dio clic: [x, y, edad]
        "resultado": "",
    }


def manejar_evento(evento: pygame.event.Event, juego: dict) -> None:
    if evento.type != pygame.MOUSEBUTTONDOWN or evento.button != 1:
        return
    x: int = evento.pos[0] // ESCALA
    y: int = evento.pos[1] // ESCALA

    if math.dist((x, y), CENTRO) < RADIO_TE:
        juego["ondas"].append([x, y, 0.0])

    for grumo in juego["grumos"]:
        if not grumo["encontrado"] and math.dist((x, y), posicion(grumo, juego["tiempo"])) < RADIO_CLIC:
            grumo["encontrado"] = True
            grumo["bambolea"] = False        # ya encontrado: se queda quieto (solo gira con el té)
            juego["encontrados"] = juego["encontrados"] + 1
            break

    if juego["encontrados"] == len(juego["grumos"]):
        juego["resultado"] = "exito"


def actualizar(juego: dict, dt: float) -> None:
    juego["tiempo"] = juego["tiempo"] + dt
    juego["tiempo_restante"] = juego["tiempo_restante"] - dt

    for onda in juego["ondas"]:
        onda[2] = onda[2] + dt
    vivas: list = []
    for onda in juego["ondas"]:
        if onda[2] < 0.6:
            vivas.append(onda)
    juego["ondas"] = vivas

    if juego["tiempo_restante"] <= 0 and juego["resultado"] == "":
        juego["resultado"] = "fallo"


# ------------------------------------------------------------ lo que se mueve

def dibujar_remolino(lienzo: pygame.Surface, tiempo: float) -> None:
    """Rayitas claras que dan vueltas en el té y un brillo que se mueve."""
    capa: pygame.Surface = pygame.Surface((ANCHO, ALTO), pygame.SRCALPHA)
    for i in range(5):
        radio: int = 24 + i * 16
        inicio: float = -giro(tiempo) * (1 - i * 0.1) + i * 1.3
        rect: pygame.Rect = pygame.Rect(0, 0, radio * 2, radio * 2)
        rect.center = CENTRO
        pygame.draw.arc(capa, (255, 236, 200, 60), rect, inicio, inicio + 0.9, 1)

    bx: int = CENTRO[0] - 40 + int(math.sin(tiempo * 0.5) * 8)
    pygame.draw.ellipse(capa, (255, 250, 236, 50), (bx, CENTRO[1] - 70, 34, 12))
    lienzo.blit(capa, (0, 0))


def dibujar_grumo(lienzo: pygame.Surface, x: int, y: int, forma: int) -> None:
    """Grumito de hojas: varias bolitas oscuras juntas, cada uno un poco distinto."""
    pygame.draw.circle(lienzo, COLOR_GRUMO, (x, y), 3)
    pygame.draw.circle(lienzo, COLOR_GRUMO, (x + 3, y - 1 + forma), 2)
    pygame.draw.circle(lienzo, COLOR_GRUMO, (x - 3, y + 2 - forma), 2)
    lienzo.set_at((x + 1 - forma, y + 4), COLOR_GRUMO)
    lienzo.set_at((x - 1, y - 1), (110, 76, 46))


def dibujar_dedo(capa: pygame.Surface, base: tuple, punta: tuple) -> None:
    """Dedo largo y flaco: contorno oscuro, relleno claro y punta redonda."""
    pygame.draw.line(capa, COLOR_FIGURA_OSCURO, base, punta, 7)
    pygame.draw.circle(capa, COLOR_FIGURA_OSCURO, punta, 3)
    pygame.draw.line(capa, COLOR_FIGURA, base, punta, 4)
    pygame.draw.circle(capa, COLOR_FIGURA, punta, 2)


def dibujar_figura(lienzo: pygame.Surface, juego: dict) -> None:
    """Al encontrar todos se ve la figura: una mano con dedos larguísimos."""
    tiempo: float = juego["tiempo"]
    capa: pygame.Surface = pygame.Surface((ANCHO, ALTO), pygame.SRCALPHA)

    # PALMA: LOS 4 PRIMEROS GRUMOS SON SUS ESQUINAS
    esquinas: list = []
    for i in [0, 1, 3, 2]:
        esquinas.append(posicion(juego["grumos"][i], tiempo))
    pygame.draw.polygon(capa, COLOR_FIGURA_OSCURO, esquinas)
    pygame.draw.polygon(capa, COLOR_FIGURA, esquinas, 2)

    # DEDOS: CADA PUNTA SALE DE SU NUDILLO
    for i in range(4, len(juego["grumos"])):
        base: tuple = posicion(nuevo_punto(NUDILLOS[i - 4][0], NUDILLOS[i - 4][1], False), tiempo)
        dibujar_dedo(capa, base, posicion(juego["grumos"][i], tiempo))

    capa.set_alpha(int(190 + math.sin(tiempo * 4) * 40))
    lienzo.blit(capa, (0, 0))


def dibujar_motitas(lienzo: pygame.Surface, juego: dict) -> None:
    """Motitas sueltas que también giran con el té (no cuentan)."""
    for motita in juego["motitas"]:
        x, y = posicion(motita, juego["tiempo"])
        lienzo.set_at((x, y), COLOR_GRUMO)
        if motita["puntos"] >= 2:
            lienzo.set_at((x + 1, y), COLOR_GRUMO)
        if motita["puntos"] == 3:
            lienzo.set_at((x, y + 1), COLOR_GRUMO)


def dibujar(ventana: pygame.Surface, juego: dict, fuentes: dict) -> None:
    lienzo: pygame.Surface = CAPAS["fijo"].copy()
    tiempo: float = juego["tiempo"]

    dibujar_remolino(lienzo, tiempo)
    dibujar_motitas(lienzo, juego)

    if juego["encontrados"] == len(juego["grumos"]):
        dibujar_figura(lienzo, juego)

    for grumo in juego["grumos"]:
        x, y = posicion(grumo, tiempo)
        dibujar_grumo(lienzo, x, y, grumo["forma"])
        if grumo["encontrado"]:
            radio: int = 8 + int(math.sin(tiempo * 5) * 1.5)
            pygame.draw.circle(lienzo, COLOR_ENCONTRADO, (x, y), radio, 1)

    for x, y, edad in juego["ondas"]:
        pygame.draw.circle(lienzo, (255, 240, 210), (x, y), 3 + int(edad * 16), 1)

    mostrar(ventana, lienzo)

    texto: str = "Hojas: " + str(juego["encontrados"]) + " / " + str(len(juego["grumos"]))
    superficie: pygame.Surface = fuentes["texto"].render(texto, True, config.COLOR_ACENTO)
    ventana.blit(superficie, (40, config.ALTO - 50))
