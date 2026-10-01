"""App Streamlit — cliente del grafo LangGraph (calidad del aire).

  streamlit run app.py
"""

from __future__ import annotations

import streamlit as st

import config
from src.agent import aprobar_plan, procesar_turno
from src.state import crear_estado

st.set_page_config(
    page_title="Agente LangGraph · calidad del aire",
    page_icon="🌬️",
    layout="centered",
)

with st.sidebar:
    st.header("Configuración")
    max_turns = st.slider(
        "max_turns", min_value=1, max_value=12, value=config.MAX_TURNS_DEFAULT
    )
    max_steps = st.slider(
        "max_steps (tools)", min_value=1, max_value=12, value=config.MAX_STEPS_DEFAULT
    )
    st.caption("max_turns = mensajes · max_steps = vueltas agent↔tools por turno.")

    estado_side = st.session_state.get("agent_state") or {}
    if estado_side.get("pendiente_hitl"):
        st.divider()
        st.subheader("HITL — aprobar plan")
        for item in estado_side.get("plan") or []:
            st.markdown(f"- {item}")
        c1, c2 = st.columns(2)
        if c1.button("Aprobar", use_container_width=True, type="primary"):
            st.session_state.agent_state = aprobar_plan(
                st.session_state.agent_state, True
            )
            st.session_state.messages.append(
                {
                    "role": "assistant",
                    "content": st.session_state.agent_state.get("respuesta")
                    or "Plan aprobado.",
                }
            )
            st.rerun()
        if c2.button("Rechazar", use_container_width=True):
            st.session_state.agent_state = aprobar_plan(
                st.session_state.agent_state, False
            )
            st.session_state.messages.append(
                {
                    "role": "assistant",
                    "content": st.session_state.agent_state.get("respuesta")
                    or "Plan rechazado.",
                }
            )
            st.rerun()

    if st.button("Nueva conversación", use_container_width=True):
        st.session_state.messages = [
            {
                "role": "assistant",
                "content": (
                    "Hola — oriento consultas de **calidad del aire** con LangGraph "
                    "(guía, API Madrid, hora). Cuéntame zona, contaminante y tipo "
                    "de consulta. Cuando el plan esté listo, lo apruebas en la sidebar."
                ),
            }
        ]
        st.session_state.agent_state = crear_estado("")
        st.rerun()

st.title("Agente · LangGraph · calidad del aire")
st.caption("Sprint 13 Live Review — grafo agent↔tools + HITL")

if "messages" not in st.session_state:
    st.session_state.messages = [
        {
            "role": "assistant",
            "content": (
                "Hola — oriento consultas de **calidad del aire** con LangGraph "
                "(guía, API Madrid, hora). Cuéntame zona, contaminante y tipo "
                "de consulta. Cuando el plan esté listo, lo apruebas en la sidebar."
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
hitl_bloquea = bool(estado.get("pendiente_hitl"))

if chat_bloqueado:
    st.info("Conversación cerrada (`done` o `error`). Pulsa «Nueva conversación».")
elif hitl_bloquea:
    st.warning("Plan pendiente de aprobación — usa los botones de la barra lateral.")
elif turnos_hechos >= max_turns:
    st.warning("Has alcanzado `max_turns`.")

if prompt := st.chat_input(
    "Escribe tu mensaje…",
    disabled=chat_bloqueado or hitl_bloquea or turnos_hechos >= max_turns,
):
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    with st.chat_message("assistant"):
        with st.spinner("Grafo LangGraph (posible uso de tools)…"):
            estado = procesar_turno(estado, prompt, max_steps=max_steps)
            st.session_state.agent_state = estado

        if estado.get("error"):
            st.error(estado["error"])

        texto = estado.get("respuesta") or "(Sin respuesta)"
        plan = estado.get("plan") or []
        if plan:
            if estado.get("pendiente_hitl"):
                etiqueta = "Plan (pendiente de aprobación)"
            elif estado.get("done"):
                etiqueta = "Plan"
            else:
                etiqueta = "Plan (borrador)"
            bullets = "\n".join(f"- {item}" for item in plan)
            texto = f"{texto}\n\n**{etiqueta}:**\n{bullets}"
        st.markdown(texto)
        st.session_state.messages.append({"role": "assistant", "content": texto})

with st.expander("Estado / traza de tools (debug)"):
    st.json(
        {
            "preferencias": st.session_state.agent_state.get("preferencias"),
            "plan": st.session_state.agent_state.get("plan"),
            "pendiente_hitl": st.session_state.agent_state.get("pendiente_hitl"),
            "plan_aprobado": st.session_state.agent_state.get("plan_aprobado"),
            "done": st.session_state.agent_state.get("done"),
            "error": st.session_state.agent_state.get("error"),
            "traza": st.session_state.agent_state.get("traza"),
        }
    )
