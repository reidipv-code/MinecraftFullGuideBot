# datos/items.py

import json
import os
import re
import urllib.request
import zipfile
from functools import lru_cache


# ============================================================
# VERSIONES
# ============================================================

# Minecraft oficial que utiliza el bot
VERSION = "26.1.2"

# PrismarineJS publica los datos de esta versión bajo 26.1
DATA_VERSION = "26.1"


# ============================================================
# RUTAS
# ============================================================

BASE_DIR = os.path.dirname(
    os.path.abspath(__file__)
)

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


# ============================================================
# URLS
# ============================================================

PRISMARINE_ITEMS_URL = (
    "https://raw.githubusercontent.com/"
    "PrismarineJS/minecraft-data/master/"
    f"data/pc/{DATA_VERSION}/items.json"
)

MOJANG_VERSION_MANIFEST = (
    "https://piston-meta.mojang.com/"
    "mc/game/version_manifest_v2.json"
)


# ============================================================
# DESCARGAS
# ============================================================

def descargar(url, timeout=180):

    request = urllib.request.Request(
        url,
        headers={
            "User-Agent": (
                "Mozilla/5.0 "
                "MinecraftFullGuideBot"
            )
        }
    )

    with urllib.request.urlopen(
        request,
        timeout=timeout
    ) as response:

        return response.read()


def descargar_json(
    url,
    timeout=180
):

    datos = descargar(
        url,
        timeout
    )

    return json.loads(
        datos.decode(
            "utf-8"
        )
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
        valor = (
            "minecraft:"
            + valor
        )

    return valor


def quitar_namespace(valor):

    if not valor:
        return ""

    return str(valor).split(
        ":",
        1
    )[-1]


def nombre_legible(
    identifier
):

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
# ITEMS COMPLETOS
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
            "[ITEMS] Error cargando "
            "Prismarine:",
            error
        )

    return []


# ============================================================
# SERVER JAR OFICIAL
# ============================================================

def _obtener_url_server():

    manifest = descargar_json(
        MOJANG_VERSION_MANIFEST,
        timeout=180
    )

    for version in manifest.get(
        "versions",
        []
    ):

        if version.get(
            "id"
        ) != VERSION:
            continue

        version_url = version.get(
            "url"
        )

        if not version_url:
            break

        version_data = (
            descargar_json(
                version_url,
                timeout=180
            )
        )

        server = (
            version_data
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

    if os.path.isfile(
        ruta
    ):
        return ruta

    print(
        "[ITEMS] Descargando "
        f"server.jar {VERSION}..."
    )

    url = _obtener_url_server()

    if not url:

        raise RuntimeError(
            "No se encontró el "
            f"server.jar de {VERSION}."
        )

    datos = descargar(
        url,
        timeout=300
    )

    with open(
        ruta,
        "wb"
    ) as archivo:

        archivo.write(
            datos
        )

    return ruta


# ============================================================
# RECETAS VANILLA
# ============================================================

def _extraer_recetas():

    marca = os.path.join(
        RECIPES_DIR,
        ".ok"
    )

    if os.path.exists(
        marca
    ):
        return

    jar = _obtener_server_jar()

    print(
        "[ITEMS] Extrayendo "
        "recetas vanilla..."
    )

    prefijo = (
        "data/minecraft/recipe/"
    )

    cantidad = 0

    with zipfile.ZipFile(
        jar,
        "r"
    ) as archivo_zip:

        for nombre in (
            archivo_zip.namelist()
        ):

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

            nombre_archivo = os.path.basename(
                nombre
            )

            destino = os.path.join(
                RECIPES_DIR,
                nombre_archivo
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
                "[RECETA] Error leyendo",
                nombre,
                error
            )

    return recetas


# ============================================================
# RESULTADO
# ============================================================

def _resultado_receta(
    receta
):

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

def _ingrediente_id(
    dato
):

    if dato is None:
        return None

    if isinstance(
        dato,
        str
    ):

        if dato.startswith(
            "#"
        ):

            return (
                "#"
                + quitar_namespace(
                    dato[1:]
                )
            )

        return quitar_namespace(
            normalizar_id(
                dato
            )
        )

    if isinstance(
        dato,
        dict
    ):

        item_id = (
            dato.get("item")
            or dato.get("id")
        )

        if item_id:

            return quitar_namespace(
                normalizar_id(
                    item_id
                )
            )

        tag = dato.get(
            "tag"
        )

        if tag:

            return (
                "#"
                + quitar_namespace(
                    normalizar_id(
                        tag
                    )
                )
            )

    if isinstance(
        dato,
        list
    ):

        opciones = []

        for elemento in dato:

            valor = _ingrediente_id(
                elemento
            )

            if valor:
                opciones.append(
                    valor
                )

        return opciones

    return None


# ============================================================
# GRID 3x3
# ============================================================

def _grid_vacia():

    return [
        [None, None, None],
        [None, None, None],
        [None, None, None],
    ]


# ============================================================
# CRAFTING SHAPED
# ============================================================

def _crafting_shaped(
    receta
):

    pattern = receta.get(
        "pattern",
        []
    )

    key = receta.get(
        "key",
        {}
    )

    matriz = _grid_vacia()

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

            matriz[y][x] = (
                _ingrediente_id(
                    dato
                )
            )

    resultado = (
        _resultado_receta(
            receta
        )
    )

    if not resultado:
        return None

    return {
        "tipo": "crafting",
        "forma": "shaped",
        "matriz": matriz,
        "ingredientes": [
            ingrediente
            for fila in matriz
            for ingrediente in fila
            if ingrediente
        ],
        "cantidad": resultado.get(
            "count",
            1
        ),
        "resultado": (
            resultado.get(
                "id"
            )
        ),
        "estacion": "mesa_de_crafteo",
        "archivo": receta.get(
            "_file"
        ),
    }


# ============================================================
# CRAFTING SHAPELESS
# ============================================================

def _crafting_shapeless(
    receta
):

    ingredientes_raw = receta.get(
        "ingredients",
        []
    )

    ingredientes = []

    for dato in ingredientes_raw:

        ingrediente = (
            _ingrediente_id(
                dato
            )
        )

        if ingrediente:

            ingredientes.append(
                ingrediente
            )

    matriz = _grid_vacia()

    for posicion, ingrediente in enumerate(
        ingredientes[:9]
    ):

        y = posicion // 3
        x = posicion % 3

        matriz[y][x] = ingrediente

    resultado = (
        _resultado_receta(
            receta
        )
    )

    if not resultado:
        return None

    return {
        "tipo": "crafting",
        "forma": "shapeless",
        "matriz": matriz,
        "ingredientes": ingredientes,
        "cantidad": resultado.get(
            "count",
            1
        ),
        "resultado": (
            resultado.get(
                "id"
            )
        ),
        "estacion": "mesa_de_crafteo",
        "archivo": receta.get(
            "_file"
        ),
    }


# ============================================================
# PROCESOS
# ============================================================

def _receta_proceso(
    receta
):

    tipo = quitar_namespace(
        receta.get(
            "type",
            ""
        )
    )

    dato = receta.get(
        "ingredient"
    )

    if dato is None:

        datos = receta.get(
            "ingredients"
        )

        if isinstance(
            datos,
            list
        ) and datos:

            dato = datos[0]

    ingrediente = (
        _ingrediente_id(
            dato
        )
    )

    resultado = (
        _resultado_receta(
            receta
        )
    )

    if not resultado:
        return None

    procesos = {
        "smelting": "horno",
        "blasting": "alto_horno",
        "smoking": "ahumador",
        "campfire_cooking": "fogata",
    }

    proceso = procesos.get(
        tipo,
        tipo
    )

    return {
        "tipo": "proceso",
        "proceso": proceso,
        "ingrediente": ingrediente,
        "cantidad": resultado.get(
            "count",
            1
        ),
        "resultado": (
            resultado.get(
                "id"
            )
        ),
        "estacion": proceso,
        "matriz": [
            [None, None, None],
            [None, ingrediente, None],
            [None, None, None],
        ],
        "archivo": receta.get(
            "_file"
        ),
    }


# ============================================================
# CORTAPIEDRAS
# ============================================================

def _stonecutting(
    receta
):

    ingrediente = (
        _ingrediente_id(
            receta.get(
                "ingredient"
            )
        )
    )

    resultado = (
        _resultado_receta(
            receta
        )
    )

    if not resultado:
        return None

    return {
        "tipo": "stonecutting",
        "ingrediente": ingrediente,
        "cantidad": resultado.get(
            "count",
            1
        ),
        "resultado": (
            resultado.get(
                "id"
            )
        ),
        "estacion": "cortapiedras",
        "matriz": [
            [None, None, None],
            [None, ingrediente, None],
            [None, None, None],
        ],
        "archivo": receta.get(
            "_file"
        ),
    }


# ============================================================
# HERRERÍA
# ============================================================

def _smithing(
    receta
):

    template = _ingrediente_id(
        receta.get(
            "template"
        )
    )

    base = _ingrediente_id(
        receta.get(
            "base"
        )
    )

    addition = _ingrediente_id(
        receta.get(
            "addition"
        )
    )

    resultado = (
        _resultado_receta(
            receta
        )
    )

    if not resultado:
        return None

    return {
        "tipo": "smithing",
        "template": template,
        "base": base,
        "addition": addition,
        "cantidad": resultado.get(
            "count",
            1
        ),
        "resultado": (
            resultado.get(
                "id"
            )
        ),
        "estacion": "mesa_de_herreria",
        "matriz": [
            [template, base, addition],
            [None, None, None],
            [None, None, None],
        ],
        "archivo": receta.get(
            "_file"
        ),
    }


# ============================================================
# CONVERTIR RECETA
# ============================================================

def convertir_receta(
    receta
):

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
        "campfire_cooking",
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
        "smithing_trim",
    }:

        return _smithing(
            receta
        )

    return None


# ============================================================
# RECETAS DE ITEM
# ============================================================

@lru_cache(
    maxsize=4096
)
def obtener_recetas_item(
    item_id
):

    item_id = normalizar_id(
        item_id
    )

    if not item_id:
        return []

    resultado = []

    for receta in _leer_recetas():

        salida = (
            _resultado_receta(
                receta
            )
        )

        if not salida:
            continue

        salida_id = normalizar_id(
            salida.get(
                "id"
            )
        )

        if salida_id != item_id:
            continue

        convertida = (
            convertir_receta(
                receta
            )
        )

        if convertida:

            resultado.append(
                convertida
            )

    return resultado


# ============================================================
# PREPARAR ITEM
# ============================================================

def _preparar_item(
    item
):

    if not isinstance(
        item,
        dict
    ):
        return None

    item = dict(
        item
    )

    nombre = (
        item.get("name")
        or item.get("identifier")
    )

    if not nombre:
        return None

    identifier = normalizar_id(
        nombre
    )

    item["identifier"] = (
        identifier
    )

    item["id"] = identifier

    item["name"] = quitar_namespace(
        identifier
    )

    item["displayName"] = (
        item.get(
            "displayName"
        )
        or nombre_legible(
            identifier
        )
    )

    item["translatedName"] = (
        item["displayName"]
    )

    item["category"] = (
        item.get(
            "category"
        )
        or "misc"
    )

    stack = (
        item.get(
            "stackSize"
        )
        or item.get(
            "maxStackSize"
        )
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
        item.get(
            "maxDurability"
        )
        or item.get(
            "durability"
        )
    )

    try:

        if durability is not None:

            durability = int(
                durability
            )

    except Exception:

        durability = None

    item["durability"] = (
        durability
    )

    item["maxDurability"] = (
        durability
    )

    # --------------------------------------------------------
    # TODAS LAS RECETAS
    # --------------------------------------------------------

    recetas = obtener_recetas_item(
        identifier
    )

    item["recipes"] = recetas

    item["recipe_count"] = len(
        recetas
    )

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

    return item


# ============================================================
# ÍNDICE COMPLETO
# ============================================================

_ITEMS_INDEX = None


def _construir_indice():

    global _ITEMS_INDEX

    if _ITEMS_INDEX is not None:
        return

    print(
        "[ITEMS] Cargando TODOS "
        "los items de Minecraft..."
    )

    items = (
        _cargar_items_prismarine()
    )

    if not items:

        raise RuntimeError(
            "No se pudieron cargar "
            "los datos de Minecraft."
        )

    indice = {}

    for item in items:

        preparado = (
            _preparar_item(
                item
            )
        )

        if not preparado:
            continue

        identifier = (
            preparado.get(
                "identifier"
            )
        )

        if identifier:

            indice[
                identifier
            ] = preparado

    if not indice:

        raise RuntimeError(
            "El registro de Minecraft "
            "está vacío."
        )

    _ITEMS_INDEX = indice

    print(
        "[ITEMS] Objetos cargados:",
        len(
            _ITEMS_INDEX
        )
    )


# ============================================================
# BÚSQUEDA
# ============================================================

def buscar_item(
    texto,
    idioma=None
):

    _construir_indice()

    if not texto:
        return None

    texto = str(
        texto
    ).strip().lower()

    # --------------------------------------------------------
    # ID EXACTO
    # --------------------------------------------------------

    item_id = normalizar_id(
        texto
    )

    if item_id in _ITEMS_INDEX:

        return _ITEMS_INDEX[
            item_id
        ]

    # --------------------------------------------------------
    # ID CORTO
    # --------------------------------------------------------

    for identifier, item in (
        _ITEMS_INDEX.items()
    ):

        corto = quitar_namespace(
            identifier
        )

        if texto == corto:

            return item

    # --------------------------------------------------------
    # ID PARCIAL
    # --------------------------------------------------------

    for identifier, item in (
        _ITEMS_INDEX.items()
    ):

        corto = quitar_namespace(
            identifier
        )

        if texto in corto:

            return item

    # --------------------------------------------------------
    # NOMBRE VISIBLE
    # --------------------------------------------------------

    texto_normalizado = re.sub(
        r"[^a-z0-9áéíóúüñ ]+",
        " ",
        texto
    ).strip()

    for item in (
        _ITEMS_INDEX.values()
    ):

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
    # NOMBRE PARCIAL
    # --------------------------------------------------------

    for item in (
        _ITEMS_INDEX.values()
    ):

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

    for item in (
        _ITEMS_INDEX.values()
    ):

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
        "data_version": DATA_VERSION,
        "items": total,
        "items_con_receta": (
            con_receta
        ),
        "recetas": total_recetas,
    }


# ============================================================
# EXPORTACIONES
# ============================================================

__all__ = [
    "VERSION",
    "DATA_VERSION",
    "buscar_item",
    "obtener_item",
    "obtener_item_representativo",
    "obtener_todos_items",
    "obtener_recetas_item",
    "estadisticas_items",
    "cargar_items",
]
