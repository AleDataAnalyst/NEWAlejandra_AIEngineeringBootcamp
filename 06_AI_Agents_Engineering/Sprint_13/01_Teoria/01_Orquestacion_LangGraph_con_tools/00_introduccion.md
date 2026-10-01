![Cabecera](../../../Sprint_11/assets/cabecera_thebridge.png)

# Introducción — Orquestación LangGraph con tools

En el Sprint 12 el ciclo de tools vivía en un **`while` / `for`** en Python (`run_tool_loop`):

1. El LLM pide tools (function calling).
2. Python ejecuta (allowlist, `validar_args`).
3. Se devuelve el resultado al modelo.
4. Se corta con `max_steps` o cuando ya hay texto.

En Sprint 13 **dibujáis ese mismo ciclo como grafo** LangGraph: nodos `agent` y `tools`, edge condicional, bucle hasta respuesta final.

> LangGraph **orquesta**. No sustituye: buen estado, buenas tools, allowlist ni `done` en Python.

## Qué ya sabéis (S12)

- Tools en Python + allowlist
- Notebooks LangGraph: grafo **lineal** y **router** condicional
- Contrato `procesar_turno` + Streamlit como cliente

## Qué aporta este bloque

- El patrón **ReAct** (Reason + Act) en LangGraph
- `bind_tools` / `@tool` / `ToolNode` (ecosistema LangChain) **o** nodos que llaman a `ejecutar_tool`
- Ver el bucle agent → tools → agent en el grafo

## Objetivos

- Explicar el diagrama LLM ↔ tools como nodos y edges.
- Ejecutar un agente con tools en LangGraph (notebook).
- Decir qué se **copia** de S12 y qué se **sustituye**.

📁 Workout: [`01_agente_tools_en_langgraph.ipynb`](../../02_Workout/01_Orquestacion_LangGraph_con_tools/01_agente_tools_en_langgraph.ipynb)
