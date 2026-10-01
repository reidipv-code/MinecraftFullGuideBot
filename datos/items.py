# ============================================================
# BASE DE DATOS DE ITEMS
# Minecraft Bedrock
# ============================================================


ITEMS = [

    # ========================================================
    # DIAMANTE
    # ========================================================

    {
        "nombre": "Diamante",
        "identificador": "diamond",
        "aliases": [
            "diamante",
        ],
        "categoria": "Materiales",
        "descripcion": (
            "Material precioso utilizado para fabricar "
            "herramientas, armas, armaduras y diversos "
            "objetos avanzados."
        ),
        "danio": None,
        "velocidad_mineria": None,
        "durabilidad": None,
        "receta": None,
    },

    # ========================================================
    # PICO DE DIAMANTE
    # ========================================================

    {
        "nombre": "Pico de diamante",
        "identificador": "diamond_pickaxe",
        "aliases": [
            "pico de diamante",
            "pico diamante",
            "diamond pickaxe",
            "diamond_pickaxe",
        ],
        "categoria": "Herramientas",
        "descripcion": (
            "Herramienta utilizada principalmente para "
            "minar piedra, minerales y otros bloques "
            "que requieren una herramienta de pico."
        ),
        "danio": 5,
        "velocidad_mineria": 8,
        "durabilidad": 1561,
        "receta": {
            "tipo": "shaped",
            "mesa": "Mesa de crafteo",
            "resultado": "diamond_pickaxe",
            "cantidad_resultado": 1,
            "patron": [
                ["diamond", "diamond", "diamond"],
                [None, "stick", None],
                [None, "stick", None],
            ],
            "ingredientes": [
                {
                    "nombre": "Diamante",
                    "identificador": "diamond",
                    "cantidad": 3,
                },
                {
                    "nombre": "Palo",
                    "identificador": "stick",
                    "cantidad": 2,
                },
            ],
        },
    },

    # ========================================================
    # PALO
    # ========================================================

    {
        "nombre": "Palo",
        "identificador": "stick",
        "aliases": [
            "palo",
            "palos",
            "stick",
        ],
        "categoria": "Materiales",
        "descripcion": (
            "Material básico utilizado para fabricar "
            "herramientas, armas y otros objetos."
        ),
        "danio": None,
        "velocidad_mineria": None,
        "durabilidad": None,
        "receta": {
            "tipo": "shaped",
            "mesa": "Mesa de crafteo",
            "resultado": "stick",
            "cantidad_resultado": 4,
            "patron": [
                [None, "planks", None],
                [None, "planks", None],
                [None, None, None],
            ],
            "ingredientes": [
                {
                    "nombre": "Tablones",
                    "identificador": "planks",
                    "cantidad": 2,
                },
            ],
        },
    },

    # ========================================================
    # MESA DE CRAFTEO
    # ========================================================

    {
        "nombre": "Mesa de crafteo",
        "identificador": "crafting_table",
        "aliases": [
            "mesa de crafteo",
            "mesa de trabajo",
            "crafting table",
            "crafting_table",
        ],
        "categoria": "Utilidad",
        "descripcion": (
            "Bloque utilizado para realizar recetas que "
            "requieren una cuadrícula de fabricación de "
            "3×3."
        ),
        "danio": None,
        "velocidad_mineria": None,
        "durabilidad": None,
        "receta": {
            "tipo": "shaped",
            "mesa": "Inventario / Mesa de crafteo",
            "resultado": "crafting_table",
            "cantidad_resultado": 1,
            "patron": [
                ["planks", "planks"],
                ["planks", "planks"],
            ],
            "ingredientes": [
                {
                    "nombre": "Tablones",
                    "identificador": "planks",
                    "cantidad": 4,
                },
            ],
        },
    },

    # ========================================================
    # BEDROCK
    # ========================================================

    {
        "nombre": "Bedrock",
        "identificador": "bedrock",
        "aliases": [
            "bedrock",
            "piedra base",
        ],
        "categoria": "Construcción",
        "descripcion": (
            "Bloque extremadamente resistente que forma "
            "parte de los límites del mundo. No puede "
            "obtenerse normalmente en Supervivencia."
        ),
        "danio": None,
        "velocidad_mineria": None,
        "durabilidad": None,
        "receta": None,
    },

    # ========================================================
    # ESPADA DE DIAMANTE
    # ========================================================

    {
        "nombre": "Espada de diamante",
        "identificador": "diamond_sword",
        "aliases": [
            "espada de diamante",
            "espada diamante",
            "diamond sword",
            "diamond_sword",
        ],
        "categoria": "Armas",
        "descripcion": (
            "Arma fabricada con diamantes utilizada "
            "principalmente para combatir criaturas "
            "y otros enemigos."
        ),
        "danio": 7,
        "velocidad_mineria": None,
        "durabilidad": 1561,
        "receta": {
            "tipo": "shaped",
            "mesa": "Mesa de crafteo",
            "resultado": "diamond_sword",
            "cantidad_resultado": 1,
            "patron": [
                ["diamond"],
                ["diamond"],
                ["stick"],
            ],
            "ingredientes": [
                {
                    "nombre": "Diamante",
                    "identificador": "diamond",
                    "cantidad": 2,
                },
                {
                    "nombre": "Palo",
                    "identificador": "stick",
                    "cantidad": 1,
                },
            ],
        },
    },

    # ========================================================
    # HORNO
    # ========================================================

    {
        "nombre": "Horno",
        "identificador": "furnace",
        "aliases": [
            "horno",
            "furnace",
        ],
        "categoria": "Utilidad",
        "descripcion": (
            "Bloque utilizado para fundir minerales, "
            "cocinar alimentos y procesar diferentes "
            "materiales."
        ),
        "danio": None,
        "velocidad_mineria": None,
        "durabilidad": None,
        "receta": {
            "tipo": "shaped",
            "mesa": "Mesa de crafteo",
            "resultado": "furnace",
            "cantidad_resultado": 1,
            "patron": [
                ["cobblestone", "cobblestone", "cobblestone"],
                ["cobblestone", None, "cobblestone"],
                ["cobblestone", "cobblestone", "cobblestone"],
            ],
            "ingredientes": [
                {
                    "nombre": "Piedra",
                    "identificador": "cobblestone",
                    "cantidad": 8,
                },
            ],
        },
    },
]


# ============================================================
# NORMALIZAR
# ============================================================

def normalizar(texto):

    texto = texto.lower().strip()

    reemplazos = {
        "á": "a",
        "é": "e",
        "í": "i",
        "ó": "o",
        "ú": "u",
        "ü": "u",
    }

    for viejo, nuevo in reemplazos.items():
        texto = texto.replace(viejo, nuevo)

    return texto


# ============================================================
# BUSCAR ITEM
# ============================================================

def buscar_item(consulta):

    consulta_normalizada = normalizar(
        consulta
    )

    # --------------------------------------------------------
    # BUSCAR ALIAS
    # --------------------------------------------------------

    for item in ITEMS:

        for alias in item.get("aliases", []):

            if normalizar(alias) == consulta_normalizada:

                return item

    # --------------------------------------------------------
    # BUSCAR NOMBRE
    # --------------------------------------------------------

    for item in ITEMS:

        if (
            normalizar(item["nombre"])
            == consulta_normalizada
        ):

            return item

    # --------------------------------------------------------
    # BUSCAR IDENTIFICADOR
    # --------------------------------------------------------

    for item in ITEMS:

        if (
            normalizar(item["identificador"])
            == consulta_normalizada
        ):

            return item

    # --------------------------------------------------------
    # BÚSQUEDA PARCIAL
    # --------------------------------------------------------

    for item in ITEMS:

        nombre = normalizar(
            item["nombre"]
        )

        identificador = normalizar(
            item["identificador"]
        )

        if (
            consulta_normalizada in nombre
            or consulta_normalizada in identificador
        ):

            return item

    return None
