![Cabecera](../../../Sprint_11/assets/cabecera_thebridge.png)

# Migración desde el Sprint 12

En el Sprint 12 el ciclo de tools era un `while` en Python (`run_tool_loop`): el modelo pedía, `ejecutar_tool` ejecutaba, y `max_steps` cortaba. LangGraph ya lo habíais usado en grafos **sin** ese bucle (lineal y router de intención).

Aquí cambia **quién encadena** los pasos. Hay dos destinos. No son el mismo grafo.

```text
S12   run_tool_loop  (while)
        │
        ├── destino 1   StateGraph ReAct     agent ↔ tools
        │
        └── destino 2   StateGraph supervisor
                         cada especialista puede llevar
                         un for de tools por dentro
```

Teoría del destino 1: [`01_react_con_tools.md`](./01_react_con_tools.md).  
Teoría del destino 2: [`../03_Multimodal_multiagente_y_cierre/01_multiagente.md`](../03_Multimodal_multiagente_y_cierre/01_multiagente.md).  
Memoria y pausa humana: [`../02_HITL_guardrails_y_persistencia/01_persistencia_y_hitl.md`](../02_HITL_guardrails_y_persistencia/01_persistencia_y_hitl.md).

---

## Destino 1 — el `while` pasa a nodos

Es el grafo de dos nodos (agent / tools). Sirve para ver el ciclo suelto.

| Pieza del Sprint 12 | En el grafo ReAct |
|---------------------|-------------------|
| `run_tool_loop` | `StateGraph` con `agent` y `tools` |
| `if function_calls` | Router por `tool_calls` |
| `max_steps` | Contador `pasos` en el State |
| `ejecutar_tool` | `ToolNode`, o un nodo que llama a la misma función |

---

## Destino 2 — el producto

El proyecto de tarde cultural y la Live Review de calidad del aire usan **el mismo grafo**: un supervisor reparte el trabajo entre especialistas y un humano aprueba antes de cerrar. Cambia el dominio, no el dibujo.

| Pieza del Sprint 12 | En el proyecto y en la Live Review |
|---------------------|-------------------------------------|
| Tools, allowlist, `ejecutar_tool` | Se reutilizan. El `for` vive **dentro** del especialista |
| `run_tool_loop` como nodos `agent` / `tools` | No es este grafo. El `StateGraph` es el supervisor |
| `sintetizar_estado` / `calcular_done` | Un nodo escribe el plan; otro pone `done` tras la pausa humana |
| `procesar_turno` | Mismo contrato. Por debajo, `invoke` con `thread_id` |
| CLI y Streamlit | Siguen siendo clientes |

```text
mensaje → procesar_turno(..., thread_id)
       → supervisor ↔ especialistas
       → pausa antes de aplicar
       → la persona aprueba o rechaza
```

📁 Proyecto: [`../03_Multimodal_multiagente_y_cierre/04_proyecto_agente_langgraph_tarde_cultural/`](../03_Multimodal_multiagente_y_cierre/04_proyecto_agente_langgraph_tarde_cultural/)  
📁 Live Review: [`../../Practica_live_review/`](../../Practica_live_review/)

---

## Qué se añade alrededor

El Sprint 12 compilaba el grafo y se olvidaba al terminar el `invoke`. Ahora el checkpointer guarda el hilo, y `interrupt_before` para el grafo antes del nodo sensible. Sin checkpointer no hay dónde dejar esa pausa.

---

## Orden de lectura

1. ReAct con tools (destino 1).
2. Persistencia y human-in-the-loop.
3. Multiagente (destino 2) y multimodal.
4. Proyecto cultural, luego Live Review de aire.
