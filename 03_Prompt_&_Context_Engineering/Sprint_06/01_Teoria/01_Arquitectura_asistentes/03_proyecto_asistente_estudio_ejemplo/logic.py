# logic.py — procesar turnos del asistente

from pathlib import Path

from config import ASSISTANT_CONFIG_DEFAULT
from context import cargar_faq, seleccionar_faq
from gemini_client import MetricasLlamada, safe_generate
from prompts import build_assistant_prompt
from state import (
    actualizar_perfil_desde_mensaje,
    append_assistant,
    append_user,
    inicializar_estado,
    ultimos_n,
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


def procesar_turno(
    state: dict,
    user_message: str,
    assistant_config: dict | None = None,
    faq_entries: list[dict] | None = None,
) -> dict:
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


def crear_estado_demo() -> dict:
    return inicializar_estado(
        {
            "nombre": "",
            "nivel": "junior",
            "tema_actual": "",
        }
    )


def demo_seleccion_faq(faq_path: Path, consulta: str) -> dict:
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
