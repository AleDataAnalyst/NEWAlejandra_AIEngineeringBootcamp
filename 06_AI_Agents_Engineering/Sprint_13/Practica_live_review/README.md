# Live Review — Sprint 13

Práctica integradora: **agente orquestado con LangGraph** (tools + control + HITL).

**Dominio:** calidad del aire.

| Carpeta | Contenido |
|---------|-----------|
| [`01_agente_langgraph_calidad_aire/`](01_agente_langgraph_calidad_aire/) | Proyecto alumno (TODOs en `graph.py` + `agent.py`) |
| [`01_agente_langgraph_calidad_aire_SOLUTION/`](01_agente_langgraph_calidad_aire_SOLUTION/) | Referencia del profesor |

## Contrato

```text
mensaje → procesar_turno(...)
       → grafo LangGraph (agent ↔ tools) → sintetizar → HITL/done → traza
CLI / Streamlit = clientes
```

## Qué se da / qué se pide

| Dado | TODO alumno |
|------|-------------|
| tools + allowlist, state, llm, app (HITL), main, verificar | Routers + `build_graph` + `invoke_tools_loop` |
| Nodos agent/tools del grafo | `procesar_turno` + `run_demo` |

## Estado

Contenido listo (alumno + SOLUTION).
