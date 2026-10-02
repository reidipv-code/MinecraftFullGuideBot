import io
import urllib.request
from pathlib import Path

from PIL import Image, ImageDraw, ImageFont


# ============================================================
# MinecraftFullGuideBot
# GENERADOR DE IMÁGENES DE CRAFTEO
#
# - Siempre utiliza cuadrícula 3x3.
# - No utiliza emojis.
# - Utiliza texturas reales de Minecraft para los objetos.
# - La interfaz se genera localmente.
# - No necesita descargar la GUI de Minecraft.
# - No realiza ninguna descarga al importar el módulo.
# ============================================================


# ============================================================
# CONFIGURACIÓN
# ============================================================

ESCALA = 4

ANCHO = 176
ALTO = 166

ANCHO_FINAL = ANCHO * ESCALA
ALTO_FINAL = ALTO * ESCALA

CACHE = Path(
    "/tmp/minecraft_fullguide_assets"
)

CACHE.mkdir(
    parents=True,
    exist_ok=True,
)


# ============================================================
# TEXTURAS REALES DE MINECRAFT
# ============================================================

BASE_URL = (
    "https://raw.githubusercontent.com/"
    "InventivetalentDev/minecraft-assets/"
    "1.21.4/assets/minecraft/"
)


TEXTURAS = {
    "diamond": "textures/item/diamond.png",
    "stick": "textures/item/stick.png",

    "diamond_pickaxe":
        "textures/item/diamond_pickaxe.png",

    "diamond_sword":
        "textures/item/diamond_sword.png",

    "planks":
        "textures/block/oak_planks.png",

    "cobblestone":
        "textures/block/cobblestone.png",

    "crafting_table":
        "textures/item/crafting_table.png",

    "furnace":
        "textures/item/furnace.png",
}


# ============================================================
# POSICIONES DE LA CUADRÍCULA VANILLA
# ============================================================

GRID_X = 30
GRID_Y = 17

SLOT = 18

RESULTADO_X = 124
RESULTADO_Y = 35


# ============================================================
# FUENTES
# ============================================================

FUENTES = [
    "/usr/share/fonts/truetype/dejavu/"
    "DejaVuSans-Bold.ttf",

    "/usr/share/fonts/truetype/dejavu/"
    "DejaVuSans.ttf",

    "/usr/share/fonts/truetype/liberation2/"
    "LiberationSans-Bold.ttf",

    "/usr/share/fonts/truetype/liberation2/"
    "LiberationSans-Regular.ttf",
]


def obtener_fuente(tamano):
    for ruta in FUENTES:
        try:
            return ImageFont.truetype(
                ruta,
                tamano,
            )
        except Exception:
            continue

    return ImageFont.load_default()


# ============================================================
# DESCARGA DE TEXTURAS
# ============================================================

def descargar_textura(
    identificador,
):
    ruta = TEXTURAS.get(
        identificador
    )

    if ruta is None:
        return None

    archivo = CACHE / (
        identificador + ".png"
    )

    # --------------------------------------------------------
    # CACHE
    # --------------------------------------------------------

    if (
        archivo.exists()
        and archivo.stat().st_size > 0
    ):
        try:
            return Image.open(
                archivo
            ).convert("RGBA")
        except Exception:
            try:
                archivo.unlink()
            except Exception:
                pass

    # --------------------------------------------------------
    # DESCARGA
    # --------------------------------------------------------

    url = BASE_URL + ruta

    try:
        request = urllib.request.Request(
            url,
            headers={
                "User-Agent":
                    "MinecraftFullGuideBot/1.0"
            },
        )

        with urllib.request.urlopen(
            request,
            timeout=15,
        ) as respuesta:

            datos = respuesta.read()

        archivo.write_bytes(
            datos
        )

        return Image.open(
            io.BytesIO(datos)
        ).convert("RGBA")

    except Exception as error:

        print(
            "[MinecraftFullGuideBot] "
            f"No se pudo descargar textura "
            f"{identificador}: {error}"
        )

        return None


# ============================================================
# ESCALAR TEXTURA
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
# DIBUJAR TEXTURA
# ============================================================

def dibujar_item(
    imagen,
    identificador,
    x,
    y,
):
    textura = descargar_textura(
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
    if cantidad is None:
        return

    try:
        cantidad = int(cantidad)
    except Exception:
        return

    if cantidad <= 1:
        return

    draw = ImageDraw.Draw(
        imagen
    )

    fuente = obtener_fuente(
        9 * ESCALA
    )

    texto = str(cantidad)

    px = (
        x + 17 * ESCALA
    )

    py = (
        y + 17 * ESCALA
    )

    # Sombra
    draw.text(
        (
            px + 2,
            py + 2,
        ),
        texto,
        font=fuente,
        fill=(
            0,
            0,
            0,
            255,
        ),
        anchor="rb",
    )

    # Número
    draw.text(
        (
            px,
            py,
        ),
        texto,
        font=fuente,
        fill=(
            255,
            255,
            255,
            255,
        ),
        anchor="rb",
    )


# ============================================================
# PATRÓN -> SIEMPRE 3x3
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
                min(
                    len(fila),
                    3,
                ),
            )

    if ancho <= 0:
        return resultado

    offset_x = (
        3 - ancho
    ) // 2

    offset_y = (
        3 - alto
    ) // 2

    for fila in range(alto):

        datos = patron[fila]

        if not datos:
            continue

        for columna in range(
            min(
                len(datos),
                3,
            )
        ):
            resultado[
                offset_y + fila
            ][
                offset_x + columna
            ] = datos[columna]

    return resultado


# ============================================================
# CREAR SLOT VANILLA
# ============================================================

def dibujar_slot(
    draw,
    x,
    y,
    tamano=SLOT,
):
    x *= ESCALA
    y *= ESCALA

    ancho = tamano * ESCALA

    # Sombra exterior
    draw.rectangle(
        (
            x,
            y,
            x + ancho - 1,
            y + ancho - 1,
        ),
        fill=(
            55,
            55,
            55,
            255,
        ),
    )

    # Borde superior/izquierdo
    draw.line(
        (
            x,
            y,
            x + ancho - 1,
            y,
        ),
        fill=(
            35,
            35,
            35,
            255,
        ),
        width=ESCALA,
    )

    draw.line(
        (
            x,
            y,
            x,
            y + ancho - 1,
        ),
        fill=(
            35,
            35,
            35,
            255,
        ),
        width=ESCALA,
    )

    # Interior
    margen = 2 * ESCALA

    draw.rectangle(
        (
            x + margen,
            y + margen,
            x + ancho - margen - 1,
            y + ancho - margen - 1,
        ),
        fill=(
            139,
            139,
            139,
            255,
        ),
    )

    # Luz interior
    draw.line(
        (
            x + margen,
            y + margen,
            x + ancho - margen - 1,
            y + margen,
        ),
        fill=(
            198,
            198,
            198,
            255,
        ),
        width=ESCALA,
    )

    draw.line(
        (
            x + margen,
            y + margen,
            x + margen,
            y + ancho - margen - 1,
        ),
        fill=(
            198,
            198,
            198,
            255,
        ),
        width=ESCALA,
    )


# ============================================================
# FLECHA
# ============================================================

def dibujar_flecha(
    draw,
):
    # La flecha de la interfaz de fabricación.
    x = 105 * ESCALA
    y = 35 * ESCALA

    # Línea horizontal
    draw.rectangle(
        (
            x,
            y + 5 * ESCALA,
            x + 18 * ESCALA,
            y + 8 * ESCALA,
        ),
        fill=(
            80,
            80,
            80,
            255,
        ),
    )

    # Punta
    draw.polygon(
        [
            (
                x + 18 * ESCALA,
                y + 2 * ESCALA,
            ),
            (
                x + 25 * ESCALA,
                y + 7 * ESCALA,
            ),
            (
                x + 18 * ESCALA,
                y + 12 * ESCALA,
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
# INTERFAZ VANILLA GENERADA LOCALMENTE
# ============================================================

def crear_interfaz():
    imagen = Image.new(
        "RGBA",
        (
            ANCHO_FINAL,
            ALTO_FINAL,
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

    # --------------------------------------------------------
    # Borde exterior
    # --------------------------------------------------------

    draw.rectangle(
        (
            0,
            0,
            ANCHO_FINAL - 1,
            ALTO_FINAL - 1,
        ),
        fill=(
            198,
            198,
            198,
            255,
        ),
        outline=(
            40,
            40,
            40,
            255,
        ),
        width=ESCALA,
    )

    # --------------------------------------------------------
    # Zona interior
    # --------------------------------------------------------

    margen = 3 * ESCALA

    draw.rectangle(
        (
            margen,
            margen,
            ANCHO_FINAL - margen - 1,
            ALTO_FINAL - margen - 1,
        ),
        fill=(
            139,
            139,
            139,
            255,
        ),
    )

    # --------------------------------------------------------
    # Sombra inferior/derecha
    # --------------------------------------------------------

    draw.line(
        (
            margen,
            ALTO_FINAL - 5 * ESCALA,
            ANCHO_FINAL - 5 * ESCALA,
            ALTO_FINAL - 5 * ESCALA,
        ),
        fill=(
            90,
            90,
            90,
            255,
        ),
        width=ESCALA,
    )

    draw.line(
        (
            ANCHO_FINAL - 5 * ESCALA,
            margen,
            ANCHO_FINAL - 5 * ESCALA,
            ALTO_FINAL - 5 * ESCALA,
        ),
        fill=(
            90,
            90,
            90,
            255,
        ),
        width=ESCALA,
    )

    # --------------------------------------------------------
    # Slots 3x3
    # --------------------------------------------------------

    for fila in range(3):

        for columna in range(3):

            x = (
                GRID_X
                + columna * SLOT
            )

            y = (
                GRID_Y
                + fila * SLOT
            )

            dibujar_slot(
                draw,
                x,
                y,
            )

    # --------------------------------------------------------
    # Slot de resultado
    # --------------------------------------------------------

    dibujar_slot(
        draw,
        RESULTADO_X,
        RESULTADO_Y,
    )

    # --------------------------------------------------------
    # Flecha
    # --------------------------------------------------------

    dibujar_flecha(
        draw
    )

    return imagen


# ============================================================
# TÍTULO SUPERIOR
# ============================================================

def agregar_titulo(
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
            28,
            28,
            28,
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

    fuente_titulo = obtener_fuente(
        25
    )

    fuente_nombre = obtener_fuente(
        18
    )

    nombre = item.get(
        "nombre",
        "Objeto",
    )

    # --------------------------------------------------------
    # Título
    # --------------------------------------------------------

    draw.text(
        (
            22,
            17,
        ),
        "FABRICACIÓN",
        font=fuente_titulo,
        fill=(
            0,
            0,
            0,
            255,
        ),
    )

    draw.text(
        (
            20,
            15,
        ),
        "FABRICACIÓN",
        font=fuente_titulo,
        fill=(
            255,
            255,
            255,
            255,
        ),
    )

    # --------------------------------------------------------
    # Nombre
    # --------------------------------------------------------

    draw.text(
        (
            21,
            58,
        ),
        nombre,
        font=fuente_nombre,
        fill=(
            0,
            0,
            0,
            255,
        ),
    )

    draw.text(
        (
            20,
            56,
        ),
        nombre,
        font=fuente_nombre,
        fill=(
            220,
            220,
            220,
            255,
        ),
    )

    return resultado


# ============================================================
# FUNCIÓN PRINCIPAL
# ============================================================

def generar_imagen_crafteo(
    item,
):
    """
    Genera la imagen de fabricación de un objeto.

    Devuelve:
        BytesIO con PNG
        o None si no existe receta.
    """

    if not item:
        return None

    receta = item.get(
        "receta"
    )

    if not receta:
        return None

    patron_original = receta.get(
        "patron"
    )

    if not patron_original:
        return None

    # --------------------------------------------------------
    # NORMALIZAR SIEMPRE A 3x3
    # --------------------------------------------------------

    patron = normalizar_patron(
        patron_original
    )

    # --------------------------------------------------------
    # CREAR INTERFAZ
    # --------------------------------------------------------

    imagen = crear_interfaz()

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

    resultado = receta.get(
        "resultado",
        item.get(
            "identificador"
        ),
    )

    x_resultado = (
        RESULTADO_X * ESCALA
    )

    y_resultado = (
        RESULTADO_Y * ESCALA
    )

    dibujar_item(
        imagen,
        resultado,
        x_resultado,
        y_resultado,
    )

    # --------------------------------------------------------
    # CANTIDAD
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
    # TÍTULO
    # --------------------------------------------------------

    imagen = agregar_titulo(
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

    buffer.name = (
        "crafteo_minecraft.png"
    )

    return buffer
