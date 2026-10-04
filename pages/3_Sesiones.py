import streamlit as st
from datetime import datetime


# ==========================================
# CONFIGURACIÓN
# ==========================================

st.title("Subir sesión")

st.write(
    "Carga una sesión para que Alegra Insight pueda analizarla."
)


# ==========================================
# ESTADO DE SESIONES
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
# PROCESAR SESIÓN
# ==========================================

if archivo is not None:

    if archivo.type and archivo.type.startswith("audio"):
    st.audio(archivo)


    if st.button(
        "✨ Procesar sesión",
        type="primary",
        use_container_width=True
    ):

        with st.spinner("Analizando sesión con IA..."):

            # ----------------------------------
            # TRANSCRIPCIÓN
            # ----------------------------------

            if archivo.type == "text/plain":

                transcripcion = archivo.read().decode(
                    "utf-8"
                )

            else:

                # Para el prototipo simulamos
                # la transcripción del audio.

                transcripcion = (
                    "El usuario comenta que tuvo "
                    "dificultades utilizando la aplicación "
                    "móvil y que encontró fricción durante "
                    "el flujo principal."
                )


            # ----------------------------------
            # CREAR SESIÓN
            # ----------------------------------

            nueva_sesion = {

                "id": len(st.session_state.sessions) + 1,

                "tipo": "Sesión",

                "pais": "Por confirmar",

                "urgencia": "Por confirmar",

                "comentario": transcripcion,

                "transcripcion": transcripcion,

                "archivo": archivo.name,

                "fecha": datetime.now().strftime(
                    "%d/%m/%Y %H:%M"
                ),

                "estado": "Pendiente"

            }


            # ----------------------------------
            # GUARDAR
            # ----------------------------------

            st.session_state.sessions.append(
                nueva_sesion
            )


            # ----------------------------------
            # CONFIRMACIÓN
            # ----------------------------------

            st.success(
                "✓ Tu sesión ya está subida y "
                "disponible en el buzón."
            )


            st.info(
                "La sesión fue transcrita y quedó "
                "lista para analizar con IA."
            )


            # ----------------------------------
            # MOSTRAR FICHA
            # ----------------------------------

            st.markdown(
                f"""
                <div style="
                    border:1px solid #dce2e8;
                    border-radius:12px;
                    padding:20px;
                    margin-top:20px;
                    background:white;
                ">

                    <div style="
                        color:#687080;
                        font-size:12px;
                        font-weight:700;
                        text-transform:uppercase;
                        margin-bottom:8px;
                    ">
                        Sesión
                    </div>

                    <div style="
                        color:#17213a;
                        font-size:20px;
                        font-weight:700;
                        margin-bottom:8px;
                    ">
                        Sesión #{len(st.session_state.sessions)}
                    </div>

                    <div style="
                        color:#687080;
                        font-size:13px;
                        margin-bottom:14px;
                    ">
                        {archivo.name}
                        · {datetime.now().strftime("%d/%m/%Y")}
                    </div>

                    <div style="
                        color:#333b4a;
                        font-size:14px;
                        line-height:1.6;
                    ">
                        {transcripcion[:400]}
                        {"..." if len(transcripcion) > 400 else ""}
                    </div>

                </div>
                """,
                unsafe_allow_html=True
            )
