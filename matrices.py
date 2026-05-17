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

    # Bueno, inicialmente tenemos que saber cuantos atomos hay en cada uno de los lados de la reaccion sino como operamos xd
    # Entonces tenienendo en cuenta que en traductor se creo una funcion con ese resultado
    # la aplicamos para los reactivos y los productos
    # obteniendo en cada una de las variables una lista de diccionarios 
    atomos_reactivos = [conocer_cantidad_moles(r) for r in reactivos]
    atomos_productos = [conocer_cantidad_moles(p) for p in productos]
  
    # Ahora con esto, lo primero que hago es definir un conjunto sin elementos
    # este almacenara los elementos presentes en la reaccion pero sin repetirlos esto usando la funcion set
    elementos = set()
    # Ahora defino un bucle for donde recorro cada uno de los elementos de ambos diccionarios 
    # ya que estoy sumandolos y definiendolos como el limite del bucle
    for conteo in atomos_reactivos + atomos_productos:
        elementos.update(conteo.keys())

    # Ahora con el conjunto de todos los elementos de la reaccion
    elementos  = sorted(elementos)
    compuestos = reactivos + productos         

    matriz = []
    for i in elementos:
        fila = []

        for conteo in atomos_reactivos:
            fila.append(float(conteo.get(i, 0)))

        for conteo in atomos_productos:
            fila.append(-float(conteo.get(i, 0)))

        matriz.append(fila)

    return matriz, elementos, compuestos




def gauss_jordan(matriz):
    
    matriz = [fila[:] for fila in matriz]
    num_filas = len(matriz)
    num_cols  = len(matriz[0]) if matriz else 0
    
    fila_pivote = 0 

    for i in range(num_cols):

        fila_no_cero = None
        for fila in range(fila_pivote, num_filas):
            if abs(matriz[fila][i]) > 1e-9: 
                fila_no_cero = fila
                break
        
        if fila_no_cero is None:
            continue

        matriz[fila_pivote], matriz[fila_no_cero] = (
            matriz[fila_no_cero], matriz[fila_pivote]
        )

        pivote = matriz[fila_pivote][i]
        matriz[fila_pivote] = [x / pivote for x in matriz[fila_pivote]]

        for fila in range(num_filas):
            if fila != fila_pivote and abs(matriz[fila][i]) > 1e-9:
                factor = matriz[fila][i]
                
                matriz[fila] = [
                    matriz[fila][j] - factor * matriz[fila_pivote][j]
                    for j in range(num_cols)
                ]

        fila_pivote += 1   

    return matriz


def extraer_coeficientes(matriz_rref, num_compuestos):

    coeficientes = [0.0] * num_compuestos

    coeficientes[num_compuestos - 1] = 1.0

    for fila in reversed(matriz_rref):

        col_pivote = None
        for j in range(num_compuestos):
            if abs(fila[j]) > 1e-9:
                col_pivote = j
                break

        if col_pivote is None:
            continue  

        valor = 0.0
        for j in range(num_compuestos):
            if j != col_pivote:
                valor -= fila[j] * coeficientes[j]
        
        coeficientes[col_pivote] = valor

    return coeficientes




def m_c_m(a, b):

    return abs(a * b) // gcd(a, b)




def racionalizar_coeficientes(coeficientes, tolerancia=1e-6, max_denominador=1000):

    denominadores = []

    for c in coeficientes:
        mejor_error      = float('inf')
        mejor_denominador = 1

        for q in range(1, max_denominador + 1):
            p     = round(c * q)
            error = abs(c - p / q)

            if error < mejor_error:
                mejor_error       = error
                mejor_denominador = q

            if error < tolerancia:
                break   

        denominadores.append(mejor_denominador)

    mcm = denominadores[0]
    for d in denominadores[1:]:
        mcm = m_c_m(mcm, d)

    enteros = [abs(round(c * mcm)) for c in coeficientes]

    mcd_total = enteros[0]
    for e in enteros[1:]:
        mcd_total = gcd(mcd_total, e)

    if mcd_total > 1:
        enteros = [e // mcd_total for e in enteros]

    return enteros




def calcular_coeficientes(reactivos, productos):

    matriz_original, elementos, compuestos = construir_matriz(reactivos, productos)

    matriz_rref = gauss_jordan(matriz_original)

    num_compuestos       = len(compuestos)
    coeficientes_float   = extraer_coeficientes(matriz_rref, num_compuestos)

    coeficientes_enteros = racionalizar_coeficientes(coeficientes_float)

    return coeficientes_enteros, compuestos, matriz_original, matriz_rref, elementos




def imprimir_matriz(matriz, elementos, compuestos, titulo="Matriz"):

    ancho_col = 10   

    print(f"\n{'='*60}")
    print(f"  {titulo}")
    print(f"{'='*60}")

    encabezado = f"{'Elem':>6} |"
    for comp in compuestos:
        encabezado += f"{comp:>{ancho_col}}"
    print(encabezado)

    print(f"{'-'*6}-+{'-'*ancho_col*len(compuestos)}")

    for i, elemento in enumerate(elementos):
        fila_str = f"{elemento:>6} |"
        for val in matriz[i]:
            fila_str += f"{val:>{ancho_col}.3f}"
        print(fila_str)

    print(f"{'='*60}\n")

    return matriz