"""FONDO DIBUJADO CON CODIGO: EL ATICO DEL ANCIANO DE LOS RATONES.

Coraline sube al atico y el anciano del bigote le da el mensaje de los
ratones: que no cruce la puerta. El anciano es altisimo y flaco, de piel
verde azulada, con contorno oscuro como el sprite de Coraline: panza redonda
con camiseta sin mangas manchada y una medalla, shorts azul marino con raya
naranja, munequeras, una curita en la rodilla y botas negras con agujetas.
Cara larga con nariz caida, ojos con el parpado a la mitad y bigote de pelos
largos y delgados. Levanta un papel con un sello (el mensaje) y tiene la otra
mano en la cintura. A un lado, sobre una caja,
esta el circo de ratones que esta entrenando. Se usa en cap02_n02.

Coraline es la Coraline chica de personajes.py. El anciano se dibuja con el mismo
estilo que la mama (figuras con luz y sombra).

Lo que se mueve: el foco se apaga y prende un poquito, los ratones corren
sobre la caja y uno se asoma en el hombro del anciano, y el anciano parpadea.
"""

import math

import pygame

from interfaz.fondos.pintura import ANCHO, ALTO
from interfaz.fondos.pintura import mezclar, degradado, brillo, orillas_oscuras, mostrar
from interfaz.fondos import personajes

Y_PISO = 316

X_CORALINE = 446          # centro de sus pies

X_ANCIANO = 534           # centro de sus pies
OJOS_ANCIANO = [(529, 86), (541, 86)]
HOMBRO_ANCIANO = (556, 138)   # donde se asoma un raton
PAPEL = (486, 62)             # centro del papel con el mensaje

CAJA = pygame.Rect(584, 262, 50, Y_PISO - 262)    # caja del circo de ratones
FOCO = (500, 40)
TRAGALUZ = pygame.Rect(568, 40, 50, 40)

COLOR_MADERA = (92, 62, 44)
COLOR_MADERA_OSCURA = (54, 36, 28)
COLOR_PARED = (138, 112, 76)
COLOR_CONTORNO = (16, 22, 30)
COLOR_PIEL = (96, 170, 168)
COLOR_PIEL_SOMBRA = (66, 128, 132)
COLOR_PIEL_LUZ = (138, 204, 198)
COLOR_PELO = (30, 30, 36)
COLOR_CAMISETA = (238, 216, 172)
COLOR_CAMISETA_SOMBRA = (204, 178, 134)
COLOR_MANCHA = (222, 142, 62)
COLOR_SHORTS = (38, 60, 142)
COLOR_SHORTS_SOMBRA = (26, 40, 100)
COLOR_RAYA = (232, 150, 52)
COLOR_BOTAS = (28, 26, 32)
COLOR_MUNEQUERA = (44, 76, 176)
COLOR_RATON = (150, 146, 150)
COLOR_LUZ_FOCO = (255, 206, 130)

CAPAS = {}


# --------------------------------------------------
# PARTE FIJA: EL ATICO
# --------------------------------------------------

def dibujar_cuarto(lienzo: pygame.Surface) -> None:

    """PARED CON PAPEL VIEJO, TECHO INCLINADO CON VIGAS, TRAGALUZ Y PISO DE TABLAS."""

    degradado(lienzo, pygame.Rect(0, 0, ANCHO, Y_PISO), (70, 54, 40), COLOR_PARED, 16)

    # RAYAS DEL PAPEL TAPIZ
    for x in range(0, ANCHO, 16):
        pygame.draw.line(lienzo, mezclar(COLOR_PARED, (60, 40, 30), 0.25), (x, 60), (x, Y_PISO))

    # TECHO INCLINADO: BAJA HACIA LA IZQUIERDA
    techo = [(0, 0), (ANCHO, 0), (ANCHO, 30), (0, 150)]
    pygame.draw.polygon(lienzo, COLOR_MADERA_OSCURA, techo)

    for i in range(7):
        x = 40 + i * 95
        y = 150 - int(x * 120 / ANCHO)
        pygame.draw.line(lienzo, COLOR_MADERA, (x, 0), (x - 20, y), 6)

    pygame.draw.line(lienzo, COLOR_MADERA, (0, 150), (ANCHO, 30), 5)

    # TRAGALUZ CON CIELO GRIS
    pygame.draw.rect(lienzo, COLOR_MADERA, TRAGALUZ.inflate(8, 8))
    degradado(lienzo, TRAGALUZ, (176, 186, 196), (130, 144, 160), 4)
    pygame.draw.line(lienzo, COLOR_MADERA, TRAGALUZ.midtop, TRAGALUZ.midbottom, 3)

    # PISO DE TABLAS
    degradado(lienzo, pygame.Rect(0, Y_PISO, ANCHO, ALTO - Y_PISO), COLOR_MADERA, COLOR_MADERA_OSCURA, 4)

    for y in range(Y_PISO + 8, ALTO, 10):
        pygame.draw.line(lienzo, COLOR_MADERA_OSCURA, (0, y), (ANCHO, y))

    pygame.draw.rect(lienzo, COLOR_MADERA_OSCURA, (0, Y_PISO - 6, ANCHO, 6))

    # CABLE DEL FOCO
    pygame.draw.line(lienzo, (30, 24, 20), (FOCO[0], 0), (FOCO[0], FOCO[1] - 6))


def dibujar_caja_circo(lienzo: pygame.Surface) -> None:

    """CAJA DE MADERA CON UN BANDERIN DE RAYAS: EL CIRCO DE RATONES EN ENSAYO."""

    pygame.draw.rect(lienzo, (126, 88, 56), CAJA)
    pygame.draw.rect(lienzo, COLOR_MADERA_OSCURA, CAJA, 2)
    pygame.draw.line(lienzo, COLOR_MADERA_OSCURA, (CAJA.x, CAJA.centery), (CAJA.right, CAJA.centery))

    # PALITO Y BANDERIN DE RAYAS ROJAS Y BLANCAS
    x = CAJA.right - 10
    pygame.draw.line(lienzo, COLOR_MADERA_OSCURA, (x, CAJA.y), (x, CAJA.y - 34), 2)

    for i in range(4):
        color = (200, 50, 50) if i % 2 == 0 else (236, 230, 216)
        pygame.draw.rect(lienzo, color, (x - 18 + i * 4, CAJA.y - 34, 4, 12))

    # ESCALERITA DE PALITOS PARA LOS RATONES
    for i in range(4):
        pygame.draw.line(lienzo, (170, 130, 80), (CAJA.x + 6, CAJA.y - 4 - i * 6), (CAJA.x + 14, CAJA.y - 4 - i * 6))

    pygame.draw.line(lienzo, (170, 130, 80), (CAJA.x + 6, CAJA.y), (CAJA.x + 6, CAJA.y - 24))
    pygame.draw.line(lienzo, (170, 130, 80), (CAJA.x + 14, CAJA.y), (CAJA.x + 14, CAJA.y - 24))


# --------------------------------------------------
# PARTE FIJA: CORALINE Y EL ANCIANO
# --------------------------------------------------

def dibujar_sombra_piso(lienzo: pygame.Surface, x: int, ancho: int) -> None:

    """SOMBRA SUAVE EN EL PISO, CENTRADA EN x."""

    sombra = pygame.Surface((ancho, 8), pygame.SRCALPHA)
    pygame.draw.ellipse(sombra, (0, 0, 0, 110), sombra.get_rect())
    lienzo.blit(sombra, (x - ancho // 2, Y_PISO - 4))


def dibujar_coraline(lienzo: pygame.Surface) -> None:

    """CORALINE CHICA (personajes.py) MIRANDO A LA DERECHA."""

    personajes.dibujar_coraline_chica(lienzo, X_CORALINE, Y_PISO, True)


def linea_con_contorno(lienzo: pygame.Surface, color: tuple, inicio: tuple, fin: tuple, grueso: int) -> None:

    """LINEA GRUESA (BRAZO, PIERNA) CON CONTORNO OSCURO Y PUNTAS REDONDAS."""

    pygame.draw.line(lienzo, COLOR_CONTORNO, inicio, fin, grueso + 2)
    pygame.draw.circle(lienzo, COLOR_CONTORNO, inicio, grueso // 2 + 1)
    pygame.draw.circle(lienzo, COLOR_CONTORNO, fin, grueso // 2 + 1)
    pygame.draw.line(lienzo, color, inicio, fin, grueso)
    pygame.draw.circle(lienzo, color, inicio, grueso // 2)
    pygame.draw.circle(lienzo, color, fin, grueso // 2)


def poligono_con_contorno(lienzo: pygame.Surface, color: tuple, puntos: list) -> None:

    pygame.draw.polygon(lienzo, color, puntos)
    pygame.draw.polygon(lienzo, COLOR_CONTORNO, puntos, 1)


def elipse_con_contorno(lienzo: pygame.Surface, color: tuple, rect: tuple) -> None:

    pygame.draw.ellipse(lienzo, color, rect)
    pygame.draw.ellipse(lienzo, COLOR_CONTORNO, rect, 1)


def dibujar_piernas_anciano(lienzo: pygame.Surface, x: int) -> None:

    """PIERNAS FLACAS, CURITA EN LA RODILLA Y BOTAS NEGRAS CON AGUJETAS."""

    linea_con_contorno(lienzo, COLOR_PIEL, (x - 11, 220), (x - 11, 276), 7)
    linea_con_contorno(lienzo, COLOR_PIEL_SOMBRA, (x + 11, 220), (x + 11, 276), 7)

    # CURITA EN LA RODILLA IZQUIERDA
    pygame.draw.rect(lienzo, (226, 180, 130), (x - 15, 244, 9, 7))
    pygame.draw.rect(lienzo, COLOR_CONTORNO, (x - 15, 244, 9, 7), 1)
    pygame.draw.line(lienzo, (190, 140, 100), (x - 13, 247), (x - 8, 247))

    for dx in [-11, 11]:

        bota = pygame.Rect(x + dx - 8, 272, 16, 38)
        pygame.draw.rect(lienzo, COLOR_BOTAS, bota)
        pygame.draw.rect(lienzo, COLOR_CONTORNO, bota, 1)

        # AGUJETAS
        for y in range(276, 304, 5):
            pygame.draw.line(lienzo, (96, 96, 104), (x + dx - 3, y), (x + dx + 3, y))

        # SUELA
        pygame.draw.rect(lienzo, (50, 46, 52), (x + dx - 10, 308, 20, 7))
        pygame.draw.rect(lienzo, COLOR_CONTORNO, (x + dx - 10, 308, 20, 7), 1)


def dibujar_cuerpo_anciano(lienzo: pygame.Surface, x: int) -> None:

    """SHORTS, PANZA CON LA CAMISETA SIN MANGAS, MANCHAS Y MEDALLA."""

    # SHORTS AZUL MARINO CON RAYA NARANJA A LOS LADOS
    shorts = [(x - 24, 192), (x + 24, 192), (x + 23, 226), (x + 2, 226), (x, 214), (x - 2, 226), (x - 23, 226)]
    poligono_con_contorno(lienzo, COLOR_SHORTS, shorts)
    pygame.draw.polygon(lienzo, COLOR_SHORTS_SOMBRA, [(x + 12, 193), (x + 23, 193), (x + 22, 225), (x + 12, 225)])
    pygame.draw.line(lienzo, COLOR_RAYA, (x - 21, 196), (x - 20, 224), 2)
    pygame.draw.line(lienzo, COLOR_RAYA, (x + 20, 196), (x + 19, 224), 2)

    # PANCITA QUE SE ASOMA ENTRE LA CAMISETA Y EL SHORT, CON EL OMBLIGO
    elipse_con_contorno(lienzo, COLOR_PIEL, (x - 22, 180, 44, 16))
    pygame.draw.line(lienzo, COLOR_PIEL_SOMBRA, (x, 186), (x, 190))

    # CAMISETA: PARTE DE ARRIBA ANGOSTA Y PANZA REDONDA
    poligono_con_contorno(lienzo, COLOR_CAMISETA, [(x - 18, 138), (x + 18, 138), (x + 26, 160), (x - 26, 160)])
    elipse_con_contorno(lienzo, COLOR_CAMISETA, (x - 34, 148, 68, 40))
    pygame.draw.polygon(lienzo, COLOR_CAMISETA, [(x - 17, 139), (x + 17, 139), (x + 25, 160), (x - 25, 160)])

    # SOMBRA DE LA PANZA Y ORILLA DE ABAJO
    pygame.draw.ellipse(lienzo, COLOR_CAMISETA_SOMBRA, (x + 8, 154, 24, 32))
    pygame.draw.arc(lienzo, COLOR_CAMISETA_SOMBRA, (x - 32, 150, 64, 36), 3.6, 5.9, 2)

    # ESCOTE CON PELITOS EN EL PECHO
    pygame.draw.polygon(lienzo, COLOR_PIEL, [(x - 10, 138), (x + 10, 138), (x, 150)])
    pygame.draw.lines(lienzo, COLOR_CONTORNO, False, [(x - 10, 138), (x, 150), (x + 10, 138)])
    pygame.draw.line(lienzo, COLOR_PELO, (x - 4, 141), (x - 2, 144))
    pygame.draw.line(lienzo, COLOR_PELO, (x + 3, 141), (x + 1, 144))

    # MANCHAS NARANJAS
    for mancha in [(x - 16, 164, 8, 5), (x + 2, 172, 9, 6), (x - 22, 176, 6, 4), (x + 18, 160, 5, 4)]:
        pygame.draw.ellipse(lienzo, COLOR_MANCHA, mancha)

    # MEDALLA: LISTON AZUL Y ROJO Y MONEDA DORADA
    pygame.draw.rect(lienzo, (190, 50, 50), (x + 12, 144, 3, 7))
    pygame.draw.rect(lienzo, (44, 76, 176), (x + 15, 144, 3, 7))
    pygame.draw.circle(lienzo, (232, 186, 60), (x + 15, 155), 4)
    pygame.draw.circle(lienzo, COLOR_CONTORNO, (x + 15, 155), 4, 1)
    pygame.draw.circle(lienzo, (190, 50, 50), (x + 15, 155), 1)


def dibujar_brazos_anciano(lienzo: pygame.Surface, x: int) -> None:

    """UN BRAZO LEVANTA EL PAPEL; EL OTRO VA A LA CINTURA. CON MUNEQUERAS."""

    # BRAZO EN LA CINTURA (FORMA UN TRIANGULO)
    linea_con_contorno(lienzo, COLOR_PIEL_SOMBRA, (x + 22, 142), (x + 44, 172), 7)
    linea_con_contorno(lienzo, COLOR_PIEL_SOMBRA, (x + 44, 172), (x + 30, 196), 7)
    pygame.draw.rect(lienzo, COLOR_MUNEQUERA, (x + 33, 184, 8, 6))
    pygame.draw.line(lienzo, (240, 240, 236), (x + 33, 186), (x + 40, 186))

    # BRAZO LEVANTADO CON EL PAPEL
    linea_con_contorno(lienzo, COLOR_PIEL, (x - 22, 142), (x - 58, 124), 7)
    linea_con_contorno(lienzo, COLOR_PIEL, (x - 58, 124), (x - 46, 80), 7)
    pygame.draw.rect(lienzo, COLOR_MUNEQUERA, (x - 54, 88, 9, 6))
    pygame.draw.line(lienzo, (240, 240, 236), (x - 54, 90), (x - 46, 90))

    # PAPEL INCLINADO CON RENGLONES Y UN SELLO MORADO
    papel = pygame.Surface((30, 26), pygame.SRCALPHA)
    papel.fill((236, 220, 180))
    pygame.draw.rect(papel, COLOR_CONTORNO, papel.get_rect(), 1)

    for i in range(3):
        pygame.draw.line(papel, (150, 120, 100), (5, 6 + i * 5), (24 - i * 3, 6 + i * 5))

    pygame.draw.circle(papel, (120, 70, 150), (8, 20), 3)

    papel = pygame.transform.rotate(papel, 14)
    lienzo.blit(papel, (PAPEL[0] - papel.get_width() // 2, PAPEL[1] - papel.get_height() // 2))

    # MANO QUE LO SOSTIENE
    elipse_con_contorno(lienzo, COLOR_PIEL, (x - 52, 72, 12, 12))


def dibujar_cabeza_anciano(lienzo: pygame.Surface, x: int) -> None:

    """CUELLO GRUESO, CARA LARGA, NARIZ CAIDA Y BIGOTE DE PELOS LARGOS. OJOS APARTE."""

    # CUELLO GRUESO
    poligono_con_contorno(lienzo, COLOR_PIEL, [(x - 10, 108), (x + 10, 108), (x + 13, 140), (x - 13, 140)])
    pygame.draw.polygon(lienzo, COLOR_PIEL_SOMBRA, [(x + 4, 109), (x + 9, 109), (x + 12, 139), (x + 5, 139)])

    # CABEZA LARGA, UN POCO MAS ANCHA ABAJO
    poligono_con_contorno(
        lienzo,
        COLOR_PIEL,
        [(x - 9, 70), (x + 9, 70), (x + 14, 80), (x + 15, 112), (x + 8, 120), (x - 8, 120), (x - 14, 112), (x - 13, 80)]
    )
    pygame.draw.polygon(lienzo, COLOR_PIEL_SOMBRA, [(x + 9, 74), (x + 13, 80), (x + 14, 112), (x + 8, 118), (x + 8, 80)])
    pygame.draw.line(lienzo, COLOR_PIEL_LUZ, (x - 10, 80), (x - 11, 104))

    # OREJAS
    elipse_con_contorno(lienzo, COLOR_PIEL, (x - 18, 84, 6, 12))
    elipse_con_contorno(lienzo, COLOR_PIEL_SOMBRA, (x + 13, 84, 6, 12))

    # CEJAS PESADAS
    pygame.draw.line(lienzo, COLOR_CONTORNO, (x - 10, 81), (x - 1, 82), 2)
    pygame.draw.line(lienzo, COLOR_CONTORNO, (x + 3, 82), (x + 12, 81), 2)

    # NARIZ LARGA QUE CUELGA HASTA CASI LA BOCA
    poligono_con_contorno(lienzo, COLOR_PIEL_LUZ, [(x - 1, 84), (x + 3, 84), (x + 6, 104), (x + 2, 108), (x - 3, 106)])
    pygame.draw.line(lienzo, COLOR_PIEL_SOMBRA, (x + 4, 90), (x + 5, 104))

    # BOCA SERIA
    pygame.draw.line(lienzo, COLOR_CONTORNO, (x - 4, 114), (x + 5, 113))

    # BIGOTE: TRES PELOS LARGOS Y DELGADOS DE CADA LADO, QUE SE CURVAN HACIA ABAJO
    for i in range(3):

        for lado in [-1, 1]:

            puntos = [
                (x + lado * 3, 110),
                (x + lado * (14 + i * 3), 104 + i * 2),
                (x + lado * (28 + i * 4), 108 + i * 3),
                (x + lado * (34 + i * 4), 116 + i * 3)
            ]

            pygame.draw.lines(lienzo, (44, 40, 40), False, puntos)


def dibujar_anciano(lienzo: pygame.Surface) -> None:

    """ANCIANO ALTISIMO Y FLACO, CON CONTORNO OSCURO COMO EL SPRITE DE CORALINE."""

    x = X_ANCIANO

    dibujar_sombra_piso(lienzo, x, 60)
    dibujar_piernas_anciano(lienzo, x)
    dibujar_cuerpo_anciano(lienzo, x)
    dibujar_brazos_anciano(lienzo, x)
    dibujar_cabeza_anciano(lienzo, x)


def dibujar_luces(lienzo: pygame.Surface) -> None:

    """LUZ GRIS DEL TRAGALUZ Y ORILLAS OSCURAS (LA LUZ DEL FOCO VA APARTE)."""

    brillo(lienzo, TRAGALUZ.center, 90, (190, 206, 230), 40)

    orillas_oscuras(lienzo)


def crear_fijo() -> pygame.Surface:

    lienzo = pygame.Surface((ANCHO, ALTO))

    dibujar_cuarto(lienzo)
    dibujar_caja_circo(lienzo)
    dibujar_coraline(lienzo)
    dibujar_anciano(lienzo)
    dibujar_luces(lienzo)

    return lienzo


def crear_luz_foco() -> pygame.Surface:

    """LUZ CALIDA DEL FOCO EN SU PROPIA CAPA, PARA PODER HACERLA PARPADEAR."""

    capa = pygame.Surface((ANCHO, ALTO), pygame.SRCALPHA)

    brillo(capa, FOCO, 190, COLOR_LUZ_FOCO, 90)

    return capa


# --------------------------------------------------
# LO QUE SE MUEVE
# --------------------------------------------------

def dibujar_raton(lienzo: pygame.Surface, x: int, y: int, mira_derecha: bool) -> None:

    """RATONCITO GRIS DE PERFIL. (x, y) ES DONDE PISA."""

    direccion = 1 if mira_derecha else -1

    pygame.draw.ellipse(lienzo, COLOR_RATON, (x - 4, y - 5, 9, 5))
    pygame.draw.circle(lienzo, COLOR_RATON, (x + direccion * 5, y - 4), 2)
    pygame.draw.circle(lienzo, (220, 170, 180), (x + direccion * 4, y - 6), 1)    # oreja
    lienzo.set_at((x + direccion * 7, y - 4), (30, 20, 24))                       # nariz
    pygame.draw.line(lienzo, (200, 160, 170), (x - direccion * 4, y - 2), (x - direccion * 9, y - 4))   # cola


def dibujar_ratones(lienzo: pygame.Surface, tiempo: float) -> None:

    """DOS RATONES VAN Y VIENEN SOBRE LA CAJA; UNO SE ASOMA EN EL HOMBRO DEL ANCIANO."""

    for i in range(2):

        vaiven = math.sin(tiempo * 1.6 + i * 2.5)
        x = CAJA.x + 25 + int(vaiven * 16)
        mira_derecha = math.cos(tiempo * 1.6 + i * 2.5) > 0

        dibujar_raton(lienzo, x, CAJA.y, mira_derecha)

    # EL DEL HOMBRO SOLO SE ASOMA UN RATITO CADA 5 SEGUNDOS
    fase = tiempo % 5

    if fase < 2.5:
        asomado = min(fase, 2.5 - fase, 0.5) * 2
        dibujar_raton(lienzo, HOMBRO_ANCIANO[0] - 4 + int(asomado * 4), HOMBRO_ANCIANO[1], False)


def dibujar_ojos_anciano(lienzo: pygame.Surface, tiempo: float) -> None:

    """OJOS CON EL PARPADO A LA MITAD (CARA DE ABURRIDO). PARPADEA CADA 3.5 SEGUNDOS."""

    parpadea = (tiempo + 1) % 3.5 < 0.15

    for x, y in OJOS_ANCIANO:

        if parpadea:
            pygame.draw.line(lienzo, COLOR_CONTORNO, (x - 3, y), (x + 3, y))
            continue

        pygame.draw.rect(lienzo, (240, 236, 222), (x - 3, y - 1, 7, 4))
        pygame.draw.rect(lienzo, COLOR_CONTORNO, (x, y, 2, 3))

        # PARPADO DE ARRIBA A LA MITAD DEL OJO
        pygame.draw.rect(lienzo, COLOR_PIEL_SOMBRA, (x - 3, y - 2, 7, 2))
        pygame.draw.line(lienzo, COLOR_CONTORNO, (x - 3, y), (x + 3, y))


def dibujar_foco(lienzo: pygame.Surface, tiempo: float) -> None:

    """EL FOCO TITILA DE VEZ EN CUANDO, COMO SI LA CORRIENTE FUERA VIEJA."""

    if "luz_foco" not in CAPAS:
        CAPAS["luz_foco"] = crear_luz_foco()

    fase = tiempo % 6
    titila = 4.2 < fase < 4.5 and int(fase * 30) % 2 == 0

    if not titila:
        lienzo.blit(CAPAS["luz_foco"], (0, 0))

    color = (255, 236, 180) if not titila else (120, 100, 70)

    pygame.draw.rect(lienzo, (40, 34, 28), (FOCO[0] - 3, FOCO[1] - 8, 6, 4))
    pygame.draw.circle(lienzo, color, FOCO, 5)


def dibujar(ventana: pygame.Surface) -> None:

    """DIBUJA LA ESCENA COMPLETA EN LA VENTANA DEL JUEGO."""

    if "fijo" not in CAPAS:
        CAPAS["fijo"] = crear_fijo()

    tiempo = pygame.time.get_ticks() / 1000

    lienzo = CAPAS["fijo"].copy()

    dibujar_ratones(lienzo, tiempo)
    dibujar_ojos_anciano(lienzo, tiempo)
    dibujar_foco(lienzo, tiempo)

    mostrar(ventana, lienzo)
