"""FONDO DIBUJADO CON CODIGO: LOS PAPAS DE CORALINE ATRAPADOS EN EL ESPEJO.

En el espejo del pasillo aparecen su mama y su papa, palidos, como atrapados
del otro lado. Su papa escribe con el dedo en el vidrio empanado una sola
palabra: AYUDANOS. El pasillo, el marco y el vidrio son los de
espejo_pasillo.py; la mama es la de personajes.py (la misma de cap01 y
cap03) y el papa de frente se dibuja aqui (en estudio_lluvioso.py solo se le
ve de espaldas: sueter verde y pelo cafe). Se usa en cap05_n04.

Lo que se mueve: los papas se desvanecen y vuelven a aparecer, el dedo del
papa escribe la palabra letra por letra, le escurren gotitas y luego se
borra para volver a empezar.
"""

import math

import pygame

from interfaz.fondos.pintura import ANCHO, ALTO
from interfaz.fondos.pintura import mezclar, brillo, orillas_oscuras, mostrar, armar_sprite
from interfaz.fondos import personajes
from interfaz.fondos import espejo_pasillo
from interfaz.fondos import sala_actrices

Y_PISO = espejo_pasillo.Y_PISO
VIDRIO = espejo_pasillo.VIDRIO

X_CORALINE = 450
X_GATO = 486

X_MAMA = VIDRIO.x + 22          # centro de la mama dentro del espejo
X_PAPA = VIDRIO.x + 74          # centro del papa dentro del espejo
Y_HOMBROS = VIDRIO.y + 92       # donde empiezan los hombros del papa

PALIDO = (214, 224, 240)

PAPA_PELO = (70, 48, 36)
PAPA_SUETER = (46, 66, 58)
PAPA_SUETER_LUZ = (66, 92, 80)
PAPA_PIEL = (210, 170, 140)
PAPA_PIEL_SOMBRA = (180, 140, 116)

# LA PALABRA ESCRITA CON EL DEDO: LETRAS DE 5 x 7 ("#" ES TRAZO)
LETRAS = {
    "A": [".###.", "#...#", "#...#", "#####", "#...#", "#...#", "#...#"],
    "Y": ["#...#", "#...#", ".#.#.", "..#..", "..#..", "..#..", "..#.."],
    "U": ["#...#", "#...#", "#...#", "#...#", "#...#", "#...#", ".###."],
    "D": ["####.", "#...#", "#...#", "#...#", "#...#", "#...#", "####."],
    "N": ["#...#", "##..#", "#.#.#", "#..##", "#...#", "#...#", "#...#"],
    "O": [".###.", "#...#", "#...#", "#...#", "#...#", "#...#", ".###."],
    "S": [".####", "#....", "#....", ".###.", "....#", "....#", "####."],
}
PALABRA = "AYUDANOS"
LETRA_CON_ACENTO = 2            # la U lleva acento: AYÚDANOS
Y_PALABRA = VIDRIO.y + 12
X_PALABRA = VIDRIO.centerx - (len(PALABRA) * 6 - 1) // 2
COLOR_LETRA = (236, 242, 250)

# CICLO DE LA ANIMACION (SEGUNDOS)
POR_LETRA = 0.45
ESCRIBIR = POR_LETRA * len(PALABRA)
QUEDARSE = 3.5
BORRARSE = 1.2
CICLO = ESCRIBIR + QUEDARSE + BORRARSE

CAPAS = {}


# --------------------------------------------------
# LOS PAPAS DENTRO DEL ESPEJO
# --------------------------------------------------

def dibujar_papa_frente(lienzo: pygame.Surface, x: int) -> None:

    """EL PAPA DE FRENTE, DE LA CINTURA PARA ARRIBA: SUETER VERDE, PELO CAFE Y LENTES.
    EL BRAZO QUE ESCRIBE SE DIBUJA APARTE PORQUE SE MUEVE."""

    y = Y_HOMBROS

    # HOMBROS Y SUETER
    alto = VIDRIO.bottom - y
    pygame.draw.rect(lienzo, PAPA_SUETER, (x - 17, y, 34, alto), border_top_left_radius=9, border_top_right_radius=9)
    pygame.draw.rect(lienzo, PAPA_SUETER_LUZ, (x - 13, y + 4, 6, alto - 4))
    pygame.draw.rect(lienzo, mezclar(PAPA_SUETER, (0, 0, 0), 0.25), (x - 5, y - 2, 10, 5), border_radius=2)  # cuello

    for yy in range(y + 10, VIDRIO.bottom, 6):
        pygame.draw.line(lienzo, mezclar(PAPA_SUETER, (0, 0, 0), 0.15), (x - 15, yy), (x + 15, yy))           # tejido

    # BRAZO IZQUIERDO, PEGADO AL CUERPO, CON LA MANO EN EL VIDRIO
    pygame.draw.line(lienzo, PAPA_SUETER, (x - 16, y + 6), (x - 20, y + 40), 6)
    pygame.draw.ellipse(lienzo, PAPA_PIEL, (x - 23, y + 38, 7, 8))

    # CUELLO Y CABEZA
    pygame.draw.rect(lienzo, PAPA_PIEL_SOMBRA, (x - 3, y - 8, 6, 8))
    pygame.draw.ellipse(lienzo, PAPA_PIEL, (x - 10, y - 32, 20, 26))
    pygame.draw.ellipse(lienzo, PAPA_PIEL, (x - 12, y - 22, 4, 7))                                              # orejas
    pygame.draw.ellipse(lienzo, PAPA_PIEL, (x + 8, y - 22, 4, 7))
    pygame.draw.ellipse(lienzo, PAPA_PIEL_SOMBRA, (x + 3, y - 28, 6, 20))

    # PELO CAFE CORTO, UN POCO DESPEINADO
    pygame.draw.ellipse(lienzo, PAPA_PELO, (x - 11, y - 36, 22, 12))
    pygame.draw.rect(lienzo, PAPA_PELO, (x - 11, y - 30, 3, 8))
    pygame.draw.rect(lienzo, PAPA_PELO, (x + 8, y - 30, 3, 7))
    pygame.draw.line(lienzo, mezclar(PAPA_PELO, (255, 255, 255), 0.2), (x - 5, y - 34), (x + 3, y - 35))

    # LENTES, OJOS PREOCUPADOS Y BOCA TRISTE
    for ojo_x in [x - 5, x + 5]:
        pygame.draw.rect(lienzo, (40, 36, 40), (ojo_x - 4, y - 23, 8, 6), 1)
        pygame.draw.rect(lienzo, (40, 30, 30), (ojo_x - 1, y - 21, 2, 2))

    pygame.draw.line(lienzo, (40, 36, 40), (x - 1, y - 21), (x + 1, y - 21))
    pygame.draw.line(lienzo, (60, 40, 40), (x - 8, y - 26), (x - 3, y - 25))                                     # cejas
    pygame.draw.line(lienzo, (60, 40, 40), (x + 3, y - 25), (x + 8, y - 26))
    pygame.draw.arc(lienzo, (120, 60, 60), (x - 4, y - 13, 8, 6), 0.4, 2.7, 1)


def crear_fantasmas() -> pygame.Surface:

    """LOS DOS PAPAS EN UNA CAPA DEL TAMANO DEL VIDRIO, YA PALIDOS (SE GUARDA)."""

    capa = pygame.Surface((ANCHO, ALTO), pygame.SRCALPHA)

    # LA MAMA DE PERFIL MIRANDO AL PAPA; SOLO SE VE DE LA CINTURA PARA ARRIBA
    personajes.dibujar_mama(capa, X_MAMA, VIDRIO.bottom + 34, True, 1)
    dibujar_papa_frente(capa, X_PAPA)

    # RECORTAMOS AL TAMANO DEL VIDRIO
    fantasmas = pygame.Surface(VIDRIO.size, pygame.SRCALPHA)
    fantasmas.blit(capa, (-VIDRIO.x, -VIDRIO.y))

    # PALIDOS: UNA CAPA BLANCA AZULADA SOLO ENCIMA DE SU SILUETA
    velo = pygame.mask.from_surface(fantasmas, 127).to_surface(setcolor=(PALIDO[0], PALIDO[1], PALIDO[2], 120),
                                                              unsetcolor=(0, 0, 0, 0))
    fantasmas.blit(velo, (0, 0))

    return fantasmas


# --------------------------------------------------
# PARTE FIJA
# --------------------------------------------------

def crear_fijo() -> pygame.Surface:

    lienzo = pygame.Surface((ANCHO, ALTO))

    espejo_pasillo.dibujar_pasillo(lienzo)
    espejo_pasillo.dibujar_marco(lienzo)
    espejo_pasillo.dibujar_vidrio(lienzo)

    # EL VIDRIO SE OSCURECE Y SE EMPANA: YA NO REFLEJA EL PASILLO
    niebla = pygame.Surface(VIDRIO.size, pygame.SRCALPHA)
    niebla.fill((24, 30, 48, 150))
    lienzo.blit(niebla, VIDRIO.topleft)

    sala_actrices.dibujar_coraline(lienzo, X_CORALINE, True)

    # EL PASILLO SE PONE MAS FRIO Y OSCURO QUE EN cap05_n03
    frio = pygame.Surface((ANCHO, ALTO), pygame.SRCALPHA)
    frio.fill((10, 16, 40, 60))
    lienzo.blit(frio, (0, 0))

    brillo(lienzo, VIDRIO.center, 110, (170, 190, 230), 45)
    orillas_oscuras(lienzo)

    return lienzo


# --------------------------------------------------
# LO QUE SE MUEVE
# --------------------------------------------------

def letras_escritas(tiempo: float) -> float:

    """CUANTAS LETRAS VAN ESCRITAS (CON DECIMALES: LA ULTIMA VA A LA MITAD)."""

    fase = tiempo % CICLO

    return min(fase / POR_LETRA, len(PALABRA))


def transparencia_palabra(tiempo: float) -> int:

    """LA PALABRA SE VE COMPLETA Y AL FINAL DEL CICLO SE BORRA POCO A POCO."""

    fase = tiempo % CICLO

    if fase < ESCRIBIR + QUEDARSE:
        return 255

    return int(255 * (1 - (fase - ESCRIBIR - QUEDARSE) / BORRARSE))


def punta_del_dedo(tiempo: float) -> tuple:

    """DONDE ESTA EL DEDO DEL PAPA: RECORRE CADA LETRA MIENTRAS LA ESCRIBE."""

    escritas = letras_escritas(tiempo)
    letra = min(int(escritas), len(PALABRA) - 1)
    avance = escritas - int(escritas) if escritas < len(PALABRA) else 1.0

    x = X_PALABRA + letra * 6 + int(avance * 4)
    y = Y_PALABRA + 6 - int(abs(math.sin(avance * math.pi * 2)) * 6)

    return (x, y)


def dibujar_palabra(lienzo: pygame.Surface, tiempo: float) -> None:

    """LA PALABRA ESCRITA EN EL VIDRIO EMPANADO, CON GOTITAS QUE ESCURREN."""

    escritas = letras_escritas(tiempo)
    alfa = transparencia_palabra(tiempo)

    capa = pygame.Surface((ANCHO, ALTO), pygame.SRCALPHA)
    color = (COLOR_LETRA[0], COLOR_LETRA[1], COLOR_LETRA[2], alfa)

    for i in range(len(PALABRA)):

        if i >= escritas:
            break

        filas = LETRAS[PALABRA[i]]
        x0 = X_PALABRA + i * 6
        y0 = Y_PALABRA + (i % 2)                     # escrita a mano: un poco chueca

        # LA LETRA QUE SE ESTA ESCRIBIENDO SOLO SE VE HASTA DONDE VA EL DEDO
        hasta = len(filas)
        if i == int(escritas):
            hasta = int((escritas - i) * len(filas)) + 1

        for fila in range(min(hasta, len(filas))):
            for columna in range(5):
                if filas[fila][columna] == "#":
                    capa.set_at((x0 + columna, y0 + fila), color)

        if i == LETRA_CON_ACENTO:
            capa.set_at((x0 + 3, y0 - 2), color)
            capa.set_at((x0 + 2, y0 - 1), color)

        # GOTITA QUE ESCURRE DEBAJO DE ALGUNAS LETRAS
        if i % 3 == 0:
            largo = min(int((tiempo % CICLO - i * POR_LETRA) * 3), 9)
            if largo > 0:
                pygame.draw.line(capa, color, (x0 + 1, y0 + 7), (x0 + 1, y0 + 6 + largo))

    lienzo.blit(capa, (0, 0))


def dibujar_brazo_papa(lienzo: pygame.Surface, tiempo: float, alfa: int) -> None:

    """EL BRAZO DEL PAPA SUBE HASTA LA PALABRA Y SIGUE AL DEDO MIENTRAS ESCRIBE."""

    dedo = punta_del_dedo(tiempo)
    hombro = (X_PAPA + 15, Y_HOMBROS + 6)
    codo = (X_PAPA + 22, Y_HOMBROS - 18)

    capa = pygame.Surface((ANCHO, ALTO), pygame.SRCALPHA)

    manga = mezclar(PAPA_SUETER, PALIDO, 0.45)
    piel = mezclar(PAPA_PIEL, PALIDO, 0.45)

    pygame.draw.line(capa, manga + (alfa,), hombro, codo, 6)
    pygame.draw.line(capa, manga + (alfa,), codo, (dedo[0] + 3, dedo[1] + 9), 5)
    pygame.draw.ellipse(capa, piel + (alfa,), (dedo[0], dedo[1] + 4, 7, 8))
    pygame.draw.line(capa, piel + (alfa,), (dedo[0] + 2, dedo[1] + 5), (dedo[0], dedo[1]), 2)                  # el dedo

    recorte = pygame.Surface(VIDRIO.size, pygame.SRCALPHA)
    recorte.blit(capa, (-VIDRIO.x, -VIDRIO.y))
    lienzo.blit(recorte, VIDRIO.topleft)


def dibujar(ventana: pygame.Surface) -> None:

    """DIBUJA LA ESCENA COMPLETA EN LA VENTANA DEL JUEGO."""

    if "fijo" not in CAPAS:
        CAPAS["fijo"] = crear_fijo()
        CAPAS["fantasmas"] = crear_fantasmas()

    tiempo = pygame.time.get_ticks() / 1000

    lienzo = CAPAS["fijo"].copy()

    # LOS PAPAS SE DESVANECEN Y VUELVEN, COMO UNA SENAL QUE SE PIERDE
    alfa = 170 + int(math.sin(tiempo * 1.7) * 45 + math.sin(tiempo * 5.3) * 10)
    fantasmas = CAPAS["fantasmas"].copy()
    fantasmas.set_alpha(alfa)
    lienzo.blit(fantasmas, VIDRIO.topleft)

    dibujar_brazo_papa(lienzo, tiempo, alfa)
    dibujar_palabra(lienzo, tiempo)
    espejo_pasillo.dibujar_destello(lienzo, tiempo)

    personajes.dibujar_gato(lienzo, X_GATO, Y_PISO + 2, True, tiempo)

    mostrar(ventana, lienzo)
