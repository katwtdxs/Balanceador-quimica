import streamlit as st
import pandas as pd

# ── Módulos originales del proyecto ──
from traductor import Separar_ecuacion
from matrices import calcular_coeficientes
from Tipo_reaccion import clasificar_reaccion
from Calculo_molar import calculo_masa_molar
from historial import guardar_en_historial, exportar_txt
from explicacion_balanceo import explicar_balanceo
from verificar_atomos import tabla_verificacion
from verificacion import ecuacion_ya_balanceada

# ── Módulos nuevos ──
from validacion import validar_ecuacion                      # Valida la ecuación antes de balancear
from explicacion_reacciones import obtener_explicacion       # Explica cada tipo de reacción
from tabla_periodica import buscar_elemento, obtener_color_categoria  # Tabla periódica
from quiz import obtener_pregunta_aleatoria, verificar_respuesta      # Modo quiz


# ════════════════════════════════════════════════════════════
# Configuración general de la página
# ════════════════════════════════════════════════════════════
st.set_page_config(
    page_title="Balanceador Químico",
    page_icon="🧪",
    layout="wide"
)

st.title("🧪 Balanceador de Ecuaciones Químicas")

# Las secciones del programa se organizan en pestañas
# para que no todo esté apilado en una sola página
pestanas = st.tabs([
    "⚖️ Balanceador",
    "🔬 Tabla Periódica",
    "🎮 Quiz",
    "📜 Historial",
])


# ════════════════════════════════════════════════════════════
# PESTAÑA 1 — Balanceador principal
# ════════════════════════════════════════════════════════════
with pestanas[0]:

    st.write(
        "Escribe una ecuación usando `=` para separar reactivos y productos, "
        "y `+` entre compuestos."
    )
    ecuacion = st.text_input("Ejemplo: H2 + O2 = H2O", key="ecuacion_input")

    if st.button("🔍 Analizar"):

        if ecuacion.strip() == "":
            st.warning("Escribe una ecuación primero.")

        else:
            # ── PASO 0: Validar la ecuación antes de cualquier cálculo ──
            es_valida, errores = validar_ecuacion(ecuacion)

            if not es_valida:
                # Si hay errores de formato o símbolos inválidos, los mostramos
                # y no seguimos procesando para no generar errores confusos
                st.error("⚠️ La ecuación tiene errores. Corrígelos antes de continuar:")
                for error in errores:
                    st.write(f"- {error}")

            else:
                # La ecuación es válida, procedemos con el análisis
                try:
                    # ── Verificar si ya está balanceada ──
                    ya_balanceada, detalle = ecuacion_ya_balanceada(ecuacion)

                    if ya_balanceada:
                        st.success("✅ Esta ecuación ya está balanceada tal como fue ingresada.")
                    else:
                        st.info("⚖️ La ecuación no está balanceada. Calculando coeficientes...")

                    # 1. Separar reactivos y productos
                    reactivos, productos = Separar_ecuacion(ecuacion)

                    # 2. Calcular coeficientes con Gauss-Jordan
                    coeficientes, compuestos, _, _, _ = calcular_coeficientes(reactivos, productos)

                    # 3. Construir el string de la ecuación balanceada
                    ecuacion_balanceada = ""
                    for i, comp in enumerate(compuestos):
                        coef = coeficientes[i]
                        ecuacion_balanceada += comp if coef == 1 else f"{coef}{comp}"
                        if i == len(reactivos) - 1:
                            ecuacion_balanceada += " = "
                        elif i < len(compuestos) - 1:
                            ecuacion_balanceada += " + "

                    # ── Resultado principal ──
                    st.subheader("✅ Ecuación balanceada")
                    st.success(ecuacion_balanceada)

                    # ── Tipo de reacción ──
                    tipo = clasificar_reaccion(ecuacion)
                    st.subheader("⚗️ Tipo de reacción")

                    # Obtenemos la explicación del tipo de reacción
                    info_tipo = obtener_explicacion(tipo)

                    # Mostramos el tipo con su icono y nombre completo
                    st.info(f"{info_tipo['icono']} **{info_tipo['nombre_completo']}**")

                    # Expandible con la explicación completa
                    with st.expander("📖 ¿Qué es este tipo de reacción? Ver explicación"):
                        st.markdown(f"**¿Qué es?**\n\n{info_tipo['descripcion']}")
                        st.markdown(f"**¿Cómo identificarla?**\n\n{info_tipo['como_identificarla']}")
                        st.markdown(f"**Ejemplo clásico:**\n\n`{info_tipo['ejemplo']}`")
                        st.markdown(f"**💡 Curiosidad:**\n\n{info_tipo['curiosidad']}")

                    # ── Masas molares ──
                    st.subheader("⚖️ Masas molares")
                    for comp in compuestos:
                        masa = calculo_masa_molar(comp)
                        st.write(f"**{comp}:** {masa} g/mol")

                    # ── Conteo de átomos ──
                    st.subheader("🔢 Conteo de átomos")
                    st.write(
                        "La siguiente tabla muestra cuántos átomos hay de cada elemento "
                        "a ambos lados de la ecuación, antes y después del balanceo."
                    )

                    datos = tabla_verificacion(reactivos, productos, coeficientes, compuestos)

                    # Tabla ANTES del balanceo
                    st.markdown("**Antes del balanceo** *(todos los coeficientes = 1)*")
                    filas_antes = []
                    for elem in datos["elementos"]:
                        filas_antes.append({
                            "Elemento":  elem,
                            "Reactivos": datos["antes_reactivos"].get(elem, 0),
                            "Productos": datos["antes_productos"].get(elem, 0),
                            "¿Igual?":   "✅" if datos["antes_reactivos"].get(elem, 0) == datos["antes_productos"].get(elem, 0) else "❌"
                        })
                    st.table(pd.DataFrame(filas_antes).set_index("Elemento"))

                    # Tabla DESPUÉS del balanceo
                    st.markdown("**Después del balanceo** *(con los coeficientes calculados)*")
                    filas_despues = []
                    for elem in datos["elementos"]:
                        filas_despues.append({
                            "Elemento":  elem,
                            "Reactivos": datos["despues_reactivos"].get(elem, 0),
                            "Productos": datos["despues_productos"].get(elem, 0),
                            "¿Igual?":   "✅" if datos["despues_reactivos"].get(elem, 0) == datos["despues_productos"].get(elem, 0) else "❌"
                        })
                    st.table(pd.DataFrame(filas_despues).set_index("Elemento"))

                    # ── Explicación paso a paso ──
                    st.subheader("📖 ¿Cómo se balanceó esta ecuación?")
                    with st.expander("Ver explicación paso a paso del balanceo"):
                        for bloque in explicar_balanceo(ecuacion):
                            st.markdown(bloque)

                    # ── Guardar en historial ──
                    guardar_en_historial(ecuacion, ecuacion_balanceada, tipo)

                except Exception as e:
                    st.error(f"Error al procesar la ecuación: {e}")


# ════════════════════════════════════════════════════════════
# PESTAÑA 2 — Tabla periódica
# ════════════════════════════════════════════════════════════
with pestanas[1]:

    st.header("🔬 Consulta de Elementos")
    st.write(
        "Escribe el símbolo de un elemento (`Fe`, `O`, `Ca`) "
        "o su nombre en español o inglés (`hierro`, `iron`, `oxígeno`)."
    )

    # Campo de búsqueda
    busqueda = st.text_input("Buscar elemento:", placeholder="Ejemplo: Fe, Hierro, Carbon")

    if busqueda.strip():
        # Buscamos el elemento con nuestra función
        elemento = buscar_elemento(busqueda.strip())

        if elemento is None:
            # No se encontró ningún elemento con ese texto
            st.error(
                f"No se encontró ningún elemento con '{busqueda}'. "
                "Verifica que el símbolo o nombre estén bien escritos."
            )
        else:
            # Encontramos el elemento — lo mostramos en una tarjeta visual

            # Color según la categoría del elemento
            color = obtener_color_categoria(elemento["categoria"])

            # Mostramos la "tarjeta" del elemento usando columnas de Streamlit
            st.markdown("---")
            col_izq, col_der = st.columns([1, 2])

            with col_izq:
                # Cuadro grande con el símbolo (simulamos la tarjeta de tabla periódica)
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
                        <div style="font-size: 14px;">{elemento['numero']}</div>
                        <div style="font-size: 60px; font-weight: bold;">{elemento['simbolo']}</div>
                        <div style="font-size: 18px;">{elemento['nombre']}</div>
                        <div style="font-size: 14px;">{elemento['masa']} g/mol</div>
                    </div>
                    """,
                    unsafe_allow_html=True,
                )

            with col_der:
                # Tabla con la información detallada
                st.markdown(f"### {elemento['nombre']} ({elemento['simbolo']})")
                st.table(pd.DataFrame({
                    "Propiedad": ["Número atómico", "Masa atómica", "Grupo", "Período", "Categoría"],
                    "Valor":     [
                        elemento["numero"],
                        f"{elemento['masa']} g/mol",
                        elemento["grupo"],
                        elemento["periodo"],
                        elemento["categoria"],
                    ]
                }).set_index("Propiedad"))


# ════════════════════════════════════════════════════════════
# PESTAÑA 3 — Quiz interactivo
# ════════════════════════════════════════════════════════════
with pestanas[2]:

    st.header("🎮 Quiz de Balanceo")
    st.write(
        "Practica tus habilidades de balanceo. El sistema te da una ecuación "
        "sin balancear y tú intentas resolverla. Si no sabes, puedes pedir pistas."
    )

    # ── Inicializar el estado del quiz en la sesión ──
    # Streamlit borra las variables al recargar, así que guardamos
    # todo en st.session_state para que persista mientras se usa la app

    if "quiz_pregunta" not in st.session_state:
        st.session_state.quiz_pregunta = None    # La pregunta activa

    if "quiz_pista_idx" not in st.session_state:
        st.session_state.quiz_pista_idx = 0      # Índice de la pista actual

    if "quiz_puntos" not in st.session_state:
        st.session_state.quiz_puntos = 0         # Puntos acumulados

    if "quiz_intentos" not in st.session_state:
        st.session_state.quiz_intentos = 0       # Total de preguntas respondidas

    if "quiz_respondida" not in st.session_state:
        st.session_state.quiz_respondida = False # Si la pregunta actual ya se respondió

    # ── Selector de dificultad y botón para nueva pregunta ──
    col_dif, col_btn = st.columns([2, 1])

    with col_dif:
        dificultad = st.selectbox(
            "Dificultad:",
            ["Cualquiera", "Fácil", "Media", "Difícil"],
            key="quiz_dificultad"
        )

    with col_btn:
        st.write("")  # Espacio para alinear el botón con el selectbox
        if st.button("🎲 Nueva pregunta"):
            # Sacamos una pregunta nueva del banco
            nivel = None if dificultad == "Cualquiera" else dificultad
            st.session_state.quiz_pregunta    = obtener_pregunta_aleatoria(nivel)
            st.session_state.quiz_pista_idx   = 0
            st.session_state.quiz_respondida  = False

    # ── Mostrar puntuación ──
    if st.session_state.quiz_intentos > 0:
        porcentaje = int(st.session_state.quiz_puntos / st.session_state.quiz_intentos * 100)
        st.metric(
            label="Puntuación",
            value=f"{st.session_state.quiz_puntos} / {st.session_state.quiz_intentos}",
            delta=f"{porcentaje}% de aciertos"
        )

    st.markdown("---")

    # ── Mostrar la pregunta activa ──
    if st.session_state.quiz_pregunta is None:
        # Todavía no se ha pedido ninguna pregunta
        st.info("Presiona **'Nueva pregunta'** para empezar el quiz.")

    else:
        pregunta = st.session_state.quiz_pregunta

        # Mostramos la ecuación sin balancear con su nivel de dificultad
        st.markdown(
            f"**Nivel:** {pregunta['dificultad']}  |  "
            f"**Balancea esta ecuación:**"
        )
        st.code(pregunta["sin_balancear"])

        if st.session_state.quiz_respondida:
            # Si ya se respondió correctamente, solo mostramos el mensaje de éxito
            # y el botón para continuar con otra pregunta
            st.success("✅ ¡Correcto! Presiona 'Nueva pregunta' para continuar.")

        else:
            # ── Campo de respuesta ──
            respuesta = st.text_input(
                "Tu respuesta (usa el mismo formato: reactivos = productos):",
                placeholder="Ejemplo: 2H2 + O2 = 2H2O",
                key="quiz_respuesta_input"
            )

            col_verificar, col_pista = st.columns([1, 1])

            with col_verificar:
                if st.button("✅ Verificar"):
                    if not respuesta.strip():
                        st.warning("Escribe tu respuesta antes de verificar.")
                    else:
                        # Verificamos la respuesta del usuario
                        es_correcta, mensaje = verificar_respuesta(
                            pregunta["sin_balancear"],
                            respuesta
                        )

                        st.session_state.quiz_intentos += 1

                        if es_correcta:
                            st.success(mensaje)
                            st.session_state.quiz_puntos   += 1
                            st.session_state.quiz_respondida = True
                        else:
                            st.error(f"❌ {mensaje}")
                            st.write(
                                f"*Intentos realizados: {st.session_state.quiz_intentos}. "
                                f"Puedes pedir una pista si la necesitas.*"
                            )

            with col_pista:
                # Botón para mostrar la siguiente pista
                if st.button("💡 Pedir pista"):
                    idx = st.session_state.quiz_pista_idx
                    pistas = pregunta["pistas"]

                    if idx < len(pistas):
                        st.info(f"**Pista {idx + 1}:** {pistas[idx]}")
                        st.session_state.quiz_pista_idx += 1
                    else:
                        # Ya se mostraron todas las pistas (la última es la respuesta)
                        st.warning("Ya no hay más pistas disponibles para esta pregunta.")

            # ── Mostrar las pistas ya usadas (para no perderlas al recargar) ──
            pistas_usadas = st.session_state.quiz_pista_idx
            if pistas_usadas > 0:
                st.markdown("**Pistas mostradas:**")
                for i in range(pistas_usadas):
                    st.write(f"- Pista {i+1}: {pregunta['pistas'][i]}")


# ════════════════════════════════════════════════════════════
# PESTAÑA 4 — Historial
# ════════════════════════════════════════════════════════════
with pestanas[3]:

    st.header("📜 Historial de ecuaciones")

    try:
        with open("historial.txt", "r") as archivo:
            contenido = archivo.read()
            if contenido.strip() == "":
                st.write("No hay historial todavía.")
            else:
                st.text(contenido)
    except FileNotFoundError:
        st.write("No hay historial todavía.")

    if st.button("📥 Exportar historial"):
        exportar_txt()
        st.success("Historial exportado como 'resultados.txt'.")
