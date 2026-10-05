import streamlit as st


# ==========================================
# CONFIGURACIÓN
# ==========================================

st.set_page_config(
    page_title="Equipos | Alegra Insight",
    page_icon="Logo_pequeño_alegra.webp",
    layout="wide"
)


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
# ESTILOS
# ==========================================

st.markdown(
    """
    <style>

    /* ==========================================
       FORZAR TEMA CLARO
       ========================================== */

    :root {
        color-scheme: light !important;
    }

    html,
    body {
        color-scheme: light !important;
    }

    .stApp {
        background-color: #ffffff !important;
        color: #17213a !important;
    }

    [data-testid="stAppViewContainer"] {
        background-color: #ffffff !important;
    }

    [data-testid="stMain"] {
        background-color: #ffffff !important;
    }


    /* ==========================================
       CONTENEDOR
       ========================================== */

    .block-container {
        padding-top: 2rem;
        padding-left: 3.5rem;
        padding-right: 3.5rem;
        padding-bottom: 3rem;
    }


    /* ==========================================
       TEXTOS PRINCIPALES
       ========================================== */

    h1,
    h2,
    h3,
    h4,
    h5,
    h6 {
        color: #17213a !important;
    }

    p,
    label,
    span,
    div {
        color: inherit;
    }

    .page-subtitle {
        color: #687080 !important;
        font-size: 16px;
        margin-top: -10px;
        margin-bottom: 25px;
    }


    /* ==========================================
       CAPTIONS
       ========================================== */

    [data-testid="stCaptionContainer"] {
        color: #687080 !important;
    }

    [data-testid="stCaptionContainer"] * {
        color: #687080 !important;
    }


    /* ==========================================
       MÉTRICAS
       ========================================== */

    [data-testid="stMetric"] {
        background-color: #f8fafb !important;
        border: 1px solid #e3e7ed !important;
        border-radius: 14px;
        padding: 16px;
    }

    [data-testid="stMetricLabel"] {
        color: #687080 !important;
    }

    [data-testid="stMetricLabel"] * {
        color: #687080 !important;
    }

    [data-testid="stMetricValue"] {
        color: #17213a !important;
    }

    [data-testid="stMetricValue"] * {
        color: #17213a !important;
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
        ) !important;

        border: none !important;
        color: #ffffff !important;
    }

    div.stButton > button[kind="primary"] * {
        color: #ffffff !important;
    }

    div.stButton > button[kind="primary"]:hover {
        opacity: 0.9;
    }


    /* ==========================================
       TABS
       ========================================== */

    button[data-baseweb="tab"] {
        color: #687080 !important;
        font-weight: 600;
    }

    button[data-baseweb="tab"] * {
        color: #687080 !important;
    }

    button[data-baseweb="tab"][aria-selected="true"] {
        color: #2fb7b5 !important;
    }

    button[data-baseweb="tab"][aria-selected="true"] * {
        color: #2fb7b5 !important;
    }


    /* ==========================================
       CONTENEDORES
       ========================================== */

    [data-testid="stVerticalBlockBorderWrapper"] {
        border-radius: 14px;
        border-color: #e3e7ed !important;
    }


    /* ==========================================
       INPUTS
       ========================================== */

    input,
    textarea,
    select {
        color: #17213a !important;
        background-color: #ffffff !important;
    }

    input::placeholder,
    textarea::placeholder {
        color: #8a93a3 !important;
    }


    /* ==========================================
       BADGES DE URGENCIA
       ========================================== */

    .urgency-badge {
        display: inline-flex;
        align-items: center;
        justify-content: center;
        gap: 8px;

        min-width: 82px;
        width: fit-content;

        padding: 8px 12px;

        border-radius: 10px;

        font-size: 14px;
        font-weight: 600;

        white-space: nowrap;
        word-break: keep-all;
        overflow-wrap: normal;
    }

    .urgency-dot {
        width: 10px;
        height: 10px;
        min-width: 10px;

        border-radius: 50%;
        display: inline-block;
    }

    .urgency-high {
        background-color: #fde7eb;
        color: #c83250 !important;
    }

    .urgency-high .urgency-dot {
        background-color: #d93655;
    }

    .urgency-medium {
        background-color: #fff9d9;
        color: #a77a00 !important;
    }

    .urgency-medium .urgency-dot {
        background-color: #e8b52d;
    }

    .urgency-low {
        background-color: #e6f7ee;
        color: #26734d !important;
    }

    .urgency-low .urgency-dot {
        background-color: #52c78a;
    }


    /* ==========================================
       ESTADOS
       ========================================== */

    .status-box {
        width: 100%;
        box-sizing: border-box;

        padding: 12px 16px;

        border-radius: 10px;

        font-size: 15px;
        font-weight: 500;

        margin-top: 12px;

        white-space: nowrap;
    }

    .status-progress {
        background-color: #eaf2ff;
        color: #1261b0 !important;
    }

    .status-pending {
        background-color: #f5f5f7;
        color: #687080 !important;
    }

    .status-review {
        background-color: #fff4df;
        color: #a56300 !important;
    }

    .status-done {
        background-color: #e7f7ee;
        color: #28734d !important;
    }


    /* ==========================================
       INFO / WARNING / SUCCESS
       ========================================== */

    [data-testid="stAlert"] {
        color: #17213a !important;
    }

    [data-testid="stAlert"] * {
        color: inherit;
    }


    /* ==========================================
       RESPONSIVE
       ========================================== */

    @media (max-width: 900px) {

        .block-container {
            padding-left: 1.5rem;
            padding-right: 1.5rem;
        }

        .urgency-badge {
            min-width: 76px;
            padding: 7px 9px;
        }

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
# FUNCIÓN PARA MOSTRAR URGENCIA
# ==========================================

def mostrar_urgencia(urgencia):

    if urgencia == "Alta":

        clase = "urgency-high"

    elif urgencia == "Media":

        clase = "urgency-medium"

    else:

        clase = "urgency-low"

    st.markdown(
        f"""
        <div class="urgency-badge {clase}">
            <span class="urgency-dot"></span>
            <span>{urgencia}</span>
        </div>
        """,
        unsafe_allow_html=True
    )


# ==========================================
# FUNCIÓN PARA MOSTRAR ESTADO
# ==========================================

def mostrar_estado(estado):

    if estado in ["En progreso", "En proceso"]:

        st.markdown(
            """
            <div class="status-box status-progress">
                🟡 En proceso
            </div>
            """,
            unsafe_allow_html=True
        )

    elif estado == "Pendiente":

        st.markdown(
            """
            <div class="status-box status-pending">
                ⚪ Pendiente
            </div>
            """,
            unsafe_allow_html=True
        )

    elif estado == "En revisión":

        st.markdown(
            """
            <div class="status-box status-review">
                🟠 En revisión
            </div>
            """,
            unsafe_allow_html=True
        )

    elif estado in ["Resuelto", "Terminado"]:

        st.markdown(
            """
            <div class="status-box status-done">
                🟢 Terminado
            </div>
            """,
            unsafe_allow_html=True
        )


# ==========================================
# FUNCIÓN PARA MOSTRAR REPORTE
# ==========================================

def mostrar_reporte(reporte):

    col1, col2 = st.columns([4.5, 1.2])

    with col1:

        st.markdown(
            f"""
            <div style="
                color:#17213a;
                font-size:16px;
                font-weight:700;
                margin-bottom:8px;
            ">
                {reporte['titulo']}
            </div>
            """,
            unsafe_allow_html=True
        )

        st.markdown(
            f"""
            <div style="
                color:#687080;
                font-size:14px;
            ">
                {reporte['pais']} · Reporte #{reporte['id']}
            </div>
            """,
            unsafe_allow_html=True
        )


    with col2:

        mostrar_urgencia(
            reporte["urgencia"]
        )


    mostrar_estado(
        reporte["estado"]
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
                    color:white !important;
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
                f"""
                <div style="
                    color:#17213a;
                    font-size:24px;
                    font-weight:700;
                    margin-bottom:5px;
                ">
                    {miembro['nombre']}
                </div>
                """,
                unsafe_allow_html=True
            )

            st.markdown(
                f"""
                <div style="
                    color:#687080;
                    font-size:15px;
                ">
                    {miembro['rol']} · {miembro['estado']}
                </div>
                """,
                unsafe_allow_html=True
            )


        st.markdown(
            f"""
            <div style="
                color:#17213a;
                font-weight:700;
                margin-top:18px;
                margin-bottom:12px;
            ">
                Reportes asignados · {len(reportes)}
            </div>
            """,
            unsafe_allow_html=True
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

    st.markdown(
        """
        <h3 style="color:#17213a !important;">
            Actividad del equipo
        </h3>
        """,
        unsafe_allow_html=True
    )

    columns = st.columns(2)

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
