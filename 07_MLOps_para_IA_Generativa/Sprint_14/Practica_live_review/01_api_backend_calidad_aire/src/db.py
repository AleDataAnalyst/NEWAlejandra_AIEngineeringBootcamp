"""Persistencia del historial con SQLModel + SQLite.

Este módulo es lo que la API llama para escribir/leer historial.db.
Modelos → src/models.py | Quién llama → app.py (tras /ask o /approve).

TODO 3: completar save_turn (crear Conversation si falta + 2 Message).
"""

from typing import Any

from sqlmodel import Session, SQLModel, create_engine, select

import config
from src.models import Conversation, Message

engine = create_engine(config.DATABASE_URL, echo=False)


def ensure_schema() -> None:
    """Crea las tablas si no existen (se llama al arrancar FastAPI)."""
    SQLModel.metadata.create_all(engine)


def save_turn(thread_id: str, pregunta: str, respuesta: str) -> None:
    """Guarda un turno completo: mensaje user + mensaje assistant."""
    # TODO 3:
    # 1. Abrir Session(engine)
    # 2. Si no existe Conversation(id=thread_id), crearla y commit
    # 3. Añadir Message role="user" y Message role="assistant"
    # 4. commit
    raise NotImplementedError("TODO 3: completar save_turn")


def list_messages(thread_id: str) -> list[dict[str, Any]]:
    """Lista mensajes del hilo ordenados por id (para GET …/messages)."""
    with Session(engine) as session:
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


def storage_mode() -> str:
    """Valor que muestra /health → "storage": "sqlite"."""
    return "sqlite"
