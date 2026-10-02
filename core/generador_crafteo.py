# core/generador_crafteo.py

import json
import zipfile
from io import BytesIO
from pathlib import Path

from PIL import Image, ImageDraw

from datos.idiomas import obtener_client_jar
from datos.items import obtener_item_representativo


CACHE_DIR = Path(
    "/tmp/minecraft_fullguide_render"
)

CACHE_DIR.mkdir(
    parents=True,
    exist_ok=True,
)

_MODELOS_CACHE = {}
_TEXTURAS_CACHE = {}


# ============================================================
# ASSETS
# ============================================================

def _leer_json_asset(ruta):
    jar = obtener_client_jar()

    try:

        with zipfile.ZipFile(
            jar,
            "r",
        ) as zf:

            if ruta not in zf.namelist():
                return None

            contenido = zf.read(
                ruta
            )

        return json.loads(
            contenido.decode(
                "utf-8"
            )
        )

    except Exception:
        return None


def _leer_bytes_asset(ruta):
    jar = obtener_client_jar()

    try:

        with zipfile.ZipFile(
            jar,
            "r",
        ) as zf:

            if ruta not in zf.namelist():
                return None

            return zf.read(
                ruta
            )

    except Exception:
        return None


# ============================================================
# MODELOS
# ============================================================

def _normalizar_modelo(modelo):

    if not modelo:
        return None

    modelo = str(
        modelo
    )

    if modelo.startswith(
        "minecraft:"
    ):
        modelo = modelo.split(
            ":",
            1,
        )[1]

    if modelo.endswith(
        ".json"
    ):
        modelo = modelo[:-5]

    return modelo


def _cargar_modelo(modelo):

    modelo = _normalizar_modelo(
        modelo
    )

    if not modelo:
        return None

    if modelo in _MODELOS_CACHE:
        return _MODELOS_CACHE[
            modelo
        ]

    ruta = (
        "assets/minecraft/models/"
        f"{modelo}.json"
    )

    datos = _leer_json_asset(
        ruta
    )

    _MODELOS_CACHE[
        modelo
    ] = datos

    return datos


def _resolver_modelo_item(
    identifier
):

    identifier = str(
        identifier
    )

    if identifier.startswith(
        "minecraft:"
    ):
        identifier = identifier.split(
            ":",
            1,
        )[1]

    ruta = (
        "assets/minecraft/items/"
        f"{identifier}.json"
    )

    datos = _leer_json_asset(
        ruta
    )

    if datos:

        modelo = datos.get(
            "model"
        )

        if isinstance(
            modelo,
            str,
        ):
            return modelo

        if isinstance(
            modelo,
            dict,
        ):

            return (
                modelo.get(
                    "model"
                )
                or modelo.get(
                    "base"
                )
            )

    # Compatibilidad con modelos
    # antiguos/directos
    return (
        f"item/{identifier}"
    )


# ============================================================
# TEXTURAS
# ============================================================

def _normalizar_textura(
    textura
):

    if not textura:
        return None

    textura = str(
        textura
    )

    if textura.startswith(
        "minecraft:"
    ):
        textura = textura.split(
            ":",
            1,
        )[1]

    if textura.startswith(
        "textures/"
    ):
        textura = textura[9:]

    if textura.endswith(
        ".png"
    ):
        textura = textura[:-4]

    return textura


def _buscar_textura(
    textura
):

    textura = _normalizar_textura(
        textura
    )

    if not textura:
        return None

    rutas = [
        (
            "assets/minecraft/textures/"
            f"{textura}.png"
        ),
    ]

    for ruta in rutas:

        datos = _leer_bytes_asset(
            ruta
        )

        if datos:
            try:
                return Image.open(
                    BytesIO(datos)
                ).convert(
                    "RGBA"
                )
            except Exception:
                pass

    return None


def _resolver_textura_desde_modelo(
    modelo,
    visitados=None,
):

    if not modelo:
        return None

    modelo = _normalizar_modelo(
        modelo
    )

    if visitados is None:
        visitados = set()

    if modelo in visitados:
        return None

    visitados.add(
        modelo
    )

    datos = _cargar_modelo(
        modelo
    )

    if not datos:
        return None

    texturas = datos.get(
        "textures",
        {},
    )

    # Prioridad para iconos/items
    prioridades = [
        "layer0",
        "all",
        "texture",
        "side",
        "front",
        "particle",
    ]

    for clave in prioridades:

        valor = texturas.get(
            clave
        )

        if valor:

            textura = _resolver_referencia_textura(
                valor,
                texturas,
                visitados,
            )

            if textura:
                return textura

    # Buscar cualquier textura
    for valor in texturas.values():

        textura = _resolver_referencia_textura(
            valor,
            texturas,
            visitados,
        )

        if textura:
            return textura

    parent = datos.get(
        "parent"
    )

    if parent:

        return _resolver_textura_desde_modelo(
            parent,
            visitados,
        )

    return None


def _resolver_referencia_textura(
    referencia,
    texturas,
    visitados,
):

    if not referencia:
        return None

    referencia = str(
        referencia
    )

    if referencia.startswith(
        "#"
    ):

        clave = referencia[1:]

        siguiente = texturas.get(
            clave
        )

        if siguiente and siguiente != referencia:

            return _resolver_referencia_textura(
                siguiente,
                texturas,
                visitados,
            )

        return None

    return _buscar_textura(
        referencia
    )


def _cargar_textura_item(
    identifier
):

    if not identifier:
        return None

    identifier = str(
        identifier
    )

    if identifier.startswith(
        "#"
    ):
        identifier = (
            obtener_item_representativo(
                identifier
            )
        )

        if not identifier:
            return None

    identifier = identifier.split(
        ":",
        1,
    )[-1]

    if identifier in _TEXTURAS_CACHE:

        textura = _TEXTURAS_CACHE[
            identifier
        ]

        return (
            textura.copy()
            if textura
            else None
        )

    modelo = _resolver_modelo_item(
        identifier
    )

    textura = _resolver_textura_desde_modelo(
        modelo
    )

    # Fallback directo
    if textura is None:

        textura = _buscar_textura(
            f"item/{identifier}"
        )

    if textura is None:

        textura = _buscar_textura(
            f"block/{identifier}"
        )

    _TEXTURAS_CACHE[
        identifier
    ] = textura

    return (
        textura.copy()
        if textura
        else None
    )


# ============================================================
# PIXEL ART
# ============================================================

def _escalar_pixel_art(
    textura,
    tamano,
):

    textura = textura.convert(
        "RGBA"
    )

    ancho, alto = textura.size

    escala = min(
        tamano / ancho,
        tamano / alto,
    )

    nuevo_ancho = max(
        1,
        int(
            ancho * escala
        ),
    )

    nuevo_alto = max(
        1,
        int(
            alto * escala
        ),
    )

    return textura.resize(
        (
            nuevo_ancho,
            nuevo_alto,
        ),
        Image.Resampling.NEAREST,
    )


# ============================================================
# ITEM
# ============================================================

def _dibujar_item(
    canvas,
    identifier,
    x,
    y,
    tamano=96,
):

    if not identifier:
        return False

    textura = _cargar_textura_item(
        identifier
    )

    if textura is None:
        return False

    textura = _escalar_pixel_art(
        textura,
        int(
            tamano * 0.82
        ),
    )

    px = (
        x
        + (
            tamano
            - textura.width
        )
        // 2
    )

    py = (
        y
        + (
            tamano
            - textura.height
        )
        // 2
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

    draw = ImageDraw.Draw(
        canvas
    )

    # borde exterior
    draw.rectangle(
        [
            x,
            y,
            x + tamano,
            y + tamano,
        ],
        fill=(
            60,
            60,
            60,
            255,
        ),
    )

    # interior
    draw.rectangle(
        [
            x + 4,
            y + 4,
            x + tamano - 4,
            y + tamano - 4,
        ],
        fill=(
            139,
            139,
            139,
            255,
        ),
        outline=(
            210,
            210,
            210,
            255,
        ),
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

    draw.rectangle(
        [
            x,
            y + 30,
            x + 110,
            y + 60,
        ],
        fill=(
            80,
            80,
            80,
            255,
        ),
    )

    draw.polygon(
        [
            (
                x + 100,
                y,
            ),
            (
                x + 180,
                y + 45,
            ),
            (
                x + 100,
                y + 90,
            ),
        ],
        fill=(
            80,
            80,
            80,
            255,
        ),
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
        (
            198,
            198,
            198,
            255,
        ),
    )

    draw = ImageDraw.Draw(
        imagen
    )

    draw.rectangle(
        [
            0,
            0,
            ancho - 1,
            alto - 1,
        ],
        outline=(
            50,
            50,
            50,
            255,
        ),
        width=6,
    )

    draw.text(
        (
            55,
            45,
        ),
        "Crafting",
        fill=(
            25,
            25,
            25,
            255,
        ),
    )

    inicio_x = 100
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
                * (
                    slot
                    + separacion
                )
            )

            y = (
                inicio_y
                + fila
                * (
                    slot
                    + separacion
                )
            )

            _dibujar_slot(
                imagen,
                x,
                y,
                slot,
            )

    # ========================================================
    # RECETA SHAPED
    # ========================================================

    matriz = receta.get(
        "matriz"
    )

    if matriz:

        alto_matriz = len(
            matriz
        )

        ancho_matriz = max(
            (
                len(fila)
                for fila in matriz
            ),
            default=1,
        )

        offset_x = (
            (
                3
                - ancho_matriz
            )
            * (
                slot
                + separacion
            )
            // 2
        )

        offset_y = (
            (
                3
                - alto_matriz
            )
            * (
                slot
                + separacion
            )
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
                    * (
                        slot
                        + separacion
                    )
                )

                y = (
                    inicio_y
                    + offset_y
                    + fila
                    * (
                        slot
                        + separacion
                    )
                )

                _dibujar_item(
                    imagen,
                    ingrediente,
                    x,
                    y,
                    slot,
                )

    # ========================================================
    # RECETA SHAPELESS
    # ========================================================

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
                * (
                    slot
                    + separacion
                )
            )

            y = (
                inicio_y
                + fila
                * (
                    slot
                    + separacion
                )
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
        535,
        270,
    )

    # ========================================================
    # SALIDA
    # ========================================================

    salida_x = 825
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
            825,
            420,
        ),
        nombre_salida,
        fill=(
            25,
            25,
            25,
            255,
        ),
    )

    cantidad = receta.get(
        "cantidad",
        1,
    )

    if cantidad > 1:

        draw.text(
            (
                825,
                455,
            ),
            f"x{cantidad}",
            fill=(
                25,
                25,
                25,
                255,
            ),
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
        (
            198,
            198,
            198,
            255,
        ),
    )

    draw = ImageDraw.Draw(
        imagen
    )

    proceso = receta.get(
        "proceso",
        "horno",
    )

    nombres = {
        "horno": "Horno",
        "alto_horno": "Alto horno",
        "ahumador": "Ahumador",
        "fogata": "Fogata",
    }

    draw.text(
        (
            50,
            40,
        ),
        nombres.get(
            proceso,
            "Horno",
        ),
        fill=(
            25,
            25,
            25,
            255,
        ),
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
        fill=(
            25,
            25,
            25,
            255,
        ),
    )

    cantidad = receta.get(
        "cantidad",
        1,
    )

    if cantidad > 1:

        draw.text(
            (
                700,
                445,
            ),
            f"x{cantidad}",
            fill=(
                25,
                25,
                25,
                255,
            ),
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

    buffer.name = (
        "minecraft_recipe.png"
    )

    return buffer
