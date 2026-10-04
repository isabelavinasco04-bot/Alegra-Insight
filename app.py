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

    st.markdown(
        """
        <div style="
            font-size:25px;
            font-weight:700;
            color:#17213a;
            margin-bottom:35px;
        ">
            🌿 alegra
        </div>
        """,
        unsafe_allow_html=True
    )

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

    st.markdown(
        """
        <div style="
            color:#687080;
            font-size:14px;
        ">
            Sofía<br>
            <span style="color:#9aa0aa;">
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
