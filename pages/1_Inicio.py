import streamlit as st
from google import genai

from data import ALL_FEEDBACK


# ==========================================
# CONFIGURACIÓN
# ==========================================

st.set_page_config(
    page_title="Alegra Insight",
    page_icon="Logo_pequeño_alegra.webp",
    layout="wide"
)


# ==========================================
# CLIENTE GEMINI
# ==========================================

try:
    client = genai.Client(
        api_key=st.secrets["GEMINI_API_KEY"]
    )
except Exception:
    client = None


# ==========================================
# ESTILOS
# ==========================================

st.markdown("""
<style>

    /* Fondo general */
    .stApp {
        background-color: #ffffff;
    }

    /* Ocultar navegación automática */
    [data-testid="stSidebarNav"] {
        display: none;
    }

    /* Sidebar */
    section[data-testid="stSidebar"] {
        background-color: #f7f8fa;
    }

    /* Hero */
    .hero {
        text-align: center;
        padding-top: 60px;
        padding-bottom: 25px;
    }

    .hero h1 {
        font-size: 42px;
        color: #17213a;
        margin-bottom: 8px;
    }

    .hero p {
        font-size: 20px;
        color: #687080;
    }

    /* Tarjetas */
    .card {
        background: white;
        border: 1px solid #e5e7eb;
        border-radius: 16px;
        padding: 24px;
        min-height: 150px;
        box-shadow: 0 2px 8px rgba(0,0,0,0.03);
    }

    .card h3 {
        color: #17213a;
        margin-bottom: 8px;
    }

    .card p {
        color: #687080;
        line-height: 1.5;
    }

    /* Respuesta IA */
    .ai-response {
        background: #f7f8fa;
        border: 1px solid #e5e7eb;
        border-radius: 16px;
        padding: 24px;
        margin-top: 18px;
        margin-bottom: 20px;
    }

    .ai-title {
        color: #17213a;
        font-size: 18px;
        font-weight: 700;
        margin-bottom: 12px;
    }

</style>
""", unsafe_allow_html=True)


# ==========================================
# PREPARAR DATOS PARA LA IA
# ==========================================

def construir_contexto():
    """
    Convierte los reportes de data.py en un contexto
    que Gemini pueda consultar.
    """

    contexto = []

    for item in ALL_FEEDBACK:

        reporte = f"""
REPORTE #{item['id']}
Tipo: {item['tipo']}
País: {item['pais']}
Urgencia: {item['urgencia']}
Estado: {item['estado']}
"""

        if "calificacion" in item:
            reporte += f"Calificación: {item['calificacion']}/5\n"

        reporte += f"Comentario: {item['comentario']}\n"

        contexto.append(reporte)

    return "\n".join(contexto)


REPORTES = construir_contexto()


# ==========================================
# FUNCIÓN IA
# ==========================================

def preguntar_a_gemini(pregunta):

    if client is None:
        return (
            "No pude conectar con Gemini. "
            "Revisa que la variable GEMINI_API_KEY "
            "esté configurada correctamente en Secrets."
        )

    prompt = f"""
Eres Alegra Insight, un asistente interno para una Product Manager
de Alegra.

Tu función es analizar los reportes de usuarios disponibles y ayudar
a identificar problemas, patrones, prioridades y oportunidades
de producto.

IMPORTANTE:
- Usa únicamente la información de los reportes proporcionados.
- No inventes datos.
- No inventes números.
- No inventes usuarios, países o problemas que no aparezcan.
- Si la información no es suficiente para responder, dilo claramente.
- Puedes agrupar problemas cuando varios reportes describan el mismo
  problema o uno muy similar.
- Diferencia entre hechos encontrados en los reportes e inferencias.
- Sé concreto y útil para una Product Manager.
- Cuando sea relevante, menciona los IDs de los reportes que sustentan
  tu respuesta.
- Responde en español.
- No necesitas mencionar que eres una IA.

Estos son TODOS los reportes disponibles:

{REPORTES}


PREGUNTA DE LA PRODUCT MANAGER:

{pregunta}


Responde de forma clara y estructurada.
"""

    try:

        response = client.models.generate_content(
            model="gemini-2.5-flash",
            contents=prompt
        )

        return response.text

    except Exception as e:

        return (
            "No pude completar el análisis en este momento.\n\n"
            f"Detalle técnico: {str(e)}"
        )


# ==========================================
# HOME
# ==========================================

st.markdown(
    """
    <div class="hero">
        <h1>Hola Sofía 👋</h1>
        <p>¿Cómo quieres trabajar hoy?</p>
    </div>
    """,
    unsafe_allow_html=True
)


# ==========================================
# PREGUNTA A LA IA
# ==========================================

question = st.text_input(
    "",
    placeholder="Pregunta a la IA sobre algún reporte...",
    label_visibility="collapsed"
)


if question:

    with st.spinner("Analizando los reportes..."):

        respuesta = preguntar_a_gemini(question)

    st.markdown(
        """
        <div class="ai-response">
            <div class="ai-title">Alegra Insight</div>
        """,
        unsafe_allow_html=True
    )

    st.markdown(respuesta)

    st.markdown(
        "</div>",
        unsafe_allow_html=True
    )


# ==========================================
# PREGUNTAS RÁPIDAS
# ==========================================

col1, col2, col3 = st.columns(3)


with col1:

    if st.button(
        "💬 ¿Qué problemas se están reportando?",
        use_container_width=True
    ):

        with st.spinner("Analizando los reportes..."):

            respuesta = preguntar_a_gemini(
                """
                ¿Cuáles son los principales problemas que aparecen
                en los reportes?

                Agrúpalos por problema o tema, indica cuáles parecen
                más importantes y menciona los IDs de los reportes
                que sustentan cada grupo.
                """
            )

        st.markdown(
            """
            <div class="ai-response">
                <div class="ai-title">Problemas detectados</div>
            """,
            unsafe_allow_html=True
        )

        st.markdown(respuesta)

        st.markdown(
            "</div>",
            unsafe_allow_html=True
        )


with col2:

    if st.button(
        "📄 Muéstrame los reportes de facturación",
        use_container_width=True
    ):

        with st.spinner("Buscando reportes de facturación..."):

            respuesta = preguntar_a_gemini(
                """
                Identifica los reportes relacionados con facturación.

                Para cada uno indica:
                - ID
                - país
                - tipo de reporte
                - problema
                - urgencia

                Al final, explica qué patrón común encuentras.
                """
            )

        st.markdown(
            """
            <div class="ai-response">
                <div class="ai-title">Reportes de facturación</div>
            """,
            unsafe_allow_html=True
        )

        st.markdown(respuesta)

        st.markdown(
            "</div>",
            unsafe_allow_html=True
        )


with col3:

    if st.button(
        "👥 ¿Qué está trabajando el equipo?",
        use_container_width=True
    ):

        st.switch_page("pages/4_Equipos.py")


# ==========================================
# ACCIONES PRINCIPALES
# ==========================================

st.markdown("<br>", unsafe_allow_html=True)

col1, col2 = st.columns(2)


with col1:

    st.markdown(
        """
        <div class="card">
            <h3>＋ Ingresar un nuevo reporte</h3>
            <p>
                Pega un comentario, ticket o describe
                el problema manualmente.
            </p>
        </div>
        """,
        unsafe_allow_html=True
    )

    st.markdown("<br>", unsafe_allow_html=True)

    if st.button(
        "Ingresar reporte →",
        use_container_width=True
    ):

        st.switch_page("pages/2_Buzon.py")


with col2:

    st.markdown(
        """
        <div class="card">
            <h3>🎙 Subir sesión con cliente</h3>
            <p>
                Carga un audio o transcripción para
                que la IA lo analice.
            </p>
        </div>
        """,
        unsafe_allow_html=True
    )

    st.markdown("<br>", unsafe_allow_html=True)

    if st.button(
        "Subir sesión →",
        use_container_width=True
    ):

        st.switch_page("pages/3_Sesiones.py")
