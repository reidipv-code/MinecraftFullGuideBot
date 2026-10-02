from __future__ import annotations

import io
import json
import logging
import zipfile
from pathlib import Path
from urllib.request import Request, urlopen

from PIL import Image, ImageDraw, ImageFont


logger = logging.getLogger(__name__)


# ============================================================
# VERSION
# ============================================================

VERSION = "26.1.2"

CACHE = Path(
    "/tmp/minecraft_fullguide_assets"
)

JAR = CACHE / (
    f"client-{VERSION}.jar"
)

MANIFEST = (
    "https://piston-meta.mojang.com/"
    "mc/game/version_manifest_v2.json"
)


# ============================================================
# TAMAÑO
# ============================================================

ANCHO = 1200
ALTO = 760


# ============================================================
# DESCARGA
# ============================================================

def download(
    url,
    path,
):

    CACHE.mkdir(
        parents=True,
        exist_ok=True,
    )

    req = Request(
        url,
        headers={
            "User-Agent":
                "MinecraftFullGuideBot/2.0"
        },
    )

    with urlopen(
        req,
        timeout=90,
    ) as response:

        data = response.read()

    path.write_bytes(
        data
    )


# ============================================================
# CLIENTE VANILLA
# ============================================================

def ensure_client():

    if (
        JAR.exists()
        and JAR.stat().st_size
        > 5_000_000
    ):

        return

    req = Request(
        MANIFEST,
        headers={
            "User-Agent":
                "MinecraftFullGuideBot/2.0"
        },
    )

    with urlopen(
        req,
        timeout=40,
    ) as response:

        manifest = json.loads(
            response.read()
            .decode("utf-8")
        )

    version_url = next(

        version["url"]

        for version in manifest[
            "versions"
        ]

        if version["id"] == VERSION

    )

    req = Request(
        version_url,
        headers={
            "User-Agent":
                "MinecraftFullGuideBot/2.0"
        },
    )

    with urlopen(
        req,
        timeout=40,
    ) as response:

        meta = json.loads(
            response.read()
            .decode("utf-8")
        )

    download(
        meta["downloads"][
            "client"
        ]["url"],
        JAR,
    )


# ============================================================
# RECURSO
# ============================================================

def resource(
    path,
):

    ensure_client()

    try:

        with zipfile.ZipFile(
            JAR
        ) as archive:

            data = archive.read(
                path
            )

        return Image.open(
            io.BytesIO(data)
        ).convert(
            "RGBA"
        )

    except Exception:

        return None


# ============================================================
# TEXTURA DEL ITEM
# ============================================================

def texture(
    ident,
):

    ident = str(
        ident
    ).replace(
        "minecraft:",
        "",
    )

    # Primero textura del objeto.
    image = resource(
        "assets/minecraft/"
        f"textures/item/"
        f"{ident}.png"
    )

    if image is not None:
        return image

    # Después textura del bloque.
    return resource(
        "assets/minecraft/"
        f"textures/block/"
        f"{ident}.png"
    )


# ============================================================
# FUENTE
# ============================================================

def font(
    size,
    bold=True,
):

    paths = [

        (
            "/usr/share/fonts/"
            "truetype/dejavu/"
            "DejaVuSans-Bold.ttf"
            if bold
            else
            "/usr/share/fonts/"
            "truetype/dejavu/"
            "DejaVuSans.ttf"
        ),

        (
            "/usr/share/fonts/"
            "truetype/liberation2/"
            "LiberationSans-Bold.ttf"
            if bold
            else
            "/usr/share/fonts/"
            "truetype/liberation2/"
            "LiberationSans-Regular.ttf"
        ),

    ]

    for path in paths:

        try:

            return ImageFont.truetype(
                path,
                size,
            )

        except Exception:
            pass

    return ImageFont.load_default()


# ============================================================
# AJUSTAR TEXTURA
# ============================================================

def fit(
    image,
    size,
):

    if image is None:
        return None

    width, height = (
        image.size
    )

    scale = min(

        size / max(
            1,
            width,
        ),

        size / max(
            1,
            height,
        ),

    )

    return image.resize(

        (

            max(
                1,
                int(
                    width * scale
                ),
            ),

            max(
                1,
                int(
                    height * scale
                ),
            ),

        ),

        Image.Resampling.NEAREST,

    )


# ============================================================
# RECTÁNGULO
# ============================================================

def rounded_rectangle(
    draw,
    box,
    radius,
    fill,
    outline=None,
    width=1,
):

    draw.rounded_rectangle(

        box,

        radius=radius,

        fill=fill,

        outline=outline,

        width=width,

    )


# ============================================================
# ITEM
# ============================================================

def draw_item(
    canvas,
    ident,
    count,
    x,
    y,
    size,
):

    image = texture(
        ident
    )

    if image is not None:

        image = fit(
            image,
            int(
                size * 0.72
            ),
        )

        canvas.alpha_composite(

            image,

            (

                x
                + (
                    size
                    - image.width
                ) // 2,

                y
                + (
                    size
                    - image.height
                ) // 2,

            ),

        )

    # Cantidad.
    if count and int(
        count
    ) > 1:

        draw = ImageDraw.Draw(
            canvas
        )

        f = font(
            24
        )

        text = str(
            int(count)
        )

        box = draw.textbbox(
            (0, 0),
            text,
            font=f,
        )

        width = (
            box[2]
            - box[0]
        )

        height = (
            box[3]
            - box[1]
        )

        tx = (
            x
            + size
            - width
            - 8
        )

        ty = (
            y
            + size
            - height
            - 7
        )

        draw.text(

            (
                tx + 2,
                ty + 2,
            ),

            text,

            font=f,

            fill=(
                0,
                0,
                0,
                255,
            ),

        )

        draw.text(

            (
                tx,
                ty,
            ),

            text,

            font=f,

            fill=(
                255,
                255,
                255,
                255,
            ),

        )


# ============================================================
# SLOT
# ============================================================

def draw_slot(
    canvas,
    ident,
    count,
    x,
    y,
    size,
):

    draw = ImageDraw.Draw(
        canvas
    )

    rounded_rectangle(

        draw,

        (
            x,
            y,
            x + size,
            y + size,
        ),

        10,

        fill=(
            220,
            220,
            220,
            255,
        ),

        outline=(
            95,
            95,
            95,
            255,
        ),

        width=3,

    )

    if ident:

        draw_item(

            canvas,

            ident,

            count,

            x,
            y,
            size,

        )


# ============================================================
# FLECHA
# ============================================================

def draw_arrow(
    canvas,
    x,
    y,
):

    draw = ImageDraw.Draw(
        canvas
    )

    draw.text(

        (
            x,
            y,
        ),

        "➜",

        font=font(
            58
        ),

        fill=(
            55,
            55,
            55,
            255,
        ),

    )


# ============================================================
# MESA DE CRAFTEO 3x3
# ============================================================

def draw_crafting(
    canvas,
    recipe,
    result_id,
    result_count,
):

    draw = ImageDraw.Draw(
        canvas
    )

    draw.text(

        (
            55,
            35,
        ),

        "FABRICACIÓN",

        font=font(
            48
        ),

        fill=(
            35,
            35,
            35,
            255,
        ),

    )

    draw.text(

        (
            57,
            92,
        ),

        "Mesa de crafteo · cuadrícula 3×3",

        font=font(
            25
        ),

        fill=(
            90,
            90,
            90,
            255,
        ),

    )

    grid = (
        recipe.get(
            "patron"
        )
        or
        [
            [None, None, None],
            [None, None, None],
            [None, None, None],
        ]
    )

    slot = 125

    start_x = 115
    start_y = 165

    gap = 16

    # SIEMPRE 3x3.
    for y in range(3):

        for x in range(3):

            ident = None

            if (
                y < len(grid)
                and x < len(grid[y])
            ):

                ident = grid[y][x]

            draw_slot(

                canvas,

                ident,

                1,

                start_x
                + x * (
                    slot + gap
                ),

                start_y
                + y * (
                    slot + gap
                ),

                slot,

            )

    draw_arrow(
        canvas,
        600,
        305,
    )

    result_x = 790
    result_y = 295

    draw_slot(

        canvas,

        result_id,

        result_count,

        result_x,
        result_y,

        170,

    )

    draw.text(

        (
            775,
            485,
        ),

        "Resultado",

        font=font(
            25
        ),

        fill=(
            70,
            70,
            70,
            255,
        ),

    )


# ============================================================
# HORNO / ALTO HORNO / AHUMADOR
# ============================================================

def draw_smelting(
    canvas,
    recipe,
    result_id,
    result_count,
):

    draw = ImageDraw.Draw(
        canvas
    )

    station = (

        recipe.get(
            "estacion"
        )

        or

        recipe.get(
            "mesa"
        )

        or

        "Horno"

    )

    draw.text(

        (
            55,
            35,
        ),

        station.upper(),

        font=font(
            48
        ),

        fill=(
            35,
            35,
            35,
            255,
        ),

    )

    draw.text(

        (
            57,
            92,
        ),

        "Entrada → proceso → resultado",

        font=font(
            25
        ),

        fill=(
            90,
            90,
            90,
            255,
        ),

    )

    entrada = recipe.get(
        "entrada"
    )

    draw_slot(

        canvas,

        entrada,

        1,

        150,
        280,

        170,

    )

    # Fuego.
    draw.text(

        (
            440,
            265,
        ),

        "🔥",

        font=font(
            70
        ),

        fill=(
            255,
            100,
            20,
            255,
        ),

    )

    draw_arrow(

        canvas,

        555,
        285,

    )

    draw_slot(

        canvas,

        result_id,

        result_count,

        760,
        280,

        170,

    )

    draw.text(

        (
            145,
            480,
        ),

        "Entrada",

        font=font(
            25
        ),

        fill=(
            70,
            70,
            70,
            255,
        ),

    )

    draw.text(

        (
            755,
            475,
        ),

        "Resultado",

        font=font(
            25
        ),

        fill=(
            70,
            70,
            70,
            255,
        ),

    )


# ============================================================
# GENERAR IMAGEN
# ============================================================

def generar_imagen_crafteo(
    item,
):

    recipe = item.get(
        "receta"
    )

    if not recipe:
        return None

    try:

        canvas = Image.new(

            "RGBA",

            (
                ANCHO,
                ALTO,
            ),

            (
                242,
                242,
                242,
                255,
            ),

        )

        draw = ImageDraw.Draw(
            canvas
        )

        # Marco.
        rounded_rectangle(

            draw,

            (
                25,
                25,
                ANCHO - 25,
                ALTO - 25,
            ),

            24,

            fill=(
                250,
                250,
                250,
                255,
            ),

            outline=(
                75,
                75,
                75,
                255,
            ),

            width=4,

        )

        result_id = str(
            item.get(
                "id"
            )
            or ""
        ).replace(
            "minecraft:",
            "",
        )

        result_count = int(
            recipe.get(
                "resultado_cantidad"
            )
            or 1
        )

        if (
            recipe.get(
                "tipo"
            )
            == "smelting"
        ):

            draw_smelting(

                canvas,

                recipe,

                result_id,

                result_count,

            )

        else:

            draw_crafting(

                canvas,

                recipe,

                result_id,

                result_count,

            )

        # Pie.
        draw.text(

            (
                55,
                700,
            ),

            "Minecraft Java 26.1.2 · MinecraftFullGuideBot",

            font=font(
                20,
                False,
            ),

            fill=(
                115,
                115,
                115,
                255,
            ),

        )

        output = io.BytesIO()

        canvas.save(
            output,
            "PNG",
            optimize=True,
        )

        output.seek(0)

        output.name = (
            "crafteo.png"
        )

        return output

    except Exception:

        logger.exception(
            "Error generando imagen de receta"
        )

        return None
