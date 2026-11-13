"""Figuras dibujadas con código para los minijuegos (llave, gato, mano, etc.).

Todas reciben la ventana y el centro (x, y). Se dibujan con formas simples de
pygame para que combinen entre sí sin depender de imágenes externas.

Responsable: Persona B
"""

import math

import pygame

NEGRO: tuple = (12, 10, 20)
PALIDO: tuple = (235, 228, 220)
DORADO: tuple = (220, 170, 60)
ROJO: tuple = (190, 40, 50)


def puerta(ventana: pygame.Surface, x: int, y: int, encontrada: bool) -> None:
    rect: pygame.Rect = pygame.Rect(0, 0, 38, 64)
    rect.center = (x, y)
    color: tuple = (110, 70, 40)
    pygame.draw.rect(ventana, color, rect, border_radius=4)
    pygame.draw.rect(ventana, (70, 42, 22), rect, 3, border_radius=4)
    pygame.draw.circle(ventana, DORADO, (rect.right - 9, rect.centery), 4)
    if encontrada:
        pygame.draw.rect(ventana, DORADO, rect.inflate(10, 10), 3, border_radius=6)


def hoja(ventana: pygame.Surface, x: int, y: int, encontrada: bool) -> None:
    rect: pygame.Rect = pygame.Rect(0, 0, 30, 16)
    rect.center = (x, y)
    pygame.draw.ellipse(ventana, (60, 90, 50), rect)
    pygame.draw.line(ventana, (35, 55, 30), rect.midleft, rect.midright, 2)
    if encontrada:
        pygame.draw.ellipse(ventana, DORADO, rect.inflate(10, 10), 3)


def llave(ventana: pygame.Surface, x: int, y: int) -> None:
    # Contorno claro para que la llave negra se vea sobre fondos oscuros
    pygame.draw.circle(ventana, (170, 160, 200), (x - 34, y), 21)
    pygame.draw.rect(ventana, (170, 160, 200), (x - 20, y - 8, 62, 16))
    pygame.draw.rect(ventana, (170, 160, 200), (x + 21, y + 2, 22, 18))
    pygame.draw.circle(ventana, NEGRO, (x - 34, y), 18)
    pygame.draw.circle(ventana, (90, 85, 110), (x - 34, y), 18, 3)
    pygame.draw.circle(ventana, (40, 36, 60), (x - 34, y), 8)
    pygame.draw.rect(ventana, NEGRO, (x - 18, y - 5, 56, 10))
    pygame.draw.rect(ventana, NEGRO, (x + 24, y + 5, 8, 12))
    pygame.draw.rect(ventana, NEGRO, (x + 34, y + 5, 6, 8))


def cerradura(ventana: pygame.Surface, x: int, y: int) -> None:
    placa: pygame.Rect = pygame.Rect(0, 0, 70, 110)
    placa.center = (x, y)
    pygame.draw.rect(ventana, DORADO, placa, border_radius=12)
    pygame.draw.rect(ventana, (150, 110, 30), placa, 3, border_radius=12)
    pygame.draw.circle(ventana, NEGRO, (x, y - 10), 12)
    pygame.draw.polygon(ventana, NEGRO, [(x - 8, y - 4), (x + 8, y - 4), (x + 12, y + 30), (x - 12, y + 30)])


def mantel(ventana: pygame.Surface, x: int, y: int) -> None:
    rect: pygame.Rect = pygame.Rect(0, 0, 120, 90)
    rect.center = (x, y)
    pygame.draw.rect(ventana, PALIDO, rect)
    for i in range(1, 4):
        pygame.draw.line(ventana, ROJO, (rect.x + i * 30, rect.y), (rect.x + i * 30, rect.bottom), 4)
        pygame.draw.line(ventana, ROJO, (rect.x, rect.y + i * 22), (rect.right, rect.y + i * 22), 4)


def pozo(ventana: pygame.Surface, x: int, y: int) -> None:
    pygame.draw.ellipse(ventana, (95, 90, 100), (x - 95, y - 50, 190, 100))
    pygame.draw.ellipse(ventana, NEGRO, (x - 70, y - 34, 140, 68))


def gato(ventana: pygame.Surface, x: int, y: int) -> None:
    pygame.draw.ellipse(ventana, NEGRO, (x - 34, y - 6, 68, 40))
    pygame.draw.circle(ventana, NEGRO, (x + 26, y - 12), 20)
    pygame.draw.polygon(ventana, NEGRO, [(x + 10, y - 22), (x + 16, y - 44), (x + 24, y - 28)])
    pygame.draw.polygon(ventana, NEGRO, [(x + 28, y - 28), (x + 38, y - 44), (x + 42, y - 22)])
    pygame.draw.circle(ventana, (120, 220, 90), (x + 20, y - 14), 4)
    pygame.draw.circle(ventana, (120, 220, 90), (x + 34, y - 14), 4)
    pygame.draw.line(ventana, NEGRO, (x - 32, y + 10), (x - 56, y - 20), 6)


def boton_ojo(ventana: pygame.Surface, x: int, y: int, radio: int) -> None:
    pygame.draw.circle(ventana, NEGRO, (x, y), radio)
    pygame.draw.circle(ventana, (60, 60, 70), (x, y), radio, 2)
    separacion: int = radio // 3
    for dx in [-separacion, separacion]:
        for dy in [-separacion, separacion]:
            pygame.draw.circle(ventana, (70, 70, 80), (x + dx, y + dy), 2)


def otra_madre(ventana: pygame.Surface, x: int, y: int) -> None:
    pygame.draw.polygon(ventana, NEGRO, [(x, y - 30), (x - 60, y + 120), (x + 60, y + 120)])
    pygame.draw.circle(ventana, NEGRO, (x, y - 60), 44)
    pygame.draw.circle(ventana, PALIDO, (x, y - 52), 34)
    boton_ojo(ventana, x - 13, y - 58, 10)
    boton_ojo(ventana, x + 13, y - 58, 10)
    pygame.draw.arc(ventana, ROJO, (x - 14, y - 46, 28, 18), math.pi + 0.3, 2 * math.pi - 0.3, 3)


def canica(ventana: pygame.Surface, x: int, y: int, brilla: bool) -> None:
    if brilla:
        for radio in [30, 22, 16]:
            pygame.draw.circle(ventana, (120 + radio * 4, 30, 30), (x, y), radio)
    pygame.draw.circle(ventana, (130, 128, 140), (x, y), 11)
    pygame.draw.circle(ventana, (200, 200, 210), (x - 4, y - 4), 3)


def rata(ventana: pygame.Surface, x: int, y: int, mirando_derecha: bool) -> None:
    direccion: int = 1 if mirando_derecha else -1
    pygame.draw.ellipse(ventana, (45, 40, 50), (x - 26, y - 12, 52, 26))
    pygame.draw.circle(ventana, (45, 40, 50), (x + 26 * direccion, y - 2), 11)
    pygame.draw.circle(ventana, ROJO, (x + 30 * direccion, y - 5), 3)
    pygame.draw.line(ventana, (45, 40, 50), (x - 24 * direccion, y + 4), (x - 52 * direccion, y - 6), 3)


def sombra(ventana: pygame.Surface, x: int, y: int, radio: int) -> None:
    pygame.draw.circle(ventana, (90, 60, 130), (x, y), radio + 5)
    pygame.draw.circle(ventana, NEGRO, (x, y), radio)
    pygame.draw.circle(ventana, ROJO, (x - radio // 3, y - radio // 5), 4)
    pygame.draw.circle(ventana, ROJO, (x + radio // 3, y - radio // 5), 4)


def mano(ventana: pygame.Surface, x: int, y: int, radio: int) -> None:
    pygame.draw.circle(ventana, PALIDO, (x, y), radio)
    for i in range(5):
        angulo: float = -2.4 + i * 0.6
        punta_x: int = x + int(math.cos(angulo) * radio * 2)
        punta_y: int = y + int(math.sin(angulo) * radio * 2)
        pygame.draw.line(ventana, PALIDO, (x, y), (punta_x, punta_y), radio // 3)
        pygame.draw.circle(ventana, ROJO, (punta_x, punta_y), radio // 5)


def coraline(ventana: pygame.Surface, x: int, y: int, parpadea: bool) -> None:
    """El personaje del jugador. Si `parpadea`, se dibuja a medias (acaba de recibir un golpe)."""
    if parpadea and pygame.time.get_ticks() // 100 % 2 == 0:
        return
    pygame.draw.polygon(ventana, (60, 110, 200), [(x, y - 8), (x - 16, y + 20), (x + 16, y + 20)])
    pygame.draw.circle(ventana, (240, 210, 190), (x, y - 16), 10)
    pygame.draw.arc(ventana, (30, 40, 90), (x - 12, y - 30, 24, 22), 0, math.pi, 6)
    pygame.draw.rect(ventana, (240, 200, 40), (x - 12, y + 20, 9, 7))
    pygame.draw.rect(ventana, (240, 200, 40), (x + 3, y + 20, 9, 7))
