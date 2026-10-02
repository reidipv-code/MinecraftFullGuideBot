from __future__ import annotations

import json
import re
import time
import unicodedata
from pathlib import Path
from urllib.request import Request, urlopen

ITEMS_URL = "https://raw.githubusercontent.com/PrismarineJS/minecraft-data/master/data/bedrock/1.26.30/items.json"
RECIPES_URL = "https://raw.githubusercontent.com/PrismarineJS/minecraft-data/master/data/bedrock/1.19.10/recipes.json"
CACHE = Path("/tmp/minecraft_fullguide_data")
ITEMS_CACHE = CACHE / "items.json"
RECIPES_CACHE = CACHE / "recipes.json"
CACHE_AGE = 7 * 24 * 60 * 60

ALIASES = {
    "mesa de crafteo": "crafting_table", "mesa de trabajo": "crafting_table",
    "mesa de fabricacion": "crafting_table", "mesa de fabricación": "crafting_table",
    "piedra base": "bedrock", "adoquin": "cobblestone", "adoquín": "cobblestone",
    "carbon": "coal", "carbón": "coal", "diamante": "diamond", "diamantes": "diamond",
    "hierro": "iron", "oro": "gold", "esmeralda": "emerald", "redstone": "redstone",
    "lapislazuli": "lapis_lazuli", "lapislázuli": "lapis_lazuli", "palo": "stick", "palos": "stick",
    "pico": "pickaxe", "espada": "sword", "hacha": "axe", "pala": "shovel", "azada": "hoe",
    "arco": "bow", "flecha": "arrow", "cubeta": "bucket", "cubo": "bucket", "horno": "furnace",
    "cofre": "chest", "vidrio": "glass", "arena": "sand", "grava": "gravel", "tierra": "dirt",
    "madera": "planks", "tablones": "planks",
}


def norm(s: str) -> str:
    s = unicodedata.normalize("NFD", str(s).lower().strip())
    s = "".join(c for c in s if unicodedata.category(c) != "Mn")
    s = s.replace("minecraft:", "")
    return re.sub(r"\s+", " ", re.sub(r"[^a-z0-9_ ]+", " ", s)).strip()


def load_json(url: str, path: Path):
    CACHE.mkdir(parents=True, exist_ok=True)
    if path.exists() and time.time() - path.stat().st_mtime < CACHE_AGE:
        return json.loads(path.read_text(encoding="utf-8"))
    req = Request(url, headers={"User-Agent": "MinecraftFullGuideBot/1.0"})
    with urlopen(req, timeout=40) as r:
        data = r.read()
    path.write_bytes(data)
    return json.loads(data.decode("utf-8"))


def item_name(display, ident):
    return str(display or ident.replace("_", " ").title())


def ingredient(x):
    if not isinstance(x, dict):
        return None
    ident = x.get("name") or x.get("item") or x.get("id")
    if not ident:
        return None
    ident = str(ident).replace("minecraft:", "")
    count = x.get("count") or x.get("quantity") or x.get("amount") or 1
    try: count = int(count)
    except Exception: count = 1
    return {"id": ident, "nombre": ident.replace("_", " ").title(), "cantidad": count}


def recipe_pattern(r):
    ingredients = r.get("ingredients") or []
    indexed = {}
    for i, x in enumerate(ingredients, 1):
        q = ingredient(x)
        if q: indexed[i] = q["id"]
    shape = r.get("inShape") or r.get("input")
    out = [[None] * 3 for _ in range(3)]
    if isinstance(shape, list) and shape:
        if not isinstance(shape[0], list): shape = [shape]
        h = min(3, len(shape)); w = min(3, max((len(x) for x in shape if isinstance(x, list)), default=0))
        oy, ox = (3-h)//2, (3-w)//2
        for y, row in enumerate(shape[:3]):
            if not isinstance(row, list): continue
            for x, v in enumerate(row[:3]):
                if v in (None, 0, "", False): continue
                if isinstance(v, str): ident = v.replace("minecraft:", "")
                else: ident = indexed.get(v)
                if ident: out[y+oy][x+ox] = ident
        return out
    flat = []
    for x in ingredients:
        q = ingredient(x)
        if q: flat.append(q["id"])
    positions = [(1,1),(0,1),(1,0),(1,2),(2,1),(0,0),(0,2),(2,0),(2,2)]
    for pos, ident in zip(positions, flat[:9]): out[pos[0]][pos[1]] = ident
    return out if flat else None


def build_recipes(raw):
    recipes = raw.get("recipes", raw.get("data", raw)) if isinstance(raw, dict) else raw
    result = {}
    if not isinstance(recipes, list): return result
    for r in recipes:
        if not isinstance(r, dict): continue
        typ = str(r.get("type") or r.get("recipeType") or "").lower()
        if "crafting" not in typ: continue
        out = r.get("result")
        if isinstance(out, dict):
            ident = out.get("name") or out.get("item") or out.get("id")
            amount = out.get("count") or out.get("quantity") or out.get("amount") or 1
        else:
            ident, amount = out, 1
        ident = ident or r.get("output") or r.get("resultItem")
        if isinstance(ident, dict): ident = ident.get("name") or ident.get("item") or ident.get("id")
        if not ident: continue
        ident = str(ident).replace("minecraft:", "")
        pattern = recipe_pattern(r)
        if not pattern: continue
        counts = {}
        for row in pattern:
            for x in row:
                if x: counts[x] = counts.get(x, 0) + 1
        ingredients = [{"id": k, "nombre": k.replace("_", " ").title(), "cantidad": v} for k,v in counts.items()]
        try: amount = int(amount)
        except Exception: amount = 1
        result.setdefault(ident, {"mesa": "Mesa de crafteo", "patron": pattern, "ingredientes": ingredients, "resultado_cantidad": amount})
    return result


def build():
    raw_items = load_json(ITEMS_URL, ITEMS_CACHE)
    raw_recipes = load_json(RECIPES_URL, RECIPES_CACHE)
    items = raw_items.get("items", raw_items.get("data", raw_items)) if isinstance(raw_items, dict) else raw_items
    recipes = build_recipes(raw_recipes)
    base = {}
    for d in items if isinstance(items, list) else []:
        if not isinstance(d, dict): continue
        ident = d.get("name") or d.get("id") or d.get("identifier")
        if not ident: continue
        ident = str(ident).replace("minecraft:", "")
        display = d.get("displayName") or d.get("display_name")
        durability = d.get("maxDurability") or d.get("max_durability") or d.get("durability")
        damage = d.get("damage") or d.get("attackDamage") or d.get("attack_damage")
        speed = d.get("miningSpeed") or d.get("mining_speed")
        base[ident] = {
            "id": ident, "nombre": item_name(display, ident), "identificador": f"minecraft:{ident}",
            "aliases": [norm(ident), norm(display or "")], "categoria": "Objeto",
            "descripcion": f"Objeto de Minecraft identificado como {ident}.",
            "danio": damage, "velocidad_mineria": speed, "durabilidad": durability,
            "stack_size": d.get("stackSize") or d.get("stack_size") or 64,
            "receta": recipes.get(ident), "variaciones": d.get("variations") or [],
        }
    for alias, ident in ALIASES.items():
        if ident in base: base[ident]["aliases"].append(norm(alias))
    return base


ITEMS = None


def buscar_item(consulta: str):
    global ITEMS
    if ITEMS is None:
        ITEMS = build()
    q = norm(consulta)
    if not q: return None
    if q in ALIASES and ALIASES[q] in ITEMS: return ITEMS[ALIASES[q]]
    if q in ITEMS: return ITEMS[q]
    for item in ITEMS.values():
        if q in item["aliases"]: return item
    words = q.split()
    best, score = None, 0
    for item in ITEMS.values():
        text = " ".join([norm(item["nombre"]), norm(item["id"])] + item["aliases"])
        n = sum(w in text for w in words)
        if n > score: best, score = item, n
    return best
