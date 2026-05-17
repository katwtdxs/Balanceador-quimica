# ============================================================
# Módulo: explicacion_balanceo.py
#
# ¿Qué hace este archivo?
# Explica paso a paso CÓMO se balancea una ecuación química
# usando el método algebraico con Gauss-Jordan, de forma que
# cualquier estudiante entienda el proceso, no solo el resultado.
#
# Pasos que se explican:
#   1. Identificar reactivos, productos y asignar incógnitas
#   2. Plantear el sistema de ecuaciones (la matriz)
#   3. Aplicar Gauss-Jordan operación por operación
#   4. Leer la solución del sistema reducido
#   5. Convertir a coeficientes enteros (MCM / MCD)
# ============================================================

from traductor import Separar_ecuacion, conocer_cantidad_moles
from matrices  import construir_matriz, gauss_jordan, extraer_coeficientes, racionalizar_coeficientes


# ────────────────────────────────────────────────────────────
# AUXILIAR: mostrar un número sin ceros decimales inútiles
#   2.0  →  "2"     |     1.5  →  "1.5"
# ────────────────────────────────────────────────────────────
def _fmt(n):
    if abs(n - round(n)) < 1e-9:
        return str(int(round(n)))
    return f"{n:.4f}"


# ────────────────────────────────────────────────────────────
# AUXILIAR: escribir la ecuación con coeficientes dados
#   Ejemplo de salida: "2H2 + O2 = 2H2O"
#   Si el coeficiente es 1 no se imprime (convención química)
# ────────────────────────────────────────────────────────────
def _escribir_ecuacion(compuestos, coeficientes, num_reactivos):
    lado_r, lado_p = [], []
    for i, comp in enumerate(compuestos):
        coef    = coeficientes[i]
        prefijo = "" if coef == 1 else str(coef)
        termino = f"{prefijo}{comp}"
        if i < num_reactivos:
            lado_r.append(termino)
        else:
            lado_p.append(termino)
    return " + ".join(lado_r) + " = " + " + ".join(lado_p)


# ────────────────────────────────────────────────────────────
# AUXILIAR: imprimir la matriz como tabla de texto
#   Filas = elementos químicos  |  Columnas = compuestos
# ────────────────────────────────────────────────────────────
def _tabla_matriz(mat, elementos, compuestos):
    ancho  = 10
    lineas = []

    # Cabecera con los nombres de los compuestos
    cab = f"{'':8s}|"
    for comp in compuestos:
        cab += f"{comp:>{ancho}}"
    lineas.append(cab)
    lineas.append("-" * (9 + ancho * len(compuestos)))

    # Una fila por cada elemento
    for i, elem in enumerate(elementos):
        fila = f"{elem:>7s} |"
        for val in mat[i]:
            fila += f"{_fmt(val):>{ancho}}"
        lineas.append(fila)

    return "\n".join(lineas)


# ────────────────────────────────────────────────────────────
# INTERNO: Gauss-Jordan registrando cada operación
#
# Devuelve una lista de tuplas (descripción, tabla_resultado)
# para que el usuario vea qué se hizo y cómo quedó la matriz.
# ────────────────────────────────────────────────────────────
def _gauss_jordan_con_pasos(matriz_in, elementos, compuestos):

    mat = [fila[:] for fila in matriz_in]   # copia para no modificar el original
    n_f = len(mat)
    n_c = len(mat[0]) if mat else 0
    ops = []

    def snap():
        return _tabla_matriz(mat, elementos, compuestos)

    fila_pivote = 0

    for col in range(n_c):

        # Buscar fila con valor distinto de cero en esta columna
        fila_nz = None
        for f in range(fila_pivote, n_f):
            if abs(mat[f][col]) > 1e-9:
                fila_nz = f
                break

        if fila_nz is None:
            continue   # columna libre, no hay pivote aquí

        # ── Operación 1: intercambio de filas (si hace falta) ──
        if fila_nz != fila_pivote:
            mat[fila_pivote], mat[fila_nz] = mat[fila_nz], mat[fila_pivote]
            ops.append((
                f"F{fila_pivote+1} ↔ F{fila_nz+1} "
                f"(subir la fila con valor no nulo en la columna {col+1})",
                snap()
            ))

        # ── Operación 2: normalizar para que el pivote sea 1 ──
        pivote = mat[fila_pivote][col]
        if abs(pivote - 1.0) > 1e-9:
            mat[fila_pivote] = [x / pivote for x in mat[fila_pivote]]
            ops.append((
                f"F{fila_pivote+1} ÷ {_fmt(pivote)} "
                f"(convertir el pivote de la columna {col+1} en 1)",
                snap()
            ))

        # ── Operación 3: eliminar el valor de esa columna en las demás filas ──
        for f in range(n_f):
            if f == fila_pivote:
                continue
            factor = mat[f][col]
            if abs(factor) < 1e-9:
                continue
            mat[f] = [mat[f][j] - factor * mat[fila_pivote][j] for j in range(n_c)]
            signo  = f"- {_fmt(abs(factor))}" if factor > 0 else f"+ {_fmt(abs(factor))}"
            ops.append((
                f"F{f+1} = F{f+1} {signo}·F{fila_pivote+1} "
                f"(poner 0 en la columna {col+1}, fila {f+1})",
                snap()
            ))

        fila_pivote += 1

    return ops


# ============================================================
# FUNCIÓN PÚBLICA — única función que Main.py necesita
# ============================================================
def explicar_balanceo(ecuacion: str) -> list:
    """
    Recibe una ecuación química ("H2+O2=H2O") y devuelve una
    lista de strings Markdown con la explicación pedagógica del
    proceso de balanceo, paso a paso.

    Cada elemento de la lista es un bloque para st.markdown().
    """

    pasos  = []
    SEP    = "---"
    letras = list("abcdefghijklmnopqrstuvwxyz")


    # ══════════════════════════════════════════════════════
    # PASO 1 — Reactivos, productos e incógnitas
    # ══════════════════════════════════════════════════════
    reactivos, productos = Separar_ecuacion(ecuacion)
    num_reactivos        = len(reactivos)
    compuestos_todos     = reactivos + productos

    pasos.append(
        "### Paso 1 — Reactivos, productos e incógnitas\n\n"
        "Separamos la ecuación y le asignamos una **letra (incógnita)** "
        "a cada compuesto. Esas letras serán los coeficientes que "
        "queremos encontrar.\n\n"
        f"**Ecuación ingresada:** `{ecuacion}`\n\n"
        f"| Compuesto | Rol | Incógnita |\n"
        f"|-----------|-----|-----------|\n"
        + "\n".join(
            f"| {comp} | {'Reactivo' if i < num_reactivos else 'Producto'} "
            f"| **{letras[i] if i < len(letras) else 'x'+str(i)}** |"
            for i, comp in enumerate(compuestos_todos)
        )
    )
    pasos.append(SEP)


    # ══════════════════════════════════════════════════════
    # PASO 2 — Plantear el sistema de ecuaciones
    # ══════════════════════════════════════════════════════
    matriz_orig, elementos, compuestos = construir_matriz(reactivos, productos)
    num_compuestos = len(compuestos)

    # Construir las ecuaciones en forma simbólica para mostrarlas
    ecuaciones_escritas = []
    for i, elem in enumerate(elementos):
        terminos = []
        for j in range(num_compuestos):
            val = matriz_orig[i][j]
            if abs(val) < 1e-9:
                continue
            var   = letras[j] if j < len(letras) else f"x{j}"
            coef  = _fmt(abs(val))
            signo = "+" if val > 0 else "−"
            parte = var if coef == "1" else f"{coef}{var}"
            terminos.append(f"{signo} {parte}")
        expr = " ".join(terminos).lstrip("+ ").strip()
        ecuaciones_escritas.append(f"- **{elem}:** &nbsp; {expr} = 0")

    pasos.append(
        "### Paso 2 — Plantear el sistema de ecuaciones\n\n"
        "Por la **ley de conservación de la masa**, los átomos de cada "
        "elemento deben ser iguales a ambos lados. Eso nos da una "
        "ecuación por elemento.\n\n"
        "Pasamos todo al mismo lado (productos con signo negativo) "
        "para obtener ecuaciones **= 0**:\n\n"
        + "\n".join(ecuaciones_escritas)
        + "\n\n"
        "Todas estas ecuaciones juntas forman la siguiente **matriz**:\n\n"
        "```\n" + _tabla_matriz(matriz_orig, elementos, compuestos) + "\n```\n\n"
        "> Cada **fila** es un elemento. Cada **columna** es un compuesto. "
        "El valor indica cuántos átomos de ese elemento hay en ese compuesto "
        "(negativo si es producto)."
    )
    pasos.append(SEP)


    # ══════════════════════════════════════════════════════
    # PASO 3 — Reducción por Gauss-Jordan
    # ══════════════════════════════════════════════════════
    pasos.append(
        "### Paso 3 — Reducción por Gauss-Jordan\n\n"
        "Ahora resolvemos la matriz con el **método de Gauss-Jordan**. "
        "El objetivo es transformarla en su forma escalonada reducida "
        "**(RREF)**, donde cada columna pivote tiene un **1** y el "
        "resto de esa columna son **0s**.\n\n"
        "Solo se permiten tres tipos de operaciones sobre las filas:\n\n"
        "| Operación | ¿Qué hace? |\n"
        "|-----------|------------|\n"
        "| **Intercambio** | Cambia el orden de dos filas |\n"
        "| **Escalado** | Divide una fila por un número para obtener pivote = 1 |\n"
        "| **Eliminación** | Resta un múltiplo de una fila a otra para poner un 0 |\n\n"
        "A continuación se muestra **cada operación** y cómo queda "
        "la matriz después de aplicarla:"
    )

    operaciones = _gauss_jordan_con_pasos(matriz_orig, elementos, compuestos)

    if not operaciones:
        pasos.append("_La matriz ya estaba reducida; no se necesitaron operaciones._")
    else:
        for i, (desc, tabla) in enumerate(operaciones, 1):
            pasos.append(
                f"**Operación {i}:** {desc}\n\n"
                f"```\n{tabla}\n```"
            )
    pasos.append(SEP)


    # ══════════════════════════════════════════════════════
    # PASO 4 — Leer la solución
    # ══════════════════════════════════════════════════════
    matriz_rref = gauss_jordan(matriz_orig)
    coef_float  = extraer_coeficientes(matriz_rref, num_compuestos)

    sol_texto = "\n".join(
        f"- **{letras[j] if j < len(letras) else 'x'+str(j)}** ({comp}) = {_fmt(coef_float[j])}"
        for j, comp in enumerate(compuestos)
    )

    pasos.append(
        "### Paso 4 — Leer la solución\n\n"
        "Con la matriz en RREF el sistema queda resuelto, pero tiene "
        "**infinitas soluciones** porque hay una variable libre "
        "(los coeficientes se pueden escalar todos por el mismo número "
        "y la ecuación sigue balanceada).\n\n"
        "Para fijar una solución concreta tomamos la convención de "
        "asignarle **1** al último coeficiente y despejamos los demás.\n\n"
        "**Valores obtenidos:**\n\n"
        + sol_texto
    )
    pasos.append(SEP)


    # ══════════════════════════════════════════════════════
    # PASO 5 — Convertir a enteros
    # ══════════════════════════════════════════════════════
    coef_enteros        = racionalizar_coeficientes(coef_float)
    ecuacion_balanceada = _escribir_ecuacion(compuestos, coef_enteros, num_reactivos)

    coef_fin_texto = "\n".join(
        f"- **{letras[j] if j < len(letras) else 'x'+str(j)}** ({comp}) = **{coef_enteros[j]}**"
        for j, comp in enumerate(compuestos)
    )

    pasos.append(
        "### Paso 5 — Convertir a coeficientes enteros\n\n"
        "Los coeficientes estequiométricos deben ser **enteros positivos**. "
        "Para convertir los decimales o fracciones obtenidos:\n\n"
        "1. Se aproxima cada decimal a una fracción **p/q**.\n"
        "2. Se multiplica todo por el **MCM** de los denominadores "
        "→ todos pasan a ser enteros.\n"
        "3. Se divide todo entre el **MCD** del conjunto "
        "→ se obtienen los valores mínimos posibles.\n\n"
        "**Coeficientes finales:**\n\n"
        + coef_fin_texto
        + f"\n\n**Ecuación balanceada:**\n\n`{ecuacion_balanceada}`"
    )

    return pasos
