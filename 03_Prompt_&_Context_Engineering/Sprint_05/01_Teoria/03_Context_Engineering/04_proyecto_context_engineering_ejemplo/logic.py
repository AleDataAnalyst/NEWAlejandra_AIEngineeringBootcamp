# logic.py — turnos de chat, resumen y respuestas estructuradas

from pathlib import Path

from config import RESUMIR_CADA, WINDOW
from context import cargar_faq, seleccionar_faq, seleccionar_faq_por_topic
from gemini_client import MetricasLlamada, safe_generate
from gemini_client import llamar_gemini_resumen
from prompts import build_resumen_prompt, build_study_prompt
from state import (
    append_model,
    append_user,
    historial_como_texto,
    inicializar_estado,
    set_summary,
    ultimos_n,
)


def respuesta_ok(mensaje: str, data: dict | None = None) -> dict:
    return {"status": "ok", "mensaje": mensaje, "data": data or {}}


def respuesta_error(mensaje: str, errores: list[str]) -> dict:
    return {"status": "error", "mensaje": mensaje, "data": {"errores": errores}}


def _debe_resumir(state: dict) -> bool:
    n = len(state.get("messages", []))
    return n >= RESUMIR_CADA and n % RESUMIR_CADA == 0


def maybe_update_summary(state: dict) -> bool:
    if not _debe_resumir(state):
        return False
    texto = historial_como_texto(state)
    prompt = build_resumen_prompt(texto, max_puntos=6)
    summary = llamar_gemini_resumen(prompt)
    set_summary(state, summary)
    return True


def responder_pregunta(
    state: dict,
    pregunta: str,
    faq_entries: list[dict] | None = None,
) -> dict:
    if not pregunta.strip():
        return respuesta_error("Pregunta vacía", ["La pregunta no puede estar vacía."])

    prompt = build_study_prompt(
        pregunta=pregunta,
        profile=state.get("user_profile", {}),
        faq_entries=faq_entries or [],
        summary=state.get("summary", ""),
        recent_messages=ultimos_n(state, WINDOW),
    )

    try:
        texto, metricas = safe_generate(prompt)
    except ValueError as e:
        return respuesta_error("Contexto demasiado grande", [str(e)])

    append_user(state, pregunta)
    append_model(state, texto)
    resumido = maybe_update_summary(state)

    return respuesta_ok(
        "Respuesta generada",
        {
            "respuesta": texto,
            "resumen_actualizado": resumido,
            "summary": state.get("summary", ""),
            "metricas": _metricas_a_dict(metricas),
            "modo_contexto": "summary+ventana" if state.get("summary") else "ventana",
        },
    )


def _metricas_a_dict(m: MetricasLlamada) -> dict:
    return {
        "elapsed_ms": m.elapsed_ms,
        "prompt_tokens": m.prompt_tokens,
        "output_tokens": m.output_tokens,
        "total_tokens": m.total_tokens,
    }


def demo_faq(faq_path: Path, consulta: str) -> dict:
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


def crear_estado_demo() -> dict:
    profile = {
        "name": "Ana",
        "language": "español",
        "level": "junior",
        "tone": "claro y directo",
        "study_topic": "Context Engineering",
    }
    return inicializar_estado(profile)


def cargar_faq_default(data_dir: Path) -> list[dict]:
    return cargar_faq(data_dir / "faq.json")


def faq_para_topic(data_dir: Path, topic_id: str) -> list[dict]:
    return seleccionar_faq_por_topic(cargar_faq_default(data_dir), topic_id)
