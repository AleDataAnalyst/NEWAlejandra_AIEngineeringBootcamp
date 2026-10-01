![Cabecera](../../../Sprint_11/assets/cabecera_thebridge.png)

# Migración desde S12

Objetivo del sprint: el **mismo producto** (tarde cultural + tools + Streamlit), orquestado con LangGraph.

## Tabla de migración

| Pieza S12 | En S13 |
|-----------|--------|
| `src/tools/*`, `TOOL_REGISTRY`, `validar_args`, `ejecutar_tool` | **Reutilizar** |
| `run_tool_loop` en `llm.py` | **Sustituir** por `src/graph.py` (StateGraph) |
| `sintetizar_estado` (JSON prefs/plan) | **Reutilizar** (tras el grafo o nodo final) |
| `calcular_done` | **Reutilizar** |
| `procesar_turno` | **Mantener contrato**; por debajo `graph.invoke` |
| `app.py` / `main.py` | Clientes; añadir HITL (bloque 2) |

## Orden recomendado de implementación

1. Notebook ReAct (este bloque) — aprender el grafo suelto.
2. Checkpoints + HITL (bloque 2).
3. Proyecto: copiar S12 → añadir `graph.py` → cablear `procesar_turno`.
4. Live Review aire (mismo patrón, otro dominio).

## Proyecto hito

📁 [`../03_Multimodal_multiagente_y_cierre/05_proyecto_agente_langgraph_tarde_cultural/`](../03_Multimodal_multiagente_y_cierre/05_proyecto_agente_langgraph_tarde_cultural/)

## Lo que no migráis aún en este bloque

- HITL / `interrupt` → bloque 2  
- Multi-agente / multimodal → bloque 3  
- Bedrock → fuera (MLOps)
