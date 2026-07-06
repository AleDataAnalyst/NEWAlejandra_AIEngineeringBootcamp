# logic.py — turnos vulnerable vs seguro

import json

from config import TEMPERATURE, TEMPERATURE_VULNERABLE
from gemini_client import MetricasLlamada, safe_generate
from prompts import build_secure_prompt, build_vulnerable_prompt
from validators import (
    parece_dominio_python,
    rechazo_fuera_de_dominio,
    validate_input,
)


def respuesta_ok(mensaje: str, data: dict | None = None) -> dict:
    return {"status": "ok", "mensaje": mensaje, "data": data or {}}


def respuesta_error(mensaje: str, errores: list[str]) -> dict:
    return {"status": "error", "mensaje": mensaje, "data": {"errores": errores}}


def _metricas_a_dict(m: MetricasLlamada) -> dict:
    return {
        "elapsed_ms": m.elapsed_ms,
        "prompt_tokens": m.prompt_tokens,
        "output_tokens": m.output_tokens,
        "total_tokens": m.total_tokens,
    }


def parsear_respuesta_tutor(raw: str) -> dict:
    try:
        obj = json.loads(raw)
    except json.JSONDecodeError as e:
        raise ValueError(f"JSON inválido del modelo: {raw!r}") from e
    for key in ("in_scope", "category", "answer"):
        if key not in obj:
            raise ValueError(f"Falta clave obligatoria en JSON: {key}")
    return obj


def procesar_turno_vulnerable(user_message: str) -> dict:
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


def procesar_turno_seguro(user_message: str) -> dict:
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
