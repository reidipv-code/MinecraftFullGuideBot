import os
import logging

from dotenv import load_dotenv
from telegram import Update
from telegram.ext import Application, CommandHandler, ContextTypes


load_dotenv()

TOKEN = os.getenv("BOT_TOKEN")


logging.basicConfig(
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    level=logging.INFO
)

logger = logging.getLogger(__name__)


async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "⛏️ ¡Bienvenido a MinecraftFullGuideBot!\n\n"
        "📚 Tu guía completa de Minecraft."
    )


async def help_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "📖 Comandos disponibles:\n\n"
        "/start - Iniciar el bot\n"
        "/help - Mostrar ayuda"
    )


async def error_handler(update, context):
    logger.error(
        "Error:",
        exc_info=context.error
    )


def main():
    if not TOKEN:
        raise RuntimeError(
            "No se encontró BOT_TOKEN en las variables de entorno."
        )

    application = (
        Application.builder()
        .token(TOKEN)
        .build()
    )

    application.add_handler(
        CommandHandler("start", start)
    )

    application.add_handler(
        CommandHandler("help", help_command)
    )

    application.add_error_handler(error_handler)

    logger.info("MinecraftFullGuideBot iniciado.")

    application.run_polling(
        allowed_updates=Update.ALL_TYPES
    )


if __name__ == "__main__":
    main()
