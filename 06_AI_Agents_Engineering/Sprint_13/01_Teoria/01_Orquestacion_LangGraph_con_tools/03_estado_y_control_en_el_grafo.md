![Cabecera](../../../Sprint_11/assets/cabecera_thebridge.png)

# Estado y control en el grafo

## State típico (ReAct)

```python
class EstadoAgente(TypedDict):
    messages: Annotated[list, add_messages]  # add_messages → acumula
    # opcionales en el proyecto:
    # preferencias, plan, done, traza, pasos_tools, ...
```

`add_messages` es un **reducer**: al devolver `{"messages": [nuevo]}` se **añade**, no se pisa todo el historial.

## Qué sigue siendo de Python (no del LLM)

Igual que S11/S12:

| Control | Dónde |
|---------|--------|
| Allowlist / `validar_args` | Nodo tools o wrapper |
| **`max_steps`** | Contador en estado o corte del bucle |
| **`calcular_done`** | Tras el grafo o en un nodo final (Python) |
| Traza `ok` / `error` / `blocked` | Al ejecutar tools |

El LLM **no** tiene tool `marcar_done`.

## Mensajes vs AgentState del proyecto

En Streamlit (S11/S12) ya distinguíais:

- `messages` → pintar el chat
- `agent_state` → preferencias, plan, done, traza

Con LangGraph, la lista de mensajes del ciclo ReAct vive en el **State del grafo**.  
El `AgentState` del producto (prefs/plan/done) se puede actualizar **después** del `invoke` (síntesis JSON), como en S12 tras `run_tool_loop`.
