"""Evaluación de respuestas generadas — Sprint 10 (COMPLETAR).

Barrido de queries/preguntas_eval.json llamando a src.logic.responder.
"""

import json

from config import QUERIES_EVAL_JSON
from .logic import responder


def evaluar_pregunta(item: dict) -> dict:
    """Ejecuta responder() para una pregunta del JSON y resume el resultado."""
    # TODO:
    # - texto = item["texto"]
    # - resultado = responder(texto)
    # - devolver dict con id, texto, deberia_abstenerse, respuesta, fuentes, error, notas
    raise NotImplementedError("Implementa evaluar_pregunta() en src/eval_generation.py")


def ejecutar_evaluacion() -> None:
    """Carga preguntas_eval.json, evalúa cada una e imprime un resumen."""
    # TODO:
    # - cargar JSON
    # - para cada pregunta: evaluar_pregunta + print legible
    # - destacar si deberia_abstenerse y la respuesta parece inventar
    # - si hay notas en el item, imprimirlas
    raise NotImplementedError("Implementa ejecutar_evaluacion() en src/eval_generation.py")
