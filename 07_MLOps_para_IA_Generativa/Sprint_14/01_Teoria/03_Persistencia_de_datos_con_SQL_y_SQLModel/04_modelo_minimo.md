![Cabecera](../../../../06_AI_Agents_Engineering/Sprint_11/assets/cabecera_thebridge.png)

# Ejemplo de modelo de conversaciones y mensajes con SQLModel

Aplicación de lo visto en [ORM y SQLModel](./03_orm_y_sqlmodel.md) al historial de la API.

Dos tablas bastan. Sin `Relationship` complejos: solo Foreign Key para relacionar las conversaciones con los mensajes.

## Modelos mínimos para persistir datos en la DB SQL

```python
from datetime import datetime, timezone
from typing import Optional

from sqlmodel import Field, SQLModel


def _now() -> datetime:
    return datetime.now(timezone.utc)


class Conversation(SQLModel, table=True): # Tabla para guardar las conversaciones de la conversación entre el usuario y el asistente
    id: str = Field(primary_key=True, max_length=100)
    created_at: datetime = Field(default_factory=_now)


class Message(SQLModel, table=True): # Tabla para guardar los mensajes
    id: Optional[int] = Field(default=None, primary_key=True)
    thread_id: str = Field(foreign_key="conversation.id", index=True, max_length=100)
    role: str = Field(max_length=20)  # 'user' | 'assistant'
    content: str
    created_at: datetime = Field(default_factory=_now)
```

`table=True` = esta clase es una tabla real.

## Cómo se usa en el turno

```text
POST /ask { pregunta, thread_id }
  1. asegura Conversation(id=thread_id)
  2. Message role=user
  3. llama a procesar_turno / responder
  4. Message role=assistant
  5. commit + AskOut
```

```text
GET /threads/{thread_id}/messages
  → select Message where thread_id = … order by id
```
---

## Resumen
- El agente puede seguir con estado en memoria / `MemorySaver` en el proceso.
- Ampliar a usuarios o tokens por mensaje es un **extra**.
- `Conversation` + `Message` con SQLModel.
- `thread_id` une API, agente y filas.

**Siguiente:** [Conectar desde FastAPI](./05_conectar_desde_fastapi.md).
