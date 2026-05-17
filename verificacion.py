# ============================================================
# Módulo: verificacion.py
#
# ¿Qué hace este archivo?
# Verifica si una ecuación química ingresada por el usuario
# ya está balanceada, antes de procesarla.
#
# La lógica es simple: si los átomos de cada elemento son
# iguales a ambos lados de la ecuación tal como fue escrita
# (es decir, con coeficientes = 1), entonces ya está balanceada.
#
# Función principal:
#   - ecuacion_ya_balanceada: recibe la ecuación como string
#     y devuelve True si ya está balanceada, False si no.
# ============================================================

from traductor import Separar_ecuacion, conocer_cantidad_moles


# ────────────────────────────────────────────────────────────
# FUNCIÓN INTERNA: sumar todos los átomos de un lado
# de la ecuación con sus coeficientes dados.
#
# Ejemplo: ["H2", "O2"] con coeficientes [2, 1]
#   → {"H": 4, "O": 2}
# ────────────────────────────────────────────────────────────
def _contar_atomos(compuestos, coeficientes):
    conteo = {}
    for comp, coef in zip(compuestos, coeficientes):
        for elemento, cantidad in conocer_cantidad_moles(comp).items():
            conteo[elemento] = conteo.get(elemento, 0) + cantidad * coef
    return conteo


# ────────────────────────────────────────────────────────────
# FUNCIÓN PÚBLICA: verificar si la ecuación ya está balanceada
#
# Toma la ecuación tal como la escribió el usuario, cuenta los
# átomos de cada lado asumiendo que todos los coeficientes son 1,
# y compara. Si todos los elementos coinciden → ya está balanceada.
#
# Devuelve una tupla (bool, dict) donde:
#   - bool: True si ya está balanceada, False si no
#   - dict: detalle del conteo por elemento para mostrar al usuario
# ────────────────────────────────────────────────────────────
def ecuacion_ya_balanceada(ecuacion: str) -> tuple:

    reactivos, productos = Separar_ecuacion(ecuacion)

    # Contar átomos con coeficiente 1 en ambos lados
    atomos_r = _contar_atomos(reactivos, [1] * len(reactivos))
    atomos_p = _contar_atomos(productos, [1] * len(productos))

    # Reunir todos los elementos presentes en la reacción
    elementos = set(atomos_r.keys()) | set(atomos_p.keys())

    # Construir el detalle para mostrarlo en pantalla
    detalle = {}
    balanceada = True

    for elem in sorted(elementos):
        cant_r = atomos_r.get(elem, 0)
        cant_p = atomos_p.get(elem, 0)
        coincide = cant_r == cant_p
        if not coincide:
            balanceada = False
        detalle[elem] = {
            "reactivos": cant_r,
            "productos": cant_p,
            "ok": coincide
        }

    return balanceada, detalle
