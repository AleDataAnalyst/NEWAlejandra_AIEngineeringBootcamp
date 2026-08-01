"""Interfaz Streamlit — código que genera la página web del RAG.

Idea de la UI: chat + historial, streaming, sidebar, tema
(misma línea que el miniproyecto Streamlit del bloque).

Aquí la lógica NO es un eco: cada mensaje llama a `src.logic.responder()`
(retrieval S9 + generación S10).

Ejecutar (con índice listo en ChromaDB):

  streamlit run app.py
"""

from __future__ import annotations

import time
from collections.abc import Iterator

import streamlit as st

from config import TOP_K
from src.logic import responder


def stream_palabras(texto: str, delay: float = 0.02) -> Iterator[str]:
    """Genera el texto palabra a palabra (efecto 'máquina de escribir').

    Streamlit usa este generador con `st.write_stream` para mostrar la
    respuesta de forma gradual. No cambia el contenido: solo la presentación.
    """
    for palabra in texto.split():
        yield palabra + " "
        time.sleep(delay)


def mensaje_bienvenida(nombre: str) -> dict:
    """Primer mensaje del asistente al abrir (o al limpiar) el chat.

    Devuelve un dict con la misma forma que el resto del historial
    (role, content, fuentes, contexto, error) para poder pintarlo
    con `render_mensaje` sin casos especiales.
    """
    return {
        "role": "assistant",
        "content": (
            f"Hola — soy **{nombre}**. "
            "Pregúntame sobre la agenda cultural de Madrid. "
            "Cada turno consulta el índice RAG (`src.logic.responder`); "
            "no reutilizo el hilo como contexto del modelo."
        ),
        "fuentes": [],
        "contexto": "",
        "error": False,
    }


def render_mensaje(message: dict) -> None:
    """Pinta un mensaje del historial en la UI (usuario o asistente).

    - Texto principal (o `st.error` si hubo fallo).
    - Fuentes bajo la respuesta (trazabilidad del retrieval).
    - Expander con el contexto recuperado (debug / puente con S9).
    """
    with st.chat_message(message["role"]):
        if message.get("error"):
            st.error(message["content"])
        else:
            st.markdown(message["content"])

        if message.get("fuentes"):
            st.markdown("**Fuentes**")
            for fuente in message["fuentes"]:
                st.write(f"- `{fuente}`")

        if message.get("contexto"):
            with st.expander("Contexto recuperado (debug)"):
                st.text(message["contexto"])


# --- Configuración de la página (título de la pestaña del navegador) ---
st.set_page_config(
    page_title="Agenda cultural Madrid — RAG",
    page_icon="🎭",
    layout="centered",
)

# --- Sidebar: controles que no van en el hilo del chat ---
with st.sidebar:
    st.header("Configuración")
    nombre_bot = st.text_input("Nombre del bot", value="Asistente cultural")
    # top_k se pasa a responder(); cambia cuántos chunks recupera el retriever
    top_k = st.slider("Top-K (chunks)", min_value=1, max_value=5, value=TOP_K)
    st.caption("Índice: `output/chroma_db/` (ejecuta `python main.py --prepare --index`).")
    if st.button("Limpiar chat", use_container_width=True):
        # Reinicia el historial; el modelo no “olvida” nada porque cada turno es independiente
        st.session_state.messages = [mensaje_bienvenida(nombre_bot)]
        st.rerun()

st.title(nombre_bot)
st.caption(
    "Sprint 10 · RAG con Streamlit · Demo Web"
)

# --- Historial en session_state (sobrevive a cada rerun de Streamlit) ---
if "messages" not in st.session_state:
    st.session_state.messages = [mensaje_bienvenida(nombre_bot)]

# Repintar todo el hilo en cada ejecución del script
for message in st.session_state.messages:
    render_mensaje(message)

# --- Nuevo mensaje del usuario ---
if prompt := st.chat_input("Tu pregunta sobre la agenda cultural…"):
    # 1) Guardar y mostrar la pregunta
    st.session_state.messages.append(
        {"role": "user", "content": prompt, "fuentes": [], "contexto": "", "error": False}
    )
    with st.chat_message("user"):
        st.markdown(prompt)

    # 2) Llamar al backend RAG (una pregunta → un dict; sin memoria de conversación)
    with st.chat_message("assistant"):
        with st.status("Consultando el corpus…", expanded=False) as status:
            resultado = responder(prompt, top_k=top_k)
            status.update(label="Listo", state="complete")

        if resultado.get("error"):
            # Validación, índice vacío, API, etc. → mensaje amigable
            st.error(resultado["error"])
            st.session_state.messages.append(
                {
                    "role": "assistant",
                    "content": resultado["error"],
                    "fuentes": resultado.get("fuentes") or [],
                    "contexto": resultado.get("contexto") or "",
                    "error": True,
                }
            )
        else:
            # 3) Mostrar respuesta con streaming; luego fuentes y contexto
            escrito = st.write_stream(stream_palabras(resultado["respuesta"]))
            contenido = escrito if isinstance(escrito, str) else resultado["respuesta"]

            if resultado.get("fuentes"):
                st.markdown("**Fuentes**")
                for fuente in resultado["fuentes"]:
                    st.write(f"- `{fuente}`")

            if resultado.get("contexto"):
                with st.expander("Contexto recuperado (debug)"):
                    st.text(resultado["contexto"])

            st.session_state.messages.append(
                {
                    "role": "assistant",
                    "content": contenido,
                    "fuentes": resultado.get("fuentes") or [],
                    "contexto": resultado.get("contexto") or "",
                    "error": False,
                }
            )
