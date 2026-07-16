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

import json
from pathlib import Path

from config import ASSISTANT_CONFIG_DEFAULT, TEMPERATURE, TEMPERATURE_VULNERABLE
from context import cargar_faq, seleccionar_faq
from gemini_client import MetricasLlamada, safe_generate
from prompts import (
    build_assistant_prompt,
    build_secure_prompt,
    build_vulnerable_prompt,
)
from state import (
    actualizar_perfil_desde_mensaje,
    append_assistant,
    append_user,
    inicializar_estado,
    ultimos_n,
)
from validators import (
    parece_dominio_python,
    rechazo_fuera_de_dominio,
    validate_input,
)


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
    if not user_message.strip():
        return respuesta_error("Mensaje vacío", ["El mensaje no puede estar vacío."])

    config = assistant_config or ASSISTANT_CONFIG_DEFAULT.copy()
    ventana = config.get("max_turnos_historial", 6)

    prompt = build_assistant_prompt(
        assistant_config=config,
        user_state=state,
        user_message=user_message,
        extra_context=faq_entries or [],
        recent_messages=ultimos_n(state, ventana),
    )

    try:
        texto, metricas = safe_generate(prompt, temperature=config["temperature"])
    except ValueError as e:
        return respuesta_error("Error de contexto", [str(e)])

    actualizar_perfil_desde_mensaje(state, user_message)
    append_user(state, user_message)
    append_assistant(state, texto)

    return respuesta_ok(
        "Turno completado",
        {
            "respuesta": texto,
            "perfil_activo": config["perfil_activo"],
            "metricas": _metricas_a_dict(metricas),
        },
    )

    # raise NotImplementedError("Implementa procesar_turno()")


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
    try:
        obj = json.loads(raw)
    except json.JSONDecodeError as e:
        raise ValueError(f"JSON inválido del modelo: {raw!r}") from e
    for key in ("in_scope", "category", "answer"):
        if key not in obj:
            raise ValueError(f"Falta clave obligatoria en JSON: {key}")
    return obj

    # raise NotImplementedError("Implementa parsear_respuesta_tutor()")


def procesar_turno_vulnerable(user_message: str) -> dict:
    """TODO: Fase 2 — pipeline débil para comparativa.

    Ver README Fase 2, Tarea 6.
    """
    if not user_message.strip():
        return respuesta_error("Mensaje vacío", ["El mensaje no puede estar vacío."])

    prompt = build_vulnerable_prompt(user_message)
    try:
        texto, metricas = safe_generate(prompt, temperature=TEMPERATURE_VULNERABLE)
    except ValueError as e:
        return respuesta_error("Error de contexto", [str(e)])

    return respuesta_ok(
        "Turno vulnerable completado",
        {
            "modo": "vulnerable",
            "respuesta": texto,
            "metricas": _metricas_a_dict(metricas),
        },
    )

    # raise NotImplementedError("Implementa procesar_turno_vulnerable()")


def procesar_turno_seguro(user_message: str) -> dict:
    """TODO: Fase 2 — pipeline seguro con defensa en capas.

    Ver README Fase 2, Tarea 7 (incluye pseudocódigo).
    """
    errores = validate_input(user_message)
    if errores:
        return respuesta_error("Input rechazado", errores)

    if not parece_dominio_python(user_message):
        return respuesta_ok(
            "Fuera de dominio (sin llamar al modelo)",
            {
                "modo": "seguro",
                "respuesta": rechazo_fuera_de_dominio(),
                "json": {
                    "in_scope": False,
                    "category": "out_of_scope",
                    "answer": rechazo_fuera_de_dominio(),
                },
                "metricas": None,
            },
        )

    prompt = build_secure_prompt(user_message)
    try:
        raw, metricas = safe_generate(prompt, temperature=TEMPERATURE, json_mode=True)
        obj = parsear_respuesta_tutor(raw)
    except ValueError as e:
        return respuesta_error("Error al procesar respuesta", [str(e)])

    return respuesta_ok(
        "Turno seguro completado",
        {
            "modo": "seguro",
            "respuesta": obj.get("answer", ""),
            "json": obj,
            "metricas": _metricas_a_dict(metricas),
        },
    )

    # raise NotImplementedError("Implementa procesar_turno_seguro()")
