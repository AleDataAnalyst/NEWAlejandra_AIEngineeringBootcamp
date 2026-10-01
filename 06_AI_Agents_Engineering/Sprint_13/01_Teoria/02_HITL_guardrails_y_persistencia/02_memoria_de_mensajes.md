![Cabecera](../../../Sprint_11/assets/cabecera_thebridge.png)

# Memoria de mensajes

## Lista de mensajes en el State

```python
from typing import Annotated, TypedDict
from langgraph.graph.message import add_messages

class Estado(TypedDict):
    messages: Annotated[list, add_messages]  # add_messages → acumula
```

`add_messages` **acumula**: el nodo devuelve solo el mensaje nuevo y LangGraph lo concatena al historial del thread.

## Chat vs AgentState del producto

| Capa | Qué guarda | Quién la mira |
|------|------------|---------------|
| Mensajes del grafo | Historial del ciclo / chat corto | Nodos LLM |
| `agent_state` (prefs, plan, done, traza) | Producto Streamlit | UI + `calcular_done` |

No mezclar: el checkpointer recuerda el State del **grafo**; el sidebar de Streamlit sigue mostrando el `AgentState` que actualicéis en `procesar_turno`.

## Inspección

```python
estado = app.get_state(config)
# estado.values → State actual del thread
```

Útil para depurar y para la UI (“¿qué plan hay pendiente de aprobar?”).
