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
}

h1, h2, h3 {
    color: #17213a;
}

.analysis-card {
    background-color: #ffffff;
    border: 1px solid #e5e7eb;
    border-radius: 16px;
    padding: 24px;
    margin-bottom: 18px;
}

.analysis-card:hover {
    border-color: #2fb7b5;
}

.section-title {
    color: #17213a;
    font-size: 20px;
    font-weight: 700;
    margin-bottom: 10px;
}

.label {
    color: #687080;
    font-size: 13px;
    font-weight: 600;
}

.report-original {
    background-color: #f7f8fa;
    border-left: 4px solid #2fb7b5;
    border-radius: 10px;
    padding: 18px;
    margin: 15px 0 25px 0;
}

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

</style>
""", unsafe_allow_html=True)


# ==========================================
# VERIFICAR REPORTE SELECCIONADO
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
# INFORMACIÓN DE TODOS LOS REPORTES
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
            f"Calificación: "
            f"{reporte['calificacion']}/5\n"
        )

    reportes_texto += "\n"


# ==========================================
# HEADER
# ==========================================

if st.button("← Volver al buzón"):

    st.switch_page("pages/2_Buzon.py")


st.markdown(
    """
    <div style="
        margin-top:20px;
        margin-bottom:10px;
    ">
        <h1>Análisis del reporte</h1>
        <p style="
            color:#687080;
            font-size:17px;
        ">
            Análisis generado con IA a partir del feedback disponible.
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

        <div class="label">
            {item['tipo']} · ID #{item['id']}
        </div>

        <div style="
            font-size:18px;
            color:#17213a;
            font-weight:600;
            margin-top:8px;
        ">
            {item['comentario']}
        </div>

        <div style="
            color:#687080;
            margin-top:12px;
        ">
            País: {item['pais']}
            &nbsp;&nbsp;·&nbsp;&nbsp;
            Urgencia: {item['urgencia']}
        </div>

    </div>
    """,
    unsafe_allow_html=True
)


# ==========================================
# GENERAR ANÁLISIS
# ==========================================

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

Tu tarea es analizar UN reporte específico
utilizando también el resto del feedback disponible
para encontrar patrones y relaciones.

IMPORTANTE:

- Basa las conclusiones únicamente en los datos proporcionados.
- No inventes información.
- Diferencia claramente hechos de hipótesis.
- Si un dato no está disponible, escribe "Por confirmar".
- No asumas información técnica que el reporte no menciona.
- Puedes identificar patrones entre diferentes reportes.
- Cuando relaciones reportes, menciona sus IDs.
- Sé concreta y útil para decisiones de producto.
- Responde en español.

------------------------------------------
REPORTE QUE DEBES ANALIZAR
------------------------------------------

ID: #{item['id']}
Tipo: {item['tipo']}
País: {item['pais']}
Urgencia: {item['urgencia']}
Comentario:

{item['comentario']}

------------------------------------------
TODOS LOS REPORTES DISPONIBLES
------------------------------------------

{reportes_texto}

------------------------------------------
FORMATO DE RESPUESTA
------------------------------------------

Devuelve el análisis exactamente con estas secciones:

## BUG REPORT

Explica de forma clara:

- Problema:
- Comportamiento observado:
- Impacto:
- Severidad:

Si el reporte no permite determinar alguno,
indica "Por confirmar".

## INSIGHTS

Identifica qué necesidad, frustración
o comportamiento del usuario revela este reporte.

## INFORMACIÓN FALTANTE

Indica qué información sería necesario obtener
para entender o reproducir mejor el problema.

## SUPUESTOS E HIPÓTESIS

Separa claramente las posibles explicaciones
de los hechos confirmados.

## RELACIÓN CON OTROS REPORTES

Busca otros reportes relacionados.

Para cada relación indica:

- ID del reporte relacionado.
- Por qué está relacionado.
- Qué patrón podría existir.

Si no encuentras relaciones claras,
indica "No se encontraron relaciones claras".

## OPORTUNIDAD DE PRODUCTO

Propón una oportunidad de producto basada
únicamente en lo encontrado.

No propongas una solución técnica específica
si los datos no la justifican.
"""

            response = client.models.generate_content(
                model=GEMINI_MODEL,
                contents=prompt
            )

            if response and response.text:

                analysis = response.text

                st.session_state.analysis_result = analysis

            else:

                st.error(
                    "Gemini no devolvió un análisis."
                )


        except Exception as e:

            st.error(
                "No pudimos completar el análisis "
                "en este momento."
            )

            st.caption(
                "Intenta nuevamente en unos segundos."
            )


# ==========================================
# MOSTRAR RESULTADO
# ==========================================

if "analysis_result" in st.session_state:

    st.markdown("---")

    st.markdown(
        """
        <div class="section-title">
            🧠 Análisis de IA
        </div>
        """,
        unsafe_allow_html=True
    )

    st.markdown(
        st.session_state.analysis_result
    )
