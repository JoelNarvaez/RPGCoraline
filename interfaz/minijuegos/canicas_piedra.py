"""Minijuego "canicas_piedra": encontrar con la piedra la canica que guarda un alma.

Pixel art dibujado con código, con la misma técnica que los fondos de las
escenas (lienzo de 640x360 escalado x2, capa fija + lo que se mueve).
Se ve desde arriba el tapete de colores del otro cuarto (otro_cuarto.py), con
la caja de juguetes volteada y todo regado. Está casi a oscuras.

El mouse es la piedra con agujero: solo por el agujero se ve con luz, y solo
ahí la canica del alma (gris y aburrida) arde roja como una brasa. Las demás
canicas son bonitas pero no son nada: cada clic en una falsa quita segundos
y la deja tachada.

En el nodo:
  "tipo": "canicas_piedra"
  "instruccion": texto que se muestra antes de empezar
  "tiempo": segundos
  "senuelos": cuántas canicas falsas hay

Responsable: Persona A
"""

import math
import random

import pygame

import config
from interfaz.fondos.pintura import ANCHO, ALTO
from interfaz.fondos.pintura import mezclar, brillo, orillas_oscuras, mostrar, COLOR_CONTORNO
from interfaz.fondos import piedra

ESCALA: int = config.ANCHO // ANCHO       # 2

RADIO_AGUJERO: int = 40                   # lo que se ve por la piedra (en pixeles del lienzo)
BORDE_PIEDRA: int = 24                    # cuanta piedra hay alrededor del agujero
LARGO_CORDON: int = 200                   # el cordon sube hasta salirse de la pantalla
COLOR_PIEDRA_OSCURA: tuple = (190, 190, 200, 255)
RADIO_CLIC: int = 8
CASTIGO_SEGUNDOS: float = 3.0
SEPARACION: int = 28                      # distancia minima entre canicas

CENTRO_TAPETE: tuple = (340, 196)
CAJA: pygame.Rect = pygame.Rect(46, 30, 92, 62)
ZONA: pygame.Rect = pygame.Rect(40, 40, ANCHO - 80, ALTO - 70)   # donde pueden caer las canicas

COLORES_CANICA: list = [(110, 170, 230), (230, 120, 160), (240, 200, 80), (120, 200, 140),
                        (200, 140, 230), (90, 200, 210), (240, 150, 90), (250, 250, 250)]
COLOR_OSCURO: tuple = (46, 42, 70)        # el tinte de la oscuridad (se multiplica)

CAPAS: dict = {}


# ------------------------------------------------------------ parte fija

def dibujar_piso(lienzo: pygame.Surface) -> None:
    """Tablas de madera vistas desde arriba y el tapete redondo de colores."""
    lienzo.fill((120, 82, 60))
    for x in range(0, ANCHO, 20):
        pygame.draw.line(lienzo, (96, 64, 48), (x, 0), (x, ALTO))
        for y in range((x * 7) % 90, ALTO, 90):
            pygame.draw.line(lienzo, (96, 64, 48), (x, y), (x + 19, y))
        pygame.draw.line(lienzo, (140, 98, 72), (x + 6, (x * 3) % 60), (x + 6, (x * 3) % 60 + 20))

    for i, color in enumerate([(220, 90, 90), (240, 200, 90), (90, 170, 120), (90, 130, 210)]):
        radio_x: int = 236 - i * 46
        radio_y: int = 140 - i * 28
        pygame.draw.ellipse(lienzo, color, (CENTRO_TAPETE[0] - radio_x, CENTRO_TAPETE[1] - radio_y, radio_x * 2, radio_y * 2))
        pygame.draw.ellipse(lienzo, mezclar(color, (0, 0, 0), 0.2),
                            (CENTRO_TAPETE[0] - radio_x, CENTRO_TAPETE[1] - radio_y, radio_x * 2, radio_y * 2), 2)


def dibujar_juguetes(lienzo: pygame.Surface) -> None:
    """La caja volteada en una esquina y los juguetes regados (siempre en el mismo lugar)."""
    # CAJA DE JUGUETES VOLTEADA, CON LA TAPA ABIERTA
    pygame.draw.rect(lienzo, (150, 70, 50), CAJA)
    pygame.draw.rect(lienzo, (100, 46, 34), CAJA.inflate(-12, -12))
    pygame.draw.rect(lienzo, COLOR_CONTORNO, CAJA, 1)
    pygame.draw.polygon(lienzo, (170, 84, 60), [CAJA.bottomleft, CAJA.bottomright, (CAJA.right + 8, CAJA.bottom + 22), (CAJA.x - 4, CAJA.bottom + 22)])
    pygame.draw.rect(lienzo, (230, 190, 70), (CAJA.centerx - 4, CAJA.bottom + 8, 8, 6))

    # CUBOS DE COLORES
    for x, y, color in [(170, 70, (240, 200, 60)), (190, 96, (80, 170, 90)), (520, 290, (220, 90, 140)), (96, 250, (240, 200, 60))]:
        pygame.draw.rect(lienzo, color, (x, y, 12, 12))
        pygame.draw.rect(lienzo, COLOR_CONTORNO, (x, y, 12, 12), 1)
        pygame.draw.line(lienzo, mezclar(color, (255, 255, 255), 0.4), (x + 2, y + 2), (x + 8, y + 2))

    # SOLDADITOS TIRADOS
    for x, y in [(230, 140), (420, 96), (470, 250), (150, 300)]:
        pygame.draw.rect(lienzo, (200, 40, 40), (x, y, 12, 4))
        pygame.draw.rect(lienzo, (30, 30, 50), (x - 4, y, 4, 4))
        pygame.draw.rect(lienzo, COLOR_CONTORNO, (x - 4, y - 1, 16, 6), 1)

    # PELOTA, TREN, LIBRO Y EL ROBOTITO ACOSTADO
    pygame.draw.circle(lienzo, COLOR_CONTORNO, (580, 80), 13)
    pygame.draw.circle(lienzo, (220, 60, 60), (580, 80), 12)
    pygame.draw.line(lienzo, (250, 250, 250), (568, 80), (592, 80), 3)

    pygame.draw.rect(lienzo, COLOR_CONTORNO, (299, 299, 42, 18))
    pygame.draw.rect(lienzo, (60, 120, 200), (300, 300, 24, 16))
    pygame.draw.rect(lienzo, (240, 200, 60), (324, 304, 16, 12))
    for x in [306, 318, 332]:
        pygame.draw.circle(lienzo, (30, 30, 40), (x, 318), 3)

    pygame.draw.rect(lienzo, COLOR_CONTORNO, (559, 199, 30, 22))
    pygame.draw.rect(lienzo, (90, 60, 120), (560, 200, 28, 20))
    pygame.draw.line(lienzo, (240, 230, 200), (574, 201), (574, 219))

    pygame.draw.rect(lienzo, (180, 186, 196), (250, 230, 16, 10))
    pygame.draw.rect(lienzo, (160, 166, 176), (266, 231, 8, 8))
    pygame.draw.rect(lienzo, (230, 60, 60), (270, 233, 2, 1))


def crear_capas() -> None:
    """La version con luz (lo que se ve por la piedra) y la version a oscuras."""
    claro: pygame.Surface = pygame.Surface((ANCHO, ALTO))
    dibujar_piso(claro)
    dibujar_juguetes(claro)
    brillo(claro, (340, 120), 260, (255, 220, 170), 40)
    CAPAS["claro"] = claro

    oscuro: pygame.Surface = claro.copy()
    tinte: pygame.Surface = pygame.Surface((ANCHO, ALTO))
    tinte.fill(COLOR_OSCURO)
    oscuro.blit(tinte, (0, 0), special_flags=pygame.BLEND_MULT)
    orillas_oscuras(oscuro)
    CAPAS["oscuro"] = oscuro

    # MASCARA REDONDA DEL AGUJERO Y LA PIEDRA QUE LO RODEA
    mascara: pygame.Surface = pygame.Surface((RADIO_AGUJERO * 2, RADIO_AGUJERO * 2), pygame.SRCALPHA)
    pygame.draw.circle(mascara, (255, 255, 255, 255), (RADIO_AGUJERO, RADIO_AGUJERO), RADIO_AGUJERO)
    CAPAS["mascara"] = mascara

    # LA PIEDRA VERDE DE TRES ESQUINAS (piedra.py), UN POCO APAGADA PORQUE ESTA A OSCURAS
    roca: pygame.Surface = piedra.sprite_piedra(RADIO_AGUJERO, BORDE_PIEDRA).copy()
    roca.fill(COLOR_PIEDRA_OSCURA, special_flags=pygame.BLEND_RGBA_MULT)
    CAPAS["piedra"] = roca


# ------------------------------------------------------------ el juego

def acomodar_canicas(cuantas: int) -> list:
    """Lugares al azar para las canicas, sin encimarse entre ellas ni caer en la caja."""
    lugares: list = []
    intentos: int = 0
    while len(lugares) < cuantas and intentos < 2000:
        intentos = intentos + 1
        punto: tuple = (random.randint(ZONA.x, ZONA.right), random.randint(ZONA.y, ZONA.bottom))
        if CAJA.inflate(20, 50).collidepoint(punto):
            continue
        lejos: bool = True
        for otro in lugares:
            if math.dist(punto, otro) < SEPARACION:
                lejos = False
        if lejos:
            lugares.append(punto)
    return lugares


def iniciar(datos: dict) -> dict:
    if "claro" not in CAPAS:
        crear_capas()
    lugares: list = acomodar_canicas(datos.get("senuelos", 8) + 1)
    raton: tuple = pygame.mouse.get_pos()
    return {
        "real": lugares[0],
        "senuelos": lugares[1:],
        "tachadas": [],
        "mouse": (raton[0] // ESCALA, raton[1] // ESCALA),
        "castigo": 0.0,              # cuanto falta para que se borre el "-3"
        "lugar_castigo": (0, 0),
        "reloj": 0.0,
        "tiempo_total": float(datos["tiempo"]),
        "tiempo_restante": float(datos["tiempo"]),
        "resultado": "",
    }


def manejar_evento(evento: pygame.event.Event, juego: dict) -> None:
    if evento.type == pygame.MOUSEMOTION:
        juego["mouse"] = (evento.pos[0] // ESCALA, evento.pos[1] // ESCALA)

    if evento.type != pygame.MOUSEBUTTONDOWN or evento.button != 1 or juego["resultado"] != "":
        return

    punto: tuple = (evento.pos[0] // ESCALA, evento.pos[1] // ESCALA)
    if math.dist(punto, juego["real"]) < RADIO_CLIC:
        juego["resultado"] = "exito"
        return

    for canica in juego["senuelos"]:
        if math.dist(punto, canica) < RADIO_CLIC and canica not in juego["tachadas"]:
            juego["tachadas"].append(canica)
            juego["tiempo_restante"] = juego["tiempo_restante"] - CASTIGO_SEGUNDOS
            juego["castigo"] = 0.8
            juego["lugar_castigo"] = canica


def actualizar(juego: dict, dt: float) -> None:
    juego["reloj"] = juego["reloj"] + dt
    juego["castigo"] = max(0.0, juego["castigo"] - dt)
    juego["tiempo_restante"] = juego["tiempo_restante"] - dt
    if juego["tiempo_restante"] <= 0 and juego["resultado"] == "":
        juego["resultado"] = "fallo"


# ------------------------------------------------------------ lo que se mueve

def dibujar_canica(lienzo: pygame.Surface, x: int, y: int, color: tuple, tachada: bool) -> None:
    """Canica de vidrio con su remolino. Las tachadas quedan opacas con una rayita."""
    pygame.draw.circle(lienzo, COLOR_CONTORNO, (x, y), 6)
    if tachada:
        pygame.draw.circle(lienzo, (90, 86, 96), (x, y), 5)
        pygame.draw.line(lienzo, COLOR_CONTORNO, (x - 4, y - 4), (x + 4, y + 4), 2)
        return
    pygame.draw.circle(lienzo, (226, 232, 240), (x, y), 5)
    pygame.draw.line(lienzo, color, (x - 3, y + 2), (x + 3, y - 2), 2)
    pygame.draw.line(lienzo, color, (x - 2, y - 1), (x + 1, y + 2))
    lienzo.set_at((x - 2, y - 3), (255, 255, 255))
    lienzo.set_at((x - 1, y - 3), (255, 255, 255))


def dibujar_canica_gris(lienzo: pygame.Surface, x: int, y: int) -> None:
    """La canica del alma, como se ve sin la piedra: gris y aburrida."""
    pygame.draw.circle(lienzo, COLOR_CONTORNO, (x, y), 6)
    pygame.draw.circle(lienzo, (84, 82, 96), (x, y), 5)
    lienzo.set_at((x - 2, y - 2), (130, 128, 140))


def dibujar_brasa(lienzo: pygame.Surface, x: int, y: int, reloj: float) -> None:
    """Por la piedra, la canica gris arde roja como carbón soplado."""
    luz: float = (math.sin(reloj * 4) + 1) / 2
    capa: pygame.Surface = pygame.Surface((40, 40), pygame.SRCALPHA)
    pygame.draw.circle(capa, (255, 80, 30, int(40 + luz * 50)), (20, 20), 16)
    pygame.draw.circle(capa, (255, 130, 40, int(70 + luz * 70)), (20, 20), 10)
    lienzo.blit(capa, (x - 20, y - 20))
    pygame.draw.circle(lienzo, COLOR_CONTORNO, (x, y), 6)
    pygame.draw.circle(lienzo, (230, int(60 + luz * 90), 30), (x, y), 5)
    pygame.draw.circle(lienzo, (255, 220, 140), (x - 1, y - 1), 2)


def dibujar_todas(lienzo: pygame.Surface, juego: dict, con_luz: bool) -> None:
    """Las canicas sobre una de las dos capas. Sin luz todas se ven iguales de apagadas."""
    for i in range(len(juego["senuelos"])):
        x, y = juego["senuelos"][i]
        tachada: bool = juego["senuelos"][i] in juego["tachadas"]
        if con_luz:
            dibujar_canica(lienzo, x, y, COLORES_CANICA[i % len(COLORES_CANICA)], tachada)
        else:
            dibujar_canica_gris(lienzo, x, y)
    x, y = juego["real"]
    if con_luz:
        dibujar_brasa(lienzo, x, y, juego["reloj"])
    else:
        dibujar_canica_gris(lienzo, x, y)


def dibujar(ventana: pygame.Surface, juego: dict, fuentes: dict) -> None:
    lienzo: pygame.Surface = CAPAS["oscuro"].copy()
    dibujar_todas(lienzo, juego, False)

    # LO QUE SE VE POR EL AGUJERO: LA CAPA CON LUZ, RECORTADA EN CIRCULO
    claro: pygame.Surface = CAPAS["claro"].copy()
    dibujar_todas(claro, juego, True)

    x, y = juego["mouse"]
    vista: pygame.Surface = pygame.Surface((RADIO_AGUJERO * 2, RADIO_AGUJERO * 2), pygame.SRCALPHA)
    vista.blit(claro, (RADIO_AGUJERO - x, RADIO_AGUJERO - y))
    vista.blit(CAPAS["mascara"], (0, 0), special_flags=pygame.BLEND_RGBA_MULT)
    lienzo.blit(vista, (x - RADIO_AGUJERO, y - RADIO_AGUJERO))

    roca: pygame.Surface = CAPAS["piedra"]
    lienzo.blit(roca, (x - roca.get_width() // 2, y - roca.get_height() // 2))
    piedra.dibujar_cordon(lienzo, x, y, RADIO_AGUJERO, LARGO_CORDON)

    mostrar(ventana, lienzo)

    # "-3" QUE SUBE DESDE LA CANICA FALSA
    if juego["castigo"] > 0:
        cx, cy = juego["lugar_castigo"]
        sube: int = int((0.8 - juego["castigo"]) * 40)
        texto: pygame.Surface = fuentes["opcion"].render("-" + str(int(CASTIGO_SEGUNDOS)) + " s", True, config.COLOR_FINAL_MALO)
        ventana.blit(texto, (cx * ESCALA - texto.get_width() // 2, cy * ESCALA - 40 - sube))
