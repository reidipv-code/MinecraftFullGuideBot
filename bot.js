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

function valido(v) {
  if (v === undefined || v === null) return false;
  const s = String(v).trim();
  return s !== "" && s !== "0" && s !== "0.0";
}

function formatearItem(item) {
  let msg = `<b>${item.nombre}</b>\n\n`;

  if (valido(item.id))          msg += `🆔 <code>${item.id}</code>\n`;
  if (valido(item.categoria))   msg += `🗂️ Categoría: ${item.categoria}\n`;
  if (valido(item.stack))       msg += `📦 Stack: ${item.stack}\n`;
  if (valido(item.durabilidad)) msg += `🛡️ Durabilidad: ${item.durabilidad}\n`;
  if (valido(item.daño))        msg += `⚔️ Daño: ${item.daño}\n`;

  if (valido(item.receta)) {
    msg += `\n🔨 <b>Receta</b>\n${item.receta}\n`;
  }

  if (valido(item.mesa)) {
    msg += `\n🛠️ Se fabrica con: ${item.mesa}`;
  }

  return msg.trim();
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

    if (valido(item.img)) {
      const rutas = item.img.split(",").map(r => r.trim());

      try {
        // Primera imagen con el caption
        const primera = path.join(__dirname, rutas[0]);
        await ctx.replyWithPhoto(
          { source: fs.createReadStream(primera) },
          { caption, parse_mode: "HTML" }
        );

        // Resto de imágenes sin caption
        for (let i = 1; i < rutas.length; i++) {
          const siguiente = path.join(__dirname, rutas[i]);
          await ctx.replyWithPhoto(
            { source: fs.createReadStream(siguiente) }
          );
        }
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
