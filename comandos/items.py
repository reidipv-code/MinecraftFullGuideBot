from telegram import Update
from telegram.ext import ContextTypes

from datos.items import buscar_item
from core.generador_crafteo import generar_imagen_crafteo


async def comando_item(
    update: Update,
    context: ContextTypes.DEFAULT_TYPE,
):

    if not context.args:

        await update.message.reply_text(
            "🔎 Escribe el nombre de un objeto.\n\n"
            "Ejemplo:\n"
            "/item pico de diamante"
        )

        return

    consulta = " ".join(context.args)

    item = buscar_item(consulta)

    if item is None:

        await update.message.reply_text(
            f"❌ No encontré ningún objeto llamado "
            f"\"{consulta}\".\n\n"
            "Comprueba el nombre e inténtalo nuevamente."
        )

        return

    # ========================================================
    # INFORMACIÓN
    # ========================================================

    nombre = item["nombre"]
    identificador = item["identificador"]
    categoria = item["categoria"]
    descripcion = item["descripcion"]

    texto = (
        f"⛏️ <b>{nombre.upper()}</b>\n\n"
        f"🆔 <b>Identificador:</b> "
        f"<code>{identificador}</code>\n\n"
        f"📦 <b>Categoría:</b> {categoria}\n\n"
        f"📖 <b>Información:</b>\n"
        f"{descripcion}\n"
    )

    # ========================================================
    # DAÑO
    # ========================================================

    if item.get("danio") is not None:

        texto += (
            f"\n⚔️ <b>Daño:</b> "
            f"{item['danio']}"
        )

    # ========================================================
    # VELOCIDAD DE MINERÍA
    # ========================================================

    if item.get("velocidad_mineria") is not None:

        texto += (
            f"\n⛏️ <b>Velocidad de minería:</b> "
            f"{item['velocidad_mineria']}"
        )

    # ========================================================
    # DURABILIDAD
    # ========================================================

    if item.get("durabilidad") is not None:

        texto += (
            f"\n🛠️ <b>Durabilidad:</b> "
            f"{item['durabilidad']}"
        )

    # ========================================================
    # CRAFTEO
    # ========================================================

    receta = item.get("receta")

    if receta is None:

        texto += (
            "\n\n❌ <b>Crafteo:</b> "
            "No tiene crafteo."
        )

        await update.message.reply_text(
            texto,
            parse_mode="HTML",
        )

        return

    mesa = receta.get(
        "mesa",
        "Mesa de crafteo",
    )

    texto += (
        f"\n\n🧱 <b>Crafteo:</b>\n"
        f"🏭 Mesa: {mesa}"
    )

    # ========================================================
    # INGREDIENTES
    # ========================================================

    ingredientes = receta.get(
        "ingredientes",
        []
    )

    if ingredientes:

        texto += "\n"

        for ingrediente in ingredientes:

            texto += (
                f"\n• {ingrediente['cantidad']}x "
                f"{ingrediente['nombre']}"
            )

    # ========================================================
    # GENERAR IMAGEN
    # ========================================================

    try:

        imagen = generar_imagen_crafteo(item)

        if imagen:

            await update.message.reply_photo(
                photo=imagen,
                caption=texto,
                parse_mode="HTML",
            )

            return

    except Exception as error:

        print(
            "Error generando imagen:",
            error,
        )

    # ========================================================
    # SI NO SE PUDO GENERAR IMAGEN
    # ========================================================

    await update.message.reply_text(
        texto,
        parse_mode="HTML",
    )
