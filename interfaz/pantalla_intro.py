import os
import math
import random
import pygame

import config
from interfaz import dibujo

DURACION_CARGA = 4.2
DURACION_INTRO = 7.5

def crear_particulas(contexto):
    # CREAMOS LAS PARTICULAS UNA SOLA VEZ
    particulas = []
    for i in range(50):
        particula = {
            "x": random.randint(0, config.ANCHO),
            "y": random.randint(0, config.ALTO),
            "velocidad": random.uniform(2, 6),
            "tamano": random.randint(2, 4),
            "brillo": random.randint(120, 190),
            "fase": random.uniform(0, 6.28),
            "color": random.choice([
                (100, 170, 220),
                (235, 205, 120)
            ])
        }
        particulas.append(particula)

    contexto["particulas"] = particulas


def actualizar_particulas(contexto, dt):
    # MOVEMOS LAS PARTICULAS LENTAMENTE
    for particula in contexto["particulas"]:
        particula["y"] -= particula["velocidad"] * dt

        # MOVIMIENTO HORIZONTAL MUY SUAVE
        particula["x"] += math.sin(
        contexto["tiempo_intro"] * 0.3 + particula["fase"]
        ) * 0.5 * dt
        
        # SI SALE DE LA PANTALLA, VUELVE A APARECER
        if particula["y"] < 0:
            particula["y"] = config.ALTO + 5
            particula["x"] = random.randint(0, config.ANCHO)


def dibujar_particulas(ventana, contexto):
    # CREAMOS UNA CAPA TRANSPARENTE
    capa = pygame.Surface(
        (config.ANCHO, config.ALTO),
        pygame.SRCALPHA
    )

    tiempo = contexto["tiempo_intro"]

    for particula in contexto["particulas"]:
        # HACEMOS QUE EL BRILLO CAMBIE SUAVEMENTE
        # HACEMOS QUE EL BRILLO CAMBIE SUAVEMENTE
        brillo = math.sin(
            tiempo * 2 + particula["fase"]
        )

        transparencia = int(
            particula["brillo"] + brillo * 45
        )

        transparencia = max(60, min(220, transparencia))

        color = (*particula["color"], transparencia)

        pygame.draw.circle(
            capa,
            color,
            (int(particula["x"]), int(particula["y"])),
            particula["tamano"]
        )

    ventana.blit(capa, (0, 0))


def manejar_evento(evento, contexto):
    if evento.type == pygame.KEYDOWN or evento.type == pygame.MOUSEBUTTONDOWN:
        return "menu"
    return ""


def actualizar(contexto, dt):
    contexto["tiempo_intro"] = contexto.get("tiempo_intro", 0.0) + dt

    # SI AUN NO EXISTEN LAS PARTICULAS, LAS CREAMOS
    if "particulas" not in contexto:
        crear_particulas(contexto)

    # ACTUALIZAMOS LAS PARTICULAS
    actualizar_particulas(contexto, dt)


def dibujar_boton(ventana, x, y, radio):
    # DIBUJAMOS EL BOTON AMARILLO
    pygame.draw.circle(ventana, (226, 202, 91), (x, y), radio)

    # BORDE EXTERIOR
    pygame.draw.circle(ventana, (105, 83, 36), (x, y), radio, 2)

    # BORDE INTERIOR
    pygame.draw.circle(ventana, (245, 222, 135), (x, y), radio - 4, 1)

    # AGREGAMOS LOS CUATRO AGUJEROS
    distancia = radio // 3
    tamano = max(2, radio // 7)

    pygame.draw.circle(ventana, (40, 32, 20),
                       (x - distancia, y - distancia), tamano)

    pygame.draw.circle(ventana, (40, 32, 20),
                       (x + distancia, y - distancia), tamano)

    pygame.draw.circle(ventana, (40, 32, 20),
                       (x - distancia, y + distancia), tamano)

    pygame.draw.circle(ventana, (40, 32, 20),
                       (x + distancia, y + distancia), tamano)


def dibujar(ventana, contexto):
    tiempo = contexto.get("tiempo_intro", 0.0)
    centro = config.ANCHO // 2
    fuentes = contexto["fuentes"]

    # FONDO COMPLETAMENTE NEGRO
    ventana.fill((0, 0, 0))

    # CARGAMOS LA IMAGEN DE CORALINE
    if "imagen_intro" not in contexto:
        ruta = os.path.join(config.RUTA_IMAGENES, "Intro.jpg")

        if os.path.exists(ruta):
            imagen = pygame.image.load(ruta).convert_alpha()
            contexto["imagen_intro"] = imagen
        else:
            contexto["imagen_intro"] = None

    imagen = contexto["imagen_intro"]

    # MOSTRAMOS LA IMAGEN DE CORALINE
    if imagen is not None:
        # HACEMOS LA IMAGEN UN POCO MAS GRANDE
        imagen = pygame.transform.smoothscale(imagen, (460, 327))

        # AGREGAMOS UN MOVIMIENTO SUAVE
        movimiento = math.sin(tiempo * 1.5) * 5

        # CALCULAMOS LA POSICION DE LA IMAGEN
        imagen_x = centro - 230
        imagen_y = 190 + movimiento

        # CREAMOS UN BRILLO AZUL DETRAS DE CORALINE
        brillo = pygame.Surface((220, 220), pygame.SRCALPHA)

        pygame.draw.circle(
            brillo,
            (35, 85, 130, 12),
            (110, 110),
            105
        )

        pygame.draw.circle(
            brillo,
            (45, 100, 155, 15),
            (110, 110),
            75
        )

        ventana.blit(brillo, (centro - 110, imagen_y + 45))

        # DIBUJAMOS UNA SOMBRA DEBAJO DE SUS PIES
        sombra = pygame.Surface((180, 30), pygame.SRCALPHA)

        pygame.draw.ellipse(
            sombra,
            (70, 65, 45, 65),
            (10, 5, 160, 20)
        )

        ventana.blit(sombra, (centro - 90, imagen_y + 295))

        # MOSTRAMOS A CORALINE
        ventana.blit(imagen, (imagen_x, imagen_y))

        # DIBUJAMOS LAS PARTICULAS SOBRE EL FONDO Y LA IMAGEN
        dibujar_particulas(ventana, contexto)

    # TITULO DEL JUEGO
    fuente_titulo = fuentes["titulo_intro"]

    # DIVIDIMOS EL TITULO EN DOS PARTES
    letra_c = fuente_titulo.render("C", True, (245, 232, 185))
    letras_finales = fuente_titulo.render("raline", True, (245, 232, 185))

    # CALCULAMOS EL TAMANO DEL BOTON
    ancho_o, alto_o = fuente_titulo.size("O")

    radio = min(ancho_o, letra_c.get_height()) // 2

    # CALCULAMOS EL ANCHO TOTAL DEL TITULO
    ancho_total = letra_c.get_width() + (radio * 2) + letras_finales.get_width()

    # CENTRAMOS EL TITULO
    titulo_x = centro - ancho_total // 2
    titulo_y = 65

    # DIBUJAMOS LA PRIMERA LETRA
    ventana.blit(letra_c, (titulo_x, titulo_y))

    # CALCULAMOS LA POSICION DEL BOTON
    boton_x = titulo_x + letra_c.get_width() + radio
    boton_y = titulo_y + letra_c.get_height() // 2

    # DIBUJAMOS EL BOTON EN LUGAR DE LA O
    dibujar_boton(ventana, boton_x, boton_y, radio)

    # DIBUJAMOS LAS LETRAS RESTANTES
    final_x = titulo_x + letra_c.get_width() + (radio * 2)

    ventana.blit(letras_finales, (final_x, titulo_y))

    # SUBTITULO
    dibujo.dibujar_texto_centrado(
        ventana,
        "Y LA PUERTA SECRETA",
        fuentes["pequena"],
        (195, 185, 155),
        centro,
        155
    )

    # TEXTO DE CARGA
    dibujo.dibujar_texto_centrado(
        ventana,
        "PREPARANDO LA HISTORIA...",
        fuentes["pequena"],
        (225, 215, 190),
        centro,
        525
    )

    # BARRA DE PROGRESO
    ancho_barra = 440
    alto_barra = 15

    x = centro - ancho_barra // 2
    y = 560

    # CALCULAMOS EL PROGRESO
    progreso = min(tiempo / DURACION_CARGA, 1.0)
    ancho_progreso = int((ancho_barra - 6) * progreso)

    # CREAMOS UNA CAPA PARA EL RESPLANDOR
    brillo_barra = pygame.Surface(
        (ancho_barra + 20, alto_barra + 20),
        pygame.SRCALPHA
    )

    # DIBUJAMOS UN RESPLANDOR DORADO
    pygame.draw.rect(
        brillo_barra,
        (255, 190, 45, 35),
        (10, 10, ancho_barra, alto_barra),
        border_radius=10
    )

    ventana.blit(brillo_barra, (x - 10, y - 10))

    # FONDO DE LA BARRA
    pygame.draw.rect(
        ventana,
        (38, 35, 30),
        (x, y, ancho_barra, alto_barra),
        border_radius=7
    )

    # BORDE DORADO
    pygame.draw.rect(
        ventana,
        (205, 178, 73),
        (x, y, ancho_barra, alto_barra),
        2,
        border_radius=7
    )

    # PARTE QUE SE VA LLENANDO
    if ancho_progreso > 0:

        pygame.draw.rect(
            ventana,
            (218, 190, 86),
            (x + 3, y + 3, ancho_progreso, alto_barra - 6),
            border_radius=5
        )

        # DESTELLO CERCA DEL EXTREMO DE LA BARRA
        ancho_destello = 24

        posicion_brillo = x + 3 + ancho_progreso - ancho_destello // 2

        # CREAMOS EL DESTELLO
        destello = pygame.Surface(
            (ancho_destello, alto_barra - 6),
            pygame.SRCALPHA
        )

        pygame.draw.ellipse(
            destello,
            (255, 250, 200, 210),
            (0, 0, ancho_destello, alto_barra - 6)
        )

        # LIMITAMOS EL DESTELLO A LA PARTE CARGADA
        ventana.blit(
            destello,
            (posicion_brillo, y + 3),
            area=pygame.Rect(
                0, 0,
                min(ancho_destello, ancho_progreso),
                alto_barra - 6
            )
        )

    # INDICACION PARA CONTINUAR
    dibujo.dibujar_texto_centrado(
        ventana,
        "PULSA CUALQUIER TECLA PARA CONTINUAR",
        fuentes["pequena"],
        (135, 130, 120),
        centro,
        610
    )
    
    # TRANSICION CINEMATOGRAFICA
    if tiempo >= DURACION_CARGA:

        # CALCULAMOS EL OSCURECIMIENTO
        tiempo_oscuro = tiempo - DURACION_CARGA

        opacidad = min(
            int(tiempo_oscuro * 235),
            235
        )

        # CREAMOS UNA CAPA NEGRA TRANSPARENTE
        capa_oscura = pygame.Surface(
            (config.ANCHO, config.ALTO),
            pygame.SRCALPHA
        )

        capa_oscura.fill((0, 0, 0, opacidad))

        ventana.blit(capa_oscura, (0, 0))

       
        # MOSTRAMOS LA FRASE MISTERIOSA
        if tiempo >= DURACION_CARGA + 1.0:

            tiempo_frase = tiempo - (DURACION_CARGA + 1.0)

            # CALCULAMOS LA APARICION DE LA FRASE
            opacidad_frase = min(
                int(tiempo_frase * 255),
                255
            )

            # HACEMOS QUE DESAPAREZCA AL FINAL
            if tiempo >= DURACION_INTRO - 0.8:
                opacidad_frase = int(
                    255 * (DURACION_INTRO - tiempo) / 0.8
                )

            opacidad_frase = max(
                0,
                min(255, opacidad_frase)
            )

            # PREPARAMOS LAS DOS FRASES
            frase_1 = fuentes["frase_intro"].render(
                "A veces, descubrir una puerta",
                True,
                (245, 232, 185)
            )

            frase_2 = fuentes["frase_intro"].render(
                "es el comienzo de una pesadilla...",
                True,
                (245, 232, 185)
            )

            # AGREGAMOS LA TRANSPARENCIA
            frase_1.set_alpha(opacidad_frase)
            frase_2.set_alpha(opacidad_frase)

            # CENTRAMOS LA PRIMERA FRASE
            ventana.blit(
                frase_1,
                frase_1.get_rect(
                    center=(centro, config.ALTO // 2 - 18)
                )
            )

            # CENTRAMOS LA SEGUNDA FRASE
            ventana.blit(
                frase_2,
                frase_2.get_rect(
                    center=(centro, config.ALTO // 2 + 22)
                )
            )