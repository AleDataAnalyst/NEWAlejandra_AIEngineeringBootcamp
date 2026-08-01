"""Carga de documentos desde data/ — Sprint 8.

Convierte archivos del corpus en objetos Document de LangChain:
  page_content → texto que se chunkará y embeddeará
  metadata     → información para filtrar después (distrito, id_evento…)

Formatos: .txt, .md, .pdf y .csv (agenda cultural).
"""

from pathlib import Path

import pandas as pd
from langchain_community.document_loaders import PyPDFLoader, TextLoader
from langchain_core.documents import Document

from config import (
    DATA_DIR,
    EXTENSIONES_CSV,
    EXTENSIONES_PDF,
    EXTENSIONES_TEXTO,
)


def valor_celda(fila, columna: str) -> str | None:
    """Lee una celda del CSV y devuelve su texto, o None si está vacía."""
    if columna not in fila or pd.isna(fila[columna]):
        return None
    texto = str(fila[columna]).strip()
    return texto if texto else None


def fila_a_texto(fila) -> str | None:
    """Convierte UNA fila del CSV de agenda en un párrafo legible.

    Cada fila es un evento cultural. Si no tiene título, devuelve None.
    """
    titulo = valor_celda(fila, "TITULO")
    if titulo is None:
        return None

    lineas = [f"Evento: {titulo}"]

    descripcion = valor_celda(fila, "DESCRIPCION")
    if descripcion:
        lineas.append(f"Descripción: {descripcion}")

    actividad = valor_celda(fila, "TITULO-ACTIVIDAD")
    if actividad:
        lineas.append(f"Actividad: {actividad}")

    lugar = valor_celda(fila, "NOMBRE-INSTALACION")
    if lugar:
        lineas.append(f"Lugar: {lugar}")

    distrito = valor_celda(fila, "DISTRITO-INSTALACION")
    if distrito:
        lineas.append(f"Distrito: {distrito}")

    fecha = valor_celda(fila, "FECHA")
    if fecha:
        lineas.append(f"Fecha: {fecha}")

    hora = valor_celda(fila, "HORA")
    if hora:
        lineas.append(f"Hora: {hora}")

    if valor_celda(fila, "GRATUITO") == "1":
        lineas.append("Gratuito: sí")
    else:
        lineas.append("Gratuito: no")

    return "\n".join(lineas)


def cargar_agenda_csv(ruta: Path) -> list[Document]:
    """Lee el CSV de eventos: un Document por fila con título válido."""
    df = pd.read_csv(ruta, sep=";", encoding="latin-1")
    documentos: list[Document] = []

    for _, fila in df.iterrows():
        texto = fila_a_texto(fila)
        if texto is None:
            continue

        id_evento = valor_celda(fila, "ID-EVENTO")
        metadata: dict = {
            "source": str(ruta),
            "distrito": valor_celda(fila, "DISTRITO-INSTALACION"),
            "tipo": "agenda_evento",
        }
        if id_evento is not None:
            metadata["id_evento"] = id_evento

        documentos.append(Document(page_content=texto, metadata=metadata))

    return documentos


def cargar_archivo(ruta: Path) -> list[Document]:
    """Elige el loader según la extensión del archivo."""
    sufijo = ruta.suffix.lower()

    if sufijo in EXTENSIONES_PDF:
        return PyPDFLoader(str(ruta)).load()

    if sufijo in EXTENSIONES_TEXTO:
        return TextLoader(str(ruta), encoding="utf-8").load()

    if sufijo in EXTENSIONES_CSV:
        return cargar_agenda_csv(ruta)

    return []


def cargar_documentos() -> list[Document]:
    """Recorre data/ y concatena todos los Document soportados."""
    if not DATA_DIR.exists():
        raise FileNotFoundError(f"No existe la carpeta de datos: {DATA_DIR}")

    documentos: list[Document] = []

    for ruta in sorted(DATA_DIR.rglob("*")):
        if not ruta.is_file():
            continue

        docs = cargar_archivo(ruta)
        if docs:
            print(f"  Cargado: {ruta.name} ({len(docs)} documento(s))")
            documentos.extend(docs)
        elif ruta.suffix:
            print(f"  [omitido] extensión no soportada: {ruta.name}")

    return documentos
