from telegram import Update
from telegram.ext import ContextTypes

from datos.items import buscar_item
from core.generador_crafteo import (
    generar_imagen_crafteo,
)


async def comando_item(
    update: Update,
    context: ContextTypes.DEFAULT_TYPE,
):

    if not context.args:

        await update.message.reply_text(

            "🔎 Escribe el nombre de un objeto.\n\n"

            "Ejemplos:\n"

            "/item pico de diamante\n"
            "/item cristal\n"
            "/item hierro"

        )

        return

    consulta = " ".join(
        context.args
    )

    item = buscar_item(
        consulta
    )

    if item is None:

        await update.message.reply_text(

            f"❌ No encontré ningún objeto "
            f"llamado «{consulta}».\n\n"

            "Puedes usar el nombre en español "
            "o el identificador de Minecraft."

        )

        return

    # ========================================================
    # INFORMACIÓN
    # ========================================================

    nombre = item[
        "nombre"
    ]

    identificador = item[
        "identificador"
    ]

    categoria = item[
        "categoria"
    ]

    descripcion = item[
        "descripcion"
    ]

    texto = (

        f"⛏️ <b>{nombre}</b>\n\n"

        f"🆔 <b>Identificador:</b> "
        f"<code>{identificador}</code>\n"

        f"📦 <b>Categoría:</b> "
        f"{categoria}\n\n"

        f"📖 <b>Información:</b> "
        f"{descripcion}"

    )

    # ========================================================
    # DAÑO
    # ========================================================

    if item.get(
        "danio"
    ) is not None:

        texto += (

            f"\n⚔️ <b>Daño:</b> "
            f"{item['danio']}"

        )

    # ========================================================
    # VELOCIDAD
    # ========================================================

    if item.get(
        "velocidad_mineria"
    ) is not None:

        texto += (

            f"\n⛏️ <b>Velocidad de minería:</b> "
            f"{item['velocidad_mineria']}"

        )

    # ========================================================
    # DURABILIDAD
    # ========================================================

    if item.get(
        "durabilidad"
    ) is not None:

        texto += (

            f"\n🛠️ <b>Durabilidad:</b> "
            f"{item['durabilidad']}"

        )

    # ========================================================
    # RECETA
    # ========================================================

    receta = item.get(
        "receta"
    )

    if not receta:

        texto += (

            "\n\n❌ <b>Obtención:</b> "
            "No tiene receta de fabricación "
            "registrada."

        )

        await update.message.reply_text(

            texto,

            parse_mode="HTML",

        )

        return

    estacion = (

        receta.get(
            "estacion"
        )

        or

        receta.get(
            "mesa"
        )

        or

        "Mesa de crafteo"

    )

    texto += (

        f"\n\n🧱 <b>Obtención:</b> "
        f"{estacion}"

    )

    # ========================================================
    # INGREDIENTES
    # ========================================================

    ingredientes = receta.get(
        "ingredientes"
    ) or []

    if ingredientes:

        texto += (
            "\n\n🧩 <b>Ingredientes:</b>"
        )

        for ingrediente in ingredientes:

            texto += (

                f"\n• "
                f"{ingrediente['cantidad']}× "
                f"{ingrediente['nombre']}"

            )

    # ========================================================
    # IMAGEN
    # ========================================================

    imagen = None

    try:

        imagen = (
            generar_imagen_crafteo(
                item
            )
        )

    except Exception as error:

        print(
            "Error generando imagen:",
            error,
        )

    if imagen:

        await update.message.reply_photo(

            photo=imagen,

            caption=texto,

            parse_mode="HTML",

        )

    else:

        await update.message.reply_text(

            texto,

            parse_mode="HTML",

        )
