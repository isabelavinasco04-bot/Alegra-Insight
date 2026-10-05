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
# ESTADO DEL EQUIPO
# ==========================================

if "team_members" not in st.session_state:
    st.session_state.team_members = TEAM_MEMBERS


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


    /* ==========================================
       BADGES DE URGENCIA
       ========================================== */

    .urgency-badge {
        display: inline-flex;
        align-items: center;
        justify-content: center;
        gap: 7px;
        padding: 7px 12px;
        border-radius: 10px;
        font-weight: 600;
        font-size: 14px;
        line-height: 1;
        white-space: nowrap;
        width: max-content;
        min-width: 72px;
        box-sizing: border-box;
    }

    .urgency-dot {
        width: 10px;
        height: 10px;
        min-width: 10px;
        border-radius: 50%;
        display: inline-block;
    }

    .urgency-high {
        background-color: #ffe5e8;
        color: #c92f45;
    }

    .urgency-high .urgency-dot {
        background-color: #d93650;
    }

    .urgency-medium {
        background-color: #fff9d9;
        color: #8a6d00;
    }

    .urgency-medium .urgency-dot {
        background-color: #e9b92f;
    }

    .urgency-low {
        background-color: #e5f8ed;
        color: #24734a;
    }

    .urgency-low .urgency-dot {
        background-color: #42c77a;
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

                    nuevo_id = len(
                        st.session_state.team_members
                    ) + 1

                    st.session_state.team_members.append(
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

for miembro in st.session_state.team_members:

    for reporte in miembro["reportes"]:

        todos_los_reportes.append(reporte)


# Aceptamos tanto "En progreso" como "En proceso"

total_progress = sum(
    1
    for reporte in todos_los_reportes
    if reporte["estado"] in ["En progreso", "En proceso"]
)


total_resolved = sum(
    1
    for reporte in todos_los_reportes
    if reporte["estado"] in ["Resuelto", "Terminado"]
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
        "En proceso",
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
# INFORMACIÓN DEL REPORTE
# ==========================================

urgencia = reporte["urgencia"]

if urgencia == "Alta":
    fondo = "#fde7e9"
    texto = "#c92f45"
    punto = "#e34b63"

elif urgencia == "Media":
    fondo = "#fff9df"
    texto = "#927000"
    punto = "#e5b83f"

else:
    fondo = "#e8f8ee"
    texto = "#14804a"
    punto = "#55c98b"


st.markdown(
    f"""
    <div style="
        display: flex;
        justify-content: space-between;
        align-items: flex-start;
        gap: 20px;
        width: 100%;
    ">

        <div style="
            flex: 1;
            min-width: 0;
        ">

            <div style="
                font-size: 18px;
                font-weight: 700;
                color: #17213a;
                line-height: 1.4;
                margin-bottom: 8px;
            ">
                {reporte['titulo']}
            </div>

            <div style="
                font-size: 14px;
                color: #687080;
            ">
                {reporte['pais']} · Reporte #{reporte['id']}
            </div>

        </div>

        <div style="
            flex-shrink: 0;
            width: 105px;
            min-width: 105px;
            box-sizing: border-box;
            background-color: {fondo};
            color: {texto};
            border-radius: 10px;
            padding: 12px 10px;
            display: flex;
            align-items: center;
            justify-content: center;
            gap: 7px;
            font-size: 14px;
            font-weight: 600;
            white-space: nowrap;
        ">

            <span style="
                width: 10px;
                height: 10px;
                min-width: 10px;
                border-radius: 50%;
                background-color: {punto};
                display: inline-block;
            "></span>

            <span>{urgencia}</span>

        </div>

    </div>
    """,
    unsafe_allow_html=True
)

        # ==========================================
        # URGENCIA
        # ==========================================

        if reporte["urgencia"] == "Alta":

            st.markdown(
                """
                <div class="urgency-badge urgency-high">
                    <span class="urgency-dot"></span>
                    <span>Alta</span>
                </div>
                """,
                unsafe_allow_html=True
            )

        elif reporte["urgencia"] == "Media":

            st.markdown(
                """
                <div class="urgency-badge urgency-medium">
                    <span class="urgency-dot"></span>
                    <span>Media</span>
                </div>
                """,
                unsafe_allow_html=True
            )

        else:

            st.markdown(
                """
                <div class="urgency-badge urgency-low">
                    <span class="urgency-dot"></span>
                    <span>Baja</span>
                </div>
                """,
                unsafe_allow_html=True
            )


    # ==========================================
    # ESTADO DEL REPORTE
    # ==========================================

    if reporte["estado"] in ["En progreso", "En proceso"]:

        st.info(
            "🟡 En proceso"
        )

    elif reporte["estado"] == "Pendiente":

        st.caption(
            "⚪ Pendiente"
        )

    elif reporte["estado"] == "En revisión":

        st.warning(
            "🟠 En revisión"
        )

    elif reporte["estado"] in ["Resuelto", "Terminado"]:

        st.success(
            "🟢 Terminado"
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

        # ==========================================
        # CABECERA DEL MIEMBRO
        # ==========================================

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


        # ==========================================
        # REPORTES DEL MIEMBRO
        # ==========================================

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

    columns = st.columns(2, gap="large")

    for index, miembro in enumerate(
        st.session_state.team_members
    ):

        with columns[index % 2]:

            mostrar_miembro(miembro)


# ==========================================
# DESARROLLADORES
# ==========================================

with tab_dev:

    desarrolladores = [
        miembro
        for miembro in st.session_state.team_members
        if miembro["rol"] == "Desarrollador"
    ]


    if desarrolladores:

        columns = st.columns(2)

        for index, miembro in enumerate(
            desarrolladores
        ):

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
        for miembro in st.session_state.team_members
        if miembro["rol"] == "Diseñadora"
    ]


    if disenadores:

        columns = st.columns(2)

        for index, miembro in enumerate(
            disenadores
        ):

            with columns[index % 2]:

                mostrar_miembro(miembro)

    else:

        st.info(
            "No hay diseñadores registrados."
        )
