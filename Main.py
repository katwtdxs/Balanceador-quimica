# Programa principal realizado por el equipo del proyecto

"""
Este archivo es el nucleo principal de la aplicacion.

Aqui conectamos todos los modulos del proyecto
para construir la interfaz interactiva en Streamlit.

El sistema permite:

- Balancear ecuaciones quimicas
- Verificar atomos antes y despues del balanceo
- Identificar el tipo de reaccion
- Calcular masas molares
- Consultar elementos de la tabla periodica
- Practicar con un quiz interactivo
- Guardar y exportar historial de resultados

Cada funcionalidad esta organizada en pestanas
para que la aplicacion sea mas clara y facil de usar.
"""

import streamlit as st
import pandas as pd

# Importamos los modulos principales del proyecto
from traductor import Separar_ecuacion
from matrices import calcular_coeficientes
from Tipo_reaccion import clasificar_reaccion
from Calculo_molar import calculo_masa_molar
from historial import guardar_en_historial, exportar_como_txt, exportar_como_pdf
from explicacion_balanceo import explicar_balanceo
from verificar_atomos import tabla_verificacion
from verificacion import ecuacion_ya_balanceada

# Importamos modulos adicionales
from validacion import validar_ecuacion
from explicacion_reacciones import obtener_explicacion
from tabla_periodica import (
    buscar_elemento,
    obtener_color_categoria
)
from quiz import (
    obtener_pregunta_aleatoria,
    verificar_respuesta
)


# Configuracion general de la pagina
st.set_page_config(
    page_title="Balanceador Quimico",
    page_icon="",
    layout="wide"
)

# Titulo principal de la aplicacion
st.title("Balanceador de Ecuaciones Quimicas")


# Creamos las pestanas principales del sistema
pestanas = st.tabs([
    "Balanceador",
    "Tabla Periodica",
    "Quiz",
    "Historial",
])


# ============================================================
# PESTANA 1 - Balanceador principal
# ============================================================
with pestanas[0]:

    st.write(
        "Escribe una ecuacion usando '=' para separar "
        "reactivos y productos, y '+' entre compuestos."
    )

    # Campo donde el usuario escribe la ecuacion
    ecuacion = st.text_input(
        "Ejemplo: H2 + O2 = H2O",
        key="ecuacion_input"
    )

    # Boton principal para analizar la ecuacion
    if st.button("Analizar"):

        # Verificamos que el usuario haya escrito algo
        if ecuacion.strip() == "":

            st.warning("Escribe una ecuacion primero.")

        else:

            # Validamos la ecuacion antes de procesarla
            es_valida, errores = validar_ecuacion(ecuacion)

            if not es_valida:

                st.error("La ecuacion tiene errores.")

                # Mostramos todos los errores encontrados
                for error in errores:
                    st.write(f"- {error}")

            else:

                try:

                    # Verificamos si ya estaba balanceada
                    ya_balanceada, detalle = (
                        ecuacion_ya_balanceada(ecuacion)
                    )

                    if ya_balanceada:
                        st.success(
                            "Esta ecuacion ya esta balanceada."
                        )
                    else:
                        st.info(
                            "La ecuacion no esta balanceada."
                        )

                    # Separamos reactivos y productos
                    reactivos, productos = (
                        Separar_ecuacion(ecuacion)
                    )

                    # Calculamos los coeficientes
                    coeficientes, compuestos, _, _, _ = (
                        calcular_coeficientes(
                            reactivos,
                            productos
                        )
                    )

                    # Construimos la ecuacion balanceada
                    ecuacion_balanceada = ""

                    for i, comp in enumerate(compuestos):

                        coef = coeficientes[i]

                        if coef == 1:
                            ecuacion_balanceada += comp
                        else:
                            ecuacion_balanceada += f"{coef}{comp}"

                        # Agregamos simbolos de separacion
                        if i == len(reactivos) - 1:
                            ecuacion_balanceada += " = "
                        elif i < len(compuestos) - 1:
                            ecuacion_balanceada += " + "

                    # Resultado principal
                    st.subheader("Ecuacion balanceada")
                    st.success(ecuacion_balanceada)

                    # Clasificamos el tipo de reaccion
                    tipo = clasificar_reaccion(ecuacion)
                    st.subheader("Tipo de reaccion")

                    # Obtenemos la explicacion del tipo
                    info_tipo = obtener_explicacion(tipo)
                    st.info(
                        f"{info_tipo['nombre_completo']}"
                    )

                    # Explicacion expandible
                    with st.expander("Ver explicacion"):

                        st.markdown(
                            f"**Que es?**\n\n"
                            f"{info_tipo['descripcion']}"
                        )
                        st.markdown(
                            f"**Como identificarla?**\n\n"
                            f"{info_tipo['como_identificarla']}"
                        )
                        st.markdown(
                            f"**Ejemplo clasico:**\n\n"
                            f"`{info_tipo['ejemplo']}`"
                        )
                        st.markdown(
                            f"**Curiosidad:**\n\n"
                            f"{info_tipo['curiosidad']}"
                        )

                    # Mostramos masas molares
                    st.subheader("Masas molares")

                    for comp in compuestos:
                        masa = calculo_masa_molar(comp)
                        st.write(f"**{comp}:** {masa} g/mol")

                    # Conteo de atomos
                    st.subheader("Conteo de atomos")

                    datos = tabla_verificacion(
                        reactivos,
                        productos,
                        coeficientes,
                        compuestos
                    )

                    # Tabla antes del balanceo
                    st.markdown("**Antes del balanceo**")

                    filas_antes = []

                    for elem in datos["elementos"]:
                        filas_antes.append({
                            "Elemento": elem,
                            "Reactivos": datos["antes_reactivos"].get(elem, 0),
                            "Productos": datos["antes_productos"].get(elem, 0),
                            "Igual?":
                            "Si"
                            if datos["antes_reactivos"].get(elem, 0)
                            == datos["antes_productos"].get(elem, 0)
                            else "No"
                        })

                    st.table(
                        pd.DataFrame(filas_antes)
                        .set_index("Elemento")
                    )

                    # Tabla despues del balanceo
                    st.markdown("**Despues del balanceo**")

                    filas_despues = []

                    for elem in datos["elementos"]:
                        filas_despues.append({
                            "Elemento": elem,
                            "Reactivos": datos["despues_reactivos"].get(elem, 0),
                            "Productos": datos["despues_productos"].get(elem, 0),
                            "Igual?":
                            "Si"
                            if datos["despues_reactivos"].get(elem, 0)
                            == datos["despues_productos"].get(elem, 0)
                            else "No"
                        })

                    st.table(
                        pd.DataFrame(filas_despues)
                        .set_index("Elemento")
                    )

                    # Explicacion paso a paso
                    st.subheader("Explicacion del balanceo")

                    with st.expander("Ver pasos"):
                        for bloque in explicar_balanceo(ecuacion):
                            st.markdown(bloque)

                    # Guardamos el resultado en historial
                    guardar_en_historial(
                        ecuacion,
                        ecuacion_balanceada,
                        tipo
                    )

                except Exception as e:
                    st.error(f"Error al procesar la ecuacion: {e}")


# ============================================================
# PESTANA 2 - Tabla periodica
#
