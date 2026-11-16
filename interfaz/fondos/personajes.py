"""PARTES DE PERSONAJES QUE SE REPITEN EN VARIOS FONDOS.

Coraline (varias versiones), la mama, la senorita Spink, la senorita
Forcible, los perritos negros y los otros padres con ojos de boton. La cabeza de Coraline va casi de frente. Asi su cara es la misma en
todas las escenas donde sale grande. Es sencilla a proposito: cara ancha,
ojos grandes, redondos y separados, cejas un poco levantadas, fleco recto
casi hasta las cejas, nariz chiquita, sonrisa pequena y pasador de estrella.

Archivo compartido: si se cambia algo aqui, avisar al otro.
"""

import math

import pygame

from interfaz.fondos.pintura import armar_sprite

PELO = (34, 42, 172)
PELO_SOMBRA = (22, 26, 118)
PELO_BRILLO = (74, 96, 222)
PIEL = (232, 184, 150)
PIEL_SOMBRA = (204, 152, 120)
PECAS = (186, 124, 96)
CEJAS = (60, 44, 70)
OJO_BLANCO = (248, 244, 236)
IRIS = (120, 76, 48)
PUPILA = (34, 22, 20)
PESTANAS = (40, 26, 34)
LABIOS = (186, 82, 84)
PASADOR = (246, 196, 60)

# CENTRO DE CADA OJO DENTRO DE LA CABEZA: GRANDES Y MUY SEPARADOS
OJOS = [(21, 35), (41, 35)]
ANCHO_OJO = 9
ALTO_OJO = 8


def dibujar_cabeza_coraline(lienzo: pygame.Surface, x: int, y: int, expresion: str) -> None:

    """DIBUJA LA CABEZA DE CORALINE. (x, y) ES LA ESQUINA DE ARRIBA A LA IZQUIERDA.

    Ocupa unos 60 x 60 pixeles del lienzo. expresion puede ser "curiosa"
    (mira a la derecha y sonrie) o "susto" (pupilas chiquitas y boca abierta).
    """

    # MELENA: CUPULA Y DOS MECHONES A LOS LADOS DE LA CARA
    pygame.draw.ellipse(lienzo, PELO, (x, y, 62, 50))
    pygame.draw.rect(lienzo, PELO, (x, y + 18, 12, 36), border_bottom_left_radius=8)
    pygame.draw.rect(lienzo, PELO, (x + 50, y + 18, 12, 34), border_bottom_right_radius=8)

    # CARA ANCHA
    pygame.draw.ellipse(lienzo, PIEL, (x + 7, y + 14, 48, 42))
    pygame.draw.arc(lienzo, PIEL_SOMBRA, (x + 7, y + 14, 48, 42), 3.6, 5.8, 1)

    # OJOS GRANDES Y REDONDOS
    for ojo_x, ojo_y in OJOS:

        ojo = pygame.Rect(x + ojo_x - ANCHO_OJO // 2, y + ojo_y - ALTO_OJO // 2, ANCHO_OJO, ALTO_OJO)

        pygame.draw.ellipse(lienzo, OJO_BLANCO, ojo)

        if expresion == "susto":
            pygame.draw.circle(lienzo, IRIS, ojo.center, 2)
            ceja_arriba = 6
        else:
            pygame.draw.circle(lienzo, IRIS, (ojo.centerx + 1, ojo.centery), 3)
            pygame.draw.circle(lienzo, PUPILA, (ojo.centerx + 1, ojo.centery), 1)
            lienzo.set_at((ojo.centerx + 2, ojo.centery - 2), (255, 255, 255))
            ceja_arriba = 4

        # LINEA DE ARRIBA DEL OJO (POR FUERA DEL BLANCO)
        pygame.draw.arc(lienzo, PESTANAS, ojo.inflate(2, 2), 0.5, 2.65, 1)

        # CEJA UN POCO LEVANTADA HACIA EL CENTRO DE LA CARA
        if ojo_x < 30:
            ceja = [(ojo.x, ojo.y - ceja_arriba + 3), (ojo.right - 1, ojo.y - ceja_arriba)]
        else:
            ceja = [(ojo.x, ojo.y - ceja_arriba), (ojo.right - 1, ojo.y - ceja_arriba + 3)]

        pygame.draw.line(lienzo, CEJAS, ceja[0], ceja[1], 2)

    # NARIZ CHIQUITA Y DOS PECAS
    pygame.draw.line(lienzo, PIEL_SOMBRA, (x + 30, y + 42), (x + 33, y + 42))
    lienzo.set_at((x + 14, y + 44), PECAS)
    lienzo.set_at((x + 48, y + 44), PECAS)

    # BOCA
    if expresion == "susto":
        pygame.draw.ellipse(lienzo, LABIOS, (x + 28, y + 47, 6, 6))
    else:
        # SONRISA PEQUENA CON LA BOCA CERRADA, UN POCO MAS ALTA DE UN LADO
        pygame.draw.lines(lienzo, LABIOS, False, [(x + 26, y + 47), (x + 29, y + 49), (x + 34, y + 49),
                                                  (x + 37, y + 46)], 2)

    # FLECO RECTO QUE BAJA CASI HASTA LAS CEJAS
    pygame.draw.polygon(
        lienzo,
        PELO,
        [(x + 4, y + 22), (x + 10, y + 6), (x + 30, y + 1), (x + 52, y + 6), (x + 58, y + 22),
         (x + 50, y + 24), (x + 40, y + 22), (x + 30, y + 24), (x + 20, y + 22), (x + 12, y + 25)]
    )
    pygame.draw.arc(lienzo, PELO_BRILLO, (x + 8, y + 2, 40, 22), 1.5, 2.9, 2)

    # PASADOR DE ESTRELLA
    centro = (x + 10, y + 16)
    puntas = []

    for i in range(10):
        radio = 4 if i % 2 == 0 else 2
        angulo = -1.5708 + i * 0.6283
        puntas.append((centro[0] + radio * math.cos(angulo), centro[1] + radio * math.sin(angulo)))

    pygame.draw.polygon(lienzo, PASADOR, puntas)


def cerrar_ojos_coraline(lienzo: pygame.Surface, x: int, y: int) -> None:

    """DIBUJA LOS OJOS CERRADOS ENCIMA (PARA PARPADEAR). MISMA (x, y) QUE LA CABEZA."""

    for ojo_x, ojo_y in OJOS:

        ojo = pygame.Rect(x + ojo_x - ANCHO_OJO // 2, y + ojo_y - ALTO_OJO // 2, ANCHO_OJO, ALTO_OJO)

        pygame.draw.ellipse(lienzo, PIEL, ojo.inflate(4, 4))
        pygame.draw.arc(lienzo, PESTANAS, (ojo.x, ojo.centery - 3, ojo.width, 6), 3.4, 6.0, 2)


# --------------------------------------------------
# CORALINE DE CUERPO COMPLETO CON IMPERMEABLE (ESTILO CHIBI)
# --------------------------------------------------

AMARILLO = (225, 174, 28)
AMARILLO_CLARO = (255, 211, 67)
AMARILLO_SOMBRA = (159, 111, 19)
AZUL_OSCURO = (17, 31, 83)
AZUL = (29, 58, 133)
AZUL_CLARO = (67, 105, 183)
PIEL_CHIBI = (231, 184, 151)
PIEL_CHIBI_SOMBRA = (190, 137, 117)
BLANCO = (240, 242, 235)


def dibujar_coraline_impermeable(lienzo: pygame.Surface, x: int, y: int, con_cabeza: bool = True) -> None:

    """CORALINE CHIBI CON IMPERMEABLE AMARILLO. (x, y) ES EL CENTRO DE LOS PIES.

    Mide unos 185 pixeles de alto y 76 de ancho en el lienzo. Con
    con_cabeza = False solo dibuja el cuerpo (para ponerle otra cabeza encima).
    """

    # SOMBRA EN EL SUELO
    pygame.draw.ellipse(lienzo, (13, 24, 43), (x - 31, y - 5, 64, 10))

    # PIERNAS
    pygame.draw.rect(lienzo, (24, 48, 88), (x - 15, y - 58, 12, 34))
    pygame.draw.rect(lienzo, (24, 48, 88), (x + 4, y - 58, 12, 34))
    pygame.draw.rect(lienzo, (16, 34, 69), (x - 15, y - 35, 12, 8))
    pygame.draw.rect(lienzo, (16, 34, 69), (x + 4, y - 35, 12, 8))

    # BOTAS AMARILLAS
    pygame.draw.polygon(lienzo, AMARILLO_SOMBRA, [(x - 17, y - 31), (x - 4, y - 31), (x - 4, y - 13),
                                                  (x + 1, y - 7), (x - 2, y - 2), (x - 28, y - 2),
                                                  (x - 27, y - 8), (x - 19, y - 13)])
    pygame.draw.polygon(lienzo, AMARILLO_CLARO, [(x - 15, y - 31), (x - 6, y - 31), (x - 7, y - 14),
                                                 (x - 2, y - 8), (x - 4, y - 5), (x - 25, y - 5),
                                                 (x - 23, y - 10), (x - 16, y - 15)])
    pygame.draw.polygon(lienzo, AMARILLO_SOMBRA, [(x + 3, y - 31), (x + 16, y - 31), (x + 17, y - 14),
                                                  (x + 24, y - 8), (x + 21, y - 2), (x - 1, y - 2),
                                                  (x - 1, y - 8), (x + 4, y - 14)])
    pygame.draw.polygon(lienzo, AMARILLO_CLARO, [(x + 5, y - 31), (x + 14, y - 31), (x + 15, y - 14),
                                                 (x + 21, y - 8), (x + 18, y - 5), (x + 2, y - 5),
                                                 (x + 2, y - 10), (x + 6, y - 15)])
    pygame.draw.line(lienzo, (255, 230, 125), (x - 14, y - 24), (x - 14, y - 14), 2)
    pygame.draw.line(lienzo, (255, 230, 125), (x + 7, y - 24), (x + 7, y - 14), 2)

    # CUELLO
    pygame.draw.rect(lienzo, PIEL_CHIBI_SOMBRA, (x - 7, y - 112, 15, 17))
    pygame.draw.rect(lienzo, PIEL_CHIBI, (x - 6, y - 113, 13, 15))

    # IMPERMEABLE: SILUETA Y CUERPO
    pygame.draw.polygon(lienzo, AMARILLO_SOMBRA, [(x - 24, y - 108), (x + 23, y - 108), (x + 32, y - 52),
                                                  (x + 26, y - 39), (x - 25, y - 39), (x - 32, y - 53)])
    pygame.draw.polygon(lienzo, AMARILLO, [(x - 21, y - 108), (x + 20, y - 108), (x + 27, y - 54),
                                           (x + 22, y - 43), (x - 21, y - 43), (x - 27, y - 55)])
    pygame.draw.polygon(lienzo, AMARILLO_CLARO, [(x - 18, y - 104), (x - 5, y - 107), (x - 9, y - 48),
                                                 (x - 20, y - 47), (x - 24, y - 56)])

    # COSTURAS Y BOTONES
    pygame.draw.line(lienzo, (255, 220, 93), (x + 1, y - 101), (x + 3, y - 46), 1)

    for y_boton in [y - 91, y - 78, y - 65, y - 52]:
        pygame.draw.circle(lienzo, (132, 93, 22), (x + 5, y_boton), 1)

    # BOLSILLOS
    pygame.draw.line(lienzo, (178, 127, 25), (x - 17, y - 67), (x - 5, y - 62), 2)
    pygame.draw.line(lienzo, (178, 127, 25), (x + 12, y - 67), (x + 22, y - 72), 2)

    # BRAZOS Y MANOS AL FRENTE
    pygame.draw.line(lienzo, AMARILLO_SOMBRA, (x - 20, y - 99), (x - 28, y - 77), 9)
    pygame.draw.line(lienzo, AMARILLO, (x - 20, y - 99), (x - 27, y - 79), 7)
    pygame.draw.line(lienzo, AMARILLO_SOMBRA, (x + 19, y - 98), (x + 13, y - 76), 9)
    pygame.draw.line(lienzo, AMARILLO_CLARO, (x + 19, y - 98), (x + 13, y - 77), 7)
    pygame.draw.circle(lienzo, PIEL_CHIBI, (x - 26, y - 76), 5)
    pygame.draw.circle(lienzo, PIEL_CHIBI, (x + 12, y - 75), 5)

    if not con_cabeza:
        dibujar_amuleto(lienzo, x, y)
        return

    # MELENA AZUL: PARTE DE ATRAS (VA ANTES QUE LA CARA PARA QUEDAR DETRAS)
    pygame.draw.ellipse(lienzo, AZUL_OSCURO, (x - 38, y - 183, 76, 82))
    pygame.draw.ellipse(lienzo, AZUL, (x - 34, y - 181, 68, 72))

    # CABEZA Y OREJAS
    pygame.draw.ellipse(lienzo, PIEL_CHIBI_SOMBRA, (x - 32, y - 168, 64, 69))
    pygame.draw.ellipse(lienzo, PIEL_CHIBI, (x - 30, y - 171, 60, 68))
    pygame.draw.circle(lienzo, PIEL_CHIBI, (x - 29, y - 139), 7)
    pygame.draw.circle(lienzo, PIEL_CHIBI, (x + 29, y - 139), 7)

    # MECHONES A LOS LADOS
    pygame.draw.polygon(lienzo, AZUL_OSCURO, [(x - 34, y - 151), (x - 33, y - 120), (x - 22, y - 108),
                                              (x - 27, y - 143), (x - 22, y - 164)])
    pygame.draw.polygon(lienzo, AZUL, [(x - 31, y - 149), (x - 28, y - 124), (x - 23, y - 117),
                                       (x - 25, y - 151)])
    pygame.draw.polygon(lienzo, AZUL_OSCURO, [(x + 29, y - 158), (x + 37, y - 145), (x + 31, y - 119),
                                              (x + 22, y - 109), (x + 27, y - 145)])
    pygame.draw.polygon(lienzo, AZUL_CLARO, [(x + 29, y - 149), (x + 32, y - 128), (x + 27, y - 119),
                                             (x + 27, y - 147)])

    # FLEQUILLO
    pygame.draw.polygon(lienzo, AZUL_OSCURO, [(x - 32, y - 160), (x - 26, y - 178), (x - 7, y - 185),
                                              (x + 18, y - 179), (x + 34, y - 164), (x + 22, y - 158),
                                              (x + 10, y - 165), (x - 2, y - 158), (x - 17, y - 163)])
    pygame.draw.polygon(lienzo, AZUL, [(x - 27, y - 165), (x - 20, y - 177), (x - 4, y - 181),
                                       (x + 14, y - 176), (x + 28, y - 165), (x + 17, y - 162),
                                       (x + 7, y - 169), (x - 5, y - 162), (x - 18, y - 166)])
    pygame.draw.line(lienzo, (91, 128, 202), (x - 18, y - 174), (x - 4, y - 179), 2)
    pygame.draw.line(lienzo, (91, 128, 202), (x + 4, y - 176), (x + 17, y - 172), 2)

    # OJOS GRANDES
    pygame.draw.ellipse(lienzo, (245, 238, 220), (x - 20, y - 145, 14, 19))
    pygame.draw.ellipse(lienzo, (245, 238, 220), (x + 6, y - 145, 14, 19))
    pygame.draw.ellipse(lienzo, (104, 117, 99), (x - 16, y - 140, 7, 10))
    pygame.draw.ellipse(lienzo, (104, 117, 99), (x + 10, y - 140, 7, 10))
    pygame.draw.circle(lienzo, (24, 31, 30), (x - 13, y - 136), 3)
    pygame.draw.circle(lienzo, (24, 31, 30), (x + 13, y - 136), 3)
    pygame.draw.circle(lienzo, BLANCO, (x - 14, y - 139), 2)
    pygame.draw.circle(lienzo, BLANCO, (x + 12, y - 139), 2)

    # CEJAS, NARIZ, SONRISA Y PECAS
    pygame.draw.arc(lienzo, (107, 77, 72), (x - 21, y - 153, 16, 7), 0.2, 2.8, 1)
    pygame.draw.arc(lienzo, (107, 77, 72), (x + 5, y - 153, 16, 7), 0.2, 2.8, 1)
    pygame.draw.line(lienzo, PIEL_CHIBI_SOMBRA, (x, y - 132), (x + 1, y - 126), 1)
    pygame.draw.arc(lienzo, (125, 73, 70), (x - 7, y - 126, 15, 8), 3.4, 6.0, 1)

    for dx, dy in [(-22, -128), (-18, -125), (20, -128), (23, -125)]:
        pygame.draw.circle(lienzo, (190, 128, 113), (x + dx, y + dy), 1)

    # FLOR PEQUENA EN EL PELO
    pygame.draw.circle(lienzo, (255, 239, 197), (x - 23, y - 169), 3)

    for dx, dy in [(-4, 0), (4, 0), (0, -4), (0, 4)]:
        pygame.draw.circle(lienzo, (255, 239, 197), (x - 23 + dx, y - 169 + dy), 2)

    pygame.draw.circle(lienzo, (230, 173, 48), (x - 23, y - 169), 2)

    dibujar_amuleto(lienzo, x, y)


def dibujar_amuleto(lienzo: pygame.Surface, x: int, y: int) -> None:

    """EL AMULETO AZUL QUE CORALINE SOSTIENE CON LAS MANOS."""

    pygame.draw.line(lienzo, (44, 57, 93), (x - 8, y - 79), (x + 8, y - 65), 3)
    pygame.draw.circle(lienzo, (47, 82, 137), (x + 4, y - 68), 7)
    pygame.draw.circle(lienzo, (115, 160, 206), (x + 4, y - 68), 4)
    pygame.draw.circle(lienzo, (238, 199, 78), (x + 4, y - 68), 2)


# --------------------------------------------------
# CABEZA DE CORALINE ESTILO RETRATO (PIXELES GRANDES)
# --------------------------------------------------
# Se dibuja en una imagen chica de 120 x 92 con las mismas coordenadas del
# retrato original, y luego se pega encima del cuerpo chibi.

ANCHO_RETRATO = 120
ALTO_RETRATO = 92

TINTA = (26, 24, 54)
PELO_RETRATO_OSCURO = (20, 25, 119)
PELO_RETRATO = (35, 43, 173)
PELO_RETRATO_MEDIO = (48, 62, 197)
PELO_RETRATO_CLARO = (75, 94, 224)
PIEL_RETRATO = (224, 169, 125)
PIEL_RETRATO_CLARA = (239, 190, 145)
PIEL_RETRATO_SOMBRA = (190, 126, 95)
OJO_RETRATO_BLANCO = (238, 226, 202)
OJO_RETRATO_CAFE = (89, 62, 42)
ROJO_RETRATO = (157, 37, 47)

# EN EL RETRATO, EL CENTRO DE LA CARA Y LA BARBILLA ESTAN EN:
CENTRO_CARA_RETRATO = 61
BARBILLA_RETRATO = 69

CABEZAS_RETRATO = {}


def bloque(lienzo: pygame.Surface, color: tuple, x: int, y: int, ancho: int, alto: int) -> None:

    """RECTANGULO SIMPLE: UN BLOQUE DE PIXELES."""

    pygame.draw.rect(lienzo, color, (int(x), int(y), int(ancho), int(alto)))


def dibujar_pelo_atras_retrato(lienzo: pygame.Surface) -> None:

    """SILUETA GRANDE DEL PELO Y SU BRILLO EN LA PARTE DE ARRIBA."""

    pygame.draw.polygon(lienzo, PELO_RETRATO_OSCURO, [
        (28, 47), (23, 39), (23, 29), (28, 20), (37, 14),
        (49, 11), (63, 10), (77, 12), (89, 19), (97, 29),
        (100, 40), (98, 53), (94, 65), (89, 73), (82, 73),
        (80, 62), (83, 48), (80, 34), (71, 27), (58, 25),
        (46, 28), (39, 37), (40, 54), (46, 68), (39, 73),
        (31, 65), (27, 56)
    ])
    pygame.draw.polygon(lienzo, PELO_RETRATO, [
        (27, 37), (27, 27), (34, 19), (46, 14), (61, 13),
        (76, 15), (88, 22), (94, 31), (90, 35), (82, 26),
        (70, 21), (57, 20), (44, 23), (35, 31)
    ])
    bloque(lienzo, PELO_RETRATO_MEDIO, 35, 18, 8, 3)
    bloque(lienzo, PELO_RETRATO_MEDIO, 49, 14, 8, 3)
    bloque(lienzo, PELO_RETRATO_CLARO, 58, 13, 5, 2)
    bloque(lienzo, PELO_RETRATO_MEDIO, 75, 17, 6, 3)
    bloque(lienzo, PELO_RETRATO_OSCURO, 89, 29, 5, 15)


def dibujar_cara_retrato(lienzo: pygame.Surface, parpadea: bool) -> None:

    """OREJAS, CARA, CEJAS, OJOS, NARIZ, PECAS, CHAPITAS Y BOCA."""

    # OREJAS
    bloque(lienzo, PIEL_RETRATO_SOMBRA, 29, 38, 7, 12)
    bloque(lienzo, PIEL_RETRATO_CLARA, 30, 39, 4, 8)
    bloque(lienzo, PIEL_RETRATO_SOMBRA, 85, 36, 7, 13)
    bloque(lienzo, PIEL_RETRATO_CLARA, 87, 38, 4, 8)

    # CARA OVALADA CON BORDES ESCALONADOS
    pygame.draw.polygon(lienzo, PIEL_RETRATO_SOMBRA, [
        (36, 26), (43, 21), (55, 18), (69, 18), (80, 23),
        (87, 31), (89, 43), (86, 55), (79, 64), (68, 69),
        (55, 69), (44, 64), (36, 56), (33, 45), (33, 34)
    ])
    pygame.draw.polygon(lienzo, PIEL_RETRATO, [
        (37, 26), (45, 22), (57, 20), (70, 20), (80, 25),
        (85, 33), (87, 44), (83, 55), (77, 63), (67, 67),
        (55, 67), (45, 62), (38, 55), (35, 44), (35, 34)
    ])

    # LUZ Y SOMBRA EN LA CARA
    bloque(lienzo, PIEL_RETRATO_CLARA, 43, 25, 10, 3)
    bloque(lienzo, PIEL_RETRATO_CLARA, 39, 34, 3, 11)
    bloque(lienzo, (213, 151, 111), 79, 48, 4, 8)
    bloque(lienzo, PIEL_RETRATO_SOMBRA, 74, 61, 6, 3)

    # CEJAS
    bloque(lienzo, (110, 75, 51), 40, 34, 7, 2)
    bloque(lienzo, (110, 75, 51), 64, 31, 8, 2)
    bloque(lienzo, (110, 75, 51), 44, 32, 3, 1)
    bloque(lienzo, (110, 75, 51), 68, 29, 3, 1)

    # OJOS
    if parpadea:
        bloque(lienzo, OJO_RETRATO_CAFE, 41, 41, 8, 2)
        bloque(lienzo, OJO_RETRATO_CAFE, 65, 38, 8, 2)
    else:
        bloque(lienzo, OJO_RETRATO_BLANCO, 40, 39, 9, 9)
        bloque(lienzo, OJO_RETRATO_BLANCO, 64, 36, 9, 9)
        bloque(lienzo, (203, 184, 151), 40, 46, 8, 2)
        bloque(lienzo, OJO_RETRATO_CAFE, 43, 41, 4, 5)
        bloque(lienzo, OJO_RETRATO_CAFE, 66, 38, 4, 5)
        bloque(lienzo, (42, 35, 30), 45, 42, 2, 4)
        bloque(lienzo, (42, 35, 30), 68, 39, 2, 4)
        bloque(lienzo, (255, 245, 224), 42, 40, 2, 2)
        bloque(lienzo, (255, 245, 224), 65, 37, 2, 2)

    # NARIZ, PECAS Y CHAPITAS
    bloque(lienzo, PIEL_RETRATO_SOMBRA, 56, 48, 3, 2)
    bloque(lienzo, (173, 112, 84), 54, 50, 5, 2)

    for px, py in [(38, 50), (42, 53), (48, 56), (76, 52), (80, 49)]:
        bloque(lienzo, (190, 126, 98), px, py, 1, 1)

    bloque(lienzo, (219, 139, 119), 38, 53, 4, 2)
    bloque(lienzo, (219, 139, 119), 77, 53, 4, 2)

    # BOCA ROJA, UN POCO LADEADA
    bloque(lienzo, ROJO_RETRATO, 55, 57, 9, 2)
    bloque(lienzo, ROJO_RETRATO, 63, 55, 4, 2)
    bloque(lienzo, (248, 211, 186), 57, 57, 5, 1)


def dibujar_fleco_retrato(lienzo: pygame.Surface) -> None:

    """MECHONES SOBRE LAS MEJILLAS, FLEQUILLO ESCALONADO, REFLEJOS Y BROCHE."""

    # MECHONES A LOS LADOS DE LA CARA
    pygame.draw.polygon(lienzo, PELO_RETRATO_OSCURO, [
        (28, 34), (33, 30), (35, 42), (38, 55),
        (44, 67), (40, 74), (33, 67), (28, 57), (25, 46)
    ])
    pygame.draw.polygon(lienzo, PELO_RETRATO, [
        (30, 39), (34, 36), (35, 50), (40, 64),
        (43, 69), (39, 70), (32, 61), (28, 50)
    ])
    pygame.draw.polygon(lienzo, PELO_RETRATO_OSCURO, [
        (82, 27), (92, 31), (97, 40), (96, 54),
        (91, 67), (86, 72), (83, 67), (88, 53), (88, 40)
    ])
    pygame.draw.polygon(lienzo, PELO_RETRATO, [
        (87, 34), (93, 40), (93, 53), (89, 64),
        (86, 67), (89, 54), (89, 43)
    ])

    # FLEQUILLO EN BLOQUES ESCALONADOS
    pygame.draw.polygon(lienzo, PELO_RETRATO_OSCURO, [
        (27, 35), (28, 26), (36, 18), (48, 13),
        (61, 12), (75, 15), (86, 22), (94, 32),
        (91, 37), (84, 31), (78, 25), (69, 23),
        (60, 25), (53, 22), (46, 26), (39, 29),
        (34, 38)
    ])
    pygame.draw.polygon(lienzo, PELO_RETRATO, [
        (29, 32), (31, 25), (40, 18), (52, 15),
        (65, 15), (78, 19), (88, 27), (91, 33),
        (85, 30), (78, 24), (68, 22), (59, 24),
        (52, 21), (45, 25), (37, 29), (33, 36)
    ])

    # REFLEJOS
    bloque(lienzo, PELO_RETRATO_MEDIO, 35, 21, 7, 3)
    bloque(lienzo, PELO_RETRATO_MEDIO, 46, 17, 8, 3)
    bloque(lienzo, PELO_RETRATO_CLARO, 58, 16, 5, 2)
    bloque(lienzo, PELO_RETRATO_MEDIO, 70, 18, 6, 3)
    bloque(lienzo, PELO_RETRATO_CLARO, 80, 23, 4, 2)
    bloque(lienzo, PELO_RETRATO_OSCURO, 50, 26, 6, 2)

    # BROCHE AMARILLO DEL LADO IZQUIERDO (RECORRIDO 14 PIXELES PARA QUE QUEDE SOBRE EL PELO)
    bloque(lienzo, (255, 218, 54), 29, 26, 2, 10)
    bloque(lienzo, (255, 218, 54), 27, 29, 6, 3)
    bloque(lienzo, (255, 239, 119), 30, 24, 2, 3)
    bloque(lienzo, (194, 130, 18), 28, 33, 2, 3)


def cabeza_retrato(parpadea: bool) -> pygame.Surface:

    """ARMA LA CABEZA DEL RETRATO EN UNA IMAGEN TRANSPARENTE (SE GUARDA PARA NO REPETIR)."""

    if parpadea not in CABEZAS_RETRATO:

        cabeza = pygame.Surface((ANCHO_RETRATO, ALTO_RETRATO), pygame.SRCALPHA)

        dibujar_pelo_atras_retrato(cabeza)
        dibujar_cara_retrato(cabeza, parpadea)
        dibujar_fleco_retrato(cabeza)

        CABEZAS_RETRATO[parpadea] = cabeza

    return CABEZAS_RETRATO[parpadea]


def dibujar_coraline_con_retrato(lienzo: pygame.Surface, x: int, y: int) -> None:

    """CUERPO CHIBI CON IMPERMEABLE Y, ENCIMA, LA CABEZA DEL RETRATO.

    (x, y) ES EL CENTRO DE LOS PIES.
    """

    dibujar_coraline_impermeable(lienzo, x, y, False)

    # LA BARBILLA DEL RETRATO QUEDA DONDE EMPIEZA EL CUELLO DEL CUERPO
    lienzo.blit(
        cabeza_retrato(False),
        (x - CENTRO_CARA_RETRATO, y - 106 - BARBILLA_RETRATO)
    )


# --------------------------------------------------
# CORALINE DE CUERPO COMPLETO, CON EL MISMO ESTILO QUE LA MAMA
# --------------------------------------------------
# Figuras sencillas (elipses, rectangulos y poligonos) con luz y sombra,
# igual que la mama de mama_llave.py, para que las dos se vean del mismo juego.

IMPERMEABLE = (232, 190, 52)
IMPERMEABLE_SOMBRA = (186, 140, 30)
IMPERMEABLE_LUZ = (250, 222, 110)
MALLAS = (38, 46, 86)
MALLAS_SOMBRA = (26, 32, 62)
BOTAS = (240, 200, 56)
BOTAS_SOMBRA = (190, 146, 30)
BOLSA = (112, 64, 46)
PIEL_NINA = (236, 196, 168)
PIEL_NINA_SOMBRA = (204, 160, 140)
PELO_NINA = (36, 52, 168)
PELO_NINA_SOMBRA = (22, 32, 112)
PELO_NINA_BRILLO = (86, 112, 220)


def dibujar_coraline_completa(lienzo: pygame.Surface, x: int, y: int) -> None:

    """CORALINE DE PIE, DE FRENTE. (x, y) ES EL CENTRO DE LOS PIES. MIDE UNOS 185 DE ALTO."""

    # SOMBRA EN EL PISO
    sombra = pygame.Surface((64, 10), pygame.SRCALPHA)
    pygame.draw.ellipse(sombra, (0, 0, 0, 120), sombra.get_rect())
    lienzo.blit(sombra, (x - 32, y - 6))

    # MALLAS AZUL MARINO
    pygame.draw.rect(lienzo, MALLAS, (x - 12, y - 52, 10, 34))
    pygame.draw.rect(lienzo, MALLAS, (x + 2, y - 52, 10, 34))
    pygame.draw.rect(lienzo, MALLAS_SOMBRA, (x - 12, y - 52, 3, 34))

    # BOTAS AMARILLAS DE AGUA, CON BORDE CLARO Y SUELA
    for x_bota in [x - 15, x + 1]:
        pygame.draw.rect(lienzo, BOTAS, (x_bota, y - 24, 14, 22), border_radius=3)
        pygame.draw.rect(lienzo, mezclar_color(BOTAS, (255, 255, 255), 0.35), (x_bota, y - 24, 14, 3))
        pygame.draw.rect(lienzo, BOTAS_SOMBRA, (x_bota, y - 21, 3, 18))
        pygame.draw.rect(lienzo, mezclar_color(BOTAS, (0, 0, 0), 0.45), (x_bota, y - 4, 15, 3))

    # IMPERMEABLE ACAMPANADO
    pygame.draw.polygon(
        lienzo,
        IMPERMEABLE,
        [(x - 19, y - 114), (x + 19, y - 114), (x + 30, y - 50), (x - 30, y - 50)]
    )
    pygame.draw.polygon(lienzo, IMPERMEABLE_SOMBRA, [(x - 19, y - 114), (x - 12, y - 114), (x - 20, y - 50),
                                                     (x - 30, y - 50)])
    pygame.draw.line(lienzo, IMPERMEABLE_LUZ, (x + 16, y - 108), (x + 26, y - 54), 2)
    pygame.draw.line(lienzo, mezclar_color(IMPERMEABLE, (0, 0, 0), 0.5), (x - 30, y - 50), (x + 30, y - 50), 2)

    # CAPUCHA CAIDA DETRAS DEL CUELLO, CIERRE Y BOTONES
    pygame.draw.ellipse(lienzo, IMPERMEABLE_SOMBRA, (x - 20, y - 122, 40, 14))
    pygame.draw.line(lienzo, IMPERMEABLE_SOMBRA, (x + 1, y - 108), (x + 3, y - 52))

    for y_boton in [y - 100, y - 88, y - 76, y - 64]:
        pygame.draw.rect(lienzo, (140, 98, 22), (x + 5, y_boton, 3, 3))

    # BOLSILLOS
    pygame.draw.line(lienzo, IMPERMEABLE_SOMBRA, (x - 20, y - 72), (x - 8, y - 70), 2)
    pygame.draw.line(lienzo, IMPERMEABLE_SOMBRA, (x + 10, y - 70), (x + 22, y - 72), 2)

    # BRAZOS CON MANGAS A LOS LADOS Y MANOS
    pygame.draw.line(lienzo, IMPERMEABLE_SOMBRA, (x - 19, y - 110), (x - 27, y - 70), 9)
    pygame.draw.line(lienzo, IMPERMEABLE, (x + 19, y - 110), (x + 27, y - 70), 9)
    pygame.draw.ellipse(lienzo, PIEL_NINA, (x - 32, y - 70, 10, 11))
    pygame.draw.ellipse(lienzo, PIEL_NINA, (x + 22, y - 70, 10, 11))

    # BOLSA CAFE CRUZADA: CORREA DEL HOMBRO DERECHO A LA CADERA IZQUIERDA
    pygame.draw.line(lienzo, BOLSA, (x + 14, y - 112), (x - 18, y - 70), 3)
    pygame.draw.rect(lienzo, BOLSA, (x - 30, y - 74, 20, 16), border_radius=4)
    pygame.draw.rect(lienzo, mezclar_color(BOLSA, (0, 0, 0), 0.3), (x - 30, y - 74, 20, 6),
                     border_top_left_radius=4, border_top_right_radius=4)

    # CUELLO
    pygame.draw.rect(lienzo, PIEL_NINA_SOMBRA, (x - 5, y - 126, 10, 10))

    dibujar_cabeza_nina(lienzo, x, y, "curiosa")


def dibujar_cabeza_nina(lienzo: pygame.Surface, x: int, y: int, expresion: str) -> None:

    """CABEZA DE CORALINE CON EL ESTILO DE LA MAMA.

    (x, y) es el centro de los pies de una Coraline de pie (la cabeza queda
    unos 126 pixeles arriba). expresion puede ser "curiosa" (sonrie) o "susto"
    (ojos muy abiertos, cejas levantadas y boca abierta).
    """

    # PELO DE ATRAS: CUPULA Y MELENA A LOS LADOS
    pygame.draw.ellipse(lienzo, PELO_NINA, (x - 30, y - 180, 60, 56))
    pygame.draw.rect(lienzo, PELO_NINA, (x - 31, y - 154, 14, 40), border_bottom_left_radius=10,
                     border_bottom_right_radius=4)
    pygame.draw.rect(lienzo, PELO_NINA, (x + 17, y - 154, 14, 40), border_bottom_left_radius=4,
                     border_bottom_right_radius=10)

    # CARA CON SOMBRA DEL LADO IZQUIERDO
    cara = pygame.Rect(x - 21, y - 166, 42, 46)
    pygame.draw.ellipse(lienzo, PIEL_NINA, cara)
    sombra_cara = pygame.Surface(cara.size, pygame.SRCALPHA)
    pygame.draw.ellipse(sombra_cara, (160, 110, 110, 45), (-24, 8, cara.width - 14, cara.height - 8))
    lienzo.blit(sombra_cara, cara.topleft)

    # CEJAS, OJOS, NARIZ, CHAPITAS, PECAS Y SONRISA
    for x_ojo in [x - 9, x + 9]:

        if expresion == "susto":
            # CEJAS MAS ARRIBA, OJO MAS ALTO Y PUPILA CHIQUITA
            pygame.draw.line(lienzo, PELO_NINA_SOMBRA, (x_ojo - 5, y - 153), (x_ojo + 4, y - 154), 2)
            pygame.draw.ellipse(lienzo, (240, 238, 232), (x_ojo - 5, y - 149, 11, 11))
            pygame.draw.circle(lienzo, (104, 74, 54), (x_ojo, y - 143), 2)
            lienzo.set_at((x_ojo, y - 143), (24, 18, 20))
            pygame.draw.arc(lienzo, (40, 28, 34), (x_ojo - 6, y - 150, 13, 13), 0.4, 2.75, 1)
            continue

        pygame.draw.line(lienzo, PELO_NINA_SOMBRA, (x_ojo - 5, y - 150), (x_ojo + 4, y - 151), 2)
        pygame.draw.ellipse(lienzo, (240, 238, 232), (x_ojo - 5, y - 147, 11, 8))
        pygame.draw.circle(lienzo, (104, 74, 54), (x_ojo, y - 143), 3)
        pygame.draw.circle(lienzo, (24, 18, 20), (x_ojo, y - 143), 1)
        lienzo.set_at((x_ojo + 1, y - 145), (255, 255, 255))
        pygame.draw.arc(lienzo, (40, 28, 34), (x_ojo - 6, y - 148, 13, 10), 0.4, 2.75, 1)

    pygame.draw.line(lienzo, PIEL_NINA_SOMBRA, (x + 1, y - 141), (x, y - 134), 2)

    chapitas = pygame.Surface((40, 10), pygame.SRCALPHA)
    pygame.draw.ellipse(chapitas, (240, 150, 150, 90), (2, 2, 9, 5))
    pygame.draw.ellipse(chapitas, (240, 150, 150, 90), (29, 2, 9, 5))
    lienzo.blit(chapitas, (x - 20, y - 138))

    for dx, dy in [(-15, -134), (-12, -132), (12, -132), (15, -134)]:
        lienzo.set_at((x + dx, y + dy), (188, 126, 100))

    # SONRISA, O BOCA ABIERTA DEL SUSTO
    if expresion == "susto":
        pygame.draw.ellipse(lienzo, (176, 84, 90), (x - 3, y - 133, 6, 6))
        pygame.draw.ellipse(lienzo, (90, 40, 48), (x - 2, y - 131, 4, 3))
    else:
        pygame.draw.lines(lienzo, (176, 84, 90), False, [(x - 5, y - 131), (x - 2, y - 129), (x + 2, y - 129),
                                                         (x + 5, y - 131)], 2)

    # FLECO RECTO SOBRE LA FRENTE Y BRILLO DEL PELO
    pygame.draw.polygon(
        lienzo,
        PELO_NINA,
        [(x - 29, y - 150), (x - 23, y - 172), (x, y - 180), (x + 23, y - 172), (x + 29, y - 150),
         (x + 21, y - 155), (x + 11, y - 153), (x, y - 156), (x - 11, y - 153), (x - 21, y - 155)]
    )
    pygame.draw.arc(lienzo, PELO_NINA_BRILLO, (x - 22, y - 178, 44, 26), 1.2, 2.6, 2)
    pygame.draw.line(lienzo, PELO_NINA_SOMBRA, (x - 29, y - 136), (x - 29, y - 118), 2)

    # PASADOR DE ESTRELLA
    centro = (x - 18, y - 162)
    puntas = []

    for i in range(10):
        radio = 4 if i % 2 == 0 else 2
        angulo = -1.5708 + i * 0.6283
        puntas.append((centro[0] + radio * math.cos(angulo), centro[1] + radio * math.sin(angulo)))

    pygame.draw.polygon(lienzo, (246, 200, 64), puntas)


def cerrar_ojos_coraline_completa(lienzo: pygame.Surface, x: int, y: int) -> None:

    """OJOS CERRADOS ENCIMA, PARA PARPADEAR. MISMA (x, y) QUE dibujar_coraline_completa."""

    for x_ojo in [x - 9, x + 9]:
        pygame.draw.ellipse(lienzo, PIEL_NINA, (x_ojo - 6, y - 148, 13, 10))
        pygame.draw.line(lienzo, (40, 28, 34), (x_ojo - 5, y - 143), (x_ojo + 5, y - 143), 2)


def mezclar_color(color: tuple, otro: tuple, cuanto: float) -> tuple:

    """COLOR INTERMEDIO ENTRE DOS COLORES."""

    return (int(color[0] + (otro[0] - color[0]) * cuanto),
            int(color[1] + (otro[1] - color[1]) * cuanto),
            int(color[2] + (otro[2] - color[2]) * cuanto))


# --------------------------------------------------
# LAS VECINAS ACTRICES Y SUS PERROS
# --------------------------------------------------
# Mismo estilo que la mama: figuras con luz y sombra. Las dos estan
# dibujadas para un piso en y = 300 (sus pies quedan ahi); x es el centro.
# Las poses cambian solo los brazos y la boca.

SPINK_PIEL = (236, 206, 190)
SPINK_PIEL_SOMBRA = (204, 170, 160)
SPINK_PELO = (196, 196, 204)
SPINK_PELO_SOMBRA = (150, 150, 164)
SPINK_ABRIGO = (150, 112, 160)
SPINK_ABRIGO_SOMBRA = (112, 80, 124)
SPINK_ABRIGO_LUZ = (180, 144, 188)
SPINK_BUFANDA = (186, 70, 80)
SPINK_MEDIAS = (210, 190, 170)
ZAPATOS_VECINAS = (44, 34, 40)

FORCIBLE_PIEL = (238, 202, 184)
FORCIBLE_PIEL_PALIDA = (214, 220, 204)
FORCIBLE_PELO = (168, 72, 42)
FORCIBLE_PELO_LUZ = (206, 108, 64)
FORCIBLE_VESTIDO = (66, 108, 88)
FORCIBLE_VESTIDO_SOMBRA = (44, 76, 62)
FORCIBLE_CHAL = (228, 216, 190)

PERRO = (24, 22, 28)
CORREA = (150, 40, 50)


def ojos_spink(x: int) -> list:

    """DONDE VAN LOS OJOS DE LA SENORITA SPINK (DETRAS DE LOS LENTES)."""

    return [(x - 6, 180), (x + 8, 180)]


def mano_spink(x: int, pose: str) -> tuple:

    """DONDE QUEDA LA MANO DE ADELANTE EN CADA POSE (PARA CORREAS U OBJETOS)."""

    if pose == "dar":
        return (x - 50, 214)

    return (x - 24, 214)


def dibujar_spink(lienzo: pygame.Surface, x: int, pose: str) -> None:

    """SENORA BAJITA Y REDONDA CON ABRIGO LILA. LOS OJOS VAN APARTE (PARPADEAN).

    pose: "correas" (mano adelante), "normal" (brazos abajo),
    "brazos_cruzados" (enojada) o "dar" (brazo estirado a la izquierda).
    """

    sombra = pygame.Surface((70, 8), pygame.SRCALPHA)
    pygame.draw.ellipse(sombra, (0, 0, 0, 90), sombra.get_rect())
    lienzo.blit(sombra, (x - 35, 296))

    # PIERNAS DELGADAS CON MEDIAS Y ZAPATOS
    pygame.draw.rect(lienzo, SPINK_MEDIAS, (x - 14, 262, 9, 34))
    pygame.draw.rect(lienzo, SPINK_MEDIAS, (x + 5, 262, 9, 34))
    pygame.draw.ellipse(lienzo, ZAPATOS_VECINAS, (x - 20, 292, 16, 9))
    pygame.draw.ellipse(lienzo, ZAPATOS_VECINAS, (x + 3, 292, 16, 9))

    # ABRIGO REDONDO, COMO UNA CAMPANA
    pygame.draw.ellipse(lienzo, SPINK_ABRIGO, (x - 34, 196, 68, 76))
    pygame.draw.ellipse(lienzo, SPINK_ABRIGO_SOMBRA, (x + 4, 204, 30, 66))
    pygame.draw.ellipse(lienzo, SPINK_ABRIGO_LUZ, (x - 28, 206, 16, 40))

    for y in [222, 238, 254]:
        pygame.draw.circle(lienzo, (90, 60, 100), (x, y), 2)

    # BRAZOS SEGUN LA POSE
    mano = mano_spink(x, pose)

    if pose == "correas" or pose == "dar":
        pygame.draw.line(lienzo, SPINK_ABRIGO_SOMBRA, (x - 26, 206), (mano[0] + 2, mano[1]), 9)
        pygame.draw.circle(lienzo, SPINK_PIEL, mano, 5)

    elif pose == "brazos_cruzados":
        pygame.draw.rect(lienzo, SPINK_ABRIGO_SOMBRA, (x - 26, 212, 52, 12), border_radius=6)
        pygame.draw.line(lienzo, SPINK_ABRIGO, (x - 24, 218), (x + 20, 214), 3)
        pygame.draw.circle(lienzo, SPINK_PIEL, (x - 20, 214), 4)
        pygame.draw.circle(lienzo, SPINK_PIEL, (x + 20, 222), 4)

    else:
        pygame.draw.line(lienzo, SPINK_ABRIGO_SOMBRA, (x - 30, 206), (x - 34, 240), 8)
        pygame.draw.circle(lienzo, SPINK_PIEL, (x - 34, 242), 4)

    # BUFANDA ROJA
    pygame.draw.ellipse(lienzo, SPINK_BUFANDA, (x - 20, 190, 40, 14))
    pygame.draw.polygon(lienzo, SPINK_BUFANDA, [(x + 6, 198), (x + 16, 198), (x + 14, 226), (x + 6, 224)])

    # CARA REDONDA, UN POCO VOLTEADA A LA IZQUIERDA
    pygame.draw.ellipse(lienzo, SPINK_PIEL, (x - 20, 160, 40, 36))
    pygame.draw.ellipse(lienzo, SPINK_PIEL_SOMBRA, (x + 8, 168, 12, 24))
    pygame.draw.circle(lienzo, (232, 160, 160), (x - 10, 186), 4)    # chapitas
    pygame.draw.circle(lienzo, (232, 160, 160), (x + 12, 186), 3)
    pygame.draw.line(lienzo, SPINK_PIEL_SOMBRA, (x + 1, 178), (x - 1, 183))   # nariz

    # BOCA: ENOJADA SI TIENE LOS BRAZOS CRUZADOS, SI NO SONRIE
    if pose == "brazos_cruzados":
        pygame.draw.arc(lienzo, (150, 70, 80), (x - 4, 186, 12, 8), 0.3, 2.8, 2)
    else:
        pygame.draw.arc(lienzo, (150, 70, 80), (x - 4, 182, 12, 8), 3.4, 6.0, 2)

    # PELO GRIS: CHONGO ARRIBA Y ONDAS A LOS LADOS
    pygame.draw.ellipse(lienzo, SPINK_PELO, (x - 22, 154, 44, 18))
    pygame.draw.circle(lienzo, SPINK_PELO, (x + 2, 150), 10)
    pygame.draw.arc(lienzo, SPINK_PELO_SOMBRA, (x - 6, 142, 16, 16), 0.5, 3.0, 2)

    for dx in [-20, 14]:
        pygame.draw.ellipse(lienzo, SPINK_PELO, (x + dx, 162, 8, 16))

    # LENTES REDONDOS
    ojos = ojos_spink(x)

    for ojo_x, ojo_y in ojos:
        pygame.draw.circle(lienzo, (90, 70, 60), (ojo_x, ojo_y), 6, 1)

    pygame.draw.line(lienzo, (90, 70, 60), (ojos[0][0] + 6, 180), (ojos[1][0] - 6, 180))


def dibujar_ojos_spink(lienzo: pygame.Surface, x: int, tiempo: float, enojada: bool) -> None:

    """OJITOS DETRAS DE LOS LENTES. PARPADEA CADA 4 SEGUNDOS. ENOJADA FRUNCE LAS CEJAS."""

    parpadea = tiempo % 4 < 0.15

    for ojo_x, ojo_y in ojos_spink(x):

        if parpadea:
            pygame.draw.line(lienzo, (60, 40, 50), (ojo_x - 3, ojo_y), (ojo_x + 3, ojo_y))
        else:
            pygame.draw.rect(lienzo, (40, 30, 40), (ojo_x - 2, ojo_y - 1, 2, 3))

    if enojada:
        izquierdo, derecho = ojos_spink(x)
        pygame.draw.line(lienzo, SPINK_PELO_SOMBRA, (izquierdo[0] - 5, 170), (izquierdo[0] + 4, 173), 2)
        pygame.draw.line(lienzo, SPINK_PELO_SOMBRA, (derecho[0] - 4, 173), (derecho[0] + 5, 170), 2)


def taza_forcible(x: int) -> tuple:

    """DONDE QUEDA LA TAZA CUANDO LA SENORITA FORCIBLE LA ESTA LEYENDO."""

    return (x - 32, 172)


def dibujar_forcible(lienzo: pygame.Surface, x: int, pose: str, palida: bool) -> None:

    """SENORA ALTA Y ROBUSTA, PELO ROJIZO RIZADO, VESTIDO VERDE, CHAL Y PERLAS.

    pose: "normal" (manos juntas al frente) o "taza" (levanta la taza para leerla).
    palida: la cara pierde el color (se asusto). Los ojos van aparte.
    """

    piel = FORCIBLE_PIEL

    if palida:
        piel = FORCIBLE_PIEL_PALIDA

    sombra = pygame.Surface((76, 8), pygame.SRCALPHA)
    pygame.draw.ellipse(sombra, (0, 0, 0, 90), sombra.get_rect())
    lienzo.blit(sombra, (x - 38, 296))

    # MEDIAS OSCURAS Y ZAPATOS
    pygame.draw.rect(lienzo, (70, 56, 66), (x - 13, 272, 9, 26))
    pygame.draw.rect(lienzo, (70, 56, 66), (x + 4, 272, 9, 26))
    pygame.draw.ellipse(lienzo, ZAPATOS_VECINAS, (x - 19, 292, 16, 9))
    pygame.draw.ellipse(lienzo, ZAPATOS_VECINAS, (x + 3, 292, 16, 9))

    # VESTIDO LARGO VERDE, ANCHO ABAJO
    pygame.draw.polygon(lienzo, FORCIBLE_VESTIDO, [(x - 22, 184), (x + 22, 184), (x + 34, 276), (x - 34, 276)])
    pygame.draw.polygon(lienzo, FORCIBLE_VESTIDO_SOMBRA, [(x + 10, 184), (x + 22, 184), (x + 34, 276), (x + 16, 276)])

    for xx in range(x - 32, x + 34, 6):
        pygame.draw.circle(lienzo, FORCIBLE_CHAL, (xx, 276), 2)       # encaje de la orilla

    # BRAZOS SEGUN LA POSE
    if pose == "taza":
        taza = taza_forcible(x)
        pygame.draw.line(lienzo, FORCIBLE_VESTIDO_SOMBRA, (x - 22, 192), (x - 34, 210), 8)
        pygame.draw.line(lienzo, FORCIBLE_VESTIDO_SOMBRA, (x - 34, 210), (taza[0] + 4, taza[1] + 8), 7)
        pygame.draw.line(lienzo, FORCIBLE_VESTIDO_SOMBRA, (x + 22, 192), (x + 28, 236), 8)
        pygame.draw.circle(lienzo, piel, (x + 28, 238), 4)

        # TAZA CON SU PLATITO
        pygame.draw.ellipse(lienzo, (240, 236, 226), (taza[0] - 9, taza[1] + 6, 20, 5))
        pygame.draw.rect(lienzo, (240, 236, 226), (taza[0] - 6, taza[1] - 2, 13, 9), border_bottom_left_radius=5,
                         border_bottom_right_radius=5)
        pygame.draw.line(lienzo, (90, 120, 170), (taza[0] - 5, taza[1] + 1), (taza[0] + 6, taza[1] + 1))
        pygame.draw.circle(lienzo, piel, (taza[0] + 4, taza[1] + 9), 4)
    else:
        pygame.draw.line(lienzo, FORCIBLE_VESTIDO_SOMBRA, (x - 22, 192), (x - 6, 226), 8)
        pygame.draw.line(lienzo, FORCIBLE_VESTIDO_SOMBRA, (x + 22, 192), (x + 6, 226), 8)
        pygame.draw.circle(lienzo, piel, (x, 228), 6)

    # CHAL SOBRE LOS HOMBROS, CON FLECOS
    pygame.draw.polygon(lienzo, FORCIBLE_CHAL, [(x - 26, 182), (x + 26, 182), (x + 16, 208), (x, 214), (x - 16, 208)])

    for xx in range(x - 14, x + 16, 4):
        pygame.draw.line(lienzo, (196, 180, 150), (xx, 208), (xx, 214))

    # CUELLO, CARA Y COLLAR DE PERLAS
    pygame.draw.rect(lienzo, piel, (x - 6, 170, 12, 14))
    pygame.draw.ellipse(lienzo, piel, (x - 16, 138, 32, 36))
    pygame.draw.ellipse(lienzo, mezclar_color(piel, (120, 90, 100), 0.2), (x + 6, 146, 10, 24))

    for i in range(7):
        pygame.draw.circle(lienzo, (246, 244, 236), (x - 9 + i * 3, 182 + abs(i - 3)), 1)

    # CHAPITAS Y LABIOS ROJOS (SIN COLOR SI ESTA PALIDA)
    if not palida:
        pygame.draw.circle(lienzo, (236, 150, 150), (x - 9, 164), 3)
        pygame.draw.circle(lienzo, (236, 150, 150), (x + 9, 164), 3)
        pygame.draw.ellipse(lienzo, (190, 40, 60), (x - 4, 166, 9, 4))
    else:
        pygame.draw.ellipse(lienzo, (120, 90, 100), (x - 3, 165, 7, 6))       # boca abierta del susto

    pygame.draw.line(lienzo, mezclar_color(piel, (0, 0, 0), 0.2), (x, 154), (x - 1, 160))   # nariz

    # PELO ROJIZO, MUY RIZADO Y ESPONJADO
    for dx, dy in [(-16, 142), (-8, 134), (2, 132), (12, 136), (18, 146), (-20, 154), (20, 158)]:
        pygame.draw.circle(lienzo, FORCIBLE_PELO, (x + dx, dy), 9)

    for dx, dy in [(-10, 134), (0, 131), (-17, 144)]:
        pygame.draw.circle(lienzo, FORCIBLE_PELO_LUZ, (x + dx, dy), 3)


def dibujar_ojos_forcible(lienzo: pygame.Surface, x: int, tiempo: float, pose: str, palida: bool) -> None:

    """OJOS DE LA SENORITA FORCIBLE. CON LA TAZA MIRA HACIA ABAJO; PALIDA LOS ABRE MUCHO."""

    if (tiempo + 2.2) % 4.5 < 0.15 and not palida:
        for ojo_x in [x - 7, x + 7]:
            pygame.draw.line(lienzo, (60, 40, 40), (ojo_x - 3, 156), (ojo_x + 3, 156))
        return

    for ojo_x in [x - 7, x + 7]:

        if palida:
            pygame.draw.ellipse(lienzo, (250, 250, 246), (ojo_x - 4, 152, 8, 8))
            pygame.draw.rect(lienzo, (30, 26, 30), (ojo_x - 3, 156, 2, 2))
        elif pose == "taza":
            pygame.draw.line(lienzo, (60, 40, 40), (ojo_x - 3, 156), (ojo_x + 3, 157), 2)   # mira la taza
        else:
            pygame.draw.rect(lienzo, (40, 30, 40), (ojo_x - 1, 154, 3, 3))

        pygame.draw.line(lienzo, (120, 60, 40), (ojo_x - 4, 150), (ojo_x + 3, 149))      # ceja


def dibujar_perro(lienzo: pygame.Surface, x: int, y_piso: int, tiempo: float, desfase: float) -> tuple:

    """PERRITO NEGRO MIRANDO A LA IZQUIERDA. x ES SU COLA. REGRESA DONDE VA EL COLLAR.

    Da saltitos y mueve la cola; desfase hace que cada perro se mueva a su tiempo.
    """

    salto = int(abs(math.sin((tiempo + desfase) * 4)) * 3)
    y = y_piso - salto

    # SOMBRA (NO SALTA)
    sombra = pygame.Surface((32, 6), pygame.SRCALPHA)
    pygame.draw.ellipse(sombra, (0, 0, 0, 90), sombra.get_rect())
    lienzo.blit(sombra, (x - 30, y_piso - 3))

    # PATAS Y CUERPO LARGO Y BAJITO
    for dx in [-24, -18, -8, -3]:
        pygame.draw.rect(lienzo, PERRO, (x + dx, y - 8, 4, 8))

    pygame.draw.rect(lienzo, PERRO, (x - 28, y - 18, 28, 12), border_radius=4)

    # CABEZA CON BARBA Y OREJAS PARADAS
    pygame.draw.rect(lienzo, PERRO, (x - 38, y - 24, 14, 12), border_radius=3)
    pygame.draw.polygon(lienzo, PERRO, [(x - 40, y - 14), (x - 30, y - 14), (x - 34, y - 8)])
    pygame.draw.polygon(lienzo, PERRO, [(x - 36, y - 24), (x - 34, y - 30), (x - 32, y - 24)])
    pygame.draw.polygon(lienzo, PERRO, [(x - 30, y - 24), (x - 28, y - 30), (x - 26, y - 24)])
    pygame.draw.rect(lienzo, (230, 230, 220), (x - 35, y - 20, 2, 2))      # brillo del ojo

    # COLA QUE SE MUEVE DE UN LADO A OTRO
    angulo = math.sin((tiempo + desfase) * 14) * 0.6
    punta = (x + 2 + int(math.sin(angulo) * 6), y - 18 - int(math.cos(angulo) * 8))
    pygame.draw.line(lienzo, PERRO, (x - 1, y - 16), punta, 3)

    # COLLAR ROJO
    pygame.draw.line(lienzo, CORREA, (x - 26, y - 20), (x - 26, y - 13), 2)

    return (x - 26, y - 18)


# --------------------------------------------------
# LA MAMA (SPRITE)
# --------------------------------------------------
# Pixel art a partir de la imagen que paso Joel: de perfil mirando a la
# derecha, melena negra, sueter de cuello de tortuga color crema, pantalon cafe
# oscuro y zapatos negros. Las manos quedan juntas al frente para cargar algo
# (camisas, la llave...), que se dibuja aparte con su_objeto. Mide 53 x 153.

MAMA_COLORES = {
    "X": (22, 20, 26),      # pelo negro
    "Y": (44, 42, 52),      # pelo con un poco de luz
    "Z": (96, 98, 112),     # brillo del pelo
    "A": (69, 35, 32),
    "B": (44, 27, 25),
    "C": (243, 203, 162),
    "D": (228, 179, 142),
    "E": (207, 156, 118),
    "F": (107, 84, 81),
    "G": (157, 108, 87),
    "H": (176, 138, 109),
    "I": (107, 68, 52),
    "J": (247, 230, 210),
    "K": (131, 60, 61),
    "L": (171, 152, 140),
}

MAMA_FILAS = [
    "..................XXXXXXXXXXXX.......................",
    ".................YXXXXXXXXXXXX...YY..................",
    ".............YXXXXXXXXXXXXXXXXXXXXXXXXXY.............",
    "...........XXXXXYYXYXXXXXXXXXXXXXXXXXXXXXXXXXXX......",
    ".........XYXXXYYZZYYXXXXXXXXXXXXXXXXXXXXXXXXXXXY.....",
    ".........XXXYZZZZXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX.....",
    ".......XXXZZZZZZXXXXXXXXXXXXXXXXXXXXXXXXXYYZZZYXX....",
    "......YXXXZZZZZXXXXXXXXXXXXXXXXXXXXXXXXXXYYYXYYXXY...",
    "......XXXZZZZZYXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXY...",
    ".....XXXYZXXZZZZXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXY...",
    "...YXXXZZXXXXZZZZZYXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX..",
    "...XXXXZZXXXXZZZZZYXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX..",
    "...XXXXXXXXXZZXXZXXZZZZZZZXXXXXXXXXXXXXXXXXXXXXXXXXXX",
    "...XXXXXXXXXZZXXXXYZZZZZZZXXXXXXXXXXXXXXXXXXXXXXXXXXX",
    "...XXXXXXXXYZXXXXXYZXXXXXYZZZYXXXXXXXXXXXXXXXGGXXXXXX",
    "..XXXXXXXXXXXXXXXXXXXXXXXXXXXXZZZXXXXXZYXXXXEEDXXXXXX",
    "..XXXXXXXXXXXXXXXXXXXXXXXXXYXXZZZXXXXYZXXXXXEEDXXXXXX",
    "..XXXXXXXXXXXXXXXXXXXXXXXXXXYZZZZZZZZZXXXXYEDCCXXXXXX",
    "..XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXZZZXXXXXXXXHDXXXXXX",
    "..XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXZYYXXXXXXIYHDXXXXXX",
    "..XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXGEEEEDCCXXXX..",
    "..XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXYYEEEEEDDDXXXX..",
    "YXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXYEEEXXXDDCXXXX..",
    "XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXGYEEDIXLXXDCDXX....",
    "XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXGEEDYZLLYXDCDXX....",
    "XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXYECCCGCJLXXCCCXX....",
    "XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXEECCCCDJJLXXDCDX.....",
    "XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXEECCCCCJJLXXCCCXY....",
    "XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXGECCCCCDDJJXXCCCDXX...",
    "XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXYYCCCDDDDDDCDCCCDDDXXXX",
    "..XXXXXXXXXXXXXXXXXXXXXXXXXXXXYECCCDDDDDDDDCCCCCDDDXX",
    "..XXXXXXXXXXXXXXXXXXXXXXXXXXXXYECCCDDDDDDDCCCCCCCCCXX",
    "..XXXXXXXXXXXXXXXXXXXXXXXXXXXXYECCCCDDDCCCCCCCCCEIXYY",
    "..XXXXXXXXXXXXXXXXXXXXXXXXXXXXYECCCCCCCCCCCCCCDGXXX..",
    "...XXXXXXXXXXXXXXXXXXXXXXXXXXXYECCCCCCCCCCDCCCCGX....",
    "...XXXXXXXXXXXXXXXXXXXXXXXXXXXIEDCCCCCCCCCDGCCCGX....",
    "....YXXXXXXXXXXXXXXXXXXXXXXXXXYEECCCCCCCCCCDKKXXY....",
    ".....XXXXXXXXXXXXXXXXXXXXXXXXXYEEDDDCCCCCCDDCDXX.....",
    "......YXXXXXXXXXXXXXXXXXXXXXXXXYYYEDCCCCCCCDDXX......",
    "........YXXXXXXXXXXXXXXXXXXXXXXXYXXXXXEDCCCDXX.......",
    ".........XXXXXXXXXXXXXXXXXXXXXXXYXXXXXXXXXXXXX.......",
    "............XXXXXXXXXXXXXXXXXXXXGXXXXXXXXXXX.........",
    "................XXXXXXXXXXXXXXXXXXXXXXXX.............",
    "...................XXXXXXXXXXXXXXX.XXXXX.............",
    "...................XIYXXXXXXXXXXXX...XXX.............",
    "....................EHCCEEDHBBBBBBB..................",
    "....................CHCCECCDECCEECCBB................",
    "....................CHCDECCDDCCDDCCBB................",
    "....................CHCCECCDDCCEECEB.................",
    "....................GHCDECCDECCEECFB.................",
    "....................BGDEECCDDCCEECBB.................",
    "....................BBBIIIIFFHHEEHB..................",
    "....................BBEDHHCEIIIIIIB..................",
    "....................BIDDEEDDHEHHHGB..................",
    "....................BCCCCDGCCCCCCDGB.................",
    "....................HCCCCCCGCCCCCCCB.................",
    "....................CCCCCCCGCCCCCCC..................",
    "....................CCCCCCCICCCCCCCD.................",
    "...................DCCCCCCDICCCCCCCC.................",
    "...................DCCCCCCEACCCCCCCC.................",
    "...................CCCCCCDHBDDCCCCCD.B...............",
    "................BB.CCCCCEHBGEDCDEEEBBBBBB............",
    "................BDDCCCCCEGBHEEEEEDGBBBFFIB...........",
    "................BCCCCCDDEGBEEEEEEDBBAEDBBB...........",
    "................BCCCCCCEIABBBBFBBBBDDDDDDD...........",
    ".................CCCCDDHAAAIIIBFDHBDCCCCCE...........",
    "...............BDCCCCGFAAIECCCFCCCBDDCCCCG...........",
    "...............BCCCCFFHCCCCCCCHGDEHBDCCCCD...........",
    "...............BCCCCGCCCCCCCCCCGCCCBHDCCCG...........",
    "...............BCCCCHCCCCCCCCCCFCCEBGCCCCE...........",
    "...............BECCCCCCCCCCCCCCGDCCBGDDCCH...........",
    "................BCCCCCCCCCCCCCHFEEEBBBBBBB...........",
    "................BCCCCCCCCCCEEEEGEEEBBBBBBB...........",
    "................BBFEEEEEEEEEEEHBBBBFHBGEEE...........",
    ".................BBBBAAABBBBBBBIHHEDEBBBBBB..........",
    "...................BBBBBBBBBBBBFHHEDDBBBBB...........",
    "....................BBHHHHHHHHEEECCCCEB..............",
    "....................BBHHHHHHHHDDDCCCCEB..............",
    "....................BHHHHDECCCCCCCCCCCBB.............",
    "....................EEECCCCCCCCCCCCCCCDB.............",
    "....................HEECCCCCCCCCCCCCCCDB.............",
    "....................EECCCCCCCCCCCDDDDHHBB............",
    "....................EECCCCCCCCCCCDEHHHGBB............",
    "....................GGHHHHHHHHHHHEHDCEH.B............",
    "...................DHCCECCECDDCDECDCCEC.B............",
    "...................DHCCECCECCDCDECDCCEC..............",
    "...................CHCCECCECCDCDDCECCEC..............",
    "....................GCCECCDCDDCDDDHDDH...............",
    "...................BBFFIFFIFFFFIIFIIIAB..............",
    "...................BBBBBBBBBBBBBBBBBBBB..............",
    "...................BBBBBBBBBBBBBBBBBBBB..............",
    "...................BBBBBBBBBBBBBBBBBBBB..............",
    "...................BBBAABBAAAAAAAABBBBB..............",
    "....................BBAABBAAAAAAAABBBBB..............",
    "....................BBBABBAAAAAAAABBBB...............",
    "....................BBBABBAAAAAAAABBBB...............",
    "....................BBBABBAAAAAAABBBBB...............",
    "......................BABBAAAAAAABBBBB...............",
    "......................BABBAAAAAAABBBBB...............",
    "......................BABBAAAAAAABBBBB...............",
    "......................BABBAAAAAABBBBB................",
    "......................BABBAAAAAABBBB.................",
    "......................BBBBAAAAAAABBB.................",
    "......................BBBBAAAAABBBBB.................",
    "......................BBBBAAAAABBBBB.................",
    "......................BABBAAAAABBBBB.................",
    "......................BABBAAAAABBBBB.................",
    ".....................BBAAAAAAAABBBBB.................",
    ".....................BBAAAAAAAABBBBB.................",
    "....................BBBAAAAAAABBBBBB.................",
    "....................BBBAAAAAAABBBBBB.................",
    "....................BBBAAAAAAABBBBBB.................",
    "....................BBBAAAAAAABBBBB..................",
    "....................BBAAAAAAAABBBBB..................",
    "....................BBAAAAAAAABBBBB..................",
    "...................BBBABAAAABBBBBBB..................",
    "...................BBAABAABBBBBBBBB..................",
    "...................BBAABABBABBBBBBB..................",
    "...................BAAAABBBABBBBBBB..................",
    "...................BAAAABAAABBBBBB...................",
    "...................BAAAAAAAABBBBBB...................",
    "...................BAAAAAAAABBBBBB...................",
    ".................BBBAAAAAAAABBBBBB...................",
    ".................BBAAAAAAAAABBBBBB...................",
    ".................BBAAAAAAAABBBBBBB...................",
    ".................BBAAAAAAAABBBBBBB...................",
    ".................BBAAAAAAAABBBBBBB...................",
    ".................BBAAAAAAAABBBBBB....................",
    ".................BBAAAAAAAABBBBBB....................",
    ".................BBAAAAAAABBBBBBB....................",
    ".................BBABAAAAABBBBBBB....................",
    ".................BBABAAAAABBBBBBB....................",
    ".................BBABBAAABBBBBBBB....................",
    ".................BBBBBBBBBBBBBBBB....................",
    ".................BBBBBBBBBBBBBBBB....................",
    ".................BBBBBBBBBBBBBBBB....................",
    ".................BBBBBBBBBBBBBBBB....................",
    ".................BBBBBBBBBBBBBBBB....................",
    ".................BBBBBBBBBBBBBBBB....................",
    ".................BBBBBBBBBBBBBBBB....................",
    "...................BBGGGGGBGGGBB.....................",
    "...................BBGGGGGBGGGBB.....................",
    "...................BBEDEEHBGGGBB.....................",
    "...................BBEEDDHBGGGBB.....................",
    "...................BBEEDDHBGGGBB.....................",
    "...................BBEEEEHBGGGGBB....................",
    "..................BBBFEEEEEBBGGGGBB..................",
    ".................BBBBBBEEEEEBAGGGGBBB................",
    ".................BBBBBBADEEEGBAGGGABBB...............",
    ".................BBBBBBBBBEEEHBBBGGGGBBB.............",
    ".................BBBBBBBBBBHEEHBBBBBBBBBB............",
    ".................BBBBBBBBBBBBBBBBBBBBBBBBBB..........",
    "................BBBBBBBBBBBBBBBBBBBBBBBBBBB..........",
]

MANOS_MAMA = (39, 66)     # donde estan sus manos dentro del sprite (mirando a la derecha)

CAMISA_GRIS = (150, 152, 156)
CAMISA_GRIS_SOMBRA = (116, 118, 124)

SPRITES_MAMA = {}


def con_contorno(sprite: pygame.Surface) -> pygame.Surface:

    """REGRESA EL SPRITE CON UNA ORILLA OSCURA DE 1 PIXEL ALREDEDOR (1 PIXEL MAS DE CADA LADO)."""

    nuevo = pygame.Surface((sprite.get_width() + 2, sprite.get_height() + 2), pygame.SRCALPHA)
    silueta = pygame.mask.from_surface(sprite).to_surface(setcolor=(16, 12, 22), unsetcolor=(0, 0, 0, 0))

    for dx, dy in [(0, 1), (2, 1), (1, 0), (1, 2)]:
        nuevo.blit(silueta, (dx, dy))

    nuevo.blit(sprite, (1, 1))

    return nuevo


def sprite_mama(mira_derecha: bool, tamano: int) -> pygame.Surface:

    """ARMA EL SPRITE CON CONTORNO UNA SOLA VEZ (POR LADO Y TAMANO) Y LO GUARDA."""

    clave = str(mira_derecha) + str(tamano)

    if clave not in SPRITES_MAMA:

        sprite = con_contorno(armar_sprite(MAMA_FILAS, MAMA_COLORES))

        if not mira_derecha:
            sprite = pygame.transform.flip(sprite, True, False)

        sprite = pygame.transform.scale(sprite, (sprite.get_width() * tamano, sprite.get_height() * tamano))

        SPRITES_MAMA[clave] = sprite

    return SPRITES_MAMA[clave]


def manos_mama(x: int, y_piso: int, mira_derecha: bool, tamano: int) -> tuple:

    """DONDE QUEDAN SUS MANOS EN EL LIENZO (PARA DIBUJAR LO QUE CARGA)."""

    sprite = sprite_mama(mira_derecha, tamano)
    izquierda = x - sprite.get_width() // 2
    arriba = y_piso - sprite.get_height()

    mano_x = MANOS_MAMA[0] + 1
    if not mira_derecha:
        mano_x = len(MAMA_FILAS[0]) + 1 - mano_x

    return (izquierda + mano_x * tamano, arriba + (MANOS_MAMA[1] + 1) * tamano)


def dibujar_mama(lienzo: pygame.Surface, x: int, y_piso: int, mira_derecha: bool, tamano: int) -> None:

    """LA MAMA PARADA CON SU SOMBRA. x ES EL CENTRO DE SUS PIES. tamano 1 O 2 (AGRANDADA)."""

    sprite = sprite_mama(mira_derecha, tamano)

    sombra = pygame.Surface((sprite.get_width(), 8 * tamano), pygame.SRCALPHA)
    pygame.draw.ellipse(sombra, (0, 0, 0, 100), sombra.get_rect())
    lienzo.blit(sombra, (x - sombra.get_width() // 2, y_piso - 4 * tamano))

    lienzo.blit(sprite, (x - sprite.get_width() // 2, y_piso - sprite.get_height()))


def dibujar_camisas(lienzo: pygame.Surface, manos: tuple) -> None:

    """PILA DE CAMISAS GRISES DOBLADAS ENCIMA DE LAS MANOS DE LA MAMA."""

    x, y = manos

    for i in range(3):
        rect = pygame.Rect(x - 12, y - 10 + i * 5, 24, 5)
        pygame.draw.rect(lienzo, CAMISA_GRIS, rect)
        pygame.draw.line(lienzo, CAMISA_GRIS_SOMBRA, rect.bottomleft, (rect.right - 1, rect.bottom - 1))

    pygame.draw.rect(lienzo, (16, 12, 22), (x - 13, y - 11, 26, 17), 1)


# --------------------------------------------------
# LOS OTROS PADRES (CON OJOS DE BOTON)
# --------------------------------------------------
# Segun la imagen que paso Joel, de frente. Pies en y = 300 y x = centro.
# Se pegan con contorno (pegar_con_contorno) para que se vean como sprites.
# La otra madre: melena negra brillante, cuello grande y picudo, gargantilla
# roja, vestido cafe oscuro con puntitos naranjas, mangas abombadas, falda
# amplia, manos juntas al frente y tacones rojos.
# El otro padre: copete cafe despeinado, lentes negros, bata naranja con
# solapas, cinturon y punos cafe oscuro, camisa estampada, pantalon oscuro y
# pantuflas de osito; una mano rascandose la cabeza y la otra en la cintura.
# Los botones de los ojos se dibujan aparte (dibujar_botones) porque brillan.

OTRA_PIEL = (244, 196, 160)
OTRA_PIEL_SOMBRA = (214, 158, 126)
OTRA_PELO = (20, 18, 26)
OTRA_PELO_BRILLO = (96, 58, 52)      # reflejos rojizos
OTRA_VESTIDO = (66, 38, 36)
OTRA_VESTIDO_SOMBRA = (46, 26, 26)
OTRA_PUNTITOS = (226, 140, 70)
OTRA_CUELLO_FORRO = (150, 110, 90)
OTRA_ROJO = (196, 34, 46)

PADRE_PIEL = (236, 190, 150)
PADRE_PIEL_SOMBRA = (206, 156, 122)
PADRE_PELO = (130, 74, 40)
PADRE_PELO_LUZ = (176, 112, 62)
PADRE_BATA = (228, 122, 42)
PADRE_BATA_SOMBRA = (190, 92, 30)
PADRE_BATA_DIBUJO = (246, 160, 80)
PADRE_ORILLAS = (52, 30, 26)
PADRE_CAMISA = (120, 112, 60)
PADRE_PANTALON = (36, 28, 34)
PADRE_OSITO = (170, 120, 76)

BOTON = (14, 12, 16)


def ojos_otra_madre(x: int) -> list:

    return [(x - 5, 146), (x + 5, 146)]


def ojos_otro_padre(x: int) -> list:

    return [(x - 5, 134), (x + 6, 134)]


def charola_otra_madre(x: int) -> tuple:

    """DONDE QUEDA EL POLLO CUANDO LA OTRA MADRE CARGA LA CHAROLA."""

    return (x, 206)


def hombro_saludo(x: int, quien: str) -> tuple:

    """HOMBRO DEL BRAZO QUE SE MUEVE AL DESPEDIRSE (EL DE AFUERA: MADRE IZQUIERDA, PADRE DERECHA)."""

    if quien == "madre":
        return (x - 13, 176)

    return (x + 14, 164)


def puntitos(lienzo: pygame.Surface, arriba: int, abajo: int, ancho_arriba: int, ancho_abajo: int, x: int) -> None:

    """PUNTITOS NARANJAS EN UNA FIGURA QUE SE ENSANCHA HACIA ABAJO (CORPINO O FALDA)."""

    fila = 0

    for y in range(arriba + 3, abajo - 2, 5):

        avance = (y - arriba) / max(abajo - arriba, 1)
        mitad = int((ancho_arriba + (ancho_abajo - ancho_arriba) * avance) / 2) - 3

        for xx in range(x - mitad + (fila % 2) * 3, x + mitad, 6):
            lienzo.set_at((xx, y), OTRA_PUNTITOS)

        fila = fila + 1


def dibujar_otra_madre(lienzo: pygame.Surface, x: int, pose: str) -> None:

    """LA OTRA MADRE DE FRENTE, SEGUN LA IMAGEN DE JOEL. LOS BOTONES VAN APARTE.

    pose: "normal" (manos juntas al frente), "charola" (carga el pollo asado)
    o "despedir" (el brazo que saluda se dibuja aparte con dibujar_brazo_saludo).
    """

    sombra = pygame.Surface((50, 8), pygame.SRCALPHA)
    pygame.draw.ellipse(sombra, (0, 0, 0, 90), sombra.get_rect())
    lienzo.blit(sombra, (x - 25, 296))

    # PIERNAS MUY DELGADAS Y TACONES ROJOS DE PUNTA
    pygame.draw.line(lienzo, OTRA_PIEL, (x - 4, 268), (x - 5, 292), 3)
    pygame.draw.line(lienzo, OTRA_PIEL_SOMBRA, (x + 4, 268), (x + 5, 292), 3)

    for lado in [-1, 1]:
        talon = x + lado * 5
        pygame.draw.polygon(lienzo, OTRA_ROJO, [(talon - 3, 291), (talon + 3, 291), (talon + lado * 8, 297), (talon - 3, 297)])
        pygame.draw.line(lienzo, (130, 20, 30), (talon - 3, 297), (talon - 3, 300))
        pygame.draw.line(lienzo, (236, 90, 100), (talon - 1, 292), (talon + 2, 292))

    # FALDA LARGA Y AMPLIA CON PLIEGUES, PUNTITOS Y EL LADO DERECHO EN SOMBRA
    pygame.draw.polygon(lienzo, OTRA_VESTIDO, [(x - 10, 206), (x + 10, 206), (x + 27, 270), (x - 27, 270)])
    pygame.draw.polygon(lienzo, OTRA_VESTIDO_SOMBRA, [(x + 4, 206), (x + 10, 206), (x + 27, 270), (x + 14, 270)])

    for dx in [-14, -5, 5, 14]:
        pygame.draw.line(lienzo, OTRA_VESTIDO_SOMBRA, (x + dx // 3, 210), (x + dx, 268))       # pliegues

    puntitos(lienzo, 206, 270, 20, 54, x)
    pygame.draw.line(lienzo, OTRA_VESTIDO_SOMBRA, (x - 27, 269), (x + 27, 269), 2)

    # CORPINO AJUSTADO, CINTURA Y MANGAS CORTAS ABOMBADAS
    pygame.draw.polygon(lienzo, OTRA_VESTIDO, [(x - 11, 174), (x + 11, 174), (x + 9, 206), (x - 9, 206)])
    puntitos(lienzo, 174, 206, 22, 18, x)
    pygame.draw.line(lienzo, OTRA_VESTIDO_SOMBRA, (x - 9, 205), (x + 9, 205), 2)
    pygame.draw.ellipse(lienzo, OTRA_VESTIDO, (x - 18, 172, 11, 13))
    pygame.draw.ellipse(lienzo, OTRA_VESTIDO_SOMBRA, (x + 7, 172, 11, 13))
    lienzo.set_at((x - 14, 177), OTRA_PUNTITOS)
    lienzo.set_at((x + 12, 178), OTRA_PUNTITOS)

    # BRAZOS SEGUN LA POSE (DELGADOS, CON DEDOS LARGOS)
    if pose == "charola":
        pollo = charola_otra_madre(x)
        pygame.draw.line(lienzo, OTRA_PIEL, (x - 13, 184), (x - 14, 206), 3)
        pygame.draw.line(lienzo, OTRA_PIEL_SOMBRA, (x + 13, 184), (x + 14, 206), 3)

        # CHAROLA PLATEADA CON EL POLLO ASADO
        pygame.draw.ellipse(lienzo, (200, 204, 210), (pollo[0] - 20, pollo[1] - 2, 40, 9))
        pygame.draw.ellipse(lienzo, (150, 84, 40), (pollo[0] - 11, pollo[1] - 12, 22, 13))
        pygame.draw.ellipse(lienzo, (196, 120, 56), (pollo[0] - 6, pollo[1] - 11, 12, 5))
        pygame.draw.line(lienzo, (150, 84, 40), (pollo[0] - 10, pollo[1] - 4), (pollo[0] - 16, pollo[1] - 10), 3)
        pygame.draw.line(lienzo, (150, 84, 40), (pollo[0] + 10, pollo[1] - 4), (pollo[0] + 16, pollo[1] - 10), 3)
        pygame.draw.circle(lienzo, (240, 236, 226), (pollo[0] - 17, pollo[1] - 11), 2)
        pygame.draw.circle(lienzo, (240, 236, 226), (pollo[0] + 17, pollo[1] - 11), 2)
        pygame.draw.circle(lienzo, OTRA_PIEL, (pollo[0] - 17, pollo[1] + 2), 3)
        pygame.draw.circle(lienzo, OTRA_PIEL, (pollo[0] + 17, pollo[1] + 2), 3)

    elif pose == "despedir":
        pygame.draw.line(lienzo, OTRA_PIEL_SOMBRA, (x + 13, 184), (x + 15, 216), 3)
        pygame.draw.ellipse(lienzo, OTRA_PIEL, (x + 13, 215, 5, 8))

    else:
        # MANOS JUNTAS ABAJO, AL FRENTE DE LA FALDA
        pygame.draw.line(lienzo, OTRA_PIEL, (x - 13, 184), (x - 6, 214), 3)
        pygame.draw.line(lienzo, OTRA_PIEL_SOMBRA, (x + 13, 184), (x + 6, 214), 3)
        pygame.draw.ellipse(lienzo, OTRA_PIEL, (x - 5, 211, 10, 11))
        for i in range(3):
            pygame.draw.line(lienzo, OTRA_PIEL_SOMBRA, (x - 3 + i * 2, 216), (x - 3 + i * 2, 221))

    # CUELLO LARGO Y DELGADO, ESCOTE EN V Y GARGANTILLA ROJA
    pygame.draw.rect(lienzo, OTRA_PIEL_SOMBRA, (x - 3, 158, 6, 16))
    pygame.draw.polygon(lienzo, OTRA_PIEL, [(x - 5, 173), (x + 5, 173), (x, 186)])
    pygame.draw.rect(lienzo, OTRA_ROJO, (x - 3, 164, 6, 2))

    # CUELLO DEL VESTIDO ALTO Y PICUDO, PARADO A LOS LADOS DEL CUELLO
    for lado in [-1, 1]:
        pico = [(x + lado * 4, 174), (x + lado * 6, 166), (x + lado * 16, 158), (x + lado * 13, 172), (x + lado * 9, 182)]
        pygame.draw.polygon(lienzo, OTRA_VESTIDO, pico)
        pygame.draw.polygon(lienzo, OTRA_CUELLO_FORRO, [(x + lado * 6, 166), (x + lado * 15, 159), (x + lado * 11, 169)])
        pygame.draw.polygon(lienzo, (24, 12, 12), pico, 1)
        lienzo.set_at((x + lado * 11, 175), OTRA_PUNTITOS)

    # CARA (MAS GRANDE), CON BARBILLA FINA
    pygame.draw.ellipse(lienzo, OTRA_PIEL, (x - 11, 130, 22, 28))
    pygame.draw.polygon(lienzo, OTRA_PIEL, [(x - 8, 152), (x + 8, 152), (x, 161)])
    pygame.draw.polygon(lienzo, OTRA_PIEL_SOMBRA, [(x + 6, 136), (x + 11, 144), (x + 8, 154), (x + 2, 160), (x + 6, 150)])

    # CEJAS FINAS Y ARQUEADAS, CHAPITAS, NARICITA, SONRISA ROJA Y LUNAR
    pygame.draw.arc(lienzo, (60, 30, 30), (x - 10, 138, 8, 4), 0.3, 2.8, 1)
    pygame.draw.arc(lienzo, (60, 30, 30), (x + 2, 138, 8, 4), 0.3, 2.8, 1)
    pygame.draw.circle(lienzo, (236, 140, 130), (x - 7, 152), 2)
    pygame.draw.circle(lienzo, (236, 140, 130), (x + 7, 152), 2)
    lienzo.set_at((x, 151), OTRA_PIEL_SOMBRA)
    pygame.draw.line(lienzo, OTRA_ROJO, (x - 3, 155), (x + 3, 155))
    lienzo.set_at((x - 4, 154), OTRA_ROJO)
    lienzo.set_at((x + 4, 154), OTRA_ROJO)
    lienzo.set_at((x - 1, 156), (150, 30, 40))
    lienzo.set_at((x, 156), (150, 30, 40))
    lienzo.set_at((x + 6, 156), (60, 30, 30))                                        # lunar

    # MELENA NEGRA ASIMETRICA: VOLUMEN ATRAS, LADO IZQUIERDO MAS LARGO,
    # FLECO QUE BAJA DE LA DERECHA Y CRUZA LA FRENTE, CON REFLEJOS ROJIZOS
    pygame.draw.ellipse(lienzo, OTRA_PELO, (x - 18, 117, 36, 28))
    pygame.draw.polygon(lienzo, OTRA_PELO, [(x - 18, 130), (x - 10, 137), (x - 10, 151), (x - 6, 157), (x - 13, 160), (x - 19, 152)])
    pygame.draw.polygon(lienzo, OTRA_PELO, [(x + 18, 130), (x + 10, 139), (x + 10, 150), (x + 13, 155), (x + 19, 147)])
    pygame.draw.polygon(lienzo, OTRA_PELO, [(x + 14, 124), (x + 13, 136), (x + 4, 132), (x - 4, 135), (x - 11, 142), (x - 16, 146), (x - 15, 128), (x - 4, 120)])
    pygame.draw.arc(lienzo, OTRA_PELO_BRILLO, (x - 12, 121, 22, 12), 1.2, 2.9, 2)
    pygame.draw.line(lienzo, OTRA_PELO_BRILLO, (x - 16, 140), (x - 15, 152))
    pygame.draw.line(lienzo, OTRA_PELO_BRILLO, (x + 15, 138), (x + 15, 148))
    pygame.draw.line(lienzo, OTRA_PELO_BRILLO, (x + 6, 125), (x - 6, 133))


def dibujar_otro_padre(lienzo: pygame.Surface, x: int, pose: str) -> None:

    """EL OTRO PADRE DE FRENTE, CON SU BATA NARANJA. LOS BOTONES VAN APARTE.

    pose: "normal" (rascandose la cabeza y una mano en la cintura) o "despedir"
    (el brazo de arriba se dibuja aparte, moviendose, con dibujar_brazo_saludo).
    """

    sombra = pygame.Surface((56, 8), pygame.SRCALPHA)
    pygame.draw.ellipse(sombra, (0, 0, 0, 90), sombra.get_rect())
    lienzo.blit(sombra, (x - 28, 296))

    # PANTALON OSCURO Y PANTUFLAS DE OSITO
    pygame.draw.rect(lienzo, PADRE_PANTALON, (x - 9, 248, 7, 44))
    pygame.draw.rect(lienzo, PADRE_PANTALON, (x + 2, 248, 7, 44))

    for dx in [-7, 7]:
        pygame.draw.ellipse(lienzo, PADRE_OSITO, (x + dx - 8, 290, 16, 10))
        pygame.draw.circle(lienzo, PADRE_OSITO, (x + dx - 5, 290), 3)
        pygame.draw.circle(lienzo, PADRE_OSITO, (x + dx + 5, 290), 3)
        lienzo.set_at((x + dx - 2, 294), (30, 20, 20))
        lienzo.set_at((x + dx + 2, 294), (30, 20, 20))
        pygame.draw.circle(lienzo, (220, 180, 140), (x + dx, 297), 2)

    # BATA NARANJA HASTA LA RODILLA, CON DIBUJITO DE CRUCECITAS
    pygame.draw.polygon(lienzo, PADRE_BATA, [(x - 14, 160), (x + 14, 160), (x + 19, 252), (x - 19, 252)])
    pygame.draw.polygon(lienzo, PADRE_BATA_SOMBRA, [(x + 6, 160), (x + 14, 160), (x + 19, 252), (x + 10, 252)])

    for y in range(172, 244, 9):
        for xx in range(x - 14 + (y // 9 % 2) * 4, x + 16, 8):
            lienzo.set_at((xx, y), PADRE_BATA_DIBUJO)
            lienzo.set_at((xx - 1, y), PADRE_BATA_DIBUJO)
            lienzo.set_at((xx + 1, y), PADRE_BATA_DIBUJO)
            lienzo.set_at((xx, y - 1), PADRE_BATA_DIBUJO)
            lienzo.set_at((xx, y + 1), PADRE_BATA_DIBUJO)

    # ORILLA DE ABAJO, SOLAPAS CRUZADAS Y CINTURON CON NUDO
    pygame.draw.polygon(lienzo, PADRE_ORILLAS, [(x - 19, 245), (x + 19, 245), (x + 19, 252), (x - 19, 252)])
    pygame.draw.polygon(lienzo, PADRE_CAMISA, [(x - 5, 158), (x + 5, 158), (x, 174)])
    lienzo.set_at((x - 1, 163), (200, 180, 100))
    lienzo.set_at((x + 1, 167), (200, 180, 100))
    pygame.draw.polygon(lienzo, PADRE_ORILLAS, [(x - 9, 158), (x - 4, 158), (x + 6, 200), (x + 1, 200)])
    pygame.draw.polygon(lienzo, PADRE_ORILLAS, [(x + 4, 158), (x + 9, 158), (x + 3, 182), (x - 1, 176)])
    pygame.draw.line(lienzo, PADRE_ORILLAS, (x + 6, 200), (x + 6, 245), 4)
    pygame.draw.rect(lienzo, PADRE_ORILLAS, (x - 16, 198, 32, 6))
    pygame.draw.line(lienzo, PADRE_ORILLAS, (x - 10, 203), (x - 12, 222), 3)
    pygame.draw.line(lienzo, PADRE_ORILLAS, (x - 7, 203), (x - 6, 218), 3)

    # BRAZO EN LA CINTURA (MANGA NARANJA, PUNO OSCURO, MANO)
    pygame.draw.line(lienzo, PADRE_BATA, (x - 14, 164), (x - 26, 186), 7)
    pygame.draw.line(lienzo, PADRE_BATA, (x - 26, 186), (x - 18, 198), 6)
    pygame.draw.line(lienzo, PADRE_ORILLAS, (x - 23, 192), (x - 18, 198), 7)
    pygame.draw.ellipse(lienzo, PADRE_PIEL, (x - 18, 196, 8, 8))

    # BRAZO DE ARRIBA, RASCANDOSE LA CABEZA (CUANDO SE DESPIDE SE DIBUJA APARTE)
    if pose != "despedir":
        pygame.draw.line(lienzo, PADRE_BATA_SOMBRA, (x + 14, 164), (x + 28, 140), 7)
        pygame.draw.line(lienzo, PADRE_ORILLAS, (x + 27, 142), (x + 24, 134), 8)
        pygame.draw.line(lienzo, PADRE_PIEL_SOMBRA, (x + 24, 134), (x + 14, 120), 3)
        pygame.draw.ellipse(lienzo, PADRE_PIEL, (x + 6, 114, 10, 9))

    # CUELLO LARGO, OREJAS Y CARA ALARGADA
    pygame.draw.rect(lienzo, PADRE_PIEL_SOMBRA, (x - 3, 144, 6, 16))
    pygame.draw.ellipse(lienzo, PADRE_PIEL, (x - 13, 130, 5, 8))
    pygame.draw.ellipse(lienzo, PADRE_PIEL, (x + 9, 130, 5, 8))
    pygame.draw.ellipse(lienzo, PADRE_PIEL, (x - 10, 120, 20, 30))
    pygame.draw.ellipse(lienzo, PADRE_PIEL_SOMBRA, (x + 4, 126, 6, 22))

    # NARIZ LARGA Y SONRISA GRANDE
    pygame.draw.polygon(lienzo, PADRE_PIEL_SOMBRA, [(x, 134), (x + 3, 143), (x - 1, 143)])
    pygame.draw.arc(lienzo, (120, 50, 50), (x - 6, 140, 13, 7), 3.3, 6.1, 2)

    # LENTES NEGROS (LOS BOTONES QUEDAN ADENTRO)
    for ojo_x, ojo_y in ojos_otro_padre(x):
        pygame.draw.rect(lienzo, (236, 214, 196), (ojo_x - 4, ojo_y - 4, 9, 9))         # vidrio (se ve la piel)
        pygame.draw.rect(lienzo, (20, 18, 22), (ojo_x - 5, ojo_y - 5, 11, 11), 1)

    pygame.draw.line(lienzo, (20, 18, 22), (x, 133), (x + 1, 133))

    # COPETE CAFE DESPEINADO CON UN RIZO
    pygame.draw.ellipse(lienzo, PADRE_PELO, (x - 11, 113, 22, 13))
    pygame.draw.ellipse(lienzo, PADRE_PELO, (x - 9, 104, 18, 14))          # copete esponjado
    pygame.draw.ellipse(lienzo, PADRE_PELO, (x - 2, 100, 14, 10))          # se va hacia un lado
    pygame.draw.arc(lienzo, PADRE_PELO, (x + 8, 97, 8, 8), 3.6, 7.0, 2)     # rizo de la punta
    pygame.draw.arc(lienzo, PADRE_PELO_LUZ, (x - 6, 104, 16, 10), 1.6, 3.0, 1)
    pygame.draw.line(lienzo, PADRE_PELO_LUZ, (x + 1, 102), (x + 7, 101))
    pygame.draw.rect(lienzo, PADRE_PELO, (x - 11, 120, 3, 8))
    pygame.draw.rect(lienzo, PADRE_PELO, (x + 8, 120, 3, 7))


def dibujar_brazo_saludo(lienzo: pygame.Surface, x: int, quien: str, tiempo: float) -> None:

    """BRAZO LEVANTADO QUE SE MUEVE DESPACIO DE UN LADO A OTRO (LOS DOS AL MISMO TIEMPO).
    LLEVA CONTORNO OSCURO, COMO EL RESTO DEL PERSONAJE."""

    hombro = hombro_saludo(x, quien)
    angulo = math.sin(tiempo * 2) * 0.35

    # EL CODO SALE HACIA AFUERA: LA MADRE SALUDA CON EL BRAZO IZQUIERDO, EL PADRE CON EL DERECHO
    lado = -1 if quien == "madre" else 1
    codo = (hombro[0] + lado * 12, hombro[1] + 18)
    mano = (codo[0] - lado * int(math.sin(angulo) * 26), codo[1] - int(math.cos(angulo) * 26))

    if quien == "madre":
        manga = OTRA_PIEL_SOMBRA
        piel = OTRA_PIEL
        grueso = 3
    else:
        manga = PADRE_BATA_SOMBRA
        piel = PADRE_PIEL
        grueso = 7

    oscuro = (16, 12, 22)
    pygame.draw.line(lienzo, oscuro, hombro, codo, grueso + 2)
    pygame.draw.line(lienzo, oscuro, codo, mano, grueso + 1)
    pygame.draw.circle(lienzo, oscuro, mano, 5)
    pygame.draw.line(lienzo, manga, hombro, codo, grueso)
    pygame.draw.line(lienzo, manga, codo, mano, grueso - 1)

    if quien == "padre":
        puno = (mano[0] + (codo[0] - mano[0]) // 4, mano[1] + (codo[1] - mano[1]) // 4)
        pygame.draw.line(lienzo, PADRE_ORILLAS, puno, (mano[0] + (codo[0] - mano[0]) // 8, mano[1] + (codo[1] - mano[1]) // 8), grueso)

    pygame.draw.circle(lienzo, piel, mano, 4)


BOTON_GRANDE = [
    "...AAA...",
    ".AACCCAA.",
    ".ACDCCDA.",
    "ACCCDCCCA",
    "ACCCDCCCA",
    ".ACDCCDA.",
    ".AACCCAA.",
    "...AAA...",
]

BOTON_CHICO = [
    "..AAA..",
    ".ACCCA.",
    "ACDCDCA",
    "ACCDCCA",
    "ACDCDCA",
    ".ACCCA.",
    "..AAA..",
]

COLORES_BOTON = {
    "A": (8, 6, 10),         # orilla
    "C": (18, 16, 22),       # el boton
    "D": (196, 170, 150),    # el hilo en X sobre los hoyitos
}

COLORES_BOTON_CAFE = {
    "A": (26, 12, 10),
    "C": (66, 36, 28),
    "D": (214, 176, 140),
}

SPRITES_BOTON = {}


def dibujar_botones(lienzo: pygame.Surface, ojos: list, tiempo: float, chico: bool = False, cafe: bool = False) -> None:

    """OJOS DE BOTON COSIDOS CON UNA X DE HILO. TIENEN UN BRILLITO FIJO ARRIBA A LA
    IZQUIERDA Y CADA 3 SEGUNDOS UN BRILLO LOS CRUZA. chico ES PARA LOS QUE VAN EN LENTES;
    cafe SON LOS DE LA OTRA MADRE."""

    clave = str(chico) + str(cafe)

    if clave not in SPRITES_BOTON:
        filas = BOTON_CHICO if chico else BOTON_GRANDE
        colores = COLORES_BOTON_CAFE if cafe else COLORES_BOTON
        SPRITES_BOTON[clave] = armar_sprite(filas, colores)

    sprite = SPRITES_BOTON[clave]
    mitad = sprite.get_width() // 2
    fase = tiempo % 3

    for x, y in ojos:

        lienzo.blit(sprite, (x - mitad, y - mitad))

        # BRILLITO FIJO
        lienzo.set_at((x - mitad + 2, y - mitad + 1), (120, 116, 134))

        # BRILLO QUE CRUZA EL BOTON EN DIAGONAL
        if fase < 0.36:
            paso = int(fase / 0.36 * (sprite.get_width() - 2))
            bx = x - mitad + 1 + paso
            by = y + mitad - 1 - paso
            lienzo.set_at((bx, by), (250, 250, 255))
            lienzo.set_at((bx + 1, by - 1), (210, 210, 224))


# --------------------------------------------------
# CORALINE CHICA (LA DE TODAS LAS ESCENAS)
# --------------------------------------------------
# Pixel art a partir de la imagen que paso Joel: de perfil mirando a la
# derecha, melena azul con pasador de libelula, pecas, impermeable amarillo
# con capucha, cordones y botones, playera a rayas, guantes sin dedos azul
# marino, medias a rayas rosa con azul y botas amarillas. Version simple
# (Joel la pidio asi): 12 colores, sin pixeles sueltos. Cada letra es un
# color; "." es transparente. Mide 38 x 92 pixeles del lienzo (sin agrandar).

CORALINE_COLORES = {
    "A": (13, 15, 28),
    "B": (249, 196, 44),
    "C": (218, 154, 29),
    "D": (16, 59, 156),
    "E": (20, 40, 99),
    "F": (251, 202, 158),
    "G": (224, 156, 110),
    "H": (161, 107, 26),
    "K": (193, 113, 131),
    "O": (170, 202, 222),
    "P": (51, 109, 216),
    "Q": (221, 225, 226),
}

CORALINE_FILAS = [
    ".............AAAAAAAAAAAAAA...........",
    ".............AAAAAAAAAAAAAA...........",
    "........AAAAAEDDDDDDDDDDDDEAAAA.......",
    "........AAAAAEDDDDDDDDDDDDDAAAA.......",
    "......AAEEDDDDDDDDDDDDDDEEEEEEEAA.....",
    "....AAEEDDDDDDDDDPPPDDDDDDDDDDDEEAA...",
    "....AAEEDAEDDDDDDPPPDDDDDDDDDDDDEAA...",
    "..AAEEDDEAAADDDDDDDDDDPPPPDDDDDEEDEA..",
    "..AAEEDDAOOAEDADDDDDDDPPPPDDDDDEEDEA..",
    "..AADDDDEAOOEAGEEDDDDDDDDDDDDDEA.EED..",
    "..AADDDAAAAAEHAAAAEDDDDDDDDDDDEAAEDDAA",
    "AAEDDDDAOOOAHAEOOAEDDDDDEEAAAAFFA.EEAA",
    "AAEDDDDEAAAAKAAAAEEDDDDDEEAAAAFFAAEEAA",
    "AAEDDDDDEEAOEAAOAEEEAAAAGFFFFFFFFGAEAA",
    "AAEDDDDDEAAOAEAOAAEEAAAAFFFFFFFFFGAEAA",
    "AAEDDDDDEAPAEEAAAAAGFFFFFFFFFFFFFGAEAA",
    "AAEDDDDDEEAAEEEAAKKFFFFFFFAAAAFFFGAA..",
    "AAEDDDDDDDDEEEAKGFFFFFFFFAQEAAFFFGA...",
    "AAEEDDDDDDDDDDAGGFFFFFFFFHQAAAFFFGA...",
    "AAEEDDDEDDDDDDAGFFFFFFFFFFQAAAFFFGAA..",
    "AAEEDDDEDDDDDDAGFFFFFFFFFFQEAAFFFGAA..",
    "AAEEEDDEDDDDDDAGFFFFFFFFFFQEAAFFFFFFAA",
    "AAEEEDDEDDDDDDAGFFFFFFFFFFFFFFFFFFFFAA",
    "AAEEEDDEDDDDDDAGGFFFFFFFFFFFFFFFFGAA..",
    "AAEEEDDEDDDDDDEAAGFFFFFFFFFFFFFFFGAA..",
    "AAEEEDDEDDDDDDDA.GGFFFFFFFFFFFFFFGA...",
    "..AEEEEEEEDDDDDDEAAFFFFFFFFFFAAHKA....",
    "..AAEEEEEEDDDDDDEAAFFFFFFFFFFFKKKA....",
    "...AAEEEEEEDEEDDDEEAGGFFFFFFFFFGA.....",
    ".....AAAAAAEEEEEEDDAGGGGGGGGGAAA......",
    ".....AAAAAAAAEEEEEEAGGAAAAAAA.A.......",
    ".....AAAHHHHHAAAAAAAGGAAAAAAA.........",
    ".....AAAHHHHHAAAAAAGGGAAAAA...........",
    "...AABBHHHHHHHHHAGGFFFAAHCHA..........",
    "...AABBHHHHHHHHAAGGFFFAAHCHH..........",
    ".AACCBBBBBBBBBBCHADDDDDDABBBA.........",
    ".AACCCCCCHHHHHBBBCADDDDECBCCA.........",
    ".AACCCCCCAAAAABBBBAQQQQABBCCA.........",
    ".AACCCCAACCCCCAAABBAEDACBBAA..........",
    ".AACCHAAACCCCCCCHHBCEDACCCAA..........",
    ".AACCHAHCBBCCBBCCEABCABBAACAA.........",
    "...AAAACBBBBCBBBCDCACCCADDBAA.........",
    "....AAACBBBBCBBBCDCHCCHHDDBAA.........",
    ".....ABBBBBBBBBBBDBBBBCCEDCBA.........",
    "....AABBBBBBBBBBBDBBBBCCKDCBCA........",
    "....AABBBBBCCABBBDBBHACCGDCBBA........",
    "....AABBBBBCCABBBEBBHHCCGDCBBA........",
    "..AABBBBBCCCACBBEEEBBBCCDDACCCAA......",
    "..AABBBBBCCCACBBEEEBBBCCDDACCBAA......",
    "..AABBBBBBBACCBBCCCBBBCCCCCCBBAA......",
    "..AABBBBBBBACCBBCCCBHHCCCCCCBBHA......",
    ".AHCBBBBBBBACCBBBBBBHACCBBBABBBA......",
    ".ACBCCCCBCCACCBBBBBBHHCCBBBACCCCA.....",
    ".ACBBBBCCCCACCBBBBBBBBCCBBBACCBCA.....",
    ".AHCBBBBCCAHCCCCCBBBBBCCBBBACCBBA.....",
    ".AAAHHBBCCACCCCCCBBBBBCCBBBACCCCA.....",
    "..AAEEAACCACCBBCCBBBHHCCBBBCAAAA......",
    "..AAEE.AAAACCBBCCBBBHACCBBBCAAAA......",
    ".AAEEEEEAACCBBCCBBBBBBCCBBBBAAEAA.....",
    ".AAEEEEEAACCBCCBBBBBBBCCBBBBAAEEA.....",
    ".AAEEEEEAACCCCCBBBBBCCCCBBBBAAE.A.....",
    ".AAEEEAFAACCCCBBBBBBHHCCBBBBAAGEA.....",
    ".AAAEAAFAACCCBBBBBBBHHCCBBBBAAFKA.....",
    ".AAGFFAACCCCBBBBBBBBBBCCBBBBAAGA......",
    "...AGGKACCCCBBBBBBBBBBCCBBBBAAAA......",
    "...AAAAACCCCBBBBBBBBBBCCBBBBAA........",
    "....AAAAAAAAAAAAAAAAAAAAAAAAAA........",
    ".......AAAAAAAAAAAAAAAAAAAAA..........",
    "..........AEAEEAAAAAAEEAAA............",
    "..........AKKKKKAAAKKKKKAA............",
    "........AAKKKKKAAAKKKKKAAA............",
    "........AAEAEEEAAAAEEEEA..............",
    "........AAEEEEEAAAEEEEEA..............",
    "........AAKKKKKAAAKKKKKA..............",
    "........AAKKKKKAAAKKKKKA..............",
    "........AAEEEE.AAEAEEEAA..............",
    "........AAEEEE.AAAAEEEAA..............",
    "........AAKKKKAAAKKKKKAA..............",
    "........AAKKKKAAAKKKKKAA..............",
    ".......AAA...AAAAAA.A.AAA.............",
    ".......AAA.AAAAAAAAAA.AAA.............",
    ".......AHCBBBBBHACCBBBCAA.............",
    ".......AHCBBBBBAACCBBBBAA.............",
    ".......AHCCCCCCAACCCCCCAA.............",
    ".......AHCCCCCAAACCCCCAA..............",
    ".......AHCCCCCAAACCCCCAA..............",
    ".......AHCCCCCAAACCCCBAAAA............",
    ".......AHCBCCCAAACCBBBHAAA............",
    ".....AACCCBBBBBCACCCBBBBBBA...........",
    ".....AACCBBBFFBBCAACCCBBBFCAA.........",
    ".....AACCCCCCCCCCAACCCCCCCCAA.........",
    "...AAAACCCCCCCCCCAACCCCCCCCAAAA.......",
]

SPRITES_CORALINE = {}     # sprites ya armados (uno por cada lado al que mira)


def sprite_coraline_chica(mira_derecha: bool) -> pygame.Surface:

    """ARMA EL SPRITE UNA SOLA VEZ Y LO GUARDA. SI NO MIRA A LA DERECHA, SE VOLTEA."""

    if mira_derecha not in SPRITES_CORALINE:

        sprite = armar_sprite(CORALINE_FILAS, CORALINE_COLORES)

        if not mira_derecha:
            sprite = pygame.transform.flip(sprite, True, False)

        SPRITES_CORALINE[mira_derecha] = sprite

    return SPRITES_CORALINE[mira_derecha]


def dibujar_coraline_chica(lienzo: pygame.Surface, x: int, y_piso: int, mira_derecha: bool) -> None:

    """CORALINE PARADA CON SU SOMBRA. x ES EL CENTRO DE SUS PIES Y y_piso DONDE PISA."""

    sprite = sprite_coraline_chica(mira_derecha)

    sombra = pygame.Surface((sprite.get_width() + 6, 8), pygame.SRCALPHA)
    pygame.draw.ellipse(sombra, (0, 0, 0, 100), sombra.get_rect())
    lienzo.blit(sombra, (x - sombra.get_width() // 2, y_piso - 4))

    lienzo.blit(sprite, (x - sprite.get_width() // 2, y_piso - sprite.get_height()))
