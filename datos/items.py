# datos/items.py
#
# MinecraftFullGuideBot
# Carga AUTOMÁTICA de todos los objetos de Minecraft Java 26.1.2
# usando los datos reales de Minecraft/PrismarineJS.
#
# NO hay una lista manual de objetos.
# NO hay recetas inventadas.
#
# Incluye:
# - Todos los items registrados
# - ID interno
# - nombre traducible
# - stack máximo
# - durabilidad
# - categoría
# - recetas
# - ingredientes
# - mesa/horno/alto horno/ahumador/fogata/cortapiedras/herrería/etc.
# - tags
#
# La representación visual de recetas SIEMPRE usa una matriz 3x3.
#
# Minecraft 26.1 añadió/cambió tipos de recetas como:
# crafting_shaped
# crafting_shapeless
# crafting_transmute
# crafting_dye
# crafting_imbue
# smelting
# blasting
# smoking
# campfire_cooking
# stonecutting
# smithing_transform
# smithing_trim
#
# ------------------------------------------------------------

import json
import os
import re
import urllib.request
import urllib.error
import zipfile
import tempfile
from functools import lru_cache


# ============================================================
# CONFIGURACIÓN
# ============================================================

VERSION = "26.1.2"

BASE_DIR = os.path.dirname(os.path.abspath(__file__))

CACHE_DIR = os.path.join(BASE_DIR, "_cache")

ITEMS_FILE = os.path.join(
    CACHE_DIR,
    f"items_{VERSION}.json"
)

TAGS_DIR = os.path.join(
    CACHE_DIR,
    f"tags_{VERSION}"
)

RECIPES_DIR = os.path.join(
    CACHE_DIR,
    f"recipes_{VERSION}"
)

os.makedirs(CACHE_DIR, exist_ok=True)
os.makedirs(TAGS_DIR, exist_ok=True)
os.makedirs(RECIPES_DIR, exist_ok=True)


# ============================================================
# URLS
# ============================================================

PRISMARINE_ITEMS_URL = (
    "https://raw.githubusercontent.com/"
    "PrismarineJS/minecraft-data/master/"
    f"data/pc/{VERSION}/items.json"
)

VERSION_MANIFEST_URL = (
    "https://piston-meta.mojang.com/mc/game/version_manifest_v2.json"
)


# ============================================================
# DESCARGA
# ============================================================

def descargar(url, timeout=120):
    """
    Descarga bytes desde una URL.

    Usa Request correctamente para que Mojang/GitHub no rechacen
    la petición por falta de User-Agent.
    """

    request = urllib.request.Request(
        url,
        headers={
            "User-Agent": (
                "MinecraftFullGuideBot/1.0 "
                "(Minecraft data reader)"
            )
        }
    )

    with urllib.request.urlopen(
        request,
        timeout=timeout
    ) as respuesta:
        return respuesta.read()


def descargar_json(url):
    datos = descargar(url)
    return json.loads(datos.decode("utf-8"))


# ============================================================
# UTILIDADES
# ============================================================

def normalizar_id(valor):
    if valor is None:
        return None

    if isinstance(valor, str):
        valor = valor.strip().lower()

        if ":" not in valor:
            valor = f"minecraft:{valor}"

        return valor

    return None


def quitar_namespace(valor):
    if not valor:
        return valor

    return valor.split(":", 1)[-1]


def nombre_legible(identifier):
    """
    minecraft:diamond_pickaxe
    ->
    Diamond Pickaxe
    """

    nombre = quitar_namespace(identifier)

    nombre = nombre.replace("_", " ")

    return " ".join(
        palabra.capitalize()
        for palabra in nombre.split()
    )


def es_item_minecraft(identifier):
    return (
        isinstance(identifier, str)
        and (
            identifier.startswith("minecraft:")
            or ":" not in identifier
        )
    )


# ============================================================
# DESCARGA DE ITEMS
# ============================================================

def _descargar_items_prismarine():
    try:
        datos = descargar_json(PRISMARINE_ITEMS_URL)

        if isinstance(datos, list):
            return datos

        if isinstance(datos, dict):
            if "items" in datos:
                return datos["items"]

            return list(datos.values())

    except Exception as error:
        print(
            "[ITEMS] Error descargando Prismarine:",
            error
        )

    return []


def _cargar_items():
    """
    Devuelve el registro completo de objetos.

    Se intenta primero usar la fuente de datos completa de PrismarineJS.
    """

    datos = _descargar_items_prismarine()

    if not datos:
        raise RuntimeError(
            "No se pudo cargar el registro completo de items "
            f"de Minecraft {VERSION}."
        )

    return datos


# ============================================================
# TAGS
# ============================================================

def _descargar_tag_directo(tag_id):
    """
    Descarga un tag individual desde MC Assets/GitHub.

    Esta función se usa como respaldo cuando el tag no está
    disponible localmente.
    """

    tag_name = quitar_namespace(tag_id)

    url = (
        "https://raw.githubusercontent.com/"
        "PrismarineJS/minecraft-data/master/"
        f"data/pc/{VERSION}/tags/items/{tag_name}.json"
    )

    try:
        return descargar_json(url)
    except Exception:
        return None


def _cargar_tags():
    """
    Intenta cargar tags de Minecraft.

    Los tags son importantes porque muchas recetas utilizan:

        #minecraft:planks
        #minecraft:logs
        etc.
    """

    tags = {}

    # --------------------------------------------------------
    # Intento mediante MC Assets.
    # --------------------------------------------------------

    # No dependemos de que todos los tags estén en una lista
    # manual. Los tags necesarios pueden resolverse posteriormente.
    return tags


@lru_cache(maxsize=4096)
def _resolver_tag(tag_id):
    """
    Resuelve un tag Minecraft.

    Ejemplo:

        #minecraft:planks

    devuelve una lista de IDs reales.
    """

    if not tag_id:
        return []

    tag_id = tag_id.strip()

    if tag_id.startswith("#"):
        tag_id = tag_id[1:]

    tag_id = normalizar_id(tag_id)

    if not tag_id:
        return []

    # --------------------------------------------------------
    # Minecraft vanilla:
    # tags/item/<tag>.json
    # --------------------------------------------------------

    nombre = quitar_namespace(tag_id)

    url = (
        "https://raw.githubusercontent.com/"
        "PrismarineJS/minecraft-data/master/"
        f"data/pc/{VERSION}/tags/items/{nombre}.json"
    )

    try:
        datos = descargar_json(url)
    except Exception:
        datos = None

    if not datos:
        return []

    valores = datos.get("values", [])

    resultado = []

    for valor in valores:

        if isinstance(valor, str):

            if valor.startswith("#"):
                resultado.extend(
                    _resolver_tag(valor)
                )
            else:
                resultado.append(
                    normalizar_id(valor)
                )

    return list(dict.fromkeys(
        x for x in resultado
        if x
    ))


# ============================================================
# RECETAS
# ============================================================

def _obtener_server_jar_url():
    """
    Obtiene desde Mojang la URL oficial del server.jar
    correspondiente a 26.1.2.
    """

    manifest = descargar_json(
        VERSION_MANIFEST_URL
    )

    versiones = manifest.get(
        "versions",
        []
    )

    for version in versiones:

        if version.get("id") == VERSION:

            version_url = version.get(
                "url"
            )

            if not version_url:
                break

            version_data = descargar_json(
                version_url
            )

            downloads = version_data.get(
                "downloads",
                {}
            )

            server = downloads.get(
                "server"
            )

            if server:
                return server.get("url")

            break

    return None


def _descargar_server_jar():
    """
    Descarga el server.jar oficial de Mojang.

    Se guarda en cache para no descargarlo cada vez que el bot inicia.
    """

    jar_path = os.path.join(
        CACHE_DIR,
        f"server_{VERSION}.jar"
    )

    if os.path.exists(jar_path):
        return jar_path

    url = _obtener_server_jar_url()

    if not url:
        raise RuntimeError(
            "No se encontró el server.jar oficial "
            f"de Minecraft {VERSION}."
        )

    print(
        f"[ITEMS] Descargando server.jar oficial {VERSION}..."
    )

    datos = descargar(
        url,
        timeout=300
    )

    with open(
        jar_path,
        "wb"
    ) as archivo:
        archivo.write(datos)

    return jar_path


def _extraer_recetas_server():
    """
    Extrae las recetas reales del server.jar.

    Minecraft guarda las recetas vanilla dentro de:

        data/minecraft/recipe/
    """

    marcador = os.path.join(
        RECIPES_DIR,
        ".extraido"
    )

    if os.path.exists(marcador):
        return

    jar_path = _descargar_server_jar()

    print(
        "[ITEMS] Extrayendo recetas vanilla..."
    )

    with zipfile.ZipFile(
        jar_path,
        "r"
    ) as jar:

        prefijo = "data/minecraft/recipe/"

        encontrados = 0

        for nombre in jar.namelist():

            if not nombre.startswith(
                prefijo
            ):
                continue

            if not nombre.endswith(
                ".json"
            ):
                continue

            destino = os.path.join(
                RECIPES_DIR,
                os.path.basename(nombre)
            )

            with jar.open(nombre) as origen:
                datos = origen.read()

            with open(
                destino,
                "wb"
            ) as archivo:
                archivo.write(datos)

            encontrados += 1

    with open(
        marcador,
        "w",
        encoding="utf-8"
    ) as archivo:
        archivo.write(
            str(encontrados)
        )

    print(
        f"[ITEMS] Recetas extraídas: {encontrados}"
    )


def _leer_recetas():
    """
    Lee TODAS las recetas vanilla disponibles.
    """

    _extraer_recetas_server()

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
                datos = json.load(
                    archivo
                )

            if isinstance(datos, dict):

                datos["_file"] = nombre

                recetas.append(
                    datos
                )

        except Exception as error:

            print(
                "[RECETA] Error leyendo",
                nombre,
                error
            )

    return recetas


# ============================================================
# RESULTADO
# ============================================================

def _resultado_receta(receta):
    """
    Obtiene el resultado de una receta.

    26.1 permite:
        "minecraft:diamond"

    y también:

        {
            "id": "minecraft:diamond",
            "count": 1
        }
    """

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

        count = resultado.get(
            "count",
            1
        )

        try:
            count = int(count)
        except Exception:
            count = 1

        return {
            "id": normalizar_id(
                resultado_id
            ),
            "count": count
        }

    return None


# ============================================================
# INGREDIENTES
# ============================================================

def _ingrediente_desde_dato(dato):
    """
    Convierte cualquier formato de ingredient de Minecraft
    en una estructura que el bot pueda utilizar.
    """

    if dato is None:
        return None

    # String
    if isinstance(
        dato,
        str
    ):

        if dato.startswith("#"):

            tag = normalizar_id(
                dato[1:]
            )

            return {
                "tipo": "tag",
                "tag": tag,
                "items": _resolver_tag(tag)
            }

        return {
            "tipo": "item",
            "id": normalizar_id(
                dato
            )
        }

    # Lista de ingredientes
    if isinstance(
        dato,
        list
    ):

        opciones = []

        for elemento in dato:

            convertido = (
                _ingrediente_desde_dato(
                    elemento
                )
            )

            if convertido:
                opciones.append(
                    convertido
                )

        return {
            "tipo": "alternativas",
            "opciones": opciones
        }

    # Objeto
    if isinstance(
        dato,
        dict
    ):

        # item
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

        # tag
        tag = dato.get(
            "tag"
        )

        if tag:

            tag = normalizar_id(
                tag
            )

            return {
                "tipo": "tag",
                "tag": tag,
                "items": _resolver_tag(
                    tag
                )
            }

    return None


def _nombre_ingrediente(ingrediente):
    if not ingrediente:
        return "Vacío"

    tipo = ingrediente.get(
        "tipo"
    )

    if tipo == "item":
        return nombre_legible(
            ingrediente.get("id")
        )

    if tipo == "tag":
        return (
            "#"
            + quitar_namespace(
                ingrediente.get("tag")
            )
        )

    if tipo == "alternativas":

        opciones = ingrediente.get(
            "opciones",
            []
        )

        if not opciones:
            return "Alternativa"

        return " / ".join(
            _nombre_ingrediente(x)
            for x in opciones
        )

    return "Ingrediente"


# ============================================================
# RECETA SHAPED
# ============================================================

def _receta_crafting_shaped(receta):
    pattern = receta.get(
        "pattern",
        []
    )

    key = receta.get(
        "key",
        {}
    )

    # Siempre 3x3
    grid = [
        [None, None, None],
        [None, None, None],
        [None, None, None]
    ]

    for y in range(
        min(3, len(pattern))
    ):

        fila = pattern[y]

        if not isinstance(
            fila,
            str
        ):
            continue

        for x in range(
            min(3, len(fila))
        ):

            simbolo = fila[x]

            if simbolo == " ":
                continue

            dato = key.get(
                simbolo
            )

            ingrediente = (
                _ingrediente_desde_dato(
                    dato
                )
            )

            if ingrediente:
                grid[y][x] = ingrediente

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
# RECETA SHAPELESS
# ============================================================

def _receta_crafting_shapeless(receta):
    ingredients = receta.get(
        "ingredients",
        []
    )

    ingredientes = []

    for dato in ingredients:

        ingrediente = (
            _ingrediente_desde_dato(
                dato
            )
        )

        if ingrediente:
            ingredientes.append(
                ingrediente
            )

    # Siempre 3x3
    grid = [
        [None, None, None],
        [None, None, None],
        [None, None, None]
    ]

    posicion = 0

    for ingrediente in ingredientes:

        if posicion >= 9:
            break

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
# TRANSFORMACIONES DE CRAFTING
# ============================================================

def _receta_transmute(receta):
    """
    Minecraft 26.1:
    minecraft:crafting_transmute
    """

    target = _ingrediente_desde_dato(
        receta.get("target")
    )

    material = _ingrediente_desde_dato(
        receta.get("material")
    )

    resultado = _resultado_receta(
        receta
    )

    if not resultado:
        return None

    grid = [
        [None, None, None],
        [None, None, None],
        [None, None, None]
    ]

    # Representación visual 3x3.
    # El target ocupa el centro.
    # El material se representa alrededor.
    grid[1][1] = target

    posiciones = [
        (0, 0),
        (0, 1),
        (0, 2),
        (1, 0),
        (1, 2),
        (2, 0),
        (2, 1),
        (2, 2)
    ]

    for posicion in posiciones:

        y, x = posicion

        grid[y][x] = material

    return {
        "tipo": "crafting_transmute",
        "estacion": "mesa_de_crafteo",
        "grid": grid,
        "resultado": resultado,
        "archivo": receta.get(
            "_file"
        )
    }


# ============================================================
# DYE
# ============================================================

def _receta_dye(receta):
    target = _ingrediente_desde_dato(
        receta.get("target")
    )

    dye = _ingrediente_desde_dato(
        receta.get("dye")
    )

    resultado = _resultado_receta(
        receta
    )

    if not resultado:
        return None

    grid = [
        [None, None, None],
        [None, None, None],
        [None, None, None]
    ]

    grid[1][1] = target

    # El dye se coloca en las posiciones restantes
    # como representación visual de la receta.
    grid[0][1] = dye
    grid[1][0] = dye
    grid[1][2] = dye
    grid[2][1] = dye

    return {
        "tipo": "crafting_dye",
        "estacion": "mesa_de_crafteo",
        "grid": grid,
        "resultado": resultado,
        "archivo": receta.get(
            "_file"
        )
    }


# ============================================================
# IMBUE
# ============================================================

def _receta_imbue(receta):
    source = _ingrediente_desde_dato(
        receta.get("source")
    )

    material = _ingrediente_desde_dato(
        receta.get("material")
    )

    resultado = _resultado_receta(
        receta
    )

    if not resultado:
        return None

    grid = [
        [material, material, material],
        [material, source, material],
        [material, material, material]
    ]

    return {
        "tipo": "crafting_imbue",
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
    tipo = receta.get(
        "type",
        ""
    )

    ingredientes_posibles = [
        receta.get("ingredient"),
        receta.get("ingredients")
    ]

    ingrediente_dato = None

    for posible in ingredientes_posibles:

        if posible is not None:

            ingrediente_dato = posible
            break

    ingrediente = (
        _ingrediente_desde_dato(
            ingrediente_dato
        )
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
        "campfire_cooking": "fogata",
        "campfire": "fogata"
    }

    estacion = estaciones.get(
        tipo,
        tipo
    )

    return {
        "tipo": tipo,
        "estacion": estacion,
        "grid": [
            [None, None, None],
            [None, ingrediente, None],
            [None, None, None]
        ],
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

def _receta_stonecutting(receta):
    ingrediente_dato = (
        receta.get("ingredient")
    )

    ingrediente = (
        _ingrediente_desde_dato(
            ingrediente_dato
        )
    )

    resultado = _resultado_receta(
        receta
    )

    if not resultado:
        return None

    return {
        "tipo": "stonecutting",
        "estacion": "cortapiedras",
        "grid": [
            [None, None, None],
            [None, ingrediente, None],
            [None, None, None]
        ],
        "ingrediente": ingrediente,
        "resultado": resultado,
        "archivo": receta.get(
            "_file"
        )
    }


# ============================================================
# HERRERÍA
# ============================================================

def _receta_smithing(receta):
    template = _ingrediente_desde_dato(
        receta.get("template")
    )

    base = _ingrediente_desde_dato(
        receta.get("base")
    )

    addition = _ingrediente_desde_dato(
        receta.get("addition")
    )

    resultado = _resultado_receta(
        receta
    )

    # Smithing recipes pueden no utilizar el campo result
    # de la misma forma dependiendo del tipo.
    if not resultado:

        # Algunos smithing_transform contienen result.
        return None

    return {
        "tipo": receta.get(
            "type",
            "smithing"
        ),
        "estacion": "mesa_de_herrería",
        "grid": [
            [template, base, addition],
            [None, None, None],
            [None, None, None]
        ],
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
    tipo = receta.get(
        "type",
        ""
    )

    tipo = quitar_namespace(
        tipo
    )

    if tipo == "crafting_shaped":
        return _receta_crafting_shaped(
            receta
        )

    if tipo == "crafting_shapeless":
        return _receta_crafting_shapeless(
            receta
        )

    if tipo == "crafting_transmute":
        return _receta_transmute(
            receta
        )

    if tipo == "crafting_dye":
        return _receta_dye(
            receta
        )

    if tipo == "crafting_imbue":
        return _receta_imbue(
            receta
        )

    if tipo in {
        "smelting",
        "blasting",
        "smoking",
        "campfire_cooking",
        "campfire"
    }:
        return _receta_proceso(
            receta
        )

    if tipo == "stonecutting":
        return _receta_stonecutting(
            receta
        )

    if tipo in {
        "smithing_transform",
        "smithing_trim"
    }:
        return _receta_smithing(
            receta
        )

    return None


# ============================================================
# TODAS LAS RECETAS DE UN ITEM
# ============================================================

@lru_cache(maxsize=4096)
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

        salida_id = normalizar_id(
            salida.get("id")
        )

        if salida_id != item_id:
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
# CATEGORÍA
# ============================================================

def obtener_categoria(item):
    """
    Intenta determinar la categoría del item
    usando la información disponible.
    """

    if not isinstance(
        item,
        dict
    ):
        return "misc"

    categoria = (
        item.get("category")
        or item.get("creative_category")
        or item.get("group")
    )

    if categoria:
        return str(
            categoria
        )

    return "misc"


# ============================================================
# DURABILIDAD
# ============================================================

def obtener_durabilidad(item):
    if not isinstance(
        item,
        dict
    ):
        return None

    for clave in (
        "maxDurability",
        "max_durability",
        "durability"
    ):

        valor = item.get(
            clave
        )

        if valor:

            try:
                return int(
                    valor
                )
            except Exception:
                pass

    return None


# ============================================================
# PREPARAR ITEM
# ============================================================

def preparar_item(item):
    """
    Convierte un registro bruto en el formato usado por el bot.
    """

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

    item["translatedName"] = (
        item.get("displayName")
        or item.get("translatedName")
        or nombre_legible(
            identifier
        )
    )

    item["displayName"] = (
        item["translatedName"]
    )

    item["category"] = (
        obtener_categoria(item)
    )

    item["maxStackSize"] = int(
        item.get(
            "stackSize",
            item.get(
                "maxStackSize",
                64
            )
        )
        or 64
    )

    durabilidad = obtener_durabilidad(
        item
    )

    item["durability"] = (
        durabilidad
    )

    item["maxDurability"] = (
        durabilidad
    )

    recetas = obtener_recetas_item(
        identifier
    )

    item["recipes"] = recetas

    # Compatibilidad con el código actual
    mesas = []

    for receta in recetas:

        estacion = receta.get(
            "estacion"
        )

        if estacion and estacion not in mesas:
            mesas.append(
                estacion
            )

    item["mesas_fabricacion"] = mesas

    item["recipe_count"] = len(
        recetas
    )

    return item


# ============================================================
# ÍNDICE COMPLETO
# ============================================================

_ITEMS_RAW = None
_ITEMS_INDEX = None


def _construir_indice():
    global _ITEMS_RAW
    global _ITEMS_INDEX

    if _ITEMS_INDEX is not None:
        return

    print(
        "[ITEMS] Cargando TODOS los items "
        f"de Minecraft {VERSION}..."
    )

    _ITEMS_RAW = _cargar_items()

    indice = {}

    for item in _ITEMS_RAW:

        preparado = preparar_item(
            item
        )

        if not preparado:
            continue

        identifier = preparado.get(
            "identifier"
        )

        if not identifier:
            continue

        indice[identifier] = preparado

    _ITEMS_INDEX = indice

    print(
        "[ITEMS] Items cargados:",
        len(_ITEMS_INDEX)
    )


# ============================================================
# BÚSQUEDA
# ============================================================

def buscar_item(texto):
    """
    Busca por:

        minecraft:diamond
        diamond
        pico_de_diamante
        diamond_pickaxe
        etc.

    El ID interno siempre permanece en inglés.
    """

    _construir_indice()

    if not texto:
        return None

    texto = texto.strip().lower()

    texto_id = normalizar_id(
        texto
    )

    # Coincidencia exacta por ID
    if texto_id in _ITEMS_INDEX:
        return _ITEMS_INDEX[
            texto_id
        ]

    # Coincidencia por nombre técnico
    for identifier, item in _ITEMS_INDEX.items():

        corto = quitar_namespace(
            identifier
        )

        if texto == corto:
            return item

    # Búsqueda parcial
    for identifier, item in _ITEMS_INDEX.items():

        corto = quitar_namespace(
            identifier
        )

        if texto in corto:
            return item

    # Nombre visible
    texto_normalizado = (
        re.sub(
            r"[^a-z0-9áéíóúüñ ]+",
            " ",
            texto
        )
    )

    for item in _ITEMS_INDEX.values():

        nombre = str(
            item.get(
                "displayName",
                ""
            )
        ).lower()

        nombre_normalizado = (
            re.sub(
                r"[^a-z0-9áéíóúüñ ]+",
                " ",
                nombre
            )
        )

        if (
            texto_normalizado
            and texto_normalizado
            in nombre_normalizado
        ):
            return item

    return None


# ============================================================
# ITEM REPRESENTATIVO
# ============================================================

def obtener_item_representativo(texto):
    return buscar_item(
        texto
    )


# ============================================================
# LISTA COMPLETA
# ============================================================

def obtener_todos_items():
    """
    Devuelve absolutamente todos los items cargados.
    """

    _construir_indice()

    return list(
        _ITEMS_INDEX.values()
    )


# ============================================================
# INFORMACIÓN DE DEPURACIÓN
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
# COMPATIBILIDAD
# ============================================================

def obtener_item(item_id):
    return buscar_item(
        item_id
    )


def cargar_items():
    _construir_indice()

    return _ITEMS_INDEX


# ============================================================
# EXPORTACIÓN
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
