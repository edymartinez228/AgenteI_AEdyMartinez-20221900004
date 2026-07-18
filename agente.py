"""
agente.py
---------
Define el Agente Tutor de Inteligencia Artificial usando el framework Agno,
conectado a un modelo ejecutado localmente en LM Studio a través de su
API compatible con OpenAI (http://localhost:1234/v1).

No se envía ninguna clave de API real: LM Studio no la requiere, por lo que
se usa un valor de relleno ("lm-studio").
"""

import os
from dotenv import load_dotenv
from agno.agent import Agent
from agno.models.openai.like import OpenAILike

# Carga las variables definidas en el archivo .env (modelo y URL local)
load_dotenv()

# Valores por defecto en caso de que el .env no los defina
LM_STUDIO_MODEL = os.getenv("LM_STUDIO_MODEL", "qwen2.5-vl-3b-instruct")
LM_STUDIO_BASE_URL = os.getenv("LM_STUDIO_BASE_URL", "http://localhost:1234/v1")


def crear_agente_tutor() -> Agent:
    """
    Crea y devuelve una nueva instancia del Agente Tutor.

    Se crea una instancia nueva por cada llamada (en lugar de reutilizar un
    único objeto global) para evitar que el historial de conversación se
    acumule entre distintas consultas hechas desde Streamlit.
    """
    return Agent(
        name="Tutor IA",
        model=OpenAILike(
            id=LM_STUDIO_MODEL,
            base_url=LM_STUDIO_BASE_URL,
            api_key="lm-studio",  # LM Studio no valida esta clave, pero el SDK la exige
            temperature=0.6,
            max_tokens=1024,
        ),
        instructions=[
            "Eres un tutor experto en Inteligencia Artificial.",
            "Responde siempre en español, con un tono claro y didáctico.",
            "Adapta el nivel de profundidad y el vocabulario al nivel del estudiante "
            "(Principiante, Intermedio o Avanzado) indicado en el mensaje.",
            "Estructura siempre la respuesta en este orden usando encabezados en markdown: "
            "1) Explicación sencilla, 2) Ejemplo práctico, 3) Analogía (si resulta útil), "
            "4) Pregunta de evaluación final.",
            "La pregunta de evaluación debe permitir comprobar si el estudiante entendió el tema.",
        ],
        markdown=True,
    )
