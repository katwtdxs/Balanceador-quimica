# Función realizada por Lizeth Sastoque

"""
En este módulo verificamos si una ecuación química
ya está balanceada antes de intentar resolverla.

La idea es sencilla:
si ambos lados de la ecuación tienen exactamente
la misma cantidad de átomos de cada elemento,
entonces la ecuación ya está balanceada.

Aquí usamos funciones del módulo traductor
para separar la ecuación y contar los átomos
presentes en cada compuesto.
"""

from traductor import Separar_ecuacion, conocer_cantidad_moles


# Esta función cuenta todos los átomos presentes
# en un lado de la ecuación teniendo en cuenta
# los coeficientes de cada compuesto
def _contar_atomos(compuestos, coeficientes):

    conteo = {}

    # Recorremos cada compuesto junto con su coeficiente
    for comp, coef in zip(compuestos, coeficientes):

        # Obtenemos los elementos y cantidades del compuesto
        for elemento, cantidad in conocer_cantidad_moles(comp).items():

            # Multiplicamos la cantidad de átomos
            # por el coeficiente correspondiente
            conteo[elemento] = (
                conteo.get(elemento, 0) +
                cantidad * coef
            )

    # Devolvemos el conteo total de átomos
    return conteo


# Esta función revisa si la ecuación escrita
# por el usuario ya está balanceada
def ecuacion_ya_balanceada(ecuacion: str) -> tuple:

    # Separamos reactivos y productos
    reactivos, productos = Separar_ecuacion(ecuacion)

    # Contamos los átomos de los reactivos
    # usando coeficiente 1 para todos
    atomos_r = _contar_atomos(
        reactivos,
        [1] * len(reactivos)
    )

    # Contamos los átomos de los productos
    atomos_p = _contar_atomos(
        productos,
        [1] * len(productos)
    )

    # Unimos todos los elementos presentes
    # en ambos lados de la ecuación
    elementos = set(atomos_r.keys()) | set(atomos_p.keys())

    detalle = {}

    # Suponemos inicialmente que sí está balanceada
    balanceada = True

    # Revisamos elemento por elemento
    for elem in sorted(elementos):

        cant_r = atomos_r.get(elem, 0)
        cant_p = atomos_p.get(elem, 0)

        # Verificamos si coinciden
        coincide = cant_r == cant_p

        # Si algún elemento no coincide
        # entonces la ecuación no está balanceada
        if not coincide:
            balanceada = False

        # Guardamos el detalle del análisis
        detalle[elem] = {

            "reactivos": cant_r,
            "productos": cant_p,
            "ok": coincide
        }

    # Devolvemos:
    # True/False dependiendo del balance
    # y el detalle completo de cada elemento
    return balanceada, detalle
