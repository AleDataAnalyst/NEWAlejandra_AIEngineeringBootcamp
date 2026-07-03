"""state.py — Estado de sesión del asistente.

Qué hace este módulo:
  - Guarda perfil del alumno e historial de mensajes entre turnos.
  - Helpers básicos (`append_user`, `ultimos_n`, …) vienen listos.
  - `actualizar_perfil_desde_mensaje()` extrae nombre/tema sin LLM (Fase 1 — TODO alumno).

Para qué sirve:
  - Memoria de sesión para demos de perfil y “¿cómo me llamo?”.

Función a implementar (Fase 1):
  - `actualizar_perfil_desde_mensaje()` — ver README Fase 1, Tarea 1.
"""


def inicializar_estado(user_profile: dict | None = None) -> dict:
    """Crea el dict de sesión. Ya implementada; no necesitas modificarla."""
    return {
        "user_profile": user_profile or {},
        "messages": [],
        "turnos": 0,
    }


def append_user(state: dict, texto: str) -> None:
    """Añade mensaje del usuario al historial. Ya implementada."""
    state["messages"].append({"role": "user", "text": texto.strip()})


def append_assistant(state: dict, texto: str) -> None:
    """Añade respuesta del asistente al historial. Ya implementada."""
    state["messages"].append({"role": "assistant", "text": texto.strip()})
    state["turnos"] = state.get("turnos", 0) + 1


def ultimos_n(state: dict, n: int) -> list[dict]:
    """Devuelve los últimos n mensajes. Ya implementada."""
    msgs = state.get("messages", [])
    return msgs[-n:] if n > 0 else []


def actualizar_perfil_desde_mensaje(state: dict, mensaje: str) -> None:
    """TODO: Fase 1 — extracción didáctica de nombre y tema (sin LLM).

    Entrada: state con user_profile, mensaje del usuario.
    Efecto: si detecta "me llamo …" guarda nombre; si detecta tema de estudio, lo guarda.

    Ver README Fase 1, Tarea 1 (incluye pseudocódigo).
    """
    raise NotImplementedError("Implementa actualizar_perfil_desde_mensaje()")
