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
    reactivos= lista_compuestos[0].split("+") #El elemento [0] son los reactivos
    productos= lista_compuestos[1].split("+") #El elemento [1] son los productos

    return reactivos, productos #Aquí nos devuelve dos listas


def conocer_cantidad_moles(sustancia):
    """
        Esta función nos permite contar la cantidad de moles que tiene un compuesto o elemento en la reacción
    """
    dict_elementos ={} #Creamos un diccionario donde se van a guardar los valores de el elemento y el numero de moles que tiene
    dict_temporal_parentesis ={} #Este es un diccionario temporal para los elementos dentro de un parentesis
    parentesis = "Fuera"
    i = 0 #Iniciamos un contador poder recorrer el string en el while

    while i < len(sustancia): 
        letra = sustancia[i] #La letra va a ser la del index 0 hasta la de index de la cantidad de letras que

        if letra == "(": #Esta condición se utiliza cuando el compuesto tiene parentesis por ejemplo Fe2(SO4)3
            #Cuando entra en un parentesis el valor adquiere una condicion que incica que esta dentro del parenteis
            parentesis = "Dentro" 
            dict_temporal_parentesis = {} #Se actualiza el diccionario de parentesis
            i += 1 #Actualiza el contador
            
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



        