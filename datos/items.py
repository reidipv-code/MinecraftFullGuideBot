# datos/items.py

import json
import os
import re
import urllib.request
import zipfile
from functools import lru_cache


# ============================================================
# CONFIGURACIÓN
# ============================================================

VERSION = "26.1.2"

BASE_DIR = os.path.dirname(os.path.abspath(__file__))

CACHE_DIR = os.path.join(
    BASE_DIR,
    "_cache"
)

RECIPES_DIR = os.path.join(
    CACHE_DIR,
    f"recipes_{VERSION}"
)

os.makedirs(
    CACHE_DIR,
    exist_ok=True
)

os.makedirs(
    RECIPES_DIR,
    exist_ok=True
)


PRISMARINE_ITEMS_URL = (
    "https://raw.githubusercontent.com/"
    "PrismarineJS/minecraft-data/master/"
    f"data/pc/{VERSION}/items.json"
)

MOJANG_VERSION_MANIFEST = (
    "https://piston-meta.mojang.com/"
    "mc/game/version_manifest_v2.json"
)


# ============================================================
# DESCARGAS
# ============================================================

def descargar(url, timeout=120):
    request = urllib.request.Request(
        url,
        headers={
            "User-Agent": "MinecraftFullGuideBot/1.0"
        }
    )

    with urllib.request.urlopen(
        request,
        timeout=timeout
    ) as response:
        return response.read()


def descargar_json(url, timeout=120):
    datos = descargar(
        url,
        timeout
    )

    return json.loads(
        datos.decode("utf-8")
    )


# ============================================================
# UTILIDADES
# ============================================================

def normalizar_id(valor):
    if valor is None:
        return None

    if not isinstance(
        valor,
        str
    ):
        return None

    valor = valor.strip().lower()

    if not valor:
        return None

    if ":" not in valor:
        valor = "minecraft:" + valor

    return valor


def quitar_namespace(valor):
    if not valor:
        return ""

    return str(valor).split(
        ":",
        1
    )[-1]


def nombre_legible(identifier):
    nombre = quitar_namespace(
        identifier
    )

    nombre = nombre.replace(
        "_",
        " "
    )

    return " ".join(
        palabra.capitalize()
        for palabra in nombre.split()
    )


# ============================================================
# ITEMS
# ============================================================

def _cargar_items_prismarine():
    try:
        datos = descargar_json(
            PRISMARINE_ITEMS_URL,
            timeout=180
        )

        if isinstance(
            datos,
            list
        ):
            return datos

        if isinstance(
            datos,
            dict
        ):
            if isinstance(
                datos.get("items"),
                list
            ):
                return datos["items"]

            return list(
                datos.values()
            )

    except Exception as error:
        print(
            "[ITEMS] Error cargando items:",
            error
        )

    return []


# ============================================================
# MOJANG SERVER JAR
# ============================================================

def _obtener_url_server():
    manifest = descargar_json(
        MOJANG_VERSION_MANIFEST,
        timeout=120
    )

    for version in manifest.get(
        "versions",
        []
    ):

        if version.get("id") != VERSION:
            continue

        version_url = version.get(
            "url"
        )

        if not version_url:
            break

        datos = descargar_json(
            version_url,
            timeout=120
        )

        server = (
            datos
            .get("downloads", {})
            .get("server")
        )

        if server:
            return server.get(
                "url"
            )

    return None


def _obtener_server_jar():
    ruta = os.path.join(
        CACHE_DIR,
        f"server_{VERSION}.jar"
    )

    if os.path.isfile(ruta):
        return ruta

    print(
        "[ITEMS] Descargando server.jar",
        VERSION
    )

    url = _obtener_url_server()

    if not url:
        raise RuntimeError(
            "No se encontró el server.jar oficial."
        )

    datos = descargar(
        url,
        timeout=300
    )

    with open(
        ruta,
        "wb"
    ) as archivo:
        archivo.write(datos)

    return ruta


# ============================================================
# RECETAS
# ============================================================

def _extraer_recetas():
    marca = os.path.join(
        RECIPES_DIR,
        ".ok"
    )

    if os.path.exists(marca):
        return

    jar = _obtener_server_jar()

    print(
        "[ITEMS] Extrayendo recetas vanilla..."
    )

    prefijo = "data/minecraft/recipe/"

    cantidad = 0

    with zipfile.ZipFile(
        jar,
        "r"
    ) as archivo_zip:

        for nombre in archivo_zip.namelist():

            if not nombre.startswith(
                prefijo
            ):
                continue

            if not nombre.endswith(
                ".json"
            ):
                continue

            datos = archivo_zip.read(
                nombre
            )

            destino = os.path.join(
                RECIPES_DIR,
                os.path.basename(nombre)
            )

            with open(
                destino,
                "wb"
            ) as archivo:
                archivo.write(
                    datos
                )

            cantidad += 1

    with open(
        marca,
        "w",
        encoding="utf-8"
    ) as archivo:
        archivo.write(
            str(cantidad)
        )

    print(
        "[ITEMS] Recetas extraídas:",
        cantidad
    )


def _leer_recetas():
    _extraer_recetas()

    recetas = []

    if not os.path.isdir(
        RECIPES_DIR
    ):
        return recetas

    for nombre in os.listdir(
        RECIPES_DIR
    ):

        if not nombre.endswith(
            ".json"
        ):
            continue

        ruta = os.path.join(
            RECIPES_DIR,
            nombre
        )

        try:
            with open(
                ruta,
                "r",
                encoding="utf-8"
            ) as archivo:

                receta = json.load(
                    archivo
                )

            if isinstance(
                receta,
                dict
            ):

                receta["_file"] = nombre

                recetas.append(
                    receta
                )

        except Exception as error:

            print(
                "[RECETA] Error:",
                nombre,
                error
            )

    return recetas


# ============================================================
# RESULTADO DE RECETA
# ============================================================

def _resultado_receta(receta):
    resultado = receta.get(
        "result"
    )

    if isinstance(
        resultado,
        str
    ):

        return {
            "id": normalizar_id(
                resultado
            ),
            "count": 1
        }

    if isinstance(
        resultado,
        dict
    ):

        resultado_id = (
            resultado.get("id")
            or resultado.get("item")
        )

        if not resultado_id:
            return None

        try:
            cantidad = int(
                resultado.get(
                    "count",
                    1
                )
            )
        except Exception:
            cantidad = 1

        return {
            "id": normalizar_id(
                resultado_id
            ),
            "count": cantidad
        }

    return None


# ============================================================
# INGREDIENTES
# ============================================================

def _ingrediente(dato):
    if dato is None:
        return None

    if isinstance(
        dato,
        str
    ):

        if dato.startswith("#"):

            return {
                "tipo": "tag",
                "tag": normalizar_id(
                    dato[1:]
                )
            }

        return {
            "tipo": "item",
            "id": normalizar_id(
                dato
            )
        }

    if isinstance(
        dato,
        list
    ):

        opciones = []

        for elemento in dato:

            convertido = _ingrediente(
                elemento
            )

            if convertido:
                opciones.append(
                    convertido
                )

        return {
            "tipo": "alternativas",
            "opciones": opciones
        }

    if isinstance(
        dato,
        dict
    ):

        item_id = (
            dato.get("item")
            or dato.get("id")
        )

        if item_id:

            return {
                "tipo": "item",
                "id": normalizar_id(
                    item_id
                )
            }

        tag = dato.get(
            "tag"
        )

        if tag:

            return {
                "tipo": "tag",
                "tag": normalizar_id(
                    tag
                )
            }

    return None


# ============================================================
# GRID 3x3
# ============================================================

def _grid_vacia():
    return [
        [None, None, None],
        [None, None, None],
        [None, None, None]
    ]


# ============================================================
# CRAFTING SHAPED
# ============================================================

def _crafting_shaped(receta):
    pattern = receta.get(
        "pattern",
        []
    )

    key = receta.get(
        "key",
        {}
    )

    grid = _grid_vacia()

    for y, fila in enumerate(
        pattern[:3]
    ):

        if not isinstance(
            fila,
            str
        ):
            continue

        for x, simbolo in enumerate(
            fila[:3]
        ):

            if simbolo == " ":
                continue

            dato = key.get(
                simbolo
            )

            grid[y][x] = _ingrediente(
                dato
            )

    resultado = _resultado_receta(
        receta
    )

    if not resultado:
        return None

    return {
        "tipo": "crafting_shaped",
        "estacion": "mesa_de_crafteo",
        "grid": grid,
        "resultado": resultado,
        "archivo": receta.get(
            "_file"
        )
    }


# ============================================================
# CRAFTING SHAPELESS
# ============================================================

def _crafting_shapeless(receta):
    ingredientes = receta.get(
        "ingredients",
        []
    )

    grid = _grid_vacia()

    posicion = 0

    for dato in ingredientes:

        if posicion >= 9:
            break

        ingrediente = _ingrediente(
            dato
        )

        if not ingrediente:
            continue

        y = posicion // 3
        x = posicion % 3

        grid[y][x] = ingrediente

        posicion += 1

    resultado = _resultado_receta(
        receta
    )

    if not resultado:
        return None

    return {
        "tipo": "crafting_shapeless",
        "estacion": "mesa_de_crafteo",
        "grid": grid,
        "resultado": resultado,
        "archivo": receta.get(
            "_file"
        )
    }


# ============================================================
# PROCESAMIENTO
# ============================================================

def _receta_proceso(receta):
    tipo = quitar_namespace(
        receta.get(
            "type",
            ""
        )
    )

    dato_ingrediente = (
        receta.get("ingredient")
    )

    if dato_ingrediente is None:
        dato_ingrediente = (
            receta.get("ingredients")
        )

    ingrediente = _ingrediente(
        dato_ingrediente
    )

    resultado = _resultado_receta(
        receta
    )

    if not resultado:
        return None

    estaciones = {
        "smelting": "horno",
        "blasting": "alto_horno",
        "smoking": "ahumador",
        "campfire_cooking": "fogata"
    }

    estacion = estaciones.get(
        tipo,
        tipo
    )

    grid = _grid_vacia()

    grid[1][1] = ingrediente

    return {
        "tipo": tipo,
        "estacion": estacion,
        "grid": grid,
        "ingrediente": ingrediente,
        "resultado": resultado,
        "archivo": receta.get(
            "_file"
        ),
        "tiempo": receta.get(
            "cookingtime"
        ),
        "experiencia": receta.get(
            "experience"
        )
    }


# ============================================================
# CORTAPIEDRAS
# ============================================================

def _stonecutting(receta):
    ingrediente = _ingrediente(
        receta.get(
            "ingredient"
        )
    )

    resultado = _resultado_receta(
        receta
    )

    if not resultado:
        return None

    grid = _grid_vacia()

    grid[1][1] = ingrediente

    return {
        "tipo": "stonecutting",
        "estacion": "cortapiedras",
        "grid": grid,
        "ingrediente": ingrediente,
        "resultado": resultado,
        "archivo": receta.get(
            "_file"
        )
    }


# ============================================================
# HERRERÍA
# ============================================================

def _smithing(receta):
    template = _ingrediente(
        receta.get(
            "template"
        )
    )

    base = _ingrediente(
        receta.get(
            "base"
        )
    )

    addition = _ingrediente(
        receta.get(
            "addition"
        )
    )

    resultado = _resultado_receta(
        receta
    )

    if not resultado:
        return None

    grid = _grid_vacia()

    grid[0][0] = template
    grid[0][1] = base
    grid[0][2] = addition

    return {
        "tipo": quitar_namespace(
            receta.get(
                "type",
                "smithing"
            )
        ),
        "estacion": "mesa_de_herreria",
        "grid": grid,
        "ingredientes": [
            template,
            base,
            addition
        ],
        "resultado": resultado,
        "archivo": receta.get(
            "_file"
        )
    }


# ============================================================
# CONVERSIÓN GENERAL
# ============================================================

def convertir_receta(receta):
    tipo = quitar_namespace(
        receta.get(
            "type",
            ""
        )
    )

    if tipo == "crafting_shaped":
        return _crafting_shaped(
            receta
        )

    if tipo == "crafting_shapeless":
        return _crafting_shapeless(
            receta
        )

    if tipo in {
        "smelting",
        "blasting",
        "smoking",
        "campfire_cooking"
    }:
        return _receta_proceso(
            receta
        )

    if tipo == "stonecutting":
        return _stonecutting(
            receta
        )

    if tipo in {
        "smithing_transform",
        "smithing_trim"
    }:
        return _smithing(
            receta
        )

    return None


# ============================================================
# RECETAS DE UN ITEM
# ============================================================

@lru_cache(
    maxsize=4096
)
def obtener_recetas_item(item_id):
    item_id = normalizar_id(
        item_id
    )

    if not item_id:
        return []

    recetas = _leer_recetas()

    resultado = []

    for receta in recetas:

        salida = _resultado_receta(
            receta
        )

        if not salida:
            continue

        if normalizar_id(
            salida.get("id")
        ) != item_id:
            continue

        convertida = convertir_receta(
            receta
        )

        if convertida:
            resultado.append(
                convertida
            )

    return resultado


# ============================================================
# INFORMACIÓN DEL ITEM
# ============================================================

def _preparar_item(item):
    if not isinstance(
        item,
        dict
    ):
        return None

    item = dict(
        item
    )

    identifier = (
        item.get("name")
        or item.get("id")
        or item.get("identifier")
    )

    if not identifier:
        return None

    identifier = normalizar_id(
        identifier
    )

    item["identifier"] = identifier
    item["id"] = identifier

    item["displayName"] = (
        item.get("displayName")
        or nombre_legible(
            identifier
        )
    )

    item["translatedName"] = (
        item["displayName"]
    )

    item["category"] = (
        item.get("category")
        or item.get(
            "creative_category"
        )
        or "misc"
    )

    stack = (
        item.get("stackSize")
        or item.get("maxStackSize")
        or 64
    )

    try:
        stack = int(
            stack
        )
    except Exception:
        stack = 64

    item["stackSize"] = stack
    item["maxStackSize"] = stack

    durability = (
        item.get("maxDurability")
        or item.get("durability")
    )

    try:
        if durability is not None:
            durability = int(
                durability
            )
    except Exception:
        durability = None

    item["durability"] = durability
    item["maxDurability"] = durability

    recetas = obtener_recetas_item(
        identifier
    )

    item["recipes"] = recetas

    estaciones = []

    for receta in recetas:

        estacion = receta.get(
            "estacion"
        )

        if (
            estacion
            and estacion not in estaciones
        ):
            estaciones.append(
                estacion
            )

    item["mesas_fabricacion"] = (
        estaciones
    )

    item["recipe_count"] = len(
        recetas
    )

    return item


# ============================================================
# ÍNDICE
# ============================================================

_ITEMS_INDEX = None


def _construir_indice():
    global _ITEMS_INDEX

    if _ITEMS_INDEX is not None:
        return

    print(
        "[ITEMS] Cargando TODOS los objetos "
        f"de Minecraft {VERSION}..."
    )

    items = _cargar_items_prismarine()

    if not items:
        raise RuntimeError(
            "No se pudieron cargar los datos "
            "de Minecraft."
        )

    indice = {}

    for item in items:

        preparado = _preparar_item(
            item
        )

        if not preparado:
            continue

        identifier = preparado.get(
            "identifier"
        )

        if identifier:
            indice[
                identifier
            ] = preparado

    if not indice:
        raise RuntimeError(
            "El registro de Minecraft "
            "no contiene objetos."
        )

    _ITEMS_INDEX = indice

    print(
        "[ITEMS] Objetos cargados:",
        len(_ITEMS_INDEX)
    )


# ============================================================
# BÚSQUEDA
# ============================================================

def buscar_item(
    texto,
    idioma=None
):
    """
    Busca un objeto.

    El segundo parámetro `idioma` existe para mantener
    compatibilidad con comandos/items.py.

    Ejemplo:

        buscar_item("diamond")
        buscar_item("diamond", "es")
    """

    _construir_indice()

    if not texto:
        return None

    texto = str(
        texto
    ).strip().lower()

    # --------------------------------------------------------
    # ID exacto
    # --------------------------------------------------------

    item_id = normalizar_id(
        texto
    )

    if item_id in _ITEMS_INDEX:
        return _ITEMS_INDEX[
            item_id
        ]

    # --------------------------------------------------------
    # ID corto exacto
    # --------------------------------------------------------

    for identifier, item in _ITEMS_INDEX.items():

        corto = quitar_namespace(
            identifier
        )

        if texto == corto:
            return item

    # --------------------------------------------------------
    # ID parcial
    # --------------------------------------------------------

    for identifier, item in _ITEMS_INDEX.items():

        corto = quitar_namespace(
            identifier
        )

        if texto in corto:
            return item

    # --------------------------------------------------------
    # Nombre visible
    # --------------------------------------------------------

    texto_normalizado = re.sub(
        r"[^a-z0-9áéíóúüñ ]+",
        " ",
        texto
    ).strip()

    if texto_normalizado:

        for item in _ITEMS_INDEX.values():

            nombre = str(
                item.get(
                    "displayName",
                    ""
                )
            ).lower()

            nombre_normalizado = re.sub(
                r"[^a-z0-9áéíóúüñ ]+",
                " ",
                nombre
            ).strip()

            if (
                texto_normalizado
                == nombre_normalizado
            ):
                return item

    # --------------------------------------------------------
    # Nombre visible parcial
    # --------------------------------------------------------

    if texto_normalizado:

        for item in _ITEMS_INDEX.values():

            nombre = str(
                item.get(
                    "displayName",
                    ""
                )
            ).lower()

            nombre_normalizado = re.sub(
                r"[^a-z0-9áéíóúüñ ]+",
                " ",
                nombre
            ).strip()

            if (
                texto_normalizado
                and texto_normalizado
                in nombre_normalizado
            ):
                return item

    return None


# ============================================================
# ALIAS
# ============================================================

def obtener_item(
    texto,
    idioma=None
):
    return buscar_item(
        texto,
        idioma
    )


def obtener_item_representativo(
    texto,
    idioma=None
):
    return buscar_item(
        texto,
        idioma
    )


# ============================================================
# TODOS LOS ITEMS
# ============================================================

def obtener_todos_items():
    _construir_indice()

    return list(
        _ITEMS_INDEX.values()
    )


def cargar_items():
    _construir_indice()

    return _ITEMS_INDEX


# ============================================================
# ESTADÍSTICAS
# ============================================================

def estadisticas_items():
    _construir_indice()

    total = len(
        _ITEMS_INDEX
    )

    con_receta = 0
    total_recetas = 0

    for item in _ITEMS_INDEX.values():

        recetas = item.get(
            "recipes",
            []
        )

        if recetas:
            con_receta += 1
            total_recetas += len(
                recetas
            )

    return {
        "version": VERSION,
        "items": total,
        "items_con_receta": con_receta,
        "recetas": total_recetas
    }


# ============================================================
# EXPORTACIONES
# ============================================================

__all__ = [
    "VERSION",
    "buscar_item",
    "obtener_item",
    "obtener_item_representativo",
    "obtener_todos_items",
    "obtener_recetas_item",
    "estadisticas_items",
    "cargar_items",
]
