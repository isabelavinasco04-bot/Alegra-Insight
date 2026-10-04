import streamlit as st
from google import genai
from data import ALL_FEEDBACK


# ==========================================
# CONFIGURACIÓN
# ==========================================

st.set_page_config(
    page_title="Alegra AI",
    page_icon="🌿",
    layout="wide"
)


# ==========================================
# CONEXIÓN CON GEMINI
# ==========================================

client = genai.Client(
    api_key=st.secrets["GEMINI_API_KEY"]
)

GEMINI_MODEL = "gemini-3.8-flash"


# ==========================================
# ESTILOS
# ==========================================

st.markdown("""
<style>

.main {
    background-color: #ffffff;
}

.block-container {
    padding-top: 2rem;
    padding-left: 3rem;
    padding-right: 3rem;
}

h1 {
    color: #172554;
}

</style>
""", unsafe_allow_html=True)


# ==========================================
# SIDEBAR
# ==========================================

with st.sidebar:

    st.markdown("## 🌿 alegra")

    st.markdown("---")

    st.markdown("⌂  Inicio")
    st.markdown("▣  Buzón")
    st.markdown("♙  Subir sesión")
    st.markdown("♧  Equipos")

    st.markdown("---")

    st.caption("Sofía")
    st.caption("Product Manager")


# ==========================================
# HEADER
# ==========================================

st.title("Buzón de usuarios")

st.caption(
    "Todos los comentarios y tickets, organizados y analizados con IA."
)


# ==========================================
# MÉTRICAS
# ==========================================

col1, col2, col3, col4 = st.columns(4)

with col1:
    st.metric(
        "Total",
        len(ALL_FEEDBACK)
    )

with col2:
    st.metric(
        "Reseñas",
        len([
            x for x in ALL_FEEDBACK
            if x["tipo"] == "Reseña"
        ])
    )

with col3:
    st.metric(
        "Tickets",
        len([
            x for x in ALL_FEEDBACK
            if x["tipo"] == "Ticket"
        ])
    )

with col4:
    st.metric(
        "Sin analizar",
        len([
            x for x in ALL_FEEDBACK
            if x["estado"] == "Sin analizar"
        ])
    )


st.markdown("---")
# ==========================================
# FILTROS
# ==========================================

col1, col2, col3, col4 = st.columns([2, 1, 1, 1])

with col1:

    search = st.text_input(
        "🔎 Buscar",
        placeholder="Buscar comentario..."
    )

with col2:

    countries = sorted(
        list(set(
            x["pais"]
            for x in ALL_FEEDBACK
        ))
    )

    country_filter = st.selectbox(
        "País",
        ["Todos"] + countries
    )

with col3:

    urgency_filter = st.selectbox(
        "Urgencia",
        ["Todas", "Alta", "Media", "Baja"]
    )

with col4:

    status_filter = st.selectbox(
        "Estado",
        ["Todos", "Sin analizar", "Analizado"]
    )

# ==========================================
# PESTAÑAS
# ==========================================

tab1, tab2, tab3 = st.tabs([
    "Todos",
    "Reseñas",
    "Tickets"
])


if "tab_selection" not in st.session_state:
    st.session_state.tab_selection = "Todos"



# ==========================================
# FUNCIÓN PARA MOSTRAR CASOS
# ==========================================

def show_feedback(items, view_key):

    filtered_data = items

    # Buscar
    if search:

        filtered_data = [
            x for x in filtered_data
            if search.lower() in x["comentario"].lower()
        ]

    # País
    if country_filter != "Todos":

        filtered_data = [
            x for x in filtered_data
            if x["pais"] == country_filter
        ]

    # Urgencia
    if urgency_filter != "Todas":

        filtered_data = [
            x for x in filtered_data
            if x["urgencia"] == urgency_filter
        ]

    # Estado
    if status_filter != "Todos":

        filtered_data = [
            x for x in filtered_data
            if x["estado"] == status_filter
        ]

    st.markdown(
        f"### {len(filtered_data)} resultados"
    )

    # ======================================
    # CASOS
    # ======================================

    for item in filtered_data:

        with st.container(border=True):

            col1, col2, col3, col4, col5 = st.columns(
                [0.5, 4, 1.2, 1.2, 1.3]
            )

            # Tipo
            with col1:

                if item["tipo"] == "Ticket":
                    st.write("🎫")
                else:
                    st.write("💬")

            # Comentario
            with col2:

                st.write(
                    f"**{item['comentario']}**"
                )

                st.caption(
                    f"{item['tipo']} · ID #{item['id']}"
                )

            # País
            with col3:

                st.write(item["pais"])

            # Urgencia
            with col4:

                if item["urgencia"] == "Alta":

                    st.error("🔴 Alta")

                elif item["urgencia"] == "Media":

                    st.warning("🟡 Media")

                else:

                    st.success("🟢 Baja")

            # Estado / botón
            with col5:

                if item["estado"] == "Sin analizar":

                    st.caption("Sin analizar")

                else:

                    st.success("Analizado")

            # ==================================
            # BOTÓN IA
            # ==================================

            if st.button(
            "Analizar con IA",
            key=f"analizar_{view_key}_{item['id']}"
            ):

                with st.spinner(
                    "Analizando comentario..."
                ):

                    try:

                        response = client.models.generate_content(
                            model=GEMINI_MODEL,
                            contents=f"""
Eres un Product Manager de Alegra.

Analiza el siguiente comentario de usuario.

COMENTARIO:
{item['comentario']}

CONTEXTO:
- Tipo: {item['tipo']}
- País: {item['pais']}
- Calificación: {item.get('calificacion', 'No aplica')}

Necesito que identifiques:

1. Problema identificado
2. Severidad
3. Impacto
4. Área afectada
5. Hipótesis
6. Información faltante

No inventes información.

Diferencia claramente los hechos
de las hipótesis.

Si algo no está disponible,
indica "Por confirmar".
"""
                        )

                        if response and response.text:

                            st.success(
                                "Análisis completado"
                            )

                            st.markdown(
                                "### 🧠 Análisis de IA"
                            )

                            st.write(
                                response.text
                            )

                        else:

                            st.warning(
                                "Gemini no devolvió contenido. "
                                "Intenta nuevamente."
                            )

                    except Exception as e:

                        st.error(
                            "No pudimos analizar este comentario "
                            "en este momento."
                        )

                        st.caption(
                            "Intenta nuevamente en unos segundos."
                        )

                        st.code(str(e))


# ==========================================
# CONTENIDO DE LAS PESTAÑASs
# ==========================================

with tab1:

    show_feedback(
        ALL_FEEDBACK,
        "todos"
    )


with tab2:

    reviews = [
        x for x in ALL_FEEDBACK
        if x["tipo"] == "Reseña"
    ]

    show_feedback(
        reviews,
        "resenas"
    )


with tab3:

    tickets = [
        x for x in ALL_FEEDBACK
        if x["tipo"] == "Ticket"
    ]

    show_feedback(
        tickets,
        "tickets"
    )
