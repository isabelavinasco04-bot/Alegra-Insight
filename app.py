import streamlit as st
from google import genai

# -----------------------------------
# CONFIGURACIÓN
# -----------------------------------

st.set_page_config(
    page_title="Alegra AI",
    page_icon="✦",
    layout="wide"
)

# -----------------------------------
# CONEXIÓN CON GEMINI
# -----------------------------------

client = genai.Client(
    api_key=st.secrets["GEMINI_API_KEY"]
)

# -----------------------------------
# INTERFAZ
# -----------------------------------

st.title("Alegra AI ✦")

st.write(
    "Asistente para analizar feedback de usuarios."
)

st.divider()

st.subheader("Prueba de IA")

comentario = st.text_area(
    "Ingresa un comentario de usuario",
    placeholder="Ejemplo: No me deja emitir la factura..."
)

# -----------------------------------
# ANALIZAR
# -----------------------------------

if st.button("Analizar con IA"):

    if not comentario:

        st.warning(
            "Ingresa un comentario primero."
        )

    else:

        with st.spinner(
            "Analizando con Gemini..."
        ):

            response = client.models.generate_content(
                model="gemini-3.8-flash",
                contents=f"""
Eres un asistente de Product Management
para una aplicación de facturación.

Analiza el siguiente comentario de usuario.

COMENTARIO:
{comentario}

Identifica:

1. Problema principal
2. Severidad
3. Impacto
4. Área afectada
5. Hipótesis inicial
6. Información faltante

REGLAS:

- No inventes información.
- Diferencia hechos de hipótesis.
- Si falta información escribe "Por confirmar".
- La hipótesis no debe presentarse como una conclusión definitiva.
- Sé claro y conciso.
"""
            )

        st.subheader("Análisis de IA")

        st.write(response.text)
