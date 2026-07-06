"""logic.py — Orquestación de turnos (Fase 1 arquitectura + Fase 2 seguridad).

Qué hace este módulo:
  - Fase 1: `procesar_turno()` — pipeline con perfiles, FAQ e historial.
  - Fase 2: `procesar_turno_vulnerable()` vs `procesar_turno_seguro()`.

Para qué sirve:
  - Punto único de reglas de negocio; main.py solo imprime resultados.

Qué NO debes hacer aquí:
  - No uses `print()` — devuelve dicts con respuesta_ok/respuesta_error.

Funciones ya implementadas (código dado):
  - `respuesta_ok`, `respuesta_error`, `crear_estado_demo`, `demo_seleccion_faq`
"""

from pathlib import Path

from context import cargar_faq, seleccionar_faq
from gemini_client import MetricasLlamada
from state import inicializar_estado


def respuesta_ok(mensaje: str, data: dict | None = None) -> dict:
    """Formato estándar de éxito. Ya implementada."""
    return {"status": "ok", "mensaje": mensaje, "data": data or {}}


def respuesta_error(mensaje: str, errores: list[str]) -> dict:
    """Formato estándar de error. Ya implementada."""
    return {"status": "error", "mensaje": mensaje, "data": {"errores": errores}}


def _metricas_a_dict(m: MetricasLlamada) -> dict:
    return {
        "elapsed_ms": m.elapsed_ms,
        "prompt_tokens": m.prompt_tokens,
        "output_tokens": m.output_tokens,
        "total_tokens": m.total_tokens,
    }


def procesar_turno(
    state: dict,
    user_message: str,
    assistant_config: dict | None = None,
    faq_entries: list[dict] | None = None,
) -> dict:
    """TODO: Fase 1 — pipeline: prompt → Gemini → actualizar estado.

    Ver README Fase 1, Tarea 5 (incluye pseudocódigo).
    """
    raise NotImplementedError("Implementa procesar_turno()")


def crear_estado_demo() -> dict:
    """Estado inicial para las demos de Fase 1. Ya implementada; no necesitas modificarla."""
    return inicializar_estado(
        {
            "nombre": "",
            "nivel": "junior",
            "tema_actual": "",
        }
    )


def demo_seleccion_faq(faq_path: Path, consulta: str) -> dict:
    """Muestra qué entrada FAQ se seleccionó. Ya implementada; no necesitas modificarla."""
    faq = cargar_faq(faq_path)
    seleccion = seleccionar_faq(faq, consulta, max_entradas=1)
    if not seleccion:
        return respuesta_error(
            "FAQ sin coincidencias",
            ["Ninguna entrada del FAQ coincide con la consulta."],
        )
    return respuesta_ok(
        "Entrada FAQ seleccionada",
        {"topic_id": seleccion[0].get("topic_id"), "entry": seleccion[0]},
    )


def parsear_respuesta_tutor(raw: str) -> dict:
    """TODO: Fase 2 — parsea y valida JSON del modelo (claves obligatorias).

    Ver README Fase 2, Tarea 5.
    """
    raise NotImplementedError("Implementa parsear_respuesta_tutor()")


def procesar_turno_vulnerable(user_message: str) -> dict:
    """TODO: Fase 2 — pipeline débil para comparativa.

    Ver README Fase 2, Tarea 6.
    """
    raise NotImplementedError("Implementa procesar_turno_vulnerable()")


def procesar_turno_seguro(user_message: str) -> dict:
    """TODO: Fase 2 — pipeline seguro con defensa en capas.

    Ver README Fase 2, Tarea 7 (incluye pseudocódigo).
    """
    raise NotImplementedError("Implementa procesar_turno_seguro()")
