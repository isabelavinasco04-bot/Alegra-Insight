import streamlit as st


# ==========================================
# DATOS DEL EQUIPO
# ==========================================

TEAM_MEMBERS = [
    {
        "id": 1,
        "nombre": "Juan",
        "rol": "Desarrollador",
        "estado": "Disponible",
        "reportes": [
            {
                "id": 1,
                "titulo": "Error al emitir facturas",
                "urgencia": "Alta",
                "estado": "En progreso",
                "pais": "México"
            },
            {
                "id": 2,
                "titulo": "La app se cierra al abrir Reportes",
                "urgencia": "Alta",
                "estado": "Pendiente",
                "pais": "Colombia"
            },
            {
                "id": 3,
                "titulo": "Problema con impresión desde celular",
                "urgencia": "Baja",
                "estado": "Resuelto",
                "pais": "Colombia"
            }
        ]
    },
    {
        "id": 2,
        "nombre": "Carlos",
        "rol": "Desarrollador",
        "estado": "Ocupado",
        "reportes": [
            {
                "id": 4,
                "titulo": "Subir e.firma desde el celular",
                "urgencia": "Media",
                "estado": "En progreso",
                "pais": "México"
            },
            {
                "id": 5,
                "titulo": "Pantalla blanca después de actualizar",
                "urgencia": "Alta",
                "estado": "Pendiente",
                "pais": "Colombia"
            }
        ]
    },
    {
        "id": 3,
        "nombre": "Sara",
        "rol": "Diseñadora",
        "estado": "Disponible",
        "reportes": [
            {
                "id": 6,
                "titulo": "Botones muy pequeños",
                "urgencia": "Baja",
                "estado": "En revisión",
                "pais": "Colombia"
            },
            {
                "id": 7,
                "titulo": "Agregar descuento por línea",
                "urgencia": "Media",
                "estado": "En progreso",
                "pais": "España"
            }
        ]
    }
]


# ==========================================
# CONFIGURACIÓN
# ==========================================

st.set_page_config(
    page_title="Equipos | Alegra Insight",
    page_icon="Logo_pequeño_alegra.webp",
    layout="wide"
)


# ==========================================
# ESTILOS
# ==========================================

st.markdown(
    """
    <style>

    .stApp {
        background-color: #ffffff;
    }

    .block-container {
        padding-top: 2rem;
        padding-left: 3.5rem;
        padding-right: 3.5rem;
        padding-bottom: 3rem;
    }

    h1, h2, h3 {
        color: #17213a;
    }

    .page-subtitle {
        color: #687080;
        font-size: 16px;
        margin-top: -10px;
        margin-bottom: 25px;
    }

    /* ==========================================
       MÉTRICAS
       ========================================== */

    [data-testid="stMetric"] {
        background-color: #f8fafb;
        border: 1px solid #e3e7ed;
        border-radius: 14px;
        padding: 16px;
    }

    [data-testid="stMetricLabel"] {
        color: #687080;
    }

    [data-testid="stMetricValue"] {
        color: #17213a;
    }


    /* ==========================================
       BOTONES
       ========================================== */

    div.stButton > button {
        border-radius: 8px;
        font-weight: 600;
        transition: all 0.2s ease;
    }

    div.stButton > button[kind="primary"] {
        background: linear-gradient(
            135deg,
            #2fb7b5,
            #17213a
        );
        border: none;
        color: white;
    }

    div.stButton > button[kind="primary"]:hover {
        opacity: 0.9;
    }


    /* ==========================================
       TABS
       ========================================== */

    button[data-baseweb="tab"] {
        color: #687080;
        font-weight: 600;
    }

    button[data-baseweb="tab"][aria-selected="true"] {
        color: #2fb7b5;
    }


    /* ==========================================
       CONTENEDORES
       ========================================== */

    [data-testid="stVerticalBlockBorderWrapper"] {
        border-radius: 14px;
    }

    </style>
    """,
    unsafe_allow_html=True
)


# ==========================================
# HEADER
# ==========================================

header_col1, header_col2 = st.columns([5, 1])

with header_col1:

    st.title("Equipos")

    st.markdown(
        """
        <div class="page-subtitle">
            Da seguimiento a los reportes y conoce en qué está
            trabajando cada miembro del equipo.
        </div>
        """,
        unsafe_allow_html=True
    )


with header_col2:

    if st.button(
        "＋ Agregar miembro",
        type="primary",
        use_container_width=True
    ):
        st.session_state["show_member_form"] = True


# ==========================================
# ESTADO DEL FORMULARIO
# ==========================================

if "show_member_form" not in st.session_state:

    st.session_state["show_member_form"] = False


# ==========================================
# FORMULARIO NUEVO MIEMBRO
# ==========================================

if st.session_state["show_member_form"]:

    with st.container(border=True):

        st.subheader("Nuevo miembro")

        col1, col2 = st.columns(2)

        with col1:

            nuevo_nombre = st.text_input(
                "Nombre",
                placeholder="Ej. Laura"
            )

        with col2:

            nuevo_rol = st.selectbox(
                "Rol",
                [
                    "Desarrollador",
                    "Diseñadora"
                ]
            )

        col1, col2 = st.columns(2)

        with col1:

            if st.button(
                "Agregar miembro",
                type="primary",
                use_container_width=True
            ):

                if nuevo_nombre.strip():

                    nuevo_id = len(TEAM_MEMBERS) + 1

                    TEAM_MEMBERS.append(
                        {
                            "id": nuevo_id,
                            "nombre": nuevo_nombre.strip(),
                            "rol": nuevo_rol,
                            "estado": "Disponible",
                            "reportes": []
                        }
                    )

                    st.session_state["show_member_form"] = False

                    st.success(
                        f"{nuevo_nombre} fue agregado al equipo."
                    )

                    st.rerun()

                else:

                    st.warning(
                        "Escribe el nombre del nuevo miembro."
                    )

        with col2:

            if st.button(
                "Cancelar",
                use_container_width=True
            ):

                st.session_state["show_member_form"] = False

                st.rerun()


st.divider()


# ==========================================
# CALCULAR MÉTRICAS
# ==========================================

todos_los_reportes = []

for miembro in TEAM_MEMBERS:

    for reporte in miembro["reportes"]:

        todos_los_reportes.append(reporte)


total_progress = sum(
    1
    for reporte in todos_los_reportes
    if reporte["estado"] == "En progreso"
)


total_resolved = sum(
    1
    for reporte in todos_los_reportes
    if reporte["estado"] == "Resuelto"
)


total_pending = sum(
    1
    for reporte in todos_los_reportes
    if reporte["estado"] == "Pendiente"
)


total_review = sum(
    1
    for reporte in todos_los_reportes
    if reporte["estado"] == "En revisión"
)


# ==========================================
# MÉTRICAS
# ==========================================

col1, col2, col3, col4 = st.columns(4)

with col1:

    st.metric(
        "En progreso",
        total_progress
    )


with col2:

    st.metric(
        "Resueltos",
        total_resolved
    )


with col3:

    st.metric(
        "Pendientes",
        total_pending
    )


with col4:

    st.metric(
        "Necesitan revisión",
        total_review
    )


st.divider()


# ==========================================
# TABS
# ==========================================

tab_general, tab_dev, tab_design = st.tabs(
    [
        "Vista general",
        "Desarrolladores",
        "Diseñadores"
    ]
)


# ==========================================
# FUNCIÓN PARA MOSTRAR REPORTE
# ==========================================

def mostrar_reporte(reporte):

    col1, col2 = st.columns([5, 1])

    with col1:

        st.markdown(
            f"**{reporte['titulo']}**"
        )

        st.caption(
            f"{reporte['pais']} · Reporte #{reporte['id']}"
        )


    with col2:

        if reporte["urgencia"] == "Alta":

            st.error("🔴 Alta")

        elif reporte["urgencia"] == "Media":

            st.warning("🟡 Media")

        else:

            st.success("🟢 Baja")


    # Estado

    if reporte["estado"] == "En progreso":

        st.info(
            "En progreso"
        )

    elif reporte["estado"] == "Pendiente":

        st.caption(
            "Pendiente"
        )

    elif reporte["estado"] == "En revisión":

        st.warning(
            "En revisión"
        )

    elif reporte["estado"] == "Resuelto":

        st.success(
            "Resuelto"
        )


# ==========================================
# FUNCIÓN PARA MOSTRAR MIEMBRO
# ==========================================

def mostrar_miembro(miembro):

    reportes = miembro["reportes"]

    iniciales = "".join(
        palabra[0]
        for palabra in miembro["nombre"].split()
    ).upper()


    with st.container(border=True):

        # --------------------------------------
        # CABECERA DEL MIEMBRO
        # --------------------------------------

        col1, col2 = st.columns([1, 5])

        with col1:

            st.markdown(
                f"""
                <div style="
                    width:48px;
                    height:48px;
                    border-radius:50%;
                    background:linear-gradient(
                        135deg,
                        #2fb7b5,
                        #17213a
                    );
                    color:white;
                    display:flex;
                    align-items:center;
                    justify-content:center;
                    font-weight:700;
                    font-size:17px;
                ">
                    {iniciales}
                </div>
                """,
                unsafe_allow_html=True
            )


        with col2:

            st.markdown(
                f"### {miembro['nombre']}"
            )

            st.caption(
                f"{miembro['rol']} · {miembro['estado']}"
            )


        st.markdown(
            f"**Reportes asignados · {len(reportes)}**"
        )


        # --------------------------------------
        # REPORTES DEL MIEMBRO
        # --------------------------------------

        if not reportes:

            st.info(
                "Este miembro no tiene reportes asignados."
            )

        else:

            for reporte in reportes:

                with st.container(border=True):

                    mostrar_reporte(reporte)


# ==========================================
# VISTA GENERAL
# ==========================================

with tab_general:

    st.subheader("Actividad del equipo")

    columns = st.columns(2)

    for index, miembro in enumerate(TEAM_MEMBERS):

        with columns[index % 2]:

            mostrar_miembro(miembro)


# ==========================================
# DESARROLLADORES
# ==========================================

with tab_dev:

    desarrolladores = [
        miembro
        for miembro in TEAM_MEMBERS
        if miembro["rol"] == "Desarrollador"
    ]


    if desarrolladores:

        columns = st.columns(2)

        for index, miembro in enumerate(desarrolladores):

            with columns[index % 2]:

                mostrar_miembro(miembro)

    else:

        st.info(
            "No hay desarrolladores registrados."
        )


# ==========================================
# DISEÑADORES
# ==========================================

with tab_design:

    disenadores = [
        miembro
        for miembro in TEAM_MEMBERS
        if miembro["rol"] == "Diseñadora"
    ]


    if disenadores:

        columns = st.columns(2)

        for index, miembro in enumerate(disenadores):

            with columns[index % 2]:

                mostrar_miembro(miembro)

    else:

        st.info(
            "No hay diseñadores registrados."
        )
