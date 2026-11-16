"""Minijuego de recorrer la casa: Coraline cuenta puertas y ventanas cuarto por cuarto.

Todo se dibuja en pixel art sobre un lienzo chico (320x180) que luego se
agranda 4 veces, así los pixeles se ven grandes y nítidos como en un RPG.

Cómo se juega:
- En cada cuarto hay que tocar (clic) todas sus puertas y ventanas.
- Coraline camina hasta lo que se toca.
- Al completar un cuarto aparece una flecha para pasar al siguiente.
- En el último cuarto está la puerta tallada: al tocarla se termina el recorrido.

Datos del JSON:
  "tiempo": segundos para todo el recorrido

Responsable: Persona A
"""

import math

import pygame

import config

ESCALA: int = 4
ANCHO_LIENZO: int = config.ANCHO // ESCALA    # 320
ALTO_LIENZO: int = config.ALTO // ESCALA      # 180
Y_PISO: int = 140                             # donde termina la pared y empieza el piso

VELOCIDAD_CORALINE: float = 90.0   # pixeles del lienzo por segundo
DURACION_FUNDIDO: float = 0.6      # segundos para cambiar de cuarto
ESPERA_FINAL: float = 1.6          # segundos para ver la puerta tallada antes de terminar

COLOR_MADERA_PISO: tuple = (66, 46, 36)
COLOR_TABLA: tuple = (52, 36, 28)
COLOR_MARCA: tuple = (255, 226, 120)
COLOR_LAPIZ: tuple = (40, 40, 60)

# Cada cuarto: nombre, colores, objetos que hay que encontrar y muebles de adorno.
# Los objetos son rectángulos del lienzo: (x, y, ancho, alto).
CUARTOS: list = [
    {
        "nombre": "La cocina",
        "pared": (62, 102, 108), "papel": (70, 112, 118), "zoclo": (40, 70, 76),
        "objetos": [
            {"tipo": "alacena", "rect": (52, 30, 22, 26)},
            {"tipo": "ventana", "rect": (130, 34, 44, 40)},
            {"tipo": "puerta", "rect": (238, 70, 34, 70)},
        ],
        "muebles": [("barra", 30), ("estufa", 96), ("cuadro", 200)],
    },
    {
        "nombre": "El pasillo",
        "pared": (56, 82, 106), "papel": (64, 92, 116), "zoclo": (36, 54, 74),
        "objetos": [
            {"tipo": "puerta", "rect": (40, 70, 34, 70)},
            {"tipo": "ventana", "rect": (150, 30, 34, 44)},
            {"tipo": "armario", "rect": (250, 62, 30, 78)},
        ],
        "muebles": [("alfombra", 60), ("cuadro", 96), ("cuadro", 204)],
    },
    {
        "nombre": "El cuarto de Coraline",
        "pared": (86, 76, 116), "papel": (96, 86, 128), "zoclo": (58, 50, 82),
        "objetos": [
            {"tipo": "puerta", "rect": (20, 70, 34, 70)},
            {"tipo": "ventana", "rect": (120, 32, 40, 40)},
        ],
        "muebles": [("cama", 120), ("lampara", 230)],
    },
    {
        # Última escena: pared lisa y solo la puerta pequeña sellada, sin distractores
        "nombre": "El salón",
        "liso": True,
        "pared": (52, 112, 116), "papel": (52, 112, 116), "zoclo": (34, 78, 82),
        "objetos": [
            {"tipo": "tallada", "rect": (204, 88, 40, 52)},
        ],
        "muebles": [],
    },
]


# ------------------------------------------------------------ Datos del juego

def contar(tipos: list) -> int:
    """Cuántos objetos de esos tipos hay en toda la casa."""
    total: int = 0
    for cuarto in CUARTOS:
        for objeto in cuarto["objetos"]:
            if objeto["tipo"] in tipos:
                total = total + 1
    return total


TIPOS_PUERTA: list = ["puerta", "alacena", "armario", "tallada"]


def iniciar(datos: dict) -> dict:
    encontrados: list = []
    for cuarto in CUARTOS:
        encontrados.append([False] * len(cuarto["objetos"]))
    juego: dict = {
        "cuarto": 0,
        "encontrados": encontrados,
        "puertas": 0,
        "ventanas": 0,
        "total_puertas": contar(TIPOS_PUERTA),
        "total_ventanas": contar(["ventana"]),
        "coraline_x": 150.0,
        "destino_x": 150.0,
        "mira_derecha": True,
        "reloj": 0.0,               # tiempo de las animaciones (lluvia, flecha, pasos)
        "fundido": 0.0,             # > 0 mientras se cambia de cuarto
        "temblor": 0.0,             # > 0 mientras tiembla la puerta tallada
        "escribiendo": 0.0,         # > 0 mientras Coraline anota en la libreta
        "anotar_al_llegar": False,  # True cuando tocó algo y va caminando hacia allá
        "espera_final": 0.0,        # > 0 cuando ya se tocó la puerta tallada
        "avisos": [],               # textos flotantes: {"texto", "x", "y", "vida"}
        "lienzo": pygame.Surface((ANCHO_LIENZO, ALTO_LIENZO)),
        "tiempo_total": float(datos["tiempo"]),
        "tiempo_restante": float(datos["tiempo"]),
        "resultado": "",
    }
    return juego


def cuarto_completo(juego: dict) -> bool:
    for encontrado in juego["encontrados"][juego["cuarto"]]:
        if not encontrado:
            return False
    return True


def es_ultimo_cuarto(juego: dict) -> bool:
    return juego["cuarto"] == len(CUARTOS) - 1


def rect_flecha() -> pygame.Rect:
    return pygame.Rect(ANCHO_LIENZO - 30, Y_PISO + 8, 24, 22)


# ------------------------------------------------------------ Eventos

def tocar_objeto(juego: dict, indice: int) -> None:
    """Marca un objeto como encontrado y manda a Coraline hacia él."""
    cuarto: dict = CUARTOS[juego["cuarto"]]
    objeto: dict = cuarto["objetos"][indice]
    juego["encontrados"][juego["cuarto"]][indice] = True

    x, y, ancho, alto = objeto["rect"]
    juego["destino_x"] = float(x + ancho // 2)
    juego["anotar_al_llegar"] = True

    if objeto["tipo"] == "ventana":
        juego["ventanas"] = juego["ventanas"] + 1
        texto: str = "+1 ventana"
    else:
        juego["puertas"] = juego["puertas"] + 1
        texto = "+1 puerta"

    if objeto["tipo"] == "tallada":
        juego["temblor"] = 0.5
        texto = "Cerrada con llave..."

    juego["avisos"].append({"texto": texto, "x": x + ancho // 2, "y": y - 4, "vida": 1.2})


def manejar_evento(evento: pygame.event.Event, juego: dict) -> None:
    if juego["fundido"] > 0 or juego["espera_final"] > 0:
        return

    quiere_avanzar: bool = evento.type == pygame.KEYDOWN and evento.key in [pygame.K_RIGHT, pygame.K_SPACE]

    if evento.type == pygame.MOUSEBUTTONDOWN and evento.button == 1:
        x: int = evento.pos[0] // ESCALA
        y: int = evento.pos[1] // ESCALA

        if cuarto_completo(juego) and rect_flecha().collidepoint(x, y):
            quiere_avanzar = True
        else:
            cuarto: dict = CUARTOS[juego["cuarto"]]
            for i in range(len(cuarto["objetos"])):
                rect: pygame.Rect = pygame.Rect(cuarto["objetos"][i]["rect"])
                if rect.collidepoint(x, y) and not juego["encontrados"][juego["cuarto"]][i]:
                    tocar_objeto(juego, i)
                    return
            # Si no tocó nada, Coraline camina hacia allá
            if y >= Y_PISO:
                juego["destino_x"] = float(x)

    if quiere_avanzar and cuarto_completo(juego) and not es_ultimo_cuarto(juego):
        juego["fundido"] = DURACION_FUNDIDO


def actualizar(juego: dict, dt: float) -> None:
    juego["reloj"] = juego["reloj"] + dt
    juego["tiempo_restante"] = juego["tiempo_restante"] - dt

    # Coraline camina hacia su destino
    distancia: float = juego["destino_x"] - juego["coraline_x"]
    paso: float = VELOCIDAD_CORALINE * dt
    if abs(distancia) <= paso:
        juego["coraline_x"] = juego["destino_x"]
    else:
        if distancia > 0:
            juego["coraline_x"] = juego["coraline_x"] + paso
            juego["mira_derecha"] = True
        else:
            juego["coraline_x"] = juego["coraline_x"] - paso
            juego["mira_derecha"] = False

    # Cambio de cuarto: a la mitad del fundido se cambia el cuarto
    if juego["fundido"] > 0:
        antes: float = juego["fundido"]
        juego["fundido"] = juego["fundido"] - dt
        mitad: float = DURACION_FUNDIDO / 2
        if antes > mitad and juego["fundido"] <= mitad:
            juego["cuarto"] = juego["cuarto"] + 1
            juego["coraline_x"] = 20.0
            juego["destino_x"] = 60.0
            juego["avisos"] = []

    if juego["temblor"] > 0:
        juego["temblor"] = juego["temblor"] - dt

    # Al llegar a lo que tocó, anota en la libreta
    if juego["anotar_al_llegar"] and juego["coraline_x"] == juego["destino_x"]:
        juego["anotar_al_llegar"] = False
        juego["escribiendo"] = 0.8
    if juego["escribiendo"] > 0:
        juego["escribiendo"] = juego["escribiendo"] - dt

    vivos: list = []
    for aviso in juego["avisos"]:
        aviso["vida"] = aviso["vida"] - dt
        aviso["y"] = aviso["y"] - 12 * dt
        if aviso["vida"] > 0:
            vivos.append(aviso)
    juego["avisos"] = vivos

    # Fin: todo encontrado en el último cuarto
    if es_ultimo_cuarto(juego) and cuarto_completo(juego) and juego["espera_final"] <= 0:
        juego["espera_final"] = ESPERA_FINAL
    elif juego["espera_final"] > 0:
        juego["espera_final"] = juego["espera_final"] - dt
        if juego["espera_final"] <= 0:
            juego["resultado"] = "exito"
            return

    if juego["tiempo_restante"] <= 0 and juego["espera_final"] <= 0:
        juego["resultado"] = "fallo"


# ------------------------------------------------------------ Dibujo del cuarto

def mezclar(color: tuple, otro: tuple, cuanto: float) -> tuple:
    """Color intermedio entre dos colores (cuanto = 0 es el primero, 1 el segundo)."""
    return (int(color[0] + (otro[0] - color[0]) * cuanto),
            int(color[1] + (otro[1] - color[1]) * cuanto),
            int(color[2] + (otro[2] - color[2]) * cuanto))


def dibujar_salon_liso(lienzo: pygame.Surface, cuarto: dict) -> None:
    """Pared lisa en degradado, zoclo sencillo y piso oscuro. Nada que distraiga."""
    for y in range(Y_PISO):
        cuanto: float = y / Y_PISO
        color: tuple = mezclar(mezclar(cuarto["pared"], (0, 0, 0), 0.45), cuarto["pared"], cuanto)
        pygame.draw.line(lienzo, color, (0, y), (ANCHO_LIENZO, y))

    # Zoclo
    pygame.draw.rect(lienzo, cuarto["zoclo"], (0, Y_PISO - 6, ANCHO_LIENZO, 6))
    pygame.draw.line(lienzo, mezclar(cuarto["pared"], (255, 255, 255), 0.12), (0, Y_PISO - 7), (ANCHO_LIENZO, Y_PISO - 7))

    # Piso oscuro verde azulado con tablas apenas marcadas
    for y in range(Y_PISO, ALTO_LIENZO):
        cuanto = (y - Y_PISO) / (ALTO_LIENZO - Y_PISO)
        pygame.draw.line(lienzo, mezclar((30, 56, 62), (12, 24, 30), cuanto), (0, y), (ANCHO_LIENZO, y))
    for fila in range(4):
        y = Y_PISO + 5 + fila * 9
        pygame.draw.line(lienzo, (22, 42, 48), (0, y), (ANCHO_LIENZO, y))


def dibujar_paredes(lienzo: pygame.Surface, cuarto: dict) -> None:
    if cuarto.get("liso", False):
        dibujar_salon_liso(lienzo, cuarto)
        return

    lienzo.fill(cuarto["pared"])

    # Papel tapiz: rombos pequeños
    for y in range(18, Y_PISO - 30, 10):
        desfase: int = 5 if (y // 10) % 2 == 0 else 0
        for x in range(desfase, ANCHO_LIENZO, 10):
            pygame.draw.polygon(lienzo, cuarto["papel"], [(x, y - 2), (x + 2, y), (x, y + 2), (x - 2, y)])

    # Moldura del techo con sombra
    pygame.draw.rect(lienzo, mezclar(cuarto["zoclo"], (0, 0, 0), 0.4), (0, 0, ANCHO_LIENZO, 12))
    pygame.draw.rect(lienzo, cuarto["zoclo"], (0, 12, ANCHO_LIENZO, 3))

    # Lambrín (parte baja de la pared) con tablas verticales
    pygame.draw.rect(lienzo, cuarto["zoclo"], (0, Y_PISO - 30, ANCHO_LIENZO, 30))
    pygame.draw.rect(lienzo, mezclar(cuarto["zoclo"], (255, 255, 255), 0.15), (0, Y_PISO - 31, ANCHO_LIENZO, 2))
    for x in range(0, ANCHO_LIENZO, 16):
        pygame.draw.line(lienzo, mezclar(cuarto["zoclo"], (0, 0, 0), 0.25), (x, Y_PISO - 28), (x, Y_PISO - 2))

    # Piso de tablas
    pygame.draw.rect(lienzo, COLOR_MADERA_PISO, (0, Y_PISO, ANCHO_LIENZO, ALTO_LIENZO - Y_PISO))
    pygame.draw.rect(lienzo, (34, 24, 20), (0, Y_PISO, ANCHO_LIENZO, 2))
    for fila in range(4):
        y: int = Y_PISO + 4 + fila * 10
        pygame.draw.line(lienzo, COLOR_TABLA, (0, y), (ANCHO_LIENZO, y))
        desfase = 0 if fila % 2 == 0 else 24
        for x in range(desfase, ANCHO_LIENZO, 48):
            pygame.draw.line(lienzo, COLOR_TABLA, (x, y), (x, y + 10))


def dibujar_lluvia(lienzo: pygame.Surface, rect: pygame.Rect, reloj: float) -> None:
    """Gotas que caen dentro de una ventana."""
    for i in range(6):
        x: int = rect.x + 3 + (i * 7) % max(rect.width - 6, 1)
        y: int = rect.y + int((reloj * 60 + i * 13) % rect.height)
        pygame.draw.line(lienzo, (150, 180, 210), (x, y), (x - 1, min(y + 3, rect.bottom - 1)))


def dibujar_ventana(lienzo: pygame.Surface, rect: pygame.Rect, reloj: float) -> None:
    pygame.draw.rect(lienzo, (230, 222, 205), rect.inflate(6, 6))          # marco
    pygame.draw.rect(lienzo, (24, 34, 58), rect)                           # noche lluviosa
    pygame.draw.rect(lienzo, (34, 48, 78), (rect.x, rect.y, rect.width, rect.height // 2))
    dibujar_lluvia(lienzo, rect, reloj)
    pygame.draw.line(lienzo, (230, 222, 205), (rect.centerx, rect.y), (rect.centerx, rect.bottom - 1), 2)
    pygame.draw.line(lienzo, (230, 222, 205), (rect.x, rect.centery), (rect.right - 1, rect.centery), 2)
    pygame.draw.rect(lienzo, (200, 190, 172), (rect.x - 5, rect.bottom + 3, rect.width + 10, 3))  # repisa


def dibujar_puerta(lienzo: pygame.Surface, rect: pygame.Rect, color: tuple) -> None:
    oscuro: tuple = mezclar(color, (0, 0, 0), 0.35)
    claro: tuple = mezclar(color, (255, 255, 255), 0.15)
    pygame.draw.rect(lienzo, (226, 218, 200), rect.inflate(6, 4).move(0, -2))   # marco
    pygame.draw.rect(lienzo, color, rect)
    # Dos tableros tallados
    alto_tablero: int = rect.height // 2 - 8
    for y in [rect.y + 5, rect.y + rect.height // 2 + 3]:
        tablero: pygame.Rect = pygame.Rect(rect.x + 5, y, rect.width - 10, alto_tablero)
        pygame.draw.rect(lienzo, oscuro, tablero, 1)
        pygame.draw.line(lienzo, claro, tablero.bottomleft, tablero.bottomright)
    pygame.draw.rect(lienzo, (210, 170, 70), (rect.right - 7, rect.centery, 3, 3))   # manija


def dibujar_tallada(lienzo: pygame.Surface, rect: pygame.Rect, temblor: float) -> None:
    """La puerta pequeña del salón: madera gris oscura con un tablero en arco, cerrada."""
    if temblor > 0:
        rect = rect.move(int(math.sin(temblor * 60) * 2), 0)
    madera: tuple = (86, 76, 74)
    clara: tuple = (108, 98, 94)
    oscura: tuple = (50, 44, 44)

    # Marco hundido en la pared y sombra en el piso
    pygame.draw.rect(lienzo, (20, 40, 44), rect.inflate(6, 4).move(0, -2))
    pygame.draw.rect(lienzo, (14, 26, 30), (rect.x - 2, rect.bottom, rect.width + 8, 3))

    # Hoja de la puerta con un poco de volumen
    pygame.draw.rect(lienzo, madera, rect)
    pygame.draw.line(lienzo, clara, (rect.x + 1, rect.y + 1), (rect.x + 1, rect.bottom - 2))
    pygame.draw.line(lienzo, oscura, (rect.right - 2, rect.y + 1), (rect.right - 2, rect.bottom - 1))

    # Tablero en arco
    tablero: pygame.Rect = pygame.Rect(rect.x + 9, rect.y + 7, rect.width - 18, rect.height - 16)
    pygame.draw.rect(lienzo, oscura, tablero, 1, border_top_left_radius=10, border_top_right_radius=10)
    pygame.draw.rect(lienzo, clara, tablero.inflate(-4, -4), 1, border_top_left_radius=8,
                     border_top_right_radius=8)

    # Manija y cerradura a la izquierda
    pygame.draw.rect(lienzo, (36, 32, 32), (rect.x + 3, rect.centery - 1, 4, 3))
    pygame.draw.rect(lienzo, (150, 130, 90), (rect.x + 4, rect.centery - 1, 2, 2))
    pygame.draw.rect(lienzo, (12, 10, 10), (rect.x + 5, rect.centery + 4, 1, 3))


def dibujar_objeto(lienzo: pygame.Surface, objeto: dict, juego: dict) -> None:
    rect: pygame.Rect = pygame.Rect(objeto["rect"])
    tipo: str = objeto["tipo"]
    if tipo == "ventana":
        dibujar_ventana(lienzo, rect, juego["reloj"])
    elif tipo == "puerta":
        dibujar_puerta(lienzo, rect, (120, 82, 58))
    elif tipo == "armario":
        dibujar_puerta(lienzo, rect, (138, 104, 76))
    elif tipo == "alacena":
        dibujar_puerta(lienzo, rect, (176, 150, 112))
    elif tipo == "tallada":
        dibujar_tallada(lienzo, rect, juego["temblor"])


def dibujar_mueble(lienzo: pygame.Surface, nombre: str, x: int, reloj: float) -> None:
    piso: int = Y_PISO
    if nombre == "barra":
        pygame.draw.rect(lienzo, (150, 120, 92), (x, piso - 30, 70, 30))
        pygame.draw.rect(lienzo, (210, 200, 180), (x - 2, piso - 33, 74, 4))
        for i in range(3):
            pygame.draw.rect(lienzo, (120, 92, 70), (x + 4 + i * 23, piso - 26, 19, 22), 1)
    elif nombre == "estufa":
        pygame.draw.rect(lienzo, (200, 204, 206), (x, piso - 32, 26, 32))
        pygame.draw.rect(lienzo, (40, 40, 46), (x + 3, piso - 22, 20, 16))
        pygame.draw.rect(lienzo, (230, 120, 60), (x + 4, piso - 36, 6, 2))
        pygame.draw.rect(lienzo, (230, 120, 60), (x + 15, piso - 36, 6, 2))
    elif nombre == "cuadro":
        pygame.draw.rect(lienzo, (176, 140, 70), (x, 40, 22, 18))
        pygame.draw.rect(lienzo, (80, 110, 90), (x + 2, 42, 18, 14))
        pygame.draw.polygon(lienzo, (60, 80, 70), [(x + 3, 55), (x + 10, 46), (x + 18, 55)])
    elif nombre == "alfombra":
        pygame.draw.rect(lienzo, (120, 50, 60), (x, piso + 8, 150, 12))
        pygame.draw.rect(lienzo, (170, 120, 70), (x + 3, piso + 10, 144, 8), 1)
    elif nombre == "cama":
        pygame.draw.rect(lienzo, (90, 60, 44), (x, piso - 26, 6, 26))
        pygame.draw.rect(lienzo, (90, 60, 44), (x + 74, piso - 18, 6, 18))
        pygame.draw.rect(lienzo, (70, 90, 150), (x + 6, piso - 16, 68, 10))
        pygame.draw.rect(lienzo, (230, 225, 210), (x + 8, piso - 22, 16, 6))
    elif nombre == "lampara":
        # Luz cálida en capas: más fuerte en el centro
        brillo: pygame.Surface = pygame.Surface((70, 70), pygame.SRCALPHA)
        intensidad: int = 16 + int(math.sin(reloj * 3) * 3)
        for radio in [34, 26, 18, 10]:
            capa: pygame.Surface = pygame.Surface((70, 70), pygame.SRCALPHA)
            pygame.draw.circle(capa, (255, 208, 130, intensidad), (35, 35), radio)
            brillo.blit(capa, (0, 0))
        lienzo.blit(brillo, (x - 35, piso - 84))
        pygame.draw.line(lienzo, (40, 36, 34), (x, piso - 44), (x, piso), 2)
        pygame.draw.polygon(lienzo, (230, 200, 140), [(x - 8, piso - 44), (x + 8, piso - 44), (x + 5, piso - 54),
                                                       (x - 5, piso - 54)])
        pygame.draw.rect(lienzo, (40, 36, 34), (x - 5, piso - 2, 10, 2))
    elif nombre == "tina":
        pygame.draw.rect(lienzo, (226, 230, 232), (x, piso - 22, 70, 18), border_radius=6)
        pygame.draw.rect(lienzo, (150, 190, 210), (x + 4, piso - 20, 62, 4))
        pygame.draw.rect(lienzo, (190, 190, 190), (x + 6, piso - 4, 4, 4))
        pygame.draw.rect(lienzo, (190, 190, 190), (x + 60, piso - 4, 4, 4))
    elif nombre == "lavabo":
        pygame.draw.rect(lienzo, (226, 230, 232), (x, piso - 34, 26, 8))
        pygame.draw.rect(lienzo, (200, 204, 206), (x + 10, piso - 26, 6, 26))
        pygame.draw.rect(lienzo, (180, 200, 210), (x + 2, piso - 72, 22, 28))   # espejo
    elif nombre == "sillon":
        pygame.draw.rect(lienzo, (110, 58, 70), (x, piso - 30, 80, 14), border_radius=4)
        pygame.draw.rect(lienzo, (130, 70, 84), (x, piso - 18, 80, 14))
        pygame.draw.rect(lienzo, (110, 58, 70), (x - 4, piso - 22, 8, 18))
        pygame.draw.rect(lienzo, (110, 58, 70), (x + 76, piso - 22, 8, 18))
        pygame.draw.rect(lienzo, (50, 34, 28), (x + 2, piso - 4, 4, 4))
        pygame.draw.rect(lienzo, (50, 34, 28), (x + 74, piso - 4, 4, 4))
    elif nombre == "reloj":
        pygame.draw.rect(lienzo, (86, 58, 40), (x, piso - 76, 22, 76))
        pygame.draw.circle(lienzo, (230, 220, 190), (x + 11, piso - 62), 8)
        angulo: float = reloj * 2
        pygame.draw.line(lienzo, (30, 26, 24), (x + 11, piso - 62),
                         (x + 11 + int(math.cos(angulo) * 6), piso - 62 + int(math.sin(angulo) * 6)))
        pendulo: int = int(math.sin(reloj * 3) * 5)
        pygame.draw.line(lienzo, (200, 170, 80), (x + 11, piso - 50), (x + 11 + pendulo, piso - 22))
        pygame.draw.circle(lienzo, (200, 170, 80), (x + 11 + pendulo, piso - 22), 3)


# ------------------------------------------------------------ Coraline (sprite pixel por pixel)

# Cada letra es un color; "." es transparente. Coraline mira a la derecha y
# carga la libreta con la mano de enfrente.
COLORES_SPRITE: dict = {
    "O": (24, 20, 30),      # contorno
    "H": (30, 48, 150),     # pelo oscuro
    "h": (48, 78, 196),     # pelo
    "l": (110, 146, 240),   # brillo del pelo
    "S": (242, 206, 178),   # piel
    "s": (212, 168, 144),   # piel en sombra
    "E": (30, 26, 40),      # ojo
    "R": (236, 146, 146),   # chapitas
    "P": (255, 120, 190),   # pasador
    "Y": (236, 190, 50),    # impermeable
    "y": (190, 140, 28),    # impermeable en sombra
    "L": (252, 226, 124),   # impermeable con luz
    "B": (130, 90, 24),     # botones
    "N": (246, 242, 230),   # libreta
    "n": (150, 180, 222),   # renglones de la libreta
    "J": (70, 44, 78),      # medias: raya oscura
    "j": (52, 32, 60),      # medias: raya oscura en sombra
    "r": (214, 150, 110),   # medias: raya clara
    "F": (164, 40, 46),     # falda roja
    "M": (112, 62, 46),     # bolsa café y su correa
    "K": (240, 200, 56),    # botas amarillas
    "k": (196, 150, 30),    # botas en sombra
}

CUERPO: list = [
    "......OOOOOO........",
    "....OOHHHHHHOO......",
    "...OHHhhhhhhHHO.....",
    "..OHhhllhhhhhhHO....",
    "..OHhlhhhhhhhhhHO...",
    ".OHhhhhhhhhhhHHHPO..",
    ".OHhhhhhHHHHSSSSO...",
    ".OHhhhhHSSSSSSSSO...",
    ".OHhhhHSSSSSSESSO...",
    ".OHhhhHSSSSSSESSSO..",
    ".OHhhhHsSSSRRSSSO...",
    ".OHhhhhHsSSSSSsO....",
    "..OHhhhHHsSSSSO.....",
    "..OHHHHOOOsssO......",
    "....OYYLLMYYO.......",
    "...OYYLYMYYYYO......",
    "...OYLYMYYYYNNNO....",
    "..OYYLMYYYYSNnNNO...",
    "..OYYMYYYBYSNNNNO...",
    "..OyMYYYYYYYNnNNO...",
    ".OMMMMYYYBYYNNNNO...",
    ".OMMMMYYYYYYOOOO....",
    ".OMMMMYYYBYYYO......",
    "..OyyyYYYYYYYO......",
    "..OOyyyyyyyyyO......",
    "...OFFFFFFFFO.......",
]

PIERNAS_QUIETA: list = [
    "...OJJjOJJJO........",
    "...OJJjOJJJO........",
    "...OJJjOJJJO........",
    "...OJJjOJJJO........",
    "...OKKKOKKKO........",
    "...OKKKOKKKO........",
    "..OkkkkOkkkkO.......",
    "..OOOOOOOOOOO.......",
]

PIERNAS_PASO: list = [
    "...OJJJJJJJO........",
    "..OJJjOOJJJJO.......",
    "..OJjO..OJJJO.......",
    ".OJJO....OJJO.......",
    ".OJjO.....OJJO......",
    ".OKKO.....OKKKO.....",
    "OKKKO.....OKKKO.....",
    "OOOOO.....OOOOO.....",
]

PIERNAS_CRUCE: list = [
    "...OJJJJJJO.........",
    "...OJJjOJJO.........",
    "...OJJjOJJO.........",
    "...OJJjOJJJO........",
    "...OJJjOKKKO........",
    "...OKKKOKkkO........",
    "..OkkkkOOOOO........",
    "..OOOOOO............",
]

SPRITES: dict = {}   # sprites ya armados, para no armarlos en cada vuelta


def armar_sprite(filas: list) -> pygame.Surface:
    """Convierte las filas de letras en una imagen con transparencia."""
    sprite: pygame.Surface = pygame.Surface((20, len(filas)), pygame.SRCALPHA)
    for y in range(len(filas)):
        fila: str = filas[y].ljust(20, ".")
        for x in range(20):
            if fila[x] in COLORES_SPRITE:
                sprite.set_at((x, y), COLORES_SPRITE[fila[x]])
    return sprite


def sprite_coraline(piernas: str, mira_derecha: bool) -> pygame.Surface:
    clave: str = piernas + str(mira_derecha)
    if clave not in SPRITES:
        filas: dict = {"quieta": PIERNAS_QUIETA, "paso": PIERNAS_PASO, "cruce": PIERNAS_CRUCE}
        piernas_con_rayas: list = []
        for i in range(len(filas[piernas])):
            fila: str = filas[piernas][i]
            if i % 2 == 0:
                fila = fila.replace("J", "r").replace("j", "r")   # medias a rayas
            piernas_con_rayas.append(fila)
        sprite: pygame.Surface = armar_sprite(CUERPO + piernas_con_rayas)
        if not mira_derecha:
            sprite = pygame.transform.flip(sprite, True, False)
        SPRITES[clave] = sprite
    return SPRITES[clave]


def dibujar_coraline(lienzo: pygame.Surface, juego: dict) -> None:
    """Coraline camina con 4 cuadros; quieta respira, y anota en la libreta al llegar."""
    x: int = int(juego["coraline_x"])
    caminando: bool = abs(juego["destino_x"] - juego["coraline_x"]) > 0.5
    reloj: float = juego["reloj"]

    if caminando:
        cuadro: int = int(reloj * 10) % 4
        piernas: str = ["paso", "cruce", "paso", "cruce"][cuadro]
        rebote: int = 1 if cuadro % 2 == 1 else 0
    else:
        piernas = "quieta"
        rebote = int(reloj * 1.5) % 2   # respira: sube un pixel cada segundo y medio

    sprite: pygame.Surface = sprite_coraline(piernas, juego["mira_derecha"])

    sombra: pygame.Surface = pygame.Surface((18, 4), pygame.SRCALPHA)
    pygame.draw.ellipse(sombra, (0, 0, 0, 100), (0, 0, 18, 4))
    lienzo.blit(sombra, (x - 9, Y_PISO + 13))

    izquierda: int = x - 10
    arriba: int = Y_PISO + 15 - sprite.get_height() - rebote
    lienzo.blit(sprite, (izquierda, arriba))

    # Lápiz que se mueve sobre la libreta mientras anota
    if juego["escribiendo"] > 0:
        movimiento: int = int(juego["escribiendo"] * 20) % 3
        if juego["mira_derecha"]:
            punta_x: int = izquierda + 13 + movimiento
        else:
            punta_x = izquierda + 6 - movimiento
        pygame.draw.line(lienzo, (240, 200, 80), (punta_x, arriba + 15), (punta_x + 2, arriba + 12))
        lienzo.set_at((punta_x, arriba + 16), (40, 40, 60))


def dibujar_marca(lienzo: pygame.Surface, rect: pygame.Rect) -> None:
    """Palomita de lápiz sobre un objeto ya encontrado."""
    x: int = rect.right - 6
    y: int = rect.y + 4
    pygame.draw.circle(lienzo, (250, 246, 232), (x, y), 5)
    pygame.draw.lines(lienzo, COLOR_LAPIZ, False, [(x - 3, y), (x - 1, y + 2), (x + 3, y - 3)], 2)


def dibujar_flecha(lienzo: pygame.Surface, reloj: float) -> None:
    rect: pygame.Rect = rect_flecha()
    mover: int = int(math.sin(reloj * 6) * 2)
    puntos: list = [(rect.x + 4 + mover, rect.y + 4), (rect.right - 4 + mover, rect.centery),
                    (rect.x + 4 + mover, rect.bottom - 4)]
    pygame.draw.polygon(lienzo, (20, 20, 30), [(px + 1, py + 1) for px, py in puntos])
    pygame.draw.polygon(lienzo, COLOR_MARCA, puntos)


def dibujar_luz_puerta(lienzo: pygame.Surface, puerta: pygame.Rect) -> None:
    """Luz tenue sobre la puerta y lo demás más oscuro, para que solo se vea ella."""
    sombra: pygame.Surface = pygame.Surface((ANCHO_LIENZO, ALTO_LIENZO), pygame.SRCALPHA)
    sombra.fill((4, 10, 14, 110))
    for paso in range(30):
        radio: int = 90 - paso * 3
        pygame.draw.circle(sombra, (4, 10, 14, 110 - (paso + 1) * 3), puerta.center, radio)
    lienzo.blit(sombra, (0, 0))


def dibujar_luz(lienzo: pygame.Surface) -> None:
    """Oscurece las orillas para dar ambiente de tarde lluviosa."""
    sombra: pygame.Surface = pygame.Surface((ANCHO_LIENZO, ALTO_LIENZO), pygame.SRCALPHA)
    for i in range(6):
        alfa: int = 70 - i * 12
        pygame.draw.rect(sombra, (8, 14, 24, alfa), (0, 0, ANCHO_LIENZO, ALTO_LIENZO), 6 - i + i * 4)
    lienzo.blit(sombra, (0, 0))


def dibujar(ventana: pygame.Surface, juego: dict, fuentes: dict) -> None:
    lienzo: pygame.Surface = juego["lienzo"]
    cuarto: dict = CUARTOS[juego["cuarto"]]
    encontrados: list = juego["encontrados"][juego["cuarto"]]
    mouse_x: int = pygame.mouse.get_pos()[0] // ESCALA
    mouse_y: int = pygame.mouse.get_pos()[1] // ESCALA

    dibujar_paredes(lienzo, cuarto)
    for nombre, x in cuarto["muebles"]:
        if nombre in ["cuadro", "alfombra"]:
            dibujar_mueble(lienzo, nombre, x, juego["reloj"])
    for i in range(len(cuarto["objetos"])):
        objeto: dict = cuarto["objetos"][i]
        dibujar_objeto(lienzo, objeto, juego)
        rect: pygame.Rect = pygame.Rect(objeto["rect"])
        if encontrados[i]:
            dibujar_marca(lienzo, rect)
        elif rect.collidepoint(mouse_x, mouse_y):
            pygame.draw.rect(lienzo, COLOR_MARCA, rect.inflate(8, 8), 1)
    for nombre, x in cuarto["muebles"]:
        if nombre not in ["cuadro", "alfombra"]:
            dibujar_mueble(lienzo, nombre, x, juego["reloj"])

    dibujar_coraline(lienzo, juego)

    if cuarto_completo(juego) and not es_ultimo_cuarto(juego):
        dibujar_flecha(lienzo, juego["reloj"])

    if cuarto.get("liso", False):
        dibujar_luz_puerta(lienzo, pygame.Rect(cuarto["objetos"][0]["rect"]))
    dibujar_luz(lienzo)
    ventana.blit(pygame.transform.scale(lienzo, (config.ANCHO, config.ALTO)), (0, 0))

    # Lo que va encima se dibuja a tamaño normal para que el texto se lea bien
    dibujar_libreta(ventana, juego, cuarto, fuentes)
    for aviso in juego["avisos"]:
        superficie: pygame.Surface = fuentes["narracion"].render(aviso["texto"], True, COLOR_MARCA)
        x = aviso["x"] * ESCALA - superficie.get_width() // 2
        y = max(int(aviso["y"] * ESCALA) - superficie.get_height(), 108)
        ventana.blit(fuentes["narracion"].render(aviso["texto"], True, (20, 20, 30)), (x + 2, y + 2))
        ventana.blit(superficie, (x, y))

    if cuarto_completo(juego) and not es_ultimo_cuarto(juego):
        texto: pygame.Surface = fuentes["pequena"].render("SIGUIENTE CUARTO", True, COLOR_MARCA)
        flecha: pygame.Rect = rect_flecha()
        ventana.blit(texto, (flecha.x * ESCALA - texto.get_width() - 12,
                             flecha.centery * ESCALA - texto.get_height() // 2))

    if juego["fundido"] > 0:
        mitad: float = DURACION_FUNDIDO / 2
        alfa: int = int(255 * (1 - abs(juego["fundido"] - mitad) / mitad))
        capa: pygame.Surface = pygame.Surface((config.ANCHO, config.ALTO))
        capa.fill((6, 8, 14))
        capa.set_alpha(alfa)
        ventana.blit(capa, (0, 0))


def dibujar_libreta(ventana: pygame.Surface, juego: dict, cuarto: dict, fuentes: dict) -> None:
    """Tira de libreta arriba con el nombre del cuarto y lo que lleva contado."""
    rect: pygame.Rect = pygame.Rect(40, 52, 760, 52)
    pygame.draw.rect(ventana, (0, 0, 0), rect.move(5, 6), border_radius=4)
    pygame.draw.rect(ventana, (250, 246, 232), rect, border_radius=4)
    pygame.draw.line(ventana, (222, 128, 128), (rect.x + 18, rect.y + 4), (rect.x + 18, rect.bottom - 4), 2)
    pygame.draw.line(ventana, (176, 199, 228), (rect.x + 4, rect.bottom - 10), (rect.right - 4, rect.bottom - 10))

    titulo: pygame.Surface = fuentes["titulo_palace"].render(cuarto["nombre"], True, (52, 88, 160))
    ventana.blit(titulo, (rect.x + 28, rect.centery - titulo.get_height() // 2))

    conteo: str = ("Puertas " + str(juego["puertas"]) + "/" + str(juego["total_puertas"])
                   + "   Ventanas " + str(juego["ventanas"]) + "/" + str(juego["total_ventanas"]))
    superficie: pygame.Surface = fuentes["narracion"].render(conteo, True, (40, 44, 70))
    cuarto_texto: str = str(juego["cuarto"] + 1) + "/" + str(len(CUARTOS))
    numero: pygame.Surface = fuentes["pequena"].render(cuarto_texto, True, (120, 120, 140))
    x_numero: int = rect.right - numero.get_width() - 12
    ventana.blit(numero, (x_numero, rect.centery - numero.get_height() // 2))

    # El conteo va pegado a la derecha, antes del número de cuarto
    x: int = x_numero - superficie.get_width() - 24
    ventana.blit(superficie, (x, rect.centery - superficie.get_height() // 2))
