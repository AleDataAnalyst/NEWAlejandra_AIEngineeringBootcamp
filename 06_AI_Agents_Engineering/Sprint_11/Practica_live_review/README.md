# Live Review — Sprint 11

Práctica integradora de **agentes con estado** (conversación multi-turno, `done` en Python, `max_turns`, Streamlit como cliente).

**Dominio:** calidad del aire. **Sin RAG ni tools.**

| Carpeta | Contenido |
|---------|-----------|
| [`01_agente_calidad_aire/`](01_agente_calidad_aire/) | Proyecto alumno (TODOs en `src/agent.py`) |
| [`01_agente_calidad_aire_SOLUTION/`](01_agente_calidad_aire_SOLUTION/) | Referencia del profesor |

## Resumen

- **Dominio:** orientar una consulta sobre calidad del aire en Madrid (sin mediciones en vivo)
- **Código dado:** `src/state.py`, `src/llm.py`, `main.py`, `app.py`
- **Implementación del alumno:** `procesar_turno` + `run_demo` en `src/agent.py`
- **`app.py`:** dado (cliente de `from src.agent import procesar_turno`)
- **Contrato:**

```text
mensaje → procesar_turno(estado, mensaje)
       → LLM (JSON sin done) → actualizar_estado → calcular_done → traza
CLI / Streamlit = clientes
```
