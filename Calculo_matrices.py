# Funcion realizada por Santiago Hernández

# Inicialmente importo la funcion gcd de la libreria math, esta funcion es por sus siglas en ingles
# Greatest Common Divisor, que es el maximo comun divisor, esta funcion es necesaria para simplificar fracciones
# Y se usara mas adelante al racionalizar los coeficientes

from math import gcd

# Adicionalmente importo la funcion conocer_cantidad_moles de Traductor para contar con el diccionario de los coeficientes 
from Traductor import conocer_cantidad_moles 


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
        # esta linea significa que en elementos se va a agragar la llave del diccionario cada iteracion
        # Por lo que voy a tener todos los elementos presentes en la reaccion, pero por el set aquellos que aparecen doble
        # no se van a repetir
        elementos.update(conteo.keys())

    # Ahora con el conjunto de todos los elementos de la reaccion
    # Lo que sigue es ordenarlos en orden alfabetico 
    elementos  = sorted(elementos)
    # Y ahora creo una lista donde junto todos los elementos de la reaccion de los productos y los reactivos   
    compuestos = reactivos + productos         

    # Creo la matriz vacia donde se almacenaran los coeficientes de cada uno de los elementos
    # Para crear esta matriz y que represente correctamente la reaccion, tengo en cuenta el documento base para el codigo
    # donde basicamente se dice que las filas de la matriz seran los elementos aislados de la reaccion por ejemplo H solo
    # y las columnas es cada uno de los compuestos, sin importar si estan repetidos o no, ya que el punto es balancearlos

    matriz = []
    # Y ahora con este bucle recorro todo el conjunto que me asegure de tener compuestos no repetidos
    for i in elementos:

        # Creo la fila vacia para cada ciclo es decir donde se guardara cada uno de los elementos
        fila = []

        # Ahora en este bucle recorro todos los reactivos o los elementos iniciales de la reaccion
        # Entonces vamos de adentro hacia afuera, lo primo que hace el bucle es buscar en los reactivos el elemento que obtiene del diccionario, si este elemento efectivamente esta en los reactivos recupera su valor lo vuelve a float y lo añade a la fila, si el elemento no esta en los reactivos devuelve 0 
        for conteo in atomos_reactivos:
            fila.append(float(conteo.get(i, 0)))

        # Aqui vuelvo a ejecutar un for similar solo que la diferencia esta en el rango, que es para los productos
        # Ademas de esto, el valor que se añade para los coeficientes es negativo 
        # porque la resta entre reactivos y productos debe ser igual a 0, asegurando que lo inicial es igual a lo final
        for conteo in atomos_productos:
            fila.append(-float(conteo.get(i, 0)))

        # Al finalizar todo este proceso de deteccion de coeficientes, se añade la fila a la matriz, y se repite esto con cada uno de los elementos de la reaccion para conseguir el numero de filas y columnas completo 
        matriz.append(fila)

    # Al finalizar ya toda la funcion devuelvo la matriz ya calculada, la lista de elementos y todos los compuestos.
    return matriz, elementos, compuestos




def gauss_jordan(matriz):
    
    # Primero genero una copia de la matriz que calucule con la funcion anterior
    # Esto basicamente para no perder los valores de la matriz original, al operarla y reducirla
    # ya que al aplicar gauss jordan, la matriz se va a ver modificada a su forma reducida
    # basicamente para generar esta copia, recorro la matriz original en su cantidad de filas, o listas 
    # y por cada bucle la copio en la matriz copia, que es identica
    matriz = [fila[:] for fila in matriz]
    # Ahora guardo en variables apartes el numero de elementos que son iguales a las filas
    # y tambien el numero de compuestos que son las columnas
    num_filas = len(matriz)
    num_cols  = len(matriz[0])
    
    # Marco la fila para el siguiente pivote, que es la fila que elimina los valores que estan por debajo de ella
    fila_pivote = 0 

    # Dentro de este for intento encontrar un punto pivote en cada una de las columnas
    for i in range(num_cols):

        # Busco una fila con un valor util en la columna encontrada como valor pivote
        # basicamente con un valor mayor a 1e-9, mantengo la precision, y si la condicion se cumple para el valor 
        # esa fila es mayor de cero, y por lo tanto es un pivote para eliminar los valores debajo de el
        fila_no_cero = None
        for fila in range(fila_pivote, num_filas):
            if abs(matriz[fila][i]) > 1e-9: 
                fila_no_cero = fila
                break
        
        # Si toda la columna tiene valores de cero, entonces no hay pivote, por lo que la variable queda libre
        if fila_no_cero is None:
            continue

        # subo la fila valida a la posicion del pivote
        matriz[fila_pivote], matriz[fila_no_cero] = (
            matriz[fila_no_cero], matriz[fila_pivote]
        )

        # Cambio el valor del pivote al valor de la iteracion del for
        # Y luego divido toda la fila entre el valor pivote como el valor de la iteracion
        pivote = matriz[fila_pivote][i]
        matriz[fila_pivote] = [x / pivote for x in matriz[fila_pivote]]

        #  Recorro el valor numerico que tengo de filas, es decir que si son dos elementos hara dos ciclos
        for fila in range(num_filas):
            # Ahora paso por alto la fila pivote, por lo que solo filas que no sean definidas de esa forma seran operadas
            # ademas de la condicion de contar con un valor mayor al limite puesto de 1e-9
            if fila != fila_pivote and abs(matriz[fila][i]) > 1e-9:
                # Factor es la variable que determina cuanto es lo que se tiene que eliminar
                #  de cada uno de los terminos de la matriz
                factor = matriz[fila][i]
                # y ahora vuelvo cambio los valores de la matriz restando la combinacion de la fila pivote por las columnas
                # como resultado esa columna queda en 0 en todas las filas que no sean la pivote
                """Dando como resultado una matriz escalonada que para no dar un ejemplo muy largo lo hare solo con una 3x3,
                siendo que se describe de la siguiente forma:
                                               [
                                                 [1 0 0]  
                                                 [0 1 0]  
                                                 [0 0 1]
                                                 ]
                entonces vemos como el valor de 1 es correspondiente a solo una columna y una fila, lo que nos indica que ese elemento tiene un coeficiente.  

                """ 
                
                matriz[fila] = [
                    matriz[fila][j] - factor * matriz[fila_pivote][j]
                    for j in range(num_cols)
                ]

        # Aumento la variable de fila pivore mas 1        
        fila_pivote += 1   

    # Y al terminar con el bucle mas grande devuelvo el valor de la matriz
    # Pero ojo esta no es la misma matriz del principio, sino la escalonada resultado de reducir la primer matriz
    return matriz


def extraer_coeficientes(matriz_rref, num_compuestos):

    # Creo una lista de coeficientes inicializada en 0
    coeficientes = [0.0] * num_compuestos

    # Fijo la ultima variable como 1 (variable libre)
    # Esto es necesario porque el sistema es homogéneo y tiene infinitas soluciones
    coeficientes[num_compuestos - 1] = 1.0

    # Recorro la matriz desde abajo hacia arriba
    # Esto simula una sustitucion hacia atras
    for fila in reversed(matriz_rref):

        # Ahora busco la posicion del pivote en la fila
        col_pivote = None
        for j in range(num_compuestos):
            if abs(fila[j]) > 1e-9:
                col_pivote = j
                break

        # Si la fila es toda cero, la ignoro porque seria una fila sin coeficientes
        if col_pivote is None:
            continue  

        # Calculo el valor del coeficiente usando los ya conocidos
        # Esto mediante un for hasta el valor de numero de compuestos
        valor = 0.0
        for j in range(num_compuestos):
            # Si el de columnas pivote es distinto de el valor de la iteracion
            # Se multiplican los valores que estan en la fila de j por el coeficiente de j
            if j != col_pivote:
                valor -= fila[j] * coeficientes[j]
        
        # Hay que recordar que cada fila de la matriz de gauss jordan (RREF) es una ecuación.
        # por lo que se puede despejar
        coeficientes[col_pivote] = valor

    return coeficientes




def m_c_m(a, b):

    # Calculo el minimo comun multiplo usando el gcd
    # Q es la funcion que importe al imprincipio
    return abs(a * b) // gcd(a, b)




def racionalizar_coeficientes(coeficientes, tolerancia=1e-6, max_denominador=1000):

    # Aqui convierto los coeficientes decimales a fracciones equivalentes
    # buscando el mejor denominador posible dentro de un rango

    denominadores = []

    for c in coeficientes:
        mejor_error      = float('inf')
        mejor_denominador = 1

        # Busco el denominador que mejor aproxima el decimal
        for q in range(1, max_denominador + 1):
            p     = round(c * q)
            error = abs(c - p / q)

            if error < mejor_error:
                mejor_error       = error
                mejor_denominador = q

            # Si ya es suficientemente preciso, corto el bucle
            if error < tolerancia:
                break   

        denominadores.append(mejor_denominador)

    # Calculo el minimo comun multiplo de todos los denominadores
    mcm = denominadores[0]
    for d in denominadores[1:]:
        mcm = m_c_m(mcm, d)

    # Multiplico todos los coeficientes para volverlos enteros
    enteros = [abs(round(c * mcm)) for c in coeficientes]

    # Simplifico dividiendo por el maximo comun divisor
    mcd_total = enteros[0]
    for e in enteros[1:]:
        mcd_total = gcd(mcd_total, e)

    if mcd_total > 1:
        enteros = [e // mcd_total for e in enteros]

    return enteros




def calcular_coeficientes(reactivos, productos):

    # Construyo la matriz inicial de la reaccion
    matriz_original, elementos, compuestos = construir_matriz(reactivos, productos)

    # Aplico Gauss-Jordan para reducir la matriz
    matriz_rref = gauss_jordan(matriz_original)

    # Extraigo los coeficientes en forma decimal
    num_compuestos       = len(compuestos)
    coeficientes_float   = extraer_coeficientes(matriz_rref, num_compuestos)

    # Los convierto a enteros
    coeficientes_enteros = racionalizar_coeficientes(coeficientes_float)

    # Devuelvo toda la informacion relevante
    return coeficientes_enteros, compuestos, matriz_original, matriz_rref, elementos




def imprimir_matriz(matriz, elementos, compuestos, titulo="Matriz"):

    # Defino el ancho de cada columna para que la impresion sea ordenada
    ancho_col = 10   

    print(f"\n{'='*60}")
    print(f"  {titulo}")
    print(f"{'='*60}")

    # Imprimo encabezados (compuestos)
    encabezado = f"{'Elem':>6} |"
    for comp in compuestos:
        encabezado += f"{comp:>{ancho_col}}"
    print(encabezado)

    print(f"{'-'*6}-+{'-'*ancho_col*len(compuestos)}")

    # Imprimo cada fila con su elemento correspondiente
    for i, elemento in enumerate(elementos):
        fila_str = f"{elemento:>6} |"
        for val in matriz[i]:
            fila_str += f"{val:>{ancho_col}.3f}"
        print(fila_str)

    print(f"{'='*60}\n")

    return matriz

