"""App Streamlit — Live Review Sprint 10 (dado).

No tienes que implementar la UI: ya llama a src.logic.responder().
Cuando tengas responder() listo:

  streamlit run app.py
"""

from __future__ import annotations

import streamlit as st

from config import TOP_K
from src.logic import responder

st.set_page_config(
    page_title="RAG calidad del aire",
    page_icon="🌬️",
    layout="centered",
)

st.title("RAG · calidad del aire Madrid")
st.caption("Sprint 10 · Live Review — generación + fuentes")

with st.sidebar:
    st.header("Configuración")
    top_k = st.slider("Top-K", min_value=1, max_value=5, value=TOP_K)
    st.caption("Índice: `python main.py --prepare --index`")

pregunta = st.text_input("Tu pregunta")
enviar = st.button("Preguntar", type="primary")

if enviar:
    if not (pregunta or "").strip():
        st.warning("Escribe una pregunta.")
    else:
        with st.spinner("Consultando el corpus…"):
            resultado = responder(pregunta.strip(), top_k=top_k)

        if resultado.get("error"):
            st.error(resultado["error"])
        else:
            st.markdown(resultado.get("respuesta") or "(sin respuesta)")
            fuentes = resultado.get("fuentes") or []
            if fuentes:
                st.markdown("**Fuentes**")
                for f in fuentes:
                    st.write(f"- `{f}`")
            if resultado.get("contexto"):
                with st.expander("Contexto recuperado (debug)"):
                    st.text(resultado["contexto"])
