import streamlit as st
from google import genai
from data import ALL_FEEDBACK

analisis_page = st.Page(
    "pages/5_Analisis.py",
    title="Análisis"
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

/* ==========================================
   BOTONES ALEGRA
   ========================================== */

div.stButton > button {
    background-color: #2fb7b5;
    color: white;
    border: 1px solid #2fb7b5;
    border-radius: 8px;
    font-weight: 600;
    transition: all 0.2s ease;
}

div.stButton > button:hover {
    background-color: #17213a;
    border-color: #17213a;
    color: white;
}

div.stButton > button:active {
    background-color: #17213a;
    border-color: #17213a;
}

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

.feedback-card {
    border: 1px solid #e5e7eb;
    border-radius: 16px;
    padding: 22px;
    margin-bottom: 14px;
    background: white;
}

.feedback-card:hover {
    border-color: #2bb8b3;
    box-shadow: 0 4px 14px rgba(23,37,84,0.06);
}

</style>
""", unsafe_allow_html=True)


# ==========================================
# HEADER
# ==========================================

header_col1, header_col2 = st.columns([5, 1])

with header_col1:

    st.title("Buzón de usuarios")

    st.caption(
        "Todos los comentarios, tickets y feedback organizados para encontrar oportunidades."
    )

with header_col2:

    st.markdown("<br>", unsafe_allow_html=True)

    if st.button(
        "＋ Reporte manual",
        use_container_width=True,
        type="primary"
    ):
        st.session_state.show_add_report = True


# ==========================================
# AGREGAR REPORTE MANUALMENTE
# ==========================================

if "show_add_report" not in st.session_state:
    st.session_state.show_add_report = False


if st.session_state.show_add_report:

    with st.container(border=True):

        st.subheader("＋ Agregar nuevo reporte")

        comentario = st.text_area(
            "Comentario",
            placeholder="Pega aquí el comentario o describe el problema..."
        )

        col1, col2, col3 = st.columns(3)

        with col1:

            tipo = st.selectbox(
                "Tipo",
                ["Reseña", "Ticket", "Sesión con cliente"]
            )

        with col2:

            pais = st.selectbox(
                "País",
                [
                    "Colombia",
                    "México",
                    "República Dominicana",
                    "España"
                ]
            )

        with col3:

            urgencia = st.selectbox(
                "Urgencia",
                ["Alta", "Media", "Baja"]
            )

        col1, col2 = st.columns(2)

        with col1:

            if st.button(
                "Guardar reporte",
                type="primary",
                use_container_width=True
            ):

                if comentario.strip():

                    nuevo_id = max(
                        [x["id"] for x in ALL_FEEDBACK]
                    ) + 1

                    ALL_FEEDBACK.append({
                        "id": nuevo_id,
                        "tipo": tipo,
                        "pais": pais,
                        "urgencia": urgencia,
                        "estado": "Sin analizar",
                        "comentario": comentario
                    })

                    st.session_state.show_add_report = False

                    st.success("Reporte agregado correctamente.")

                    st.rerun()

                else:

                    st.warning(
                        "Escribe un comentario antes de guardar."
                    )

        with col2:

            if st.button(
                "Cancelar",
                use_container_width=True
            ):

                st.session_state.show_add_report = False

                st.rerun()


st.markdown("---")


# ==========================================
# MÉTRICAS
# ==========================================

col1, col2, col3, col4 = st.columns(4)

with col1:

    st.metric(
        "Feedback total",
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
        "Países",
        len(set(
            x["pais"]
            for x in ALL_FEEDBACK
        ))
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

    type_filter = st.selectbox(
        "Tipo",
        ["Todos", "Reseña", "Ticket", "Sesión con cliente"]
    )


# ==========================================
# FILTRAR DATOS
# ==========================================

filtered_data = ALL_FEEDBACK.copy()


if search:

    filtered_data = [
        x for x in filtered_data
        if search.lower() in x["comentario"].lower()
    ]


if country_filter != "Todos":

    filtered_data = [
        x for x in filtered_data
        if x["pais"] == country_filter
    ]


if urgency_filter != "Todas":

    filtered_data = [
        x for x in filtered_data
        if x["urgencia"] == urgency_filter
    ]


if type_filter != "Todos":

    filtered_data = [
        x for x in filtered_data
        if x["tipo"] == type_filter
    ]


# ==========================================
# RESULTADOS
# ==========================================

st.markdown(
    f"### {len(filtered_data)} resultados"
)


# ==========================================
# MOSTRAR FEEDBACK
# ==========================================

for item in filtered_data:

    with st.container(border=True):

        col1, col2, col3, col4 = st.columns(
            [0.5, 4.5, 1.2, 1.5]
        )

        # ------------------------------
        # ICONO
        # ------------------------------

        with col1:

            if item["tipo"] == "Ticket":
                st.write("🎫")
            else:
                st.write("💬")


        # ------------------------------
        # COMENTARIO
        # ------------------------------

        with col2:

            st.markdown(
                f"**{item['comentario']}**"
            )

            st.caption(
                f"{item['tipo']} · ID #{item['id']}"
            )


        # ------------------------------
        # PAÍS
        # ------------------------------

        with col3:

            st.write(item["pais"])

            if item["urgencia"] == "Alta":

                st.error("🔴 Alta")

            elif item["urgencia"] == "Media":

                st.warning("🟡 Media")

            else:

                st.success("🟢 Baja")


        # ------------------------------
        # BOTÓN IA
        # ------------------------------

        with col4:

            if st.button(
                "✨ Analizar con IA",
                key=f"analizar_{item['id']}",
                use_container_width=True
            ):

                st.session_state.selected_feedback = item

                st.switch_page(analisis_page)

