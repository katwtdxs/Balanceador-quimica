"""
Módulo: Main
Descripción:
    Punto de entrada del programa. Gestiona el flujo principal de la
    aplicación: recibe la ecuación del usuario, invoca el balanceo,
    clasifica la reacción, calcula masas molares y registra el resultado
    en el historial.
Dependencias:
    - Traductor
    - matrices
    - Tipo_reaccion
    - Calculo_molar
    - Historial
"""

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

# MASA MOLARES 
#Función realizada por Karen González

"""
    Para expresar más información del balanceo tambien calculamos la masa molar de los compuestos
    tanto de los reactivos y de los productos
"""

# Import necesario para usar el traductor
from Traductor import conocer_cantidad_moles

#Creamos un diccionario con los elementos y sus respectivas masas molares
masa_molar_elementos ={
    "H": 1.008, "He": 4.003, "Li": 6.941, "Be": 9.012,
    "B": 10.811, "C": 12.011, "N": 14.007, "O": 15.999,
    "F": 18.998, "Ne": 20.180, "Na": 22.990, "Mg": 24.305,
    "Al": 26.982, "Si": 28.086, "P": 30.974, "S": 32.060,
    "Cl": 35.453, "Ar": 39.948, "K": 39.098, "Ca": 40.078,
    "Sc": 44.956, "Ti": 47.867, "V": 50.942, "Cr": 51.996,
    "Mn": 54.938, "Fe": 55.845, "Co": 58.933, "Ni": 58.693,
    "Cu": 63.546, "Zn": 65.380, "Ga": 69.723, "Ge": 72.630,
    "As": 74.922, "Se": 78.971, "Br": 79.904, "Kr": 83.798,
    "Rb": 85.468, "Sr": 87.620, "Y": 88.906, "Zr": 91.224,
    "Nb": 92.906, "Mo": 95.950, "Tc": 98.000, "Ru": 101.070,
    "Rh": 102.906, "Pd": 106.420, "Ag": 107.868, "Cd": 112.414,
    "In": 114.818, "Sn": 118.710, "Sb": 121.760, "Te": 127.600,
    "I": 126.904, "Xe": 131.293, "Cs": 132.905, "Ba": 137.327,
    "La": 138.905, "Ce": 140.116, "Pr": 140.908, "Nd": 144.242,
    "Pm": 145.000, "Sm": 150.360, "Eu": 151.964, "Gd": 157.250,
    "Tb": 158.925, "Dy": 162.500, "Ho": 164.930, "Er": 167.259,
    "Tm": 168.934, "Yb": 173.054, "Lu": 174.967, "Hf": 178.490,
    "Ta": 180.948, "W": 183.840, "Re": 186.207, "Os": 190.230,
    "Ir": 192.217, "Pt": 195.084, "Au": 196.967, "Hg": 200.592,
    "Tl": 204.383, "Pb": 207.200, "Bi": 208.980, "Po": 209.000,
    "At": 210.000, "Rn": 222.000, "Fr": 223.000, "Ra": 226.000,
    "Ac": 227.000, "Th": 232.038, "Pa": 231.036, "U": 238.029,
    "Np": 237.000, "Pu": 244.000, "Am": 243.000, "Cm": 247.000,
    "Bk": 247.000, "Cf": 251.000, "Es": 252.000, "Fm": 257.000,
    "Md": 258.000, "No": 259.000, "Lr": 262.000
    }
 
def calculo_masa_molar(compuesto):
    elementos = conocer_cantidad_moles(compuesto) #Con la función de calculo de moles de las sustancias sacamos esos valores
    masa = 0 #Iniciamos un contador para la masa
    
    for simbolo, cantidad in elementos.items(): #Se abre un bucle para recorrer los elementos del compuesto 
        # Validación mínima por si el elemento no está en la tabla
        if simbolo not in masa_molar_elementos:
            raise ValueError(f"Elemento desconocido: {simbolo}")
        
        masa += masa_molar_elementos[simbolo] * cantidad #A la masa se le añade el valor de la masa del elemento multiplicado por los moles presentes
    
    return round(masa, 3) # Se devuelve el valor de la masa redondeado con 3 decimales


# HISTORIAL EN TXT 
# Función realizada por Lizeth Sastoque

ARCHIVO_HISTORIAL = "historial.txt"


def guardar_en_historial(ecuacion, balanceada, tipo, masas):
    """
    Guarda los resultados en un archivo .txt de forma legible
    """

    with open(ARCHIVO_HISTORIAL, "a", encoding="utf-8") as archivo:
        archivo.write("=====================================\n")
        archivo.write(f"Ecuación: {ecuacion}\n")
        archivo.write(f"Balanceada: {balanceada}\n")
        archivo.write(f"Tipo de reacción: {tipo}\n")
        archivo.write("Masas molares:\n")

        for comp, masa in masas.items():
            archivo.write(f"  {comp}: {masa} g/mol\n")

        archivo.write("=====================================\n\n")


import streamlit as st
import os


#  INTERFAZ 

st.set_page_config(page_title="Balanceador Químico", page_icon="🧪")

st.title("🧪 Balanceador de Ecuaciones Químicas")
st.write("Ingresa una ecuación química para analizarla")

ecuacion = st.text_input("Ejemplo: H2 + O2 = H2O")

if st.button("🔍 Analizar"):

    if ecuacion.strip() == "":
        st.warning("Por favor ingresa una ecuación")
    else:
        try:
#  SEPARAR 
            reactivos, productos = Separar_ecuacion(ecuacion)

 # BALANCEAR 
            coeficientes, compuestos, _, _, _ = calcular_coeficientes(reactivos, productos)

# Construir ecuación balanceada
            ecuacion_balanceada = ""
            for i, comp in enumerate(compuestos):
                coef = coeficientes[i]

                if coef != 1:
                    ecuacion_balanceada += f"{coef}{comp}"
                else:
                    ecuacion_balanceada += comp

                if i == len(reactivos) - 1:
                    ecuacion_balanceada += " = "
                elif i < len(compuestos) - 1:
                    ecuacion_balanceada += " + "

            st.subheader(" Ecuación balanceada")
            st.success(ecuacion_balanceada)
 #  TIPO DE REACCIÓN 
            tipo = clasificar_reaccion(ecuacion)

            st.subheader(" Tipo de reacción")
            st.info(tipo)

 # MASA MOLAR 
            st.subheader(" Masas molares")

            masas = {}
            for comp in compuestos:
                masa = calculo_masa_molar(comp)
                masas[comp] = masa
                st.write(f"{comp}: {masa} g/mol")

#  GUARDAR HISTORIAL
            guardar_en_historial(
                ecuacion,
                ecuacion_balanceada,
                tipo,
                masas
            )

        except Exception as e:
            st.error(f"Error: {e}")


#  HISTORIAL

st.markdown("---")
st.header(" Historial")

mostrar_historial()
exportar_historial()

st.header("Historial ecuaciones balanceadas")

# Mostrar historial en Streamlit
try:
    with open("historial.txt", "r") as archivo:
        contenido = archivo.read()
        if contenido.strip() == "":
            st.write("No hay historial todavía")
        else:
            st.text(contenido)
except FileNotFoundError:
    st.write("No hay historial todavía")

# Botón exportar
if st.button("Exportar historial"):
    exportar_txt()

