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

client = genai.Client(
    api_key=st.secrets["GEMINI_API_KEY"]
)


# ==========================================
# ESTILOS
# ==========================================

st.markdown("""
<style>

    .stApp {
        background-color: #ffffff;
    }

    [data-testid="stSidebarNav"] {
        display: none;
    }

    section[data-testid="stSidebar"] {
        background-color: #f7f8fa;
    }

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

</style>
""", unsafe_allow_html=True)


# ==========================================
# PREPARAR LOS REPORTES PARA GEMINI
# ==========================================

reportes_texto = ""

for reporte in ALL_FEEDBACK:

    reportes_texto += f"""
REPORTE #{reporte['id']}
Tipo: {reporte['tipo']}
País: {reporte['pais']}
Urgencia: {reporte['urgencia']}
Estado: {reporte['estado']}
Comentario: {reporte['comentario']}
"""

    if "calificacion" in reporte:
        reportes_texto += (
            f"Calificación: {reporte['calificacion']}/5\n"
        )

    reportes_texto += "\n"


# ==========================================
# FUNCIÓN DE ANÁLISIS CON IA
# ==========================================

def preguntar_a_ia(pregunta):

    prompt = f"""
Eres Alegra Insight, una herramienta interna de análisis de feedback
para el equipo de producto de Alegra.

Tu función es ayudar a Sofía, Product Manager, a entender los problemas,
necesidades y patrones encontrados en los comentarios de usuarios.

IMPORTANTE:

- Basa tus respuestas únicamente en los reportes proporcionados.
- No inventes datos.
- No inventes usuarios, problemas o estadísticas que no aparezcan
  en los reportes.
- Puedes encontrar patrones y hacer inferencias razonables a partir
  de los datos.
- Si la información no está disponible en los reportes, dilo claramente.
- Cuando sea útil, menciona cuántos reportes respaldan una conclusión.
- Responde en español.
- Sé clara, directa y útil para tomar decisiones de producto.
- No necesitas mencionar que eres una IA.
- No repitas todos los comentarios completos a menos que sea necesario.

Estos son TODOS los reportes disponibles actualmente:

{reportes_texto}


PREGUNTA DE SOFÍA:

{pregunta}


Responde la pregunta utilizando únicamente la información anterior.
"""

    response = client.models.generate_content(
        model="gemini-3.8-flash",
        contents=prompt
    )

    return response.text


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
# BUSCADOR + BOTÓN
# ==========================================

col_search, col_button = st.columns([5, 1])

with col_search:

    question = st.text_input(
        "",
        placeholder="Pregunta a la IA sobre algún reporte...",
        label_visibility="collapsed"
    )


with col_button:

    buscar = st.button(
        "Buscar →",
        use_container_width=True
    )


# ==========================================
# RESPUESTA DE LA IA
# ==========================================

if buscar:

    if not question.strip():

        st.warning(
            "Escribe una pregunta para poder analizar los reportes."
        )

    else:

        with st.spinner("Analizando los reportes..."):

            try:

                respuesta = preguntar_a_ia(question)

                st.markdown(
                    """
                    <div style="
                        margin-top: 25px;
                        padding: 24px;
                        border: 1px solid #e5e7eb;
                        border-radius: 16px;
                        background-color: #ffffff;
                    ">
                        <h3 style="
                            color: #17213a;
                            margin-bottom: 15px;
                        ">
                            Alegra Insight
                        </h3>
                    </div>
                    """,
                    unsafe_allow_html=True
                )

                st.markdown(respuesta)

            except Exception as e:

                st.error(
                    "No pude completar el análisis en este momento."
                )

                st.caption(
                    f"Detalle técnico: {e}"
                )


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

    if st.button(
        "Ingresar un nuevo reporte",
        key="nuevo_reporte",
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

    if st.button(
        "Subir sesión con cliente",
        key="subir_sesion",
        use_container_width=True
    ):
        st.switch_page("pages/3_Sesiones.py")


# ==========================================
# INGRESAR REPORTE
# ==========================================

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


# ==========================================
# SUBIR SESIÓN
# ==========================================

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
