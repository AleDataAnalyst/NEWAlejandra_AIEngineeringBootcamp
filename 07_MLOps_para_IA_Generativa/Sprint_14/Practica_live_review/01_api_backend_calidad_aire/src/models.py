"""Modelos SQLModel del historial.

Cada clase con table=True = una tabla en historial.db.
Relación 1–N: una Conversation tiene muchos Message (FK thread_id).

TODO 2: completar Conversation y Message (campos + Field).
"""

from datetime import datetime, timezone
from typing import Optional

from sqlmodel import Field, SQLModel


def _now() -> datetime:
    """Marca de tiempo en UTC al crear la fila."""
    return datetime.now(timezone.utc)


class Conversation(SQLModel, table=True):
    """Un hilo de chat (= el thread_id que manda el cliente en /ask)."""

    # TODO 2: PK string (mismo id que la API) + marca de tiempo al crear
    # id: str          # PK
    # created_at: datetime
    pass


class Message(SQLModel, table=True):
    """Un mensaje dentro de un hilo (pregunta o respuesta)."""

    # TODO 2: PK autoincremental, FK → conversation.id, rol, texto, marca de tiempo
    # id: Optional[int]   # PK autoincremental
    # thread_id: str      # FK a conversation.id
    # role: str
    # content: str
    # created_at: datetime
    pass
