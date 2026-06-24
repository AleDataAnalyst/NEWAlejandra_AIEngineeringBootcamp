# logic.py — validación, parseo y carga de datos (sin print)

import csv
import json
from pathlib import Path

from config import CATEGORIAS, MAX_CHARS_PROMPT, PRIORIDADES
from gemini_client import llamar_gemini_json, llamar_gemini_texto
from prompts import (
    build_clasificacion_prompt,
    build_ficha_producto_prompt,
    build_recomendacion_clima_prompt,
)


def respuesta_ok(mensaje: str, data: dict | None = None) -> dict:
    return {"status": "ok", "mensaje": mensaje, "data": data or {}}


def respuesta_error(mensaje: str, errores: list[str]) -> dict:
    return {"status": "error", "mensaje": mensaje, "data": {"errores": errores}}


def assert_prompt_razonable(prompt: str) -> None:
    if len(prompt) > MAX_CHARS_PROMPT:
        raise ValueError(
            f"Prompt demasiado largo ({len(prompt)} caracteres). "
            "Recorta datos de referencia en Python."
        )


def parsear_clasificacion(raw: str) -> dict:
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


def clasificar_mensaje(mensaje: str) -> dict:
    if not mensaje.strip():
        return respuesta_error("Mensaje vacío", ["El mensaje no puede estar vacío."])

    prompt = build_clasificacion_prompt(mensaje)
    assert_prompt_razonable(prompt)

    try:
        raw = llamar_gemini_json(prompt)
        obj = parsear_clasificacion(raw)
        return respuesta_ok("Clasificación completada", obj)
    except ValueError as e:
        return respuesta_error("Salida del modelo inválida", [str(e)])


def cargar_productos_csv(ruta: Path) -> list[dict]:
    with ruta.open(encoding="utf-8", newline="") as f:
        return list(csv.DictReader(f))


def producto_por_sku(productos: list[dict], sku: str) -> dict:
    fila = next((p for p in productos if p.get("sku") == sku), None)
    if fila is None:
        raise ValueError(f"SKU no encontrado: {sku}")
    return fila


def generar_ficha_producto(producto: dict) -> dict:
    prompt = build_ficha_producto_prompt(producto)
    assert_prompt_razonable(prompt)
    try:
        texto = llamar_gemini_texto(prompt)
        return respuesta_ok("Ficha generada", {"descripcion": texto, "sku": producto.get("sku")})
    except Exception as e:
        return respuesta_error("Error al llamar al modelo", [str(e)])


def generar_recomendacion_clima(weather: dict) -> dict:
    prompt = build_recomendacion_clima_prompt(weather)
    assert_prompt_razonable(prompt)
    try:
        texto = llamar_gemini_texto(prompt)
        return respuesta_ok("Recomendaciones generadas", {"texto": texto})
    except Exception as e:
        return respuesta_error("Error al llamar al modelo", [str(e)])
