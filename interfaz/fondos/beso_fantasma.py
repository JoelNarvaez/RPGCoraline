"""FONDO DIBUJADO CON CODIGO: UN BESO FANTASMA Y "MIRA A TRAVES DE LA PIEDRA".

Un acercamiento al piso del hueco detras del espejo (hueco_espejo.py). Coraline
duerme acostada de lado, hecha casi bolita porque no cabe, con la cabeza sobre
su sueter doblado y la piedra con agujero (piedra.py) entre las manos, junto
al pecho. La unica luz es la fria y azul que entra por el vidrio y la tibia de
la piedra. El fantasma mas pequeno baja hasta su mejilla, le da un beso y le
susurra al oido: el susurro son hilitos de aire que llegan a su oreja. Los
otros dos fantasmas apenas se adivinan en lo oscuro. Se usa en cap07_n05 y en
su rama cap07_r05 (volteada con "espejo", para que quede a la izquierda).

Como es un acercamiento, todo se dibuja al doble de tamaño: las medidas de
abajo estan "a tamano normal" y las funciones p(), r() y g() las agrandan
(AUMENTO) hacia la esquina de abajo a la derecha. Asi Coraline ocupa todo lo
ancho de abajo, que es lo que los paneles de texto dejan libre.

Coraline acostada esta dibujada aqui mismo (no es el sprite de pie girado):
pelo azul con el pasador, cara con los ojos cerrados, pecas y chapitas,
impermeable amarillo, medias a rayas y botas.

Lo que se mueve: Coraline respira (el pecho sube y baja), la piedra late
tibia, el fantasma baja a besarla (destellito en la mejilla), los hilitos del
susurro, las caras lejanas que aparecen y se borran, y polvo en la luz.
"""

import math

import pygame

from interfaz.fondos.pintura import ANCHO, ALTO
from interfaz.fondos.pintura import capa_vacia, pegar_con_contorno
from interfaz.fondos.pintura import mezclar, degradado, brillo, orillas_oscuras, mostrar
from interfaz.fondos import personajes
from interfaz.fondos import hueco_espejo
from interfaz.fondos import piedra

AUMENTO = 2
ANCLA = (632, 304)                 # este punto se queda en su lugar; lo demas se agranda alrededor
ANCLA_PANTALLA = (636, 332)        # y aqui queda en la pantalla (justo arriba de la barra de controles)

Y_PISO = 304
TECHO = 220
VIDRIO_X = 624

CABEZA = (444, 266)                # centro de la cara
PIEDRA = (480, 284)                # entre sus manos, junto al pecho
PECHO = (456, 252, 70, 46)         # lo que sube y baja al respirar
MEJILLA = (452, 270)

PELO = personajes.PELO
PELO_SOMBRA = personajes.PELO_SOMBRA
PELO_BRILLO = personajes.PELO_BRILLO
PIEL = personajes.PIEL
PIEL_SOMBRA = personajes.PIEL_SOMBRA

CAPAS = {}


# --------------------------------------------------
# DE MEDIDAS "NORMALES" A LA PANTALLA (AGRANDADO)
# --------------------------------------------------

def p(x: float, y: float) -> tuple:

    """UN PUNTO."""

    return (int(ANCLA_PANTALLA[0] + (x - ANCLA[0]) * AUMENTO), int(ANCLA_PANTALLA[1] + (y - ANCLA[1]) * AUMENTO))


def r(x: float, y: float, ancho: float, alto: float) -> pygame.Rect:

    """UN RECTANGULO."""

    esquina = p(x, y)

    return pygame.Rect(esquina[0], esquina[1], int(ancho * AUMENTO), int(alto * AUMENTO))


def g(grueso: float) -> int:

    """UN GROSOR O UN RADIO."""

    return max(1, int(grueso * AUMENTO))


# --------------------------------------------------
# PARTE FIJA
# --------------------------------------------------

def dibujar_hueco(lienzo: pygame.Surface) -> None:

    """EL PISO Y LAS TABLAS DEL HUECO DE CERCA, MUY OSCURO, CON EL VIDRIO A LA DERECHA."""

    lienzo.fill(hueco_espejo.COLOR_NEGRO)

    pared = pygame.Rect(0, p(0, TECHO)[1], p(VIDRIO_X, 0)[0], p(0, Y_PISO)[1] - p(0, TECHO)[1])
    degradado(lienzo, pared, (12, 10, 14), (36, 30, 34), 8)

    for y in range(pared.y + 22, pared.bottom, 30):
        pygame.draw.line(lienzo, (16, 12, 16), (0, y), (pared.right, y), 2)
        pygame.draw.line(lienzo, (46, 40, 42), (0, y + 2), (pared.right, y + 2))
        for x in range((y * 13) % 120, pared.right, 150):
            pygame.draw.line(lienzo, (16, 12, 16), (x, y), (x, min(y + 30, pared.bottom)), 2)

    # PISO DE TABLAS
    piso = p(0, Y_PISO)[1]
    degradado(lienzo, pygame.Rect(0, piso, ANCHO, ALTO - piso), (44, 34, 34), (20, 16, 18), 3)

    # EL VIDRIO FRIO: AZULADO, CON REFLEJOS
    vidrio = pygame.Rect(pared.right, pared.y - 20, ANCHO - pared.right, pared.height + 20)
    degradado(lienzo, vidrio, (70, 86, 116), (40, 50, 72), 6)
    pygame.draw.line(lienzo, (150, 170, 204), (vidrio.x + 4, vidrio.y + 60), (vidrio.x + 12, vidrio.y + 26), 2)
    pygame.draw.line(lienzo, (110, 126, 160), (vidrio.x, vidrio.y), (vidrio.x, vidrio.bottom), 2)


def dibujar_sueter(capa: pygame.Surface) -> None:

    """EL SUETER GRIS DOBLADO QUE USA DE ALMOHADA, CON PUNTO TEJIDO Y UNA MANGA COLGANDO."""

    pygame.draw.rect(capa, (104, 106, 118), r(404, 280, 64, 22), border_radius=g(5))
    pygame.draw.rect(capa, (88, 90, 102), r(404, 292, 64, 10), border_radius=g(4))
    pygame.draw.line(capa, (128, 130, 142), p(408, 284), p(462, 284), g(1))
    for x in range(408, 466, 3):
        pygame.draw.line(capa, (92, 94, 106), p(x, 286), p(x + 1, 290), 2)
    pygame.draw.polygon(capa, (96, 98, 110), [p(404, 294), p(394, 300), p(398, Y_PISO), p(412, 300)])          # manga


def dibujar_pierna(capa: pygame.Surface, inicio: tuple, fin: tuple) -> None:

    """UN PEDAZO DE PIERNA CON LAS MEDIAS A RAYAS ROSA Y AZUL."""

    pygame.draw.line(capa, (150, 80, 120), p(*inicio), p(*fin), g(9))
    pasos = 8
    for i in range(pasos):
        x = inicio[0] + (fin[0] - inicio[0]) * (i + 0.5) / pasos
        y = inicio[1] + (fin[1] - inicio[1]) * (i + 0.5) / pasos
        color = (60, 70, 140) if i % 2 else (230, 140, 170)
        pygame.draw.line(capa, color, p(x - 0.5, y - 4), p(x + 0.5, y + 4), g(2))


def dibujar_cuerpo(capa: pygame.Surface) -> None:

    """EL CUERPO ACOSTADO DE LADO, UN POCO HECHO BOLITA: IMPERMEABLE, MEDIAS A RAYAS Y BOTAS."""

    amarillo = personajes.AMARILLO
    sombra = personajes.AMARILLO_SOMBRA
    luz = personajes.AMARILLO_CLARO

    # LA PIERNA DE ATRAS, MAS OSCURA, Y LA DE ADELANTE DOBLADA (MUSLO Y ESPINILLA)
    pygame.draw.line(capa, (90, 50, 80), p(518, 297), p(560, 299), g(8))
    pygame.draw.rect(capa, mezclar(amarillo, (0, 0, 0), 0.35), r(556, 293, 18, 10), border_radius=g(4))
    dibujar_pierna(capa, (520, 290), (552, 280))
    dibujar_pierna(capa, (552, 280), (572, 295))

    # BOTA DE ADELANTE
    pygame.draw.rect(capa, amarillo, r(566, 287, 20, 14), border_radius=g(4))
    pygame.draw.rect(capa, sombra, r(566, 297, 22, 4))
    pygame.draw.line(capa, luz, p(569, 289), p(582, 289), g(1))

    # EL IMPERMEABLE: TORSO DE LADO, CAPUCHA DETRAS DEL CUELLO Y LA FALDA DEL ABRIGO
    pygame.draw.ellipse(capa, amarillo, r(456, 256, 70, 42))
    pygame.draw.ellipse(capa, sombra, r(462, 282, 64, 16))
    pygame.draw.polygon(capa, amarillo, [p(512, 266), p(534, 284), p(526, 300), p(504, 298)])
    pygame.draw.polygon(capa, sombra, [p(522, 290), p(534, 284), p(526, 300)])
    pygame.draw.ellipse(capa, sombra, r(452, 260, 24, 11))                                          # capucha caida
    pygame.draw.ellipse(capa, mezclar(sombra, (0, 0, 0), 0.2), r(456, 263, 16, 6))
    pygame.draw.arc(capa, luz, r(464, 258, 52, 28), 1.0, 2.6, g(1))                                 # brillo del hule
    for x in [490, 500, 510]:
        pygame.draw.circle(capa, (130, 90, 24), p(x, 266), g(1))                                    # botones
    pygame.draw.line(capa, sombra, p(484, 262), p(516, 268), g(1))


def dibujar_brazo_y_manos(capa: pygame.Surface) -> None:

    """EL BRAZO DOBLADO HACIA EL PECHO Y LAS MANOS (GUANTES AZULES SIN DEDOS) JUNTITAS, CON LA PIEDRA ENTRE ELLAS."""

    pygame.draw.line(capa, personajes.AMARILLO, p(474, 266), p(490, 282), g(9))
    pygame.draw.line(capa, personajes.AMARILLO_SOMBRA, p(477, 273), p(489, 285), g(2))
    pygame.draw.rect(capa, personajes.AMARILLO_SOMBRA, r(484, 278, 10, 6), border_radius=g(2))   # puno
    pygame.draw.ellipse(capa, personajes.AZUL_OSCURO, r(484, 282, 12, 10))
    pygame.draw.ellipse(capa, personajes.AZUL_OSCURO, r(466, 284, 12, 9))
    pygame.draw.line(capa, personajes.AZUL, p(486, 284), p(493, 284), g(1))
    for x, y in [(469, 291), (472, 292), (475, 292), (486, 290), (489, 291), (492, 291)]:
        pygame.draw.circle(capa, PIEL, p(x, y), g(1.4))                                              # puntas de los dedos


def dibujar_cabeza(capa: pygame.Surface) -> None:

    """LA CABEZA SOBRE EL SUETER: PELO AZUL QUE SE DESPARRAMA, CARA DORMIDA, PECAS Y EL PASADOR."""

    cx, cy = CABEZA

    # PELO DE ATRAS, QUE CAE SOBRE EL SUETER EN MECHONES
    pygame.draw.ellipse(capa, PELO_SOMBRA, r(cx - 26, cy - 22, 46, 40))
    for dx in [-30, -24, -18]:
        pygame.draw.polygon(capa, PELO_SOMBRA, [p(cx + dx + 6, cy + 4), p(cx + dx, cy + 16), p(cx + dx + 8, cy + 14), p(cx + dx + 12, cy + 6)])

    # CARA (DE TRES CUARTOS, MIRANDO UN POCO HACIA ARRIBA), MEJILLA APLASTADA EN LA ALMOHADA Y OREJA
    pygame.draw.ellipse(capa, PIEL, r(cx - 10, cy - 12, 26, 26))
    pygame.draw.ellipse(capa, PIEL_SOMBRA, r(cx - 6, cy + 10, 16, 4))
    pygame.draw.ellipse(capa, PIEL, r(cx - 14, cy - 2, 6, 8))
    pygame.draw.arc(capa, PIEL_SOMBRA, r(cx - 13, cy, 4, 5), 1.5, 4.7, g(1))

    # FLECO QUE CAE DE LADO SOBRE LA FRENTE, CON MECHONES Y BRILLOS
    pygame.draw.polygon(capa, PELO, [p(cx - 22, cy - 18), p(cx + 4, cy - 22), p(cx + 18, cy - 14), p(cx + 15, cy - 6),
                                     p(cx + 9, cy - 9), p(cx + 4, cy - 6), p(cx - 2, cy - 9), p(cx - 8, cy - 3),
                                     p(cx - 18, cy - 4)])
    pygame.draw.line(capa, PELO_BRILLO, p(cx - 16, cy - 16), p(cx + 2, cy - 19), g(1.5))
    pygame.draw.line(capa, PELO_BRILLO, p(cx + 6, cy - 17), p(cx + 12, cy - 13), g(1))
    pygame.draw.line(capa, PELO_SOMBRA, p(cx + 2, cy - 18), p(cx - 1, cy - 9), g(1))

    # PASADOR DE LIBELULA
    pygame.draw.line(capa, personajes.PASADOR, p(cx - 15, cy - 14), p(cx - 5, cy - 16), g(1.5))
    for dx in [-13, -9]:
        pygame.draw.ellipse(capa, (200, 230, 240), r(cx + dx, cy - 21, 4, 4))

    # OJOS CERRADOS (CURVITAS CON PESTANAS), CEJAS, NARIZ, BOCA ENTREABIERTA, CHAPITAS Y PECAS
    for ox in [cx - 2, cx + 8]:
        pygame.draw.arc(capa, personajes.PESTANAS, r(ox - 3, cy - 3, 7, 5), 3.4, 6.0, g(1))
        for i in range(3):
            pygame.draw.line(capa, personajes.PESTANAS, p(ox - 2 + i * 2, cy), p(ox - 2 + i * 2, cy + 1.2))
        pygame.draw.arc(capa, personajes.CEJAS, r(ox - 3, cy - 8, 7, 4), 0.4, 2.7, 1)
    pygame.draw.line(capa, PIEL_SOMBRA, p(cx + 4, cy + 1), p(cx + 5, cy + 4), 1)
    pygame.draw.ellipse(capa, personajes.LABIOS, r(cx + 2, cy + 6, 4, 2))
    for x, y in [(cx - 4, cy + 4), (cx + 12, cy + 3)]:
        pygame.draw.circle(capa, (240, 160, 150), p(x, y), g(2))
    for x, y in [(cx - 2, cy + 2), (cx, cy + 3), (cx + 10, cy + 1), (cx + 12, cy + 1), (cx + 11, cy + 2)]:
        pygame.draw.rect(capa, personajes.PECAS, (*p(x, y), 2, 2))


def crear_fijo() -> pygame.Surface:

    lienzo = pygame.Surface((ANCHO, ALTO))
    dibujar_hueco(lienzo)

    capa = capa_vacia()
    dibujar_sueter(capa)
    pegar_con_contorno(lienzo, capa)

    capa = capa_vacia()
    dibujar_cuerpo(capa)
    dibujar_cabeza(capa)
    dibujar_brazo_y_manos(capa)
    pegar_con_contorno(lienzo, capa)

    # SOLO HAY LUZ FRIA DEL VIDRIO: TODO SE PONE AZULADO Y MAS OSCURO
    tinte = pygame.Surface((ANCHO, ALTO))
    tinte.fill((150, 156, 196))
    lienzo.blit(tinte, (0, 0), special_flags=pygame.BLEND_MULT)
    brillo(lienzo, (ANCHO - 10, 260), 150, (90, 110, 170), 50)

    orillas_oscuras(lienzo)

    # LA RESPIRACION MUEVE ESTE PEDAZO (EL PECHO), ASI QUE SE GUARDA APARTE
    pecho = r(*PECHO)
    CAPAS["pecho"] = (lienzo.subsurface(pecho).copy(), pecho.topleft)

    return lienzo


# --------------------------------------------------
# LO QUE SE MUEVE
# --------------------------------------------------

def dibujar_respiracion(lienzo: pygame.Surface, tiempo: float) -> None:

    """EL PECHO SUBE TANTITO AL TOMAR AIRE (RESPIRA DESPACIO, DORMIDA)."""

    if math.sin(tiempo * 1.4) > 0.2:
        imagen, (x, y) = CAPAS["pecho"]
        lienzo.blit(imagen, (x, y - 2))


def dibujar_luz_piedra(lienzo: pygame.Surface, tiempo: float) -> None:

    """LA LUZ TIBIA DE LA PIEDRA: SE SUMA A LO QUE ALUMBRA (MANOS Y PECHO) Y LATE COMO SI ESTUVIERA VIVA."""

    late = (math.sin(tiempo * 1.6) + 1) / 2
    centro = p(*PIEDRA)

    if "luz" not in CAPAS:
        luz = pygame.Surface((120, 120))
        for i in range(30):
            radio = 60 - i * 2
            tono = int((i / 30) ** 2 * 70)
            pygame.draw.circle(luz, (tono, int(tono * 0.6), int(tono * 0.15)), (60, 60), radio)
        CAPAS["luz"] = luz

    luz = CAPAS["luz"].copy()
    luz.fill((int(170 + late * 85),) * 3, special_flags=pygame.BLEND_MULT)
    lienzo.blit(luz, (centro[0] - 60, centro[1] - 60), special_flags=pygame.BLEND_ADD)

    piedra.dibujar_piedra(lienzo, centro[0], centro[1], 3, 5, 0)


def bajada_del_fantasma(tiempo: float) -> float:

    """0 = ARRIBA, 1 = PEGADO A SU MEJILLA. BAJA DESPACIO, SE QUEDA UN MOMENTO Y SUBE."""

    fase = tiempo % 7

    if fase < 2.5:
        avance = fase / 2.5
    elif fase < 4.0:
        avance = 1.0
    elif fase < 6.0:
        avance = 1 - (fase - 4.0) / 2.0
    else:
        avance = 0.0

    return avance * avance * (3 - 2 * avance)


def dibujar_fantasma(lienzo: pygame.Surface, tiempo: float) -> None:

    """EL FANTASMA PEQUENO: CABECITA PALIDA QUE SE INCLINA SOBRE ELLA Y UNA COLA DE NIEBLA QUE SE DESHACE HACIA ARRIBA."""

    baja = bajada_del_fantasma(tiempo)
    cabeza = p(MEJILLA[0] + 7, 230 + baja * 26)
    color = hueco_espejo.COLOR_FANTASMA

    capa = pygame.Surface((ANCHO, ALTO), pygame.SRCALPHA)

    # COLA DE NIEBLA: UNA FRANJA QUE SE ADELGAZA Y SE ONDULA, CADA VEZ MAS TRANSPARENTE
    for i in range(40):
        avance = i / 40
        x = cabeza[0] + int(math.sin(avance * 4 + tiempo * 1.5) * 6 * avance) + int(avance * 30)
        y = cabeza[1] - 14 - int(avance * 80)
        ancho = int(22 * (1 - avance) + 4)
        pygame.draw.ellipse(capa, (*color, int(60 * (1 - avance))), (x - ancho // 2, y - 4, ancho, 8))

    # CABECITA CON UN BRILLO SUAVE ALREDEDOR (VARIOS CIRCULOS CADA VEZ MAS CLAROS HACIA EL CENTRO)
    for i in range(6):
        pygame.draw.circle(capa, (*color, 8), cabeza, 28 - i * 2)
    pygame.draw.circle(capa, (*color, 190), cabeza, 16)
    for dx in [-7, 4]:
        pygame.draw.ellipse(capa, (*hueco_espejo.COLOR_FANTASMA_OJOS, 170), (cabeza[0] + dx, cabeza[1] - 3, 4, 6))
    pygame.draw.arc(capa, (*hueco_espejo.COLOR_FANTASMA_OJOS, 150), (cabeza[0] - 4, cabeza[1] + 5, 8, 5), 3.5, 5.9, 1)

    lienzo.blit(capa, (0, 0))

    # LUZ PALIDA QUE ECHA SOBRE LA CARA DE CORALINE CUANDO ESTA CERCA
    tono = int(baja * 34)
    if tono > 0:
        reflejo = pygame.Surface((90, 90))
        pygame.draw.circle(reflejo, (tono // 2, tono // 2, tono // 2), (45, 45), 44)
        pygame.draw.circle(reflejo, (tono, tono, int(tono * 1.2)), (45, 45), 28)
        cara = p(*CABEZA)
        lienzo.blit(reflejo, (cara[0] - 45, cara[1] - 45), special_flags=pygame.BLEND_ADD)

    # EL BESO: UN DESTELLITO EN LA MEJILLA MIENTRAS ESTA PEGADO A ELLA
    fase = tiempo % 7
    if 2.6 < fase < 3.6:
        mejilla = p(*MEJILLA)
        largo = 3 + int(math.sin((fase - 2.6) * math.pi) * 6)
        for dx, dy in [(-1, 0), (1, 0), (0, -1), (0, 1)]:
            pygame.draw.line(lienzo, (240, 244, 255), mejilla, (mejilla[0] + dx * largo, mejilla[1] + dy * largo))


def dibujar_susurro(lienzo: pygame.Surface, tiempo: float) -> None:

    """EL SUSURRO: HILITOS DE AIRE PALIDO QUE SALEN DEL FANTASMA Y SE ENROSCAN HACIA SU OREJA."""

    fase = tiempo % 7

    if fase < 3.6 or fase > 6.2:
        return

    capa = pygame.Surface((ANCHO, ALTO), pygame.SRCALPHA)
    boca = p(MEJILLA[0] + 4, 246)
    oreja = p(CABEZA[0] - 12, CABEZA[1] + 2)

    for i in range(3):
        avance = (tiempo * 0.8 + i / 3) % 1
        puntos = []
        for paso in range(14):
            t = paso / 13 * avance
            x = boca[0] + (oreja[0] - boca[0]) * t
            y = boca[1] + (oreja[1] - boca[1]) * t + math.sin(t * 9 + i * 2) * 5 - math.sin(t * math.pi) * 22
            puntos.append((x, y))
        pygame.draw.lines(capa, (210, 220, 245, int(150 * (1 - avance * 0.6))), False, puntos)

    lienzo.blit(capa, (0, 0))


def dibujar_lejanos(lienzo: pygame.Surface, tiempo: float) -> None:

    """LOS OTROS DOS FANTASMAS: SOLO SUS CARAS, MUY TENUES, QUE APARECEN EN LO OSCURO Y SE BORRAN."""

    for i, (x, y) in enumerate([(560, 210), (600, 196)]):
        alfa = int(max(0.0, math.sin(tiempo * 0.5 + i * 2)) * 55)
        if alfa == 0:
            continue
        capa = pygame.Surface((24, 28), pygame.SRCALPHA)
        pygame.draw.ellipse(capa, (*hueco_espejo.COLOR_FANTASMA, alfa), (2, 1, 20, 26))
        pygame.draw.rect(capa, (*hueco_espejo.COLOR_FANTASMA_OJOS, alfa), (7, 10, 3, 4))
        pygame.draw.rect(capa, (*hueco_espejo.COLOR_FANTASMA_OJOS, alfa), (14, 10, 3, 4))
        lienzo.blit(capa, (x - 12, y - 14))


def dibujar_polvo(lienzo: pygame.Surface, tiempo: float) -> None:

    """MOTITAS DE POLVO FLOTANDO EN LA LUZ DEL VIDRIO."""

    for i in range(10):
        x = ANCHO - 30 - (i * 17 + int(tiempo * 3)) % 140
        y = 190 + (i * 23) % 120 + int(math.sin(tiempo * 0.7 + i) * 5)
        lienzo.set_at((x, y), (110, 126, 164))


def dibujar(ventana: pygame.Surface) -> None:

    """DIBUJA LA ESCENA COMPLETA EN LA VENTANA DEL JUEGO."""

    if "fijo" not in CAPAS:
        CAPAS["fijo"] = crear_fijo()

    tiempo = pygame.time.get_ticks() / 1000

    lienzo = CAPAS["fijo"].copy()

    dibujar_respiracion(lienzo, tiempo)
    dibujar_lejanos(lienzo, tiempo)
    dibujar_polvo(lienzo, tiempo)
    dibujar_luz_piedra(lienzo, tiempo)
    dibujar_fantasma(lienzo, tiempo)
    dibujar_susurro(lienzo, tiempo)

    mostrar(ventana, lienzo)
