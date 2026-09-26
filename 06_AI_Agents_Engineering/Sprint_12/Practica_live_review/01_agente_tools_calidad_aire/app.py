"""App Streamlit — chat con tools (cliente UI). DADO.

  streamlit run app.py
"""

import streamlit as st

import config
from src.agent import procesar_turno
from src.state import crear_estado

st.set_page_config(
    page_title="Agente tools · calidad del aire",
    page_icon="🌬️",
    layout="centered",
)

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
    st.caption(
        "max_turns = mensajes de usuario · max_steps = vueltas de tools por turno."
    )
    if st.button("Nueva conversación", use_container_width=True):
        st.session_state.messages = [
            {
                "role": "assistant",
                "content": (
                    "Hola — oriento consultas de calidad del aire con tools "
                    "(guía RAG, API Madrid, hora). "
                    "Cuéntame zona, contaminante y tipo de consulta."
                ),
            }
        ]
        st.session_state.agent_state = crear_estado("")
        st.rerun()

st.title("Agente · tools · calidad del aire")
st.caption("Live Review Sprint 12 — function calling + allowlist + max_steps")

if "messages" not in st.session_state:
    st.session_state.messages = [
        {
            "role": "assistant",
            "content": (
                "Hola — oriento consultas de calidad del aire con tools "
                "(guía RAG, API Madrid, hora). "
                "Cuéntame zona, contaminante y tipo de consulta."
            ),
        }
    ]
if "agent_state" not in st.session_state:
    st.session_state.agent_state = crear_estado("")

for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

estado = st.session_state.agent_state
chat_bloqueado = bool(estado.get("done") or estado.get("error"))
turnos_hechos = len(estado.get("traza") or [])

if chat_bloqueado:
    st.info("Conversación cerrada (`done` o `error`). Pulsa «Nueva conversación».")
elif turnos_hechos >= max_turns:
    st.warning("Has alcanzado `max_turns`. Pulsa «Nueva conversación» o sube el límite.")

if prompt := st.chat_input(
    "Escribe tu mensaje…",
    disabled=chat_bloqueado or turnos_hechos >= max_turns,
):
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    with st.chat_message("assistant"):
        with st.spinner("Pensando (posible uso de tools)…"):
            estado = procesar_turno(estado, prompt, max_steps=max_steps)
            st.session_state.agent_state = estado

        if estado.get("error"):
            st.error(estado["error"])

        texto = estado.get("respuesta") or "(Sin respuesta)"
        plan = estado.get("plan") or []
        if plan:
            etiqueta = "Plan" if estado.get("done") else "Plan (borrador)"
            bullets = "\n".join(f"- {item}" for item in plan)
            texto = f"{texto}\n\n**{etiqueta}:**\n{bullets}"
        st.markdown(texto)
        st.session_state.messages.append({"role": "assistant", "content": texto})

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
