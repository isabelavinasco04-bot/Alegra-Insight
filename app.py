import streamlit as st

st.set_page_config(
    page_title="Alegra AI",
    page_icon="✦",
    layout="wide"
)

st.title("Alegra AI ✦")
st.write("Tu asistente para analizar feedback de usuarios.")

st.divider()

st.subheader("Prueba inicial")

comentario = st.text_area(
    "Ingresa un comentario de usuario",
    placeholder="Ejemplo: No me deja emitir la factura..."
)

if st.button("Analizar con IA"):
    if comentario:
        st.success("Comentario recibido.")
        st.write(comentario)
    else:
        st.warning("Ingresa un comentario primero.")
