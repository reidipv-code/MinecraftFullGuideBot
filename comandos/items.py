# comandos/items.py

from telegram import Update
from telegram.ext import ContextTypes

from datos.idiomas import obtener_idioma_usuario
from datos.items import buscar_item
from core.generador_crafteo import generar_imagen_crafteo


def _nombre_ingrediente(
    ingrediente,
    idioma,
):
    if not ingrediente:
        return "—"

    if ingrediente.startswith("#"):
        return (
            "Cualquier "
            + ingrediente[1:].replace(
                "_",
                " ",
            )
        )

    from datos.idiomas import traducir_identificador

    return traducir_identificador(
        ingrediente,
        idioma,
    )


def _texto_receta(
    receta,
    idioma,
):
    tipo = receta.get("tipo")

    if tipo == "crafting":
        forma = receta.get("forma")

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

            return "\n".join(partes)

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

        return "\n".join(partes)

    if tipo == "proceso":
        ingrediente = _nombre_ingrediente(
            receta.get("ingrediente"),
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

        return (
            f"{ingrediente} → "
            f"{nombres.get(proceso, proceso)}"
        )

    return "Sin información."


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

    try:
        item = buscar_item(
            consulta,
            idioma,
        )
    except Exception as error:
        await update.message.reply_text(
            "❌ No se pudieron cargar los "
            "datos de Minecraft.\n\n"
            f"Error: {error}"
        )
        return

    if not item:
        await update.message.reply_text(
            f"❌ No encontré ningún objeto "
            f"para: {consulta}"
        )
        return

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
        item.get("name", ""),
    )

    lineas = [
        f"⛏️ <b>{nombre}</b>",
        "",
        f"🆔 <code>{identifier}</code>",
    ]

    if item.get("stackSize"):
        lineas.append(
            f"📦 Stack: {item['stackSize']}"
        )

    if item.get("durability"):
        lineas.append(
            f"🛡️ Durabilidad: {item['durability']}"
        )

    recetas = item.get(
        "recipes",
        [],
    )

    if not recetas:
        lineas.extend(
            [
                "",
                "📖 Este objeto no tiene una "
                "receta de fabricación normal.",
            ]
        )

        await update.message.reply_text(
            "\n".join(lineas),
            parse_mode="HTML",
        )
        return

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

    await update.message.reply_text(
        "\n".join(lineas),
        parse_mode="HTML",
    )

    try:
        imagen = generar_imagen_crafteo(
            item,
            receta,
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
            "⚠️ No se pudo generar la "
            "imagen de la receta.\n"
            f"{error}"
        )
