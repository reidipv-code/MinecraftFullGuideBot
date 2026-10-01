import io
import os
import urllib.request
from pathlib import Path

from PIL import Image, ImageDraw, ImageFont


# ============================================================
# CONFIGURACIÓN
# ============================================================

ANCHO_GUI = 176
ALTO_GUI = 166

ESCALA = 4

ANCHO_FINAL = ANCHO_GUI * ESCALA
ALTO_FINAL = ALTO_GUI * ESCALA

VERSION_MINECRAFT = "1.21.4"

CACHE_DIR = Path(
    os.getenv(
        "MINECRAFT_ASSETS_CACHE",
        "/tmp/minecraft_fullguide_assets",
    )
)

CACHE_DIR.mkdir(
    parents=True,
    exist_ok=True,
)


# ============================================================
# URLS OFICIALES DE MINECRAFT
# ============================================================

VERSION_MANIFEST_URL = (
    "https://piston-meta.mojang.com/mc/game/"
    "version_manifest_v2.json"
)

ASSET_BASE_URL = (
    "https://resources.download.minecraft.net"
)


# ============================================================
# POSICIONES DE LA INTERFAZ VANILLA
# ============================================================

GRID_X = 30
GRID_Y = 17

SLOT = 18

RESULTADO_X = 124
RESULTADO_Y = 35


# ============================================================
# RUTAS DE TEXTURAS
# ============================================================

TEXTURAS = {
    "diamond": [
        "minecraft/textures/item/diamond.png",
    ],

    "stick": [
        "minecraft/textures/item/stick.png",
    ],

    "diamond_pickaxe": [
        "minecraft/textures/item/diamond_pickaxe.png",
    ],

    "diamond_sword": [
        "minecraft/textures/item/diamond_sword.png",
    ],

    "planks": [
        "minecraft/textures/block/oak_planks.png",
    ],

    "cobblestone": [
        "minecraft/textures/block/cobblestone.png",
    ],

    "crafting_table": [
        "minecraft/textures/item/crafting_table.png",
        "minecraft/textures/block/crafting_table_front.png",
        "minecraft/textures/block/crafting_table_side.png",
    ],

    "furnace": [
        "minecraft/textures/item/furnace.png",
        "minecraft/textures/block/furnace_front.png",
    ],
}


# ============================================================
# FUENTES
# ============================================================

FUENTES = [
    "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf",
    "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf",
    "/usr/share/fonts/truetype/liberation2/LiberationSans-Bold.ttf",
    "/usr/share/fonts/truetype/liberation2/LiberationSans-Regular.ttf",
]


def obtener_fuente(tamano):
    for ruta in FUENTES:
        try:
            return ImageFont.truetype(
                ruta,
                tamano,
            )
        except Exception:
            pass

    return ImageFont.load_default()


# ============================================================
# HTTP
# ============================================================

def descargar_bytes(url):
    request = urllib.request.Request(
        url,
        headers={
            "User-Agent": (
                "MinecraftFullGuideBot/1.0 "
                "(Minecraft guide bot)"
            )
        },
    )

    with urllib.request.urlopen(
        request,
        timeout=20,
    ) as response:
        return response.read()


# ============================================================
# MANIFEST DE VERSIONES
# ============================================================

def obtener_version_url():
    cache = CACHE_DIR / "version_manifest.json"

    try:
        if cache.exists():
            datos = cache.read_bytes()
        else:
            datos = descargar_bytes(
                VERSION_MANIFEST_URL
            )
            cache.write_bytes(datos)

        import json

        manifest = json.loads(
            datos.decode("utf-8")
        )

        for version in manifest.get(
            "versions",
            [],
        ):
            if version.get("id") == VERSION_MINECRAFT:
                return version.get("url")

    except Exception as error:
        print(
            "[MinecraftFullGuideBot] "
            f"Error obteniendo manifest: {error}"
        )

    return None


# ============================================================
# ASSET INDEX
# ============================================================

def obtener_asset_index():
    import json

    cache = CACHE_DIR / (
        f"asset_index_{VERSION_MINECRAFT}.json"
    )

    try:
        if cache.exists():
            datos = cache.read_bytes()

            return json.loads(
                datos.decode("utf-8")
            )

        version_url = obtener_version_url()

        if not version_url:
            return None

        datos_version = descargar_bytes(
            version_url
        )

        version = json.loads(
            datos_version.decode("utf-8")
        )

        asset_index = version.get(
            "assetIndex"
        )

        if not asset_index:
            return None

        asset_url = asset_index.get(
            "url"
        )

        if not asset_url:
            return None

        datos_assets = descargar_bytes(
            asset_url
        )

        cache.write_bytes(
            datos_assets
        )

        return json.loads(
            datos_assets.decode("utf-8")
        )

    except Exception as error:
        print(
            "[MinecraftFullGuideBot] "
            f"Error obteniendo assets: {error}"
        )

        return None


# ============================================================
# OBTENER TEXTURA DESDE LOS ASSETS DE MOJANG
# ============================================================

def obtener_asset_minecraft(
    ruta,
):
    import json

    nombre_cache = ruta.replace(
        "/",
        "_",
    )

    archivo_cache = (
        CACHE_DIR / nombre_cache
    )

    if (
        archivo_cache.exists()
        and archivo_cache.stat().st_size > 0
    ):
        return archivo_cache

    indice = obtener_asset_index()

    if not indice:
        return None

    objeto = indice.get(
        "objects",
        {},
    ).get(ruta)

    if not objeto:
        return None

    hash_asset = objeto.get(
        "hash"
    )

    if not hash_asset:
        return None

    url = (
        f"{ASSET_BASE_URL}/"
        f"{hash_asset[:2]}/"
        f"{hash_asset}"
    )

    try:
        datos = descargar_bytes(
            url
        )

        archivo_cache.write_bytes(
            datos
        )

        return archivo_cache

    except Exception as error:
        print(
            "[MinecraftFullGuideBot] "
            f"No se pudo descargar {ruta}: "
            f"{error}"
        )

        return None


# ============================================================
# CARGAR TEXTURA
# ============================================================

def cargar_textura(
    identificador,
):
    rutas = TEXTURAS.get(
        identificador,
        [],
    )

    for ruta in rutas:

        archivo = obtener_asset_minecraft(
            ruta
        )

        if archivo is None:
            continue

        try:
            return Image.open(
                archivo
            ).convert("RGBA")

        except Exception as error:
            print(
                "[MinecraftFullGuideBot] "
                f"Error leyendo {ruta}: {error}"
            )

    print(
        "[MinecraftFullGuideBot] "
        f"No se encontró textura para "
        f"{identificador}"
    )

    return None


# ============================================================
# CARGAR GUI VANILLA
# ============================================================

def cargar_interfaz_vanilla():
    rutas = [
        "minecraft/textures/gui/container/"
        "crafting_table.png",

        "minecraft/textures/gui/container/"
        "crafting_table.png",
    ]

    for ruta in rutas:

        archivo = obtener_asset_minecraft(
            ruta
        )

        if archivo is None:
            continue

        try:
            return Image.open(
                archivo
            ).convert("RGBA")

        except Exception as error:
            print(
                "[MinecraftFullGuideBot] "
                f"Error leyendo GUI: {error}"
            )

    return None


# ============================================================
# PATRÓN -> 3x3
# ============================================================

def normalizar_patron(
    patron,
):
    resultado = [
        [None, None, None],
        [None, None, None],
        [None, None, None],
    ]

    if not patron:
        return resultado

    alto = min(
        len(patron),
        3,
    )

    ancho = 0

    for fila in patron[:3]:
        if fila:
            ancho = max(
                ancho,
                min(len(fila), 3),
            )

    if ancho == 0:
        return resultado

    desplazamiento_x = (
        3 - ancho
    ) // 2

    desplazamiento_y = (
        3 - alto
    ) // 2

    for fila in range(alto):

        datos = patron[fila]

        if not datos:
            continue

        for columna in range(
            min(len(datos), 3)
        ):
            resultado[
                desplazamiento_y + fila
            ][
                desplazamiento_x + columna
            ] = datos[columna]

    return resultado


# ============================================================
# PREPARAR TEXTURA
# ============================================================

def preparar_textura(
    textura,
):
    if textura is None:
        return None

    return textura.resize(
        (
            16 * ESCALA,
            16 * ESCALA,
        ),
        Image.Resampling.NEAREST,
    )


# ============================================================
# DIBUJAR TEXTURA EN SLOT
# ============================================================

def dibujar_item(
    imagen,
    identificador,
    x,
    y,
):
    textura = cargar_textura(
        identificador
    )

    if textura is None:
        return False

    textura = preparar_textura(
        textura
    )

    if textura is None:
        return False

    imagen.alpha_composite(
        textura,
        (
            x + ESCALA,
            y + ESCALA,
        ),
    )

    return True


# ============================================================
# CANTIDAD
# ============================================================

def dibujar_cantidad(
    imagen,
    cantidad,
    x,
    y,
):
    if not cantidad or cantidad <= 1:
        return

    draw = ImageDraw.Draw(
        imagen
    )

    fuente = obtener_fuente(
        10 * ESCALA
    )

    texto = str(cantidad)

    posicion = (
        x + 17 * ESCALA,
        y + 17 * ESCALA,
    )

    draw.text(
        (
            posicion[0] + 2,
            posicion[1] + 2,
        ),
        texto,
        font=fuente,
        fill=(0, 0, 0, 255),
        anchor="rb",
    )

    draw.text(
        posicion,
        texto,
        font=fuente,
        fill=(255, 255, 255, 255),
        anchor="rb",
    )


# ============================================================
# TEXTO EXTERIOR
# ============================================================

def agregar_texto(
    imagen,
    item,
):
    alto_extra = 105

    resultado = Image.new(
        "RGBA",
        (
            imagen.width,
            imagen.height + alto_extra,
        ),
        (
            25,
            25,
            25,
            255,
        ),
    )

    resultado.alpha_composite(
        imagen,
        (
            0,
            alto_extra,
        ),
    )

    draw = ImageDraw.Draw(
        resultado
    )

    titulo = obtener_fuente(
        25
    )

    subtitulo = obtener_fuente(
        19
    )

    nombre = item.get(
        "nombre",
        "Objeto",
    )

    # Sombra del título
    draw.text(
        (21, 16),
        "FABRICACIÓN",
        font=titulo,
        fill=(0, 0, 0, 255),
    )

    draw.text(
        (20, 15),
        "FABRICACIÓN",
        font=titulo,
        fill=(255, 255, 255, 255),
    )

    # Nombre
    draw.text(
        (21, 57),
        nombre,
        font=subtitulo,
        fill=(0, 0, 0, 255),
    )

    draw.text(
        (20, 56),
        nombre,
        font=subtitulo,
        fill=(220, 220, 220, 255),
    )

    return resultado


# ============================================================
# GENERADOR PRINCIPAL
# ============================================================

def generar_imagen_crafteo(
    item,
):
    """
    Genera la imagen del crafteo.

    IMPORTANTE:
    Esta función es la que importa comandos/items.py.
    """

    receta = item.get(
        "receta"
    )

    if not receta:
        return None

    patron = receta.get(
        "patron"
    )

    if not patron:
        return None

    # --------------------------------------------------------
    # SIEMPRE 3x3
    # --------------------------------------------------------

    patron = normalizar_patron(
        patron
    )

    # --------------------------------------------------------
    # CARGAR GUI REAL DE MINECRAFT
    # --------------------------------------------------------

    interfaz = cargar_interfaz_vanilla()

    if interfaz is None:
        print(
            "[MinecraftFullGuideBot] "
            "No se pudo cargar la GUI vanilla."
        )

        return None

    # --------------------------------------------------------
    # La GUI vanilla utiliza los primeros 176x166 px.
    # --------------------------------------------------------

    if (
        interfaz.width >= 176
        and interfaz.height >= 166
    ):
        interfaz = interfaz.crop(
            (
                0,
                0,
                176,
                166,
            )
        )
    else:
        interfaz = interfaz.resize(
            (
                176,
                166,
            ),
            Image.Resampling.NEAREST,
        )

    # --------------------------------------------------------
    # ESCALAR SIN SUAVIZADO
    # --------------------------------------------------------

    imagen = interfaz.resize(
        (
            ANCHO_FINAL,
            ALTO_FINAL,
        ),
        Image.Resampling.NEAREST,
    )

    # --------------------------------------------------------
    # INGREDIENTES
    # --------------------------------------------------------

    for fila in range(3):

        for columna in range(3):

            identificador = (
                patron[fila][columna]
            )

            if not identificador:
                continue

            x = (
                GRID_X
                + columna * SLOT
            ) * ESCALA

            y = (
                GRID_Y
                + fila * SLOT
            ) * ESCALA

            dibujar_item(
                imagen,
                identificador,
                x,
                y,
            )

    # --------------------------------------------------------
    # RESULTADO
    # --------------------------------------------------------

    identificador_resultado = (
        receta.get(
            "resultado",
            item.get(
                "identificador"
            ),
        )
    )

    x_resultado = (
        RESULTADO_X * ESCALA
    )

    y_resultado = (
        RESULTADO_Y * ESCALA
    )

    dibujar_item(
        imagen,
        identificador_resultado,
        x_resultado,
        y_resultado,
    )

    # --------------------------------------------------------
    # CANTIDAD DEL RESULTADO
    # --------------------------------------------------------

    dibujar_cantidad(
        imagen,
        receta.get(
            "cantidad_resultado",
            1,
        ),
        x_resultado,
        y_resultado,
    )

    # --------------------------------------------------------
    # TÍTULO Y NOMBRE
    # --------------------------------------------------------

    imagen = agregar_texto(
        imagen,
        item,
    )

    # --------------------------------------------------------
    # PNG
    # --------------------------------------------------------

    buffer = io.BytesIO()

    imagen.save(
        buffer,
        format="PNG",
        optimize=True,
    )

    buffer.seek(0)

    # Telegram puede utilizar este nombre al enviar el buffer.
    buffer.name = "crafteo_minecraft.png"

    return buffer
