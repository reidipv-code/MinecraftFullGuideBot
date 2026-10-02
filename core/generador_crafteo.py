import zipfile
from io import BytesIO
from pathlib import Path

from PIL import Image, ImageDraw

from datos.idiomas import obtener_client_jar


CACHE_DIR = Path("/tmp/minecraft_fullguide_render")
CACHE_DIR.mkdir(parents=True, exist_ok=True)


def _cargar_asset(ruta):
    jar = obtener_client_jar()

    with zipfile.ZipFile(jar, "r") as zf:
        if ruta not in zf.namelist():
            return None

        return zf.read(ruta)


def _cargar_textura_item(identifier):
    if not identifier:
        return None

    identifier = str(identifier)

    if identifier.startswith("#"):
        identifier = identifier[1:]

    rutas = [
        f"assets/minecraft/textures/item/{identifier}.png",
        f"assets/minecraft/textures/block/{identifier}.png",
    ]

    for ruta in rutas:
        data = _cargar_asset(ruta)

        if data:
            try:
                return Image.open(
                    BytesIO(data)
                ).convert("RGBA")

            except Exception:
                pass

    return None


def _cargar_gui(nombre):
    rutas = [
        f"assets/minecraft/textures/gui/container/{nombre}.png",
        f"assets/minecraft/textures/gui/{nombre}.png",
    ]

    for ruta in rutas:
        data = _cargar_asset(ruta)

        if data:
            try:
                return Image.open(
                    BytesIO(data)
                ).convert("RGBA")

            except Exception:
                pass

    return None


def _textura(identifier):
    return _cargar_textura_item(identifier)


def _dibujar_item(
    canvas,
    identifier,
    x,
    y,
    tamano=96,
):
    textura = _textura(identifier)

    if textura is None:
        return

    textura.thumbnail(
        (
            int(tamano * 0.82),
            int(tamano * 0.82),
        ),
        Image.Resampling.NEAREST,
    )

    px = x + (tamano - textura.width) // 2
    py = y + (tamano - textura.height) // 2

    canvas.alpha_composite(
        textura,
        (
            px,
            py,
        ),
    )


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
        fill=(35, 35, 35, 255),
        outline=(10, 10, 10, 255),
        width=4,
    )

    draw.rectangle(
        [
            x + 5,
            y + 5,
            x + tamano - 5,
            y + tamano - 5,
        ],
        outline=(90, 90, 90, 255),
        width=2,
    )


def _dibujar_crafting(
    receta,
    salida,
    nombre_salida,
):
    ancho = 1200
    alto = 760

    imagen = Image.new(
        "RGBA",
        (ancho, alto),
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
        outline=(70, 70, 70, 255),
        width=6,
    )

    draw.text(
        (55, 45),
        "Crafting",
        fill=(25, 25, 25, 255),
    )

    inicio_x = 150
    inicio_y = 160

    slot = 110
    separacion = 8

    matriz = receta.get("matriz")

    # ========================================================
    # MATRIZ 3x3 SIEMPRE
    # ========================================================

    for fila in range(3):
        for columna in range(3):
            x = (
                inicio_x
                + columna * (slot + separacion)
            )

            y = (
                inicio_y
                + fila * (slot + separacion)
            )

            _dibujar_slot(
                imagen,
                x,
                y,
                slot,
            )

    if matriz:
        alto_matriz = len(matriz)

        ancho_matriz = max(
            len(fila)
            for fila in matriz
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
                + columna * (slot + separacion)
            )

            y = (
                inicio_y
                + fila * (slot + separacion)
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

    flecha_x = 590
    flecha_y = 285

    draw.polygon(
        [
            (flecha_x, flecha_y),
            (flecha_x + 120, flecha_y),
            (flecha_x + 120, flecha_y - 25),
            (flecha_x + 175, flecha_y + 45),
            (flecha_x + 120, flecha_y + 115),
            (flecha_x + 120, flecha_y + 90),
            (flecha_x, flecha_y + 90),
        ],
        fill=(80, 80, 80, 255),
    )

    # ========================================================
    # RESULTADO
    # ========================================================

    salida_x = 830
    salida_y = 220

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
        (830, 430),
        nombre_salida,
        fill=(25, 25, 25, 255),
    )

    return imagen


def _dibujar_proceso(
    receta,
    salida,
    nombre_salida,
):
    ancho = 1100
    alto = 650

    imagen = Image.new(
        "RGBA",
        (ancho, alto),
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
        (50, 40),
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
        receta.get("ingrediente"),
        izquierda_x,
        izquierda_y,
        180,
    )

    draw.polygon(
        [
            (450, 250),
            (610, 250),
            (610, 220),
            (680, 290),
            (610, 360),
            (610, 330),
            (450, 330),
        ],
        fill=(80, 80, 80, 255),
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
        (700, 410),
        nombre_salida,
        fill=(25, 25, 25, 255),
    )

    return imagen


def generar_imagen_crafteo(
    item,
    receta,
    nombre_salida,
):
    salida = item.get(
        "identifier",
        "",
    )

    if receta.get("tipo") == "crafting":
        imagen = _dibujar_crafting(
            receta,
            salida,
            nombre_salida,
        )

    elif receta.get("tipo") == "proceso":
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
