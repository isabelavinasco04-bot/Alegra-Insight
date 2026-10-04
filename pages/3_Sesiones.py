import streamlit as st

st.title("Subir sesión")

st.write(
    "Carga una sesión para que Alegra Insight pueda analizarla."
)

st.file_uploader(
    "Sube un audio o archivo de texto",
    type=["mp3", "wav", "m4a", "txt"]
)

st.info(
    "El análisis de sesiones con IA lo conectaremos después."
)
