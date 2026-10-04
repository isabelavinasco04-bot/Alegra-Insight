import streamlit as st
from google import genai


# ==========================================
# CONEXIÓN CON GEMINI
# ==========================================

client = genai.Client(
    api_key=st.secrets["GEMINI_API_KEY"]
)

GEMINI_MODEL = "gemini-3.8-flash"


# ==========================================
# SUBIR SESIÓN
# ==========================================

st.title("Subir sesión")

st.write(
    "Carga una sesión para que Alegra Insight pueda "
    "transcribirla y convertirla en información accionable."
)


# ==========================================
# ESTADO
# ==========================================

if "sessions" not in st.session_state:
    st.session_state.sessions = []


# ==========================================
# SUBIR ARCHIVO
# ==========================================

archivo = st.file_uploader(
    "Sube un audio o archivo de texto",
    type=["mp3", "wav", "m4a", "txt"]
)


# ==========================================
# ARCHIVO CARGADO
# ==========================================

if archivo is not None:

    if archivo.type and archivo.type.startswith("audio"):
        st.audio(archivo)

    st.write(
        f"Archivo: **{archivo.name}**"
    )


    # ==========================================
    # PROCESAR SESIÓN
    # ==========================================

    if st.button(
        "✨ Procesar sesión",
        type="primary",
        use_container_width=True
    ):

        with st.spinner(
            "Analizando la sesión con IA..."
        ):

            try:

                # --------------------------------------
                # CASO AUDIO
                # --------------------------------------

                if archivo.type and archivo.type.startswith("audio"):

                    mime_types = {
                        "mp3": "audio/mpeg",
                        "wav": "audio/wav",
                        "m4a": "audio/mp4"
                    }

                    extension = (
                        archivo.name
                        .lower()
                        .split(".")[-1]
                    )

                    mime_type = mime_types.get(
                        extension,
                        archivo.type or "audio/mpeg"
                    )

                    archivo_subido = client.files.upload(
                        file=archivo,
                        config={
                            "mime_type": mime_type
                        }
                    )

                    prompt = """
Analiza esta sesión de usuario de Alegra.

Primero transcribe la conversación de forma clara.

Después genera una ficha estructurada con:

1. RESUMEN
Un resumen breve de la conversación.

2. NECESIDAD PRINCIPAL
¿Qué necesitaba o intentaba lograr el usuario?

3. PROBLEMAS IDENTIFICADOS
¿Qué problemas, frustraciones o dificultades menciona?

4. SENTIMIENTO
Indica el sentimiento predominante del usuario.

5. OPORTUNIDADES
¿Qué oportunidades de producto o experiencia aparecen?

6. TEMAS
Enumera los principales temas mencionados.

7. TRANSCRIPCIÓN
Incluye la transcripción completa de la sesión.

Sé concreto y útil para un equipo de producto.
No inventes información que no aparezca en la conversación.

Devuelve la respuesta usando exactamente estas etiquetas:

RESUMEN:
NECESIDAD PRINCIPAL:
PROBLEMAS IDENTIFICADOS:
SENTIMIENTO:
OPORTUNIDADES:
TEMAS:
TRANSCRIPCIÓN:
"""

                    respuesta = client.models.generate_content(
                        model=GEMINI_MODEL,
                        contents=[
                            archivo_subido,
                            prompt
                        ]
                    )


                # --------------------------------------
                # CASO ARCHIVO DE TEXTO
                # --------------------------------------

                else:

                    texto = archivo.getvalue().decode(
                        "utf-8",
                        errors="ignore"
                    )

                    prompt = f"""
Analiza la siguiente transcripción de una sesión
de usuario de Alegra.

TRANSCRIPCIÓN:

{texto}

Genera una ficha estructurada con:

1. RESUMEN
2. NECESIDAD PRINCIPAL
3. PROBLEMAS IDENTIFICADOS
4. SENTIMIENTO
5. OPORTUNIDADES
6. TEMAS
7. TRANSCRIPCIÓN

No inventes información.

Usa exactamente estas etiquetas:

RESUMEN:
NECESIDAD PRINCIPAL:
PROBLEMAS IDENTIFICADOS:
SENTIMIENTO:
OPORTUNIDADES:
TEMAS:
TRANSCRIPCIÓN:
"""

                    respuesta = client.models.generate_content(
                        model=GEMINI_MODEL,
                        contents=prompt
                    )


                # ======================================
                # GUARDAR RESULTADO
                # ======================================

                texto_generado = respuesta.text

                nuevo_id = (
                    1000
                    + len(st.session_state.sessions)
                    + 1
                )

                nueva_sesion = {
                    "id": nuevo_id,
                    "tipo": "Sesión con cliente",
                    "pais": "Por confirmar",
                    "urgencia": "Media",

                    "comentario": (
                        "Sesión analizada con IA. "
                        + texto_generado[:300]
                    ),

                    "transcripcion": texto_generado,

                    "analisis_sesion": texto_generado,

                    "archivo": archivo.name,

                    "estado": "Sin analizar"
                }


                st.session_state.sessions.append(
                    nueva_sesion
                )


                # --------------------------------------
                # GUARDAR PARA EL BUZÓN
                # --------------------------------------

                st.session_state.uploaded_session = (
                    nueva_sesion
                )


                # ======================================
                # RESULTADO
                # ======================================

                st.success(
                    "✓ Tu sesión ya está subida y disponible en el buzón."
                )

                st.info(
                    "La IA transcribió y estructuró la sesión. "
                    "Ahora puedes encontrarla en el Buzón."
                )


                # --------------------------------------
                # MOSTRAR FICHA
                # --------------------------------------

                with st.expander(
                    "Ver ficha generada por IA"
                ):

                    st.write(
                        texto_generado
                    )


            except Exception as e:

                st.error(
                    "No se pudo procesar la sesión."
                )

                st.caption(
                    f"Detalle técnico: {e}"
                )
