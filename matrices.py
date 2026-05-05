# Funcion realizada por Santiago Hernández

# Inicialmente importo la funcion gcd de la libreria math, esta funcion es por sus siglas en ingles
# Greatest Common Divisor, que es el maximo comun divisor, esta funcion es necesaria para simplificar fracciones
# Y se usara mas adelante al racionalizar los coeficientes
from math import gcd

# Adicionalmente importo la funcion conocer_cantidad_moles de traductor para contar con el diccionario de los coeficientes 
from traductor import conocer_cantidad_moles


# Esta funcion como su nombre lo dice toma la ecuacion quimica especialmente los coeficientes 
# Y los convierte en una matriz, es basicamente la base para el resto de operaciones dentro del codigo
def construir_matriz(reactivos, productos):

    # Aqui se obtiene la cantidad de atomos de cada compuesto en reactivos y productos
    # Esto devuelve una lista de diccionarios donde cada diccionario representa un compuesto
    atomos_reactivos = [conocer_cantidad_moles(r) for r in reactivos]
    atomos_productos = [conocer_cantidad_moles(p) for p in productos]
  
    # Se crea un conjunto vacio para almacenar todos los elementos sin repetir
    elementos = set()

    # Se recorren todos los diccionarios para obtener las llaves (elementos quimicos)
    # y agregarlos al conjunto
    for conteo in atomos_reactivos + atomos_productos:
        elementos.update(conteo.keys())

    # Se ordenan los elementos para mantener consistencia en la matriz
    elementos  = sorted(elementos)

    # Se juntan reactivos y productos en una sola lista
    compuestos = reactivos + productos         

    # Aqui se construye la matriz fila por fila
    matriz = []
    for i in elementos:
        fila = []

        # Para reactivos los valores son positivos
        for conteo in atomos_reactivos:
            fila.append(float(conteo.get(i, 0)))

        # Para productos los valores son negativos (pasan al otro lado de la ecuacion)
        for conteo in atomos_productos:
            fila.append(-float(conteo.get(i, 0)))

        matriz.append(fila)

    return matriz, elementos, compuestos




# Funcion que aplica el metodo de Gauss-Jordan para llevar la matriz a su forma reducida
def gauss_jordan(matriz):
    
    # Se crea una copia de la matriz para no modificar la original
    matriz = [fila[:] for fila in matriz]

    # Se obtienen dimensiones
    num_filas = len(matriz)
    num_cols  = len(matriz[0]) if matriz else 0
    
    # Esta variable indica en que fila estamos trabajando el pivote
    fila_pivote = 0 

    # Se recorren las columnas
    for i in range(num_cols):

        # Se busca una fila con un valor distinto de cero para usarla como pivote
        fila_no_cero = None
        for fila in range(fila_pivote, num_filas):
            if abs(matriz[fila][i]) > 1e-9: 
                fila_no_cero = fila
                break
        
        # Si no se encuentra pivote en esta columna, se pasa a la siguiente
        if fila_no_cero is None:
            continue

        # Se intercambian filas para subir el pivote
        matriz[fila_pivote], matriz[fila_no_cero] = (
            matriz[fila_no_cero], matriz[fila_pivote]
        )

        # Se normaliza la fila del pivote dividiendo por su valor
        pivote = matriz[fila_pivote][i]
        matriz[fila_pivote] = [x / pivote for x in matriz[fila_pivote]]

        # Se eliminan los valores de la columna del pivote en las otras filas
        for fila in range(num_filas):
            if fila != fila_pivote and abs(matriz[fila][i]) > 1e-9:
                factor = matriz[fila][i]
                
                matriz[fila] = [
                    matriz[fila][j] - factor * matriz[fila_pivote][j]
                    for j in range(num_cols)
                ]

        # Se pasa a la siguiente fila pivote
        fila_pivote += 1   

    return matriz



# Funcion para extraer los coeficientes desde la matriz en forma reducida
def extraer_coeficientes(matriz_rref, num_compuestos):

    # Se inicializa la lista de coeficientes
    coeficientes = [0.0] * num_compuestos

    # Se fija el ultimo coeficiente como 1 (variable libre)
    coeficientes[num_compuestos - 1] = 1.0

    # Se recorren las filas de abajo hacia arriba
    for fila in reversed(matriz_rref):

        # Se busca la columna pivote
        col_pivote = None
        for j in range(num_compuestos):
            if abs(fila[j]) > 1e-9:
                col_pivote = j
                break

        # Si la fila es nula se ignora
        if col_pivote is None:
            continue  

        # Se calcula el valor del coeficiente usando sustitucion hacia atras
        valor = 0.0
        for j in range(num_compuestos):
            if j != col_pivote:
                valor -= fila[j] * coeficientes[j]
        
        coeficientes[col_pivote] = valor

    return coeficientes




# Funcion para calcular el minimo comun multiplo usando el gcd
def m_c_m(a, b):

    return abs(a * b) // gcd(a, b)




# Funcion que convierte coeficientes decimales en enteros
def racionalizar_coeficientes(coeficientes, tolerancia=1e-6, max_denominador=1000):

    # Lista para guardar los denominadores aproximados
    denominadores = []

    # Se aproxima cada coeficiente a una fraccion
    for c in coeficientes:
        mejor_error      = float('inf')
        mejor_denominador = 1

        # Se prueban denominadores hasta encontrar buena aproximacion
        for q in range(1, max_denominador + 1):
            p     = round(c * q)
            error = abs(c - p / q)

            if error < mejor_error:
                mejor_error       = error
                mejor_denominador = q

            if error < tolerancia:
                break   

        denominadores.append(mejor_denominador)

    # Se calcula el minimo comun multiplo de todos los denominadores
    mcm = denominadores[0]
    for d in denominadores[1:]:
        mcm = m_c_m(mcm, d)

    # Se convierten todos los coeficientes a enteros
    enteros = [abs(round(c * mcm)) for c in coeficientes]

    # Se simplifica dividiendo por el maximo comun divisor
    mcd_total = enteros[0]
    for e in enteros[1:]:
        mcd_total = gcd(mcd_total, e)

    if mcd_total > 1:
        enteros = [e // mcd_total for e in enteros]

    return enteros




# Funcion principal que une todo el proceso
def calcular_coeficientes(reactivos, productos):

    # Se construye la matriz inicial
    matriz_original, elementos, compuestos = construir_matriz(reactivos, productos)

    # Se aplica Gauss-Jordan
    matriz_rref = gauss_jordan(matriz_original)

    # Se extraen los coeficientes
    num_compuestos       = len(compuestos)
    coeficientes_float   = extraer_coeficientes(matriz_rref, num_compuestos)

    # Se convierten a enteros
    coeficientes_enteros = racionalizar_coeficientes(coeficientes_float)

    return coeficientes_enteros, compuestos, matriz_original, matriz_rref, elementos




# Funcion para imprimir la matriz de forma organizada
def imprimir_matriz(matriz, elementos, compuestos, titulo="Matriz"):

    # Ancho de cada columna
    ancho_col = 10   

    print(f"\n{'='*60}")
    print(f"  {titulo}")
    print(f"{'='*60}")

    # Se imprime encabezado con nombres de compuestos
    encabezado = f"{'Elem':>6} |"
    for comp in compuestos:
        encabezado += f"{comp:>{ancho_col}}"
    print(encabezado)

    # Linea separadora
    print(f"{'-'*6}-+{'-'*ancho_col*len(compuestos)}")

    # Se imprime cada fila con su elemento correspondiente
    for i, elemento in enumerate(elementos):
        fila_str = f"{elemento:>6} |"
        for val in matriz[i]:
            fila_str += f"{val:>{ancho_col}.3f}"
        print(fila_str)

    print(f"{'='*60}\n")

    return matriz