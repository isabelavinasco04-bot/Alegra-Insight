import streamlit as st

st.title("Equipos")

st.write(
    "Seguimiento del estado de los reportes "
    "y trabajo de desarrolladores y diseñadores."
)

col1, col2, col3, col4 = st.columns(4)

with col1:
    st.metric("En progreso", "8")

with col2:
    st.metric("Resueltos", "5")

with col3:
    st.metric("Pendientes", "3")

with col4:
    st.metric("Necesitan revisión", "2")

st.divider()

st.subheader("Actividad del equipo")

st.write("👨‍💻 Juan — Error al emitir facturas · México")
st.write("👨‍💻 Carlos — Subir e.firma desde el celular")
st.write("🎨 Sara — Botones muy pequeños")
