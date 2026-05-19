# Programa principal realizado por el equipo del proyecto

"""
Este archivo es el núcleo principal de la aplicación.

Aquí conectamos todos los módulos del proyecto
para construir la interfaz interactiva en Streamlit.

El sistema permite:

- Balancear ecuaciones químicas
- Verificar átomos antes y después del balanceo
- Identificar el tipo de reacción
- Calcular masas molares
- Consultar elementos de la tabla periódica
- Practicar con un quiz interactivo
- Guardar y exportar historial de resultados

Cada funcionalidad está organizada en pestañas
para que la aplicación sea más clara y fácil de usar.
"""

import streamlit as st
import pandas as pd

# Importamos los módulos principales del proyecto
from traductor import Separar_ecuacion
from matrices import calcular_coeficientes
from Tipo_reaccion import clasificar_reaccion
from Calculo_molar import calculo_masa_molar
from historial import guardar_en_historial, exportar_como_txt, exportar_como_pdf
from explicacion_balanceo import explicar_balanceo
from verificar_atomos import tabla_verificacion
from verificacion import ecuacion_ya_balanceada

# Importamos módulos adicionales
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


# Configuración general de la página
st.set_page_config(

    page_title="Balanceador Químico",

    page_icon="🧪",

    layout="wide"
)

# Título principal de la aplicación
st.title("🧪 Balanceador de Ecuaciones Químicas")


# Creamos las pestañas principales del sistema
pestanas = st.tabs([

    " Balanceador",

    " Tabla Periódica",

    " Quiz",

    " Historial",
])


# ============================================================
# PESTAÑA 1 — Balanceador principal
# ============================================================
with pestanas[0]:

    st.write(
        "Escribe una ecuación usando '=' para separar "
        "reactivos y productos, y '+' entre compuestos."
    )

    # Campo donde el usuario escribe la ecuación
    ecuacion = st.text_input(
        "Ejemplo: H2 + O2 = H2O",
        key="ecuacion_input"
    )

    # Botón principal para analizar la ecuación
    if st.button(" Analizar"):

        # Verificamos que el usuario haya escrito algo
        if ecuacion.strip() == "":

            st.warning(
                "Escribe una ecuación primero."
            )

        else:

            # Validamos la ecuación antes de procesarla
            es_valida, errores = validar_ecuacion(ecuacion)

            if not es_valida:

                st.error(
                    " La ecuación tiene errores."
                )

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
                            " Esta ecuación ya está balanceada."
                        )

                    else:

                        st.info(
                            " La ecuación no está balanceada."
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

                    # Construimos la ecuación balanceada
                    ecuacion_balanceada = ""

                    for i, comp in enumerate(compuestos):

                        coef = coeficientes[i]

                        if coef == 1:

                            ecuacion_balanceada += comp

                        else:

                            ecuacion_balanceada += (
                                f"{coef}{comp}"
                            )

                        # Agregamos símbolos de separación
                        if i == len(reactivos) - 1:

                            ecuacion_balanceada += " = "

                        elif i < len(compuestos) - 1:

                            ecuacion_balanceada += " + "

                    # Resultado principal
                    st.subheader(
                        " Ecuación balanceada"
                    )

                    st.success(ecuacion_balanceada)

                    # Clasificamos el tipo de reacción
                    tipo = clasificar_reaccion(ecuacion)

                    st.subheader(
                        " Tipo de reacción"
                    )

                    # Obtenemos la explicación del tipo
                    info_tipo = obtener_explicacion(tipo)

                    st.info(
                        f"{info_tipo['icono']} "
                        f"**{info_tipo['nombre_completo']}**"
                    )

                    # Explicación expandible
                    with st.expander(
                        " Ver explicación"
                    ):

                        st.markdown(
                            f"**¿Qué es?**\n\n"
                            f"{info_tipo['descripcion']}"
                        )

                        st.markdown(
                            f"**¿Cómo identificarla?**\n\n"
                            f"{info_tipo['como_identificarla']}"
                        )

                        st.markdown(
                            f"**Ejemplo clásico:**\n\n"
                            f"`{info_tipo['ejemplo']}`"
                        )

                        st.markdown(
                            f"** Curiosidad:**\n\n"
                            f"{info_tipo['curiosidad']}"
                        )

                    # Mostramos masas molares
                    st.subheader(" Masas molares")

                    for comp in compuestos:

                        masa = calculo_masa_molar(comp)

                        st.write(
                            f"**{comp}:** {masa} g/mol"
                        )

                    # Conteo de átomos
                    st.subheader(" Conteo de átomos")

                    datos = tabla_verificacion(
                        reactivos,
                        productos,
                        coeficientes,
                        compuestos
                    )

                    # Tabla antes del balanceo
                    st.markdown(
                        "**Antes del balanceo**"
                    )

                    filas_antes = []

                    for elem in datos["elementos"]:

                        filas_antes.append({

                            "Elemento": elem,

                            "Reactivos":
                            datos["antes_reactivos"].get(elem, 0),

                            "Productos":
                            datos["antes_productos"].get(elem, 0),

                            "¿Igual?":
                            "✅"
                            if datos["antes_reactivos"].get(elem, 0)
                            ==
                            datos["antes_productos"].get(elem, 0)
                            else "❌"
                        })

                    st.table(
                        pd.DataFrame(filas_antes)
                        .set_index("Elemento")
                    )

                    # Tabla después del balanceo
                    st.markdown(
                        "**Después del balanceo**"
                    )

                    filas_despues = []

                    for elem in datos["elementos"]:

                        filas_despues.append({

                            "Elemento": elem,

                            "Reactivos":
                            datos["despues_reactivos"].get(elem, 0),

                            "Productos":
                            datos["despues_productos"].get(elem, 0),

                            "¿Igual?":
                            "✅"
                            if datos["despues_reactivos"].get(elem, 0)
                            ==
                            datos["despues_productos"].get(elem, 0)
                            else "❌"
                        })

                    st.table(
                        pd.DataFrame(filas_despues)
                        .set_index("Elemento")
                    )

                    # Explicación paso a paso
                    st.subheader(
                        "📖 Explicación del balanceo"
                    )

                    with st.expander(
                        "Ver pasos"
                    ):

                        for bloque in explicar_balanceo(ecuacion):

                            st.markdown(bloque)

                    # Guardamos el resultado en historial
                    guardar_en_historial(
                        ecuacion,
                        ecuacion_balanceada,
                        tipo
                    )

                except Exception as e:

                    st.error(
                        f"Error al procesar la ecuación: {e}"
                    )



# PESTAÑA 2 — Tabla periódica

with pestanas[1]:

    st.header(" Consulta de Elementos")

    st.write(
        "Busca un elemento usando su símbolo "
        "o nombre."
    )

    # Campo de búsqueda
    busqueda = st.text_input(
        "Buscar elemento:",
        placeholder="Ejemplo: Fe, Hierro, Carbon"
    )

    if busqueda.strip():

        # Buscamos el elemento
        elemento = buscar_elemento(busqueda.strip())

        if elemento is None:

            st.error(
                f"No se encontró ningún elemento "
                f"con '{busqueda}'."
            )

        else:

            # Obtenemos el color de la categoría
            color = obtener_color_categoria(
                elemento["categoria"]
            )

            st.markdown("---")

            col_izq, col_der = st.columns([1, 2])

            with col_izq:

                # Tarjeta visual del elemento
                st.markdown(
                    f"""
                    <div style="
                        background-color: {color};
                        color: white;
                        border-radius: 12px;
                        padding: 20px;
                        text-align: center;
                        font-family: monospace;
                    ">
                        <div style="font-size: 14px;">
                            {elemento['numero']}
                        </div>

                        <div style="
                            font-size: 60px;
                            font-weight: bold;
                        ">
                            {elemento['simbolo']}
                        </div>

                        <div style="font-size: 18px;">
                            {elemento['nombre']}
                        </div>

                        <div style="font-size: 14px;">
                            {elemento['masa']} g/mol
                        </div>
                    </div>
                    """,

                    unsafe_allow_html=True,
                )

            with col_der:

                # Tabla de información del elemento
                st.markdown(
                    f"### {elemento['nombre']} "
                    f"({elemento['simbolo']})"
                )

                st.table(
                    pd.DataFrame({

                        "Propiedad": [
                            "Número atómico",
                            "Masa atómica",
                            "Grupo",
                            "Período",
                            "Categoría"
                        ],

                        "Valor": [
                            elemento["numero"],
                            f"{elemento['masa']} g/mol",
                            elemento["grupo"],
                            elemento["periodo"],
                            elemento["categoria"],
                        ]

                    }).set_index("Propiedad")
                )



# PESTAÑA 3 — Quiz interactivo

with pestanas[2]:

    st.header("🎮 Quiz de Balanceo")

    st.write(
        "Practica balanceando ecuaciones químicas."
    )

    # Inicializamos variables de sesión
    if "quiz_pregunta" not in st.session_state:

        st.session_state.quiz_pregunta = None

    if "quiz_pista_idx" not in st.session_state:

        st.session_state.quiz_pista_idx = 0

    if "quiz_puntos" not in st.session_state:

        st.session_state.quiz_puntos = 0

    if "qui
