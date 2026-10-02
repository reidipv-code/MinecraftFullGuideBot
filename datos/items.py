# datos/items.py

import json
import zipfile
from pathlib import Path
from urllib.request import Request, urlopen

from datos.idiomas import traducir_identificador


MINECRAFT_DATA_URL = (
    "https://raw.githubusercontent.com/"
    "PrismarineJS/minecraft-data/master/"
    "data/pc/26.1/items.json"
)

VERSION_MANIFEST_URL = (
    "https://piston-meta.mojang.com/"
    "mc/game/version_manifest_v2.json"
)

MINECRAFT_VERSION = "26.1.2"

CACHE_DIR = Path("/tmp/minecraft_fullguide_data")
CACHE_DIR.mkdir(parents=True, exist_ok=True)

_items = None
_recipes = None
_server_jar = None


def descargar(url):
    req = Request(
        url,
        headers={
            "User-Agent": "MinecraftFullGuideBot/1.0",
        },
    )

    with urlopen(req, timeout=90) as response:
        return response.read()


def cargar_items():
    global _items

    if _items is not None:
        return _items

    cache = CACHE_DIR / "items.json"

    if cache.exists():
        try:
            _items = json.loads(
                cache.read_text(encoding="utf-8")
            )
            return _items
        except Exception:
            pass

    datos = json.loads(
        descargar(MINECRAFT_DATA_URL).decode("utf-8")
    )

    cache.write_text(
        json.dumps(datos, ensure_ascii=False),
        encoding="utf-8",
    )

    _items = datos

    return datos


def obtener_server_jar():
    global _server_jar

    if _server_jar and _server_jar.exists():
        return _server_jar

    cache = CACHE_DIR / f"server-{MINECRAFT_VERSION}.jar"

    if cache.exists():
        _server_jar = cache
        return cache

    manifest = json.loads(
        descargar(VERSION_MANIFEST_URL).decode("utf-8")
    )

    version_url = None

    for version in manifest.get("versions", []):
        if version.get("id") == MINECRAFT_VERSION:
            version_url = version.get("url")
            break

    if not version_url:
        raise RuntimeError(
            f"No se encontró Minecraft {MINECRAFT_VERSION}."
        )

    version_data = json.loads(
        descargar(version_url).decode("utf-8")
    )

    server_url = version_data["downloads"]["server"]["url"]

    data = descargar(server_url)

    cache.write_bytes(data)

    _server_jar = cache

    return cache


def _id_minecraft(valor):
    if not valor:
        return None

    valor = str(valor)

    if valor.startswith("minecraft:"):
        return valor.split(":", 1)[1]

    return valor


def _ingrediente(valor):
    if not valor:
        return None

    if isinstance(valor, str):
        return _id_minecraft(valor)

    if isinstance(valor, list):
        for elemento in valor:
            resultado = _ingrediente(elemento)
            if resultado:
                return resultado
        return None

    if isinstance(valor, dict):
        if "item" in valor:
            return _id_minecraft(valor["item"])

        if "items" in valor:
            items = valor["items"]

            if isinstance(items, list):
                for item in items:
                    resultado = _ingrediente(item)
                    if resultado:
                        return resultado

        if "tag" in valor:
            return "#" + str(valor["tag"]).split(":", 1)[-1]

    return None


def _leer_recetas():
    global _recipes

    if _recipes is not None:
        return _recipes

    recetas = []

    jar = obtener_server_jar()

    with zipfile.ZipFile(jar, "r") as zf:
        nombres = sorted(
            nombre
            for nombre in zf.namelist()
            if nombre.startswith("data/minecraft/recipe/")
            and nombre.endswith(".json")
        )

        for nombre in nombres:
            try:
                datos = json.loads(
                    zf.read(nombre).decode("utf-8")
                )

                datos["_nombre_archivo"] = (
                    Path(nombre).stem
                )

                recetas.append(datos)

            except Exception:
                continue

    _recipes = recetas

    return recetas


def _resultado_receta(receta):
    resultado = receta.get("result")

    if isinstance(resultado, str):
        return _id_minecraft(resultado)

    if isinstance(resultado, dict):
        if "id" in resultado:
            return _id_minecraft(resultado["id"])

        if "item" in resultado:
            return _id_minecraft(resultado["item"])

    return None


def _nombre_resultado(receta):
    resultado = receta.get("result")

    if isinstance(resultado, dict):
        if "id" in resultado:
            return _id_minecraft(resultado["id"])

        if "item" in resultado:
            return _id_minecraft(resultado["item"])

    if isinstance(resultado, str):
        return _id_minecraft(resultado)

    return None


def _receta_crafting(receta):
    tipo = receta.get("type", "")

    if "crafting_shaped" in tipo:
        patron = receta.get("pattern", [])
        key = receta.get("key", {})

        matriz = []

        for fila in patron:
            fila_resultado = []

            for caracter in fila:
                if caracter == " ":
                    fila_resultado.append(None)
                    continue

                ingrediente = _ingrediente(
                    key.get(caracter)
                )

                fila_resultado.append(ingrediente)

            matriz.append(fila_resultado)

        return {
            "tipo": "crafting",
            "forma": "shaped",
            "matriz": matriz,
        }

    if "crafting_shapeless" in tipo:
        ingredientes = [
            _ingrediente(ingrediente)
            for ingrediente in receta.get(
                "ingredients",
                [],
            )
        ]

        ingredientes = [
            ingrediente
            for ingrediente in ingredientes
            if ingrediente
        ]

        return {
            "tipo": "crafting",
            "forma": "shapeless",
            "ingredientes": ingredientes,
        }

    return None


def _receta_proceso(receta):
    tipo = receta.get("type", "")

    if any(
        nombre in tipo
        for nombre in (
            "smelting",
            "blasting",
            "smoking",
            "campfire_cooking",
        )
    ):
        ingrediente = _ingrediente(
            receta.get("ingredient")
        )

        if not ingrediente:
            ingrediente = _ingrediente(
                receta.get("ingredients")
            )

        resultado = _resultado_receta(receta)

        if not resultado:
            return None

        if "blasting" in tipo:
            proceso = "alto_horno"

        elif "smoking" in tipo:
            proceso = "ahumador"

        elif "campfire" in tipo:
            proceso = "fogata"

        else:
            proceso = "horno"

        return {
            "tipo": "proceso",
            "proceso": proceso,
            "ingrediente": ingrediente,
            "resultado": resultado,
        }

    if "stonecutting" in tipo:
        ingrediente = _ingrediente(
            receta.get("ingredient")
        )

        resultado = _resultado_receta(receta)

        if ingrediente and resultado:
            return {
                "tipo": "stonecutting",
                "ingrediente": ingrediente,
                "resultado": resultado,
            }

    return None


def obtener_recetas_item(identifier):
    identifier = _id_minecraft(identifier)

    recetas = []

    for receta in _leer_recetas():
        resultado = _resultado_receta(receta)

        if resultado != identifier:
            continue

        datos = (
            _receta_crafting(receta)
            or _receta_proceso(receta)
        )

        if datos:
            datos["_nombre"] = receta.get(
                "_nombre_archivo",
                "",
            )
            recetas.append(datos)

    return recetas


def _normalizar(texto):
    reemplazos = {
        "á": "a",
        "é": "e",
        "í": "i",
        "ó": "o",
        "ú": "u",
        "ü": "u",
        "ñ": "n",
    }

    texto = str(texto).lower()

    for original, reemplazo in reemplazos.items():
        texto = texto.replace(
            original,
            reemplazo,
        )

    return " ".join(texto.split())


ALIASES = {
    "pico de diamante": "diamond_pickaxe",
    "pico diamante": "diamond_pickaxe",
    "espada de diamante": "diamond_sword",
    "espada diamante": "diamond_sword",
    "pala de diamante": "diamond_shovel",
    "hacha de diamante": "diamond_axe",
    "azada de diamante": "diamond_hoe",
    "mesa de crafteo": "crafting_table",
    "mesa de trabajo": "crafting_table",
    "horno": "furnace",
    "piedra": "stone",
    "piedra labrada": "stone",
    "cobblestone": "cobblestone",
    "piedra bruta": "cobblestone",
    "cristal": "glass",
    "vidrio": "glass",
    "arena": "sand",
    "palo": "stick",
    "palos": "stick",
    "diamante": "diamond",
    "oro": "gold_ingot",
    "lingote de oro": "gold_ingot",
    "hierro": "iron_ingot",
    "lingote de hierro": "iron_ingot",
    "madera": "oak_log",
    "tronco de roble": "oak_log",
    "tablones": "oak_planks",
    "tablones de roble": "oak_planks",
}


def buscar_item(texto, idioma="es_es"):
    texto_original = texto.strip()

    if not texto_original:
        return None

    normalizado = _normalizar(texto_original)

    identificador = ALIASES.get(normalizado)

    items = cargar_items()

    if identificador:
        for item in items:
            if item.get("name") == identificador:
                return preparar_item(
                    item,
                    idioma,
                )

    exacto = None

    for item in items:
        if item.get("name") == normalizado.replace(
            " ",
            "_",
        ):
            exacto = item
            break

    if exacto:
        return preparar_item(
            exacto,
            idioma,
        )

    candidatos = []

    for item in items:
        nombre = item.get("name", "")
        display = item.get("displayName", "")

        score = 0

        nombre_normalizado = _normalizar(nombre)
        display_normalizado = _normalizar(display)

        if normalizado == nombre_normalizado:
            score += 100

        if normalizado == display_normalizado:
            score += 100

        if normalizado in nombre_normalizado:
            score += 50

        if normalizado in display_normalizado:
            score += 50

        palabras = normalizado.split()

        for palabra in palabras:
            if palabra in nombre_normalizado:
                score += 10

            if palabra in display_normalizado:
                score += 10

        if score:
            candidatos.append(
                (
                    score,
                    len(nombre),
                    item,
                )
            )

    if not candidatos:
        return None

    candidatos.sort(
        key=lambda x: (
            -x[0],
            x[1],
            x[2].get("name", ""),
        )
    )

    return preparar_item(
        candidatos[0][2],
        idioma,
    )


def preparar_item(item, idioma):
    identifier = item.get("name", "")

    resultado = dict(item)

    resultado["identifier"] = identifier

    resultado["translatedName"] = traducir_identificador(
        identifier,
        idioma,
    )

    resultado["recipes"] = obtener_recetas_item(
        identifier
    )

    return resultado
