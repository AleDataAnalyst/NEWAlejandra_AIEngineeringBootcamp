# Live Review — Sprint 13

Práctica integradora: **multiagente LangGraph** (supervisor + especialistas + HITL con `interrupt_before`) y una tool **multimodal** dada (`describir_imagen`).

**Dominio:** calidad del aire.

| Carpeta | Contenido |
|---------|-----------|
| [`01_agente_langgraph_calidad_aire/`](01_agente_langgraph_calidad_aire/) | Proyecto alumno (3 TODOs) |
| [`01_agente_langgraph_calidad_aire_SOLUTION/`](01_agente_langgraph_calidad_aire_SOLUTION/) | Referencia del profesor |

## Contrato

```text
mensaje → procesar_turno(..., thread_id)
       → grafo multiagente (MemorySaver)
       → interrupt_before[aplicar] → humano aprueba / rechaza
CLI / Streamlit = clientes
```

## Qué se da / qué se pide

| Dado | TODO alumno |
|------|-------------|
| tools `@tool` (RAG, API, hora, `describir_imagen`), nodos especialistas, `aprobar_plan`, `run_demo`, app/main | `_fallback_siguiente` |
| `_router_supervisor`, state, llm | `build_graph` (edges + interrupt) |
| | `procesar_turno` |
