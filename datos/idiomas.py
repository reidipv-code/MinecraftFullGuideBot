# datos/idiomas.py

import json
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


def descargar(url):
    request = Request(
        url,
        headers={
            "User-Agent": (
                "Mozilla/5.0 "
                "MinecraftFullGuideBot/1.0"
            )
        },
    )

    with urlopen(
        request,
        timeout=60,
    ) as response:
        return response.read()


def normalizar_idioma(valor):
    if not valor:
        return IDIOMA_DEFECTO

    valor = str(valor).strip().lower()

    if valor in IDIOMAS:
        return IDIOMAS[valor]

    if valor in NOMBRES_IDIOMAS:
        return valor

    # Permitir directamente códigos como es_es,
    # en_us, ja_jp, etc.
    if (
        len(valor) == 5
        and valor[2] == "_"
    ):
        return valor

    return IDIOMA_DEFECTO


def _cargar_desde_url(idioma):
    """
    Descarga el archivo de idioma oficial correspondiente
    a la versión de Minecraft configurada.
    """

    urls = [
        (
            "https://assets.mcasset.cloud/"
            f"{MINECRAFT_VERSION}/assets/minecraft/"
            f"lang/{idioma}.json"
        ),
        (
            "https://mcasset.cloud/"
            f"{MINECRAFT_VERSION}/assets/minecraft/"
            f"lang/{idioma}.json"
        ),
    ]

    ultimo_error = None

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

    if ultimo_error:
        raise ultimo_error

    raise RuntimeError(
        f"No se pudo cargar el idioma {idioma}."
    )


def cargar_idioma(idioma):
    idioma = normalizar_idioma(idioma)

    if idioma in _cache_idiomas:
        return _cache_idiomas[idioma]

    archivo_cache = (
        CACHE_DIR / f"{idioma}.json"
    )

    # Primero usamos cache.
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

    # Descarga directa de los assets.
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

    # Algunos nombres pueden existir bajo
    # claves que no empiezan exactamente por
    # item.minecraft o block.minecraft.
    sufijo = f".{identifier}"

    for clave, valor in datos.items():
        if clave.endswith(sufijo):
            if isinstance(valor, str):
                return valor

    # Último fallback.
    return identifier.replace(
        "_",
        " ",
    ).title()


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

    # Comprobamos que realmente exista.
    cargar_idioma(idioma)

    context.user_data["idioma"] = idioma

    return idioma


def obtener_nombre_idioma(idioma):
    idioma = normalizar_idioma(idioma)

    return NOMBRES_IDIOMAS.get(
        idioma,
        idioma,
    )
