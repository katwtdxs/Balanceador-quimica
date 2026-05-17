# Módulo: tabla_periodica.py
#
# ¿Qué hace este archivo?
# Guarda la información de todos los elementos de la tabla periódica
# y permite consultarla fácilmente por símbolo o por nombre.
#
# Cada elemento tiene: número atómico, nombre, masa atómica, grupo,
# período y categoría (metal, no metal, etc.)
#
# La función principal es buscar_elemento(texto) que acepta tanto
# el símbolo ("Fe") como el nombre ("hierro" o "iron").


# Diccionario principal. La clave es el SÍMBOLO del elemento.
# Cada entrada tiene toda la información que queremos mostrar.

TABLA_PERIODICA = {
    "H":  {"numero": 1,   "nombre": "Hidrógeno",     "masa": 1.008,    "grupo": 1,   "periodo": 1, "categoria": "No metal"},
    "He": {"numero": 2,   "nombre": "Helio",          "masa": 4.003,    "grupo": 18,  "periodo": 1, "categoria": "Gas noble"},
    "Li": {"numero": 3,   "nombre": "Litio",          "masa": 6.941,    "grupo": 1,   "periodo": 2, "categoria": "Metal alcalino"},
    "Be": {"numero": 4,   "nombre": "Berilio",        "masa": 9.012,    "grupo": 2,   "periodo": 2, "categoria": "Metal alcalinotérreo"},
    "B":  {"numero": 5,   "nombre": "Boro",           "masa": 10.811,   "grupo": 13,  "periodo": 2, "categoria": "Metaloide"},
    "C":  {"numero": 6,   "nombre": "Carbono",        "masa": 12.011,   "grupo": 14,  "periodo": 2, "categoria": "No metal"},
    "N":  {"numero": 7,   "nombre": "Nitrógeno",      "masa": 14.007,   "grupo": 15,  "periodo": 2, "categoria": "No metal"},
    "O":  {"numero": 8,   "nombre": "Oxígeno",        "masa": 15.999,   "grupo": 16,  "periodo": 2, "categoria": "No metal"},
    "F":  {"numero": 9,   "nombre": "Flúor",          "masa": 18.998,   "grupo": 17,  "periodo": 2, "categoria": "Halógeno"},
    "Ne": {"numero": 10,  "nombre": "Neón",           "masa": 20.180,   "grupo": 18,  "periodo": 2, "categoria": "Gas noble"},
    "Na": {"numero": 11,  "nombre": "Sodio",          "masa": 22.990,   "grupo": 1,   "periodo": 3, "categoria": "Metal alcalino"},
    "Mg": {"numero": 12,  "nombre": "Magnesio",       "masa": 24.305,   "grupo": 2,   "periodo": 3, "categoria": "Metal alcalinotérreo"},
    "Al": {"numero": 13,  "nombre": "Aluminio",       "masa": 26.982,   "grupo": 13,  "periodo": 3, "categoria": "Metal"},
    "Si": {"numero": 14,  "nombre": "Silicio",        "masa": 28.086,   "grupo": 14,  "periodo": 3, "categoria": "Metaloide"},
    "P":  {"numero": 15,  "nombre": "Fósforo",        "masa": 30.974,   "grupo": 15,  "periodo": 3, "categoria": "No metal"},
    "S":  {"numero": 16,  "nombre": "Azufre",         "masa": 32.060,   "grupo": 16,  "periodo": 3, "categoria": "No metal"},
    "Cl": {"numero": 17,  "nombre": "Cloro",          "masa": 35.453,   "grupo": 17,  "periodo": 3, "categoria": "Halógeno"},
    "Ar": {"numero": 18,  "nombre": "Argón",          "masa": 39.948,   "grupo": 18,  "periodo": 3, "categoria": "Gas noble"},
    "K":  {"numero": 19,  "nombre": "Potasio",        "masa": 39.098,   "grupo": 1,   "periodo": 4, "categoria": "Metal alcalino"},
    "Ca": {"numero": 20,  "nombre": "Calcio",         "masa": 40.078,   "grupo": 2,   "periodo": 4, "categoria": "Metal alcalinotérreo"},
    "Sc": {"numero": 21,  "nombre": "Escandio",       "masa": 44.956,   "grupo": 3,   "periodo": 4, "categoria": "Metal de transición"},
    "Ti": {"numero": 22,  "nombre": "Titanio",        "masa": 47.867,   "grupo": 4,   "periodo": 4, "categoria": "Metal de transición"},
    "V":  {"numero": 23,  "nombre": "Vanadio",        "masa": 50.942,   "grupo": 5,   "periodo": 4, "categoria": "Metal de transición"},
    "Cr": {"numero": 24,  "nombre": "Cromo",          "masa": 51.996,   "grupo": 6,   "periodo": 4, "categoria": "Metal de transición"},
    "Mn": {"numero": 25,  "nombre": "Manganeso",      "masa": 54.938,   "grupo": 7,   "periodo": 4, "categoria": "Metal de transición"},
    "Fe": {"numero": 26,  "nombre": "Hierro",         "masa": 55.845,   "grupo": 8,   "periodo": 4, "categoria": "Metal de transición"},
    "Co": {"numero": 27,  "nombre": "Cobalto",        "masa": 58.933,   "grupo": 9,   "periodo": 4, "categoria": "Metal de transición"},
    "Ni": {"numero": 28,  "nombre": "Níquel",         "masa": 58.693,   "grupo": 10,  "periodo": 4, "categoria": "Metal de transición"},
    "Cu": {"numero": 29,  "nombre": "Cobre",          "masa": 63.546,   "grupo": 11,  "periodo": 4, "categoria": "Metal de transición"},
    "Zn": {"numero": 30,  "nombre": "Zinc",           "masa": 65.380,   "grupo": 12,  "periodo": 4, "categoria": "Metal de transición"},
    "Ga": {"numero": 31,  "nombre": "Galio",          "masa": 69.723,   "grupo": 13,  "periodo": 4, "categoria": "Metal"},
    "Ge": {"numero": 32,  "nombre": "Germanio",       "masa": 72.630,   "grupo": 14,  "periodo": 4, "categoria": "Metaloide"},
    "As": {"numero": 33,  "nombre": "Arsénico",       "masa": 74.922,   "grupo": 15,  "periodo": 4, "categoria": "Metaloide"},
    "Se": {"numero": 34,  "nombre": "Selenio",        "masa": 78.971,   "grupo": 16,  "periodo": 4, "categoria": "No metal"},
    "Br": {"numero": 35,  "nombre": "Bromo",          "masa": 79.904,   "grupo": 17,  "periodo": 4, "categoria": "Halógeno"},
    "Kr": {"numero": 36,  "nombre": "Kriptón",        "masa": 83.798,   "grupo": 18,  "periodo": 4, "categoria": "Gas noble"},
    "Rb": {"numero": 37,  "nombre": "Rubidio",        "masa": 85.468,   "grupo": 1,   "periodo": 5, "categoria": "Metal alcalino"},
    "Sr": {"numero": 38,  "nombre": "Estroncio",      "masa": 87.620,   "grupo": 2,   "periodo": 5, "categoria": "Metal alcalinotérreo"},
    "Y":  {"numero": 39,  "nombre": "Itrio",          "masa": 88.906,   "grupo": 3,   "periodo": 5, "categoria": "Metal de transición"},
    "Zr": {"numero": 40,  "nombre": "Circonio",       "masa": 91.224,   "grupo": 4,   "periodo": 5, "categoria": "Metal de transición"},
    "Nb": {"numero": 41,  "nombre": "Niobio",         "masa": 92.906,   "grupo": 5,   "periodo": 5, "categoria": "Metal de transición"},
    "Mo": {"numero": 42,  "nombre": "Molibdeno",      "masa": 95.950,   "grupo": 6,   "periodo": 5, "categoria": "Metal de transición"},
    "Ag": {"numero": 47,  "nombre": "Plata",          "masa": 107.868,  "grupo": 11,  "periodo": 5, "categoria": "Metal de transición"},
    "Cd": {"numero": 48,  "nombre": "Cadmio",         "masa": 112.414,  "grupo": 12,  "periodo": 5, "categoria": "Metal de transición"},
    "Sn": {"numero": 50,  "nombre": "Estaño",         "masa": 118.710,  "grupo": 14,  "periodo": 5, "categoria": "Metal"},
    "I":  {"numero": 53,  "nombre": "Yodo",           "masa": 126.904,  "grupo": 17,  "periodo": 5, "categoria": "Halógeno"},
    "Xe": {"numero": 54,  "nombre": "Xenón",          "masa": 131.293,  "grupo": 18,  "periodo": 5, "categoria": "Gas noble"},
    "Cs": {"numero": 55,  "nombre": "Cesio",          "masa": 132.905,  "grupo": 1,   "periodo": 6, "categoria": "Metal alcalino"},
    "Ba": {"numero": 56,  "nombre": "Bario",          "masa": 137.327,  "grupo": 2,   "periodo": 6, "categoria": "Metal alcalinotérreo"},
    "La": {"numero": 57,  "nombre": "Lantano",        "masa": 138.905,  "grupo": 3,   "periodo": 6, "categoria": "Lantánido"},
    "Ce": {"numero": 58,  "nombre": "Cerio",          "masa": 140.116,  "grupo": 3,   "periodo": 6, "categoria": "Lantánido"},
    "W":  {"numero": 74,  "nombre": "Wolframio",      "masa": 183.840,  "grupo": 6,   "periodo": 6, "categoria": "Metal de transición"},
    "Au": {"numero": 79,  "nombre": "Oro",            "masa": 196.967,  "grupo": 11,  "periodo": 6, "categoria": "Metal de transición"},
    "Hg": {"numero": 80,  "nombre": "Mercurio",       "masa": 200.592,  "grupo": 12,  "periodo": 6, "categoria": "Metal de transición"},
    "Pb": {"numero": 82,  "nombre": "Plomo",          "masa": 207.200,  "grupo": 14,  "periodo": 6, "categoria": "Metal"},
    "U":  {"numero": 92,  "nombre": "Uranio",         "masa": 238.029,  "grupo": 3,   "periodo": 7, "categoria": "Actínido"},
}

# Mapa de nombres en español → símbolo, para poder buscar por nombre
# Incluimos también algunas variantes comunes
NOMBRES_A_SIMBOLO = {
    info["nombre"].lower(): simbolo
    for simbolo, info in TABLA_PERIODICA.items()
}

# Agregamos nombres alternativos en inglés o variantes frecuentes
NOMBRES_ALTERNATIVOS = {
    "hydrogen": "H",  "carbon": "C",   "oxygen": "O",  "nitrogen": "N",
    "iron": "Fe",     "gold": "Au",    "silver": "Ag", "copper": "Cu",
    "lead": "Pb",     "sodium": "Na",  "potassium": "K","calcium": "Ca",
    "chlorine": "Cl", "sulfur": "S",   "phosphorus": "P",
    "zinc": "Zn",     "mercury": "Hg", "tin": "Sn",
    "azufre": "S",    "hierro": "Fe",  "sodio": "Na",
    "potasio": "K",   "calcio": "Ca",  "cloro": "Cl",
    "plomo": "Pb",    "mercurio": "Hg","plata": "Ag",
    "oro": "Au",      "cobre": "Cu",   "zinc": "Zn",
    "estano": "Sn",   "yodo": "I",     "fosforo": "P",
    "wolframio": "W", "uranio": "U",   "hidrogeno": "H",
    "nitrogeno": "N", "oxigeno": "O",  "carbono": "C",
    "fluor": "F",     "bromo": "Br",   "silicio": "Si",
}


def buscar_elemento(texto):
    """
    Recibe un texto que puede ser el símbolo ("Fe"), el nombre en español
    ("Hierro"), el nombre en inglés ("iron") o una variante común ("hierro").

    Devuelve un diccionario con toda la información del elemento,
    o None si no se encontró nada.

    Ejemplos:
        buscar_elemento("Fe")     → info del Hierro
        buscar_elemento("hierro") → info del Hierro
        buscar_elemento("iron")   → info del Hierro
        buscar_elemento("Xyz")    → None
    """
    # Limpiamos el texto: quitamos espacios y lo ponemos con la primera
    # letra mayúscula para ver si coincide con un símbolo directo
    texto_limpio = texto.strip()

    # Intento 1: buscar directamente como símbolo (ej: "Fe", "H", "Cl")
    # Usamos el texto con capitalización original
    if texto_limpio in TABLA_PERIODICA:
        return {"simbolo": texto_limpio, **TABLA_PERIODICA[texto_limpio]}

    # Intento 2: convertir la primera letra a mayúscula (ej: "fe" → "Fe")
    texto_cap = texto_limpio.capitalize()
    if texto_cap in TABLA_PERIODICA:
        return {"simbolo": texto_cap, **TABLA_PERIODICA[texto_cap]}

    # Intento 3: buscar por nombre en el diccionario de nombres
    texto_lower = texto_limpio.lower()
    if texto_lower in NOMBRES_A_SIMBOLO:
        simbolo = NOMBRES_A_SIMBOLO[texto_lower]
        return {"simbolo": simbolo, **TABLA_PERIODICA[simbolo]}

    # Intento 4: buscar en nombres alternativos e inglés
    if texto_lower in NOMBRES_ALTERNATIVOS:
        simbolo = NOMBRES_ALTERNATIVOS[texto_lower]
        return {"simbolo": simbolo, **TABLA_PERIODICA[simbolo]}

    # Si no encontramos nada, devolvemos None
    return None


def obtener_color_categoria(categoria):
    """
    Devuelve un color (en formato hex) para cada categoría de elemento.
    Se usa para darle color a la tarjeta del elemento en Streamlit.
    """
    colores = {
        "No metal":              "#4CAF50",   # verde
        "Metal":                 "#2196F3",   # azul
        "Metal alcalino":        "#FF5722",   # naranja fuerte
        "Metal alcalinotérreo":  "#FF9800",   # naranja
        "Metal de transición":   "#9C27B0",   # morado
        "Metaloide":             "#795548",   # café
        "Halógeno":              "#00BCD4",   # cyan
        "Gas noble":             "#607D8B",   # gris azulado
        "Lantánido":             "#E91E63",   # rosa
        "Actínido":              "#F44336",   # rojo
    }
    # Si la categoría no está en el diccionario, devolvemos gris
    return colores.get(categoria, "#9E9E9E")
