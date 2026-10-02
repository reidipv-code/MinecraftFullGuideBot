from __future__ import annotations

import json
import re
import time
import unicodedata
from pathlib import Path
from urllib.request import Request, urlopen


# ============================================================
# DATOS: MINECRAFT JAVA 26.1
# ============================================================

ITEMS_URL = (
    "https://raw.githubusercontent.com/"
    "PrismarineJS/minecraft-data/master/"
    "data/pc/26.1/items.json"
)

RECIPES_URL = (
    "https://raw.githubusercontent.com/"
    "PrismarineJS/minecraft-data/master/"
    "data/pc/26.1/recipes.json"
)

# Traducciones oficiales del cliente 26.1.2
LANG_URL = (
    "https://assets.mcasset.cloud/"
    "26.1.2/assets/minecraft/lang/es_es.json"
)


# ============================================================
# CACHE
# ============================================================

CACHE = Path("/tmp/minecraft_fullguide_data")

ITEMS_CACHE = CACHE / "items_26.1.json"
RECIPES_CACHE = CACHE / "recipes_26.1.json"
LANG_CACHE = CACHE / "es_es_26.1.2.json"

CACHE_AGE = 7 * 24 * 60 * 60


# ============================================================
# ALIAS EN ESPAÑOL
# ============================================================

ALIASES = {

    "mesa": "crafting_table",
    "mesa de crafteo": "crafting_table",
    "mesa de trabajo": "crafting_table",
    "mesa de fabricacion": "crafting_table",
    "mesa de fabricación": "crafting_table",

    "horno": "furnace",
    "alto horno": "blast_furnace",
    "ahumador": "smoker",

    "cristal": "glass",
    "vidrio": "glass",

    "arena": "sand",
    "adoquin": "cobblestone",
    "adoquín": "cobblestone",

    "piedra": "stone",

    "carbon": "coal",
    "carbón": "coal",
    "carbón mineral": "coal",

    "carbon vegetal": "charcoal",
    "carbón vegetal": "charcoal",

    "diamante": "diamond",
    "diamantes": "diamond",

    "hierro": "iron_ingot",
    "lingote de hierro": "iron_ingot",

    "oro": "gold_ingot",
    "lingote de oro": "gold_ingot",

    "esmeralda": "emerald",

    "redstone": "redstone",

    "lapislazuli": "lapis_lazuli",
    "lapislázuli": "lapis_lazuli",

    "palo": "stick",
    "palos": "stick",

    "pico": "pickaxe",
    "espada": "sword",
    "hacha": "axe",
    "pala": "shovel",
    "azada": "hoe",

    "arco": "bow",
    "flecha": "arrow",

    "cubeta": "bucket",
    "cubo": "bucket",

    "cofre": "chest",

    "tierra": "dirt",
    "grava": "gravel",

    "obsidiana": "obsidian",

    "netherita": "netherite_ingot",
    "lingote de netherita": "netherite_ingot",

    "escombros ancestrales": "ancient_debris",
}


# ============================================================
# MATERIALES
# ============================================================

MATERIALS = {

    "madera": "oak",

    "roble": "oak",

    "abedul": "birch",

    "abeto": "spruce",
    "pino": "spruce",

    "jungla": "jungle",

    "acacia": "acacia",

    "roble oscuro": "dark_oak",

    "manglar": "mangrove",
    "mangle": "mangrove",

    "cerezo": "cherry",

    "bambu": "bamboo",
    "bambú": "bamboo",

    "roble palido": "pale_oak",
    "roble pálido": "pale_oak",

    "crimson": "crimson",
    "carmesí": "crimson",

    "warped": "warped",
    "distorsionado": "warped",

    "piedra": "stone",

    "hierro": "iron",
    "oro": "gold",
    "diamante": "diamond",
    "netherita": "netherite",
}


# ============================================================
# HERRAMIENTAS
# ============================================================

TOOLS = {

    "pico": "pickaxe",
    "espada": "sword",
    "hacha": "axe",
    "pala": "shovel",
    "azada": "hoe",

}


# ============================================================
# RECETAS DE HORNO
#
# minecraft-data Java no guarda todas las recetas de horno
# dentro del recipes.json de fabricación.
# ============================================================

FURNACE_RECIPES = {

    # Bloques / materiales
    "sand": ("glass", "Horno"),
    "red_sand": ("red_stained_glass", "Horno"),

    "cobblestone": ("stone", "Horno"),
    "stone": ("smooth_stone", "Horno"),

    "clay_ball": ("brick", "Horno"),
    "clay": ("terracotta", "Horno"),

    "cactus": ("green_dye", "Horno"),
    "kelp": ("dried_kelp", "Horno"),

    "wet_sponge": ("sponge", "Horno"),

    "ancient_debris": (
        "netherite_scrap",
        "Horno",
    ),

    "netherrack": (
        "nether_brick",
        "Horno",
    ),

    "quartz_ore": (
        "quartz",
        "Horno",
    ),

    "nether_quartz_ore": (
        "quartz",
        "Horno",
    ),

    "chorus_fruit": (
        "popped_chorus_fruit",
        "Horno",
    ),

    "potato": (
        "baked_potato",
        "Horno",
    ),

    # Minerales
    "raw_iron": (
        "iron_ingot",
        "Horno",
    ),

    "raw_gold": (
        "gold_ingot",
        "Horno",
    ),

    "raw_copper": (
        "copper_ingot",
        "Horno",
    ),

    "iron_ore": (
        "iron_ingot",
        "Horno",
    ),

    "deepslate_iron_ore": (
        "iron_ingot",
        "Horno",
    ),

    "gold_ore": (
        "gold_ingot",
        "Horno",
    ),

    "deepslate_gold_ore": (
        "gold_ingot",
        "Horno",
    ),

    "copper_ore": (
        "copper_ingot",
        "Horno",
    ),

    "deepslate_copper_ore": (
        "copper_ingot",
        "Horno",
    ),

    "coal_ore": (
        "coal",
        "Horno",
    ),

    "deepslate_coal_ore": (
        "coal",
        "Horno",
    ),

    "diamond_ore": (
        "diamond",
        "Horno",
    ),

    "deepslate_diamond_ore": (
        "diamond",
        "Horno",
    ),

    "emerald_ore": (
        "emerald",
        "Horno",
    ),

    "deepslate_emerald_ore": (
        "emerald",
        "Horno",
    ),

    "lapis_ore": (
        "lapis_lazuli",
        "Horno",
    ),

    "deepslate_lapis_ore": (
        "lapis_lazuli",
        "Horno",
    ),

    "redstone_ore": (
        "redstone",
        "Horno",
    ),

    "deepslate_redstone_ore": (
        "redstone",
        "Horno",
    ),

    # Madera → carbón vegetal
    "oak_log": ("charcoal", "Horno"),
    "spruce_log": ("charcoal", "Horno"),
    "birch_log": ("charcoal", "Horno"),
    "jungle_log": ("charcoal", "Horno"),
    "acacia_log": ("charcoal", "Horno"),
    "dark_oak_log": ("charcoal", "Horno"),
    "mangrove_log": ("charcoal", "Horno"),
    "cherry_log": ("charcoal", "Horno"),
    "pale_oak_log": ("charcoal", "Horno"),

    # Comida
    "beef": (
        "cooked_beef",
        "Horno",
    ),

    "porkchop": (
        "cooked_porkchop",
        "Horno",
    ),

    "chicken": (
        "cooked_chicken",
        "Horno",
    ),

    "mutton": (
        "cooked_mutton",
        "Horno",
    ),

    "rabbit": (
        "cooked_rabbit",
        "Horno",
    ),

    "cod": (
        "cooked_cod",
        "Horno",
    ),

    "salmon": (
        "cooked_salmon",
        "Horno",
    ),
}


# ============================================================
# ALTO HORNO
# ============================================================

BLAST_RECIPES = {

    key: (
        value[0],
        "Alto horno",
    )

    for key, value in FURNACE_RECIPES.items()

    if (
        key.endswith("_ore")
        or key.startswith("deepslate_")
        or key.startswith("raw_")
        or key == "ancient_debris"
    )
}


# ============================================================
# AHUMADOR
# ============================================================

SMOKER_RECIPES = {

    "beef": (
        "cooked_beef",
        "Ahumador",
    ),

    "porkchop": (
        "cooked_porkchop",
        "Ahumador",
    ),

    "chicken": (
        "cooked_chicken",
        "Ahumador",
    ),

    "mutton": (
        "cooked_mutton",
        "Ahumador",
    ),

    "rabbit": (
        "cooked_rabbit",
        "Ahumador",
    ),

    "cod": (
        "cooked_cod",
        "Ahumador",
    ),

    "salmon": (
        "cooked_salmon",
        "Ahumador",
    ),

    "potato": (
        "baked_potato",
        "Ahumador",
    ),
}


# ============================================================
# NORMALIZACIÓN
# ============================================================

def norm(value: str) -> str:

    value = unicodedata.normalize(
        "NFD",
        str(value).lower().strip(),
    )

    value = "".join(
        c
        for c in value
        if unicodedata.category(c) != "Mn"
    )

    value = value.replace(
        "minecraft:",
        "",
    )

    value = re.sub(
        r"[^a-z0-9_ ]+",
        " ",
        value,
    )

    return re.sub(
        r"\s+",
        " ",
        value,
    ).strip()


# ============================================================
# ID
# ============================================================

def clean_id(
    value,
    id_to_name=None,
):

    if value is None:
        return None

    if isinstance(value, dict):

        value = (
            value.get("name")
            or value.get("item")
            or value.get("id")
            or value.get("identifier")
        )

    if isinstance(
        value,
        (list, tuple),
    ):

        value = (
            value[0]
            if value
            else None
        )

    if isinstance(
        value,
        int,
    ):

        if id_to_name:
            return id_to_name.get(
                value
            )

        return None

    if isinstance(
        value,
        float,
    ) and value.is_integer():

        if id_to_name:
            return id_to_name.get(
                int(value)
            )

        return None

    if value is None:
        return None

    return str(value).replace(
        "minecraft:",
        "",
    ).strip()


# ============================================================
# DESCARGAR JSON
# ============================================================

def load_json(
    url: str,
    path: Path,
):

    CACHE.mkdir(
        parents=True,
        exist_ok=True,
    )

    if (
        path.exists()
        and time.time()
        - path.stat().st_mtime
        < CACHE_AGE
    ):

        try:

            return json.loads(
                path.read_text(
                    encoding="utf-8"
                )
            )

        except Exception:
            pass

    req = Request(
        url,
        headers={
            "User-Agent":
                "MinecraftFullGuideBot/2.0"
        },
    )

    with urlopen(
        req,
        timeout=60,
    ) as response:

        data = response.read()

    path.write_bytes(data)

    return json.loads(
        data.decode("utf-8")
    )


# ============================================================
# IDIOMA ESPAÑOL
# ============================================================

def load_language():

    try:

        return load_json(
            LANG_URL,
            LANG_CACHE,
        )

    except Exception:

        return {}


# ============================================================
# NOMBRE TRADUCIDO
# ============================================================

def translated_name(
    ident,
    lang,
):

    ident = str(
        ident
    ).replace(
        "minecraft:",
        "",
    )

    keys = (
        f"item.minecraft.{ident}",
        f"block.minecraft.{ident}",
    )

    for key in keys:

        value = lang.get(
            key
        )

        if value:
            return str(value)

    return (
        ident
        .replace("_", " ")
        .title()
    )


# ============================================================
# CANTIDAD
# ============================================================

def value_count(value):

    if isinstance(
        value,
        dict,
    ):

        return int(
            value.get("count")
            or value.get("quantity")
            or value.get("amount")
            or 1
        )

    return 1


# ============================================================
# INGREDIENTE
# ============================================================

def make_ingredient(
    value,
    id_to_name,
    lang,
):

    ident = clean_id(
        value,
        id_to_name,
    )

    if not ident:
        return None

    if ident == "air":
        return None

    return {

        "id": ident,

        "nombre":
            translated_name(
                ident,
                lang,
            ),

        "cantidad":
            value_count(
                value
            ),
    }


# ============================================================
# CREAR CUADRÍCULA 3x3
# ============================================================

def make_grid(
    shape,
    id_to_name,
):

    if not isinstance(
        shape,
        list,
    ):
        return None

    if not shape:
        return None

    height = min(
        3,
        len(shape),
    )

    width = min(
        3,
        max(
            (
                len(row)
                for row in shape
                if isinstance(
                    row,
                    list,
                )
            ),
            default=0,
        ),
    )

    if not width:
        return None

    grid = [
        [None, None, None],
        [None, None, None],
        [None, None, None],
    ]

    offset_y = (
        3 - height
    ) // 2

    offset_x = (
        3 - width
    ) // 2

    for y, row in enumerate(
        shape[:3]
    ):

        if not isinstance(
            row,
            list,
        ):
            continue

        for x, value in enumerate(
            row[:3]
        ):

            ident = clean_id(
                value,
                id_to_name,
            )

            if (
                ident
                and ident != "air"
            ):

                grid[
                    y + offset_y
                ][
                    x + offset_x
                ] = ident

    if any(
        cell
        for row in grid
        for cell in row
    ):

        return grid

    return None


# ============================================================
# RECETAS DE CRAFTEO
# ============================================================

def build_crafting_recipes(
    raw,
    id_to_name,
    lang,
):

    result = {}

    if not isinstance(
        raw,
        dict,
    ):
        return result

    for recipes in raw.values():

        if not isinstance(
            recipes,
            list,
        ):

            recipes = [
                recipes
            ]

        for recipe in recipes:

            if not isinstance(
                recipe,
                dict,
            ):
                continue

            output = make_ingredient(
                recipe.get("result"),
                id_to_name,
                lang,
            )

            if not output:
                continue

            grid = make_grid(
                recipe.get("inShape"),
                id_to_name,
            )

            ingredients = []

            # ------------------------------------------------
            # RECETA CON FORMA
            # ------------------------------------------------

            if grid:

                for row in grid:

                    for ident in row:

                        if ident:

                            ingredients.append({

                                "id": ident,

                                "nombre":
                                    translated_name(
                                        ident,
                                        lang,
                                    ),

                                "cantidad": 1,

                            })

            # ------------------------------------------------
            # RECETA SIN FORMA
            # ------------------------------------------------

            else:

                for value in recipe.get(
                    "ingredients",
                    [],
                ):

                    ingredient = make_ingredient(
                        value,
                        id_to_name,
                        lang,
                    )

                    if ingredient:

                        ingredients.append(
                            ingredient
                        )

                if ingredients:

                    grid = [
                        [None, None, None],
                        [None, None, None],
                        [None, None, None],
                    ]

                    positions = [

                        (1, 1),
                        (0, 1),
                        (1, 0),
                        (1, 2),
                        (2, 1),

                        (0, 0),
                        (0, 2),
                        (2, 0),
                        (2, 2),

                    ]

                    for (
                        position,
                        ingredient,
                    ) in zip(
                        positions,
                        ingredients[:9],
                    ):

                        grid[
                            position[0]
                        ][
                            position[1]
                        ] = ingredient["id"]

            if not grid:
                continue

            data = {

                "tipo":
                    "crafting",

                "mesa":
                    "Mesa de crafteo",

                "estacion":
                    "Mesa de crafteo",

                "patron":
                    grid,

                "ingredientes":
                    ingredients,

                "resultado_cantidad":
                    output["cantidad"],

            }

            ident = output["id"]

            if ident not in result:

                result[ident] = data

            else:

                result[
                    ident
                ].setdefault(
                    "alternativas",
                    [],
                ).append(
                    data
                )

    return result


# ============================================================
# CONSTRUIR BASE COMPLETA
# ============================================================

def build():

    raw_items = load_json(
        ITEMS_URL,
        ITEMS_CACHE,
    )

    raw_recipes = load_json(
        RECIPES_URL,
        RECIPES_CACHE,
    )

    lang = load_language()

    items_list = (
        raw_items
        if isinstance(
            raw_items,
            list,
        )
        else raw_items.get(
            "items",
            [],
        )
    )

    id_to_name = {}

    for data in items_list:

        if not isinstance(
            data,
            dict,
        ):
            continue

        ident = str(
            data.get("name")
            or ""
        ).replace(
            "minecraft:",
            "",
        )

        if not ident:
            continue

        try:

            id_to_name[
                int(
                    data["id"]
                )
            ] = ident

        except Exception:
            pass

    crafting_recipes = (
        build_crafting_recipes(
            raw_recipes,
            id_to_name,
            lang,
        )
    )

    items = {}

    # ========================================================
    # TODOS LOS ITEMS
    # ========================================================

    for data in items_list:

        if not isinstance(
            data,
            dict,
        ):
            continue

        ident = str(
            data.get("name")
            or ""
        ).replace(
            "minecraft:",
            "",
        )

        if (
            not ident
            or ident == "air"
        ):
            continue

        name = translated_name(
            ident,
            lang,
        )

        items[ident] = {

            "id":
                ident,

            "nombre":
                name,

            "identificador":
                f"minecraft:{ident}",

            "aliases": [
                norm(ident),
                norm(name),
            ],

            "categoria":
                "Objeto",

            "descripcion":
                f"Objeto de Minecraft: {name}.",

            "danio":
                data.get(
                    "damage"
                )
                or data.get(
                    "attackDamage"
                ),

            "velocidad_mineria":
                data.get(
                    "miningSpeed"
                )
                or data.get(
                    "mining_speed"
                ),

            "durabilidad":
                data.get(
                    "maxDurability"
                )
                or data.get(
                    "max_durability"
                ),

            "stack_size":
                data.get(
                    "stackSize"
                )
                or 64,

            "receta":
                crafting_recipes.get(
                    ident
                ),

            "variaciones":
                data.get(
                    "variations"
                )
                or [],

        }

    # ========================================================
    # ALIAS BÁSICOS
    # ========================================================

    for alias, ident in (
        ALIASES.items()
    ):

        if ident in items:

            items[ident][
                "aliases"
            ].append(
                norm(alias)
            )

    # ========================================================
    # HERRAMIENTAS COMPUESTAS
    #
    # pico de diamante
    # espada de hierro
    # etc.
    # ========================================================

    for (
        material_es,
        material_id,
    ) in MATERIALS.items():

        for (
            tool_es,
            tool_id,
        ) in TOOLS.items():

            ident = (
                f"{material_id}_"
                f"{tool_id}"
            )

            if ident not in items:
                continue

            items[ident][
                "aliases"
            ].extend([

                norm(
                    f"{tool_es} "
                    f"de "
                    f"{material_es}"
                ),

                norm(
                    f"{tool_es} "
                    f"{material_es}"
                ),

            ])

    # ========================================================
    # RECETAS ESPECIALES
    # ========================================================

    special_recipes = {}

    special_recipes.update(
        FURNACE_RECIPES
    )

    special_recipes.update(
        BLAST_RECIPES
    )

    special_recipes.update(
        SMOKER_RECIPES
    )

    for (
        input_id,
        (
            output_id,
            station,
        ),
    ) in special_recipes.items():

        if input_id not in items:
            continue

        if output_id not in items:
            continue

        special_recipe = {

            "tipo":
                "smelting",

            "mesa":
                station,

            "estacion":
                station,

            "entrada":
                input_id,

            "patron": [

                [None, None, None],
                [None, None, None],
                [None, None, None],

            ],

            "ingredientes": [

                {

                    "id":
                        input_id,

                    "nombre":
                        items[input_id][
                            "nombre"
                        ],

                    "cantidad":
                        1,

                }

            ],

            "resultado_cantidad":
                1,

        }

        special_recipe[
            "patron"
        ][1][1] = input_id

        # Si no tiene crafteo, esta pasa a ser
        # la receta principal.
        if not items[output_id].get(
            "receta"
        ):

            items[output_id][
                "receta"
            ] = special_recipe

        else:

            # Si tiene varias formas de obtenerse,
            # conservamos todas.
            items[output_id][
                "receta"
            ].setdefault(
                "alternativas",
                [],
            ).append(
                special_recipe
            )

    return items


# ============================================================
# BASE GLOBAL
# ============================================================

ITEMS = None


# ============================================================
# BUSCAR HERRAMIENTA COMPUESTA
# ============================================================

def compound_lookup(
    query,
):

    if not ITEMS:
        return None

    words = [

        word

        for word in query.split()

        if word not in {

            "de",
            "del",
            "la",
            "el",
            "los",
            "las",
            "un",
            "una",

        }

    ]

    if len(words) < 2:
        return None

    tool_id = None
    material_id = None

    for word in words:

        if word in TOOLS:

            tool_id = TOOLS[
                word
            ]

        if word in MATERIALS:

            material_id = MATERIALS[
                word
            ]

    if not tool_id:
        return None

    if not material_id:
        return None

    ident = (
        f"{material_id}_"
        f"{tool_id}"
    )

    return ITEMS.get(
        ident
    )


# ============================================================
# BUSCAR ITEM
# ============================================================

def buscar_item(
    consulta,
):

    global ITEMS

    if ITEMS is None:

        ITEMS = build()

    query = norm(
        consulta
    )

    if not query:
        return None

    # ========================================================
    # ALIAS EXACTO
    # ========================================================

    if query in ALIASES:

        ident = ALIASES[
            query
        ]

        if ident in ITEMS:

            return ITEMS[
                ident
            ]

    # ========================================================
    # ID EXACTO
    # ========================================================

    if query in ITEMS:

        return ITEMS[
            query
        ]

    # ========================================================
    # COMPUESTO
    # ========================================================

    item = compound_lookup(
        query
    )

    if item:
        return item

    # ========================================================
    # NOMBRE EXACTO
    # ========================================================

    for item in ITEMS.values():

        if query == norm(
            item["id"]
        ):

            return item

        if query == norm(
            item["nombre"]
        ):

            return item

        aliases = {

            norm(alias)

            for alias in item.get(
                "aliases",
                [],
            )

        }

        if query in aliases:

            return item

    # ========================================================
    # BÚSQUEDA POR PALABRAS
    #
    # Solo devuelve coincidencias si TODAS las palabras
    # importantes aparecen.
    # ========================================================

    words = [

        word

        for word in query.split()

        if word not in {

            "de",
            "del",
            "la",
            "el",
            "los",
            "las",
            "un",
            "una",

        }

    ]

    best = None
    best_score = 0

    for item in ITEMS.values():

        tokens = set()

        names = [

            item.get(
                "id",
                ""
            ),

            item.get(
                "nombre",
                ""
            ),

        ]

        names.extend(
            item.get(
                "aliases",
                [],
            )
        )

        for name in names:

            normalized = norm(
                name
            )

            tokens.update(
                normalized
                .replace(
                    "_",
                    " ",
                )
                .split()
            )

        if not words:
            continue

        if not all(
            word in tokens
            for word in words
        ):
            continue

        score = sum(
            5
            for word in words
            if word in tokens
        )

        score += 20

        if score > best_score:

            best_score = score
            best = item

    if best_score < 20:

        return None

    return best


# ============================================================
# TODOS LOS ITEMS
# ============================================================

def obtener_items():

    global ITEMS

    if ITEMS is None:

        ITEMS = build()

    return ITEMS


# ============================================================
# ESTADÍSTICAS
# ============================================================

def obtener_estadisticas():

    items = obtener_items()

    con_receta = sum(

        1

        for item in items.values()

        if item.get(
            "receta"
        )

    )

    return {

        "total_items":
            len(items),

        "con_receta":
            con_receta,

        "sin_receta":
            len(items) - con_receta,

        "version":
            "Minecraft Java 26.1.2",

    }
