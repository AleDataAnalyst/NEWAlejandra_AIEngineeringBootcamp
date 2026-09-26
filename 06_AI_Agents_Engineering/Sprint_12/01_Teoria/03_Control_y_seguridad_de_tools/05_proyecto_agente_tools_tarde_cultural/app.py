"""App Streamlit — chat con tools (cliente UI).

  streamlit run app.py

Dos memorias en session_state (no confundirlas):
  - messages     → lo que se ve en el chat
  - agent_state  → dict interno (preferencias, plan, done, traza)
"""

from __future__ import annotations

import streamlit as st

import config
from src.agent import procesar_turno
from src.state import crear_estado

# --- Página ---
st.set_page_config(
    page_title="Agente tools · tarde cultural",
    page_icon="🛠️",
    layout="centered",
)

# --- Sidebar: límites y reset ---
with st.sidebar:
    st.header("Configuración")
    max_turns = st.slider(
        "max_turns",
        min_value=1,
        max_value=12,
        value=config.MAX_TURNS_DEFAULT,
    )
    max_steps = st.slider(
        "max_steps (tools)",
        min_value=1,
        max_value=12,
        value=config.MAX_STEPS_DEFAULT,
    )
    st.caption("max_turns = mensajes de usuario · max_steps = vueltas de tools por turno.")
    if st.button("Nueva conversación", use_container_width=True):
        # Reinicia chat + estado del agente
        st.session_state.messages = [
            {
                "role": "assistant",
                "content": (
                    "Hola — planifico tardes culturales con tools "
                    "(guía RAG, eventos Madrid, hora). "
                    "Cuéntame intereses, presupuesto y zona."
                ),
            }
        ]
        st.session_state.agent_state = crear_estado("")
        st.rerun()

# --- Cabecera ---
st.title("Agente · tools · tarde cultural")
st.caption("Sprint 12 — function calling + allowlist + max_steps + Streamlit")

# --- Init de session_state (solo la primera vez) ---
if "messages" not in st.session_state:
    st.session_state.messages = [
        {
            "role": "assistant",
            "content": (
                "Hola — planifico tardes culturales con tools "
                "(guía RAG, eventos Madrid, hora). "
                "Cuéntame intereses, presupuesto y zona."
            ),
        }
    ]
if "agent_state" not in st.session_state:
    st.session_state.agent_state = crear_estado("")

# --- Pintar historial del chat ---
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# --- ¿Se puede seguir escribiendo? ---
estado = st.session_state.agent_state
chat_bloqueado = bool(estado.get("done") or estado.get("error"))
turnos_hechos = len(estado.get("traza") or [])

if chat_bloqueado:
    st.info("Conversación cerrada (`done` o `error`). Pulsa «Nueva conversación».")
elif turnos_hechos >= max_turns:
    st.warning("Has alcanzado `max_turns`. Pulsa «Nueva conversación» o sube el límite.")

# --- Entrada del usuario → un turno del agente ---
if prompt := st.chat_input(
    "Escribe tu mensaje…",
    disabled=chat_bloqueado or turnos_hechos >= max_turns,
):
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    with st.chat_message("assistant"):
        with st.spinner("Pensando (posible uso de tools)…"):
            # Aquí entra la lógica real (tools + JSON + done)
            estado = procesar_turno(estado, prompt, max_steps=max_steps)
            st.session_state.agent_state = estado

        if estado.get("error"):
            st.error(estado["error"])

        # Texto al usuario; si hay plan, lo añadimos debajo
        texto = estado.get("respuesta") or "(Sin respuesta)"
        plan = estado.get("plan") or []
        if plan:
            etiqueta = "Plan" if estado.get("done") else "Plan (borrador)"
            bullets = "\n".join(f"- {item}" for item in plan)
            texto = f"{texto}\n\n**{etiqueta}:**\n{bullets}"
        st.markdown(texto)
        st.session_state.messages.append({"role": "assistant", "content": texto})

# --- Debug: estado interno (no es el chat) ---
with st.expander("Estado / traza de tools (debug)"):
    st.json(
        {
            "preferencias": st.session_state.agent_state.get("preferencias"),
            "plan": st.session_state.agent_state.get("plan"),
            "done": st.session_state.agent_state.get("done"),
            "error": st.session_state.agent_state.get("error"),
            "traza": st.session_state.agent_state.get("traza"),
        }
    )
