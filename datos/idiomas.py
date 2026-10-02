# datos/idiomas.py

import json
import os
import zipfile
from pathlib import Path
from urllib.request import Request, urlopen

MINECRAFT_VERSION = "26.1.2"
IDIOMA_DEFECTO = "es_es"

CACHE_DIR = Path("/tmp/minecraft_fullguide_languages")
CACHE_DIR.mkdir(parents=True, exist_ok=True)

IDIOMAS = {
    "es": "es_es",
    "espanol": "es_es",
    "español": "es_es",
    "spanish": "es_es",
    "ingles": "en_us",
    "inglés": "en_us",
    "english": "en_us",
    "japones": "ja_jp",
    "japonés": "ja_jp",
    "japanese": "ja_jp",
    "frances": "fr_fr",
    "francés": "fr_fr",
    "french": "fr_fr",
    "aleman": "de_de",
    "alemán": "de_de",
    "german": "de_de",
    "italiano": "it_it",
    "italian": "it_it",
    "portugues": "pt_pt",
    "portugués": "pt_pt",
    "portuguese": "pt_pt",
    "brasileno": "pt_br",
    "brasileño": "pt_br",
    "brazilian": "pt_br",
    "ruso": "ru_ru",
    "russian": "ru_ru",
    "chino": "zh_cn",
    "chinese": "zh_cn",
    "coreano": "ko_kr",
    "korean": "ko_kr",
}

NOMBRES_IDIOMAS = {
    "es_es": "Español",
    "en_us": "English",
    "ja_jp": "日本語",
    "fr_fr": "Français",
    "de_de": "Deutsch",
    "it_it": "Italiano",
    "pt_pt": "Português",
    "pt_br": "Português (Brasil)",
    "ru_ru": "Русский",
    "zh_cn": "简体中文",
    "ko_kr": "한국어",
}

_client_jar = None
_cache_idiomas = {}


def normalizar_idioma(valor):
    if not valor:
        return IDIOMA_DEFECTO

    valor = str(valor).strip().lower()

    if valor in IDIOMAS:
        return IDIOMAS[valor]

    if valor in NOMBRES_IDIOMAS:
        return valor

    if "_" in valor and len(valor) == 5:
        return valor

    return IDIOMA_DEFECTO


def obtener_url_manifest():
    return (
        "https://piston-meta.mojang.com/mc/game/version_manifest_v2.json"
    )


def descargar_url(url):
    req = Request(
        url,
        headers={"User-Agent": "MinecraftFullGuideBot/1.0"},
    )

    with urlopen(req, timeout=60) as response:
        return response.read()


def obtener_client_jar():
    global _client_jar

    if _client_jar and _client_jar.exists():
        return _client_jar

    cache = CACHE_DIR / f"minecraft-{MINECRAFT_VERSION}.jar"

    if cache.exists():
        _client_jar = cache
        return cache

    manifest = json.loads(descargar_url(obtener_url_manifest()))

    version_url = None

    for version in manifest.get("versions", []):
        if version.get("id") == MINECRAFT_VERSION:
            version_url = version.get("url")
            break

    if not version_url:
        raise RuntimeError(
            f"No se encontró Minecraft Java {MINECRAFT_VERSION}."
        )

    version_data = json.loads(descargar_url(version_url))
    client_url = version_data["downloads"]["client"]["url"]

    data = descargar_url(client_url)
    cache.write_bytes(data)

    _client_jar = cache
    return cache


def cargar_idioma(idioma):
    idioma = normalizar_idioma(idioma)

    if idioma in _cache_idiomas:
        return _cache_idiomas[idioma]

    cache_file = CACHE_DIR / f"{idioma}.json"

    if cache_file.exists():
        try:
            datos = json.loads(
                cache_file.read_text(encoding="utf-8")
            )
            _cache_idiomas[idioma] = datos
            return datos
        except Exception:
            pass

    jar = obtener_client_jar()

    ruta = f"assets/minecraft/lang/{idioma}.json"

    with zipfile.ZipFile(jar, "r") as zf:
        if ruta not in zf.namelist():
            idioma = IDIOMA_DEFECTO
            ruta = f"assets/minecraft/lang/{idioma}.json"

        datos = json.loads(
            zf.read(ruta).decode("utf-8")
        )

    cache_file.write_text(
        json.dumps(datos, ensure_ascii=False),
        encoding="utf-8",
    )

    _cache_idiomas[idioma] = datos

    return datos


def traducir_identificador(identifier, idioma=IDIOMA_DEFECTO):
    identifier = str(identifier)

    datos = cargar_idioma(idioma)

    claves = [
        f"item.minecraft.{identifier}",
        f"block.minecraft.{identifier}",
        f"entity.minecraft.{identifier}",
    ]

    for clave in claves:
        if clave in datos:
            return datos[clave]

    return identifier.replace("_", " ").title()


def establecer_idioma_usuario(context, idioma):
    idioma = normalizar_idioma(idioma)
    context.user_data["idioma"] = idioma
    return idioma


def obtener_idioma_usuario(context):
    return normalizar_idioma(
        context.user_data.get(
            "idioma",
            IDIOMA_DEFECTO,
        )
)
