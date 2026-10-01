![Cabecera](../../../Sprint_11/assets/cabecera_thebridge.png)

# Checkpoints y thread_id

## Problema

Sin checkpointer, cada `app.invoke(...)` empieza **de cero**: no hay historial entre llamadas.

## Solución

```python
from langgraph.checkpoint.memory import MemorySaver

app = grafo.compile(checkpointer=MemorySaver())

config = {"configurable": {"thread_id": "alumno-42"}}
app.invoke({"messages": [...]}, config=config)
# segundo turno, mismo thread_id → el estado previo está disponible
app.invoke({"messages": [...]}, config=config)
```

| Concepto | Idea |
|----------|------|
| **Checkpoint** | Foto del State tras (casi) cada nodo |
| **`thread_id`** | ID de conversación / sesión |
| **`MemorySaver`** | Checkpoints en RAM (se pierden al cerrar el proceso) |
| **SqliteSaver** (opcional) | Checkpoints en disco entre sesiones |

## Regla práctica

Con checkpointer, el `config` con `thread_id` es **obligatorio** en cada `invoke`.

Dos `thread_id` distintos = dos conversaciones independientes (útil en Streamlit: un hilo por usuario o por sesión).
