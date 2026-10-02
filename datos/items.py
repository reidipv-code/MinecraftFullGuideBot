from __future__ import annotations

import json
import re
import time
import unicodedata
from pathlib import Path
from urllib.request import Request, urlopen


# ============================================================
# FUENTES DE DATOS
# ============================================================

ITEMS_URL = (
    "https://raw.githubusercontent.com/"
    "PrismarineJS/minecraft-data/master/"
    "data/bedrock/1.26.30/items.json"
)

RECIPES_URL = (
    "https://raw.githubusercontent.com/"
    "PrismarineJS/minecraft-data/master/"
    "data/bedrock/1.19.10/recipes.json"
)


# ============================================================
# CACHE
# ============================================================

CACHE = Path("/tmp/minecraft_fullguide_data")

ITEMS_CACHE = CACHE / "items.json"
RECIPES_CACHE = CACHE / "recipes.json"

CACHE_AGE = 7 * 24 * 60 * 60


# ============================================================
# ALIASES EN ESPAÑOL
# ============================================================

ALIASES = {
    "mesa de crafteo": "crafting_table",
    "mesa de trabajo": "crafting_table",
    "mesa de fabricacion": "crafting_table",
    "mesa de fabricación": "crafting_table",

    "piedra base": "bedrock",

    "adoquin": "cobblestone",
    "adoquín": "cobblestone",

    "carbon": "coal",
    "carbón": "coal",

    "diamante": "diamond",
    "diamantes": "diamond",

    "hierro": "iron",
    "oro": "gold",
    "esmeralda": "emerald",
    "redstone": "redstone",

    "lapislazuli": "lapis_lazuli",
    "lapislázuli": "lapis_lazuli",

    "palo": "stick",
    "palos": "stick",

    "pico": "pickaxe",
    "picos": "pickaxe",

    "espada": "sword",
    "espadas": "sword",

    "hacha": "axe",
    "hachas": "axe",

    "pala": "shovel",
    "palas": "shovel",

    "azada": "hoe",
    "azadas": "hoe",

    "arco": "bow",
    "flecha": "arrow",

    "cubeta": "bucket",
    "cubo": "bucket",

    "horno": "furnace",

    "cofre": "chest",

    "vidrio": "glass",

    "arena": "sand",
    "grava": "gravel",
    "tierra": "dirt",

    "madera": "planks",
    "tablones": "planks",

    "tronco": "log",

    "libro": "book",
    "papel": "paper",
}


# ============================================================
# MATERIALES
# ============================================================

MATERIALS = {
    "madera": "wood",
    "madera de roble": "oak",
    "roble": "oak",

    "abedul": "birch",
    "madera de abedul": "birch",

    "abeto": "spruce",
    "madera de abeto": "spruce",

    "jungla": "jungle",
    "madera de jungla": "jungle",

    "acacia": "acacia",
    "madera de acacia": "acacia",

    "roble oscuro": "dark_oak",
    "madera de roble oscuro": "dark_oak",

    "manglar": "mangrove",
    "madera de manglar": "mangrove",

    "cerezo": "cherry",
    "madera de cerezo": "cherry",

    "bambu": "bamboo",
    "bambú": "bamboo",

    "piedra": "stone",
    "adoquin": "cobblestone",
    "adoquín": "cobblestone",
    "cobblestone": "cobblestone",

    "hierro": "iron",
    "oro": "gold",
    "diamante": "diamond",

    "netherita": "netherite",
    "netherite": "netherite",
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
# NORMALIZACIÓN
# ============================================================

def norm(s: str) -> str:

    s = unicodedata.normalize(
        "NFD",
        str(s).lower().strip(),
    )

    s = "".join(
        c
        for c in s
        if unicodedata.category(c) != "Mn"
    )

    s = s.replace(
        "minecraft:",
        "",
    )

    s = re.sub(
        r"[^a-z0-9_ ]+",
        " ",
        s,
    )

    return re.sub(
        r"\s+",
        " ",
        s,
    ).strip()


# ============================================================
# LIMPIAR IDENTIFICADORES
# ============================================================

def clean_id(value):

    if value is None:
        return None

    if isinstance(value, dict):

        value = (
            value.get("name")
            or value.get("item")
            or value.get("id")
            or value.get("identifier")
        )

    if value is None:
        return None

    if isinstance(value, (int, float)):
        return None

    value = str(value)

    value = value.replace(
        "minecraft:",
        "",
    )

    return value


# ============================================================
# DESCARGAR JSON
# ============================================================

def load_json(url: str, path: Path):

    CACHE.mkdir(
        parents=True,
        exist_ok=True,
    )

    if (
        path.exists()
        and time.time() - path.stat().st_mtime
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
                "MinecraftFullGuideBot/1.0"
        },
    )

    with urlopen(
        req,
        timeout=40,
    ) as response:

        data = response.read()

    path.write_bytes(data)

    return json.loads(
        data.decode("utf-8")
    )


# ============================================================
# NOMBRE DEL ITEM
# ============================================================

def item_name(display, ident):

    if display:
        return str(display)

    return (
        ident
        .replace("_", " ")
        .title()
    )


# ============================================================
# INGREDIENTE
# ============================================================

def ingredient(value):

    if value is None:
        return None

    # --------------------------------------------
    # Diccionario
    # --------------------------------------------

    if isinstance(value, dict):

        ident = clean_id(value)

        if not ident:
            return None

        count = (
            value.get("count")
            or value.get("quantity")
            or value.get("amount")
            or 1
        )

    # --------------------------------------------
    # String
    # --------------------------------------------

    elif isinstance(value, str):

        ident = clean_id(value)

        if not ident:
            return None

        count = 1

    else:
        return None

    try:
        count = int(count)
    except Exception:
        count = 1

    return {
        "id": ident,
        "nombre": (
            ident
            .replace("_", " ")
            .title()
        ),
        "cantidad": count,
    }


# ============================================================
# EXTRAER INGREDIENTES DE LISTAS
# ============================================================

def extract_ingredients(values):

    result = []

    if not isinstance(values, list):
        return result

    for value in values:

        # Algunas estructuras contienen listas.
        if isinstance(value, list):

            for nested in value:

                item = ingredient(nested)

                if item:
                    result.append(item)

        else:

            item = ingredient(value)

            if item:
                result.append(item)

    return result


# ============================================================
# PATRÓN DE RECETA
# ============================================================

def recipe_pattern(recipe):

    # ========================================================
    # FORMATO BEDROCK
    #
    # pattern + key
    # ========================================================

    pattern = recipe.get("pattern")

    if isinstance(
        pattern,
        list,
    ) and pattern:

        key = recipe.get(
            "key",
            {},
        )

        grid = [
            [None, None, None],
            [None, None, None],
            [None, None, None],
        ]

        height = min(
            3,
            len(pattern),
        )

        width = min(
            3,
            max(
                (
                    len(row)
                    for row in pattern
                    if isinstance(
                        row,
                        str,
                    )
                ),
                default=0,
            ),
        )

        offset_y = (
            3 - height
        ) // 2

        offset_x = (
            3 - width
        ) // 2

        for y, row in enumerate(
            pattern[:3]
        ):

            if not isinstance(
                row,
                str,
            ):
                continue

            for x, symbol in enumerate(
                row[:3]
            ):

                if symbol in (
                    "",
                    " ",
                    None,
                ):
                    continue

                value = key.get(
                    symbol
                )

                if isinstance(
                    value,
                    list,
                ):

                    value = (
                        value[0]
                        if value
                        else None
                    )

                ident = clean_id(
                    value
                )

                if ident:

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

    # ========================================================
    # FORMATO MINECRAFT-DATA
    #
    # inShape
    # ========================================================

    shape = recipe.get(
        "inShape"
    )

    if isinstance(
        shape,
        list,
    ) and shape:

        grid = [
            [None, None, None],
            [None, None, None],
            [None, None, None],
        ]

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

                if value in (
                    None,
                    "",
                    0,
                    False,
                ):
                    continue

                ident = clean_id(
                    value
                )

                if ident:

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

    # ========================================================
    # FORMATO BEDROCK input
    # ========================================================

    input_grid = recipe.get(
        "input"
    )

    if isinstance(
        input_grid,
        list,
    ) and input_grid:

        # Si input ya viene como matriz.
        if any(
            isinstance(x, list)
            for x in input_grid
        ):

            rows = input_grid

            height = min(
                3,
                len(rows),
            )

            width = min(
                3,
                max(
                    (
                        len(row)
                        for row in rows
                        if isinstance(
                            row,
                            list,
                        )
                    ),
                    default=0,
                ),
            )

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
                rows[:3]
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
                        value
                    )

                    if ident:

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

    # ========================================================
    # RECETA SIN FORMA
    #
    # Colocamos ingredientes en una
    # cuadrícula 3x3.
    # ========================================================

    ingredients = (
        recipe.get("ingredients")
        or recipe.get("input")
        or []
    )

    flat = extract_ingredients(
        ingredients
    )

    if flat:

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

        for position, item in zip(
            positions,
            flat[:9],
        ):

            y, x = position

            grid[y][x] = item["id"]

        return grid

    return None


# ============================================================
# RECETAS
# ============================================================

def build_recipes(raw):

    if isinstance(
        raw,
        dict,
    ):

        recipes = raw.get(
            "recipes"
        )

        if recipes is None:

            recipes = raw.get(
                "data"
            )

        if recipes is None:
            recipes = raw

    else:
        recipes = raw

    result = {}

    # ========================================================
    # NUEVO FORMATO BEDROCK:
    #
    # {
    #   "123": {
    #       "type": "...",
    #       "name": "...",
    #       "ingredients": [...],
    #       "input": [...],
    #       "output": [...]
    #   }
    # }
    # ========================================================

    if isinstance(
        recipes,
        dict,
    ):

        iterator = []

        for key, value in recipes.items():

            if isinstance(
                value,
                list,
            ):

                for recipe in value:

                    if isinstance(
                        recipe,
                        dict,
                    ):
                        iterator.append(
                            recipe
                        )

            elif isinstance(
                value,
                dict,
            ):

                iterator.append(
                    value
                )

        recipes = iterator

    if not isinstance(
        recipes,
        list,
    ):
        return result

    # ========================================================
    # PROCESAR RECETAS
    # ========================================================

    for recipe in recipes:

        if not isinstance(
            recipe,
            dict,
        ):
            continue

        recipe_type = str(
            recipe.get("type")
            or recipe.get(
                "recipeType"
            )
            or ""
        ).lower()

        # Ignorar hornos, cortapiedras,
        # mesas de cartografía, etc.
        #
        # Aquí solamente queremos crafteo.
        if recipe_type:

            if (
                "crafting" not in
                recipe_type
                and recipe_type
                not in (
                    "crafting_table",
                    "crafting_table_shapeless",
                )
            ):
                continue

        # ====================================================
        # RESULTADO
        # ====================================================

        output = (
            recipe.get("result")
            or recipe.get("output")
        )

        result_items = []

        if isinstance(
            output,
            list,
        ):

            result_items = (
                extract_ingredients(
                    output
                )
            )

        elif output is not None:

            item = ingredient(
                output
            )

            if item:
                result_items = [
                    item
                ]

        # Algunos datos usan:
        # resultItem
        if not result_items:

            fallback = (
                recipe.get(
                    "resultItem"
                )
            )

            item = ingredient(
                fallback
            )

            if item:
                result_items = [
                    item
                ]

        if not result_items:
            continue

        output_item = (
            result_items[0]
        )

        ident = output_item["id"]

        amount = output_item[
            "cantidad"
        ]

        # ====================================================
        # PATRÓN
        # ====================================================

        pattern = recipe_pattern(
            recipe
        )

        if not pattern:
            continue

        # ====================================================
        # CONTAR INGREDIENTES
        # ====================================================

        counts = {}

        for row in pattern:

            for item_id in row:

                if item_id:

                    counts[item_id] = (
                        counts.get(
                            item_id,
                            0,
                        )
                        + 1
                    )

        ingredients = []

        for item_id, count in (
            counts.items()
        ):

            ingredients.append(
                {
                    "id": item_id,
                    "nombre": (
                        item_id
                        .replace(
                            "_",
                            " ",
                        )
                        .title()
                    ),
                    "cantidad": count,
                }
            )

        # ====================================================
        # GUARDAR
        # ====================================================

        if ident not in result:

            result[ident] = {
                "mesa": (
                    "Mesa de crafteo"
                ),
                "patron": pattern,
                "ingredientes": (
                    ingredients
                ),
                "resultado_cantidad": (
                    amount
                ),
            }

    return result


# ============================================================
# CONSTRUIR BASE DE ITEMS
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

    # ========================================================
    # ITEMS
    # ========================================================

    if isinstance(
        raw_items,
        dict,
    ):

        items = (
            raw_items.get(
                "items"
            )
            or raw_items.get(
                "data"
            )
            or []
        )

    else:
        items = raw_items

    recipes = build_recipes(
        raw_recipes
    )

    base = {}

    if not isinstance(
        items,
        list,
    ):
        return base

    # ========================================================
    # ITEMS
    # ========================================================

    for data in items:

        if not isinstance(
            data,
            dict,
        ):
            continue

        ident = (
            data.get("name")
            or data.get("id")
            or data.get(
                "identifier"
            )
        )

        if not ident:
            continue

        ident = str(
            ident
        ).replace(
            "minecraft:",
            "",
        )

        # No mostrar air.
        if ident == "air":
            continue

        display = (
            data.get(
                "displayName"
            )
            or data.get(
                "display_name"
            )
        )

        durability = (
            data.get(
                "maxDurability"
            )
            or data.get(
                "max_durability"
            )
            or data.get(
                "durability"
            )
        )

        damage = (
            data.get("damage")
            or data.get(
                "attackDamage"
            )
            or data.get(
                "attack_damage"
            )
        )

        speed = (
            data.get(
                "miningSpeed"
            )
            or data.get(
                "mining_speed"
            )
        )

        aliases = [
            norm(ident),
        ]

        if display:
            aliases.append(
                norm(display)
            )

        base[ident] = {

            "id": ident,

            "nombre": item_name(
                display,
                ident,
            ),

            "identificador":
                f"minecraft:{ident}",

            "aliases": aliases,

            "categoria":
                "Objeto",

            "descripcion": (
                "Objeto de Minecraft "
                f"identificado como "
                f"{ident}."
            ),

            "danio": damage,

            "velocidad_mineria":
                speed,

            "durabilidad":
                durability,

            "stack_size": (
                data.get(
                    "stackSize"
                )
                or data.get(
                    "stack_size"
                )
                or 64
            ),

            "receta":
                recipes.get(
                    ident
                ),

            "variaciones":
                data.get(
                    "variations"
                )
                or [],
        }

    # ========================================================
    # ALIASES BÁSICOS
    # ========================================================

    for alias, ident in (
        ALIASES.items()
    ):

        if ident in base:

            base[ident][
                "aliases"
            ].append(
                norm(alias)
            )

    # ========================================================
    # ALIASES:
    #
    # pico de diamante
    # espada de hierro
    # etc.
    # ========================================================

    for material_es, material_id in (
        MATERIALS.items()
    ):

        for tool_es, tool_id in (
            TOOLS.items()
        ):

            ident = (
                f"{material_id}_"
                f"{tool_id}"
            )

            if ident not in base:
                continue

            aliases = [
                f"{tool_es} de "
                f"{material_es}",

                f"{tool_es} "
                f"{material_es}",
            ]

            for alias in aliases:

                base[ident][
                    "aliases"
                ].append(
                    norm(alias)
                )

    return base


# ============================================================
# BASE GLOBAL
# ============================================================

ITEMS = None


# ============================================================
# BUSCAR HERRAMIENTA COMPUESTA
# ============================================================

def compound_lookup(query):

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

def buscar_item(consulta):

    global ITEMS

    if ITEMS is None:

        ITEMS = build()

    query = norm(
        consulta
    )

    if not query:
        return None

    # ========================================================
    # 1. ALIAS EXACTO
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
    # 2. ID EXACTO
    # ========================================================

    if query in ITEMS:
        return ITEMS[
            query
        ]

    # ========================================================
    # 3. HERRAMIENTAS COMPUESTAS
    #
    # pico de diamante
    # ========================================================

    item = compound_lookup(
        query
    )

    if item:
        return item

    # ========================================================
    # 4. ALIAS EXACTO
    # ========================================================

    for item in ITEMS.values():

        for alias in item.get(
            "aliases",
            [],
        ):

            if norm(alias) == query:
                return item

    # ========================================================
    # 5. BÚSQUEDA POR PALABRAS
    #
    # MUY IMPORTANTE:
    #
    # No devolvemos cualquier cosa.
    # ========================================================

    stopwords = {
        "de",
        "del",
        "la",
        "el",
        "los",
        "las",
        "un",
        "una",
    }

    words = [
        word
        for word in query.split()
        if word not in stopwords
    ]

    if not words:
        return None

    best = None
    best_score = 0

    for item in ITEMS.values():

        names = [
            norm(
                item.get(
                    "id",
                    "",
                )
            ),

            norm(
                item.get(
                    "nombre",
                    "",
                )
            ),
        ]

        names.extend(
            norm(alias)
            for alias in item.get(
                "aliases",
                [],
            )
            if alias
        )

        tokens = set()

        for name in names:

            tokens.update(
                name
                .replace(
                    "_",
                    " ",
                )
                .split()
            )

        score = 0

        for word in words:

            if word in tokens:
                score += 5

        # Todas las palabras tienen
        # que aparecer.
        if all(
            word in tokens
            for word in words
        ):

            score += 20

        if score > best_score:

            best = item
            best_score = score

    # ========================================================
    # NO INVENTAR RESULTADOS
    # ========================================================

    if best_score <= 0:
        return None

    return best


# ============================================================
# OBTENER TODOS LOS ITEMS
# ============================================================

def obtener_items():

    global ITEMS

    if ITEMS is None:
        ITEMS = build()

    return ITEMS
