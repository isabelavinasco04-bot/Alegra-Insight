import streamlit as st
from google import genai
from data import ALL_FEEDBACK

# ==========================================
# CONFIGURACIÓN
# ==========================================

st.set_page_config(
    page_title="Alegra AI",
    page_icon="✦",
    layout="wide"
)

# ==========================================
# CONEXIÓN CON GEMINI
# ==========================================

client = genai.Client(
    api_key=st.secrets["GEMINI_API_KEY"]
)

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

.feedback-card {
    border: 1px solid #e5e7eb;
    border-radius: 12px;
    padding: 16px;
    margin-bottom: 10px;
    background: white;
}

.badge {
    padding: 4px 9px;
    border-radius: 20px;
    font-size: 12px;
    font-weight: 600;
}

</style>
""", unsafe_allow_html=True)


# ==========================================
# SIDEBAR
# ==========================================

with st.sidebar:

    st.markdown("## Alegra")

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

st.markdown("")


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
        len([x for x in ALL_FEEDBACK if x["tipo"] == "Reseña"])
    )

with col3:
    st.metric(
        "Tickets",
        len([x for x in ALL_FEEDBACK if x["tipo"] == "Ticket"])
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

tab1, tab2, tab3 = st.tabs([
    "Todos",
    "Reseñas",
    "Tickets"
])

with tab1:

    selected_data = ALL_FEEDBACK

with tab2:

    selected_data = [
        x for x in ALL_FEEDBACK
        if x["tipo"] == "Reseña"
    ]

with tab3:

    selected_data = [
        x for x in ALL_FEEDBACK
        if x["tipo"] == "Ticket"
    ]


col1, col2, col3, col4 = st.columns([2, 1, 1, 1])

with col1:

    search = st.text_input(
        "🔎 Buscar",
        placeholder="Buscar comentario..."
    )

with col2:

    countries = sorted(
        list(set(x["pais"] for x in ALL_FEEDBACK))
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
# APLICAR FILTROS
# ==========================================

filtered_data = selected_data

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

if status_filter != "Todos":

    filtered_data = [
        x for x in filtered_data
        if x["estado"] == status_filter
    ]


st.markdown("")


# ==========================================
# LISTADO
# ==========================================

st.subheader(
    f"{len(filtered_data)} resultados"
)

for item in filtered_data:

    with st.container(border=True):

        col1, col2, col3, col4, col5 = st.columns(
            [0.6, 4, 1.2, 1.4, 1]
        )

        with col1:

            if item["tipo"] == "Ticket":
                st.write("🎫")
            else:
                st.write("💬")

        with col2:

            st.write(
                f"**{item['comentario']}**"
            )

            st.caption(
                f"{item['tipo']} · ID #{item['id']}"
            )

        with col3:

            st.write(item["pais"])

        with col4:

            if item["urgencia"] == "Alta":
                st.error("🔴 Alta")

            elif item["urgencia"] == "Media":
                st.warning("🟡 Media")

            else:
                st.success("🟢 Baja")

        with col5:

            if item["estado"] == "Sin analizar":
                st.caption("Sin analizar")
            else:
                st.success("Analizado")

        # ----------------------------------
        # ANALIZAR
        # ----------------------------------

       # ----------------------------------
# ANALIZAR CON IA
# ----------------------------------

if st.button(
    "Analizar con IA",
    key=f"analizar_{item['id']}"
):

    with st.spinner("Analizando comentario..."):

        try:

            response = client.models.generate_content(
                model="gemini-3.8-flash",
                contents=f"""
Eres un Product Manager de Alegra.

Analiza este comentario de usuario:

{item['comentario']}

Contexto:
- Tipo: {item['tipo']}
- País: {item['pais']}
- Calificación: {item.get('calificacion', 'No aplica')}

Devuelve:

1. Problema identificado
2. Severidad
3. Impacto
4. Área afectada
5. Hipótesis
6. Información faltante

No inventes información.
Diferencia claramente los hechos de las hipótesis.
Si algo no está disponible, indica "Por confirmar".
"""
            )

            # Mostrar resultado solamente si Gemini respondió
            if response and response.text:

                st.success("Análisis completado")

                st.markdown("### Análisis de IA")

                st.write(response.text)

            else:

                st.warning(
                    "Gemini no devolvió contenido. Intenta nuevamente."
                )

        except Exception as e:

            st.error(
                "No pudimos analizar este comentario en este momento."
            )

            st.caption(
                "Intenta nuevamente en unos segundos."
            )

            # Información para depuración
            st.code(str(e))

        st.subheader("Análisis de IA")

        st.write(response.text)
