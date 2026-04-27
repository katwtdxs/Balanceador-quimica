# Traductor y visualización 

#Función realizada por Karen González
"""
    Para poder iniciar a asignarle un coeficiente a cada compuesto es necesalio convertir
    el string que se ingresa en el input en información que se pueda manejar en el calculo
"""

## Función :

def Separar_ecuacion(cadena):
    """
        Esta función sirve para separar los reactivos de productos teniendo en cuenta que en el 
        imput (cadena) se separa por el simbolo "=" nos devuelve en el return las listas de compuestos 
        de reactivos y productos, los cuales se separan por el simbolo "+"
    """
    cadena=cadena.replace(" ", "") #Eliminamos posibles espacios
    lista_compuestos= cadena.split("=") 
    
    # Validación mínima para evitar errores si la ecuación está mal escrita
    if len(lista_compuestos) != 2:
        raise ValueError("La ecuación debe contener un '='")
    
    reactivos= lista_compuestos[0].split("+") #El elemento [0] son los reactivos
    productos= lista_compuestos[1].split("+") #El elemento [1] son los productos

    return reactivos, productos #Aquí nos devuelve dos listas


def conocer_cantidad_moles(sustancia):
    """
        Esta función nos permite contar la cantidad de moles que tiene un compuesto o elemento en la reacción
    """
    dict_elementos ={} #Creamos un diccionario donde se van a guardar los valores de el elemento y el numero de moles que tiene
    dict_temporal_parentesis ={} #Este es un diccionario temporal para los elementos dentro de un parentesis

# TIPO DE REACCION
# Funcion realizada por Julian Ruiz

# Importaciones necesarias para que funcione con el resto del sistema
from Traductor import conocer_cantidad_moles, Separar_ecuacion


def contar_elementos(compuesto):
 #Obtiene los elementos presentes en un compuesto
  
    return set(conocer_cantidad_moles(compuesto).keys())


def es_elemento_puro(compuesto):
    return len(contar_elementos(compuesto)) == 1
#Determina si es un elemento puro

def es_compuesto(compuesto):
    return len(contar_elementos(compuesto)) > 1
#Determina si es un compuesto

def es_hidrocarburo(compuesto):
    elems = contar_elementos(compuesto)
    return elems.issubset({"C", "H"}) and "C" in elems
#Identifica hidrocarburos

def contiene_oxigeno_molecular(lista):
    return "O2" in lista
#Hace que el sistema se de cuenta si los reactivos tienen O2 para darse cuenta de la combustion

# Ahora diferenciara las reacciones

def es_combustion(reactivos, productos):
#Determina si la reacción corresponde a una combustión.
    if not contiene_oxigeno_molecular(reactivos):
        return False

    hidrocarburo = any(es_hidrocarburo(r) for r in reactivos)

    produce_CO2 = any("CO2" in p for p in productos)
    produce_H2O = any("H2O" in p for p in productos)

    return hidrocarburo and produce_CO2 and produce_H2O


def es_sintesis(reactivos, productos):
    return len(reactivos) > len(productos)
 """
        Reacción de síntesis:

            A + B → AB
    """

def es_descomposicion(reactivos, productos):
    return len(reactivos) < len(productos)
 """
        Reacción de descomposición:

            AB → A + B
    """

def es_sustitucion_simple(reactivos, productos):
    """
        Reacción de sustitución simple:

            A + BC → AC + B
    """
    react_elemento = any(es_elemento_puro(r) for r in reactivos)
    react_compuesto = any(es_compuesto(r) for r in reactivos)

    prod_elemento = any(es_elemento_puro(p) for p in productos)
    prod_compuesto = any(es_compuesto(p) for p in productos)

    return react_elemento and react_compuesto and prod_elemento and prod_compuesto


def es_doble_sustitucion(reactivos, productos):
    """
        Reacción de doble sustitución:

            AB + CD → AD + CB
    """
    if len(reactivos) != 2 or len(productos) != 2:
        return False

    return all(es_compuesto(x) for x in reactivos + productos)


#Funcion principal para que entregue resultados

def clasificar_reaccion(ecuacion):
    """
    Recibe una ecuación química como string
    y devuelve el tipo de reacción.
    """

    reactivos, productos = Separar_ecuacion(ecuacion)

    if es_combustion(reactivos, productos):
        return "Combustion"

    if es_sintesis(reactivos, productos):
        return "Sintesis"

    if es_descomposicion(reactivos, productos):
        return "Descomposicion"

    if es_sustitucion_simple(reactivos, productos):
        return "Sustitucion simple"

    if es_doble_sustitucion(reactivos, productos):
        return "Doble sustitucion"

    return "Desconocida"
    parentesis = "Fuera"
    i = 0 #Iniciamos un contador poder recorrer el string en el while

    while i < len(sustancia): 
        letra = sustancia[i] #La letra va a ser la del index 0 hasta la de index de la cantidad de letras que

        if letra == "(": #Esta condición se utiliza cuando el compuesto tiene parentesis por ejemplo Fe2(SO4)3
            #Cuando entra en un parentesis el valor adquiere una condicion que incica que esta dentro del parenteis
            parentesis = "Dentro" 
            dict_temporal_parentesis = {} #Se actualiza el diccionario de parentesis
            i += 1 #Actualiza el contador
            continue
            
        elif letra == ")":
            #Cuando sale del parentesis el valor adquiere una condicion que indica que esta fuera del parenteis
            parentesis = "Fuera"
            i += 1
            
            # Al salir del parentesis debe haber un numero que multiplica el valor en el interior
            num = "" #Iniciamos un contador para ese numero
            while i < len(sustancia) and sustancia[i].isdigit():
                 #Este bucle nos agrega el caracter en el index [i]
                num += sustancia[i]
                i += 1 #Actualiza el contador
            if num:
              multiplicador = int(num)  #Pasa ese caracter a un valor numerico
            else:
              multiplicador= 1

            for elemento, cantidad in dict_temporal_parentesis.items(): #Aqui nos entrega los clave-valor del diccionario de los parentesis

                #Se actualizan los valores en el diccionario principal multiplicando el coeficiente del parentesis
                dict_elementos[elemento] = dict_elementos.get(elemento, 0) + cantidad * multiplicador 
            continue

            """
                Estos condicionales son los que determinan los elementos existentes en base a su estructura de simbolo: 
                Letra mayúscula o Letra mayúscula + Letra minúscula
            """
        elif letra.isupper():#La función .isupper() determina si es Mayúscula
            elemento = letra #Se actualiza el valor de el elemento
            i += 1 #Pasamos a la siguiente letra
            
            while i < len(sustancia) and sustancia[i].islower(): #Verificamos si la siguiente letra es minúscula ".islower()"
                elemento += sustancia[i] #Si lo es, se añade al elemento
                i += 1 #Pasa al siguiente carácter
            num = "" #Se crea un contador para el numero que acompaña al elemento
            while i < len(sustancia) and sustancia[i].isdigit(): #Verificamos sí el siguiemte valor es in numero ".isdigit"
                num += sustancia[i] #Se agrega ese numero al valor
                i += 1 #Pasa al siguiente carácter
            if num:
                cantidad = int(num)  #Pasa ese caracter a un valor numerico
            else:
                cantidad= 1


        #Estos condicionales indican que se hace con los valores en el diccionario si estan fuera o dentro del paréntesis
            if parentesis=="Dentro": #Dentro del paréntesis
                #Guarda el elemento en el diccionario temporal (el de adentro del paréntesis)
                dict_temporal_parentesis[elemento] = dict_temporal_parentesis.get(elemento, 0) + cantidad
            elif parentesis=="Fuera": #Fuera del paréntesis
                #Guarda el elemento en el diccionario principal                    
                dict_elementos[elemento] = dict_elementos.get(elemento, 0) + cantidad
                
        else: #Si no entra a ninguna condicion se actualiza para evitar un bucle infinito
            i+=1
    return dict_elementos #Devuelve un diccionario con los moles de cada elemento


# -------- FUNCIÓN AÑADIDA (SIN TOCAR LO ORIGINAL) --------

def mostrar_conteo(compuesto):
    """
    Muestra el conteo de átomos de forma organizada (para visualización)
    """
    conteo = conocer_cantidad_moles(compuesto)

    print(f"\nConteo de átomos en {compuesto}:")
    for elemento, cantidad in conteo.items():
        print(f"{elemento}: {cantidad}")

# CALCULO MATRICES 
# Función por Santiago Hernandez 

# Import necesario para usar el traductor
from Traductor import conocer_cantidad_moles


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
    conteos_reactivos = [conocer_cantidad_moles(r) for r in reactivos]
    conteos_productos = [conocer_cantidad_moles(p) for p in productos]

    conjunto_elementos = set()
    for conteo in conteos_reactivos + conteos_productos:
        conjunto_elementos.update(conteo.keys())

    elementos = sorted(conjunto_elementos)
    compuestos = reactivos + productos

    matriz = []
    for elemento in elementos:
        fila = []
        for conteo in conteos_reactivos:
            fila.append(float(conteo.get(elemento, 0)))
        for conteo in conteos_productos:
            fila.append(-float(conteo.get(elemento, 0)))
        matriz.append(fila)

    return matriz, elementos, compuestos


def gauss_jordan(matriz):

    """
    Aplica el método de eliminación de Gauss-Jordán a la matriz dada.
    """
    matriz = [fila[:] for fila in matriz]
    num_filas = len(matriz)
    num_cols = len(matriz[0]) if matriz else 0  # ajuste de seguridad

    fila_pivote = 0

    for col in range(num_cols):
        fila_no_cero = None
        for fila in range(fila_pivote, num_filas):
            if abs(matriz[fila][col]) > 1e-9:
                fila_no_cero = fila
                break

        if fila_no_cero is None:
            continue

        matriz[fila_pivote], matriz[fila_no_cero] = matriz[fila_no_cero], matriz[fila_pivote]

        pivote = matriz[fila_pivote][col]
        matriz[fila_pivote] = [x / pivote for x in matriz[fila_pivote]]

        for fila in range(num_filas):
            if fila != fila_pivote and abs(matriz[fila][col]) > 1e-9:
                factor = matriz[fila][col]
                matriz[fila] = [
                    matriz[fila][j] - factor * matriz[fila_pivote][j]
                    for j in range(num_cols)
                ]

        fila_pivote += 1

    return matriz


def extraer_coeficientes(matriz_rref, num_compuestos):

    """
    Extrae los coeficientes estequiométricos a partir de la matriz RREF.
    """
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


def minimo_comun_multiplo(a, b):
    from math import gcd
    return abs(a * b) // gcd(a, b)


def racionalizar_coeficientes(coeficientes, tolerancia=1e-6, max_denominador=1000):

    """
    Convierte los coeficientes de punto flotante en números enteros positivos.
    """
    from math import gcd

    denominadores = []

    for c in coeficientes:
        mejor_error = float('inf')
        mejor_denominador = 1

        for q in range(1, max_denominador + 1):
            p = round(c * q)
            error = abs(c - p / q)
            if error < mejor_error:
                mejor_error = error
                mejor_denominador = q
            if error < tolerancia:
                break

        denominadores.append(mejor_denominador)

    mcm = denominadores[0]
    for d in denominadores[1:]:
        mcm = minimo_comun_multiplo(mcm, d)

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

    num_compuestos = len(compuestos)
    coeficientes_float = extraer_coeficientes(matriz_rref, num_compuestos)

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


# -------- FUNCIÓN EXTRA PARA STREAMLIT --------

def matriz_a_texto(matriz, elementos, compuestos):
    """
    Convierte la matriz en texto para mostrar en Streamlit
    """
    texto = ""
    ancho_col = 10

    encabezado = f"{'Elem':>6} |"
    for comp in compuestos:
        encabezado += f"{comp:>{ancho_col}}"
    texto += encabezado + "\n"
    texto += f"{'-'*6}-+{'-'*ancho_col*len(compuestos)}\n"

    for i, elemento in enumerate(elementos):
        fila_str = f"{elemento:>6} |"
        for val in matriz[i]:
            fila_str += f"{val:>{ancho_col}.3f}"
        texto += fila_str + "\n"

    return texto


