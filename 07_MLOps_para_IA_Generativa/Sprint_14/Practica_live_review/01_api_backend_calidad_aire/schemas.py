"""
Contratos HTTP de la API (Pydantic).

TODO 1: completar AskIn, AskOut, ApproveIn y MessageOut (Field, min_length donde toque).
"""

from typing import Optional

from pydantic import BaseModel, Field


class AskIn(BaseModel):
    """Body de POST /ask — una pregunta sobre calidad del aire."""

    # TODO 1: pregunta obligatoria (min_length=1, max_length=2000),
    #         thread_id opcional, auto_aprobar bool (default True)
    # pregunta: str
    # thread_id: Optional[str]
    # auto_aprobar: bool = True
    pass


class AskOut(BaseModel):
    """Respuesta de POST /ask y POST /approve."""

    # TODO 1: respuesta, thread_id, done, pendiente_hitl, error opcional
    # respuesta: str
    # thread_id: str
    # done: bool = False
    # pendiente_hitl: bool = False
    # error: Optional[str] = None
    pass


class ApproveIn(BaseModel):
    """Body de POST /approve — HITL manual."""

    # TODO 1: thread_id obligatorio (min_length=1) y aprobado bool
    # thread_id: str
    # aprobado: bool
    pass


class MessageOut(BaseModel):
    """Un mensaje del historial SQL."""

    # TODO 1: role, content, created_at opcional (str)
    # role: str
    # content: str
    # created_at: Optional[str] = None
    pass
