"""Revisa que el árbol de la historia esté completo y sin errores.

Ejecutar con: python -m herramientas.verificador
No abre ventana: imprime los errores en la consola.

Revisa:
- Que haya 300 decisiones en total (nodos con 2 o más opciones).
- Que 70 de ellas sean canónicas ("canonico": true).
- Que todo "destino" apunte a un nodo que existe.
- Que todos los nodos se puedan alcanzar desde el nodo inicial.
- Que todo nodo sin opciones tenga "final".
- Que ningún nombre de nodo se repita entre archivos.
- Que ningún nodo pase de MAXIMO_OPCIONES ni de MAXIMO_LETRAS_TEXTO
  (si no, no cabe en la pantalla).
- Que todo nodo que no sea final tenga al menos una opción sin "requiere".
- Que toda "imagen" exista en recursos/imagenes/.
- Que los minijuegos sean de un tipo que existe y que sus destinos existan.

Responsable: Persona B
"""

import os

import config
from juego import motor
from juego import partida

TOTAL_DECISIONES: int = 300
DECISIONES_CANONICAS: int = 70
TIPOS_MINIJUEGO: list = ["clic", "arrastrar", "buscar", "esquivar", "presionar"]


def destinos_de(nodo: dict) -> list:
    """Todos los nodos a los que se puede ir desde este: por sus opciones o por su minijuego."""
    destinos: list = []
    for opcion in nodo["opciones"]:
        destinos.append(opcion["destino"])
    if motor.es_minijuego(nodo):
        destinos.append(nodo["minijuego"]["exito"]["destino"])
        destinos.append(nodo["minijuego"]["fallo"]["destino"])
    return destinos


def revisar_repetidos(errores: list) -> None:
    """Busca nombres de nodo repetidos. Se leen los archivos uno por uno porque
    en cargar_historia un nodo repetido borra al otro sin avisar."""
    visto_en: dict = {}   # nombre de nodo -> archivo donde apareció primero
    for ruta in motor.archivos_de_historia(config.RUTA_HISTORIA):
        archivo: str = os.path.basename(ruta)
        datos: dict = motor.cargar_archivo(ruta)
        for nombre in datos["nodos"]:
            if nombre in visto_en:
                errores.append(nombre + ": repetido en " + visto_en[nombre] + " y " + archivo)
            else:
                visto_en[nombre] = archivo


def revisar_nodos(nodos: dict, errores: list) -> None:
    """Revisiones que se hacen nodo por nodo."""
    for nombre in nodos:
        nodo: dict = nodos[nombre]
        opciones: list = nodo["opciones"]

        if len(opciones) == 0 and not motor.es_final(nodo) and not motor.es_minijuego(nodo):
            errores.append(nombre + ": no tiene opciones y no es final (el jugador se atora)")

        if len(opciones) > config.MAXIMO_OPCIONES:
            errores.append(nombre + ": tiene " + str(len(opciones)) + " opciones (máximo "
                           + str(config.MAXIMO_OPCIONES) + ")")

        if len(nodo["texto"]) > config.MAXIMO_LETRAS_TEXTO:
            errores.append(nombre + ": el texto tiene " + str(len(nodo["texto"])) + " letras (máximo "
                           + str(config.MAXIMO_LETRAS_TEXTO) + ")")

        if len(opciones) > 0:
            tiene_opcion_libre: bool = False
            for opcion in opciones:
                if "requiere" not in opcion:
                    tiene_opcion_libre = True
            if not tiene_opcion_libre:
                errores.append(nombre + ": todas sus opciones tienen \"requiere\" (el jugador se puede atorar)")

        for destino in destinos_de(nodo):
            if destino not in nodos:
                errores.append(nombre + ": tiene un destino \"" + destino + "\" que no existe")

        if motor.es_minijuego(nodo) and nodo["minijuego"]["tipo"] not in TIPOS_MINIJUEGO:
            errores.append(nombre + ": el minijuego \"" + nodo["minijuego"]["tipo"] + "\" no existe")

        if "imagen" in nodo:
            ruta_imagen: str = os.path.join(config.RUTA_IMAGENES, nodo["imagen"])
            if not os.path.exists(ruta_imagen):
                errores.append(nombre + ": no existe la imagen " + nodo["imagen"])


def revisar_alcanzables(nodos: dict, errores: list) -> None:
    """Recorre el árbol desde el nodo inicial y avisa de los nodos a los que nadie llega."""
    if partida.NODO_INICIAL not in nodos:
        errores.append("No existe el nodo inicial " + partida.NODO_INICIAL)
        return

    alcanzados: list = [partida.NODO_INICIAL]
    pendientes: list = [partida.NODO_INICIAL]
    while len(pendientes) > 0:
        nombre: str = pendientes.pop()
        for destino in destinos_de(nodos[nombre]):
            if destino in nodos and destino not in alcanzados:
                alcanzados.append(destino)
                pendientes.append(destino)

    for nombre in nodos:
        if nombre not in alcanzados:
            errores.append(nombre + ": ninguna opción lleva a este nodo (inalcanzable)")


def contar_decisiones(nodos: dict) -> list:
    """Regresa [total de decisiones, decisiones canónicas]."""
    total: int = 0
    canonicas: int = 0
    for nombre in nodos:
        nodo: dict = nodos[nombre]
        if len(nodo["opciones"]) >= 2:
            total = total + 1
            if nodo["canonico"]:
                canonicas = canonicas + 1
    return [total, canonicas]


def main() -> None:
    nodos: dict = motor.cargar_historia(config.RUTA_HISTORIA)
    errores: list = []

    revisar_repetidos(errores)
    revisar_nodos(nodos, errores)
    revisar_alcanzables(nodos, errores)
    conteo: list = contar_decisiones(nodos)

    print("=== Verificador de la historia ===")
    print("Nodos cargados:       ", len(nodos))
    print("Decisiones:           ", conteo[0], "de", TOTAL_DECISIONES)
    print("Decisiones canónicas: ", conteo[1], "de", DECISIONES_CANONICAS)
    minijuegos: int = 0
    for nombre in nodos:
        if motor.es_minijuego(nodos[nombre]):
            minijuegos = minijuegos + 1
    print("Minijuegos:           ", minijuegos)
    print()
    if len(errores) == 0:
        print("Sin errores.")
    else:
        print("Errores encontrados:", len(errores))
        for error in errores:
            print("  -", error)


if __name__ == "__main__":
    main()
