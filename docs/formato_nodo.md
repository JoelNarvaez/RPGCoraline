# Formato de un nodo

Cada capítulo vive en `historia/capXX.json`. Los finales viven en `historia/finales.json`.

```json
{
  "capitulo": 1,
  "titulo": "",
  "responsable": "Persona A",
  "nodos": {
    "cap01_n01": { ... },
    "cap01_r01": { ... }
  }
}
```

## Nombres de nodos

| Tipo | Formato | Ejemplo |
|---|---|---|
| Ruta canónica | `capXX_nYY` | `cap03_n05` |
| Rama | `capXX_rYY` | `cap03_r02` |
| Final | `final_<nombre>` | `final_ojos_de_boton` |
| Minijuego | `capXX_mYY` | `cap03_m01` |

Una rama puede regresar a la ruta canónica apuntando su `destino` a un nodo `capXX_nYY`, incluso de otro capítulo.

## Campos de un nodo

| Campo | Obligatorio | Descripción |
|---|---|---|
| `texto` | Sí | Lo que se le muestra al jugador |
| `canonico` | Sí | `true` si el nodo es parte de la historia del libro |
| `opciones` | Sí | Lista de opciones. Vacía solo si es un final |
| `final` | Solo en finales | `"canonico"`, `"bueno"` o `"malo"` |
| `imagen` | No | Imagen de fondo, de `recursos/imagenes/` (ej. `"sotano.png"`). Si no tiene, se usa el color de fondo |

### Límites para que quepa en pantalla

- Máximo **4 opciones** por nodo (`MAXIMO_OPCIONES` en `config.py`).
- Máximo **600 letras** de `texto` por nodo (`MAXIMO_LETRAS_TEXTO`). Si una escena es más larga, se parte en dos nodos con una sola opción "Continuar".
- Todo nodo que no sea final debe tener **al menos una opción sin `requiere`**, para que el jugador nunca se quede atorado.

El verificador revisa los tres.

## Campos de una opción

| Campo | Obligatorio | Descripción |
|---|---|---|
| `texto` | Sí | Texto de la opción |
| `destino` | Sí | Nombre del nodo al que lleva |
| `canonica` | Sí | `true` si es la elección que sigue el libro |
| `requiere` | No | Condiciones para que la opción aparezca |
| `efectos` | No | Cambios al elegirla |

### `requiere`

```json
"requiere": {
  "objetos": ["piedra_con_agujero"],
  "estadisticas": { "valentia": 3 }
}
```

La opción solo aparece si Coraline tiene **todos** los objetos y **cada** estadística es mayor o igual al número indicado.

### `efectos`

```json
"efectos": {
  "agregar_objetos": ["llave_negra"],
  "quitar_objetos": ["vela"],
  "estadisticas": { "valentia": 1, "cordura": -2 }
}
```

## Nodos con minijuego

Un nodo puede tener `"minijuego"` en lugar de opciones (`"opciones": []`). El jugador lee el texto, presiona "Aceptar el reto" y juega. El resultado lo manda a `exito` o a `fallo`, que tienen la misma forma que una opción (`destino` y `efectos`). Para que pueda volver a intentarlo, `fallo` puede apuntar al mismo nodo.

```json
"cap03_m01": {
  "texto": "La llave negra está helada...",
  "canonico": true,
  "imagen": "salon.jpg",
  "opciones": [],
  "minijuego": {
    "tipo": "arrastrar",
    "instruccion": "Arrastra la llave negra hasta la cerradura y suéltala ahí.",
    "tiempo": 15,
    "objeto": "llave",
    "zona": "cerradura",
    "exito": { "destino": "cap03_n03" },
    "fallo": { "destino": "cap03_m01", "efectos": { "estadisticas": { "cordura": -1 } } }
  }
}
```

| `tipo` | Campos propios |
|---|---|
| `clic` | `figura` (`"puerta"` u `"hoja"`), `cantidad` |
| `arrastrar` | `objeto` (`"llave"`, `"mantel"`, `"gato"`), `zona` (`"cerradura"`, `"pozo"`, `"otra_madre"`), `zona_se_mueve` (opcional) |
| `buscar` | `senuelos` (canicas falsas), `se_mueve` (la lleva una rata) |
| `esquivar` | `enemigo` (`"sombra"`, `"mano"`, `"otro_padre"`), `cantidad`, `persiguen` |
| `presionar` | `empuje` (qué tan fuerte empuja la otra madre) |

Todos llevan `tipo`, `instruccion`, `tiempo`, `exito` y `fallo`. Los nodos de minijuego se nombran `capXX_mYY` y no cuentan como decisión.

## Qué cuenta como decisión

Una **decisión** es un nodo con 2 o más opciones. Una **decisión canónica** es una decisión cuyo nodo tiene `"canonico": true`.

Meta: **300 decisiones**, de las cuales **70 son canónicas**. El verificador (`python -m herramientas.verificador`) las cuenta.
