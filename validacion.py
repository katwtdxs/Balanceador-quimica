# Módulo: validacion.py
#
# ¿Qué hace este archivo?
# Revisa que la ecuación química escrita por el usuario sea válida
# ANTES de intentar balancearla. Así evitamos errores confusos más adelante.
#
# Valida tres cosas:
#   1. Que los símbolos usados existan (no haya letras inventadas)
#   2. Que los paréntesis estén bien abiertos y cerrados
#   3. Que la ecuación tenga el formato correcto (reactivos = productos)
#
# Si algo está mal, devuelve un mensaje claro explicando el problema.


import re

# Lista de todos los elementos válidos de la tabla periódica.
# Están ordenados de mayor a menor longitud para que el parser
# detecte primero "Cl" antes de detectar "C" sola.
ELEMENTOS_VALIDOS = [
    "He", "Li", "Be", "Ne", "Na", "Mg", "Al", "Si", "Cl", "Ar",
    "Ca", "Sc", "Ti", "Cr", "Mn", "Fe", "Co", "Ni", "Cu", "Zn",
    "Ga", "Ge", "As", "Se", "Br", "Kr", "Rb", "Sr", "Zr", "Nb",
    "Mo", "Tc", "Ru", "Rh", "Pd", "Ag", "Cd", "In", "Sn", "Sb",
    "Te", "Xe", "Cs", "Ba", "La", "Ce", "Pr", "Nd", "Pm", "Sm",
    "Eu", "Gd", "Tb", "Dy", "Ho", "Er", "Tm", "Yb", "Lu", "Hf",
    "Ta", "Re", "Os", "Ir", "Pt", "Au", "Hg", "Tl", "Pb", "Bi",
    "Po", "At", "Rn", "Fr", "Ra", "Ac", "Th", "Pa", "Np", "Pu",
    "Am", "Cm", "Bk", "Cf", "Es", "Fm", "Md", "No", "Lr",
    # Elementos de una sola letra van al final para no bloquear los de dos
    "H", "B", "C", "N", "O", "F", "P", "S", "K", "V", "Y", "I",
    "W", "U",
]

# Convertimos a set para búsquedas rápidas
SET_ELEMENTOS = set(ELEMENTOS_VALIDOS)


def _validar_parentesis(formula):
    """
    Revisa que los paréntesis de una fórmula estén bien balanceados.
    Devuelve (True, "") si todo está bien, o (False, mensaje) si hay error.

    Ejemplos:
        Fe2(SO4)3  →  OK
        Fe2(SO4    →  Error, falta cerrar
        Fe2SO4)3   →  Error, cierra sin abrir
    """
    contador = 0  # Cuenta cuántos paréntesis abiertos hay sin cerrar

    for i, caracter in enumerate(formula):
        if caracter == "(":
            contador += 1
        elif caracter == ")":
            contador -= 1
            # Si el contador baja de 0, se cerró antes de abrir
            if contador < 0:
                return False, f"Paréntesis ')' en posición {i+1} sin un '(' que lo abra."

    # Si al final quedó contador > 0, hay paréntesis sin cerrar
    if contador > 0:
        return False, "Hay un '(' que nunca se cerró con ')'."

    return True, ""


def _extraer_simbolos(formula):
    """
    Recorre la fórmula carácter por carácter y extrae todos los
    símbolos de elementos que encuentra.

    Devuelve una lista con los símbolos encontrados.
    Ejemplo: "Fe2(SO4)3" → ["Fe", "S", "O"]
    """
    simbolos = []
    i = 0

    while i < len(formula):
        letra = formula[i]

        # Los símbolos siempre empiezan con mayúscula
        if letra.isupper():
            simbolo = letra
            i += 1

            # Si la siguiente letra es minúscula, hace parte del símbolo
            while i < len(formula) and formula[i].islower():
                simbolo += formula[i]
                i += 1

            simbolos.append(simbolo)

        else:
            # Saltamos números, paréntesis, etc.
            i += 1

    return simbolos


def _validar_simbolos(formula):
    """
    Extrae los símbolos de la fórmula y verifica que cada uno
    exista en la tabla periódica.

    Devuelve (True, "") si todos son válidos,
    o (False, mensaje) con los símbolos problemáticos.
    """
    simbolos = _extraer_simbolos(formula)
    invalidos = []

    for s in simbolos:
        if s not in SET_ELEMENTOS:
            invalidos.append(s)

    if invalidos:
        # Eliminamos duplicados para no repetir el mismo error
        invalidos_unicos = list(dict.fromkeys(invalidos))
        return False, f"Símbolo(s) no reconocido(s): {', '.join(invalidos_unicos)}. Verifica que estén bien escritos."

    return True, ""


def _validar_estructura_ecuacion(ecuacion):
    """
    Verifica que la ecuación tenga la forma básica:
    algo = algo  (exactamente un signo igual, con cosas a ambos lados)

    Devuelve (True, "") si el formato es correcto, o (False, mensaje).
    """
    # Quitamos espacios para analizar limpio
    ecuacion_limpia = ecuacion.replace(" ", "")

    # Debe haber exactamente un "="
    partes = ecuacion_limpia.split("=")
    if len(partes) != 2:
        return False, "La ecuación debe tener exactamente un signo '=' separando reactivos y productos."

    reactivos_str, productos_str = partes

    # Ambos lados deben tener algo
    if not reactivos_str:
        return False, "No hay reactivos antes del '='."
    if not productos_str:
        return False, "No hay productos después del '='."

    # Cada lado se separa por "+"
    reactivos = reactivos_str.split("+")
    productos  = productos_str.split("+")

    # Ningún compuesto debe quedar vacío (evita "H2++O2" o cosas así)
    for r in reactivos:
        if not r:
            return False, "Hay un '+' extra o mal puesto en los reactivos."
    for p in productos:
        if not p:
            return False, "Hay un '+' extra o mal puesto en los productos."

    return True, ""


def validar_ecuacion(ecuacion):
    """
    Función principal del módulo.
    Recibe la ecuación como string y la revisa completamente.

    Devuelve una tupla:
      - (True,  [])              si la ecuación es válida
      - (False, [lista errores]) si hay problemas

    El orden de validación es:
      1. Estructura general (formato con = y +)
      2. Paréntesis de cada compuesto
      3. Símbolos de elementos existentes
    """
    errores = []

    # ── 1. Revisamos la estructura general ──
    ok, msg = _validar_estructura_ecuacion(ecuacion)
    if not ok:
        # Si la estructura está mal no tiene sentido seguir revisando
        return False, [msg]

    # Separamos la ecuación para revisar compuesto por compuesto
    limpia = ecuacion.replace(" ", "")
    partes = limpia.split("=")
    todos_compuestos = partes[0].split("+") + partes[1].split("+")

    # ── 2. Revisamos paréntesis en cada compuesto ──
    for comp in todos_compuestos:
        ok, msg = _validar_parentesis(comp)
        if not ok:
            errores.append(f"Error en '{comp}': {msg}")

    # ── 3. Revisamos que los símbolos sean elementos reales ──
    for comp in todos_compuestos:
        ok, msg = _validar_simbolos(comp)
        if not ok:
            errores.append(f"Error en '{comp}': {msg}")

    if errores:
        return False, errores

    return True, []
