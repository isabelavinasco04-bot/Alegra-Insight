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

# Modelo disponible para proyectos nuevos
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

/* TITULOS */

h1, h2, h3 {
    color: #17213a;
}


/* BOTONES ALEGRA */

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


/* TARJETAS */

.analysis-box {
    background-color: #ffffff;
    border: 1px solid #e5e7eb;
    border-radius: 16px;
    padding: 24px;
    margin-bottom: 18px;
}


/* BUG REPORT */

.bug-box {
    background-color: #f8fafc;
    border: 1px solid #dfe5eb;
    border-left: 5px solid #2fb7b5;
    border-radius: 16px;
    padding: 28px;
}


/* TITULO DE SECCION */

.section-title {
    font-size: 20px;
    font-weight: 700;
    color: #17213a;
    margin-bottom: 14px;
}


/* REPORTE ORIGINAL */

.original-box {
    background-color: #f7f8fa;
    border-radius: 12px;
    padding: 18px;
    margin-bottom: 25px;
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
# BOTÓN VOLVER
# ==========================================

if st.button("← Volver al buzón"):

    st.switch_page("pages/2_Buzon.py")


# ==========================================
# HEADER
# ==========================================

st.title("Análisis del reporte")

st.caption(
    "Alegra Insight analiza el reporte, identifica el problema "
    "y encuentra posibles relaciones con otros casos."
)


# ==========================================
# REPORTE ORIGINAL
# ==========================================

with st.container(border=True):

    st.markdown("### Reporte seleccionado")

    st.caption(
        f"{item['tipo']} · ID #{item['id']} · {item['pais']}"
    )

    st.markdown(
        f"**{item['comentario']}**"
    )

    st.caption(
        f"Urgencia: {item['urgencia']}"
    )


# ==========================================
# PREPARAR INFORMACIÓN DE TODOS LOS REPORTES
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
# GENERAR ANÁLISIS AUTOMÁTICAMENTE
# ==========================================

analysis_key = f"analysis_{item['id']}"


if analysis_key not in st.session_state:

    with st.spinner(
        "✨ Analizando el reporte y buscando relaciones..."
    ):

        try:

            prompt = f"""
Eres Alegra Insight, una herramienta interna
para Product Managers de Alegra.

Analiza el reporte seleccionado utilizando
también el resto del feedback disponible.

REGLAS IMPORTANTES:

- No inventes información.
- Diferencia hechos de hipótesis.
- Si falta información escribe "Por confirmar".
- Busca relaciones reales entre reportes.
- Cuando encuentres una relación menciona el ID.
- Sé concreta.
- El resultado debe ser útil para un Product Manager.
- Responde en español.

==========================================
REPORTE SELECCIONADO
==========================================

ID: #{item['id']}
Tipo: {item['tipo']}
País: {item['pais']}
Urgencia: {item['urgencia']}

Comentario:
{item['comentario']}

==========================================
OTROS REPORTES DISPONIBLES
==========================================

{reportes_texto}

==========================================
FORMATO
==========================================

Devuelve exactamente estas secciones:

BUG REPORT

Problema:
Describe claramente el problema.

Comportamiento observado:
Describe qué está ocurriendo.

Comportamiento esperado:
Indica qué debería ocurrir.
Si no se puede determinar: Por confirmar.

Impacto:
Explica el impacto para el usuario o negocio.

Severidad:
Alta, Media o Baja.
Explica brevemente por qué.

INFORMACIÓN FALTANTE

Lista la información que sería necesaria
para comprender o reproducir el problema.

SUPUESTOS E HIPÓTESIS

Separa claramente posibles explicaciones
de los hechos confirmados.

RELACIÓN CON OTROS REPORTES

Identifica reportes relacionados.

Para cada relación indica:

ID:
Por qué está relacionado:
Patrón posible:

Si no existen relaciones claras:
No se encontraron relaciones claras.

INSIGHTS

Explica qué necesidad, frustración,
comportamiento o oportunidad del usuario
revela este reporte.

OPORTUNIDAD DE PRODUCTO

Describe una oportunidad de producto
basada únicamente en la evidencia encontrada.

No propongas soluciones técnicas específicas
si los datos no las justifican.
"""

            response = client.models.generate_content(
                model=GEMINI_MODEL,
                contents=prompt
            )

            if response and response.text:

                st.session_state[analysis_key] = response.text

            else:

                st.error(
                    "Gemini no devolvió contenido."
                )

                st.stop()

        except Exception as e:

            st.error(
                "No pudimos completar el análisis."
            )

            st.caption(
                "Revisa la conexión con Gemini o intenta nuevamente."
            )

            # Útil mientras estamos desarrollando
            st.code(str(e))

            st.stop()


analysis = st.session_state[analysis_key]


# ==========================================
# SEPARAR EL BUG REPORT DEL RESTO
# ==========================================

def get_section(text, title, next_titles):

    start = text.find(title)

    if start == -1:
        return "Por confirmar."

    start += len(title)

    end = len(text)

    for next_title in next_titles:

        position = text.find(next_title, start)

        if position != -1 and position < end:
            end = position

    return text[start:end].strip()


bug_report = get_section(
    analysis,
    "BUG REPORT",
    [
        "INFORMACIÓN FALTANTE",
        "SUPUESTOS E HIPÓTESIS",
        "RELACIÓN CON OTROS REPORTES",
        "INSIGHTS",
        "OPORTUNIDAD DE PRODUCTO"
    ]
)

informacion_faltante = get_section(
    analysis,
    "INFORMACIÓN FALTANTE",
    [
        "SUPUESTOS E HIPÓTESIS",
        "RELACIÓN CON OTROS REPORTES",
        "INSIGHTS",
        "OPORTUNIDAD DE PRODUCTO"
    ]
)

supuestos = get_section(
    analysis,
    "SUPUESTOS E HIPÓTESIS",
    [
        "RELACIÓN CON OTROS REPORTES",
        "INSIGHTS",
        "OPORTUNIDAD DE PRODUCTO"
    ]
)

relaciones = get_section(
    analysis,
    "RELACIÓN CON OTROS REPORTES",
    [
        "INSIGHTS",
        "OPORTUNIDAD DE PRODUCTO"
    ]
)

insights = get_section(
    analysis,
    "INSIGHTS",
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
# RESULTADO
# ==========================================

st.markdown("---")

st.markdown("## Resultado del análisis")


# ==========================================
# DOS COLUMNAS
# ==========================================

left, right = st.columns([1.15, 1])


# ==========================================
# IZQUIERDA — BUG REPORT
# ==========================================

with left:

    st.markdown(
        '<div class="section-title">🐛 Bug Report</div>',
        unsafe_allow_html=True
    )

    with st.container(border=True):

        st.markdown(bug_report)


# ==========================================
# DERECHA — ANÁLISIS
# ==========================================

with right:

    st.markdown(
        '<div class="section-title">🧠 Análisis de IA</div>',
        unsafe_allow_html=True
    )

    with st.container(border=True):

        st.markdown("### 💡 Insights")

        st.markdown(insights)

    with st.container(border=True):

        st.markdown("### 🔎 Supuestos e hipótesis")

        st.markdown(supuestos)

    with st.container(border=True):

        st.markdown("### 🔗 Relación con otros reportes")

        st.markdown(relaciones)

    with st.container(border=True):

        st.markdown("### 📋 Información faltante")

        st.markdown(informacion_faltante)


# ==========================================
# OPORTUNIDAD
# ==========================================

st.markdown("---")

with st.container(border=True):

    st.markdown("### 🚀 Oportunidad de producto")

    st.markdown(oportunidad)


# ==========================================
# ACCIONES
# ==========================================

st.markdown("---")

st.markdown("### Acciones")

col1, col2, col3, col4 = st.columns(4)


# ==========================================
# ENVIAR BUG REPORT
# ==========================================

with col1:

    if st.button(
        "🐛 Enviar bug report",
        use_container_width=True
    ):

        st.success(
            "Bug report enviado al equipo."
        )


# ==========================================
# EDITAR
# ==========================================

with col2:

    if st.button(
        "✏️ Editar",
        use_container_width=True
    ):

        st.session_state.editing_report = True


# ==========================================
# ADJUNTAR ANÁLISIS
# ==========================================

with col3:

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

with col4:

    st.download_button(
        "⬇️ Descargar",
        data=analysis,
        file_name=f"analisis_reporte_{item['id']}.txt",
        mime="text/plain",
        use_container_width=True
    )


# ==========================================
# EDITOR
# ==========================================

if st.session_state.get("editing_report", False):

    st.markdown("---")

    st.markdown("### Editar Bug Report")

    edited_bug = st.text_area(
        "Puedes modificar el reporte antes de enviarlo.",
        value=bug_report,
        height=300
    )

    col1, col2 = st.columns(2)

    with col1:

        if st.button(
            "Guardar cambios",
            type="primary",
            use_container_width=True
        ):

            st.session_state.edited_bug_report = edited_bug
            st.session_state.editing_report = False

            st.success(
                "Cambios guardados."
            )

            st.rerun()

    with col2:

        if st.button(
            "Cancelar",
            use_container_width=True
        ):

            st.session_state.editing_report = False
            st.rerun()
