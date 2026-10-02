# comandos/items.py

from telegram import Update
from telegram.ext import ContextTypes

from datos.idiomas import (
    obtener_idioma_usuario,
    traducir_identificador,
)

from datos.items import (
    buscar_item,
    obtener_item_representativo,
)

from core.generador_crafteo import (
    generar_imagen_crafteo,
)


# ============================================================
# NOMBRE DE INGREDIENTE
# ============================================================

def _nombre_ingrediente(
    ingrediente,
    idioma,
):
    if not ingrediente:
        return "—"

    if ingrediente.startswith("#"):

        tag = ingrediente[1:].replace(
            "_",
            " ",
        )

        return (
            "Cualquier "
            + tag
        )

    return traducir_identificador(
        ingrediente,
        idioma,
    )


# ============================================================
# TEXTO DE RECETA
# ============================================================

def _texto_receta(
    receta,
    idioma,
):
    tipo = receta.get(
        "tipo"
    )

    # ========================================================
    # CRAFTING
    # ========================================================

    if tipo == "crafting":

        forma = receta.get(
            "forma"
        )

        # ----------------------------------------------------
        # SHAPED
        # ----------------------------------------------------

        if forma == "shaped":

            matriz = receta.get(
                "matriz",
                [],
            )

            ingredientes = []

            for fila in matriz:

                for ingrediente in fila:

                    if ingrediente:
                        ingredientes.append(
                            ingrediente
                        )

            if not ingredientes:
                return "Sin ingredientes."

            cantidades = {}

            for ingrediente in ingredientes:

                cantidades[ingrediente] = (
                    cantidades.get(
                        ingrediente,
                        0,
                    )
                    + 1
                )

            partes = []

            for ingrediente, cantidad in cantidades.items():

                nombre = _nombre_ingrediente(
                    ingrediente,
                    idioma,
                )

                partes.append(
                    f"{cantidad}× {nombre}"
                )

            texto = "\n".join(
                partes
            )

        # ----------------------------------------------------
        # SHAPELESS
        # ----------------------------------------------------

        else:

            ingredientes = receta.get(
                "ingredientes",
                [],
            )

            cantidades = {}

            for ingrediente in ingredientes:

                cantidades[ingrediente] = (
                    cantidades.get(
                        ingrediente,
                        0,
                    )
                    + 1
                )

            partes = []

            for ingrediente, cantidad in cantidades.items():

                nombre = _nombre_ingrediente(
                    ingrediente,
                    idioma,
                )

                partes.append(
                    f"{cantidad}× {nombre}"
                )

            texto = "\n".join(
                partes
            )

        cantidad = receta.get(
            "cantidad",
            1,
        )

        texto += (
            "\n\n"
            "🛠️ <b>Se fabrica con:</b> "
            "Mesa de crafteo"
        )

        if cantidad > 1:
            texto += (
                f"\n📦 Resultado: "
                f"{cantidad}"
            )

        return texto

    # ========================================================
    # HORNO / PROCESOS
    # ========================================================

    if tipo == "proceso":

        ingrediente = _nombre_ingrediente(
            receta.get(
                "ingrediente"
            ),
            idioma,
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

        texto = (
            f"{ingrediente} → "
            f"{nombres.get(
                proceso,
                proceso,
            )}"
        )

        cantidad = receta.get(
            "cantidad",
            1,
        )

        if cantidad > 1:
            texto += (
                f"\n📦 Resultado: "
                f"{cantidad}"
            )

        return texto

    # ========================================================
    # CORTAPIEDRAS
    # ========================================================

    if tipo == "stonecutting":

        ingrediente = _nombre_ingrediente(
            receta.get(
                "ingrediente"
            ),
            idioma,
        )

        cantidad = receta.get(
            "cantidad",
            1,
        )

        texto = (
            f"{ingrediente} → "
            "Cortapiedras"
        )

        if cantidad > 1:
            texto += (
                f"\n📦 Resultado: "
                f"{cantidad}"
            )

        return texto

    return "Sin información."


# ============================================================
# COMANDO ITEM
# ============================================================

async def comando_item(
    update: Update,
    context: ContextTypes.DEFAULT_TYPE,
):
    if not update.message:
        return

    if not context.args:

        await update.message.reply_text(
            "❌ Usa:\n"
            "/item <nombre>\n\n"
            "Ejemplo:\n"
            "/item pico de diamante"
        )

        return

    consulta = " ".join(
        context.args
    )

    idioma = obtener_idioma_usuario(
        context
    )

    # ========================================================
    # BUSCAR
    # ========================================================

    try:

        item = buscar_item(
            consulta,
            idioma,
        )

    except Exception as error:

        await update.message.reply_text(
            "❌ No se pudieron cargar "
            "los datos de Minecraft.\n\n"
            f"Error: {error}"
        )

        return

    if not item:

        await update.message.reply_text(
            f"❌ No encontré ningún objeto "
            f"para: {consulta}"
        )

        return

    # ========================================================
    # DATOS PRINCIPALES
    # ========================================================

    nombre = item.get(
        "translatedName",
        item.get(
            "displayName",
            item.get(
                "name",
                consulta,
            ),
        ),
    )

    identifier = item.get(
        "identifier",
        item.get(
            "name",
            "",
        ),
    )

    lineas = [
        f"⛏️ <b>{nombre}</b>",
        "",
        f"🆔 <code>{identifier}</code>",
    ]

    # ========================================================
    # CATEGORÍA
    # ========================================================

    categoria = (
        item.get("category")
        or item.get("type")
    )

    if categoria:
        lineas.append(
            f"🗂️ Categoría: "
            f"{categoria}"
        )

    # ========================================================
    # STACK
    # ========================================================

    if item.get(
        "stackSize"
    ) is not None:

        lineas.append(
            f"📦 Stack: "
            f"{item['stackSize']}"
        )

    # ========================================================
    # DURABILIDAD
    # ========================================================

    if item.get(
        "durability"
    ):

        lineas.append(
            f"🛡️ Durabilidad: "
            f"{item['durability']}"
        )

    # ========================================================
    # RECETAS
    # ========================================================

    recetas = item.get(
        "recipes",
        [],
    )

    if recetas:

        # Mostrar la primera receta real
        receta = recetas[0]

        lineas.extend(
            [
                "",
                "🔨 <b>Receta</b>",
                _texto_receta(
                    receta,
                    idioma,
                ),
            ]
        )

        # Si hay varias recetas
        if len(recetas) > 1:

            lineas.append(
                ""
            )

            lineas.append(
                f"📚 Este objeto tiene "
                f"{len(recetas)} recetas "
                f"registradas."
            )

    else:

        lineas.extend(
            [
                "",
                "📖 Este objeto no tiene "
                "una receta de fabricación "
                "normal.",
            ]
        )

    # ========================================================
    # ENVIAR INFORMACIÓN
    # ========================================================

    await update.message.reply_text(
        "\n".join(lineas),
        parse_mode="HTML",
    )

    # ========================================================
    # IMAGEN
    # ========================================================

    if not recetas:
        return

    try:

        imagen = generar_imagen_crafteo(
            item,
            recetas[0],
            nombre,
        )

        if imagen:

            await update.message.reply_photo(
                photo=imagen,
                caption=(
                    f"🔨 {nombre}\n"
                    f"🆔 {identifier}"
                ),
            )

    except Exception as error:

        await update.message.reply_text(
            "⚠️ La receta sí existe, "
            "pero ocurrió un error al "
            "generar su imagen.\n\n"
            f"{error}"
        )
