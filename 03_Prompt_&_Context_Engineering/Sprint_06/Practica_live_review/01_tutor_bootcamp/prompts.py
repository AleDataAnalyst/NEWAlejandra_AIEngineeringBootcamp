"""prompts.py — Construcción de prompts (Fase 1 arquitectura + Fase 2 seguridad).

Qué hace este módulo:
  - Fase 1: `build_assistant_prompt()` ensambla rol, perfil, FAQ e historial.
  - Fase 2: `build_vulnerable_prompt()` vs `build_secure_prompt()` para comparativa.

Para qué sirve:
  - Separar «qué texto enviamos al modelo» de «cuándo llamamos» (logic.py).

Funciones a implementar:
  - Fase 1: build_faq_block, build_history_block, build_assistant_prompt
  - Fase 2: build_vulnerable_prompt, build_secure_prompt
"""

from config import PERFILES


def resolver_perfil(assistant_config: dict) -> dict:
    """Resuelve el perfil activo desde assistant_config. Helper ya implementado."""
    clave = assistant_config["perfil_activo"]
    if clave not in PERFILES:
        raise ValueError(f"Perfil desconocido: {clave}")
    return PERFILES[clave]


def build_faq_block(faq_entries: list[dict]) -> str:
    """TODO: Fase 1 — bloque de texto con entradas FAQ seleccionadas.

    Entrada: lista de dicts del FAQ (puede estar vacía).
    Salida: string con delimitadores --- FAQ --- o "" si no hay entradas.

    Ver README Fase 1, Tarea 2.
    """
    raise NotImplementedError("Implementa build_faq_block()")


def build_history_block(messages: list[dict]) -> str:
    """TODO: Fase 1 — formatea el historial reciente como texto.

    Entrada: lista de {"role": "user"|"assistant", "text": "..."}.
    Salida: string multilínea; si vacío, mensaje indicando sin turnos previos.

    Ver README Fase 1, Tarea 3.
    """
    raise NotImplementedError("Implementa build_history_block()")


def build_assistant_prompt(
    *,
    assistant_config: dict,
    user_state: dict,
    user_message: str,
    extra_context: list[dict] | None = None,
    recent_messages: list[dict] | None = None,
) -> str:
    """TODO: Fase 1 — ensambla el prompt del tutor con arquitectura de asistente.

    Entrada: config, state, mensaje, FAQ opcional, historial reciente.
    Salida: string completo para enviar a Gemini.

    Ver README Fase 1, Tarea 4 (incluye pseudocódigo).
    """
    raise NotImplementedError("Implementa build_assistant_prompt()")


def build_vulnerable_prompt(user_message: str) -> str:
    """TODO: Fase 2 — anti-patrón: mezcla instrucciones y mensaje del usuario.

    Ver README Fase 2, Tarea 3.
    """
    raise NotImplementedError("Implementa build_vulnerable_prompt()")


def build_secure_prompt(user_message: str) -> str:
    """TODO: Fase 2 — SYSTEM fijo + delimitadores de usuario + hint JSON.

    Ver README Fase 2, Tarea 4.
    """
    raise NotImplementedError("Implementa build_secure_prompt()")
