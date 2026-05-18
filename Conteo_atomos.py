"""
Módulo: conteo_atomos
Autor: Santiago Hernandez
Descripción:
    Cuenta los átomos totales de cada elemento en ambos lados de la
    ecuación (reactivos y productos), antes y después del balanceo.
    Permite verificar que la ecuación quede correctamente balanceada.
Funciones:
    - contar_atomos_lado(compuestos, coeficientes): Cuenta átomos totales
      de una lista de compuestos con sus coeficientes.
    - tabla_verificacion(reactivos, productos, coeficientes, compuestos):
      Devuelve un diccionario con el conteo antes y después del balanceo.
Dependencias:
    - traductor.conocer_cantidad_moles
"""

# Importo conocer_cantidad_moles de traductor, que es la funcion que ya sabe
# leer un compuesto como "H2O" y devuelve cuantos atomos tiene de cada elemento
from traductor import conocer_cantidad_moles


# Esta funcion se encarga de sumar todos los atomos de un lado de la ecuacion
# Recibe los compuestos y sus coeficientes en el mismo orden, y los recorre juntos con zip
def contar_atomos_lado(compuestos, coeficientes):

    # Aqui vamos a ir acumulando el total de atomos de cada elemento
    conteo = {}

    for comp, coef in zip(compuestos, coeficientes):

        # Le pregunto a traductor cuantos atomos tiene este compuesto
        atomos = conocer_cantidad_moles(comp)

        for elemento, cantidad in atomos.items():
            # Multiplico la cantidad de atomos por el coeficiente del compuesto
            # y la sumo al total, usando get para arrancar en 0 si el elemento es nuevo
            conteo[elemento] = conteo.get(elemento, 0) + cantidad * coef

    return conteo


# Funcion principal del modulo, construye toda la informacion que necesita la tabla
# Recibe los reactivos, productos, los coeficientes ya balanceados y la lista unificada de compuestos
def tabla_verificacion(reactivos, productos, coeficientes, compuestos):

    # Necesito saber cuantos reactivos hay para poder partir la lista de coeficientes en dos
    n_reactivos = len(reactivos)

    # El truco para el "antes": simplemente uso coeficiente 1 en todos los compuestos
    # como si la ecuacion todavia no estuviera balanceada
    antes_react = contar_atomos_lado(reactivos, [1] * n_reactivos)
    antes_prod  = contar_atomos_lado(productos,  [1] * len(productos))

    # Para el "despues" parto la lista de coeficientes balanceados en dos:
    # los primeros n_reactivos son de los reactivos, el resto son de los productos
    coef_react_bal = coeficientes[:n_reactivos]
    coef_prod_bal  = coeficientes[n_reactivos:]

    desp_react = contar_atomos_lado(reactivos, coef_react_bal)
    desp_prod  = contar_atomos_lado(productos,  coef_prod_bal)

    # Uno los elementos de ambos lados con | (union de conjuntos) para no perder ninguno
    # y los ordeno alfabeticamente para que la tabla siempre salga igual
    elementos = sorted(set(antes_react) | set(antes_prod))

    # Devuelvo todo en un diccionario para que Main.py pueda armar la tabla facilmente
    return {
        "antes_reactivos":   antes_react,
        "antes_productos":   antes_prod,
        "despues_reactivos": desp_react,
        "despues_productos": desp_prod,
        "elementos":         elementos,
    }