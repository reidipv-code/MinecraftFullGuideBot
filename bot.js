const { Telegraf } = require("telegraf");
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
  return `📦 *${item.nombre}*\n\n` +
    `🆔 \`${item.id}\`\n` +
    `🗂️ Categoría: ${item.categoria}\n` +
    `📦 Stack: ${item.stack}\n` +
    `🛡️ Durabilidad: ${item.durabilidad}\n` +
    `⚔️ Daño: ${item.daño}\n\n` +
    `🔨 Receta\n${item.receta}\n\n` +
    `🛠️ Se fabrica con: ${item.mesa}`;
}

bot.on("text", async (ctx) => {
  const texto = ctx.message.text.trim();

  if (texto.startsWith("/item_")) {
    return ctx.reply(
      "❌ Ese comando no existe.\n\n" +
      "Usa el formato correcto:\n" +
      "`/item pico de diamante`",
      { parse_mode: "Markdown" }
    );
  }

  if (texto === "/item") {
    return ctx.reply(
      "📖 *Uso de /item*\n\n" +
      "😱 Uso: `/item <nombre del ítem>`\n" +
      "👨‍🏫 Ejemplo: `/item pico de diamante`\n\n" +
      "⚠️ No uses guiones bajos, usa espacios.",
      { parse_mode: "Markdown" }
    );
  }

  if (texto.startsWith("/item ")) {
    const nombre = texto.replace("/item ", "").trim();
    const item = buscarItem(nombre);

    if (!item) {
      return ctx.reply(
        `❌ No encontré el ítem: *${nombre}*\n\n` +
        "Revisa la ortografía o usa `/item` para ver la guía.",
        { parse_mode: "Markdown" }
      );
    }

    if (item.img) {
      try {
        await ctx.replyWithPhoto(item.img, {
          caption: formatearItem(item),
          parse_mode: "Markdown"
        });
      } catch (e) {
        await ctx.reply(formatearItem(item), { parse_mode: "Markdown" });
      }
    } else {
      await ctx.reply(formatearItem(item), { parse_mode: "Markdown" });
    }
  }
});

bot.launch();
console.log("🤖 Bot iniciado correctamente");
