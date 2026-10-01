"""Tool: API_consultar_calidad_aire — HTTP open data Madrid + fallback local.

DADO: no hace falta implementarla. Léela para entender api vs fallback.

Idea: try API → si falla (red, timeout, JSON raro) → data/aire_fallback.json.
"""

import json

import requests

import config


def _ultimo_valor_validado(record: dict) -> tuple[str, str]:
    """Coge la última hora con dato validado de un registro Madrid.

    El open data no trae un solo "valor": trae 24 columnas por fila:
      H01, H02, … H24  → el número medido
      V01, V02, … V24  → bandera ("V" = validado)

    Recorremos 1..24 y nos quedamos con el último par validado.
    No hace falta memorizar el formato: solo saber que "resumimos" la fila.
    """
    ultimo = ("?", "?")
    for h in range(1, 25):
        clave_h = f"H{h:02d}"  # ej. H08
        clave_v = f"V{h:02d}"  # ej. V08
        if record.get(clave_v) == "V" and record.get(clave_h) not in (None, ""):
            ultimo = (clave_h, str(record.get(clave_h)))
    return ultimo


def _resumir_records(items: list, limite: int, fuente: str) -> str:
    """Pasa de registros crudos a un texto corto para el LLM."""
    if not items:
        return f"No hay mediciones (fuente={fuente})."

    lineas = [f"Fuente: {fuente}", ""]
    for item in items[:limite]:
        estacion = item.get("ESTACION", "?")
        mag = str(item.get("MAGNITUD", "?"))
        nombre = config.MAGNITUDES.get(mag, f"magnitud_{mag}")
        hora, valor = _ultimo_valor_validado(item)
        fecha = f"{item.get('ANO', '?')}-{item.get('MES', '?')}-{item.get('DIA', '?')}"
        lineas.append(
            f"- estación {estacion} | {nombre} ({mag}) | {hora}={valor} | fecha {fecha}"
        )
    lineas.append("")
    lineas.append(
        "Nota: datos orientativos de la red; no inventes umbrales oficiales."
    )
    return "\n".join(lineas)


def API_consultar_calidad_aire(limite: int = 5) -> str:
    """
    Trae un resumen de mediciones de calidad del aire (Madrid).
    Si falla la red, usa data/aire_fallback.json.
    """
    try:
        resp = requests.get(
            config.MADRID_AIRE_URL,
            timeout=config.HTTP_TIMEOUT_SECONDS,
        )
        resp.raise_for_status()
        payload = resp.json()
        items = payload.get("records") or []
        fuente = "api"
    except Exception:
        # Plan B: mismos "records", pero desde fichero local.
        data = json.loads(config.AIRE_FALLBACK_PATH.read_text(encoding="utf-8"))
        items = data.get("records") or []
        fuente = "fallback"

    return _resumir_records(items, limite, fuente)
