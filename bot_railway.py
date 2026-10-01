import logging
import os

from dotenv import load_dotenv
from telegram import Update
from telegram.ext import (
    Application,
    CommandHandler,
    ContextTypes,
)

from comandos.items import comando_item


# ============================================================
# CONFIGURACIÓN
# ============================================================

load_dotenv()

TOKEN = os.getenv("BOT_TOKEN")


# ============================================================
# LOGGING
# ============================================================

logging.basicConfig(
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    level=logging.INFO,
)

logger = logging.getLogger(__name__)


# ============================================================
# COMANDOS
# ============================================================

async def start(
    update: Update,
    context: ContextTypes.DEFAULT_TYPE,
):
    await update.message.reply_text(
        "⛏️ ¡Bienvenido a MinecraftFullGuideBot!\n\n"
        "📚 Aquí encontrarás información sobre "
        "objetos, bloques, herramientas, armas, "
        "armaduras, comida y mucho más.\n\n"
        "🔎 Usa:\n"
        "/item <nombre>\n\n"
        "Ejemplo:\n"
        "/item pico de diamante"
    )


async def help_command(
    update: Update,
    context: ContextTypes.DEFAULT_TYPE,
):
    await update.message.reply_text(
        "📖 AYUDA\n\n"
        "/start - Iniciar el bot\n"
        "/help - Mostrar ayuda\n"
        "/item <nombre> - Buscar un objeto\n\n"
        "Ejemplo:\n"
        "/item diamante"
    )


# ============================================================
# ERRORES
# ============================================================

async def error_handler(
    update: object,
    context: ContextTypes.DEFAULT_TYPE,
):
    logger.error(
        "Se produjo un error:",
        exc_info=context.error,
    )


# ============================================================
# MAIN
# ============================================================

def main():

    if not TOKEN:
        raise RuntimeError(
            "No se encontró BOT_TOKEN en las variables de entorno."
        )

    logger.info(
        "Iniciando MinecraftFullGuideBot..."
    )

    application = (
        Application.builder()
        .token(TOKEN)
        .build()
    )

    # --------------------------------------------------------
    # COMANDOS
    # --------------------------------------------------------

    application.add_handler(
        CommandHandler("start", start)
    )

    application.add_handler(
        CommandHandler("help", help_command)
    )

    application.add_handler(
        CommandHandler("item", comando_item)
    )

    # --------------------------------------------------------
    # ERRORES
    # --------------------------------------------------------

    application.add_error_handler(
        error_handler
    )

    # --------------------------------------------------------
    # INICIAR
    # --------------------------------------------------------

    logger.info(
        "MinecraftFullGuideBot iniciado correctamente."
    )

    application.run_polling(
        allowed_updates=Update.ALL_TYPES
    )


# ============================================================
# EJECUCIÓN
# ============================================================

if __name__ == "__main__":
    main()
