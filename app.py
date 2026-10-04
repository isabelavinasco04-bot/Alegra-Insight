import streamlit as st


# ==========================================
# CONFIGURACIÓN
# ==========================================

st.set_page_config(
    page_title="Alegra Insight",
    page_icon="Logo_pequeño_alegra.webp",
    layout="wide"
)

# ==========================================
# ESTILOS SIDEBAR
# ==========================================

st.markdown("""
<style>

    /* Sidebar */
    section[data-testid="stSidebar"] {
        background:
            radial-gradient(
                circle at 20% 10%,
                rgba(40, 191, 190, 0.35) 0%,
                rgba(40, 191, 190, 0.10) 28%,
                transparent 55%
            ),
            linear-gradient(
                180deg,
                #17213a 0%,
                #172b42 50%,
                #123d4b 100%
            );

        border-right: none;
    }

    /* ==========================================
   NAVEGACIÓN SIDEBAR
   ========================================== */

    /* Texto de los botones */
    section[data-testid="stSidebar"] a,
    section[data-testid="stSidebar"] a span,
    section[data-testid="stSidebar"] a p {
        color: #ffffff !important;
        border-radius: 10px;
        transition: all 0.2s ease;
    }

    /* Hover */
    section[data-testid="stSidebar"] a:hover,
    section[data-testid="stSidebar"] a:hover span,
    section[data-testid="stSidebar"] a:hover p {
        background-color: #2fb7b5 !important;
        color: #17213a !important;
    }
    
    /* Página activa */
    section[data-testid="stSidebar"] a[aria-current="page"],
    section[data-testid="stSidebar"] a[aria-current="page"] span,
    section[data-testid="stSidebar"] a[aria-current="page"] p {
        background-color: #2fb7b5 !important;
        color: #17213a !important;
        font-weight: 600;
    }
    
    </style>
    """, unsafe_allow_html=True)
# ==========================================
# PÁGINAS
# ==========================================

home_page = st.Page(
    "pages/1_Inicio.py",
    title="Inicio",
    default=True
)

buzon_page = st.Page(
    "pages/2_Buzon.py",
    title="Buzón"
)

sesiones_page = st.Page(
    "pages/3_Sesiones.py",
    title="Subir sesión"
)

equipos_page = st.Page(
    "pages/4_Equipos.py",
    title="Equipos"
)


# ==========================================
# NAVEGACIÓN
# ==========================================

pg = st.navigation(
    [
        home_page,
        buzon_page,
        sesiones_page,
        equipos_page
    ],
    position="hidden"
)


# ==========================================
# SIDEBAR
# ==========================================

with st.sidebar:

    # Logo oficial de Alegra
    st.image(
        "alegra_blanco.png",
        width=130
    )

    # Navegación
    st.page_link(
        home_page,
        label="Inicio"
    )

    st.page_link(
        buzon_page,
        label="Buzón"
    )

    st.page_link(
        sesiones_page,
        label="Subir sesión"
    )

    st.page_link(
        equipos_page,
        label="Equipos"
    )

    st.divider()

    # Usuario
    st.markdown(
    """
    <div style="
        color:#ffffff;
        font-size:14px;
        margin-top:10px;
    ">
        Sofía<br>
        <span style="color:#9fd9d8;">
            Product Manager
        </span>
    </div>
    """,
    unsafe_allow_html=True
    )


# ==========================================
# EJECUTAR
# ==========================================

pg.run()
