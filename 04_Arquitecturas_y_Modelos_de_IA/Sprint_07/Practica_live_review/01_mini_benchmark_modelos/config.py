"""Parámetros y rutas centralizadas del mini-benchmark.

Define los modelos a comparar, la temperatura de generación y las
rutas a los datos de entrada (preguntas.json) y a la carpeta de salida.
Modificar MODELS o TEMPERATURE aquí solo si el enunciado lo indica.
"""

from pathlib import Path

MODELS = [
    "gemini-2.5-flash",
    "gemini-3.1-flash-lite",
]

TEMPERATURE = 0.3

DATA_DIR = Path(__file__).parent / "data"
PREGUNTAS_PATH = DATA_DIR / "preguntas.json"

OUTPUT_DIR = Path(__file__).parent / "output"
ENTREGABLES_DIR = Path(__file__).parent / "entregables"

MIN_PREGUNTAS = 4
