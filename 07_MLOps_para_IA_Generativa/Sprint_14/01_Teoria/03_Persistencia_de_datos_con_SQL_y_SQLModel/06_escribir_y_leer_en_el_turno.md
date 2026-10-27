![Cabecera](../../../../06_AI_Agents_Engineering/Sprint_11/assets/cabecera_thebridge.png)

# Escribir y leer en el turno (SQLModel)

## Guardar tras `/ask`

```python
from sqlmodel import select

from src.models import Conversation, Message


def save_turn(thread_id: str, pregunta: str, respuesta: str) -> None:
    with get_session() as session:
        conv = session.get(Conversation, thread_id)
        if conv is None:
            session.add(Conversation(id=thread_id))
            session.commit()

        session.add(Message(thread_id=thread_id, role="user", content=pregunta))
        session.add(Message(thread_id=thread_id, role="assistant", content=respuesta))
        session.commit()
```

En la ruta:

```python
@app.post("/ask", response_model=AskOut)
def ask(body: AskIn) -> AskOut:
    thread_id = body.thread_id or "default"
    out = procesar_turno(body.pregunta)
    save_turn(thread_id, body.pregunta, out["respuesta"])
    return AskOut(respuesta=out["respuesta"], thread_id=thread_id)
```

## Listar historial

```python
@app.get("/threads/{thread_id}/messages")
def list_messages(thread_id: str):
    with get_session() as session:
        rows = session.exec(
            select(Message)
            .where(Message.thread_id == thread_id)
            .order_by(Message.id)
        ).all()
    return [
        {
            "role": m.role,
            "content": m.content,
            "created_at": m.created_at.isoformat() if m.created_at else None,
        }
        for m in rows
    ]
```

## Orden recomendado

1. Validar body.
2. Llamar a la lógica de IA.
3. Persistir **si** la lógica respondió OK.
4. Devolver JSON.

Si la IA falla, no insertéis una respuesta vacía.

---

## Resumen

- Un turno = 2 `Message` bajo el mismo `thread_id`.
- `select` + `order_by` para comprobar que persistió.
