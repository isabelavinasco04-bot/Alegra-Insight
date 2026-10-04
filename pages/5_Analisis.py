import streamlit as st
from google import genai
from data import ALL_FEEDBACK
from io import BytesIO
from reportlab.lib.pagesizes import A4
from reportlab.platypus import (
    SimpleDocTemplate,
    Paragraph,
    Spacer,
    Table,
    TableStyle
)
from reportlab.lib import colors
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.enums import TA_LEFT


# ==========================================
# CONFIGURACIÓN
# ==========================================

st.set_page_config(
    page_title="Análisis | Alegra Insight",
    page_icon="Logo_pequeño_alegra.webp",
    layout="wide"
)


# ==========================================
# GEMINI
# ==========================================

client = genai.Client(
    api_key=st.secrets["GEMINI_API_KEY"]
)

GEMINI_MODEL = "gemini-3.8-flash"


# ==========================================
# ESTILOS
# ==========================================

st.markdown("""
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
   CARDS
   ========================================== */

.report-card {
    background: #ffffff;
    border: 1px solid #e3e7ed;
    border-radius: 16px;
    padding: 24px;
    height: 590px;
    overflow-y: auto;
}

.analysis-card {
    background: #f8fafb;
    border: 1px solid #e3e7ed;
    border-radius: 16px;
    padding: 24px;
    height: 590px;
    overflow-y: auto;
}


/* Scroll bonito */

.report-card::-webkit-scrollbar,
.analysis-card::-webkit-scrollbar {
    width: 7px;
}

.report-card::-webkit-scrollbar-thumb,
.analysis-card::-webkit-scrollbar-thumb {
    background: #cbd5df;
    border-radius: 10px;
}


/* ==========================================
   TÍTULOS
   ========================================== */

.card-title {
    color: #17213a;
    font-size: 21px;
    font-weight: 700;
    margin-bottom: 18px;
}

.section-title {
    color: #17213a;
    font-size: 17px;
    font-weight: 700;
    margin-top: 20px;
    margin-bottom: 8px;
}

.field-label {
    color: #687080;
    font-size: 12px;
    font-weight: 700;
    text-transform: uppercase;
    letter-spacing: .3px;
    margin-top: 16px;
    margin-bottom: 5px;
}

.field-value {
    color: #17213a;
    font-size: 15px;
    line-height: 1.6;
}


/* ==========================================
   BADGES
   ========================================== */

.badge {
    display: inline-block;
    padding: 5px 10px;
    border-radius: 20px;
    font-size: 12px;
    font-weight: 600;
    margin-right: 5px;
}

.badge-teal {
    background: #d9f7f5;
    color: #168d89;
}

.badge-dark {
    background: #e8edf5;
    color: #17213a;
}


/* ==========================================
   BOTONES
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

.secondary-button div.stButton > button {
    background-color: white;
    color: #17213a;
    border: 1px solid #d5dbe3;
}

.secondary-button div.stButton > button:hover {
    background-color: #17213a;
    color: white;
    border-color: #17213a;
}


/* ==========================================
   TOGGLE
   ========================================== */

[data-testid="stToggle"] label {
    color: #17213a !important;
    font-weight: 600;
}


/* Switch apagado */

[data-testid="stToggle"] div[role="switch"] {
    background-color: #dfe3e8 !important;
    border: 1px solid #dfe3e8 !important;
}


/* Switch encendido */

[data-testid="stToggle"] div[role="switch"][aria-checked="true"] {
    background: linear-gradient(
        135deg,
        #2fb7b5 0%,
        #17213a 100%
    ) !important;

    border-color: transparent !important;
}


/* Círculo del switch */

[data-testid="stToggle"] div[role="switch"]::before {
    background-color: #ffffff !important;
    border-color: #ffffff !important;
    box-shadow: 0 1px 4px rgba(23, 33, 58, 0.18) !important;
}


/* ==========================================
   DIVISOR
   ========================================== */

.action-divider {
    margin-top: 28px;
    margin-bottom: 18px;
    border-top: 1px solid #e5e7eb;
}

/* Switch - Alegra */
div[data-testid="stToggle"] [role="switch"] {
    background: linear-gradient(
        135deg,
        #2fb7b5,
        #17213a
    ) !important;
}

div[data-testid="stToggle"] [role="switch"][aria-checked="false"] {
    background: #dfe3e8 !important;
}

div[data-testid="stToggle"] [role="switch"][aria-checked="true"] {
    background: linear-gradient(
        135deg,
        #2fb7b5,
        #17213a
    ) !important;
}

</style>
""", unsafe_allow_html=True)


# ==========================================
# VERIFICAR REPORTE
# ==========================================

if "selected_feedback" not in st.session_state:

    st.warning(
        "No hay ningún reporte seleccionado para analizar."
    )

    if st.button("← Volver al buzón"):

        st.switch_page("pages/2_Buzon.py")

    st.stop()


item = st.session_state.selected_feedback


# ==========================================
# IDENTIFICADOR DEL ANÁLISIS
# ==========================================

analysis_key = f"analysis_{item['id']}"


# ==========================================
# TODOS LOS REPORTES
# ==========================================

reportes_texto = ""

for reporte in ALL_FEEDBACK:

    reportes_texto += f"""
REPORTE #{reporte['id']}
Tipo: {reporte['tipo']}
País: {reporte['pais']}
Urgencia: {reporte['urgencia']}
Comentario: {reporte['comentario']}
"""

    if "calificacion" in reporte:

        reportes_texto += (
            f"Calificación: "
            f"{reporte['calificacion']}/5\n"
        )

    reportes_texto += "\n"


# ==========================================
# GENERAR ANÁLISIS
# ==========================================

def generar_analisis():

    prompt = f"""
Eres Alegra Insight, una herramienta interna
para Product Managers de Alegra.

Analiza el siguiente reporte utilizando también
el resto del feedback disponible.

IMPORTANTE:

- Basa las conclusiones únicamente en los datos proporcionados.
- No inventes información.
- Diferencia hechos de hipótesis.
- Si falta información, escribe "Por confirmar".
- No inventes detalles técnicos.
- Busca relaciones reales entre reportes.
- Cuando relaciones reportes, menciona sus IDs.
- Sé concreta y útil para decisiones de producto.
- Responde en español.

========================================
REPORTE PRINCIPAL
========================================

ID: #{item['id']}
Tipo: {item['tipo']}
País: {item['pais']}
Urgencia: {item['urgencia']}

Comentario:
{item['comentario']}

========================================
TODOS LOS REPORTES
========================================

{reportes_texto}

========================================
RESPONDE EXACTAMENTE CON ESTAS SECCIONES
========================================

## BUG REPORT

Problema:
Describe el problema principal.

Comportamiento observado:
Describe qué está pasando.

Comportamiento esperado:
Describe qué debería pasar.

Impacto:
Explica el impacto para el usuario o negocio.

Severidad:
Baja, Media o Alta y explica brevemente por qué.

## INSIGHTS

Identifica las necesidades, frustraciones
o comportamientos que revela el reporte.

## INFORMACIÓN FALTANTE

Indica qué información hace falta para
comprender o reproducir mejor el problema.

## SUPUESTOS E HIPÓTESIS

Separa claramente:
Hechos confirmados:
Hipótesis:

## RELACIÓN CON OTROS REPORTES

Menciona reportes relacionados utilizando
sus IDs y explica el posible patrón.

Si no existen relaciones claras:
"No se encontraron relaciones claras."

## OPORTUNIDAD DE PRODUCTO

Propón una oportunidad de producto basada
únicamente en los hallazgos.

No propongas una solución técnica específica
si los datos no la justifican.
"""

    response = client.models.generate_content(
        model=GEMINI_MODEL,
        contents=prompt
    )

    if response and response.text:
        return response.text

    return None


# ==========================================
# PARSEAR RESPUESTA DE GEMINI
# ==========================================

def extraer_seccion(texto, titulo, siguiente=None):

    if not texto:
        return "Por confirmar."

    inicio = texto.find(titulo)

    if inicio == -1:
        return "Por confirmar."

    inicio += len(titulo)

    if siguiente:

        fin = texto.find(siguiente, inicio)

        if fin != -1:
            return texto[inicio:fin].strip()

    return texto[inicio:].strip()


def limpiar_texto(texto):

    if not texto:
        return ""

    texto = texto.replace("**", "")
    texto = texto.replace("###", "")
    texto = texto.replace("##", "")

    return texto.strip()


def parsear_analisis(texto):

    bug = extraer_seccion(
        texto,
        "## BUG REPORT",
        "## INSIGHTS"
    )

    insights = extraer_seccion(
        texto,
        "## INSIGHTS",
        "## INFORMACIÓN FALTANTE"
    )

    faltante = extraer_seccion(
        texto,
        "## INFORMACIÓN FALTANTE",
        "## SUPUESTOS E HIPÓTESIS"
    )

    supuestos = extraer_seccion(
        texto,
        "## SUPUESTOS E HIPÓTESIS",
        "## RELACIÓN CON OTROS REPORTES"
    )

    relaciones = extraer_seccion(
        texto,
        "## RELACIÓN CON OTROS REPORTES",
        "## OPORTUNIDAD DE PRODUCTO"
    )

    oportunidad = extraer_seccion(
        texto,
        "## OPORTUNIDAD DE PRODUCTO"
    )

    return {
        "bug": limpiar_texto(bug),
        "insights": limpiar_texto(insights),
        "faltante": limpiar_texto(faltante),
        "supuestos": limpiar_texto(supuestos),
        "relaciones": limpiar_texto(relaciones),
        "oportunidad": limpiar_texto(oportunidad)
    }


# ==========================================
# GENERACIÓN AUTOMÁTICA
# ==========================================

if analysis_key not in st.session_state:

    with st.spinner(
        "Analizando reporte y buscando patrones..."
    ):

        try:

            resultado = generar_analisis()

            if resultado:

                st.session_state[analysis_key] = parsear_analisis(
                    resultado
                )

            else:

                st.error(
                    "Gemini no devolvió un análisis."
                )

                st.stop()

        except Exception:

            st.error(
                "No pudimos completar el análisis en este momento."
            )

            st.caption(
                "Revisa la conexión con Gemini e intenta nuevamente."
            )

            st.stop()


analysis = st.session_state[analysis_key]


# ==========================================
# ESTADO DEL TOGGLE
# ==========================================

if "attach_analysis" not in st.session_state:
    st.session_state.attach_analysis = True


# ==========================================
# HEADER
# ==========================================

header_col1, header_col2 = st.columns([5, 1])

with header_col1:

    st.markdown(
        """
        <h1 style="
            margin-bottom:4px;
            color:#17213a;
        ">
            Resultado del análisis
        </h1>
        """,
        unsafe_allow_html=True
    )

    st.markdown(
        f"""
        <div style="
            color:#687080;
            font-size:15px;
            margin-bottom:22px;
        ">
            Reporte #{item['id']}
            &nbsp; · &nbsp;
            {item['tipo']}
            &nbsp; · &nbsp;
            {item['pais']}
        </div>
        """,
        unsafe_allow_html=True
    )


with header_col2:

    if st.button(
        "← Volver",
        use_container_width=True
    ):

        st.switch_page("pages/2_Buzon.py")


# ==========================================
# DOS COLUMNAS PRINCIPALES
# ==========================================

left, right = st.columns(
    [1, 1],
    gap="large"
)


# ==========================================
# BUG REPORT
# ==========================================

with left:

    st.markdown(
        """
        <div class="card-title">
            🐛 Bug Report
        </div>
        """,
        unsafe_allow_html=True
    )

    with st.container(
        height=590,
        border=True
    ):

        st.markdown(
            f"""
            <span class="badge badge-teal">
                {item['tipo']}
            </span>

            <span class="badge badge-dark">
                ID #{item['id']}
            </span>
            """,
            unsafe_allow_html=True
        )

        bug_text = analysis["bug"]

        campos_bug = [
            "Problema:",
            "Comportamiento observado:",
            "Comportamiento esperado:",
            "Impacto:",
            "Severidad:"
        ]

        for i, campo in enumerate(campos_bug):

            siguiente = (
                campos_bug[i + 1]
                if i + 1 < len(campos_bug)
                else None
            )

            inicio = bug_text.find(campo)

            if inicio != -1:

                inicio += len(campo)

                if siguiente:

                    fin = bug_text.find(
                        siguiente,
                        inicio
                    )

                    contenido = (
                        bug_text[inicio:fin]
                        if fin != -1
                        else bug_text[inicio:]
                    )

                else:

                    contenido = bug_text[inicio:]

                st.markdown(
                    f"""
                    <div class="field-label">
                        {campo.replace(":", "")}
                    </div>

                    <div class="field-value">
                        {contenido.strip()}
                    </div>
                    """,
                    unsafe_allow_html=True
                )


# ==========================================
# ANÁLISIS IA
# ==========================================

with right:

    st.markdown(
        """
        <div class="card-title">
            🧠 Análisis de IA
        </div>
        """,
        unsafe_allow_html=True
    )

    with st.container(
        height=590,
        border=True
    ):

        # INSIGHTS

        st.markdown(
            """
            <div class="section-title">
                💡 Insights
            </div>
            """,
            unsafe_allow_html=True
        )

        st.markdown(
            analysis["insights"]
        )

        st.divider()


        # INFORMACIÓN FALTANTE

        st.markdown(
            """
            <div class="section-title">
                🔎 Información faltante
            </div>
            """,
            unsafe_allow_html=True
        )

        st.markdown(
            analysis["faltante"]
        )

        st.divider()


        # SUPUESTOS

        st.markdown(
            """
            <div class="section-title">
                🔍 Supuestos e hipótesis
            </div>
            """,
            unsafe_allow_html=True
        )

        st.markdown(
            analysis["supuestos"]
        )

        st.divider()


        # RELACIONES

        st.markdown(
            """
            <div class="section-title">
                🔗 Relación con otros reportes
            </div>
            """,
            unsafe_allow_html=True
        )

        st.markdown(
            analysis["relaciones"]
        )

        st.divider()


        # OPORTUNIDAD

        st.markdown(
            """
            <div class="section-title">
                🚀 Oportunidad de producto
            </div>
            """,
            unsafe_allow_html=True
        )

        st.markdown(
            analysis["oportunidad"]
        )
# ==========================================
# EDITAR + ADJUNTAR
# ==========================================

st.markdown(
    '<div class="action-divider"></div>',
    unsafe_allow_html=True
)

edit_col, attach_col = st.columns([1, 3])


with edit_col:

    edit_mode = st.button(
        "✏️ Editar",
        use_container_width=True
    )


with attach_col:

    st.toggle(
        "Adjuntar análisis",
        key="attach_analysis",
        help=(
            "Si está activado, el envío incluirá "
            "Insights, información faltante, hipótesis, "
            "relaciones y oportunidad."
        )
    )


# ==========================================
# FORMULARIO DE EDICIÓN
# ==========================================

if edit_mode:

    st.markdown("---")

    st.markdown(
        "### ✏️ Editar Bug Report"
    )

    edited_problem = st.text_area(
        "Problema",
        value=analysis["bug"],
        height=180
    )

    edited_insights = st.text_area(
        "Insights",
        value=analysis["insights"],
        height=150
    )

    edited_supuestos = st.text_area(
        "Supuestos e hipótesis",
        value=analysis["supuestos"],
        height=150
    )

    edited_relaciones = st.text_area(
        "Relación con otros reportes",
        value=analysis["relaciones"],
        height=150
    )

    edited_oportunidad = st.text_area(
        "Oportunidad de producto",
        value=analysis["oportunidad"],
        height=150
    )

    save_col, cancel_col = st.columns(2)

    with save_col:

        if st.button(
            "Guardar cambios",
            type="primary",
            use_container_width=True
        ):

            st.session_state[analysis_key] = {
                "bug": edited_problem,
                "insights": edited_insights,
                "faltante": analysis["faltante"],
                "supuestos": edited_supuestos,
                "relaciones": edited_relaciones,
                "oportunidad": edited_oportunidad
            }

            st.success(
                "Cambios guardados correctamente."
            )

            st.rerun()

    with cancel_col:

        if st.button(
            "Cancelar",
            use_container_width=True
        ):

            st.rerun()


# ==========================================
# PDF
# ==========================================

def crear_pdf():

    buffer = BytesIO()

    doc = SimpleDocTemplate(
        buffer,
        pagesize=A4,
        rightMargin=45,
        leftMargin=45,
        topMargin=45,
        bottomMargin=45
    )

    styles = getSampleStyleSheet()

    title_style = ParagraphStyle(
        "TitleCustom",
        parent=styles["Title"],
        fontSize=24,
        leading=28,
        textColor=colors.HexColor("#17213a"),
        spaceAfter=8
    )

    subtitle_style = ParagraphStyle(
        "SubtitleCustom",
        parent=styles["Normal"],
        fontSize=10,
        textColor=colors.HexColor("#687080"),
        spaceAfter=20
    )

    section_style = ParagraphStyle(
        "SectionCustom",
        parent=styles["Heading2"],
        fontSize=15,
        leading=18,
        textColor=colors.HexColor("#17213a"),
        spaceBefore=14,
        spaceAfter=8
    )

    body_style = ParagraphStyle(
        "BodyCustom",
        parent=styles["BodyText"],
        fontSize=10,
        leading=15,
        textColor=colors.HexColor("#333b4a"),
        spaceAfter=8
    )

    small_style = ParagraphStyle(
        "SmallCustom",
        parent=styles["Normal"],
        fontSize=9,
        textColor=colors.HexColor("#687080"),
        spaceAfter=5
    )

    story = []

    story.append(
        Paragraph(
            "Alegra Insight",
            title_style
        )
    )

    story.append(
        Paragraph(
            "Bug Report generado a partir de análisis con IA",
            subtitle_style
        )
    )

    # Información del reporte

    info_data = [
        [
            Paragraph("<b>Reporte</b>", small_style),
            Paragraph(f"#{item['id']}", body_style)
        ],
        [
            Paragraph("<b>Tipo</b>", small_style),
            Paragraph(item["tipo"], body_style)
        ],
        [
            Paragraph("<b>País</b>", small_style),
            Paragraph(item["pais"], body_style)
        ],
        [
            Paragraph("<b>Urgencia</b>", small_style),
            Paragraph(item["urgencia"], body_style)
        ],
    ]

    info_table = Table(
        info_data,
        colWidths=[90, 390]
    )

    info_table.setStyle(
        TableStyle([
            (
                "BACKGROUND",
                (0, 0),
                (0, -1),
                colors.HexColor("#f1f7f7")
            ),
            (
                "BOX",
                (0, 0),
                (-1, -1),
                0.5,
                colors.HexColor("#dce5e7")
            ),
            (
                "INNERGRID",
                (0, 0),
                (-1, -1),
                0.3,
                colors.HexColor("#e5e7eb")
            ),
            (
                "VALIGN",
                (0, 0),
                (-1, -1),
                "TOP"
            ),
            (
                "LEFTPADDING",
                (0, 0),
                (-1, -1),
                10
            ),
            (
                "RIGHTPADDING",
                (0, 0),
                (-1, -1),
                10
            ),
            (
                "TOPPADDING",
                (0, 0),
                (-1, -1),
                7
            ),
            (
                "BOTTOMPADDING",
                (0, 0),
                (-1, -1),
                7
            ),
        ])
    )

    story.append(info_table)

    story.append(Spacer(1, 20))

    # Bug report

    story.append(
        Paragraph(
            "🐛 Bug Report",
            section_style
        )
    )

    story.append(
        Paragraph(
            analysis["bug"].replace("\n", "<br/>"),
            body_style
        )
    )

    # Solo adjuntar análisis si el toggle está activo

    if st.session_state.attach_analysis:

        story.append(
            Paragraph(
                "🧠 Análisis de IA",
                section_style
            )
        )

        story.append(
            Paragraph(
                "<b>Insights</b>",
                body_style
            )
        )

        story.append(
            Paragraph(
                analysis["insights"].replace(
                    "\n",
                    "<br/>"
                ),
                body_style
            )
        )

        story.append(
            Paragraph(
                "<b>Información faltante</b>",
                body_style
            )
        )

        story.append(
            Paragraph(
                analysis["faltante"].replace(
                    "\n",
                    "<br/>"
                ),
                body_style
            )
        )

        story.append(
            Paragraph(
                "<b>Supuestos e hipótesis</b>",
                body_style
            )
        )

        story.append(
            Paragraph(
                analysis["supuestos"].replace(
                    "\n",
                    "<br/>"
                ),
                body_style
            )
        )

        story.append(
            Paragraph(
                "<b>Relación con otros reportes</b>",
                body_style
            )
        )

        story.append(
            Paragraph(
                analysis["relaciones"].replace(
                    "\n",
                    "<br/>"
                ),
                body_style
            )
        )

        story.append(
            Paragraph(
                "<b>Oportunidad de producto</b>",
                body_style
            )
        )

        story.append(
            Paragraph(
                analysis["oportunidad"].replace(
                    "\n",
                    "<br/>"
                ),
                body_style
            )
        )

    doc.build(story)

    buffer.seek(0)

    return buffer


# ==========================================
# ACCIONES PRINCIPALES
# ==========================================

st.markdown(
    '<div class="action-divider"></div>',
    unsafe_allow_html=True
)

send_col, pdf_col = st.columns([1, 1])


with send_col:

    if st.button(
        "🚀 Enviar bug report",
        use_container_width=True,
        type="primary"
    ):

        if st.session_state.attach_analysis:

            st.success(
                "Bug report enviado con el análisis adjunto."
            )

        else:

            st.success(
                "Bug report enviado correctamente."
            )


with pdf_col:

    pdf_file = crear_pdf()

    st.download_button(
        label="📄 Descargar PDF",
        data=pdf_file,
        file_name=f"alegra_bug_report_{item['id']}.pdf",
        mime="application/pdf",
        use_container_width=True
    )
