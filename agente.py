import os
from dotenv import load_dotenv
from agno.agent import Agent
from agno.models.openai import OpenAI

# Carga el archivo .env si ejecutas de forma local
load_dotenv()

# Lee las variables dinámicamente (Streamlit inyecta los Secrets como variables de entorno)
base_url = os.getenv("LM_STUDIO_BASE_URL")
model_name = os.getenv("LM_STUDIO_MODEL")
api_key = os.getenv("AI_API_KEY", "lm-studio") 

# Usamos la clase OpenAI nativa pasándole la URL base y API key de Hugging Face
modelo_llm = OpenAI(
    id=model_name,
    base_url=base_url,
    api_key=api_key,
    temperature=0.6,
    max_tokens=1024,
)

def crear_agente_tutor() -> Agent:
    """
    Crea y devuelve una nueva instancia del Agente Tutor.

    Se crea una instancia nueva por cada llamada (en lugar de reutilizar un
    único objeto global) para evitar que el historial de conversación se
    acumule entre distintas consultas hechas desde Streamlit.
    """
    return Agent(
        name="Tutor IA",
        model=modelo_llm,
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
