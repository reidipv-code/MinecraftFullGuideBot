from __future__ import annotations

import io
import json
import logging
import zipfile
from pathlib import Path
from urllib.request import Request, urlopen

from PIL import Image, ImageDraw, ImageFont

logger = logging.getLogger(__name__)
VERSION = "1.21.4"
CACHE = Path("/tmp/minecraft_fullguide_assets")
JAR = CACHE / f"client-{VERSION}.jar"
MANIFEST = "https://piston-meta.mojang.com/mc/game/version_manifest_v2.json"
GUI = "assets/minecraft/textures/gui/container/crafting_table.png"


def download(url, path):
    CACHE.mkdir(parents=True, exist_ok=True)
    req = Request(url, headers={"User-Agent": "MinecraftFullGuideBot/1.0"})
    with urlopen(req, timeout=60) as r: data = r.read()
    path.write_bytes(data)


def ensure_client():
    if JAR.exists() and JAR.stat().st_size > 1_000_000: return
    req = Request(MANIFEST, headers={"User-Agent": "MinecraftFullGuideBot/1.0"})
    with urlopen(req, timeout=30) as r: manifest = json.loads(r.read().decode())
    version_url = next(v["url"] for v in manifest["versions"] if v["id"] == VERSION)
    req = Request(version_url, headers={"User-Agent": "MinecraftFullGuideBot/1.0"})
    with urlopen(req, timeout=30) as r: meta = json.loads(r.read().decode())
    download(meta["downloads"]["client"]["url"], JAR)


def resource(path):
    ensure_client()
    try:
        with zipfile.ZipFile(JAR) as z: data = z.read(path)
        return Image.open(io.BytesIO(data)).convert("RGBA")
    except Exception:
        return None


def texture(ident):
    ident = ident.replace("minecraft:", "")
    return resource(f"assets/minecraft/textures/item/{ident}.png") or resource(f"assets/minecraft/textures/block/{ident}.png")


def block_textures(ident):
    ident = ident.replace("minecraft:", "")
    side = resource(f"assets/minecraft/textures/block/{ident}.png")
    top = side
    special = {
        "grass_block": ("grass_block_side.png", "grass_block_top.png"),
        "crafting_table": ("crafting_table_side.png", "crafting_table_top.png"),
        "furnace": ("furnace_side.png", "furnace_top.png"),
        "blast_furnace": ("blast_furnace_side.png", "blast_furnace_top.png"),
        "smoker": ("smoker_side.png", "smoker_top.png"),
    }
    if ident in special:
        s, t = special[ident]
        side = resource(f"assets/minecraft/textures/block/{s}") or side
        top = resource(f"assets/minecraft/textures/block/{t}") or top
    return side, top


def looks_block(ident):
    prefixes = ("stone","deepslate","cobblestone","dirt","grass","sand","gravel","netherrack","end_stone","blackstone","basalt","obsidian","glass","ice","snow","brick","planks","log","wood","leaves","wool","concrete","terracotta","ore","block","crafting_table","furnace","blast_furnace","smoker")
    return ident.replace("minecraft:", "").startswith(prefixes)


def fit(img, size):
    w,h=img.size; scale=min(size/w,size/h)
    return img.resize((max(1,int(w*scale)),max(1,int(h*scale))), Image.Resampling.NEAREST)


def draw_cube(canvas, ident, cx, cy, size):
    side, top = block_textures(ident)
    if side is None:
        img=texture(ident)
        if img: canvas.alpha_composite(fit(img,size),(cx-fit(img,size).width//2,cy-fit(img,size).height//2))
        return
    side=side.resize((size,size),Image.Resampling.NEAREST)
    top=(top or side).resize((size,size//2),Image.Resampling.NEAREST)
    # Cubo simple con volumen, usando las texturas reales.
    left=side.resize((size//2,size),Image.Resampling.NEAREST)
    right=side.resize((size//2,size),Image.Resampling.NEAREST)
    mask=Image.new("L",(size//2,size),0); d=ImageDraw.Draw(mask)
    d.polygon([(size//4,0),(size//2-1,size//8),(size//2-1,size),(size//4,7*size//8),(0,size),(0,size//8)],fill=255)
    x=cx-size//2; y=cy-size//3
    canvas.paste(left,(x,y+size//4),mask)
    canvas.paste(right,(cx,y+size//4),mask)
    tm=Image.new("L",(size,size//2),0); td=ImageDraw.Draw(tm)
    td.polygon([(size//2,0),(size-1,size//4),(size//2,size//2-1),(0,size//4)],fill=255)
    canvas.paste(top,(x,y-size//8),tm)


def draw_count(img,count,x,y):
    if int(count)<=1:return
    try: font=ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf",15)
    except Exception: font=ImageFont.load_default()
    s=str(count); box=ImageDraw.Draw(img).textbbox((0,0),s,font=font); w=box[2]-box[0]; h=box[3]-box[1]
    dr=ImageDraw.Draw(img)
    dr.text((x-w-1,y-h),s,font=font,fill="black")
    dr.text((x-w-2,y-h-1),s,font=font,fill="white")


def draw_item(img,ident,count,x,y,size):
    ident=ident.replace("minecraft:","")
    if looks_block(ident): draw_cube(img,ident,x+size//2,y+size//2,size)
    else:
        tex=texture(ident)
        if tex:
            tex=fit(tex,int(size*.82)); img.alpha_composite(tex,(x+(size-tex.width)//2,y+(size-tex.height)//2))
    draw_count(img,count,x+size-2,y+size-2)


def generar_imagen_crafteo(item):
    receta=item.get("receta")
    if not receta:return None
    try:
        gui=resource(GUI)
        if gui is None:
            logger.error("No se pudo cargar la GUI vanilla.")
            return None
        gui=gui.resize((704,664),Image.Resampling.NEAREST)
        dr=ImageDraw.Draw(gui)
        try: font=ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf",48)
        except Exception: font=ImageFont.load_default()
        dr.text((32,24),"Fabricación",font=font,fill=(64,64,64,255))

        # SIEMPRE 3x3, aunque la receta original use 2x2.
        pattern=receta.get("patron") or [[None]*3 for _ in range(3)]
        grid=[[None]*3 for _ in range(3)]
        for y in range(min(3,len(pattern))):
            if isinstance(pattern[y],list):
                for x in range(min(3,len(pattern[y]))): grid[y][x]=pattern[y][x]
        ox,oy,step,slot=30*4,17*4,18*4,16*4
        for y in range(3):
            for x in range(3):
                if grid[y][x]: draw_item(gui,grid[y][x],1,ox+x*step,oy+y*step,slot)
        rid=str(item.get("id") or item.get("identificador","")).replace("minecraft:","")
        draw_item(gui,rid,int(receta.get("resultado_cantidad") or 1),124*4,35*4,slot)
        out=io.BytesIO(); gui.save(out,"PNG",optimize=True); out.seek(0); out.name="crafteo.png"; return out
    except Exception:
        logger.exception("Error generando imagen de crafteo")
        return None
