const { Telegraf } = require("telegraf");
const fs = require("fs");
const path = require("path");
const items = require("./items");

const bot = new Telegraf(process.env.BOT_TOKEN);

function buscarItem(nombreBuscado) {
  const limpio = nombreBuscado.toLowerCase().trim();
  return items.find(i => {
    const nombreLimpio = i.nombre
      .replace(/[^\p{L}\p{N}\s]/gu, "")
      .toLowerCase()
      .trim();
    return nombreLimpio === limpio || nombreLimpio.includes(limpio);
  });
}

function formatearItem(item) {
  return `<b>📦 ${item.nombre}</b>\n\n` +
    `🆔 <code>${item.id}</code>\n` +
    `🗂️ Categoría: ${item.categoria}\n` +
    `📦 Stack: ${item.stack}\n` +
    `🛡️ Durabilidad: ${item.durabilidad}\n` +
    `⚔️ Daño: ${item.daño}\n\n` +
    `🔨 <b>Receta</b>\n${item.receta}\n\n` +
    `🛠️ Se fabrica con: ${item.mesa}`;
}

bot.on("text", async (ctx) => {
  const texto = ctx.message.text.trim();

  if (texto.startsWith("/item_")) {
    return ctx.reply(
      "❌ Ese comando no existe.\n\n" +
      "Usa el formato correcto:\n" +
      "<code>/item pico de diamante</code>",
      { parse_mode: "HTML" }
    );
  }

  if (texto === "/item") {
    return ctx.reply(
      "<b>📖 Uso de /item</b>\n\n" +
      "😱 Uso: <code>/item &lt;nombre del ítem&gt;</code>\n" +
      "👨‍🏫 Ejemplo: <code>/item pico de diamante</code>\n\n" +
      "⚠️ No uses guiones bajos, usa espacios.",
      { parse_mode: "HTML" }
    );
  }

  if (texto.startsWith("/item ")) {
    const nombre = texto.replace("/item ", "").trim();
    const item = buscarItem(nombre);

    if (!item) {
      return ctx.reply(
        `❌ No encontré el ítem: <b>${nombre}</b>\n\n` +
        "Revisa la ortografía o usa <code>/item</code> para ver la guía.",
        { parse_mode: "HTML" }
      );
    }

    const caption = formatearItem(item);

    if (item.img) {
      const rutaAbsoluta = path.join(__dirname, item.img);
      console.log("🔍 Intentando enviar imagen desde:", rutaAbsoluta);
      console.log("📁 ¿Existe el archivo?", fs.existsSync(rutaAbsoluta));

      try {
        await ctx.replyWithPhoto(
          { source: fs.createReadStream(rutaAbsoluta) },
          { caption, parse_mode: "HTML" }
        );
        console.log("✅ Imagen enviada correctamente");
      } catch (e) {
        console.error("❌ Error al enviar imagen:", e.message);
        await ctx.reply(caption, { parse_mode: "HTML" });
      }
    } else {
      await ctx.reply(caption, { parse_mode: "HTML" });
    }
  }
});

bot.launch();
console.log("🤖 Bot iniciado correctamente");
