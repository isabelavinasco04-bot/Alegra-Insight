import streamlit as st

# ==========================================
# CONFIGURACIÓN
# ==========================================

st.set_page_config(
    page_title="Alegra Insight",
    page_icon="🌿",
    layout="wide"
)


# ==========================================
# ESTILOS
# ==========================================

st.markdown("""
<style>

    /* Fondo general */
    .stApp {
        background-color: #ffffff;
    }

    /* Ocultar menú automático de Streamlit */
    [data-testid="stSidebarNav"] {
        display: none;
    }

    /* Sidebar */
    section[data-testid="stSidebar"] {
        background-color: #f7f8fa;
    }

    /* Botones de navegación */
    .nav-title {
        font-size: 15px;
        color: #555b66;
        margin-top: 10px;
        margin-bottom: 8px;
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

</style>
""", unsafe_allow_html=True)


# ==========================================
# SIDEBAR
# ==========================================

with st.sidebar:

    st.markdown(
        """
        <div style="font-size:25px; font-weight:700;
        color:#17213a; margin-bottom:35px;">
        🌿 alegra
        </div>
        """,
        unsafe_allow_html=True
    )

    st.page_link(
        "app.py",
        label="⌂  Inicio"
    )

    st.page_link(
        "pages/2_Buzon.py",
        label="▣  Buzón"
    )

    st.page_link(
        "pages/3_Sesiones.py",
        label="♙  Subir sesión"
    )

    st.page_link(
        "pages/4_Equipos.py",
        label="♧  Equipos"
    )

    st.divider()

    st.markdown(
        """
        <div style="color:#687080; font-size:14px;">
        Sofía<br>
        <span style="color:#9aa0aa;">Product Manager</span>
        </div>
        """,
        unsafe_allow_html=True
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
    st.info(
        "La búsqueda con IA estará disponible próximamente."
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
        st.switch_page("pages/2_Buzon.py")


with col2:

    if st.button(
        "📄 Muéstrame los reportes de facturación",
        use_container_width=True
    ):
        st.switch_page("pages/2_Buzon.py")


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
