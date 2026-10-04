import streamlit as st


# ==========================================
# SUBIR SESIÓN
# ==========================================

st.title("Subir sesión")

st.write(
    "Carga una sesión para que Alegra Insight pueda analizarla."
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

    st.write(f"Archivo: {archivo.name}")


    # ==========================================
    # PROCESAR
    # ==========================================

    if st.button(
        "✨ Procesar sesión",
        type="primary",
        use_container_width=True
    ):

        st.session_state.sessions.append(
            {
                "id": len(st.session_state.sessions) + 1,
                "tipo": "Sesión",
                "pais": "Por confirmar",
                "urgencia": "Por confirmar",
                "comentario": (
                    "Sesión cargada correctamente. "
                    "La transcripción será analizada con IA."
                ),
                "transcripcion": (
                    "Sesión cargada correctamente. "
                    "La transcripción será analizada con IA."
                ),
                "archivo": archivo.name,
                "estado": "Pendiente"
            }
        )

        st.success(
            "✓ Tu sesión ya está subida y disponible en el buzón."
        )

        st.info(
            "La sesión quedó lista para analizar con IA."
        )
