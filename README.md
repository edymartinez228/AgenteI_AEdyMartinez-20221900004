# Agente Tutor de Inteligencia Artificial

Proyecto educativo que implementa un agente tutor de IA capaz de explicar
temas de Inteligencia Artificial adaptando el nivel de la explicación
(Principiante, Intermedio o Avanzado). Usa **Agno** como framework de
agentes, **Streamlit** como interfaz y un modelo de lenguaje ejecutado
**localmente en LM Studio** (`Qwen2.5-VL-3B-Instruct`), sin depender de
ninguna API de pago.

## Objetivo

El estudiante escribe un tema y selecciona su nivel. El agente:

- Explica el tema de manera sencilla.
- Adapta la explicación al nivel del estudiante.
- Presenta un ejemplo práctico y, cuando resulta útil, una analogía.
- Genera una pregunta de evaluación sobre el tema.

## Estructura del proyecto

```
agente-tutor-ia/
├── app.py              # Interfaz Streamlit
├── agente.py            # Definición del agente (Agno + LM Studio)
├── requirements.txt      # Dependencias del proyecto
├── .env                  # Configuración local (modelo y URL de LM Studio)
├── .gitignore
└── README.md
```

## Requisitos

- Python 3.10 o superior.
- [LM Studio](https://lmstudio.ai/) instalado (no requiere API key ni conexión a un servicio de pago).
- Conexión a Internet solo para descargar el modelo la primera vez.

## 1. Crear y activar el entorno virtual

```bash
python -m venv .venv

# Windows
.venv\Scripts\activate

# macOS / Linux
source .venv/bin/activate
```

## 2. Instalar dependencias

```bash
pip install -r requirements.txt
```

## 3. Configurar LM Studio

1. Descarga e instala LM Studio desde <https://lmstudio.ai/>.
2. En la pestaña **Search**, busca y descarga el modelo `Qwen2.5-VL-3B-Instruct`.
3. Ve a la pestaña **Chat** (o **Local Server**) y carga el modelo descargado.
4. Ve a la pestaña **Developer** y activa **Start Server**.
   - El servidor local se inicia por defecto en `http://localhost:1234`.
   - Copia el identificador exacto del modelo que aparece en LM Studio.
5. Abre el archivo `.env` y verifica que los valores coincidan con tu instalación:

```
LM_STUDIO_MODEL=qwen2.5-vl-3b-instruct
LM_STUDIO_BASE_URL=http://localhost:1234/v1
```

> Si LM Studio muestra el modelo con otro identificador (por ejemplo
> `lmstudio-community/Qwen2.5-VL-3B-Instruct-GGUF`), reemplázalo en
> `LM_STUDIO_MODEL` para que coincida exactamente.

## 4. Ejecutar el proyecto

Antes de ejecutar, confirma que:

- LM Studio esté abierto.
- El modelo `Qwen2.5-VL-3B-Instruct` esté cargado.
- El servidor local esté iniciado (puerto `1234`).

Luego ejecuta:

```bash
streamlit run app.py
```

Abre el navegador en <http://localhost:8501>. La barra lateral de la
aplicación indica si el servidor de LM Studio está conectado.

## Cómo funciona el código

- **`agente.py`**: crea un `Agent` de Agno usando el modelo `OpenAILike`,
  apuntando al endpoint local de LM Studio (`http://localhost:1234/v1`) en
  lugar de a la API de OpenAI. Se define un conjunto de instrucciones que
  fuerzan al modelo a responder en español, adaptar el nivel y seguir una
  estructura fija (explicación, ejemplo, analogía, pregunta).
- **`app.py`**: construye la interfaz con Streamlit, arma el prompt con el
  tema y el nivel elegidos, verifica la disponibilidad del servidor de
  LM Studio y muestra la respuesta generada por el agente.

## Despliegue público (URL de Streamlit)

Streamlit Community Cloud no tiene acceso a `localhost` de tu computador, así
que para que el enlace público pueda usar tu modelo local hay que exponer el
puerto de LM Studio a Internet con un túnel (`ngrok`) y apuntar la app a esa
URL pública. Pasos:

### 1. Preparar el repositorio en GitHub

1. Sube este proyecto a un repositorio de GitHub **sin** `.venv`, `__pycache__`
   ni el archivo `.env` real (agrégalo a `.gitignore`; Streamlit Cloud usa su
   propio gestor de "Secrets", no el `.env`).
2. Asegúrate de que `requirements.txt` esté en la raíz del repositorio.

### 2. Exponer LM Studio con ngrok

1. Con LM Studio abierto, el modelo cargado y el servidor iniciado
   (puerto `1234`), instala ngrok: <https://ngrok.com/download>.
2. En una terminal, ejecuta:
   ```bash
   ngrok http 1234
   ```
3. Copia la URL pública que genera ngrok (algo como
   `https://xxxx-xxxx.ngrok-free.app`). Esa URL solo funciona mientras ngrok
   y LM Studio sigan corriendo en tu máquina.

### 3. Desplegar en Streamlit Community Cloud

1. Entra a <https://share.streamlit.io> e inicia sesión con GitHub.
2. Haz clic en **Create app** y selecciona el repositorio, la rama y
   `app.py` como archivo principal.
3. Antes de desplegar, abre **Advanced settings → Secrets** y agrega:
   ```
   LM_STUDIO_MODEL = "qwen2.5-vl-3b-instruct"
   LM_STUDIO_BASE_URL = "https://xxxx-xxxx.ngrok-free.app/v1"
   ```
   (usa la URL de ngrok del paso anterior, terminada en `/v1`).
4. Haz clic en **Deploy**. Streamlit Cloud instalará `requirements.txt` y
   levantará la app en una URL tipo `https://tu-app.streamlit.app`.
5. Verifica que `agente.py` lea primero `st.secrets` y, si no existe, el
   `.env` local (ya soportado por `os.getenv`, ya que Streamlit Cloud
   inyecta los Secrets como variables de entorno automáticamente).

### 4. Verificar el funcionamiento

- Mientras quieras que el enlace público funcione, deja LM Studio y ngrok
  abiertos en tu computador (ngrok gratuito genera una URL nueva cada vez
  que lo reinicias; si eso pasa, actualiza el Secret en Streamlit Cloud).
- Entrega el enlace `https://tu-app.streamlit.app` como URL del proyecto.

## Notas

- No se usa ninguna API key real: LM Studio no la requiere, por lo que se
  envía un valor de relleno (`"lm-studio"`).
- El modelo `Qwen2.5-VL-3B-Instruct` es multimodal (texto e imagen); en este
  proyecto se utiliza únicamente su capacidad de generación de texto.
