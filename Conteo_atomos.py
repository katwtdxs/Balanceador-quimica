"""
Módulo: verificar_atomos
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

# Lo primero que hago es importar la funcion de traductor
# que es el diccionario con la cantidad de moles de cada elemento

from traductor import conocer_cantidad_moles


def contar_atomos_lado(compuestos, coeficientes):
   
    conteo = {}
    for comp, coef in zip(compuestos, coeficientes):
        atomos = conocer_cantidad_moles(comp)
        for elemento, cantidad in atomos.items():
            conteo[elemento] = conteo.get(elemento, 0) + cantidad * coef
    return conteo


def tabla_verificacion(reactivos, productos, coeficientes, compuestos):
   
    n_reactivos = len(reactivos)


    coef_antes = [1] * len(compuestos)


    coef_react_bal = coeficientes[:n_reactivos]
    coef_prod_bal  = coeficientes[n_reactivos:]

    antes_react = contar_atomos_lado(reactivos, [1] * n_reactivos)
    antes_prod  = contar_atomos_lado(productos,  [1] * len(productos))

    desp_react  = contar_atomos_lado(reactivos, coef_react_bal)
    desp_prod   = contar_atomos_lado(productos,  coef_prod_bal)


    elementos = sorted(set(antes_react) | set(antes_prod))

    return {
        "antes_reactivos":   antes_react,
        "antes_productos":   antes_prod,
        "despues_reactivos": desp_react,
        "despues_productos": desp_prod,
        "elementos":         elementos,
    }