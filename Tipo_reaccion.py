#Parte hecha por: Julian Ruiz

from traductor import conocer_cantidad_moles, Separar_ecuacion

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
    """
        Reacción de síntesis:

            A + B → AB
    """
    return len(reactivos) > len(productos)


def es_descomposicion(reactivos, productos):
    """
        Reacción de descomposición:

            AB → A + B
    """
    return len(reactivos) < len(productos)


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
