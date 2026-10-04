import streamlit as st
from google import genai
from data import ALL_FEEDBACK


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
    padding-left: 4rem;
    padding-right: 4rem;
    padding-bottom: 4rem;
}


/* ------------------------------------------
   TÍTULOS
------------------------------------------ */

h1, h2, h3 {
    color: #17213a;
}


/* ------------------------------------------
   BOTONES ALEGRA
------------------------------------------ */

div.stButton > button,
div.stDownloadButton > button {

    background-color: #2fb7b5;
    color: white;

    border: 1px solid #2fb7b5;
    border-radius: 8px;

    font-weight: 600;

    transition:
        background-color 0.2s ease,
        border-color 0.2s ease,
        transform 0.2s ease;
}


div.stButton > button:hover,
div.stDownloadButton > button:hover {

    background-color: #17213a;
    border-color: #17213a;
    color: white;

    transform: translateY(-1px);
}


/* ------------------------------------------
   BOTÓN SECUNDARIO
------------------------------------------ */

.secondary-button div.stButton > button {

    background-color: white;
    color: #17213a;

    border: 1px solid #d9dee7;
}


.secondary-button div.stButton > button:hover {

    background-color: #17213a;
    color: white;

    border-color: #17213a;
}


/* ------------------------------------------
   REPORTE ORIGINAL
------------------------------------------ */

.report-original {

    background-color: #f7f9fb;

    border: 1px solid #e5e7eb;
    border-left: 4px solid #2fb7b5;

    border-radius: 12px;

    padding: 20px;

    margin-top: 20px;
    margin-bottom: 28px;
}


.report-label {

    color: #687080;

    font-size: 13px;

    font-weight: 600;

    margin-bottom: 8px;
}


.report-comment {

    color: #17213a;

    font-size: 18px;

    font-weight: 600;

    line-height: 1.5;
}


.report-meta {

    color: #687080;

    margin-top: 12px;

    font-size: 14px;
}


/* ------------------------------------------
   COLUMNAS DEL ANÁLISIS
------------------------------------------ */

.analysis-main {

    background: white;

    border: 1px solid #e3e7ed;

    border-radius: 16px;

    padding: 26px;

    min-height: 500px;

    box-shadow: 0 2px 8px rgba(23,37,84,0.03);
}


.analysis-side {

    background: white;

    border: 1px solid #e3e7ed;

    border-radius: 16px;

    padding: 22px;

    margin-bottom: 16px;

    box-shadow: 0 2px 8px rgba(23,37,84,0.03);
}


.analysis-side:hover,
.analysis-main:hover {

    border-color: #2fb7b5;

}


/* ------------------------------------------
   TÍTULOS DE SECCIÓN
------------------------------------------ */

.analysis-title {

    color: #17213a;

    font-size: 19px;

    font-weight: 700;

    margin-bottom: 16px;
}


.side-title {

    color: #17213a;

    font-size: 16px;

    font-weight: 700;

    margin-bottom: 10px;
}


/* ------------------------------------------
   BUG REPORT
------------------------------------------ */

.bug-report {

    background-color: #f8fafc;

    border-radius: 12px;

    padding: 20px;

    border: 1px solid #e5e7eb;
}


.bug-label {

    color: #687080;

    font-size: 12px;

    font-weight: 700;

    text-transform: uppercase;

    letter-spacing: 0.04em;

    margin-top: 15px;

    margin-bottom: 5px;
}


.bug-value {

    color: #17213a;

    font-size: 15px;

    line-height: 1.6;
}


/* ------------------------------------------
   ESTADO VACÍO
------------------------------------------ */

.empty-analysis {

    text-align: center;

    padding: 70px 20px;

    color: #687080;
}


/* ------------------------------------------
   DIVISOR
------------------------------------------ */

.action-bar {

    margin-top: 28px;

    padding-top: 22px;

    border-top: 1px solid #e5e7eb;
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
# HEADER
# ==========================================

if st.button("← Volver al buzón"):

    st.switch_page("pages/2_Buzon.py")


st.markdown(
    """
    <div style="margin-top:15px;">
        <h1>Análisis del reporte</h1>

        <p style="
            color:#687080;
            font-size:17px;
            margin-top:-8px;
        ">
            Convierte el feedback en un reporte accionable
            para el equipo.
        </p>
    </div>
    """,
    unsafe_allow_html=True
)


# ==========================================
# REPORTE ORIGINAL
# ==========================================

st.markdown(
    f"""
    <div class="report-original">

        <div class="report-label">
            {item['tipo']} · ID #{item['id']}
        </div>

        <div class="report-comment">
            {item['comentario']}
        </div>

        <div class="report-meta">
            País: {item['pais']}
            &nbsp;&nbsp;·&nbsp;&nbsp;
            Urgencia: {item['urgencia']}
        </div>

    </div>
    """,
    unsafe_allow_html=True
)


# ==========================================
# CONSTRUIR INFORMACIÓN DE REPORTES
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

if "analysis_result" not in st.session_state:

    st.markdown(
        """
        <div class="empty-analysis">

            <div style="
                font-size:42px;
                margin-bottom:15px;
            ">
                ✨
            </div>

            <h3>
                Genera el análisis con IA
            </h3>

            <p>
                Alegra Insight analizará este reporte,
                identificará el problema y buscará
                relaciones con otros casos.
            </p>

        </div>
        """,
        unsafe_allow_html=True
    )

    if st.button(
        "✨ Analizar reporte con IA",
        use_container_width=True
    ):

        with st.spinner(
            "Analizando reporte y buscando relaciones..."
        ):

            try:

                prompt = f"""
Eres Alegra Insight, una herramienta interna
para Product Managers de Alegra.

Analiza UN reporte específico utilizando también
el resto del feedback disponible.

IMPORTANTE:

- Basa las conclusiones únicamente en los datos proporcionados.
- No inventes información.
- Diferencia hechos de hipótesis.
- Si un dato no está disponible, escribe "Por confirmar".
- No asumas información técnica que el reporte no menciona.
- Puedes identificar patrones entre diferentes reportes.
- Cuando relaciones reportes, menciona sus IDs.
- Sé concreta y útil para decisiones de producto.
- Responde en español.

==========================================
REPORTE A ANALIZAR
==========================================

ID: #{item['id']}
Tipo: {item['tipo']}
País: {item['pais']}
Urgencia: {item['urgencia']}

Comentario:

{item['comentario']}


==========================================
RESTO DE REPORTES
==========================================

{reportes_texto}


==========================================
FORMATO
==========================================

Devuelve EXACTAMENTE estas secciones:

## BUG REPORT

Problema:
Comportamiento observado:
Impacto:
Severidad:

## INSIGHTS

Explica la necesidad, frustración o comportamiento
del usuario que revela este reporte.

## INFORMACIÓN FALTANTE

Lista la información necesaria para comprender
o reproducir mejor el problema.

## SUPUESTOS E HIPÓTESIS

Separa claramente las posibles explicaciones
de los hechos confirmados.

## RELACIÓN CON OTROS REPORTES

Identifica reportes relacionados.

Para cada relación indica:

- ID
- Motivo de la relación
- Patrón posible

Si no existen relaciones claras:
"No se encontraron relaciones claras."

## OPORTUNIDAD DE PRODUCTO

Propón una oportunidad basada únicamente
en los hallazgos.

No inventes soluciones técnicas.
"""

                response = client.models.generate_content(
                    model=GEMINI_MODEL,
                    contents=prompt
                )

                if response and response.text:

                    st.session_state.analysis_result = response.text

                    st.rerun()

                else:

                    st.error(
                        "Gemini no devolvió un análisis."
                    )

            except Exception:

                st.error(
                    "No pudimos completar el análisis "
                    "en este momento."
                )

                st.caption(
                    "Intenta nuevamente en unos segundos."
                )

    st.stop()


# ==========================================
# PROCESAR RESULTADO
# ==========================================

analysis = st.session_state.analysis_result


def get_section(text, section_name, next_sections):

    start_marker = f"## {section_name}"

    if start_marker not in text:
        return "Por confirmar."

    content = text.split(start_marker, 1)[1]

    positions = []

    for section in next_sections:

        marker = f"## {section}"

        if marker in content:

            positions.append(
                content.index(marker)
            )

    if positions:

        content = content[:min(positions)]

    return content.strip()


bug_report = get_section(
    analysis,
    "BUG REPORT",
    [
        "INSIGHTS",
        "INFORMACIÓN FALTANTE",
        "SUPUESTOS E HIPÓTESIS",
        "RELACIÓN CON OTROS REPORTES",
        "OPORTUNIDAD DE PRODUCTO"
    ]
)

insights = get_section(
    analysis,
    "INSIGHTS",
    [
        "INFORMACIÓN FALTANTE",
        "SUPUESTOS E HIPÓTESIS",
        "RELACIÓN CON OTROS REPORTES",
        "OPORTUNIDAD DE PRODUCTO"
    ]
)

info_faltante = get_section(
    analysis,
    "INFORMACIÓN FALTANTE",
    [
        "SUPUESTOS E HIPÓTESIS",
        "RELACIÓN CON OTROS REPORTES",
        "OPORTUNIDAD DE PRODUCTO"
    ]
)

supuestos = get_section(
    analysis,
    "SUPUESTOS E HIPÓTESIS",
    [
        "RELACIÓN CON OTROS REPORTES",
        "OPORTUNIDAD DE PRODUCTO"
    ]
)

relaciones = get_section(
    analysis,
    "RELACIÓN CON OTROS REPORTES",
    [
        "OPORTUNIDAD DE PRODUCTO"
    ]
)

oportunidad = get_section(
    analysis,
    "OPORTUNIDAD DE PRODUCTO",
    []
)


# ==========================================
# MOSTRAR ANÁLISIS
# ==========================================

st.markdown("---")

left, right = st.columns(
    [1.15, 1]
)


# ==========================================
# IZQUIERDA — BUG REPORT
# ==========================================

with left:

    st.markdown(
        """
        <div class="analysis-main">

            <div class="analysis-title">
                🐛 Bug report
            </div>

            <div class="bug-report">
        """,
        unsafe_allow_html=True
    )

    st.markdown(bug_report)

    st.markdown(
        """
            </div>

        </div>
        """,
        unsafe_allow_html=True
    )


# ==========================================
# DERECHA — ANÁLISIS COMPLEMENTARIO
# ==========================================

with right:

    # INSIGHTS

    st.markdown(
        """
        <div class="analysis-side">

            <div class="side-title">
                💡 Insights
            </div>
        """,
        unsafe_allow_html=True
    )

    st.markdown(insights)

    st.markdown("</div>", unsafe_allow_html=True)


    # INFORMACIÓN FALTANTE

    st.markdown(
        """
        <div class="analysis-side">

            <div class="side-title">
                🔎 Información faltante
            </div>
        """,
        unsafe_allow_html=True
    )

    st.markdown(info_faltante)

    st.markdown("</div>", unsafe_allow_html=True)


    # SUPUESTOS

    st.markdown(
        """
        <div class="analysis-side">

            <div class="side-title">
                💭 Supuestos e hipótesis
            </div>
        """,
        unsafe_allow_html=True
    )

    st.markdown(supuestos)

    st.markdown("</div>", unsafe_allow_html=True)


    # RELACIONES

    st.markdown(
        """
        <div class="analysis-side">

            <div class="side-title">
                🔗 Relación con otros reportes
            </div>
        """,
        unsafe_allow_html=True
    )

    st.markdown(relaciones)

    st.markdown("</div>", unsafe_allow_html=True)


    # OPORTUNIDAD

    st.markdown(
        """
        <div class="analysis-side">

            <div class="side-title">
                🚀 Oportunidad de producto
            </div>
        """,
        unsafe_allow_html=True
    )

    st.markdown(oportunidad)

    st.markdown("</div>", unsafe_allow_html=True)


# ==========================================
# BARRA DE ACCIONES
# ==========================================

st.markdown(
    """
    <div class="action-bar">
        <div style="
            color:#17213a;
            font-size:18px;
            font-weight:700;
            margin-bottom:15px;
        ">
            ¿Qué quieres hacer con este reporte?
        </div>
    </div>
    """,
    unsafe_allow_html=True
)


action1, action2, action3, action4 = st.columns(4)


# ==========================================
# ENVIAR BUG REPORT
# ==========================================

with action1:

    if st.button(
        "🚀 Enviar bug report",
        use_container_width=True
    ):

        st.success(
            "Bug report enviado al equipo."
        )


# ==========================================
# EDITAR
# ==========================================

with action2:

    if st.button(
        "✏️ Editar",
        use_container_width=True
    ):

        st.session_state.editing_analysis = True


# ==========================================
# ADJUNTAR ANÁLISIS
# ==========================================

with action3:

    if st.button(
        "📎 Adjuntar análisis",
        use_container_width=True
    ):

        st.success(
            "Análisis adjuntado al bug report."
        )


# ==========================================
# DESCARGAR
# ==========================================

with action4:

    download_content = f"""
ALEGRA INSIGHT
REPORTE #{item['id']}

TIPO:
{item['tipo']}

PAÍS:
{item['pais']}

URGENCIA:
{item['urgencia']}


==============================
BUG REPORT
==============================

{bug_report}


==============================
INSIGHTS
==============================

{insights}


==============================
INFORMACIÓN FALTANTE
==============================

{info_faltante}


==============================
SUPUESTOS E HIPÓTESIS
==============================

{supuestos}


==============================
RELACIÓN CON OTROS REPORTES
==============================

{relaciones}


==============================
OPORTUNIDAD DE PRODUCTO
==============================

{oportunidad}
"""

    st.download_button(
        "⬇️ Descargar",
        data=download_content,
        file_name=f"alegra_reporte_{item['id']}.txt",
        mime="text/plain",
        use_container_width=True
    )


# ==========================================
# MODO EDICIÓN
# ==========================================

if st.session_state.get("editing_analysis", False):

    st.markdown("---")

    st.subheader("Editar análisis")

    edited_analysis = st.text_area(
        "Puedes modificar el análisis antes de enviarlo.",
        value=st.session_state.analysis_result,
        height=400
    )

    col1, col2 = st.columns(2)

    with col1:

        if st.button(
            "Guardar cambios",
            type="primary",
            use_container_width=True
        ):

            st.session_state.analysis_result = edited_analysis

            st.session_state.editing_analysis = False

            st.rerun()

    with col2:

        if st.button(
            "Cancelar",
            use_container_width=True
        ):

            st.session_state.editing_analysis = False

            st.rerun()
