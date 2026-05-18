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

    # Construyo la matriz fila por fila, una fila por cada elemento
    # Los reactivos son positivos mientras que los productos son negativos
    # para que al ser totalmente iguales den como resultado total 0
    matriz = []
    for i in elementos:  
        fila = []

        # Recorro los reactivos y agrego su conteo de atomos del elemento actual
        for conteo in atomos_reactivos:
            fila.append(float(conteo.get(i, 0)))

        # De igual forma recorro los productos solo que con signo negativo
        for conteo in atomos_productos:
            fila.append(-float(conteo.get(i, 0)))
        
        # Y aqui voy poniendo cada una de las filas dentro de la matriz
        matriz.append(fila)

    return matriz, elementos, compuestos




# Esta funcion aplica el metodo de eliminacion de Gauss-Jordan sobre la matriz
# El objetivo es reducirla a su forma reducida o escalonada
# Ya que de esta forma se identifican facilmente los coefientes del balanceo
def gauss_jordan(matriz):
    
    # Hago una copia de la matriz para no modificar la original
    matriz = [fila[:] for fila in matriz]
    # E identifico el numero de filas y el numero de columnas

    num_filas = len(matriz)
    num_cols  = len(matriz[0]) if matriz else 0
    
    # Esta variable lleva el control de en que fila estamos colocando el siguiente pivote
    fila_pivote = 0 

    # Recorro columna por columna buscando pivotes para ir reduciendo la matriz
    for i in range(num_cols):

        # Busco la primera fila desde fila_pivote hacia abajo que tenga un valor distinto de cero en esta columna
        # ese sera el elemento pivote con el que vamos a operar
        fila_no_cero = None
        for fila in range(fila_pivote, num_filas):
            if abs(matriz[fila][i]) > 1e-9: 
                fila_no_cero = fila
                break
        
        # Si no encuentro ningun valor distinto de cero en esta columna, la salto
        # esto significa que es una columna libre y no aporta un pivote
        if fila_no_cero is None:
            continue

        # Intercambio la fila encontrada con la fila pivote actual
        # para colocar el pivote en la posicion correcta de la matriz
        matriz[fila_pivote], matriz[fila_no_cero] = (
            matriz[fila_no_cero], matriz[fila_pivote]
        )

        # Normalizo la fila del pivote dividiendo toda la fila por el valor del pivote
        # de esta manera el pivote queda igual a 1, como requiere la forma RREF
        pivote = matriz[fila_pivote][i]
        matriz[fila_pivote] = [x / pivote for x in matriz[fila_pivote]]

        # Elimino el valor de esta columna en todas las demas filas
        # tanto hacia arriba como hacia abajo, para que solo el pivote tenga valor distinto de cero
        for fila in range(num_filas):
            if fila != fila_pivote and abs(matriz[fila][i]) > 1e-9:
                factor = matriz[fila][i]
                
                # Resto a cada elemento de la fila actual el factor multiplicado por la fila pivote
                # esto es el paso clasico de eliminacion de Gauss-Jordan
                matriz[fila] = [
                    matriz[fila][j] - factor * matriz[fila_pivote][j]
                    for j in range(num_cols)
                ]

        # Avanzo al siguiente pivote en la fila de abajo
        fila_pivote += 1   

    return matriz


# Esta funcion toma la matriz ya reducida (RREF) y extrae los coeficientes de la ecuacion quimica
# Se fija el ultimo compuesto con valor 1 y despeja los demas usando las filas de la matriz
def extraer_coeficientes(matriz_rref, num_compuestos):
    
    coeficientes = [0.0] * num_compuestos

    # Fijo el ultimo compuesto en 1 como variable libre
    # esto es necesario porque el sistema es homogeneo y tiene infinitas soluciones
    # al fijar uno podemos encontrar los valores de los demas
    coeficientes[num_compuestos - 1] = 1.0

    # Recorro las filas de la matriz en orden inverso para hacer sustitucion hacia atras
    for fila in reversed(matriz_rref):

        # Busco el pivote de esta fila, es decir el primer valor distinto de cero
        col_pivote = None
        for j in range(num_compuestos):
            if abs(fila[j]) > 1e-9:
                col_pivote = j
                break

        # Si la fila es toda ceros la salto ya que no aporta informacion util
        if col_pivote is None:
            continue  

        # Despejo el coeficiente correspondiente al pivote
        # sumando la contribucion de todas las otras columnas de esa fila
        valor = 0.0
        for j in range(num_compuestos):
            if j != col_pivote:
                valor -= fila[j] * coeficientes[j]
        
        coeficientes[col_pivote] = valor

    return coeficientes




# Esta es una funcion auxiliar que calcula el Minimo Comun Multiplo (MCM) de dos numeros
# Lo usaremos mas adelante para convertir los coeficientes decimales en numeros enteros
def m_c_m(a, b):

    # La formula del MCM se obtiene dividiendo el producto de los dos numeros entre su MCD
    return abs(a * b) // gcd(a, b)




# Esta funcion convierte los coeficientes flotantes que salen de la RREF en numeros enteros
# ya que los coeficientes de una ecuacion quimica balanceada deben ser enteros positivos
def racionalizar_coeficientes(coeficientes, tolerancia=1e-6, max_denominador=1000):

    # Para cada coeficiente busco el denominador que mejor lo aproxima como fraccion p/q
    denominadores = []

    for c in coeficientes:
        mejor_error      = float('inf')
        mejor_denominador = 1

        # Pruebo denominadores desde 1 hasta max_denominador y me quedo con el que da menor error
        for q in range(1, max_denominador + 1):
            p     = round(c * q)
            error = abs(c - p / q)

            if error < mejor_error:
                mejor_error       = error
                mejor_denominador = q

            # Si el error ya es suficientemente pequeno con este denominador, no sigo buscando
            if error < tolerancia:
                break   

        denominadores.append(mejor_denominador)

    # Calculo el MCM de todos los denominadores encontrados
    # esto me da el minimo numero por el que debo multiplicar para que todos queden enteros
    mcm = denominadores[0]
    for d in denominadores[1:]:
        mcm = m_c_m(mcm, d)

    # Multiplico cada coeficiente por el MCM y redondeo para obtener enteros
    # uso abs para asegurar que todos sean positivos
    enteros = [abs(round(c * mcm)) for c in coeficientes]

    # Finalmente simplifico los coeficientes dividiendo entre su MCD total
    # asi obtenemos los coeficientes minimos enteros positivos de la ecuacion balanceada
    mcd_total = enteros[0]
    for e in enteros[1:]:
        mcd_total = gcd(mcd_total, e)

    if mcd_total > 1:
        enteros = [e // mcd_total for e in enteros]

    return enteros




# Esta es la funcion principal del modulo que une todos los pasos anteriores
# Recibe los reactivos y productos como listas de strings y devuelve los coeficientes balanceados
def calcular_coeficientes(reactivos, productos):

    # Primero construyo la matriz estequiometrica a partir de los compuestos
    matriz_original, elementos, compuestos = construir_matriz(reactivos, productos)

    # Luego aplico Gauss-Jordan para reducir la matriz a su forma RREF
    matriz_rref = gauss_jordan(matriz_original)

    # Con la matriz reducida extraigo los coeficientes como valores flotantes
    num_compuestos       = len(compuestos)
    coeficientes_float   = extraer_coeficientes(matriz_rref, num_compuestos)

    # Finalmente los convierto a enteros para obtener los coeficientes finales de la ecuacion
    coeficientes_enteros = racionalizar_coeficientes(coeficientes_float)

    return coeficientes_enteros, compuestos, matriz_original, matriz_rref, elementos




# Esta funcion es de utilidad para visualizar cualquier matriz de forma ordenada en la consola
# Recibe la matriz, los elementos quimicos, los compuestos y un titulo opcional
def imprimir_matriz(matriz, elementos, compuestos, titulo="Matriz"):

    # Defino el ancho de cada columna para que la tabla se vea alineada
    ancho_col = 10   

    # Imprimo el encabezado con el titulo de la matriz
    print(f"\n{'='*60}")
    print(f"  {titulo}")
    print(f"{'='*60}")

    # Construyo y muestro la fila de encabezado con los nombres de los compuestos
    encabezado = f"{'Elem':>6} |"
    for comp in compuestos:
        encabezado += f"{comp:>{ancho_col}}"
    print(encabezado)

    # Imprimo una linea separadora entre el encabezado y los datos
    print(f"{'-'*6}-+{'-'*ancho_col*len(compuestos)}")

    # Recorro cada fila de la matriz e imprimo el elemento y sus valores con formato de 3 decimales
    for i, elemento in enumerate(elementos):
        fila_str = f"{elemento:>6} |"
        for val in matriz[i]:
            fila_str += f"{val:>{ancho_col}.3f}"
        print(fila_str)

    # Cierro la tabla con una linea final
    print(f"{'='*60}\n")

    return matriz