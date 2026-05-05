import streamlit as st

# Importar módulos
from traductor import Separar_ecuacion
from matrices import calcular_coeficientes
from Tipo_reaccion import clasificar_reaccion
from Calculo_molar import calculo_masa_molar
from historial import guardar_en_historial, exportar_txt


# CONFIGURACIÓN
st.set_page_config(page_title="Balanceador Químico", page_icon="🧪")

st.title("Balanceador de Ecuaciones Químicas")
st.write("Ingresa una ecuación química")

ecuacion = st.text_input("Ejemplo: H2 + O2 = H2O")


# BOTÓN PRINCIPAL
if st.button(" Analizar"):

    if ecuacion.strip() == "":
        st.warning("Escribe una ecuación primero")
    else:
        try:
            # 1. Separar
            reactivos, productos = Separar_ecuacion(ecuacion)

            # 2. Balancear
            coeficientes, compuestos, _, _, _ = calcular_coeficientes(reactivos, productos)

            # 3. Construir ecuación balanceada
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

            st.subheader("Ecuación balanceada")
            st.success(ecuacion_balanceada)

            # 4. Tipo de reacción
            tipo = clasificar_reaccion(ecuacion)

            st.subheader("Tipo de reacción")
            st.info(tipo)

            # 5. Masas molares
            st.subheader(" Masas molares")

            masas = {}
            for comp in compuestos:
                masa = calculo_masa_molar(comp)
                masas[comp] = masa
                st.write(f"{comp}: {masa} g/mol")

            # 6. Guardar historial
            guardar_en_historial(
                ecuacion,
                ecuacion_balanceada,
                tipo
            )

        except Exception as e:
            st.error(f"Error: {e}")


# HISTORIAL
st.markdown("---")
st.header(" Historial")

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
if st.button(" Exportar historial"):
    exportar_txt()