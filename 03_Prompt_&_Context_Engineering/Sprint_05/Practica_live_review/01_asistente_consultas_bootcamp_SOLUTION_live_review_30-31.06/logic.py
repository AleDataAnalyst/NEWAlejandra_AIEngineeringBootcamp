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

from validators import validar_consulta

from config import (
    CATEGORIAS,
    MSG_CLASIFICACION_OK,
    MSG_ERROR_VALIDACION,
    PRIORIDADES,
)

from prompts import build_clasificacion_prompt

def respuesta_ok(mensaje: str, data: dict | None = None) -> dict:
    return {"status": "ok", "mensaje": mensaje, "data": data or {}}


def respuesta_error(mensaje: str, errores: list[str]) -> dict:
    return {"status": "error", "mensaje": mensaje, "data": {"errores": errores}}


def parsear_clasificacion(raw: str) -> dict:
    """TODO: clasificación — json.loads + whitelist de category y priority.

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

    # raise NotImplementedError("Implementa parsear_clasificacion()")


def clasificar_consulta(datos: dict) -> dict:
    """TODO: clasificación — orquesta validar → prompt → Gemini → parsear.

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
    
    # raise NotImplementedError("Implementa clasificar_consulta()")

def responder_chat(
    state: dict,
    pregunta: str,
    faq_entries: list[dict],
) -> dict:
    """TODO: contexto y chat — prompt con perfil, FAQ filtrado e historial.

    Entrada: state (inicializar_estado), pregunta del alumno, faq_entries de seleccionar_faq.
    Salida OK: respuesta del modelo + metricas (elapsed_ms, tokens).
    Actualiza state con append_user/append_model tras respuesta OK.

    Ver README FASE 2, Tarea 4.
    """
    raise NotImplementedError("Implementa responder_chat()")


def demo_seleccion_faq(faq_path: Path, consulta: str) -> dict:
    """TODO: contexto y chat — prueba seleccionar_faq sin chat completo.

    Entrada: ruta a faq.json y texto de consulta.
    Salida OK: {"status": "ok", "data": {"topic_id": "...", "entry": {...}}}

    Ver README FASE 2, Tarea 4.
    """
    raise NotImplementedError("Implementa demo_seleccion_faq()")
