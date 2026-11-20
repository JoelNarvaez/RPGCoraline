"""FONDO DIBUJADO CON CODIGO: METER LA MANO EN LA TELARANA POR LA SEGUNDA CANICA.

De cerca, en el escenario oscuro del teatro abandonado (teatro_abandonado.py):
una telarana enorme con la segunda canica envuelta en hilos en el centro. La
mano de Coraline (manga amarilla, guante azul) entra desde abajo y se acerca
despacio, dudando. En la oscuridad detras de la telarana se van asomando las
dos caras palidas de la criatura y, por la orilla, entra un brazo largo de
dedos flacos que tambien va hacia la canica. Se usa en cap08_n04.

Todo va en un ciclo de DURACION segundos:
- la mano avanza, se detiene, se echa un poco para atras y vuelve a avanzar,
- la criatura se asoma poco a poco y su brazo se arrastra por la telarana,
- la telarana tiembla mas entre mas cerca esta la mano,
- las orillas se oscurecen con un latido que se va acelerando,
- al final se abren los ojos de la criatura, la telarana se sacude y todo
  se va a negro antes de volver a empezar.
"""

import math

import pygame

from interfaz.fondos.pintura import ANCHO, ALTO
from interfaz.fondos.pintura import COLOR_CONTORNO
from interfaz.fondos.pintura import mezclar, degradado, brillo, mostrar
from interfaz.fondos import personajes
from interfaz.fondos import teatro_abandonado
from interfaz.fondos import hueco_espejo

CENTRO = (506, 196)                 # el centro de la telarana, donde esta la canica
RADIO = 132
RAYOS = 16
VUELTAS = 9

ANGULO_MANO = 38                    # la mano entra en diagonal, de abajo a la izquierda
INICIO_MANO = (402, 404)            # donde esta la punta de los dedos al empezar (fuera de la pantalla)
FIN_MANO = (494, 210)               # casi tocando la canica
LARGO_MANGA = 300
PUNTA_MANO = LARGO_MANGA + 60       # la punta del indice, contada desde el hombro del sprite (sin girar)

DURACION = 10.0
SUSTO = 7.6                         # cuando se le abren los ojos a la criatura
NEGRO = 8.8                         # desde aqui se va a negro

COLOR_TELARANA = (200, 204, 214)
ANCHO_CRIATURA = 100
COLOR_PALIDO = teatro_abandonado.COLOR_PALIDO

CAPAS = {}


# --------------------------------------------------
# PARTE FIJA
# --------------------------------------------------

def crear_fondo() -> pygame.Surface:

    """EL FONDO DEL ESCENARIO: TELON VINO CASI NEGRO Y UNA LUZ DEBIL QUE CAE SOBRE LA TELARANA."""

    lienzo = pygame.Surface((ANCHO, ALTO))
    degradado(lienzo, pygame.Rect(0, 0, ANCHO, ALTO), (14, 8, 14), (30, 14, 22), 10)

    # PLIEGUES DEL TELON
    for x in range(0, ANCHO, 22):
        pygame.draw.line(lienzo, (40, 18, 28), (x, 0), (x + 4, ALTO), 3)
        pygame.draw.line(lienzo, (22, 10, 16), (x + 9, 0), (x + 12, ALTO), 2)

    # LA ORILLA DEL ESCENARIO, ABAJO
    pygame.draw.rect(lienzo, (26, 16, 18), (0, 326, ANCHO, ALTO - 326))
    pygame.draw.line(lienzo, (70, 52, 40), (0, 326), (ANCHO, 326), 2)

    brillo(lienzo, (CENTRO[0], CENTRO[1] - 40), 160, (150, 150, 190), 45)

    return lienzo


def crear_sombra() -> pygame.Surface:

    """UNA ORILLA OSCURA MUY FUERTE (SE CALCULA CHICA Y SE AGRANDA). SU TRANSPARENCIA LATE."""

    chica = pygame.Surface((160, 90), pygame.SRCALPHA)

    for y in range(90):
        for x in range(160):
            dx = abs(x - (CENTRO[0] / 4)) / 80
            dy = abs(y - (CENTRO[1] / 4)) / 45
            distancia = math.sqrt(dx * dx * 0.8 + dy * dy * 0.8)
            alfa = int(max(0.0, distancia - 0.25) * 300)
            chica.set_at((x, y), (0, 0, 0, min(alfa, 235)))

    return pygame.transform.smoothscale(chica, (ANCHO, ALTO))


def crear_mano() -> pygame.Surface:

    """LA MANO DE CORALINE APUNTANDO A LA DERECHA (DESPUES SE GIRA): MANGA LARGA, GUANTE Y DEDOS ESTIRADOS.

    La manga es tan larga que siempre se sale por la orilla de abajo de la pantalla.
    """

    m = LARGO_MANGA
    mano = pygame.Surface((m + 70, 44), pygame.SRCALPHA)

    # MANGA DEL IMPERMEABLE CON SU PUNO
    pygame.draw.rect(mano, personajes.AMARILLO, (0, 6, m, 32))
    pygame.draw.line(mano, personajes.AMARILLO_CLARO, (0, 10), (m - 4, 10), 2)
    pygame.draw.line(mano, personajes.AMARILLO_SOMBRA, (0, 33), (m - 4, 33), 3)
    pygame.draw.rect(mano, personajes.AMARILLO_SOMBRA, (m - 8, 4, 10, 36))

    # GUANTE AZUL MARINO SIN DEDOS
    pygame.draw.ellipse(mano, personajes.AZUL_OSCURO, (m - 2, 8, 40, 28))
    pygame.draw.line(mano, personajes.AZUL, (m + 4, 14), (m + 28, 12), 2)

    # DEDOS ESTIRADOS (EL INDICE MAS LARGO) Y EL PULGAR
    for i, largo in enumerate([30, 26, 22, 18]):
        dedo = pygame.Rect(m + 30, 12 + i * 6, largo, 6)
        pygame.draw.rect(mano, personajes.PIEL_CHIBI, dedo, border_radius=3)
        pygame.draw.line(mano, personajes.PIEL_CHIBI_SOMBRA, (dedo.x + 2, dedo.bottom - 1), (dedo.right - 3, dedo.bottom - 1))
    pygame.draw.ellipse(mano, personajes.PIEL_CHIBI, (m + 22, 2, 22, 10))

    return pygame.transform.rotate(personajes.con_contorno(mano), ANGULO_MANO)


def crear_capas() -> None:

    CAPAS["fondo"] = crear_fondo()
    CAPAS["sombra"] = crear_sombra()
    CAPAS["mano"] = crear_mano()


# --------------------------------------------------
# EL TIEMPO DE LA ESCENA
# --------------------------------------------------

def suave(avance: float) -> float:

    avance = max(0.0, min(1.0, avance))

    return avance * avance * (3 - 2 * avance)


def avance_de_la_mano(fase: float) -> float:

    """0 = FUERA DE LA PANTALLA, 1 = CASI TOCANDO LA CANICA. AVANZA, DUDA, SE ECHA PARA ATRAS Y VUELVE."""

    if fase < 2.8:
        return suave(fase / 2.8) * 0.55
    if fase < 3.6:
        return 0.55                                              # se queda quieta: duda
    if fase < 4.4:
        return 0.55 - suave((fase - 3.6) / 0.8) * 0.12          # se echa un poco para atras
    if fase < SUSTO:
        return 0.43 + suave((fase - 4.4) / (SUSTO - 4.4)) * 0.57

    return 1.0


def cercania(fase: float) -> float:

    """QUE TAN CERCA ESTA TODO DEL SUSTO (0 AL EMPEZAR, 1 EN EL SUSTO)."""

    return max(0.0, min(1.0, fase / SUSTO))


# --------------------------------------------------
# LO QUE SE MUEVE
# --------------------------------------------------

def crear_criatura(ojos_prendidos: bool) -> pygame.Surface:

    """LAS DOS CABEZAS DE LA CRIATURA SALIENDO DE UN SOLO CUERPO QUE SE PIERDE EN LO OSCURO.

    Caras alargadas, ladeadas una hacia la otra, con cuencas hundidas y la boca
    cosida. Con ojos_prendidos, cada cuenca tiene un puntito blanco (el susto).
    """

    criatura = pygame.Surface((ANCHO_CRIATURA, 190), pygame.SRCALPHA)
    centro = ANCHO_CRIATURA // 2
    sombra = teatro_abandonado.COLOR_PALIDO_SOMBRA
    hueco = (12, 8, 14)

    # CUERPO ANGOSTO, COMO DOS HOMBROS PEGADOS
    pygame.draw.ellipse(criatura, mezclar(sombra, (0, 0, 0), 0.3), (centro - 36, 56, 72, 140))

    for cx, cy, chongo, ladeo in [(centro - 18, 24, True, 3), (centro + 18, 30, False, -3)]:

        # CUELLO QUE SE ESTIRA HACIA EL CUERPO Y CARA ALARGADA
        pygame.draw.line(criatura, sombra, (cx, cy + 14), (cx + ladeo * 3, cy + 40), 8)
        pygame.draw.ellipse(criatura, COLOR_PALIDO, (cx - 11 + ladeo, cy - 15, 22, 32))
        if chongo:
            pygame.draw.circle(criatura, sombra, (cx + ladeo, cy - 17), 7)
        else:
            for rx in [-9, -3, 3, 9]:
                pygame.draw.circle(criatura, sombra, (cx + ladeo + rx, cy - 14), 5)

        # CUENCAS HUNDIDAS Y BOCA COSIDA
        for dx in [-6, 3]:
            pygame.draw.ellipse(criatura, hueco, (cx + ladeo + dx, cy - 5, 5, 8))
            if ojos_prendidos:
                pygame.draw.rect(criatura, (255, 255, 255), (cx + ladeo + dx + 2, cy - 2, 2, 2))

        boca_y = cy + 9
        pygame.draw.line(criatura, hueco, (cx + ladeo - 5, boca_y), (cx + ladeo + 5, boca_y))
        for px in range(-4, 6, 3):
            pygame.draw.line(criatura, hueco, (cx + ladeo + px, boca_y - 2), (cx + ladeo + px, boca_y + 2))

    # DE LOS HOMBROS PARA ABAJO SE VA HACIENDO TRANSPARENTE
    hueco_espejo.desvanecer_abajo(criatura, 0.3)

    return criatura


def dibujar_criatura(lienzo: pygame.Surface, fase: float, tiempo: float) -> None:

    """LA CRIATURA SE ASOMA DETRAS DE LA TELARANA (CADA VEZ MAS VISIBLE Y MAS CERCA).
    EN EL SUSTO SE LE ABREN LOS OJOS."""

    aparece = suave((fase - 1.5) / 5.5)

    if aparece <= 0:
        return

    clave = "criatura_susto" if fase >= SUSTO else "criatura"
    if clave not in CAPAS:
        CAPAS[clave] = crear_criatura(fase >= SUSTO)

    criatura = CAPAS[clave].copy()
    criatura.set_alpha(int(aparece * 190))

    x = 588 - ANCHO_CRIATURA // 2 - int(aparece * 12)
    y = 88 + int(math.sin(tiempo * 0.7) * 2)

    lienzo.blit(criatura, (x, y))


def dibujar_telarana(lienzo: pygame.Surface, fase: float, tiempo: float) -> None:

    """LA TELARANA GRANDE. TIEMBLA MAS ENTRE MAS CERCA ESTA LA MANO, Y SE SACUDE EN EL SUSTO."""

    if fase >= SUSTO:
        fuerza = 4.0 * (1 - (fase - SUSTO) / (DURACION - SUSTO))
    else:
        fuerza = avance_de_la_mano(fase) ** 3 * 1.6

    puntos = []

    for i in range(RAYOS):
        angulo = i / RAYOS * math.pi * 2 + 0.1
        rayo = []
        for vuelta in range(VUELTAS + 1):
            distancia = RADIO * vuelta / VUELTAS * (0.92 + 0.08 * math.sin(i * 1.7))
            tiembla = math.sin(tiempo * 23 + vuelta * 1.3 + i) * fuerza * (vuelta / VUELTAS)
            rayo.append((CENTRO[0] + math.cos(angulo) * distancia + tiembla,
                         CENTRO[1] + math.sin(angulo) * distancia + tiembla * 0.6))
        puntos.append(rayo)

    capa = pygame.Surface((ANCHO, ALTO), pygame.SRCALPHA)

    for i in range(RAYOS):
        pygame.draw.lines(capa, (*COLOR_TELARANA, 150), False, puntos[i])

    for vuelta in range(1, VUELTAS + 1):
        alfa = 170 - vuelta * 12
        anillo = [puntos[i][vuelta] for i in range(RAYOS)]
        pygame.draw.lines(capa, (*COLOR_TELARANA, alfa), True, anillo)

    lienzo.blit(capa, (0, 0))

    # UN BRILLO QUE CORRE POR UN RAYO, COMO SI ALGO LO HUBIERA TOCADO
    rayo = puntos[int(tiempo * 1.3) % RAYOS]
    paso = int((tiempo * 6) % VUELTAS)
    lienzo.set_at((int(rayo[paso][0]), int(rayo[paso][1])), (250, 250, 255))


def dibujar_canica(lienzo: pygame.Surface, tiempo: float) -> None:

    """LA SEGUNDA CANICA ENVUELTA EN HILOS, CON UN BRILLO AZUL QUE LATE (ES UN ALMA)."""

    x, y = CENTRO
    luz = (math.sin(tiempo * 3) + 1) / 2

    capa = pygame.Surface((40, 40), pygame.SRCALPHA)
    pygame.draw.circle(capa, (160, 200, 255, int(30 + luz * 40)), (20, 20), 16)
    lienzo.blit(capa, (x - 20, y - 20))

    pygame.draw.circle(lienzo, COLOR_CONTORNO, (x, y), 7)
    pygame.draw.circle(lienzo, (210, 220, 236), (x, y), 6)
    pygame.draw.line(lienzo, (230, 150, 200), (x - 3, y + 2), (x + 3, y - 2), 2)
    lienzo.set_at((x - 2, y - 3), (255, 255, 255))

    for dy in [-4, 0, 3]:                                                     # hilos que la envuelven
        pygame.draw.line(lienzo, COLOR_TELARANA, (x - 8, y + dy - 2), (x + 8, y + dy + 2))


def dibujar_brazo(lienzo: pygame.Surface, fase: float, tiempo: float) -> None:

    """EL BRAZO LARGO Y PALIDO DE LA CRIATURA SE ARRASTRA POR LA TELARANA DESDE LA ORILLA DERECHA."""

    avance = suave((fase - 3.0) / (SUSTO - 3.0)) * 0.9

    if avance <= 0:
        return

    hombro = (ANCHO + 10, 120)
    codo = (ANCHO - 40 - int(avance * 30), 150 + int(math.sin(tiempo * 2) * 2))
    mano = (ANCHO - int(avance * (ANCHO - CENTRO[0] - 22)), CENTRO[1] - 10 + int(math.sin(tiempo * 3) * 2))

    for grueso, color in [(5, COLOR_CONTORNO), (3, COLOR_PALIDO)]:
        pygame.draw.line(lienzo, color, hombro, codo, grueso)
        pygame.draw.line(lienzo, color, codo, mano, grueso)

    # DEDOS LARGUISIMOS QUE SE MUEVEN COMO PATAS
    for i in range(4):
        angulo = math.radians(150 + i * 22) + math.sin(tiempo * 6 + i) * 0.15
        punta = (mano[0] + int(math.cos(angulo) * 16), mano[1] + int(math.sin(angulo) * 16))
        pygame.draw.line(lienzo, COLOR_CONTORNO, mano, punta, 3)
        pygame.draw.line(lienzo, COLOR_PALIDO, mano, punta, 1)


def dibujar_mano(lienzo: pygame.Surface, fase: float) -> None:

    """LA MANO DE CORALINE: LA PUNTA DE LOS DEDOS VA DE INICIO_MANO A FIN_MANO."""

    avance = avance_de_la_mano(fase)
    punta = (INICIO_MANO[0] + (FIN_MANO[0] - INICIO_MANO[0]) * avance,
             INICIO_MANO[1] + (FIN_MANO[1] - INICIO_MANO[1]) * avance)

    # DEL CENTRO DEL SPRITE A LA PUNTA HAY (PUNTA_MANO - MITAD DEL ANCHO), EN LA DIRECCION EN QUE APUNTA
    angulo = math.radians(ANGULO_MANO)
    distancia = PUNTA_MANO - (LARGO_MANGA + 70) / 2
    centro = (punta[0] - math.cos(angulo) * distancia, punta[1] + math.sin(angulo) * distancia)

    mano = CAPAS["mano"]
    lienzo.blit(mano, (int(centro[0] - mano.get_width() / 2), int(centro[1] - mano.get_height() / 2)))


def dibujar_latido(lienzo: pygame.Surface, fase: float, tiempo: float) -> None:

    """LAS ORILLAS SE OSCURECEN CON UN LATIDO DOBLE (PUM-PUM) QUE SE ACELERA HACIA EL SUSTO."""

    ritmo = 1.0 + cercania(fase) * 1.6
    golpe = (tiempo * ritmo) % 1
    latido = max(0.0, 1 - golpe / 0.12) + max(0.0, 1 - abs(golpe - 0.22) / 0.1) * 0.7

    sombra = CAPAS["sombra"]
    sombra.set_alpha(int(150 + cercania(fase) * 60 + latido * 45))
    lienzo.blit(sombra, (0, 0))


def dibujar_negro(lienzo: pygame.Surface, fase: float) -> None:

    """DESPUES DEL SUSTO TODO SE VA A NEGRO Y LUEGO VUELVE POCO A POCO."""

    if fase < NEGRO:
        if fase < 0.6:
            alfa = int((1 - fase / 0.6) * 255)                         # regresa del negro
        else:
            return
    else:
        alfa = int(suave((fase - NEGRO) / (DURACION - NEGRO - 0.3)) * 255)

    negro = pygame.Surface((ANCHO, ALTO))
    negro.set_alpha(alfa)
    lienzo.blit(negro, (0, 0))


def dibujar(ventana: pygame.Surface) -> None:

    """DIBUJA LA ESCENA COMPLETA EN LA VENTANA DEL JUEGO."""

    if "fondo" not in CAPAS:
        crear_capas()

    # EL CICLO EMPIEZA DESDE CERO CADA VEZ QUE SE ENTRA A LA ESCENA (SI NO SE HABIA DIBUJADO
    # EN EL ULTIMO MEDIO SEGUNDO, ES QUE EL JUGADOR ACABA DE LLEGAR)
    ahora = pygame.time.get_ticks() / 1000
    if ahora - CAPAS.get("ultimo", -10.0) > 0.5:
        CAPAS["inicio"] = ahora
    CAPAS["ultimo"] = ahora

    tiempo = ahora - CAPAS["inicio"]
    fase = tiempo % DURACION

    lienzo = CAPAS["fondo"].copy()

    dibujar_criatura(lienzo, fase, tiempo)
    dibujar_telarana(lienzo, fase, tiempo)
    dibujar_canica(lienzo, tiempo)
    dibujar_brazo(lienzo, fase, tiempo)
    dibujar_mano(lienzo, fase)
    teatro_abandonado.dibujar_polvo(lienzo, tiempo)
    dibujar_latido(lienzo, fase, tiempo)

    # EN EL SUSTO, UN DESTELLO PALIDO MUY CORTO
    if SUSTO <= fase < SUSTO + 0.12:
        destello = pygame.Surface((ANCHO, ALTO))
        destello.fill(mezclar((200, 200, 220), (0, 0, 0), 0.3))
        destello.set_alpha(90)
        lienzo.blit(destello, (0, 0))

    dibujar_negro(lienzo, fase)

    mostrar(ventana, lienzo)
