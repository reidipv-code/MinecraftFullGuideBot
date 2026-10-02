# core/generador_crafteo.py

import json
import zipfile
from io import BytesIO
from pathlib import Path

from PIL import Image, ImageDraw

from datos.idiomas import obtener_client_jar


CACHE_DIR = Path("/tmp/minecraft_fullguide_render")
CACHE_DIR.mkdir(parents=True, exist_ok=True)

_MODELOS_CACHE = {}
_TEXTURAS_CACHE = {}


# ============================================================
# ASSETS DEL CLIENTE
# ============================================================

def _leer_json_asset(ruta):
    """
    Lee un JSON directamente desde el client.jar oficial.
    """

    jar = obtener_client_jar()

    try:
        with zipfile.ZipFile(jar, "r") as zf:
            if ruta not in zf.namelist():
                return None

            contenido = zf.read(ruta)

        return json.loads(
            contenido.decode("utf-8")
        )

    except Exception:
        return None


def _leer_bytes_asset(ruta):
    """
    Lee bytes directamente desde el client.jar oficial.
    """

    jar = obtener_client_jar()

    try:
        with zipfile.ZipFile(jar, "r") as zf:
            if ruta not in zf.namelist():
                return None

            return zf.read(ruta)

    except Exception:
        return None


# ============================================================
# MODELOS
# ============================================================

def _normalizar_modelo(modelo):
    if not modelo:
        return None

    modelo = str(modelo)

    if modelo.startswith("minecraft:"):
        modelo = modelo.split(":", 1)[1]

    if modelo.endswith(".json"):
        modelo = modelo[:-5]

    return modelo


def _cargar_modelo(modelo):
    modelo = _normalizar_modelo(modelo)

    if not modelo:
        return None

    if modelo in _MODELOS_CACHE:
        return _MODELOS_CACHE[modelo]

    rutas = [
        f"assets/minecraft/models/{modelo}.json",
    ]

    for ruta in rutas:
        datos = _leer_json_asset(ruta)

        if datos is not None:
            _MODELOS_CACHE[modelo] = datos
            return datos

    _MODELOS_CACHE[modelo] = None

    return None


def _resolver_modelo_item(identifier):
    """
    Minecraft 26.1.x utiliza:

        assets/minecraft/items/<item>.json

    Ese archivo apunta al modelo real del objeto.
    """

    identifier = str(identifier)

    if identifier.startswith("minecraft:"):
        identifier = identifier.split(
            ":",
            1,
        )[1]

    ruta = (
        f"assets/minecraft/items/"
        f"{identifier}.json"
    )

    datos = _leer_json_asset(ruta)

    if not datos:
        return f"item/{identifier}"

    modelo = datos.get("model")

    if isinstance(modelo, str):
        return _normalizar_modelo(modelo)

    if isinstance(modelo, dict):
        modelo_id = modelo.get("model")

        if modelo_id:
            return _normalizar_modelo(
                modelo_id
            )

        # Algunos modelos pueden utilizar
        # referencias alternativas.
        modelo_type = modelo.get("type")

        if modelo_type == "minecraft:model":
            return _normalizar_modelo(
                modelo.get("model")
            )

    return f"item/{identifier}"


# ============================================================
# TEXTURAS
# ============================================================

def _normalizar_textura(textura):
    if not textura:
        return None

    textura = str(textura)

    if textura.startswith("#"):
        return textura

    if textura.startswith("minecraft:"):
        textura = textura.split(
            ":",
            1,
        )[1]

    if textura.endswith(".png"):
        textura = textura[:-4]

    return textura


def _buscar_textura(nombre):
    nombre = _normalizar_textura(nombre)

    if not nombre:
        return None

    if nombre.startswith("#"):
        return None

    if nombre in _TEXTURAS_CACHE:
        return _TEXTURAS_CACHE[nombre]

    rutas = [
        f"assets/minecraft/textures/{nombre}.png",
    ]

    for ruta in rutas:
        data = _leer_bytes_asset(ruta)

        if data:
            try:
                imagen = Image.open(
                    BytesIO(data)
                ).convert("RGBA")

                _TEXTURAS_CACHE[nombre] = imagen

                return imagen

            except Exception:
                pass

    _TEXTURAS_CACHE[nombre] = None

    return None


def _resolver_textura_desde_modelo(
    modelo_id,
    _visitados=None,
):
    """
    Resuelve recursivamente:

        item -> modelo
        modelo -> parent
        modelo -> textures
        texture -> PNG

    Esto permite encontrar texturas de:
    - herramientas
    - bloques
    - objetos
    - armas
    - comida
    - etc.
    """

    if _visitados is None:
        _visitados = set()

    modelo_id = _normalizar_modelo(modelo_id)

    if not modelo_id:
        return None

    if modelo_id in _visitados:
        return None

    _visitados.add(modelo_id)

    modelo = _cargar_modelo(modelo_id)

    if not modelo:
        return None

    texturas = modelo.get(
        "textures",
        {},
    )

    # --------------------------------------------------------
    # Buscar textura directa
    # --------------------------------------------------------

    preferencias = [
        "layer0",
        "particle",
        "side",
        "front",
        "all",
        "top",
        "bottom",
    ]

    for clave in preferencias:
        textura = texturas.get(clave)

        if textura:
            textura = _resolver_referencia_textura(
                textura,
                texturas,
            )

            imagen = _buscar_textura(
                textura
            )

            if imagen is not None:
                return imagen

    # --------------------------------------------------------
    # Cualquier textura disponible
    # --------------------------------------------------------

    for textura in texturas.values():
        if not isinstance(textura, str):
            continue

        textura = _resolver_referencia_textura(
            textura,
            texturas,
        )

        imagen = _buscar_textura(
            textura
        )

        if imagen is not None:
            return imagen

    # --------------------------------------------------------
    # Herencia del modelo
    # --------------------------------------------------------

    parent = modelo.get("parent")

    if parent:
        return _resolver_textura_desde_modelo(
            parent,
            _visitados,
        )

    return None


def _resolver_referencia_textura(
    referencia,
    texturas,
):
    if not referencia:
        return None

    referencia = str(referencia)

    if referencia.startswith("#"):
        clave = referencia[1:]

        valor = texturas.get(clave)

        if valor:
            return _resolver_referencia_textura(
                valor,
                texturas,
            )

        return None

    return referencia


# ============================================================
# TEXTURA PRINCIPAL DEL ITEM
# ============================================================

def _cargar_textura_item(identifier):
    if not identifier:
        return None

    identifier = str(identifier)

    if identifier.startswith("minecraft:"):
        identifier = identifier.split(
            ":",
            1,
        )[1]

    # --------------------------------------------------------
    # 1. Modelo moderno de Minecraft
    # --------------------------------------------------------

    modelo = _resolver_modelo_item(
        identifier
    )

    imagen = _resolver_textura_desde_modelo(
        modelo
    )

    if imagen is not None:
        return imagen.copy()

    # --------------------------------------------------------
    # 2. Fallback directo
    # --------------------------------------------------------

    rutas_directas = [
        f"item/{identifier}",
        f"block/{identifier}",
    ]

    for ruta in rutas_directas:
        imagen = _buscar_textura(ruta)

        if imagen is not None:
            return imagen.copy()

    return None


# ============================================================
# DIBUJAR ITEM
# ============================================================

def _escalar_pixel_art(
    textura,
    tamano,
):
    if textura is None:
        return None

    textura = textura.copy()

    textura.thumbnail(
        (
            int(tamano * 0.82),
            int(tamano * 0.82),
        ),
        Image.Resampling.NEAREST,
    )

    return textura


def _dibujar_item(
    canvas,
    identifier,
    x,
    y,
    tamano=96,
):
    textura = _cargar_textura_item(
        identifier
    )

    if textura is None:
        return False

    textura = _escalar_pixel_art(
        textura,
        tamano,
    )

    px = (
        x
        + (tamano - textura.width) // 2
    )

    py = (
        y
        + (tamano - textura.height) // 2
    )

    canvas.alpha_composite(
        textura,
        (
            px,
            py,
        ),
    )

    return True


# ============================================================
# SLOT
# ============================================================

def _dibujar_slot(
    canvas,
    x,
    y,
    tamano=96,
):
    draw = ImageDraw.Draw(canvas)

    draw.rectangle(
        [
            x,
            y,
            x + tamano,
            y + tamano,
        ],
        fill=(139, 139, 139, 255),
        outline=(35, 35, 35, 255),
        width=4,
    )

    draw.rectangle(
        [
            x + 6,
            y + 6,
            x + tamano - 6,
            y + tamano - 6,
        ],
        fill=(90, 90, 90, 255),
        outline=(190, 190, 190, 255),
        width=2,
    )


# ============================================================
# FLECHA
# ============================================================

def _dibujar_flecha(
    draw,
    x,
    y,
):
    draw.polygon(
        [
            (x, y),
            (x + 110, y),
            (x + 110, y - 22),
            (x + 170, y + 45),
            (x + 110, y + 112),
            (x + 110, y + 90),
            (x, y + 90),
        ],
        fill=(80, 80, 80, 255),
    )


# ============================================================
# CRAFTING 3x3
# ============================================================

def _dibujar_crafting(
    receta,
    salida,
    nombre_salida,
):
    ancho = 1200
    alto = 760

    imagen = Image.new(
        "RGBA",
        (
            ancho,
            alto,
        ),
        (198, 198, 198, 255),
    )

    draw = ImageDraw.Draw(imagen)

    draw.rectangle(
        [
            0,
            0,
            ancho - 1,
            alto - 1,
        ],
        fill=(198, 198, 198, 255),
        outline=(60, 60, 60, 255),
        width=6,
    )

    draw.text(
        (55, 45),
        "Crafting",
        fill=(25, 25, 25, 255),
    )

    inicio_x = 120
    inicio_y = 145

    slot = 110
    separacion = 8

    # ========================================================
    # SIEMPRE 3x3
    # ========================================================

    for fila in range(3):
        for columna in range(3):

            x = (
                inicio_x
                + columna
                * (slot + separacion)
            )

            y = (
                inicio_y
                + fila
                * (slot + separacion)
            )

            _dibujar_slot(
                imagen,
                x,
                y,
                slot,
            )

    matriz = receta.get(
        "matriz"
    )

    if matriz:

        alto_matriz = len(matriz)

        ancho_matriz = max(
            (
                len(fila)
                for fila in matriz
            ),
            default=1,
        )

        offset_x = (
            (3 - ancho_matriz)
            * (slot + separacion)
            // 2
        )

        offset_y = (
            (3 - alto_matriz)
            * (slot + separacion)
            // 2
        )

        for fila, datos_fila in enumerate(
            matriz
        ):
            for columna, ingrediente in enumerate(
                datos_fila
            ):

                if not ingrediente:
                    continue

                x = (
                    inicio_x
                    + offset_x
                    + columna
                    * (slot + separacion)
                )

                y = (
                    inicio_y
                    + offset_y
                    + fila
                    * (slot + separacion)
                )

                _dibujar_item(
                    imagen,
                    ingrediente,
                    x,
                    y,
                    slot,
                )

    else:

        ingredientes = receta.get(
            "ingredientes",
            [],
        )

        for indice, ingrediente in enumerate(
            ingredientes[:9]
        ):

            fila = indice // 3
            columna = indice % 3

            x = (
                inicio_x
                + columna
                * (slot + separacion)
            )

            y = (
                inicio_y
                + fila
                * (slot + separacion)
            )

            _dibujar_item(
                imagen,
                ingrediente,
                x,
                y,
                slot,
            )

    # ========================================================
    # FLECHA
    # ========================================================

    _dibujar_flecha(
        draw,
        550,
        285,
    )

    # ========================================================
    # SALIDA
    # ========================================================

    salida_x = 820
    salida_y = 210

    _dibujar_slot(
        imagen,
        salida_x,
        salida_y,
        180,
    )

    _dibujar_item(
        imagen,
        salida,
        salida_x,
        salida_y,
        180,
    )

    draw.text(
        (
            820,
            430,
        ),
        nombre_salida,
        fill=(25, 25, 25, 255),
    )

    return imagen


# ============================================================
# PROCESOS
# ============================================================

def _dibujar_proceso(
    receta,
    salida,
    nombre_salida,
):
    ancho = 1100
    alto = 650

    imagen = Image.new(
        "RGBA",
        (
            ancho,
            alto,
        ),
        (198, 198, 198, 255),
    )

    draw = ImageDraw.Draw(imagen)

    proceso = receta.get(
        "proceso",
        "horno",
    )

    nombres = {
        "horno": "Furnace",
        "alto_horno": "Blast Furnace",
        "ahumador": "Smoker",
        "fogata": "Campfire",
    }

    draw.text(
        (
            50,
            40,
        ),
        nombres.get(
            proceso,
            "Furnace",
        ),
        fill=(25, 25, 25, 255),
    )

    izquierda_x = 180
    izquierda_y = 190

    derecha_x = 700
    derecha_y = 190

    _dibujar_slot(
        imagen,
        izquierda_x,
        izquierda_y,
        180,
    )

    _dibujar_item(
        imagen,
        receta.get(
            "ingrediente"
        ),
        izquierda_x,
        izquierda_y,
        180,
    )

    _dibujar_flecha(
        draw,
        450,
        250,
    )

    _dibujar_slot(
        imagen,
        derecha_x,
        derecha_y,
        180,
    )

    _dibujar_item(
        imagen,
        salida,
        derecha_x,
        derecha_y,
        180,
    )

    draw.text(
        (
            700,
            410,
        ),
        nombre_salida,
        fill=(25, 25, 25, 255),
    )

    return imagen


# ============================================================
# PUNTO DE ENTRADA
# ============================================================

def generar_imagen_crafteo(
    item,
    receta,
    nombre_salida,
):
    salida = item.get(
        "identifier",
        "",
    )

    if not salida:
        salida = item.get(
            "name",
            "",
        )

    tipo = receta.get(
        "tipo"
    )

    if tipo == "crafting":
        imagen = _dibujar_crafting(
            receta,
            salida,
            nombre_salida,
        )

    elif tipo == "proceso":
        imagen = _dibujar_proceso(
            receta,
            salida,
            nombre_salida,
        )

    else:
        return None

    buffer = BytesIO()

    imagen.save(
        buffer,
        format="PNG",
    )

    buffer.seek(0)

    buffer.name = "recipe.png"

    return buffer
