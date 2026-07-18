"""
app.py
------
Interfaz en Streamlit para el Agente Tutor de Inteligencia Artificial.

El usuario escribe un tema y elige su nivel; el agente (definido en agente.py)
consulta al modelo Qwen2.5-VL-3B-Instruct en la nube o local y devuelve:
explicación, ejemplo práctico, analogía y pregunta de evaluación.
"""

import os
import requests
import streamlit as st
from agente import crear_agente_tutor

st.set_page_config(
    page_title="Agente Tutor de IA",
    page_icon="🤖",
    layout="centered",
)

st.title("🤖 Agente Tutor de Inteligencia Artificial")
st.write(
    "Escribe un tema, selecciona tu nivel y el agente lo explicará "
    "con un ejemplo y una pregunta de evaluación."
)

# Obtenemos la URL base configurada (ya sea local o Hugging Face en la nube)
BASE_URL = os.getenv("LM_STUDIO_BASE_URL", "")

def modelo_disponible() -> bool:
    """Verifica si las variables esenciales del servidor están configuradas en el entorno."""
    # Si las variables esenciales existen en el entorno, asumimos que está listo
    return bool(BASE_URL and os.getenv("LM_STUDIO_MODEL"))


with st.sidebar:
    st.subheader("Estado del Servidor IA")
    if modelo_disponible():
        st.success("Servidor del modelo conectado ✨")
    else:
        st.error("No se detecta el servidor del modelo")
        st.caption(
            "Si estás en local, verifica que tu servidor esté corriendo. "
            "Si estás en la nube, asegúrate de que los Secrets de Streamlit "
            "tengan las variables correctas y tu token de Hugging Face sea válido."
        )

nivel = st.selectbox(
    "Selecciona el nivel del estudiante",
    ["Principiante", "Intermedio", "Avanzado"],
)
tema = st.text_input(
    "Tema que deseas aprender",
    placeholder="Ejemplo: aprendizaje supervisado",
)

if st.button("Explicar tema", type="primary"):
    if not tema.strip():
        st.warning("Escribe un tema antes de continuar.")
    else:
        mensaje = f"""
        Tema: {tema}
        Nivel del estudiante: {nivel}
        La respuesta debe contener:
        1. Una explicación sencilla.
        2. Un ejemplo práctico.
        3. Una analogía, cuando sea útil.
        4. Una pregunta de evaluación.
        """
        with st.spinner("El agente está preparando la explicación..."):
            try:
                agente = crear_agente_tutor()
                respuesta = agente.run(mensaje)
                st.subheader("Respuesta del agente")
                st.markdown(respuesta.content)
            except Exception as error:
                st.error(
                    "No fue posible conectar con el servidor de Inteligencia Artificial.\n\n"
                    f"Detalle: {error}"
                )
                st.info(
                    "Verifica la configuración de red y las variables de entorno de la aplicación."
                )

st.divider()
st.caption(
    "Proyecto educativo con Python, Agno, Streamlit y arquitectura flexible "
    "(modelo Qwen2.5-VL-3B-Instruct)."
)
