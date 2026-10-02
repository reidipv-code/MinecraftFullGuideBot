import io
import urllib.request
from pathlib import Path

from PIL import Image, ImageDraw


# ============================================================
# CONFIGURACIÓN
# ============================================================

ESCALA = 5

SLOT = 18
SEPARACION = 2

GRID_X = 12
GRID_Y = 16

RESULTADO_X = 100
RESULTADO_Y = 34

ANCHO = 142
ALTO = 90

CACHE = Path("/tmp/minecraft_fullguide_assets")
CACHE.mkdir(parents=True, exist_ok=True)

BASE_URL = (
    "https://raw.githubusercontent.com/"
    "InventivetalentDev/minecraft-assets/"
    "1.21.4/assets/minecraft/"
)


# ============================================================
# TEXTURAS REALES
# ============================================================

TEXTURAS = {
    "diamond": "textures/item/diamond.png",
    "stick": "textures/item/stick.png",

    "diamond_sword":
        "textures/item/diamond_sword.png",

    "diamond_pickaxe":
        "textures/item/diamond_pickaxe.png",

    "crafting_table":
        "textures/block/crafting_table_front.png",

    "furnace":
        "textures/block/furnace_front.png",

    "planks":
        "textures/block/oak_planks.png",

    "cobblestone":
        "textures/block/cobblestone.png",
}


# ============================================================
# CACHE DE TEXTURAS
# ============================================================

def cargar_textura(identificador):
    ruta = TEXTURAS.get(identificador)

    if ruta is None:
        return None

    archivo = CACHE / f"{identificador}.png"

    # --------------------------------------------------------
    # CACHE LOCAL
    # --------------------------------------------------------

    if archivo.exists():
        try:
            return Image.open(archivo).convert("RGBA")
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
        ) as response:
            datos = response.read()

        archivo.write_bytes(datos)

        return Image.open(
            io.BytesIO(datos)
        ).convert("RGBA")

    except Exception as error:
        print(
            "[MinecraftFullGuideBot] "
            f"No se pudo cargar textura "
            f"{identificador}: {error}"
        )

        return None


# ============================================================
# DIBUJAR SLOT
# ============================================================

def dibujar_slot(draw, x, y):
    s = SLOT * ESCALA

    x *= ESCALA
    y *= ESCALA

    # Sombra exterior
    draw.rectangle(
        (
            x,
            y,
            x + s - 1,
            y + s - 1,
        ),
        fill=(55, 55, 55, 255),
    )

    # Borde superior
    draw.rectangle(
        (
            x + ESCALA,
            y + ESCALA,
            x + s - ESCALA - 1,
            y + 2 * ESCALA - 1,
        ),
        fill=(198, 198, 198, 255),
    )

    # Borde izquierdo
    draw.rectangle(
        (
            x + ESCALA,
            y + ESCALA,
            x + 2 * ESCALA - 1,
            y + s - ESCALA - 1,
        ),
        fill=(198, 198, 198, 255),
    )

    # Interior
    draw.rectangle(
        (
            x + 2 * ESCALA,
            y + 2 * ESCALA,
            x + s - 2 * ESCALA - 1,
            y + s - 2 * ESCALA - 1,
        ),
        fill=(139, 139, 139, 255),
    )

    # Sombra inferior
    draw.rectangle(
        (
            x + 2 * ESCALA,
            y + s - 2 * ESCALA,
            x + s - 2 * ESCALA - 1,
            y + s - ESCALA - 1,
        ),
        fill=(85, 85, 85, 255),
    )

    # Sombra derecha
    draw.rectangle(
        (
            x + s - 2 * ESCALA,
            y + 2 * ESCALA,
            x + s - ESCALA - 1,
            y + s - ESCALA - 1,
        ),
        fill=(85, 85, 85, 255),
    )


# ============================================================
# DIBUJAR TEXTURA
# ============================================================

def dibujar_textura(
    imagen,
    identificador,
    x,
    y,
):
    textura = cargar_textura(identificador)

    if textura is None:
        return False

    textura = textura.resize(
        (
            16 * ESCALA,
            16 * ESCALA,
        ),
        Image.Resampling.NEAREST,
    )

    imagen.alpha_composite(
        textura,
        (
            int(x * ESCALA + ESCALA),
            int(y * ESCALA + ESCALA),
        ),
    )

    return True


# ============================================================
# PATRÓN 3x3
# ============================================================

def normalizar_patron(patron):
    resultado = [
        [None, None, None],
        [None, None, None],
        [None, None, None],
    ]

    if not patron:
        return resultado

    alto = min(len(patron), 3)

    ancho_real = 0

    for fila in patron[:3]:
        if fila:
            ancho_real = max(
                ancho_real,
                min(len(fila), 3),
            )

    if ancho_real == 0:
        return resultado

    # Centrar recetas pequeñas dentro del 3x3
    offset_x = (3 - ancho_real) // 2
    offset_y = (3 - alto) // 2

    for fila in range(alto):
        datos = patron[fila]

        if not datos:
            continue

        for columna in range(
            min(len(datos), 3)
        ):
            resultado[
                offset_y + fila
            ][
                offset_x + columna
            ] = datos[columna]

    return resultado


# ============================================================
# FLECHA
# ============================================================

def dibujar_flecha(draw):
    # Posición en píxeles Minecraft
    x = 72
    y = 39

    # Línea
    draw.rectangle(
        (
            x * ESCALA,
            (y + 4) * ESCALA,
            (x + 20) * ESCALA,
            (y + 7) * ESCALA,
        ),
        fill=(85, 85, 85, 255),
    )

    # Punta
    draw.polygon(
        [
            (
                (x + 20) * ESCALA,
                (y + 1) * ESCALA,
            ),
            (
                (x + 28) * ESCALA,
                (y + 5) * ESCALA,
            ),
            (
                (x + 20) * ESCALA,
                (y + 10) * ESCALA,
            ),
        ],
        fill=(85, 85, 85, 255),
    )


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

    draw = ImageDraw.Draw(imagen)

    # Fuente pixelada simple usando rectángulos
    # para mantener el aspecto Minecraft.
    texto = str(cantidad)

    # Para cantidades normales de Minecraft.
    # Se dibuja blanco con sombra.
    try:
        from PIL import ImageFont

        fuente = ImageFont.truetype(
            "/usr/share/fonts/truetype/"
            "dejavu/DejaVuSans-Bold.ttf",
            9 * ESCALA,
        )
    except Exception:
        fuente = ImageFont.load_default()

    px = (x + 16) * ESCALA
    py = (y + 16) * ESCALA

    draw.text(
        (
            px + ESCALA,
            py + ESCALA,
        ),
        texto,
        font=fuente,
        fill=(0, 0, 0, 255),
        anchor="rb",
    )

    draw.text(
        (
            px,
            py,
        ),
        texto,
        font=fuente,
        fill=(255, 255, 255, 255),
        anchor="rb",
    )


# ============================================================
# INTERFAZ
# ============================================================

def crear_interfaz():
    imagen = Image.new(
        "RGBA",
        (
            ANCHO * ESCALA,
            ALTO * ESCALA,
        ),
        (198, 198, 198, 255),
    )

    draw = ImageDraw.Draw(imagen)

    ancho = ANCHO * ESCALA
    alto = ALTO * ESCALA

    # --------------------------------------------------------
    # FONDO VANILLA
    # --------------------------------------------------------

    draw.rectangle(
        (
            0,
            0,
            ancho - 1,
            alto - 1,
        ),
        fill=(198, 198, 198, 255),
    )

    # Borde oscuro
    draw.rectangle(
        (
            0,
            0,
            ancho - 1,
            alto - 1,
        ),
        outline=(55, 55, 55, 255),
        width=ESCALA,
    )

    # Borde interior
    draw.line(
        (
            3 * ESCALA,
            3 * ESCALA,
            ancho - 4 * ESCALA,
            3 * ESCALA,
        ),
        fill=(255, 255, 255, 255),
        width=ESCALA,
    )

    draw.line(
        (
            3 * ESCALA,
            3 * ESCALA,
            3 * ESCALA,
            alto - 4 * ESCALA,
        ),
        fill=(255, 255, 255, 255),
        width=ESCALA,
    )

    draw.line(
        (
            3 * ESCALA,
            alto - 4 * ESCALA,
            ancho - 4 * ESCALA,
            alto - 4 * ESCALA,
        ),
        fill=(80, 80, 80, 255),
        width=ESCALA,
    )

    draw.line(
        (
            ancho - 4 * ESCALA,
            3 * ESCALA,
            ancho - 4 * ESCALA,
            alto - 4 * ESCALA,
        ),
        fill=(80, 80, 80, 255),
        width=ESCALA,
    )

    # --------------------------------------------------------
    # GRID 3x3
    # --------------------------------------------------------

    for fila in range(3):
        for columna in range(3):

            x = (
                GRID_X
                + columna * (
                    SLOT + SEPARACION
                )
            )

            y = (
                GRID_Y
                + fila * (
                    SLOT + SEPARACION
                )
            )

            dibujar_slot(
                draw,
                x,
                y,
            )

    # --------------------------------------------------------
    # RESULTADO
    # --------------------------------------------------------

    dibujar_slot(
        draw,
        RESULTADO_X,
        RESULTADO_Y,
    )

    # --------------------------------------------------------
    # FLECHA
    # --------------------------------------------------------

    dibujar_flecha(draw)

    return imagen


# ============================================================
# FUNCIÓN PRINCIPAL
# ============================================================

def generar_imagen_crafteo(item):
    if not item:
        return None

    receta = item.get("receta")

    if not receta:
        return None

    patron = receta.get("patron")

    if not patron:
        return None

    # --------------------------------------------------------
    # SIEMPRE 3x3
    # --------------------------------------------------------

    patron = normalizar_patron(patron)

    # --------------------------------------------------------
    # CREAR INTERFAZ
    # --------------------------------------------------------

    imagen = crear_interfaz()

    # --------------------------------------------------------
    # INGREDIENTES
    # --------------------------------------------------------

    for fila in range(3):
        for columna in range(3):

            identificador = patron[
                fila
            ][
                columna
            ]

            if not identificador:
                continue

            x = (
                GRID_X
                + columna * (
                    SLOT + SEPARACION
                )
            )

            y = (
                GRID_Y
                + fila * (
                    SLOT + SEPARACION
                )
            )

            dibujar_textura(
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
        item.get("identificador"),
    )

    dibujar_textura(
        imagen,
        resultado,
        RESULTADO_X,
        RESULTADO_Y,
    )

    # --------------------------------------------------------
    # CANTIDAD
    # --------------------------------------------------------

    cantidad = receta.get(
        "cantidad_resultado",
        1,
    )

    dibujar_cantidad(
        imagen,
        cantidad,
        RESULTADO_X,
        RESULTADO_Y,
    )

    # --------------------------------------------------------
    # RECORTAR AL CONTENIDO
    # --------------------------------------------------------

    # No dejamos espacio inútil alrededor.
    bbox = imagen.getbbox()

    if bbox:
        imagen = imagen.crop(bbox)

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

    buffer.name = "crafteo.png"

    return buffer
