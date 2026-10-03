const items = [
  // ===== PICOS =====
  {
    nombre: "🪵 Pico de madera",
    id: "minecraft:wooden_pickaxe",
    categoria: "Herramientas",
    stack: 1,
    durabilidad: 59,
    daño: 2,
    receta: "3 Tablones de madera + 2 Palos",
    mesa: "Mesa de crafteo",
    img: "https://i.ibb.co/TUIMAGEN/pico_madera.png"
  },
  {
    nombre: "🪨 Pico de piedra",
    id: "minecraft:stone_pickaxe",
    categoria: "Herramientas",
    stack: 1,
    durabilidad: 131,
    daño: 3,
    receta: "3 Piedra + 2 Palos",
    mesa: "Mesa de crafteo",
    img: "https://i.ibb.co/TUIMAGEN/pico_piedra.png"
  },
  {
    nombre: "🟠 Pico de cobre",
    id: "minecraft:copper_pickaxe",
    categoria: "Herramientas",
    stack: 1,
    durabilidad: 190,
    daño: 3,
    receta: "3 Lingotes de cobre + 2 Palos",
    mesa: "Mesa de crafteo",
    img: "https://i.ibb.co/TUIMAGEN/pico_cobre.png"
  },
  {
    nombre: "⚙️ Pico de hierro",
    id: "minecraft:iron_pickaxe",
    categoria: "Herramientas",
    stack: 1,
    durabilidad: 250,
    daño: 4,
    receta: "3 Lingotes de hierro + 2 Palos",
    mesa: "Mesa de crafteo",
    img: "https://i.ibb.co/TUIMAGEN/pico_hierro.png"
  },
  {
    nombre: "🪙 Pico de oro",
    id: "minecraft:golden_pickaxe",
    categoria: "Herramientas",
    stack: 1,
    durabilidad: 32,
    daño: 2,
    receta: "3 Lingotes de oro + 2 Palos",
    mesa: "Mesa de crafteo",
    img: "https://i.ibb.co/TUIMAGEN/pico_oro.png"
  },
  {
    nombre: "💎 Pico de diamante",
    id: "minecraft:diamond_pickaxe",
    categoria: "Herramientas",
    stack: 1,
    durabilidad: 1561,
    daño: 5,
    receta: "3 Diamantes + 2 Palos",
    mesa: "Mesa de crafteo",
    img: "https://i.ibb.co/TUIMAGEN/pico_diamante.png"
  },
  {
    nombre: "🪨 Pico de netherita",
    id: "minecraft:netherite_pickaxe",
    categoria: "Herramientas",
    stack: 1,
    durabilidad: 2031,
    daño: 6,
    receta: "1 Pico de diamante + 1 Lingote de netherita + 1 Plantilla de mejora",
    mesa: "Mesa de herrería",
    img: "https://i.ibb.co/TUIMAGEN/pico_netherita.png"
  },

  // ===== HACHAS =====
  {
    nombre: "🪓 Hacha de madera",
    id: "minecraft:wooden_axe",
    categoria: "Herramientas",
    stack: 1,
    durabilidad: 59,
    daño: 7,
    receta: "3 Tablones de madera + 2 Palos",
    mesa: "Mesa de crafteo",
    img: "https://i.ibb.co/TUIMAGEN/hacha_madera.png"
  },
  {
    nombre: "🪓 Hacha de piedra",
    id: "minecraft:stone_axe",
    categoria: "Herramientas",
    stack: 1,
    durabilidad: 131,
    daño: 9,
    receta: "3 Piedra + 2 Palos",
    mesa: "Mesa de crafteo",
    img: "https://i.ibb.co/TUIMAGEN/hacha_piedra.png"
  },
  {
    nombre: "🟠 Hacha de cobre",
    id: "minecraft:copper_axe",
    categoria: "Herramientas",
    stack: 1,
    durabilidad: 190,
    daño: 9,
    receta: "3 Lingotes de cobre + 2 Palos",
    mesa: "Mesa de crafteo",
    img: "https://i.ibb.co/TUIMAGEN/hacha_cobre.png"
  },
  {
    nombre: "⚙️ Hacha de hierro",
    id: "minecraft:iron_axe",
    categoria: "Herramientas",
    stack: 1,
    durabilidad: 250,
    daño: 9,
    receta: "3 Lingotes de hierro + 2 Palos",
    mesa: "Mesa de crafteo",
    img: "https://i.ibb.co/TUIMAGEN/hacha_hierro.png"
  },
  {
    nombre: "🪙 Hacha de oro",
    id: "minecraft:golden_axe",
    categoria: "Herramientas",
    stack: 1,
    durabilidad: 32,
    daño: 7,
    receta: "3 Lingotes de oro + 2 Palos",
    mesa: "Mesa de crafteo",
    img: "https://i.ibb.co/TUIMAGEN/hacha_oro.png"
  },
  {
    nombre: "💎 Hacha de diamante",
    id: "minecraft:diamond_axe",
    categoria: "Herramientas",
    stack: 1,
    durabilidad: 1561,
    daño: 9,
    receta: "3 Diamantes + 2 Palos",
    mesa: "Mesa de crafteo",
    img: "https://i.ibb.co/TUIMAGEN/hacha_diamante.png"
  },
  {
    nombre: "🪓 Hacha de netherita",
    id: "minecraft:netherite_axe",
    categoria: "Herramientas",
    stack: 1,
    durabilidad: 2031,
    daño: 10,
    receta: "1 Hacha de diamante + 1 Lingote de netherita + 1 Plantilla",
    mesa: "Mesa de herrería",
    img: "https://i.ibb.co/TUIMAGEN/hacha_netherita.png"
  },

  // ===== PALAS =====
  {
    nombre: "🥄 Pala de madera",
    id: "minecraft:wooden_shovel",
    categoria: "Herramientas",
    stack: 1,
    durabilidad: 59,
    daño: 2.5,
    receta: "1 Tablón + 2 Palos",
    mesa: "Mesa de crafteo",
    img: "https://i.ibb.co/TUIMAGEN/pala_madera.png"
  },
  {
    nombre: "🥄 Pala de piedra",
    id: "minecraft:stone_shovel",
    categoria: "Herramientas",
    stack: 1,
    durabilidad: 131,
    daño: 3.5,
    receta: "1 Piedra + 2 Palos",
    mesa: "Mesa de crafteo",
    img: "https://i.ibb.co/TUIMAGEN/pala_piedra.png"
  },
  {
    nombre: "🟠 Pala de cobre",
    id: "minecraft:copper_shovel",
    categoria: "Herramientas",
    stack: 1,
    durabilidad: 190,
    daño: 3.5,
    receta: "1 Lingote de cobre + 2 Palos",
    mesa: "Mesa de crafteo",
    img: "https://i.ibb.co/TUIMAGEN/pala_cobre.png"
  },
  {
    nombre: "⚙️ Pala de hierro",
    id: "minecraft:iron_shovel",
    categoria: "Herramientas",
    stack: 1,
    durabilidad: 250,
    daño: 4.5,
    receta: "1 Lingote de hierro + 2 Palos",
    mesa: "Mesa de crafteo",
    img: "https://i.ibb.co/TUIMAGEN/pala_hierro.png"
  },
  {
    nombre: "🪙 Pala de oro",
    id: "minecraft:golden_shovel",
    categoria: "Herramientas",
    stack: 1,
    durabilidad: 32,
    daño: 2.5,
    receta: "1 Lingote de oro + 2 Palos",
    mesa: "Mesa de crafteo",
    img: "https://i.ibb.co/TUIMAGEN/pala_oro.png"
  },
  {
    nombre: "💎 Pala de diamante",
    id: "minecraft:diamond_shovel",
    categoria: "Herramientas",
    stack: 1,
    durabilidad: 1561,
    daño: 5.5,
    receta: "1 Diamante + 2 Palos",
    mesa: "Mesa de crafteo",
    img: "https://i.ibb.co/TUIMAGEN/pala_diamante.png"
  },
  {
    nombre: "🥄 Pala de netherita",
    id: "minecraft:netherite_shovel",
    categoria: "Herramientas",
    stack: 1,
    durabilidad: 2031,
    daño: 6.5,
    receta: "1 Pala de diamante + 1 Lingote de netherita + 1 Plantilla",
    mesa: "Mesa de herrería",
    img: "https://i.ibb.co/TUIMAGEN/pala_netherita.png"
  },

  // ===== AZADAS =====
  {
    nombre: "🌾 Azada de madera",
    id: "minecraft:wooden_hoe",
    categoria: "Herramientas",
    stack: 1,
    durabilidad: 59,
    daño: 1,
    receta: "2 Tablones + 2 Palos",
    mesa: "Mesa de crafteo",
    img: "https://i.ibb.co/TUIMAGEN/azada_madera.png"
  },
  {
    nombre: "🌾 Azada de piedra",
    id: "minecraft:stone_hoe",
    categoria: "Herramientas",
    stack: 1,
    durabilidad: 131,
    daño: 1,
    receta: "2 Piedra + 2 Palos",
    mesa: "Mesa de crafteo",
    img: "https://i.ibb.co/TUIMAGEN/azada_piedra.png"
  },
  {
    nombre: "🌾 Azada de cobre",
    id: "minecraft:copper_hoe",
    categoria: "Herramientas",
    stack: 1,
    durabilidad: 190,
    daño: 1,
    receta: "2 Lingotes de cobre + 2 Palos",
    mesa: "Mesa de crafteo",
    img: "https://i.ibb.co/TUIMAGEN/azada_cobre.png"
  },
  {
    nombre: "🌾 Azada de hierro",
    id: "minecraft:iron_hoe",
    categoria: "Herramientas",
    stack: 1,
    durabilidad: 250,
    daño: 1,
    receta: "2 Lingotes de hierro + 2 Palos",
    mesa: "Mesa de crafteo",
    img: "https://i.ibb.co/TUIMAGEN/azada_hierro.png"
  },
  {
    nombre: "🌾 Azada de oro",
    id: "minecraft:golden_hoe",
    categoria: "Herramientas",
    stack: 1,
    durabilidad: 32,
    daño: 1,
    receta: "2 Lingotes de oro + 2 Palos",
    mesa: "Mesa de crafteo",
    img: "https://i.ibb.co/TUIMAGEN/azada_oro.png"
  },
  {
    nombre: "🌾 Azada de diamante",
    id: "minecraft:diamond_hoe",
    categoria: "Herramientas",
    stack: 1,
    durabilidad: 1561,
    daño: 1,
    receta: "2 Diamantes + 2 Palos",
    mesa: "Mesa de crafteo",
    img: "https://i.ibb.co/TUIMAGEN/azada_diamante.png"
  },
  {
    nombre: "🌾 Azada de netherita",
    id: "minecraft:netherite_hoe",
    categoria: "Herramientas",
    stack: 1,
    durabilidad: 2031,
    daño: 1,
    receta: "1 Azada de diamante + 1 Lingote de netherita + 1 Plantilla",
    mesa: "Mesa de herrería",
    img: "https://i.ibb.co/TUIMAGEN/azada_netherita.png"
  },

  // ===== ESPADAS =====
  {
    nombre: "🗡️ Espada de madera",
    id: "minecraft:wooden_sword",
    categoria: "Herramientas",
    stack: 1,
    durabilidad: 59,
    daño: 4,
    receta: "2 Tablones + 1 Palo",
    mesa: "Mesa de crafteo",
    img: "https://i.ibb.co/TUIMAGEN/espada_madera.png"
  },
  {
    nombre: "🗡️ Espada de piedra",
    id: "minecraft:stone_sword",
    categoria: "Herramientas",
    stack: 1,
    durabilidad: 131,
    daño: 5,
    receta: "2 Piedra + 1 Palo",
    mesa: "Mesa de crafteo",
    img: "https://i.ibb.co/TUIMAGEN/espada_piedra.png"
  },
  {
    nombre: "🗡️ Espada de cobre",
    id: "minecraft:copper_sword",
    categoria: "Herramientas",
    stack: 1,
    durabilidad: 190,
    daño: 5,
    receta: "2 Lingotes de cobre + 1 Palo",
    mesa: "Mesa de crafteo",
    img: "https://i.ibb.co/TUIMAGEN/espada_cobre.png"
  },
  {
    nombre: "🗡️ Espada de hierro",
    id: "minecraft:iron_sword",
    categoria: "Herramientas",
    stack: 1,
    durabilidad: 250,
    daño: 6,
    receta: "2 Lingotes de hierro + 1 Palo",
    mesa: "Mesa de crafteo",
    img: "https://i.ibb.co/TUIMAGEN/espada_hierro.png"
  },
  {
    nombre: "🗡️ Espada de oro",
    id: "minecraft:golden_sword",
    categoria: "Herramientas",
    stack: 1,
    durabilidad: 32,
    daño: 4,
    receta: "2 Lingotes de oro + 1 Palo",
    mesa: "Mesa de crafteo",
    img: "https://i.ibb.co/TUIMAGEN/espada_oro.png"
  },
  {
    nombre: "🗡️ Espada de diamante",
    id: "minecraft:diamond_sword",
    categoria: "Herramientas",
    stack: 1,
    durabilidad: 1561,
    daño: 7,
    receta: "2 Diamantes + 1 Palo",
    mesa: "Mesa de crafteo",
    img: "https://i.ibb.co/TUIMAGEN/espada_diamante.png"
  },
  {
    nombre: "🗡️ Espada de netherita",
    id: "minecraft:netherite_sword",
    categoria: "Herramientas",
    stack: 1,
    durabilidad: 2031,
    daño: 8,
    receta: "1 Espada de diamante + 1 Lingote de netherita + 1 Plantilla",
    mesa: "Mesa de herrería",
    img: "https://i.ibb.co/TUIMAGEN/espada_netherita.png"
  },

  // ===== LANZAS =====
  {
    nombre: "🔱 Lanza de madera",
    id: "minecraft:wooden_spear",
    categoria: "Herramientas",
    stack: 1,
    durabilidad: 59,
    daño: 1,
    receta: "1 Tablón + 2 Palos",
    mesa: "Mesa de crafteo",
    img: "https://i.ibb.co/TUIMAGEN/lanza_madera.png"
  },
  {
    nombre: "🔱 Lanza de piedra",
    id: "minecraft:stone_spear",
    categoria: "Herramientas",
    stack: 1,
    durabilidad: 131,
    daño: 2,
    receta: "1 Piedra + 2 Palos",
    mesa: "Mesa de crafteo",
    img: "https://i.ibb.co/TUIMAGEN/lanza_piedra.png"
  },
  {
    nombre: "🔱 Lanza de cobre",
    id: "minecraft:copper_spear",
    categoria: "Herramientas",
    stack: 1,
    durabilidad: 190,
    daño: 2,
    receta: "1 Lingote de cobre + 2 Palos",
    mesa: "Mesa de crafteo",
    img: "https://i.ibb.co/TUIMAGEN/lanza_cobre.png"
  },
  {
    nombre: "🔱 Lanza de hierro",
    id: "minecraft:iron_spear",
    categoria: "Herramientas",
    stack: 1,
    durabilidad: 250,
    daño: 3,
    receta: "1 Lingote de hierro + 2 Palos",
    mesa: "Mesa de crafteo",
    img: "https://i.ibb.co/TUIMAGEN/lanza_hierro.png"
  },
  {
    nombre: "🔱 Lanza de oro",
    id: "minecraft:golden_spear",
    categoria: "Herramientas",
    stack: 1,
    durabilidad: 32,
    daño: 1,
    receta: "1 Lingote de oro + 2 Palos",
    mesa: "Mesa de crafteo",
    img: "https://i.ibb.co/TUIMAGEN/lanza_oro.png"
  },
  {
    nombre: "🔱 Lanza de diamante",
    id: "minecraft:diamond_spear",
    categoria: "Herramientas",
    stack: 1,
    durabilidad: 1561,
    daño: 4,
    receta: "1 Diamante + 2 Palos",
    mesa: "Mesa de crafteo",
    img: "https://i.ibb.co/TUIMAGEN/lanza_diamante.png"
  },
  {
    nombre: "🔱 Lanza de netherita",
    id: "minecraft:netherite_spear",
    categoria: "Herramientas",
    stack: 1,
    durabilidad: 2031,
    daño: 5,
    receta: "1 Lanza de diamante + 1 Lingote de netherita + 1 Plantilla",
    mesa: "Mesa de herrería",
    img: "https://i.ibb.co/TUIMAGEN/lanza_netherita.png"
  }
];

module.exports = items;
