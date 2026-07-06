"""logic.py — Orquestación: validar, clasificar y responder.

Qué hace este módulo:
  - Fase 1: `clasificar_consulta()` — validar → prompt → Gemini → parsear JSON.
  - Fase 2: `responder_chat()` — prompt con contexto → Gemini → actualizar state.
  - Helpers `respuesta_ok()` y `respuesta_error()` (ya implementados).

Para qué sirve:
  - Es el «cerebro» que conecta validators, prompts, context, state y gemini_client.
  - `main.py` solo llama funciones de aquí; no duplica reglas.

Reglas importantes:
  - No uses `print` en este archivo (la salida la hace main.py).
  - Importa `llamar_gemini_json` / `safe_generate_texto` dentro de las funciones.

Funciones a implementar:
  - Fase 1: `parsear_clasificacion`, `clasificar_consulta`
  - Fase 2: `demo_seleccion_faq`, `responder_chat`
"""

import json
from pathlib import Path

from config import (
    CATEGORIAS,
    MSG_CHAT_OK,
    MSG_CLASIFICACION_OK,
    MSG_ERROR_VALIDACION,
    PRIORIDADES,
    WINDOW,
)
from context import cargar_faq, seleccionar_faq
from prompts import build_chat_prompt, build_clasificacion_prompt
from state import append_model, append_user, guardar_clasificacion, ultimos_n
from validators import validar_consulta


def respuesta_ok(mensaje: str, data: dict | None = None) -> dict:
    return {"status": "ok", "mensaje": mensaje, "data": data or {}}


def respuesta_error(mensaje: str, errores: list[str]) -> dict:
    return {"status": "error", "mensaje": mensaje, "data": {"errores": errores}}


def parsear_clasificacion(raw: str) -> dict:
    """Convierte la respuesta del modelo en dict validado (whitelist).

    Entrada: '{"category": "tecnico", "priority": "media", "summary": "..."}'
    Salida: dict con esas tres claves validadas.
    Lanza ValueError si el JSON es inválido o las claves no están en config.

    Ver README FASE 1, Tarea 3.
    """
    try:
        obj = json.loads(raw)
    except json.JSONDecodeError as e:
        raise ValueError(f"JSON inválido del modelo: {raw!r}") from e

    if not isinstance(obj, dict):
        raise ValueError(f"Se esperaba un objeto JSON, recibido: {type(obj)}")

    faltan = {"category", "priority", "summary"} - obj.keys()
    if faltan:
        raise ValueError(f"Faltan claves en la respuesta: {faltan}")

    if obj["category"] not in CATEGORIAS:
        raise ValueError(f"category inválida: {obj['category']!r}")
    if obj["priority"] not in PRIORIDADES:
        raise ValueError(f"priority inválida: {obj['priority']!r}")

    return obj


def clasificar_consulta(datos: dict) -> dict:
    """Orquesta validar → prompt → Gemini → parsear (fase 1).

    Entrada: dict como en consultas_ejemplo.json.
    Salida OK: {"status": "ok", "mensaje": "...", "data": {category, priority, summary}}
    Salida error: {"status": "error", "mensaje": "...", "data": {"errores": [...]}}

    Sin print. Ver README FASE 1, Tarea 4.
    """
    errores = validar_consulta(datos)
    if errores:
        return respuesta_error(MSG_ERROR_VALIDACION, errores)

    mensaje = str(datos.get("mensaje", "")).strip()
    prompt = build_clasificacion_prompt(mensaje)

    try:
        from gemini_client import llamar_gemini_json

        raw = llamar_gemini_json(prompt)
        obj = parsear_clasificacion(raw)
        return respuesta_ok(MSG_CLASIFICACION_OK, obj)
    except ValueError as e:
        return respuesta_error("Salida del modelo inválida", [str(e)])
    except Exception as e:
        return respuesta_error("Error al llamar al modelo", [str(e)])


def clasificar_y_guardar(datos: dict, state: dict) -> dict:
    r = clasificar_consulta(datos)
    if r.get("status") == "ok":
        guardar_clasificacion(state, datos, r["data"])
    return r


def responder_chat(
    state: dict,
    pregunta: str,
    faq_entries: list[dict],
) -> dict:
    """Chat con perfil, FAQ filtrado e historial (fase 2).

    Entrada: state (inicializar_estado), pregunta del alumno, faq_entries de seleccionar_faq.
    Salida OK: respuesta del modelo + metricas (elapsed_ms, tokens).
    Actualiza state con append_user/append_model tras respuesta OK.

    Ver README FASE 2, Tarea 4 (incluye pseudocódigo).
    """
    if not pregunta.strip():
        return respuesta_error("Pregunta vacía", ["La pregunta no puede estar vacía."])

    profile = state.get("user_profile", {})
    prompt = build_chat_prompt(
        pregunta=pregunta,
        profile=profile,
        faq_entries=faq_entries,
        recent_messages=ultimos_n(state, WINDOW),
    )

    try:
        from gemini_client import safe_generate_texto

        texto, metricas = safe_generate_texto(prompt)
    except ValueError as e:
        return respuesta_error("Contexto demasiado grande", [str(e)])
    except Exception as e:
        return respuesta_error("Error al llamar al modelo", [str(e)])

    append_user(state, pregunta)
    append_model(state, texto)

    return respuesta_ok(
        MSG_CHAT_OK,
        {
            "respuesta": texto,
            "metricas": {
                "elapsed_ms": metricas.elapsed_ms,
                "prompt_tokens": metricas.prompt_tokens,
                "output_tokens": metricas.output_tokens,
                "total_tokens": metricas.total_tokens,
            },
        },
    )


def demo_seleccion_faq(faq_path: Path, consulta: str) -> dict:
    """Prueba seleccionar_faq sin chat completo.

    Entrada: ruta a faq.json y texto de consulta.
    Salida OK: {"status": "ok", "data": {"topic_id": "...", "entry": {...}}}

    Ver README FASE 2, Tarea 4.
    """
    faq = cargar_faq(faq_path)
    seleccion = seleccionar_faq(faq, consulta, max_entradas=1)
    if not seleccion:
        return respuesta_error(
            "FAQ sin coincidencias",
            ["Ninguna entrada del FAQ coincide con la consulta."],
        )
    entry = seleccion[0]
    return respuesta_ok(
        "Entrada FAQ seleccionada",
        {"topic_id": entry.get("topic_id"), "entry": entry},
    )
