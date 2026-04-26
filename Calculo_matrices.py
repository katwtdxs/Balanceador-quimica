def construir_matriz(reactivos, productos):


    """
    Construye la matriz de reacción a partir de las listas de reactivos y productos.

    Utiliza la función conocer_cantidad_moles() de Traductor.py para obtener
    el conteo de átomos de cada compuesto.

    Parámetros:
        reactivos (list): Lista de strings con los compuestos reactivos.
        productos (list): Lista de strings con los compuestos productos.

    Retorna:
        matriz (list of list): Matriz de reacción como lista de listas de floats.
        elementos (list): Lista ordenada de los elementos químicos presentes.
        compuestos (list): Lista ordenada de todos los compuestos (reactivos + productos).
    """
    # Obtenemos el conteo de átomos para cada compuesto usando Traductor.py
    conteos_reactivos = [conocer_cantidad_moles(r) for r in reactivos]
    conteos_productos = [conocer_cantidad_moles(p) for p in productos]

    # Recopilamos todos los elementos presentes en la reacción (sin duplicados)
    conjunto_elementos = set()
    for conteo in conteos_reactivos + conteos_productos:
        conjunto_elementos.update(conteo.keys())

    elementos = sorted(conjunto_elementos)  # Orden consistente
    compuestos = reactivos + productos      # Reactivos primero, luego productos

    # Construimos la matriz fila por fila (un elemento = una fila)
    matriz = []
    for elemento in elementos:
        fila = []
        # Columnas de reactivos: coeficiente POSITIVO
        for conteo in conteos_reactivos:
            fila.append(float(conteo.get(elemento, 0)))
        # Columnas de productos: coeficiente NEGATIVO (pasan al otro lado de la igualdad)
        for conteo in conteos_productos:
            fila.append(-float(conteo.get(elemento, 0)))
        matriz.append(fila)

    return matriz, elementos, compuestos


def gauss_jordan(matriz):
    """
    Aplica el método de eliminación de Gauss-Jordán a la matriz dada.

    El objetivo es reducir la matriz a su forma escalonada reducida por filas (RREF),
    que permite leer directamente las relaciones entre los coeficientes
    estequiométricos (sistema homogéneo Ax = 0).

    Operaciones de fila permitidas:
        1. Intercambiar dos filas.
        2. Multiplicar una fila por un escalar no nulo.
        3. Sumar a una fila un múltiplo de otra fila.

    Parámetros:
        matriz (list of list): Matriz de reacción a reducir.

    Retorna:
        matriz (list of list): Matriz en forma escalonada reducida (RREF).
    """
    # Trabajamos con una copia para no modificar la original
    matriz = [fila[:] for fila in matriz]
    num_filas = len(matriz)
    num_cols = len(matriz[0])

    fila_pivote = 0  # Índice de la fila donde colocaremos el siguiente pivote

    for col in range(num_cols):
        # Buscamos una fila con un elemento no nulo en la columna actual
        fila_no_cero = None
        for fila in range(fila_pivote, num_filas):
            if abs(matriz[fila][col]) > 1e-9:  # Tolerancia numérica
                fila_no_cero = fila
                break

        if fila_no_cero is None:
            continue  # Columna con todos ceros, pasamos a la siguiente

        # Operación 1: Intercambiamos la fila encontrada con la fila pivote actual
        matriz[fila_pivote], matriz[fila_no_cero] = matriz[fila_no_cero], matriz[fila_pivote]

        # Operación 2: Normalizamos la fila pivote dividiendo por el valor del pivote
        pivote = matriz[fila_pivote][col]
        matriz[fila_pivote] = [x / pivote for x in matriz[fila_pivote]]

        # Operación 3: Eliminamos el elemento de esta columna en TODAS las demás filas
        for fila in range(num_filas):
            if fila != fila_pivote and abs(matriz[fila][col]) > 1e-9:
                factor = matriz[fila][col]
                matriz[fila] = [
                    matriz[fila][j] - factor * matriz[fila_pivote][j]
                    for j in range(num_cols)
                ]

        fila_pivote += 1  # Avanzamos al siguiente pivote

    return matriz


def extraer_coeficientes(matriz_rref, num_compuestos):
    """
    Extrae los coeficientes estequiométricos a partir de la matriz RREF.

    En el sistema homogéneo Ax = 0 con una variable libre (la última columna,
    correspondiente al último compuesto), se asigna x_n = 1 y se despeja
    el resto de coeficientes desde las ecuaciones reducidas.

    Parámetros:
        matriz_rref (list of list): Matriz en forma RREF.
        num_compuestos (int): Número total de compuestos en la reacción.

    Retorna:
        coeficientes (list of float): Lista de coeficientes estequiométricos
                                      en el mismo orden que los compuestos.
    """
    coeficientes = [0.0] * num_compuestos

    # La última variable es la libre: se le asigna el valor 1
    coeficientes[num_compuestos - 1] = 1.0

    # Recorremos las filas de la RREF de abajo hacia arriba para hacer back-substitution
    for fila in reversed(matriz_rref):
        # Identificamos la columna pivote de esta fila (primer elemento no nulo)
        col_pivote = None
        for j in range(num_compuestos):
            if abs(fila[j]) > 1e-9:
                col_pivote = j
                break

        if col_pivote is None:
            continue  # Fila de ceros, la ignoramos

        # Despejamos el coeficiente de la columna pivote usando los ya conocidos
        # Ecuación: fila[col_pivote]*x_pivote + Σ(fila[j]*x_j) = 0
        # => x_pivote = -Σ(fila[j]*x_j) para j != col_pivote
        valor = 0.0
        for j in range(num_compuestos):
            if j != col_pivote:
                valor -= fila[j] * coeficientes[j]
        coeficientes[col_pivote] = valor

    return coeficientes


def minimo_comun_multiplo(a, b):
    """
    Calcula el mínimo común múltiplo (MCM) de dos enteros usando el algoritmo de Euclides.
    Se usa para convertir coeficientes fraccionarios en enteros.
    """
    from math import gcd
    return abs(a * b) // gcd(a, b)


def racionalizar_coeficientes(coeficientes, tolerancia=1e-6, max_denominador=1000):
    """
    Convierte los coeficientes de punto flotante en números enteros positivos.

    El proceso es:
        1. Aproximar cada coeficiente como una fracción p/q.
        2. Calcular el MCM de todos los denominadores.
        3. Multiplicar todos los coeficientes por ese MCM para eliminar fracciones.
        4. Asegurarse de que todos los valores sean positivos (tomar valor absoluto).

    Parámetros:
        coeficientes (list of float): Coeficientes en punto flotante.
        tolerancia (float): Margen de error para la aproximación racional.
        max_denominador (int): Denominador máximo para la búsqueda de fracciones.

    Retorna:
        enteros (list of int): Coeficientes estequiométricos enteros y positivos.
    """
    from math import gcd

    denominadores = []

    for c in coeficientes:
        # Buscamos la mejor fracción p/q que aproxime el valor c
        mejor_error = float('inf')
        mejor_denominador = 1

        for q in range(1, max_denominador + 1):
            p = round(c * q)
            error = abs(c - p / q)
            if error < mejor_error:
                mejor_error = error
                mejor_denominador = q
            if error < tolerancia:
                break  # Aproximación suficientemente buena

        denominadores.append(mejor_denominador)

    # Calculamos el MCM de todos los denominadores encontrados
    mcm = denominadores[0]
    for d in denominadores[1:]:
        mcm = minimo_comun_multiplo(mcm, d)

    # Multiplicamos todos los coeficientes por el MCM y redondeamos a entero
    enteros = [abs(round(c * mcm)) for c in coeficientes]

    # Reducimos por el MCD para obtener los mínimos coeficientes enteros posibles
    mcd_total = enteros[0]
    for e in enteros[1:]:
        mcd_total = gcd(mcd_total, e)

    if mcd_total > 1:
        enteros = [e // mcd_total for e in enteros]

    return enteros


def calcular_coeficientes(reactivos, productos):

    # Paso 1: Construir la matriz de reacción
    matriz_original, elementos, compuestos = construir_matriz(reactivos, productos)

    # Paso 2: Reducir por Gauss-Jordán
    matriz_rref = gauss_jordan(matriz_original)

    # Paso 3: Extraer coeficientes flotantes
    num_compuestos = len(compuestos)
    coeficientes_float = extraer_coeficientes(matriz_rref, num_compuestos)

    # Paso 4: Convertir a enteros positivos mínimos
    coeficientes_enteros = racionalizar_coeficientes(coeficientes_float)

    return coeficientes_enteros, compuestos, matriz_original, matriz_rref, elementos


def imprimir_matriz(matriz, elementos, compuestos, titulo="Matriz"):
    """
    Imprime la matriz de forma legible en consola, con encabezados de
    elementos (filas) y compuestos (columnas).

    Parámetros:
        matriz (list of list): Matriz a imprimir.
        elementos (list): Etiquetas de las filas.
        compuestos (list): Etiquetas de las columnas.
        titulo (str): Título descriptivo para identificar la matriz.
    """
    ancho_col = 10  # Ancho fijo de cada columna para alineación

    print(f"\n{'='*60}")
    print(f"  {titulo}")
    print(f"{'='*60}")

    # Encabezado con los nombres de los compuestos
    encabezado = f"{'Elem':>6} |"
    for comp in compuestos:
        encabezado += f"{comp:>{ancho_col}}"
    print(encabezado)
    print(f"{'-'*6}-+{'-'*ancho_col*len(compuestos)}")

    # Filas de la matriz (una por elemento)
    for i, elemento in enumerate(elementos):
        fila_str = f"{elemento:>6} |"
        for val in matriz[i]:
            fila_str += f"{val:>{ancho_col}.3f}"
        print(fila_str)

    print(f"{'='*60}\n")