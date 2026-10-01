import io
import os
import urllib.request
from pathlib import Path

from PIL import Image, ImageDraw, ImageFont


# ============================================================
# MinecraftFullGuideBot
# GENERADOR DE CRAFTEO VANILLA
# ============================================================
#
# - Interfaz basada en la textura real de Minecraft.
# - Texturas reales de los objetos.
# - SIEMPRE cuadrícula 3x3.
# - Las recetas 1x3 / 2x2 se centran dentro del 3x3.
# - NO utiliza emojis.
# - Pixel art ampliado con NEAREST.
# ============================================================


# ============================================================
# CONFIGURACIÓN
# ============================================================

ANCHO_GUI = 176
ALTO_GUI = 166

# Escala final para Telegram.
ESCALA = 4

ANCHO_FINAL = ANCHO_GUI * ESCALA
ALTO_FINAL = ALTO_GUI * ESCALA

VERSION_MINECRAFT = "1.21.4"

URL_ASSETS = (
    "https://raw.githubusercontent.com/"
    "InventivetalentDev/minecraft-assets/"
    f"{VERSION_MINECRAFT}/assets/minecraft"
)

CACHE = Path("/tmp/minecraft_fullguide_assets")
CACHE.mkdir(parents=True, exist_ok=True)


# ============================================================
# POSICIONES DE LA INTERFAZ VANILLA
# ============================================================
#
# En la interfaz vanilla de crafting:
#
# Grid:
#
#   30  48  66
#   30  48  66
#   30  48  66
#
# Y:
#
#   17
#   35
#   53
#
# Output:
#
#   X = 124
#   Y = 35
#
# Cada slot mide 18x18.
# ============================================================

GRID_X = 30
