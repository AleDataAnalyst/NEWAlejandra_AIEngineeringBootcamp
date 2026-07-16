"""Carga de documentos desde data/ — Fase 1.

Convierte archivos del corpus en objetos Document de LangChain:
  page_content → texto que se chunkará y embeddeará
  metadata     → información para filtrar después (estación, magnitud…)

Formatos: .txt, .md, .pdf y .csv (mediciones). Se omiten .json y README.md.
"""

from pathlib import Path

import pandas as pd
from langchain_community.document_loaders import PyPDFLoader, TextLoader
from langchain_core.documents import Document

from config import (
    CSV_METEO,
    DATA_DIR,
    EXTENSIONES_CSV,
    EXTENSIONES_PDF,
    EXTENSIONES_TEXTO,
    MAGNITUDES,
    MAX_FILAS_CSV,
)

# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------


def valor_celda(fila, columna: str) -> str | None:
    """Lee una celda del CSV y devuelve su texto, o None si está vacía."""
    if columna not in fila or pd.isna(fila[columna]):
        return None
    texto = str(fila[columna]).strip()
    return texto if texto else None


# ---------------------------------------------------------------------------
# Ingesta del CSV meteorológico (ver README)
# ---------------------------------------------------------------------------


def nombre_magnitud(codigo) -> str:
    """Devuelve el nombre legible de una magnitud (81, 82, 83…).

    Pista: usa el diccionario MAGNITUDES de config.py.
    """
    raise NotImplementedError("Completa nombre_magnitud() en load.py")


def fila_meteo_a_texto(fila) -> str | None:
    """Convierte UNA fila del CSV meteorológico en texto legible.

    Debe incluir al menos:
    - magnitud (código + nombre)
    - municipio, estación, punto_muestreo
    - fecha (ano, mes, dia)
    - un resumen de las horas h01-h24 con su validación v01-v24

    Pista: bucle for hora in range(1, 25) y columnas h01…h24, v01…v24.

    Si la fila no tiene magnitud, devuelve None.
    """
    raise NotImplementedError("Completa fila_meteo_a_texto() en load.py")


def cargar_meteo_csv(ruta: Path) -> list[Document]:
    """Lee el CSV meteorológico: un Document por fila válida.

    Pistas:
    - sep=';' y encoding='utf-8'
    - respeta MAX_FILAS_CSV de config.py
    - metadata: source, magnitud, municipio, estacion, punto_muestreo, tipo='meteo_medicion'
    """
    raise NotImplementedError("Completa cargar_meteo_csv() en load.py")


# ---------------------------------------------------------------------------
# Carga del corpus
# ---------------------------------------------------------------------------


def cargar_archivo(ruta: Path) -> list[Document]:
    """Elige el loader según la extensión del archivo."""
    sufijo = ruta.suffix.lower()

    if sufijo in EXTENSIONES_PDF:
        return PyPDFLoader(str(ruta)).load()

    if sufijo in EXTENSIONES_TEXTO:
        return TextLoader(str(ruta), encoding="utf-8").load()

    if sufijo in EXTENSIONES_CSV:
        return cargar_meteo_csv(ruta)

    return []


def cargar_documentos() -> list[Document]:
    """Recorre data/ y concatena todos los Document soportados."""
    if not DATA_DIR.exists():
        raise FileNotFoundError(f"No existe la carpeta de datos: {DATA_DIR}")

    csv_path = DATA_DIR / CSV_METEO
    if not csv_path.is_file():
        raise FileNotFoundError(
            f"Falta {CSV_METEO} en data/. Comprueba que el corpus está en la carpeta data/."
        )

    documentos: list[Document] = []

    for ruta in sorted(DATA_DIR.rglob("*")):
        if not ruta.is_file():
            continue
        if ruta.suffix.lower() == ".json":
            continue
        if ruta.name == "README.md":
            continue

        docs = cargar_archivo(ruta)
        if docs:
            print(f"  Cargado: {ruta.name} ({len(docs)} documento(s))")
            documentos.extend(docs)
        elif ruta.suffix:
            print(f"  [omitido] extensión no soportada: {ruta.name}")

    return documentos
