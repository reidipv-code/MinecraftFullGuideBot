# comandos/lang.py

from telegram import Update
from telegram.ext import ContextTypes

from datos.idiomas import (
    IDIOMAS,
    NOMBRES_IDIOMAS,
    establecer_idioma_usuario,
    obtener_idioma_usuario,
)


async def comando_lang(
    update: Update,
    context: ContextTypes.DEFAULT_TYPE,
):
    if not update.message:
        return

    if not context.args:
        idioma_actual = obtener_idioma_usuario(context)
        nombre_actual = NOMBRES_IDIOMAS.get(
            idioma_actual,
            idioma_actual,
        )

        disponibles = "\n".join(
            f"• `{codigo}` — {nombre}"
            for codigo, nombre in NOMBRES_IDIOMAS.items()
        )

        await update.message.reply_text(
            "🌐 <b>Idioma</b>\n\n"
            f"Idioma actual: <b>{nombre_actual}</b>\n\n"
            "Para cambiarlo:\n"
            "<code>/lang english</code>\n"
            "<code>/lang spanish</code>\n"
            "<code>/lang japanese</code>\n\n"
            "<b>Idiomas disponibles:</b>\n"
            f"{disponibles}",
            parse_mode="HTML",
        )
        return

    texto = " ".join(context.args).strip().lower()

    if texto not in IDIOMAS:
        await update.message.reply_text(
            "❌ Idioma no reconocido.\n\n"
            "Usa /lang para ver los idiomas disponibles."
        )
        return

    idioma = establecer_idioma_usuario(
        context,
        IDIOMAS[texto],
    )

    nombre = NOMBRES_IDIOMAS.get(
        idioma,
        idioma,
    )

    await update.message.reply_text(
        f"🌐 Idioma cambiado a <b>{nombre}</b>.",
        parse_mode="HTML",
  )
