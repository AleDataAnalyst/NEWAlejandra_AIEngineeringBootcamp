"""state.py — Memoria de la sesión de chat (Fase 2).

Qué hace este módulo:
  - Guarda el perfil del alumno y el historial de mensajes entre turnos.
  - `inicializar_estado()` crea el dict de sesión (ya implementada).
  - `append_user` / `append_model` añaden turnos; `ultimos_n` recorta el historial.

Para qué sirve:
  - Que el asistente recuerde el nombre y el contexto en preguntas siguientes.
  - Alimentar `build_historial_block()` en prompts.py con los últimos mensajes.

Funciones a implementar:
  - `append_user`, `append_model`, `ultimos_n` — ver README FASE 2, Tarea 3.
  - `guardar_clasificacion` — opcional (experimentos).
"""


def inicializar_estado(user_profile: dict | None = None) -> dict:
    """Crea el dict de sesión. Ya está implementada; no necesitas modificarla."""
    return {
        "user_profile": user_profile or {},
        "messages": [],
        "consultas_clasificadas": [],
    }


def append_user(state: dict, texto: str) -> None:
    """TODO: contexto y chat — añade mensaje del alumno al historial.

    Entrada: state de inicializar_estado, texto = pregunta del usuario.
    Efecto: state["messages"].append({"role": "user", "text": texto.strip()})

    Ver README FASE 2, Tarea 3.
    """
    raise NotImplementedError("Implementa append_user()")


def append_model(state: dict, texto: str) -> None:
    """TODO: contexto y chat — añade respuesta del modelo al historial.

    Entrada: state, texto = respuesta de Gemini.
    Efecto: state["messages"].append({"role": "model", "text": texto.strip()})

    Ver README FASE 2, Tarea 3.
    """
    raise NotImplementedError("Implementa append_model()")


def ultimos_n(state: dict, n: int) -> list[dict]:
    """TODO: contexto y chat — devuelve los últimos n mensajes del chat.

    Entrada: state, n = WINDOW (desde config.py, suele ser 6).
    Salida: lista de {"role": "user"|"model", "text": "..."}; [] si n <= 0.

    Ver README FASE 2, Tarea 3.
    """
    raise NotImplementedError("Implementa ultimos_n()")


def guardar_clasificacion(state: dict, consulta: dict, clasificacion: dict) -> None:
    """TODO: contexto y chat (opcional) — guarda clasificación en el state.

    Entrada: consulta original + dict category/priority/summary.
    Efecto: añade un registro a state["consultas_clasificadas"].

    Ver README experimentos opcionales.
    """
    raise NotImplementedError("Implementa guardar_clasificacion()")
