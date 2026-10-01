import os
import logging

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
# /START
# ============================================================

async def start(
    update: Update,
    context: ContextTypes.DEFAULT_TYPE,
):

    await update.message.reply_text(
        "⛏️ ¡Bienvenido a MinecraftFullGuideBot!\n\n"
        "📚 Tu guía completa de Minecraft.\n\n"
        "Usa /help para ver los comandos disponibles."
    )


# ============================================================
# /HELP
# ============================================================

async def help_command(
    update: Update,
    context: ContextTypes.DEFAULT_TYPE,
):

    await update.message.reply_text(
        "📖 Comandos disponibles:\n\n"
        "/start - Iniciar el bot\n"
        "/help - Mostrar ayuda\n"
        "/item <nombre> - Buscar información de un objeto\n\n"
        "Ejemplos:\n"
        "/item pico de diamante\n"
        "/item espada de diamante\n"
        "/item mesa de crafteo\n"
        "/item bedrock"
    )


# ============================================================
# COMANDO DESCONOCIDO
# ============================================================

async def comando_desconocido(
    update: Update,
    context: ContextTypes.DEFAULT_TYPE,
):

    if not update.message:
        return

    texto = update.message.text or ""

    # --------------------------------------------------------
    # Solo procesar mensajes que realmente sean comandos.
    # --------------------------------------------------------

    if not texto.startswith("/"):
        return

    comando = texto.split()[0]

    # Quitar @nombre_del_bot si se utiliza:
    #
    # /pepito@MinecraftFullGuideBot
    #
    if "@" in comando:
        comando = comando.split("@")[0]

    await update.message.reply_text(
        f"❌ El comando {comando} no existe.\n\n"
        "📖 Usa /help para ver los comandos disponibles."
    )


# ============================================================
# MANEJADOR DE ERRORES
# ============================================================

async def error_handler(
    update: object,
    context: ContextTypes.DEFAULT_TYPE,
):

    logger.error(
        "Error durante la ejecución:",
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

    application = (
        Application.builder()
        .token(TOKEN)
        .build()
    )

    # --------------------------------------------------------
    # COMANDOS EXISTENTES
    # --------------------------------------------------------

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

    # --------------------------------------------------------
    # COMANDOS DESCONOCIDOS
    #
    # IMPORTANTE:
    # Este handler va DESPUÉS de los comandos conocidos.
    # Así /start, /help y /item funcionan normalmente,
    # mientras que cualquier otro comando llega aquí.
    # --------------------------------------------------------

    application.add_handler(
        MessageHandler(
            filters.COMMAND,
            comando_desconocido,
        )
    )

    # --------------------------------------------------------
    # ERRORES
    # --------------------------------------------------------

    application.add_error_handler(
        error_handler
    )

    logger.info(
        "MinecraftFullGuideBot iniciado."
    )

    # --------------------------------------------------------
    # POLLING
    # --------------------------------------------------------

    application.run_polling(
        allowed_updates=Update.ALL_TYPES
    )


# ============================================================
# EJECUCIÓN
# ============================================================

if __name__ == "__main__":
    main()
