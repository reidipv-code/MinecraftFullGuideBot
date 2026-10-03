const items = [
  // ==================== PICOS ====================
  {
    nombre: "🪵 Pico de madera",
    id: "minecraft:wooden_pickaxe",
    categoria: "Equipo",
    stack: 1,
    durabilidad: 59,
    daño: 2,
    receta: "3 Tablones + 2 Palos",
    mesa: "Mesa de crafteo",
    img: "assets/craft/pico_madera.png"
  },
  {
    nombre: "🪨 Pico de piedra",
    id: "minecraft:stone_pickaxe",
    categoria: "Equipo",
    stack: 1,
    durabilidad: 131,
    daño: 3,
    receta: "3 Piedra + 2 Palos",
    mesa: "Mesa de crafteo",
    img: "assets/craft/pico_piedra.png"
  },
  {
    nombre: "🟠 Pico de cobre",
    id: "minecraft:copper_pickaxe",
    categoria: "Equipo",
    stack: 1,
    durabilidad: 190,
    daño: 3,
    receta: "3 Lingotes de cobre + 2 Palos",
    mesa: "Mesa de crafteo",
    img: "assets/craft/pico_cobre.png"
  },
  {
    nombre: "⚙️ Pico de hierro",
    id: "minecraft:iron_pickaxe",
    categoria: "Equipo",
    stack: 1,
    durabilidad: 250,
    daño: 4,
    receta: "3 Lingotes de hierro + 2 Palos",
    mesa: "Mesa de crafteo",
    img: "assets/craft/pico_hierro.png"
  },
  {
    nombre: "🪙 Pico de oro",
    id: "minecraft:golden_pickaxe",
    categoria: "Equipo",
    stack: 1,
    durabilidad: 32,
    daño: 2,
    receta: "3 Lingotes de oro + 2 Palos",
    mesa: "Mesa de crafteo",
    img: "assets/craft/pico_oro.png"
  },
  {
    nombre: "💎 Pico de diamante",
    id: "minecraft:diamond_pickaxe",
    categoria: "Equipo",
    stack: 1,
    durabilidad: 1561,
    daño: 5,
    receta: "3 Diamantes + 2 Palos",
    mesa: "Mesa de crafteo",
    img: "assets/craft/pico_diamante.png"
  },
  {
    nombre: "🪨 Pico de netherita",
    id: "minecraft:netherite_pickaxe",
    categoria: "Equipo",
    stack: 1,
    durabilidad: 2031,
    daño: 6,
    receta: "1 Pico de diamante + 1 Lingote de netherita + 1 Plantilla",
    mesa: "Mesa de herrería",
    img: "assets/craft/pico_netherita.png"
  },

  // ==================== PALAS ====================
  {
    nombre: "🥄 Pala de madera",
    id: "minecraft:wooden_shovel",
    categoria: "Equipo",
    stack: 1,
    durabilidad: 59,
    daño: 2.5,
    receta: "1 Tablón + 2 Palos",
    mesa: "Mesa de crafteo",
    img: "assets/craft/pala_madera.png"
  },
  {
    nombre: "🥄 Pala de piedra",
    id: "minecraft:stone_shovel",
    categoria: "Equipo",
    stack: 1,
    durabilidad: 131,
    daño: 3.5,
    receta: "1 Piedra + 2 Palos",
    mesa: "Mesa de crafteo",
    img: "assets/craft/pala_piedra.png"
  },
  {
    nombre: "🟠 Pala de cobre",
    id: "minecraft:copper_shovel",
    categoria: "Equipo",
    stack: 1,
    durabilidad: 190,
    daño: 3.5,
    receta: "1 Lingote de cobre + 2 Palos",
    mesa: "Mesa de crafteo",
    img: "assets/craft/pala_cobre.png"
  },
  {
    nombre: "⚙️ Pala de hierro",
    id: "minecraft:iron_shovel",
    categoria: "Equipo",
    stack: 1,
    durabilidad: 250,
    daño: 4.5,
    receta: "1 Lingote de hierro + 2 Palos",
    mesa: "Mesa de crafteo",
    img: "assets/craft/pala_hierro.png"
  },
  {
    nombre: "🪙 Pala de oro",
    id: "minecraft:golden_shovel",
    categoria: "Equipo",
    stack: 1,
    durabilidad: 32,
    daño: 2.5,
    receta: "1 Lingote de oro + 2 Palos",
    mesa: "Mesa de crafteo",
    img: "assets/craft/pala_oro.png"
  },
  {
    nombre: "💎 Pala de diamante",
    id: "minecraft:diamond_shovel",
    categoria: "Equipo",
    stack: 1,
    durabilidad: 1561,
    daño: 5.5,
    receta: "1 Diamante + 2 Palos",
    mesa: "Mesa de crafteo",
    img: "assets/craft/pala_diamante.png"
  },
  {
    nombre: "🥄 Pala de netherita",
    id: "minecraft:netherite_shovel",
    categoria: "Equipo",
    stack: 1,
    durabilidad: 2031,
    daño: 6.5,
    receta: "1 Pala de diamante + 1 Lingote de netherita + 1 Plantilla",
    mesa: "Mesa de herrería",
    img: "assets/craft/pala_netherita.png"
  },

  // ==================== ESPADAS ====================
  {
    nombre: "🗡️ Espada de madera",
    id: "minecraft:wooden_sword",
    categoria: "Equipo",
    stack: 1,
    durabilidad: 59,
    daño: 4,
    receta: "2 Tablones + 1 Palo",
    mesa: "Mesa de crafteo",
    img: "assets/craft/espada_madera.png"
  },
  {
    nombre: "🗡️ Espada de piedra",
    id: "minecraft:stone_sword",
    categoria: "Equipo",
    stack: 1,
    durabilidad: 131,
    daño: 5,
    receta: "2 Piedra + 1 Palo",
    mesa: "Mesa de crafteo",
    img: "assets/craft/espada_piedra.png"
  },
  {
    nombre: "🗡️ Espada de cobre",
    id: "minecraft:copper_sword",
    categoria: "Equipo",
    stack: 1,
    durabilidad: 190,
    daño: 5,
    receta: "2 Lingotes de cobre + 1 Palo",
    mesa: "Mesa de crafteo",
    img: "assets/craft/espada_cobre.png"
  },
  {
    nombre: "🗡️ Espada de hierro",
    id: "minecraft:iron_sword",
    categoria: "Equipo",
    stack: 1,
    durabilidad: 250,
    daño: 6,
    receta: "2 Lingotes de hierro + 1 Palo",
    mesa: "Mesa de crafteo",
    img: "assets/craft/espada_hierro.png"
  },
  {
    nombre: "🗡️ Espada de oro",
    id: "minecraft:golden_sword",
    categoria: "Equipo",
    stack: 1,
    durabilidad: 32,
    daño: 4,
    receta: "2 Lingotes de oro + 1 Palo",
    mesa: "Mesa de crafteo",
    img: "assets/craft/espada_oro.png"
  },
  {
    nombre: "🗡️ Espada de diamante",
    id: "minecraft:diamond_sword",
    categoria: "Equipo",
    stack: 1,
    durabilidad: 1561,
    daño: 7,
    receta: "2 Diamantes + 1 Palo",
    mesa: "Mesa de crafteo",
    img: "assets/craft/espada_diamante.png"
  },
  {
    nombre: "🗡️ Espada de netherita",
    id: "minecraft:netherite_sword",
    categoria: "Equipo",
    stack: 1,
    durabilidad: 2031,
    daño: 8,
    receta: "1 Espada de diamante + 1 Lingote de netherita + 1 Plantilla",
    mesa: "Mesa de herrería",
    img: "assets/craft/espada_netherita.png"
  },

  // ==================== HACHAS ====================
  {
    nombre: "🪓 Hacha de madera",
    id: "minecraft:wooden_axe",
    categoria: "Equipo",
    stack: 1,
    durabilidad: 59,
    daño: 7,
    receta: "3 Tablones + 2 Palos",
    mesa: "Mesa de crafteo",
    img: "assets/craft/hacha_madera.png"
  },
  {
    nombre: "🪓 Hacha de piedra",
    id: "minecraft:stone_axe",
    categoria: "Equipo",
    stack: 1,
    durabilidad: 131,
    daño: 9,
    receta: "3 Piedra + 2 Palos",
    mesa: "Mesa de crafteo",
    img: "assets/craft/hacha_piedra.png"
  },
  {
    nombre: "🟠 Hacha de cobre",
    id: "minecraft:copper_axe",
    categoria: "Equipo",
    stack: 1,
    durabilidad: 190,
    daño: 9,
    receta: "3 Lingotes de cobre + 2 Palos",
    mesa: "Mesa de crafteo",
    img: "assets/craft/hacha_cobre.png"
  },
  {
    nombre: "⚙️ Hacha de hierro",
    id: "minecraft:iron_axe",
    categoria: "Equipo",
    stack: 1,
    durabilidad: 250,
    daño: 9,
    receta: "3 Lingotes de hierro + 2 Palos",
    mesa: "Mesa de crafteo",
    img: "assets/craft/hacha_hierro.png"
  },
  {
    nombre: "🪙 Hacha de oro",
    id: "minecraft:golden_axe",
    categoria: "Equipo",
    stack: 1,
    durabilidad: 32,
    daño: 7,
    receta: "3 Lingotes de oro + 2 Palos",
    mesa: "Mesa de crafteo",
    img: "assets/craft/hacha_oro.png"
  },
  {
    nombre: "💎 Hacha de diamante",
    id: "minecraft:diamond_axe",
    categoria: "Equipo",
    stack: 1,
    durabilidad: 1561,
    daño: 9,
    receta: "3 Diamantes + 2 Palos",
    mesa: "Mesa de crafteo",
    img: "assets/craft/hacha_diamante.png"
  },
  {
    nombre: "🪓 Hacha de netherita",
    id: "minecraft:netherite_axe",
    categoria: "Equipo",
    stack: 1,
    durabilidad: 2031,
    daño: 10,
    receta: "1 Hacha de diamante + 1 Lingote de netherita + 1 Plantilla",
    mesa: "Mesa de herrería",
    img: "assets/craft/hacha_netherita.png"
  },

  // ==================== AZADAS ====================
  {
    nombre: "🌾 Azada de madera",
    id: "minecraft:wooden_hoe",
    categoria: "Equipo",
    stack: 1,
    durabilidad: 59,
    daño: 1,
    receta: "2 Tablones + 2 Palos",
    mesa: "Mesa de crafteo",
    img: "assets/craft/azada_madera.png"
  },
  {
    nombre: "🌾 Azada de piedra",
    id: "minecraft:stone_hoe",
    categoria: "Equipo",
    stack: 1,
    durabilidad: 131,
    daño: 1,
    receta: "2 Piedra + 2 Palos",
    mesa: "Mesa de crafteo",
    img: "assets/craft/azada_piedra.png"
  },
  {
    nombre: "🌾 Azada de cobre",
    id: "minecraft:copper_hoe",
    categoria: "Equipo",
    stack: 1,
    durabilidad: 190,
    daño: 1,
    receta: "2 Lingotes de cobre + 2 Palos",
    mesa: "Mesa de crafteo",
    img: "assets/craft/azada_cobre.png"
  },
  {
    nombre: "🌾 Azada de hierro",
    id: "minecraft:iron_hoe",
    categoria: "Equipo",
    stack: 1,
    durabilidad: 250,
    daño: 1,
    receta: "2 Lingotes de hierro + 2 Palos",
    mesa: "Mesa de crafteo",
    img: "assets/craft/azada_hierro.png"
  },
  {
    nombre: "🌾 Azada de oro",
    id: "minecraft:golden_hoe",
    categoria: "Equipo",
    stack: 1,
    durabilidad: 32,
    daño: 1,
    receta: "2 Lingotes de oro + 2 Palos",
    mesa: "Mesa de crafteo",
    img: "assets/craft/azada_oro.png"
  },
  {
    nombre: "🌾 Azada de diamante",
    id: "minecraft:diamond_hoe",
    categoria: "Equipo",
    stack: 1,
    durabilidad: 1561,
    daño: 1,
    receta: "2 Diamantes + 2 Palos",
    mesa: "Mesa de crafteo",
    img: "assets/craft/azada_diamante.png"
  },
  {
    nombre: "🌾 Azada de netherita",
    id: "minecraft:netherite_hoe",
    categoria: "Equipo",
    stack: 1,
    durabilidad: 2031,
    daño: 1,
    receta: "1 Azada de diamante + 1 Lingote de netherita + 1 Plantilla",
    mesa: "Mesa de herrería",
    img: "assets/craft/azada_netherita.png"
  },

  // ==================== LANZAS ====================
  {
    nombre: "🔱 Lanza de madera",
    id: "minecraft:wooden_spear",
    categoria: "Equipo",
    stack: 1,
    durabilidad: 59,
    daño: 1,
    receta: "1 Tablón + 2 Palos",
    mesa: "Mesa de crafteo",
    img: "assets/craft/lanza_madera.png"
  },
  {
    nombre: "🔱 Lanza de piedra",
    id: "minecraft:stone_spear",
    categoria: "Equipo",
    stack: 1,
    durabilidad: 131,
    daño: 2,
    receta: "1 Piedra + 2 Palos",
    mesa: "Mesa de crafteo",
    img: "assets/craft/lanza_piedra.png"
  },
  {
    nombre: "🔱 Lanza de cobre",
    id: "minecraft:copper_spear",
    categoria: "Equipo",
    stack: 1,
    durabilidad: 190,
    daño: 1,
    receta: "1 Lingote de Cobre + 2 Palos",
    mesa: "Mesa de crafteo",
    img: "assets/craft/lanza_cobre.png"
  },
  {
    nombre: "🔱 Lanza de hierro",
    id: "minecraft:iron_spear",
    categoria: "Equipo",
    stack: 1,
    durabilidad: 250,
    daño: 3,
    receta: "1 Lingote de hierro + 2 Palos",
    mesa: "Mesa de crafteo",
    img: "assets/craft/lanza_hierro.png"
  },
  {
    nombre: "🔱 Lanza de oro",
    id: "minecraft:golden_spear",
    categoria: "Equipo",
    stack: 1,
    durabilidad: 32,
    daño: 1,
    receta: "1 Lingote de oro + 2 Palos",
    mesa: "Mesa de crafteo",
    img: "assets/craft/lanza_oro.png"
  },
  {
    nombre: "🔱 Lanza de diamante",
    id: "minecraft:diamond_spear",
    categoria: "Equipo",
    stack: 1,
    durabilidad: 1561,
    daño: 4,
    receta: "1 Diamante + 2 Palos",
    mesa: "Mesa de crafteo",
    img: "assets/craft/lanza_diamante.png"
  },
  {
    nombre: "🔱 Lanza de netherita",
    id: "minecraft:netherite_spear",
    categoria: "Equipo",
    stack: 1,
    durabilidad: 2031,
    daño: 5,
    receta: "1 Lanza de diamante + 1 Lingote de netherita + 1 Plantilla",
    mesa: "Mesa de herrería",
    img: "assets/craft/lanza_netherita.png"
  },

  // ==================== POCIONES ====================
  {
    nombre: "Receta de las Pociones",
    id: "",
    categoria: "Equipo",
    stack: "",
    durabilidad: "",
    daño: "",
    receta: "",
    mesa: "",
    img: "assets/craft/recetas.png"
  },
  {
    nombre: "🧪 Poción de Regeneración",
    id: "minecraft:potion",
    categoria: "Equipo",
    stack: 1,
    durabilidad: 0,
    daño: 0,
    receta: "Lágrima de Ghast + Poción Rara",
    mesa: "Soporte de pociones",
    img: "assets/craft/pocion_regeneracion.png"
  },
  {
    nombre: "🧪 Poción de Rapidez",
    id: "minecraft:potion",
    categoria: "Equipo",
    stack: 1,
    durabilidad: 0,
    daño: 0,
    receta: "Azúcar + Poción Rara",
    mesa: "Soporte de pociones",
    img: "assets/craft/pocion_rapidez.png"
  },
  {
    nombre: "🧪 Poción de Resistencia al Fuego",
    id: "minecraft:potion",
    categoria: "Equipo",
    stack: 1,
    durabilidad: 0,
    daño: 0,
    receta: "Crema de Magma + Poción Rara",
    mesa: "Soporte de pociones",
    img: "assets/craft/pocion_resistencia_fuego.png"
  },
  {
    nombre: "🧪 Poción de Curación",
    id: "minecraft:potion",
    categoria: "Equipo",
    stack: 1,
    durabilidad: 0,
    daño: 0,
    receta: "Sandía Reluciente + Poción Rara",
    mesa: "Soporte de pociones",
    img: "assets/craft/pocion_curacion.png"
  },
  {
    nombre: "🧪 Poción de Visión Nocturna",
    id: "minecraft:potion",
    categoria: "Equipo",
    stack: 1,
    durabilidad: 0,
    daño: 0,
    receta: "Zanahoria Dorada + Poción Rara",
    mesa: "Soporte de pociones",
    img: "assets/craft/pocion_vision_nocturna.png"
  },
  {
    nombre: "🧪 Poción de Fuerza",
    id: "minecraft:potion",
    categoria: "Equipo",
    stack: 1,
    durabilidad: 0,
    daño: 0,
    receta: "Polvo de Blaze + Poción Rara",
    mesa: "Soporte de pociones",
    img: "assets/craft/pocion_fuerza.png"
  },
  {
    nombre: "🧪 Poción de Salto",
    id: "minecraft:potion",
    categoria: "Equipo",
    stack: 1,
    durabilidad: 0,
    daño: 0,
    receta: "Pata de Conejo + Poción Rara",
    mesa: "Soporte de pociones",
    img: "assets/craft/pocion_salto.png"
  },
  {
    nombre: "🧪 Poción de Respiración Acuática",
    id: "minecraft:potion",
    categoria: "Equipo",
    stack: 1,
    durabilidad: 0,
    daño: 0,
    receta: "Pez Globo + Poción Rara",
    mesa: "Soporte de pociones",
    img: "assets/craft/pocion_respiracion.png"
  },
  {
    nombre: "🧪 Poción de Invisibilidad",
    id: "minecraft:potion",
    categoria: "Equipo",
    stack: 1,
    durabilidad: 0,
    daño: 0,
    receta: "Ojo de Araña Fermentado + Poción de Visión Nocturna",
    mesa: "Soporte de pociones",
    img: "assets/craft/pocion_invisibilidad.png"
  },
  {
    nombre: "🧪 Poción de Caída Lenta",
    id: "minecraft:potion",
    categoria: "Equipo",
    stack: 1,
    durabilidad: 0,
    daño: 0,
    receta: "Membrana de Fantasma + Poción Rara",
    mesa: "Soporte de pociones",
    img: "assets/craft/pocion_caida_lenta.png"
  },
  {
    nombre: "🧪 Poción del Maestro Tortuga",
    id: "minecraft:potion",
    categoria: "Equipo",
    stack: 1,
    durabilidad: 0,
    daño: 0,
    receta: "Caparazón de Tortuga + Poción Rara",
    mesa: "Soporte de pociones",
    img: "assets/craft/pocion_tortuga.png"
  },
  {
    nombre: "🧪 Poción de Veneno",
    id: "minecraft:potion",
    categoria: "Equipo",
    stack: 1,
    durabilidad: 0,
    daño: 0,
    receta: "Ojo de Araña + Poción Rara",
    mesa: "Soporte de pociones",
    img: "assets/craft/pocion_veneno.png"
  },
  {
    nombre: "🧪 Poción de Debilidad",
    id: "minecraft:potion",
    categoria: "Equipo",
    stack: 1,
    durabilidad: 0,
    daño: 0,
    receta: "Ojo de Araña Fermentado + Frasco de Agua",
    mesa: "Soporte de pociones",
    img: "assets/craft/pocion_debilidad.png"
  },
  {
    nombre: "🧪 Poción de Lentitud",
    id: "minecraft:potion",
    categoria: "Equipo",
    stack: 1,
    durabilidad: 0,
    daño: 0,
    receta: "Ojo de Araña Fermentado + Poción de Rapidez",
    mesa: "Soporte de pociones",
    img: "assets/craft/pocion_lentitud.png"
  },
  {
    nombre: "🧪 Poción de Daño",
    id: "minecraft:potion",
    categoria: "Equipo",
    stack: 1,
    durabilidad: 0,
    daño: 0,
    receta: "Ojo de Araña Fermentado + Poción de Curación",
    mesa: "Soporte de pociones",
    img: "assets/craft/pocion_dano.png"
  },

  // ==================== BRÚJULAS Y MAPAS ====================
  {
    nombre: "🧭 Brújula",
    id: "minecraft:compass",
    categoria: "Equipo",
    stack: 1,
    durabilidad: 0,
    daño: 0,
    receta: "4 Lingotes de hierro + 1 Redstone",
    mesa: "Mesa de crafteo",
    img: "assets/craft/brujula.png"
  },
  {
    nombre: "🧭 Brújula de Recuperación",
    id: "minecraft:recovery_compass",
    categoria: "Equipo",
    stack: 1,
    durabilidad: 0,
    daño: 0,
    receta: "8 Fragmentos de Eco + 1 Brújula",
    mesa: "Mesa de crafteo",
    img: "assets/craft/brujula_recuperacion.png"
  },
  {
    nombre: "🗺️ Mapa Vacío",
    id: "minecraft:map",
    categoria: "Equipo",
    stack: 1,
    durabilidad: 0,
    daño: 0,
    receta: "8 Papel + 1 Brújula",
    mesa: "Mesa de crafteo",
    img: "assets/craft/mapa_vacio.png"
  },
  {
    nombre: "🗺️ Mapa Localizador",
    id: "minecraft:filled_map",
    categoria: "Equipo",
    stack: 1,
    durabilidad: 0,
    daño: 0,
    receta: "Mapa Vacío + Brújula",
    mesa: "Mesa de crafteo",
    img: "assets/craft/mapa_localizador.png"
  },
  {
    nombre: "⏰ Reloj",
    id: "minecraft:clock",
    categoria: "Equipo",
    stack: 1,
    durabilidad: 0,
    daño: 0,
    receta: "4 Lingotes de oro + 1 Redstone",
    mesa: "Mesa de crafteo",
    img: "assets/craft/reloj.png"
  },

  // ==================== MECHEROS Y UTILIDADES ====================
  {
    nombre: "🔥 Mechero",
    id: "minecraft:flint_and_steel",
    categoria: "Equipo",
    stack: 1,
    durabilidad: 64,
    daño: 0,
    receta: "1 Lingote de hierro + 1 Pedernal",
    mesa: "Mesa de crafteo",
    img: "assets/craft/mechero.png"
  },
  {
    nombre: "✂️ Tijeras",
    id: "minecraft:shears",
    categoria: "Equipo",
    stack: 1,
    durabilidad: 238,
    daño: 0,
    receta: "2 Lingotes de hierro",
    mesa: "Mesa de crafteo",
    img: "assets/craft/tijeras.png"
  },
  {
    nombre: "🪣 Cubo",
    id: "minecraft:bucket",
    categoria: "Equipo",
    stack: 1,
    durabilidad: 0,
    daño: 0,
    receta: "3 Lingotes de hierro",
    mesa: "Mesa de crafteo",
    img: "assets/craft/cubo.png"
  },
  {
    nombre: "🎣 Caña de Pescar",
    id: "minecraft:fishing_rod",
    categoria: "Equipo",
    stack: 1,
    durabilidad: 64,
    daño: 0,
    receta: "3 Palos + 2 Hilos",
    mesa: "Mesa de crafteo",
    img: "assets/craft/cana_pescar.png"
  },
  {
    nombre: "🥕 Zanahoria en un Palo",
    id: "minecraft:carrot_on_a_stick",
    categoria: "Equipo",
    stack: 1,
    durabilidad: 25,
    daño: 0,
    receta: "1 Caña de Pescar + 1 Zanahoria",
    mesa: "Mesa de crafteo",
    img: "assets/craft/zanahoria_palo.png"
  },
  {
    nombre: "🍄 Hongo Distorsionado en un Palo",
    id: "minecraft:warped_fungus_on_a_stick",
    categoria: "Equipo",
    stack: 1,
    durabilidad: 25,
    daño: 0,
    receta: "1 Caña de Pescar + 1 Hongo Distorsionado",
    mesa: "Mesa de crafteo",
    img: "assets/craft/hongo_palo.png"
  },
  {
    nombre: "🪶 Elytra",
    id: "minecraft:elytra",
    categoria: "Equipo",
    stack: 1,
    durabilidad: 432,
    daño: 0,
    receta: "No se fabrica. Se encuentra en la Ciudad del End",
    mesa: "Ninguna",
    img: "assets/craft/elytra.png"
  },

  // ==================== COMBATE ====================
  {
    nombre: "🏹 Arco",
    id: "minecraft:bow",
    categoria: "Equipo",
    stack: 1,
    durabilidad: 384,
    daño: 0,
    receta: "3 Palos + 3 Hilos",
    mesa: "Mesa de crafteo",
    img: "assets/craft/arco.png"
  },
  {
    nombre: "🎯 Ballesta",
    id: "minecraft:crossbow",
    categoria: "Equipo",
    stack: 1,
    durabilidad: 465,
    daño: 0,
    receta: "2 Palos + 1 Hierro + 1 Hilo + 1 Gancho de Cuerda",
    mesa: "Mesa de crafteo",
    img: "assets/craft/ballesta.png"
  },
  {
    nombre: "➡️ Flecha",
    id: "minecraft:arrow",
    categoria: "Equipo",
    stack: 64,
    durabilidad: 0,
    daño: 0,
    receta: "1 Pedernal + 1 Palo + 1 Pluma",
    mesa: "Mesa de crafteo",
    img: "assets/craft/flecha.png"
  },
  {
    nombre: "✨ Flecha Espectral",
    id: "minecraft:spectral_arrow",
    categoria: "Equipo",
    stack: 64,
    durabilidad: 0,
    daño: 0,
    receta: "4 Polvo de Piedra Luminosa + 1 Flecha",
    mesa: "Mesa de crafteo",
    img: "assets/craft/flecha_espectral.png"
  },
  {
    nombre: "🔱 Tridente",
    id: "minecraft:trident",
    categoria: "Equipo",
    stack: 1,
    durabilidad: 250,
    daño: 9,
    receta: "No se fabrica. Se obtiene de los Ahogados",
    mesa: "Ninguna",
    img: "assets/craft/tridente.png"
  },
  {
    nombre: "🛡️ Escudo",
    id: "minecraft:shield",
    categoria: "Equipo",
    stack: 1,
    durabilidad: 336,
    daño: 0,
    receta: "6 Tablones + 1 Lingote de hierro",
    mesa: "Mesa de crafteo",
    img: "assets/craft/escudo.png"
  },
  {
    nombre: "🗿 Tótem de la Inmortalidad",
    id: "minecraft:totem_of_undying",
    categoria: "Equipo",
    stack: 1,
    durabilidad: 0,
    daño: 0,
    receta: "No se fabrica. Se obtiene de los Invocadores",
    mesa: "Ninguna",
    img: "assets/craft/totem.png"
  },

  // ==================== ARMADURAS HUMANAS ====================
  {
    nombre: "🪖 Casco de Cuero",
    id: "minecraft:leather_helmet",
    categoria: "Equipo",
    stack: 1,
    durabilidad: 55,
    daño: 0,
    receta: "5 Cuero",
    mesa: "Mesa de crafteo",
    img: "assets/craft/casco_cuero.png"
  },
  {
    nombre: "🦺 Pechera de Cuero",
    id: "minecraft:leather_chestplate",
    categoria: "Equipo",
    stack: 1,
    durabilidad: 80,
    daño: 0,
    receta: "8 Cuero",
    mesa: "Mesa de crafteo",
    img: "assets/craft/pechera_cuero.png"
  },
  {
    nombre: "👖 Pantalones de Cuero",
    id: "minecraft:leather_leggings",
    categoria: "Equipo",
    stack: 1,
    durabilidad: 75,
    daño: 0,
    receta: "7 Cuero",
    mesa: "Mesa de crafteo",
    img: "assets/craft/pantalones_cuero.png"
  },
  {
    nombre: "🥾 Botas de Cuero",
    id: "minecraft:leather_boots",
    categoria: "Equipo",
    stack: 1,
    durabilidad: 65,
    daño: 0,
    receta: "4 Cuero",
    mesa: "Mesa de crafteo",
    img: "assets/craft/botas_cuero.png"
  },
  {
    nombre: "🪖 Casco de Cobre",
    id: "minecraft:copper_helmet",
    categoria: "Equipo",
    stack: 1,
    durabilidad: 121,
    daño: 0,
    receta: "5 Lingotes de cobre",
    mesa: "Mesa de crafteo",
    img: "assets/craft/casco_cobre.png"
  },
  {
    nombre: "🦺 Pechera de Cobre",
    id: "minecraft:copper_chestplate",
    categoria: "Equipo",
    stack: 1,
    durabilidad: 176,
    daño: 0,
    receta: "8 Lingotes de cobre",
    mesa: "Mesa de crafteo",
    img: "assets/craft/pechera_cobre.png"
  },
  {
    nombre: "👖 Pantalones de Cobre",
    id: "minecraft:copper_leggings",
    categoria: "Equipo",
    stack: 1,
    durabilidad: 165,
    daño: 0,
    receta: "7 Lingotes de cobre",
    mesa: "Mesa de crafteo",
    img: "assets/craft/pantalones_cobre.png"
  },
  {
    nombre: "🥾 Botas de Cobre",
    id: "minecraft:copper_boots",
    categoria: "Equipo",
    stack: 1,
    durabilidad: 143,
    daño: 0,
    receta: "4 Lingotes de cobre",
    mesa: "Mesa de crafteo",
    img: "assets/craft/botas_cobre.png"
  },
  {
    nombre: "🪖 Casco de Hierro",
    id: "minecraft:iron_helmet",
    categoria: "Equipo",
    stack: 1,
    durabilidad: 165,
    daño: 0,
    receta: "5 Lingotes de hierro",
    mesa: "Mesa de crafteo",
    img: "assets/craft/casco_hierro.png"
  },
  {
    nombre: "🦺 Pechera de Hierro",
    id: "minecraft:iron_chestplate",
    categoria: "Equipo",
    stack: 1,
    durabilidad: 240,
    daño: 0,
    receta: "8 Lingotes de hierro",
    mesa: "Mesa de crafteo",
    img: "assets/craft/pechera_hierro.png"
  },
  {
    nombre: "👖 Pantalones de Hierro",
    id: "minecraft:iron_leggings",
    categoria: "Equipo",
    stack: 1,
    durabilidad: 225,
    daño: 0,
    receta: "7 Lingotes de hierro",
    mesa: "Mesa de crafteo",
    img: "assets/craft/pantalones_hierro.png"
  },
  {
    nombre: "🥾 Botas de Hierro",
    id: "minecraft:iron_boots",
    categoria: "Equipo",
    stack: 1,
    durabilidad: 195,
    daño: 0,
    receta: "4 Lingotes de hierro",
    mesa: "Mesa de crafteo",
    img: "assets/craft/botas_hierro.png"
  },
  {
    nombre: "🪖 Casco de Oro",
    id: "minecraft:golden_helmet",
    categoria: "Equipo",
    stack: 1,
    durabilidad: 77,
    daño: 0,
    receta: "5 Lingotes de oro",
    mesa: "Mesa de crafteo",
    img: "assets/craft/casco_oro.png"
  },
  {
    nombre: "🦺 Pechera de Oro",
    id: "minecraft:golden_chestplate",
    categoria: "Equipo",
    stack: 1,
    durabilidad: 112,
    daño: 0,
    receta: "8 Lingotes de oro",
    mesa: "Mesa de crafteo",
    img: "assets/craft/pechera_oro.png"
  },
  {
    nombre: "👖 Pantalones de Oro",
    id: "minecraft:golden_leggings",
    categoria: "Equipo",
    stack: 1,
    durabilidad: 105,
    daño: 0,
    receta: "7 Lingotes de oro",
    mesa: "Mesa de crafteo",
    img: "assets/craft/pantalones_oro.png"
  },
  {
    nombre: "🥾 Botas de Oro",
    id: "minecraft:golden_boots",
    categoria: "Equipo",
    stack: 1,
    durabilidad: 91,
    daño: 0,
    receta: "4 Lingotes de oro",
    mesa: "Mesa de crafteo",
    img: "assets/craft/botas_oro.png"
  },
  {
    nombre: "🪖 Casco de Diamante",
    id: "minecraft:diamond_helmet",
    categoria: "Equipo",
    stack: 1,
    durabilidad: 363,
    daño: 0,
    receta: "5 Diamantes",
    mesa: "Mesa de crafteo",
    img: "assets/craft/casco_diamante.png"
  },
  {
    nombre: "🦺 Pechera de Diamante",
    id: "minecraft:diamond_chestplate",
    categoria: "Equipo",
    stack: 1,
    durabilidad: 528,
    daño: 0,
    receta: "8 Diamantes",
    mesa: "Mesa de crafteo",
    img: "assets/craft/pechera_diamante.png"
  },
  {
    nombre: "👖 Pantalones de Diamante",
    id: "minecraft:diamond_leggings",
    categoria: "Equipo",
    stack: 1,
    durabilidad: 495,
    daño: 0,
    receta: "7 Diamantes",
    mesa: "Mesa de crafteo",
    img: "assets/craft/pantalones_diamante.png"
  },
  {
    nombre: "🥾 Botas de Diamante",
    id: "minecraft:diamond_boots",
    categoria: "Equipo",
    stack: 1,
    durabilidad: 429,
    daño: 0,
    receta: "4 Diamantes",
    mesa: "Mesa de crafteo",
    img: "assets/craft/botas_diamante.png"
  },
  {
    nombre: "🪖 Casco de Netherita",
    id: "minecraft:netherite_helmet",
    categoria: "Equipo",
    stack: 1,
    durabilidad: 407,
    daño: 0,
    receta: "1 Casco de diamante + 1 Lingote de netherita + 1 Plantilla",
    mesa: "Mesa de herrería",
    img: "assets/craft/casco_netherita.png"
  },
  {
    nombre: "🦺 Pechera de Netherita",
    id: "minecraft:netherite_chestplate",
    categoria: "Equipo",
    stack: 1,
    durabilidad: 592,
    daño: 0,
    receta: "1 Pechera de diamante + 1 Lingote de netherita + 1 Plantilla",
    mesa: "Mesa de herrería",
    img: "assets/craft/pechera_netherita.png"
  },
  {
    nombre: "👖 Pantalones de Netherita",
    id: "minecraft:netherite_leggings",
    categoria: "Equipo",
    stack: 1,
    durabilidad: 555,
    daño: 0,
    receta: "1 Pantalones de diamante + 1 Lingote de netherita + 1 Plantilla",
    mesa: "Mesa de herrería",
    img: "assets/craft/pantalones_netherita.png"
  },
  {
    nombre: "🥾 Botas de Netherita",
    id: "minecraft:netherite_boots",
    categoria: "Equipo",
    stack: 1,
    durabilidad: 481,
    daño: 0,
    receta: "1 Botas de diamante + 1 Lingote de netherita + 1 Plantilla",
    mesa: "Mesa de herrería",
    img: "assets/craft/botas_netherita.png"
  },

  // ==================== ARMADURAS DE CABALLO ====================
  {
    nombre: "🐴 Armadura de Caballo de Cuero",
    id: "minecraft:leather_horse_armor",
    categoria: "Equipo",
    stack: 1,
    durabilidad: 0,
    daño: 0,
    receta: "7 Cuero",
    mesa: "Mesa de crafteo",
    img: "assets/craft/caballo_cuero.png"
  },
  {
    nombre: "🐴 Armadura de Caballo de Cobre",
    id: "minecraft:copper_horse_armor",
    categoria: "Equipo",
    stack: 1,
    durabilidad: 0,
    daño: 0,
    receta: "7 Lingotes de cobre",
    mesa: "Mesa de crafteo",
    img: "assets/craft/caballo_cobre.png"
  },
  {
    nombre: "🐴 Armadura de Caballo de Hierro",
    id: "minecraft:iron_horse_armor",
    categoria: "Equipo",
    stack: 1,
    durabilidad: 0,
    daño: 0,
    receta: "No se fabrica. Se encuentra en cofres de mazmorras, minas y fortalezas",
    mesa: "Ninguna",
    img: "assets/craft/caballo_hierro.png"
  },
  {
    nombre: "🐴 Armadura de Caballo de Oro",
    id: "minecraft:golden_horse_armor",
    categoria: "Equipo",
    stack: 1,
    durabilidad: 0,
    daño: 0,
    receta: "No se fabrica. Se encuentra en cofres de fortalezas del Nether y templos",
    mesa: "Ninguna",
    img: "assets/craft/caballo_oro.png"
  },
  {
    nombre: "🐴 Armadura de Caballo de Diamante",
    id: "minecraft:diamond_horse_armor",
    categoria: "Equipo",
    stack: 1,
    durabilidad: 0,
    daño: 0,
    receta: "No se fabrica. Se encuentra en cofres de mazmorras, fortalezas y ciudades del End",
    mesa: "Ninguna",
    img: "assets/craft/caballo_diamante.png"
  },
  {
    nombre: "🐴 Armadura de Caballo de Netherita",
    id: "minecraft:netherite_horse_armor",
    categoria: "Equipo",
    stack: 1,
    durabilidad: 0,
    daño: 0,
    receta: "1 Armadura de caballo de diamante + 1 Lingote de netherita + 1 Plantilla",
    mesa: "Mesa de herrería",
    img: "assets/craft/caballo_netherita.png"
  },

  // ==================== ARMADURAS DE NAUTILUS ====================
  {
    nombre: "🐚 Armadura de Nautilus de Cobre",
    id: "minecraft:copper_nautilus_armor",
    categoria: "Equipo",
    stack: 1,
    durabilidad: 0,
    daño: 0,
    receta: "No se fabrica. Se encuentra en cofres de Tesoros Enterrados, Ruinas Oceánicas y Naufragios",
    mesa: "Ninguna",
    img: "assets/craft/nautilus_cobre.png"
  },
  {
    nombre: "🐚 Armadura de Nautilus de Hierro",
    id: "minecraft:iron_nautilus_armor",
    categoria: "Equipo",
    stack: 1,
    durabilidad: 0,
    daño: 0,
    receta: "No se fabrica. Se encuentra en cofres de Tesoros Enterrados, Ruinas Oceánicas y Naufragios",
    mesa: "Ninguna",
    img: "assets/craft/nautilus_hierro.png"
  },
  {
    nombre: "🐚 Armadura de Nautilus de Oro",
    id: "minecraft:golden_nautilus_armor",
    categoria: "Equipo",
    stack: 1,
    durabilidad: 0,
    daño: 0,
    receta: "No se fabrica. Se encuentra en cofres de Tesoros Enterrados, Ruinas Oceánicas y Naufragios",
    mesa: "Ninguna",
    img: "assets/craft/nautilus_oro.png"
  },
  {
    nombre: "🐚 Armadura de Nautilus de Diamante",
    id: "minecraft:diamond_nautilus_armor",
    categoria: "Equipo",
    stack: 1,
    durabilidad: 0,
    daño: 0,
    receta: "No se fabrica. Se encuentra en cofres de Tesoros Enterrados, Ruinas Oceánicas y Naufragios",
    mesa: "Ninguna",
    img: "assets/craft/nautilus_diamante.png"
  },
  {
    nombre: "🐚 Armadura de Nautilus de Netherita",
    id: "minecraft:netherite_nautilus_armor",
    categoria: "Equipo",
    stack: 1,
    durabilidad: 0,
    daño: 0,
    receta: "1 Armadura de Nautilus de diamante + 1 Lingote de netherita + 1 Plantilla",
    mesa: "Mesa de herrería",
    img: "assets/craft/nautilus_netherita.png"
  },

  // ==================== MONTURAS Y RIENDAS ====================
  {
    nombre: "🐴 Silla de Montar",
    id: "minecraft:saddle",
    categoria: "Equipo",
    stack: 1,
    durabilidad: 0,
    daño: 0,
    receta: "No se fabrica. Se encuentra en cofres de mazmorras, fortalezas y templos",
    mesa: "Ninguna",
    img: "assets/craft/silla_montar.png"
  },
  {
    nombre: "🪢 Rienda",
    id: "minecraft:lead",
    categoria: "Equipo",
    stack: 1,
    durabilidad: 0,
    daño: 0,
    receta: "4 Hilos + 1 Bola de Slime (en versiones anteriores a la 1.21.60), 5 Hilos (en versiones posteriores a la 1.21.60)",
    mesa: "Mesa de crafteo",
    img: "assets/craft/rienda1.png, assets/craft/rienda2.png"
  },

  // ==================== COMIDA ====================
  {
    nombre: "🍞 Pan",
    id: "minecraft:bread",
    categoria: "Equipo",
    stack: 64,
    durabilidad: 0,
    daño: 0,
    receta: "3 Trigo",
    mesa: "Mesa de crafteo",
    img: "assets/craft/pan.png"
  },
  {
    nombre: "🍪 Galleta",
    id: "minecraft:cookie",
    categoria: "Equipo",
    stack: 64,
    durabilidad: 0,
    daño: 0,
    receta: "2 Trigo + 1 Cacao",
    mesa: "Mesa de crafteo",
    img: "assets/craft/galleta.png"
  },
  {
    nombre: "🥣 Estofado de Champiñones",
    id: "minecraft:mushroom_stew",
    categoria: "Equipo",
    stack: 1,
    durabilidad: 0,
    daño: 0,
    receta: "2 Champiñones + 1 Cuenco",
    mesa: "Mesa de crafteo",
    img: "assets/craft/estofado_champinones.png"
  },
  {
    nombre: "🥣 Estofado de Conejo",
    id: "minecraft:rabbit_stew",
    categoria: "Equipo",
    stack: 1,
    durabilidad: 0,
    daño: 0,
    receta: "1 Carne de Conejo Cocida + 1 Zanahoria + 1 Patata + 1 Seta + 1 Cuenco",
    mesa: "Mesa de crafteo",
    img: "assets/craft/estofado_conjeo.png"
  },
  {
    nombre: "🥣 Estofado Sospechoso",
    id: "minecraft:suspicious_stew",
    categoria: "Equipo",
    stack: 1,
    durabilidad: 0,
    daño: 0,
    receta: "1 Cuenco + 1 Flor + 1 Champiñón + 1 Seta",
    mesa: "Mesa de crafteo",
    img: "assets/craft/estofado_sospechoso.png"
  },
  {
    nombre: "🥔 Patata Cocida",
    id: "minecraft:baked_potato",
    categoria: "Equipo",
    stack: 64,
    durabilidad: 0,
    daño: 0,
    receta: "1 Patata",
    mesa: "Horno",
    img: "assets/craft/patata_cocida.png"
  },
  {
    nombre: "🍰 Pastel",
    id: "minecraft:cake",
    categoria: "Equipo",
    stack: 1,
    durabilidad: 0,
    daño: 0,
    receta: "3 Leche + 2 Azúcar + 1 Huevo + 3 Trigo",
    mesa: "Mesa de crafteo",
    img: "assets/craft/pastel.png"
  },
  {
    nombre: "🎃 Pastel de Calabaza",
    id: "minecraft:pumpkin_pie",
    categoria: "Equipo",
    stack: 64,
    durabilidad: 0,
    daño: 0,
    receta: "1 Calabaza + 1 Azúcar + 1 Huevo",
    mesa: "Mesa de crafteo",
    img: "assets/craft/pastel_calabaza.png"
  },
  {
    nombre: "🍖 Carne de Vaca Cocida",
    id: "minecraft:cooked_beef",
    categoria: "Equipo",
    stack: 64,
    durabilidad: 0,
    daño: 0,
    receta: "1 Carne de Vaca",
    mesa: "Horno",
    img: "assets/craft/carne_vaca_cocida.png"
  },
  {
    nombre: "🍗 Pollo Cocido",
    id: "minecraft:cooked_chicken",
    categoria: "Equipo",
    stack: 64,
    durabilidad: 0,
    daño: 0,
    receta: "1 Pollo Crudo",
    mesa: "Horno",
    img: "assets/craft/pollo_cocido.png"
  },
  {
    nombre: "🥓 Chuleta de Cerdo Cocida",
    id: "minecraft:cooked_porkchop",
    categoria: "Equipo",
    stack: 64,
    durabilidad: 0,
    daño: 0,
    receta: "1 Chuleta de Cerdo Cruda",
    mesa: "Horno",
    img: "assets/craft/chuleta_cocida.png"
  },
  {
    nombre: "🐟 Salmón Cocido",
    id: "minecraft:cooked_salmon",
    categoria: "Equipo",
    stack: 64,
    durabilidad: 0,
    daño: 0,
    receta: "1 Salmón Crudo",
    mesa: "Horno",
    img: "assets/craft/salmon_cocido.png"
  },
  {
    nombre: "🐟 Bacalao Cocido",
    id: "minecraft:cooked_cod",
    categoria: "Equipo",
    stack: 64,
    durabilidad: 0,
    daño: 0,
    receta: "1 Bacalao Crudo",
    mesa: "Horno",
    img: "assets/craft/bacalao_cocido.png"
  },
  {
    nombre: "🍖 Cordero Cocido",
    id: "minecraft:cooked_mutton",
    categoria: "Equipo",
    stack: 64,
    durabilidad: 0,
    daño: 0,
    receta: "1 Cordero Crudo",
    mesa: "Horno",
    img: "assets/craft/cordero_cocido.png"
  },
  {
    nombre: "🥔 Patata Venenosa",
    id: "minecraft:poisonous_potato",
    categoria: "Equipo",
    stack: 64,
    durabilidad: 0,
    daño: 0,
    receta: "No se fabrica. Se obtiene al cosechar patatas",
    mesa: "Ninguna",
    img: "assets/craft/patata_venenosa.png"
  },
  {
    nombre: "🌿 Alga Marina Seca",
    id: "minecraft:dried_kelp",
    categoria: "Equipo",
    stack: 64,
    durabilidad: 0,
    daño: 0,
    receta: "1 Alga Marina",
    mesa: "Horno",
    img: "assets/craft/alga_seca.png"
  },

  // ==================== BOLAS DE NIEVE Y CAPARAZÓN ====================
  {
    nombre: "❄️ Bola de Nieve",
    id: "minecraft:snowball",
    categoria: "Equipo",
    stack: 16,
    durabilidad: 0,
    daño: 0,
    receta: "4 Bolas de Nieve (de nieve)",
    mesa: "Mesa de crafteo",
    img: "assets/craft/bola_nieve.png"
  },
  {
    nombre: "🐢 Caparazón de Tortuga",
    id: "minecraft:turtle_helmet",
    categoria: "Equipo",
    stack: 1,
    durabilidad: 275,
    daño: 0,
    receta: "5 Escamas de Tortuga",
    mesa: "Mesa de crafteo",
    img: "assets/craft/caparazon_tortuga.png"
  },

  // ==================== BOTELLAS ====================
  {
    nombre: "🍾 Botella Vacía",
    id: "minecraft:glass_bottle",
    categoria: "Equipo",
    stack: 64,
    durabilidad: 0,
    daño: 0,
    receta: "3 Vidrio",
    mesa: "Mesa de crafteo",
    img: "assets/craft/botella_vacia.png"
  },
  {
    nombre: "✨ Botella de Experiencia",
    id: "minecraft:experience_bottle",
    categoria: "Equipo",
    stack: 64,
    durabilidad: 0,
    daño: 0,
    receta: "No se fabrica. Se obtiene de comerciar con clérigos o de cofres",
    mesa: "Ninguna",
    img: "assets/craft/botella_experiencia.png"
  }
];

module.exports = items;
