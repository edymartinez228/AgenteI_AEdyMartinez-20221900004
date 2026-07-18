"""
app.py
------
Interfaz en Streamlit para el Agente Tutor de Inteligencia Artificial.

El usuario escribe un tema y elige su nivel; el agente (definido en agente.py)
consulta al modelo Qwen2.5-VL-3B-Instruct cargado en LM Studio y devuelve:
explicación, ejemplo práctico, analogía y pregunta de evaluación.
"""

import os
import requests
import streamlit as st
from agente import crear_agente_tutor, LM_STUDIO_BASE_URL

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


def lm_studio_disponible() -> bool:
    """Verifica si el servidor local de LM Studio está respondiendo."""
    try:
        base = LM_STUDIO_BASE_URL.rstrip("/")
        respuesta = requests.get(f"{base}/models", timeout=2)
        return respuesta.status_code == 200
    except requests.exceptions.RequestException:
        return False


with st.sidebar:
    st.subheader("Estado de LM Studio")
    if lm_studio_disponible():
        st.success("Servidor local conectado")
    else:
        st.error("No se detecta el servidor de LM Studio")
        st.caption(
            "Verifica que LM Studio esté abierto, el modelo "
            "Qwen2.5-VL-3B-Instruct cargado y el servidor iniciado "
            "en la pestaña Developer (puerto 1234)."
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
                    "No fue posible conectar con LM Studio.\n\n"
                    f"Detalle: {error}"
                )
                st.info(
                    "Revisa que LM Studio esté abierto, con el modelo cargado "
                    "y el servidor local iniciado antes de volver a intentarlo."
                )

st.divider()
st.caption(
    "Proyecto educativo con Python, Agno, Streamlit y LM Studio "
    "(modelo local Qwen2.5-VL-3B-Instruct)."
)
