"""FONDO DIBUJADO CON CODIGO: EL OTRO CUARTO VISTO A TRAVES DE LA PIEDRA.

Se ve desde los ojos de Coraline: el tapete con los juguetes regados de
caja_juguetes.py, de cerca (el cuarto agrandado x2). Coraline sostiene la
piedra con agujero (piedra.py) frente a su ojo, con la mano del guante azul
agarrando una esquina. Afuera de la piedra todo tiene los colores bonitos y
falsos del otro mundo; por el agujero se ve como es de verdad: gris, apagado
y frio. Solo una cosa tiene color ahi adentro: la canica gris, que arde roja
como una brasa. La piedra va recorriendo el tapete hasta que la encuentra.
Se usa en cap08_n03 y en su rama cap08_r03.

Lo que se mueve: la piedra que busca y se detiene en la canica (con un
temblorcito de la mano) y la brasa que late y se aviva cuando la encuentra.
"""

import math

import pygame

from interfaz.fondos.pintura import ANCHO, ALTO
from interfaz.fondos.pintura import capa_vacia, pegar_con_contorno, COLOR_CONTORNO
from interfaz.fondos.pintura import brillo, orillas_oscuras, mostrar
from interfaz.fondos import personajes
from interfaz.fondos import otro_cuarto
from interfaz.fondos import caja_juguetes
from interfaz.fondos import piedra

ZONA = pygame.Rect(300, 180, ANCHO // 2, ALTO // 2)       # el pedazo del cuarto que se agranda x2 (el tapete)

RADIO_AGUJERO = 40                                         # la misma piedra que el minijuego
BORDE_PIEDRA = 24

# LA CANICA DEL ALMA EN LA VISTA AGRANDADA
BRASA = ((caja_juguetes.BRASA[0] - ZONA.x) * 2, (caja_juguetes.BRASA[1] - ZONA.y) * 2)

DURACION = 9.0              # segundos que dura la busqueda completa antes de volver a empezar
BUSCANDO = 4.5              # los primeros segundos la piedra recorre el tapete
LLEGANDO = 1.2              # luego tarda esto en acomodarse sobre la canica

COLOR_VERDAD = (150, 150, 172)      # el tinte frio de lo que se ve por la piedra

CAPAS = {}


# --------------------------------------------------
# PARTE FIJA
# --------------------------------------------------

def crear_capas() -> None:

    """LA VISTA NORMAL (COLORES FALSOS, UN POCO EN SOMBRA) Y LA VISTA DE VERDAD (GRIS)."""

    cuarto = pygame.Surface((ANCHO, ALTO))
    otro_cuarto.dibujar_cuarto(cuarto, False)
    caja_juguetes.dibujar_juguetes_regados(cuarto)

    capa = capa_vacia()
    caja_juguetes.dibujar_caja_volteada(capa)
    pegar_con_contorno(cuarto, capa)

    cerca = pygame.transform.scale(cuarto.subsurface(ZONA), (ANCHO, ALTO))

    # POR LA PIEDRA: SIN COLOR, MAS OSCURO Y AZULADO
    verdad = pygame.transform.grayscale(cerca)
    tinte = pygame.Surface((ANCHO, ALTO))
    tinte.fill(COLOR_VERDAD)
    verdad.blit(tinte, (0, 0), special_flags=pygame.BLEND_MULT)
    CAPAS["verdad"] = verdad

    # AFUERA DE LA PIEDRA: LOS COLORES DEL OTRO MUNDO, PERO EN LA SOMBRA DE LA PIEDRA
    afuera = cerca.copy()
    tinte.fill((170, 160, 190))
    afuera.blit(tinte, (0, 0), special_flags=pygame.BLEND_MULT)
    brillo(afuera, (560, 60), 200, (255, 210, 150), 40)
    orillas_oscuras(afuera)
    CAPAS["afuera"] = afuera

    mascara = pygame.Surface((RADIO_AGUJERO * 2, RADIO_AGUJERO * 2), pygame.SRCALPHA)
    pygame.draw.circle(mascara, (255, 255, 255, 255), (RADIO_AGUJERO, RADIO_AGUJERO), RADIO_AGUJERO)
    CAPAS["mascara"] = mascara


# --------------------------------------------------
# LO QUE SE MUEVE
# --------------------------------------------------

def centro_de_la_piedra(tiempo: float) -> tuple:

    """DONDE ESTA EL AGUJERO: PRIMERO RECORRE EL TAPETE, LUEGO SE ACOMODA EN LA CANICA Y AHI SE QUEDA."""

    fase = tiempo % DURACION
    temblor = (int(math.sin(tiempo * 7) * 1.2), int(math.cos(tiempo * 5) * 1.2))

    # LA BUSQUEDA: UN OCHO QUE BARRE EL TAPETE
    def buscando(t: float) -> tuple:
        return (500 + math.sin(t * 1.1) * 90, 230 + math.sin(t * 2.2) * 50)

    if fase < BUSCANDO:
        x, y = buscando(fase)
    else:
        avance = min(1.0, (fase - BUSCANDO) / LLEGANDO)
        suave = avance * avance * (3 - 2 * avance)
        inicio = buscando(BUSCANDO)
        x = inicio[0] + (BRASA[0] - inicio[0]) * suave
        y = inicio[1] + (BRASA[1] - inicio[1]) * suave

    return (int(x) + temblor[0], int(y) + temblor[1])


def la_encontro(tiempo: float) -> bool:

    return tiempo % DURACION > BUSCANDO + LLEGANDO


def dibujar_brasa(lienzo: pygame.Surface, tiempo: float) -> None:

    """LA CANICA ARDE ROJA (EN LA VISTA DE VERDAD). CUANDO LA PIEDRA LA ENCUENTRA, SE AVIVA."""

    luz = (math.sin(tiempo * 4) + 1) / 2
    fuerza = 1.6 if la_encontro(tiempo) else 1.0
    x, y = BRASA

    capa = pygame.Surface((80, 80), pygame.SRCALPHA)
    pygame.draw.circle(capa, (255, 70, 20, int((30 + luz * 40) * fuerza)), (40, 40), int(26 * fuerza))
    pygame.draw.circle(capa, (255, 130, 40, int((60 + luz * 60) * fuerza)), (40, 40), 14)
    lienzo.blit(capa, (x - 40, y - 40))

    pygame.draw.circle(lienzo, COLOR_CONTORNO, (x, y), 8)
    pygame.draw.circle(lienzo, (230, int(60 + luz * 90), 30), (x, y), 7)
    pygame.draw.circle(lienzo, (255, 220, 140), (x - 2, y - 2), 3)

    # CUANDO LA ENCUENTRA, RAYITAS DE LUZ QUE SALEN DE LA CANICA
    if la_encontro(tiempo):
        for i in range(8):
            angulo = i / 8 * math.pi * 2 + tiempo
            largo = 14 + int(luz * 6)
            inicio = (x + int(math.cos(angulo) * 11), y + int(math.sin(angulo) * 11))
            fin = (x + int(math.cos(angulo) * largo), y + int(math.sin(angulo) * largo))
            pygame.draw.line(lienzo, (255, 170, 90), inicio, fin)


def dibujar_mano(lienzo: pygame.Surface, centro: tuple) -> None:

    """LA MANO DE CORALINE (MANGA AMARILLA Y GUANTE AZUL SIN DEDOS) AGARRANDO EL LADO IZQUIERDO DE LA PIEDRA."""

    # EL GUANTE QUEDA ABAJO A LA IZQUIERDA DEL AGUJERO, SOBRE LA ORILLA DE LA PIEDRA
    x, y = centro[0] - 74, centro[1] + 30

    capa = capa_vacia()

    # MANGA ANCHA DEL IMPERMEABLE QUE ENTRA DESDE ABAJO, CON SU PUNO
    pygame.draw.polygon(capa, personajes.AMARILLO, [(x - 46, ALTO + 10), (x - 18, y + 20), (x + 18, y + 26), (x + 14, ALTO + 10)])
    pygame.draw.line(capa, personajes.AMARILLO_SOMBRA, (x + 2, ALTO), (x + 6, y + 30), 4)
    pygame.draw.line(capa, personajes.AMARILLO_CLARO, (x - 30, ALTO), (x - 12, y + 26), 2)

    # GUANTE AZUL MARINO, EL PULGAR Y LOS DEDOS QUE SE DOBLAN SOBRE LA PIEDRA HACIA EL AGUJERO
    pygame.draw.ellipse(capa, personajes.AZUL_OSCURO, (x - 18, y - 6, 38, 34))
    pygame.draw.line(capa, personajes.AZUL, (x - 12, y + 2), (x + 10, y - 2), 2)
    for i in range(4):
        dedo = pygame.Rect(x + 12, y - 14 + i * 8, 16, 7)
        pygame.draw.rect(capa, personajes.PIEL_CHIBI, dedo, border_radius=3)
        pygame.draw.line(capa, personajes.PIEL_CHIBI_SOMBRA, (dedo.x + 4, dedo.bottom - 1), (dedo.right - 2, dedo.bottom - 1))
    pygame.draw.ellipse(capa, personajes.PIEL_CHIBI, (x - 6, y - 22, 12, 20))                    # el pulgar

    pegar_con_contorno(lienzo, capa)


def dibujar(ventana: pygame.Surface) -> None:

    """DIBUJA LA ESCENA COMPLETA EN LA VENTANA DEL JUEGO."""

    if "afuera" not in CAPAS:
        crear_capas()

    tiempo = pygame.time.get_ticks() / 1000
    centro = centro_de_la_piedra(tiempo)

    lienzo = CAPAS["afuera"].copy()

    # LO QUE SE VE POR EL AGUJERO: LA VISTA DE VERDAD CON LA BRASA, RECORTADA EN CIRCULO
    verdad = CAPAS["verdad"].copy()
    dibujar_brasa(verdad, tiempo)

    vista = pygame.Surface((RADIO_AGUJERO * 2, RADIO_AGUJERO * 2), pygame.SRCALPHA)
    vista.blit(verdad, (RADIO_AGUJERO - centro[0], RADIO_AGUJERO - centro[1]))
    vista.blit(CAPAS["mascara"], (0, 0), special_flags=pygame.BLEND_RGBA_MULT)
    lienzo.blit(vista, (centro[0] - RADIO_AGUJERO, centro[1] - RADIO_AGUJERO))

    piedra.dibujar_piedra(lienzo, centro[0], centro[1], RADIO_AGUJERO, BORDE_PIEDRA, 0)
    dibujar_mano(lienzo, centro)

    mostrar(ventana, lienzo)
