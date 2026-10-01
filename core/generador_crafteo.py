import io

from PIL import Image, ImageDraw, ImageFont


# ============================================================
# CONFIGURACIÓN
# ============================================================

ANCHO = 1000
ALTO = 650

FONDO = (198, 198, 198)
BORDE = (90, 90, 90)
CASILLA = (139, 139, 139)
INTERIOR = (180, 180, 180)
TEXTO = (35, 35, 35)


# ============================================================
# FUENTES
# ============================================================

def obtener_fuente(tamano):

    rutas = [
        "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf",
        "/usr/share/fonts/truetype/liberation2/LiberationSans-Regular.ttf",
    ]

    for ruta in rutas:

        try:
            return ImageFont.truetype(
                ruta,
                tamano,
            )
        except Exception:
            continue

    return ImageFont.load_default()


# ============================================================
# DIBUJAR TEXTO CENTRADO
# ============================================================

def texto_centrado(
    draw,
    texto,
    centro_x,
    centro_y,
    fuente,
):

    caja = draw.textbbox(
        (0, 0),
        texto,
        font=fuente,
    )

    ancho = caja[2] - caja[0]
    alto = caja[3] - caja[1]

    draw.text(
        (
            centro_x - ancho / 2,
            centro_y - alto / 2,
        ),
        texto,
        fill=TEXTO,
        font=fuente,
    )


# ============================================================
# NOMBRE VISUAL DEL ITEM
# ============================================================

def nombre_visual(identificador):

    nombres = {

        "diamond": "💎",

        "stick": "🪵",

        "planks": "🪵",

        "cobblestone": "🪨",

        "diamond_pickaxe": "⛏️",

        "diamond_sword": "⚔️",

        "crafting_table": "🧱",

        "furnace": "🔥",
    }

    return nombres.get(
        identificador,
        "■",
    )


# ============================================================
# GENERAR IMAGEN
# ============================================================

def generar_imagen_crafteo(item):

    receta = item.get("receta")

    if not receta:
        return None

    patron = receta.get(
        "patron"
    )

    if not patron:
        return None

    imagen = Image.new(
        "RGB",
        (
            ANCHO,
            ALTO,
        ),
        FONDO,
    )

    draw = ImageDraw.Draw(imagen)

    fuente_titulo = obtener_fuente(48)
    fuente_item = obtener_fuente(40)
    fuente_resultado = obtener_fuente(55)

    # ========================================================
    # TÍTULO
    # ========================================================

    texto_centrado(
        draw,
        "Fabricación",
        ANCHO // 2,
        60,
        fuente_titulo,
    )

    # ========================================================
    # CONFIGURACIÓN DE GRID
    # ========================================================

    tamano = 120
    separacion = 8

    columnas = max(
        len(fila)
        for fila in patron
    )

    filas = len(patron)

    grid_ancho = (
        columnas * tamano
        + (columnas - 1) * separacion
    )

    grid_alto = (
        filas * tamano
        + (filas - 1) * separacion
    )

    inicio_x = 110
    inicio_y = 150

    # ========================================================
    # GRID
    # ========================================================

    for fila_index, fila in enumerate(patron):

        for columna_index, identificador in enumerate(fila):

            x = (
                inicio_x
                + columna_index
                * (tamano + separacion)
            )

            y = (
                inicio_y
                + fila_index
                * (tamano + separacion)
            )

            draw.rectangle(
                (
                    x,
                    y,
                    x + tamano,
                    y + tamano,
                ),
                fill=INTERIOR,
                outline=BORDE,
                width=6,
            )

            if identificador:

                simbolo = nombre_visual(
                    identificador
                )

                texto_centrado(
                    draw,
                    simbolo,
                    x + tamano // 2,
                    y + tamano // 2,
                    fuente_item,
                )

    # ========================================================
    # FLECHA
    # ========================================================

    centro_grid_y = (
        inicio_y
        + grid_alto // 2
    )

    flecha_x1 = (
        inicio_x
        + grid_ancho
        + 50
    )

    flecha_x2 = (
        flecha_x1
        + 130
    )

    draw.line(
        (
            flecha_x1,
            centro_grid_y,
            flecha_x2,
            centro_grid_y,
        ),
        fill=BORDE,
        width=12,
    )

    draw.polygon(
        [
            (
                flecha_x2,
                centro_grid_y,
            ),
            (
                flecha_x2 - 30,
                centro_grid_y - 25,
            ),
            (
                flecha_x2 - 30,
                centro_grid_y + 25,
            ),
        ],
        fill=BORDE,
    )

    # ========================================================
    # RESULTADO
    # ========================================================

    resultado_x = (
        flecha_x2 + 50
    )

    resultado_y = (
        centro_grid_y - tamano // 2
    )

    draw.rectangle(
        (
            resultado_x,
            resultado_y,
            resultado_x + tamano,
            resultado_y + tamano,
        ),
        fill=INTERIOR,
        outline=BORDE,
        width=6,
    )

    simbolo_resultado = nombre_visual(
        receta.get(
            "resultado",
            item["identificador"],
        )
    )

    texto_centrado(
        draw,
        simbolo_resultado,
        resultado_x + tamano // 2,
        resultado_y + tamano // 2,
        fuente_resultado,
    )

    # ========================================================
    # NOMBRE DEL RESULTADO
    # ========================================================

    fuente_nombre = obtener_fuente(32)

    texto_centrado(
        draw,
        item["nombre"],
        resultado_x + tamano // 2,
        resultado_y + tamano + 45,
        fuente_nombre,
    )

    # ========================================================
    # GUARDAR EN MEMORIA
    # ========================================================

    buffer = io.BytesIO()

    imagen.save(
        buffer,
        format="PNG",
    )

    buffer.seek(0)

    return buffer
