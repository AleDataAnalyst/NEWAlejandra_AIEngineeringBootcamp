![Cabecera](../../assets/cabecera_rag.png)

# Streamlit: desarrollo de un Frontend MVP con Python

## Objetivos

- Situar Streamlit frente a un frontend clásico (HTML/CSS/JS).
- Entender qué es, para qué sirve y cómo se estructura una app mínima.
- Saber dónde buscar en los [tutoriales oficiales](https://docs.streamlit.io/develop/tutorials) (p. ej. apps de chat/LLM).
- Capturar una entrada, llamar a una función Python y mostrar el resultado.
- Lanzar la app en local con `streamlit run`.

![Streamlit](../../assets/streamilt.svg)

---

## 1) Frontend clásico vs MVP en Python

En web «de producto», la interfaz suele construirse con **HTML** (estructura), **CSS** (estilo) y **JavaScript** (interactividad), a menudo con frameworks (React, Vue…). Eso implica otro stack, otro ciclo de build y, casi siempre, una **API** detrás.

En este curso el objetivo no es aprender el desarrollo Web frontend a medida. Para ello, necesitaríamos un curso dedicado aparte. El objetivo es montar **interfaces / MVP** con los que interactuar con nuestro software —modelos, pipelines, agentes— **sin salir de Python**.

[Streamlit](https://docs.streamlit.io/) es la herramienta elegida para eso.

---

## 2) Qué es Streamlit

Streamlit convierte un script Python en una aplicación web. Declaras widgets (`st.text_input`, `st.button`…) y la librería genera la UI. Cada interacción **vuelve a ejecutar** el script de arriba abajo (modelo mental importante).

Instalación típica:

```bash
pip install streamlit
streamlit run app.py
```

Tras esto, se puede abrir una URL local en el navegador (por defecto `http://localhost:8501`). Podrías visualizar en tu equipo local la web que estás desarrollando.

---

## 3) Por qué Streamlit (y para qué)

**Por qué Streamlit es la opción elegida**

- Encaja con el stack Python del módulo.
- Pocas líneas hasta una demo compartible en local.
- Suficiente para enseñar separación UI vs lógica.
- No exige HTML/CSS/JS propio.

**Para qué se usa fuera del aula**

- Demos de modelos ML o de chat/LLM.
- Herramientas internas (formularios sobre un pipeline).
- Prototipos rápidos antes de un producto con API + front.

No es la única opción del mercado: hay más herramientas como Gradio, entre otras.
---

## 4) Widgets: componentes web de Streamlit

Los widgets son los elementos que se muestran en la interfaz y que el usuario puede interactuar con ellos. Si quieres algún widget, basta con copiar el código de ejemplo y adaptarlo a tus necesidades. Puedes revisar la documentación oficial de los widgets para ver los disponibles:

[Widgets de Streamlit](https://docs.streamlit.io/library/api-reference/widgets)


| Widget | Uso habitual |
|--------|----------------|
| `st.set_page_config` / `st.title` | Título y layout de la página |
| `st.text_input` | Texto libre (pregunta, prompt…) |
| `st.chat_input` / `st.chat_message` | Variante estilo chat |
| `st.spinner` | Feedback mientras corre el backend |
| `st.markdown` / `st.write` | Mostrar el resultado |
| `st.error` | Errores amigables |
| `st.expander` | Detalle u opción debug |
| `st.sidebar` | Controles secundarios |

No hace falta memorizarlos todos: con input + llamada a función + salida ya tienes un MVP. Cuando necesites algo en específico, puedes leer la documentación oficial.

---

## 5) Tutoriales oficiales: dónde buscar

Streamlit publica tutoriales por tipo de app en [Develop → Tutorials](https://docs.streamlit.io/develop/tutorials): chat/LLM, datos, theming, multipágina, execution model, etc. No hace falta aprenderlos todos; sí saber **dónde mirar** cuando necesites un patrón.

### Apps de chat y LLMs

Si tu interfaz es del tipo pregunta–respuesta (o un asistente), el bloque más útil del índice es [Chat and LLM apps](https://docs.streamlit.io/develop/tutorials/chat-and-llm-apps/build-conversational-apps), en concreto [Build a basic LLM chat app](https://docs.streamlit.io/develop/tutorials/chat-and-llm-apps/build-conversational-apps).

Ahí verás:

- widgets de chat (`st.chat_message`, `st.chat_input`);
- ejemplos de app conversacional paso a paso;
- cómo guardar el historial de mensajes (cuando lo necesites).

Puedes **reutilizar el patrón de la interfaz** y conectar tu propia función de negocio (`responder()`, `predict()`, etc.) en lugar del ejemplo de la documentación. Empieza por una app sencilla (una pregunta, una respuesta) y amplía con la doc cuando quieras más turnos o más detalles de UI.

---

## 6) Partes de una app mínima con Streamlit

Antes del miniproyecto de chat, conviene ver **cómo se monta una app por piezas**. El patrón es siempre el mismo: cabecera → entrada → función de lógica → salida. El proyecto RAG del sprint usa este esquema con `text_input` (no hace falta chat).

### Instalación

```bash
python -m venv .venv
source .venv/bin/activate          # Git Bash / macOS / Linux
# .venv\Scripts\Activate.ps1       # Windows PowerShell

pip install streamlit
streamlit --version
```

### Carpeta y script

Por convención el script de entrada se llama `app.py`:

```text
mi_demo_streamlit/
└── app.py
```

```bash
mkdir mi_demo_streamlit
cd mi_demo_streamlit
```

### Pieza A — Cabecera

```python
import streamlit as st

st.set_page_config(page_title="Mi demo", layout="centered")
st.title("Mi demo")
st.caption("MVP con Streamlit")
```

```bash
streamlit run app.py
```

Se abre `http://localhost:8501`. Al guardar, Streamlit suele recargar solo.

### Pieza B — Entrada del usuario

```python
entrada = st.text_input("Escribe tu petición")
```

### Pieza C — Función de lógica (simulada)

La UI no implementa el modelo: **llama** a una función.

```python
def mi_funcion(texto: str) -> dict:
    """Sustituye esto luego por tu backend real."""
    if not texto.strip():
        return {"error": "Escribe algo en el campo de texto.", "respuesta": None}
    return {"error": None, "respuesta": f"Has escrito: {texto}"}
```

### Pieza D — Conectar input → función → salida

```python
if entrada:
    with st.spinner("Procesando..."):
        resultado = mi_funcion(entrada)

    if resultado.get("error"):
        st.error(resultado["error"])
    else:
        st.subheader("Resultado")
        st.markdown(resultado["respuesta"])
```

### Script completo de referencia

```python
import streamlit as st


def mi_funcion(texto: str) -> dict:
    if not texto.strip():
        return {"error": "Escribe algo en el campo de texto.", "respuesta": None}
    return {"error": None, "respuesta": f"Has escrito: {texto}"}


st.set_page_config(page_title="Mi demo", layout="centered")
st.title("Mi demo")
st.caption("MVP con Streamlit")

entrada = st.text_input("Escribe tu petición")

if entrada:
    with st.spinner("Procesando..."):
        resultado = mi_funcion(entrada)

    if resultado.get("error"):
        st.error(resultado["error"])
    else:
        st.subheader("Resultado")
        st.markdown(resultado["respuesta"])
```

Con esto ya entiendes las **partes**. El siguiente apartado es un miniproyecto listo para ejecutar, con chat (historial, streaming y sidebar).

---

## 7) Miniproyecto chat Streamlit (para ejecutar)

Demo corta de chat (historial + streaming + sidebar mínima), inspirada en [Build a basic LLM chat app](https://docs.streamlit.io/develop/tutorials/chat-and-llm-apps/build-conversational-apps) para entender una web sencilla montada con Streamlit.

📁 [`06_miniproyecto_streamlit/`](./06_miniproyecto_streamlit/)

### Paso 0 — Instalación y arranque

```bash
cd 06_miniproyecto_streamlit
python -m venv .venv
source .venv/bin/activate          # Git Bash / macOS / Linux
# .venv\Scripts\Activate.ps1       # Windows PowerShell

pip install -r requirements.txt
streamlit run app.py
```

Abre `http://localhost:8501`. Solo hace falta `app.py` (+ `requirements.txt`).

### Paso 1: chat + historial

Escribe varios mensajes. El hilo se guarda en `st.session_state.messages` y se vuelve a pintar en cada rerun.

En el código: `st.chat_input`, `st.chat_message` y el bucle sobre el historial.

### Paso 2: streaming

La respuesta del asistente aparece palabra a palabra con `st.write_stream` y un generador (`stream_palabras`). La “inteligencia” es local (frase de plantilla + eco): el objetivo es practicar la UI, no el modelo.

### Paso 3: sidebar mínima

En la barra lateral: cambia el **nombre del bot** (el título se actualiza) y usa **Limpiar chat** para reiniciar el hilo con un mensaje de bienvenida.

### Paso 4: Estilos (tema)

Los colores están en `.streamlit/config.toml` (no en `app.py`). Cambia `primaryColor`, guarda y recarga. Docs: [configuration / theming](https://docs.streamlit.io/develop/concepts/configuration).

### Qué llevarte al proyecto RAG

| Aquí | Proyecto RAG |
|------|----------------|
| Chat multi-turno + historial | Suele bastar 1 pregunta → 1 respuesta |
| Streaming de texto | Respuesta + **fuentes** + expander debug |
| Sidebar simple | Controles opcionales (p. ej. Top-K) |

Para más patrones (feedback, LLM real…), sigue el [tutorial oficial](https://docs.streamlit.io/develop/tutorials/chat-and-llm-apps/build-conversational-apps) por tu cuenta.

---

## 8) Proyecto RAG de este sprint (misma UI, otro backend)

La demo ejecutable está en [`05_proyecto_rag_aplicacion/`](./05_proyecto_rag_aplicacion/). Reutiliza el patrón del [miniproyecto chat](./06_miniproyecto_streamlit/) y sustituye el eco por `logic.responder()`:

```python
# Idea central (ver app.py completo en el proyecto)
resultado = responder(pregunta, top_k=top_k)  # from src.logic import responder

# En el mensaje del asistente:
# - streaming del texto de resultado["respuesta"]
# - lista de resultado["fuentes"]
# - expander con resultado["contexto"]
# - st.error si resultado["error"]
```

| Miniproyecto chat | Proyecto RAG |
|-------------------|--------------|
| `mi_funcion` / eco local | `logic.responder()` (retrieve + generate) |
| Sin fuentes | Fuentes + contexto debug |
| Sidebar: nombre + limpiar | + Top-K |
| Tema en `.streamlit/config.toml` | El mismo enfoque |

Layout mental:

```text
┌─────────────────────────────────────┐
│  Sidebar: nombre · Top-K · limpiar  │
│  Título                             │
│  [ historial chat …………… ]           │
│  Respuesta (+ streaming)            │
│  Fuentes                            │
│  ▸ Contexto recuperado (debug)      │
│  [________ chat_input ________]     │
└─────────────────────────────────────┘
```

Detalle de fuentes/errores: [documento 3](./03_mostrar_fuentes_estado_y_errores.md). Contrato backend: [De script a aplicación](./02_de_script_a_aplicacion.md).

---

## 9) Ejecución en local

Desde la carpeta del proyecto (donde está `app.py`):

```bash
cd 05_proyecto_rag_aplicacion
source .venv/bin/activate   # o Activate.ps1 en Windows
streamlit run app.py
```

`app.py` debe poder importar la lógica (`from src.logic import responder`). Variables sensibles (p. ej. `GEMINI_API_KEY`) van en `.env`, no en el código de la UI.

---

## 10) Despliegue en cloud

En local basta `streamlit run`. Para compartir fuera de tu máquina existen opciones como [Streamlit Community Cloud](https://streamlit.io/cloud) o un servidor propio. En cualquier caso: **secretos fuera del repo** y el mismo contrato de backend que uses en local.

No es obligatorio desplegar en este sprint; sí entender que el MVP local es el primer paso.

---

## 11) Referencias

**Punto de entrada:** [Tutorials](https://docs.streamlit.io/develop/tutorials) — índice de todos los tutoriales por tema.

**Más cercanos a este sprint:**

- [Chat and LLM apps → Build a basic LLM chat app](https://docs.streamlit.io/develop/tutorials/chat-and-llm-apps/build-conversational-apps) — widgets de chat, sesión, streaming (adaptar el backend a tu función).
- [Get started](https://docs.streamlit.io/get-started) — instalación y primera app.
- [API reference · widgets](https://docs.streamlit.io/library/api-reference/widgets) — catálogo de componentes.

**Otros tutoriales del índice** (cuando los necesites): datos, theming, multipágina, execution model, componentes custom — todos desde la misma [página de Tutorials](https://docs.streamlit.io/develop/tutorials).

**Ejemplo ML genérico (fuera de docs oficiales):** [Deploy a machine learning model using Streamlit (GeeksforGeeks)](https://www.geeksforgeeks.org/machine-learning/deploy-a-machine-learning-model-using-streamlit-library/).

---

## Resumen

- Frontend clásico = HTML/CSS/JS; aquí el foco es MVP con Streamlit en Python.
- Proyecto RAG del sprint: UI simple sobre `responder()` + fuentes.
- Más patrones: tutoriales de [Chat and LLM apps](https://docs.streamlit.io/develop/tutorials/chat-and-llm-apps/build-conversational-apps).
