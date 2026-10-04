import streamlit as st
import textwrap
from data import ALL_FEEDBACK


# ==========================================
# CONFIGURACIÓN
# ==========================================

st.set_page_config(
    page_title="Equipos | Alegra Insight",
    page_icon="Logo_pequeño_alegra.webp",
    layout="wide"
)


# ==========================================
# MIEMBROS DEL EQUIPO
# ==========================================

TEAM_MEMBERS = [
    {
        "id": 1,
        "nombre": "Juan",
        "rol": "Desarrollador",
        "estado": "Disponible"
    },
    {
        "id": 2,
        "nombre": "Carlos",
        "rol": "Desarrollador",
        "estado": "Ocupado"
    },
    {
        "id": 3,
        "nombre": "Sara",
        "rol": "Diseñadora",
        "estado": "Disponible"
    }
]


# ==========================================
# REPORTES DE EJEMPLO
# ==========================================

TEAM_REPORTS = [
    {
        "id": 1,
        "miembro_id": 1,
        "titulo": "Error al emitir facturas",
        "urgencia": "Alta",
        "estado": "En progreso",
        "pais": "México"
    },
    {
        "id": 2,
        "miembro_id": 1,
        "titulo": "La app se cierra al abrir reportes",
        "urgencia": "Media",
        "estado": "Pendiente",
        "pais": "Colombia"
    },
    {
        "id": 3,
        "miembro_id": 1,
        "titulo": "Problema con impresión",
        "urgencia": "Baja",
        "estado": "Resuelto",
        "pais": "Colombia"
    },
    {
        "id": 4,
        "miembro_id": 2,
        "titulo": "Subir e.firma desde el celular",
        "urgencia": "Alta",
        "estado": "En progreso",
        "pais": "México"
    },
    {
        "id": 5,
        "miembro_id": 2,
        "titulo": "Pantalla en blanco al abrir facturas",
        "urgencia": "Media",
        "estado": "Pendiente",
        "pais": "Colombia"
    },
    {
        "id": 6,
        "miembro_id": 3,
        "titulo": "Botones muy pequeños",
        "urgencia": "Baja",
        "estado": "En progreso",
        "pais": "Colombia"
    },
    {
        "id": 7,
        "miembro_id": 3,
        "titulo": "Agregar descuento en la factura",
        "urgencia": "Media",
        "estado": "En revisión",
        "pais": "México"
    }
]


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
   MEMBER CARDS
   ========================================== */

.member-card {
    background: #ffffff;
    border: 1px solid #e3e7ed;
    border-radius: 16px;
    padding: 22px;
    margin-bottom: 18px;
    box-shadow: 0 2px 8px rgba(23, 33, 58, 0.03);
}

.member-card:hover {
    border-color: #2fb7b5;
    box-shadow: 0 5px 18px rgba(23, 33, 58, 0.07);
}


/* ==========================================
   AVATAR
   ========================================== */

.avatar {
    width: 46px;
    height: 46px;
    border-radius: 50%;
    background: linear-gradient(
        135deg,
        #2fb7b5,
        #17213a
    );
    color: white;
    display: flex;
    align-items: center;
    justify-content: center;
    font-weight: 700;
    font-size: 17px;
    flex-shrink: 0;
}


/* ==========================================
   REPORT ROW
   ========================================== */

.report-row {
    background: #f8fafb;
    border: 1px solid #e8edf2;
    border-radius: 10px;
    padding: 13px 15px;
    margin-top: 10px;
}

.report-title {
    color: #17213a;
    font-weight: 600;
    font-size: 14px;
}

.report-meta {
    color: #687080;
    font-size: 12px;
    margin-top: 4px;
}


/* ==========================================
   BADGES
   ========================================== */

.badge {
    display: inline-block;
    padding: 5px 9px;
    border-radius: 20px;
    font-size: 11px;
    font-weight: 600;
}

.badge-high {
    background: #fde7e7;
    color: #c03939;
}

.badge-medium {
    background: #fff2d6;
    color: #a56a00;
}

.badge-low {
    background: #dff6f4;
    color: #168d89;
}

.badge-progress {
    background: #e3f3f4;
    color: #168d89;
}

.badge-pending {
    background: #f0f2f5;
    color: #687080;
}

.badge-review {
    background: #eee9ff;
    color: #7056b8;
}

.badge-resolved {
    background: #e1f5e9;
    color: #25804c;
}


/* ==========================================
   BUTTONS
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
   DIVIDER
   ========================================== */

hr {
    border-color: #e5e7eb;
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
        '<div class="page-subtitle">'
        'Da seguimiento a los reportes y conoce en qué está trabajando cada miembro del equipo.'
        '</div>',
        unsafe_allow_html=True
    )

with header_col2:
    if st.button(
        "＋ Agregar nuevo miembro",
        use_container_width=True,
        type="primary"
    ):
        st.session_state.show_member_form = True


# ==========================================
# FORMULARIO NUEVO MIEMBRO
# ==========================================

if "show_member_form" not in st.session_state:
    st.session_state.show_member_form = False


if st.session_state.show_member_form:

    with st.container(border=True):

        st.subheader("＋ Nuevo miembro")

        col1, col2 = st.columns(2)

        with col1:
            nombre = st.text_input(
                "Nombre",
                placeholder="Ej. Laura"
            )

        with col2:
            rol = st.selectbox(
                "Rol",
                [
                    "Desarrollador",
                    "Diseñador"
                ]
            )

        col1, col2 = st.columns(2)

        with col1:

            if st.button(
                "Agregar miembro",
                type="primary",
                use_container_width=True
            ):

                if nombre.strip():

                    st.success(
                        f"{nombre} fue agregado al equipo."
                    )

                    st.session_state.show_member_form = False
                    st.rerun()

                else:

                    st.warning(
                        "Escribe un nombre."
                    )

        with col2:

            if st.button(
                "Cancelar",
                use_container_width=True
            ):

                st.session_state.show_member_form = False
                st.rerun()


st.markdown("---")


# ==========================================
# MÉTRICAS
# ==========================================

total_progress = len([
    x for x in TEAM_REPORTS
    if x["estado"] == "En progreso"
])

total_resolved = len([
    x for x in TEAM_REPORTS
    if x["estado"] == "Resuelto"
])

total_pending = len([
    x for x in TEAM_REPORTS
    if x["estado"] == "Pendiente"
])

total_review = len([
    x for x in TEAM_REPORTS
    if x["estado"] == "En revisión"
])


col1, col2, col3, col4 = st.columns(4)

with col1:
    st.metric("En progreso", total_progress)

with col2:
    st.metric("Resueltos", total_resolved)

with col3:
    st.metric("Pendientes", total_pending)

with col4:
    st.metric("Necesitan revisión", total_review)


st.markdown("---")


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
# FUNCIÓN PARA MOSTRAR MIEMBRO
# ==========================================

def mostrar_miembro(miembro):

    reportes = [
        x for x in TEAM_REPORTS
        if x["miembro_id"] == miembro["id"]
    ]

    iniciales = "".join(
        parte[0]
        for parte in miembro["nombre"].split()
    ).upper()


    # ------------------------------
    # CABECERA DE LA CARD
    # ------------------------------

    st.markdown(
    textwrap.dedent(f"""
    <div class="member-card">

        <div style="
            display:flex;
            align-items:center;
            gap:14px;
            margin-bottom:18px;
        ">

            <div class="avatar">
                {iniciales}
            </div>

            <div>

                <div style="
                    color:#17213a;
                    font-size:18px;
                    font-weight:700;
                ">
                    {miembro["nombre"]}
                </div>

                <div style="
                    color:#687080;
                    font-size:13px;
                    margin-top:3px;
                ">
                    {miembro["rol"]} · {miembro["estado"]}
                </div>

            </div>

            </div>
    
            <div style="
                color:#17213a;
                font-size:13px;
                font-weight:700;
                margin-bottom:8px;
            ">
                Reportes asignados · {len(reportes)}
            </div>
        """),
        unsafe_allow_html=True
        )


    # ------------------------------
    # REPORTES
    # ------------------------------

    if reportes:

        for reporte in reportes:

            if reporte["urgencia"] == "Alta":
                urgency_class = "badge-high"

            elif reporte["urgencia"] == "Media":
                urgency_class = "badge-medium"

            else:
                urgency_class = "badge-low"


            if reporte["estado"] == "En progreso":
                status_class = "badge-progress"

            elif reporte["estado"] == "Pendiente":
                status_class = "badge-pending"

            elif reporte["estado"] == "En revisión":
                status_class = "badge-review"

            else:
                status_class = "badge-resolved"


           st.markdown(
            textwrap.dedent(f"""
                <div class="report-row">

                <div class="report-title">
                    {reporte["titulo"]}
                </div>

                <div class="report-meta">
                    {reporte["pais"]}
                </div>

                <div style="
                    margin-top:8px;
                    display:flex;
                    gap:6px;
                ">

            <span class="badge {urgency_class}">
                {reporte["urgencia"]}
            </span>

            <span class="badge {status_class}">
                {reporte["estado"]}
            </span>

            </div>

            </div>
            """),
            unsafe_allow_html=True
            )

    else:

        st.caption(
            "No hay reportes asignados."
        )


    # Cerrar card

    st.markdown(
        "</div>",
        unsafe_allow_html=True
    )


# ==========================================
# VISTA GENERAL
# ==========================================

with tab_general:

    st.subheader("Actividad del equipo")

    if TEAM_MEMBERS:

        columns = st.columns(2)

        for index, miembro in enumerate(TEAM_MEMBERS):

            with columns[index % 2]:

                mostrar_miembro(miembro)


# ==========================================
# DESARROLLADORES
# ==========================================

with tab_dev:

    desarrolladores = [
        x for x in TEAM_MEMBERS
        if x["rol"] == "Desarrollador"
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
        x for x in TEAM_MEMBERS
        if x["rol"] == "Diseñadora"
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
