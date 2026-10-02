# bot_railway.py

import logging
import os

from dotenv import load_dotenv

from telegram import Update
from telegram.ext import (
    Application,
    CommandHandler,
    ContextTypes,
    MessageHandler,
    filters,
)

from comandos.items import comando_item
from comandos.lang import comando_lang


load_dotenv()

TOKEN = os.getenv("BOT_TOKEN")


logging.basicConfig(
    format=(
        "%(asctime)s - "
        "%(name)s - "
        "%(levelname)s - "
        "%(message)s"
    ),
    level=logging.INFO,
)

logger = logging.getLogger(__name__)


async def start(
    update: Update,
    context: ContextTypes.DEFAULT_TYPE,
):
    if not update.message:
        return

    await update.message.reply_text(
        "⛏️ ¡Bienvenido a "
        "MinecraftFullGuideBot!\n\n"
        "📚 Tu guía completa de Minecraft.\n\n"
        "🔨 Usa /item para consultar "
        "objetos y recetas.\n"
        "🌐 Usa /lang para cambiar el idioma.\n\n"
        "Ejemplos:\n"
        "/item pico de diamante\n"
        "/item horno\n"
        "/item cristal\n"
        "/lang english"
    )


async def help_command(
    update: Update,
    context: ContextTypes.DEFAULT_TYPE,
):
    if not update.message:
        return

    await update.message.reply_text(
        "📖 <b>Comandos disponibles</b>\n\n"
        "/start — Iniciar el bot\n"
        "/help — Mostrar ayuda\n"
        "/item &lt;nombre&gt; — "
        "Buscar un objeto\n"
        "/lang &lt;idioma&gt; — "
        "Cambiar idioma\n\n"
        "<b>Ejemplos:</b>\n"
        "/item pico de diamante\n"
        "/item espada de diamante\n"
        "/item mesa de crafteo\n"
        "/item horno\n"
        "/item cristal\n"
        "/lang spanish\n"
        "/lang english\n"
        "/lang japanese",
        parse_mode="HTML",
    )


async def comando_desconocido(
    update: Update,
    context: ContextTypes.DEFAULT_TYPE,
):
    if not update.message:
        return

    texto = update.message.text or ""

    if not texto.startswith("/"):
        return

    comando = texto.split()[0]

    if "@" in comando:
        comando = comando.split("@")[0]

    await update.message.reply_text(
        f"❌ El comando {comando} no existe.\n\n"
        "📖 Usa /help para ver los comandos."
    )


async def error_handler(
    update: object,
    context: ContextTypes.DEFAULT_TYPE,
):
    logger.error(
        "Error durante la ejecución:",
        exc_info=context.error,
    )


def main():
    if not TOKEN:
        raise RuntimeError(
            "No se encontró BOT_TOKEN "
            "en las variables de entorno."
        )

    application = (
        Application
        .builder()
        .token(TOKEN)
        .build()
    )

    application.add_handler(
        CommandHandler(
            "start",
            start,
        )
    )

    application.add_handler(
        CommandHandler(
            "help",
            help_command,
        )
    )

    application.add_handler(
        CommandHandler(
            "item",
            comando_item,
        )
    )

    application.add_handler(
        CommandHandler(
            "lang",
            comando_lang,
        )
    )

    application.add_handler(
        MessageHandler(
            filters.COMMAND,
            comando_desconocido,
        )
    )

    application.add_error_handler(
        error_handler
    )

    logger.info(
        "MinecraftFullGuideBot iniciado."
    )

    application.run_polling(
        allowed_updates=Update.ALL_TYPES
    )


if __name__ == "__main__":
    main()
