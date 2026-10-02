import json
from pathlib import Path
from urllib.request import Request, urlopen


# ============================================================
# CONFIGURACIÓN
# ============================================================

MINECRAFT_VERSION = "26.1.2"

IDIOMA_DEFECTO = "es_es"

CACHE_DIR = Path("/tmp/minecraft_fullguide_languages")
CACHE_DIR.mkdir(parents=True, exist_ok=True)

CACHE_MINECRAFT = Path("/tmp/minecraft_fullguide_minecraft")
CACHE_MINECRAFT.mkdir(parents=True, exist_ok=True)


# ============================================================
# IDIOMAS
# ============================================================

IDIOMAS = {
    "es": "es_es",
    "espanol": "es_es",
    "español": "es_es",
    "spanish": "es_es",

    "en": "en_us",
    "ingles": "en_us",
    "inglés": "en_us",
    "english": "en_us",

    "ja": "ja_jp",
    "japones": "ja_jp",
    "japonés": "ja_jp",
    "japanese": "ja_jp",

    "fr": "fr_fr",
    "frances": "fr_fr",
    "francés": "fr_fr",
    "french": "fr_fr",

    "de": "de_de",
    "aleman": "de_de",
    "alemán": "de_de",
    "german": "de_de",

    "it": "it_it",
    "italiano": "it_it",
    "italian": "it_it",

    "pt": "pt_pt",
    "portugues": "pt_pt",
    "portugués": "pt_pt",
    "portuguese": "pt_pt",

    "br": "pt_br",
    "brasileno": "pt_br",
    "brasileño": "pt_br",
    "brazilian": "pt_br",

    "ru": "ru_ru",
    "ruso": "ru_ru",
    "russian": "ru_ru",

    "zh": "zh_cn",
    "chino": "zh_cn",
    "chinese": "zh_cn",

    "ko": "ko_kr",
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


_cache_idiomas = {}
_client_jar = None
_version_data = None


# ============================================================
# DESCARGA
# ============================================================

def descargar(url, timeout=60):
    request = Request(
        url,
        headers={
            "User-Agent": (
                "Mozilla/5.0 "
                "MinecraftFullGuideBot/1.0"
            )
        },
    )

    with urlopen(request, timeout=timeout) as response:
        return response.read()


# ============================================================
# IDIOMA
# ============================================================

def normalizar_idioma(valor):
    if not valor:
        return IDIOMA_DEFECTO

    valor = str(valor).strip().lower()

    if valor in IDIOMAS:
        return IDIOMAS[valor]

    if valor in NOMBRES_IDIOMAS:
        return valor

    if (
        len(valor) == 5
        and valor[2] == "_"
    ):
        return valor

    return IDIOMA_DEFECTO


# ============================================================
# MANIFIESTO OFICIAL DE MINECRAFT
# ============================================================

def _obtener_version_data():
    global _version_data

    if _version_data is not None:
        return _version_data

    cache = CACHE_MINECRAFT / (
        f"version_{MINECRAFT_VERSION}.json"
    )

    if cache.exists():
        try:
            datos = json.loads(
                cache.read_text(
                    encoding="utf-8"
                )
            )

            if isinstance(datos, dict):
                _version_data = datos
                return datos

        except Exception:
            pass

    manifiesto_url = (
        "https://piston-meta.mojang.com/"
        "mc/game/version_manifest_v2.json"
    )

    manifiesto = json.loads(
        descargar(manifiesto_url).decode("utf-8")
    )

    version_encontrada = None

    for version in manifiesto.get(
        "versions",
        [],
    ):
        if version.get("id") == MINECRAFT_VERSION:
            version_encontrada = version
            break

    if version_encontrada is None:
        raise RuntimeError(
            "No se encontró la versión de Minecraft "
            f"{MINECRAFT_VERSION} en el manifiesto oficial."
        )

    version_url = version_encontrada.get("url")

    if not version_url:
        raise RuntimeError(
            "La versión de Minecraft no contiene "
            "una URL válida de configuración."
        )

    datos = json.loads(
        descargar(version_url).decode("utf-8")
    )

    cache.write_text(
        json.dumps(
            datos,
            ensure_ascii=False,
        ),
        encoding="utf-8",
    )

    _version_data = datos

    return datos


# ============================================================
# CLIENT JAR
# ============================================================

def obtener_client_jar():
    """
    Descarga y devuelve la ruta al client.jar oficial
    de la versión configurada de Minecraft.

    Se utiliza principalmente para obtener texturas
    originales de Minecraft.
    """

    global _client_jar

    if _client_jar is not None:
        if _client_jar.exists():
            return _client_jar

    archivo = CACHE_MINECRAFT / (
        f"minecraft-{MINECRAFT_VERSION}-client.jar"
    )

    if archivo.exists() and archivo.stat().st_size > 100000:
        _client_jar = archivo
        return archivo

    datos = _obtener_version_data()

    downloads = datos.get(
        "downloads",
        {},
    )

    client = downloads.get("client")

    if not client:
        raise RuntimeError(
            "La versión de Minecraft no contiene "
            "el client.jar oficial."
        )

    url = client.get("url")

    if not url:
        raise RuntimeError(
            "No se encontró la URL oficial del client.jar."
        )

    contenido = descargar(
        url,
        timeout=180,
    )

    archivo.write_bytes(contenido)

    _client_jar = archivo

    return archivo


# ============================================================
# ASSET INDEX OFICIAL
# ============================================================

def obtener_asset_index():
    datos = _obtener_version_data()

    asset_index = datos.get(
        "assetIndex",
        {},
    )

    url = asset_index.get("url")

    if not url:
        raise RuntimeError(
            "No se encontró el Asset Index oficial."
        )

    archivo = CACHE_MINECRAFT / (
        f"asset_index_{MINECRAFT_VERSION}.json"
    )

    if archivo.exists():
        try:
            contenido = json.loads(
                archivo.read_text(
                    encoding="utf-8"
                )
            )

            if isinstance(contenido, dict):
                return contenido

        except Exception:
            pass

    contenido = json.loads(
        descargar(url).decode("utf-8")
    )

    archivo.write_text(
        json.dumps(
            contenido,
            ensure_ascii=False,
        ),
        encoding="utf-8",
    )

    return contenido


# ============================================================
# ASSETS
# ============================================================

def obtener_asset_oficial(ruta):
    """
    Obtiene un asset oficial de Minecraft usando
    el Asset Index y resources.download.minecraft.net.
    """

    asset_index = obtener_asset_index()

    objetos = asset_index.get(
        "objects",
        {},
    )

    objeto = objetos.get(ruta)

    if not objeto:
        return None

    hash_asset = objeto.get("hash")

    if not hash_asset:
        return None

    url = (
        "https://resources.download.minecraft.net/"
        f"{hash_asset[:2]}/{hash_asset}"
    )

    return descargar(
        url,
        timeout=120,
    )


# ============================================================
# IDIOMAS OFICIALES
# ============================================================

def _cargar_desde_oficial(idioma):
    ruta = (
        f"minecraft/lang/{idioma}.json"
    )

    contenido = obtener_asset_oficial(ruta)

    if contenido is None:
        raise RuntimeError(
            "No se encontró el asset oficial de idioma "
            f"{idioma}."
        )

    datos = json.loads(
        contenido.decode("utf-8")
    )

    if not isinstance(datos, dict):
        raise RuntimeError(
            f"El archivo de idioma {idioma} "
            "no contiene un objeto JSON válido."
        )

    return datos


def _cargar_desde_url(idioma):
    """
    Fallback para compatibilidad.
    Primero se intenta siempre el asset oficial.
    """

    try:
        return _cargar_desde_oficial(idioma)

    except Exception as error_oficial:
        urls = [
            (
                "https://assets.mcasset.cloud/"
                f"{MINECRAFT_VERSION}/assets/"
                f"minecraft/lang/{idioma}.json"
            ),
            (
                "https://mcasset.cloud/"
                f"{MINECRAFT_VERSION}/assets/"
                f"minecraft/lang/{idioma}.json"
            ),
        ]

        ultimo_error = error_oficial

        for url in urls:
            try:
                contenido = descargar(url)

                datos = json.loads(
                    contenido.decode("utf-8")
                )

                if isinstance(datos, dict):
                    return datos

            except Exception as error:
                ultimo_error = error

        raise ultimo_error


def cargar_idioma(idioma):
    idioma = normalizar_idioma(idioma)

    if idioma in _cache_idiomas:
        return _cache_idiomas[idioma]

    archivo_cache = (
        CACHE_DIR / f"{idioma}.json"
    )

    if archivo_cache.exists():
        try:
            datos = json.loads(
                archivo_cache.read_text(
                    encoding="utf-8"
                )
            )

            if isinstance(datos, dict):
                _cache_idiomas[idioma] = datos
                return datos

        except Exception:
            pass

    datos = _cargar_desde_url(idioma)

    archivo_cache.write_text(
        json.dumps(
            datos,
            ensure_ascii=False,
        ),
        encoding="utf-8",
    )

    _cache_idiomas[idioma] = datos

    return datos


# ============================================================
# TRADUCCIONES
# ============================================================

def traducir_identificador(
    identifier,
    idioma=IDIOMA_DEFECTO,
):
    if not identifier:
        return ""

    identifier = str(identifier)

    if identifier.startswith("#"):
        identifier = identifier[1:]

    idioma = normalizar_idioma(idioma)

    datos = cargar_idioma(idioma)

    claves = [
        f"item.minecraft.{identifier}",
        f"block.minecraft.{identifier}",
        f"entity.minecraft.{identifier}",
        f"effect.minecraft.{identifier}",
        f"enchantment.minecraft.{identifier}",
        f"potion.minecraft.{identifier}",
    ]

    for clave in claves:
        valor = datos.get(clave)

        if valor:
            return valor

    sufijo = f".{identifier}"

    for clave, valor in datos.items():
        if clave.endswith(sufijo):
            if isinstance(valor, str):
                return valor

    return identifier.replace(
        "_",
        " ",
    ).title()


# ============================================================
# IDIOMA DEL USUARIO
# ============================================================

def obtener_idioma_usuario(context):
    return normalizar_idioma(
        context.user_data.get(
            "idioma",
            IDIOMA_DEFECTO,
        )
    )


def establecer_idioma_usuario(
    context,
    idioma,
):
    idioma = normalizar_idioma(idioma)

    cargar_idioma(idioma)

    context.user_data["idioma"] = idioma

    return idioma


def obtener_nombre_idioma(idioma):
    idioma = normalizar_idioma(idioma)

    return NOMBRES_IDIOMAS.get(
        idioma,
        idioma,
    )
