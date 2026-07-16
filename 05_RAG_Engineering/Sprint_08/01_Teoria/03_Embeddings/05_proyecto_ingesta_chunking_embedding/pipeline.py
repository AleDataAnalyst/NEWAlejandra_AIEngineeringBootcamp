"""Orquestación del pipeline de ingesta: load → clean → chunk → JSON.

Une los tres módulos de preparación de datos y guarda el resultado en chunks.json.
"""

import json
from collections import Counter
from pathlib import Path

from langchain_core.documents import Document

from chunk import fragmentar_documentos
from clean import limpiar_documentos
from config import CHUNK_OVERLAP, CHUNK_SIZE, CHUNKS_JSON, DATA_DIR
from load import cargar_documentos


def _nombre_fuente(metadata: dict) -> str:
    """Extrae el nombre del archivo desde metadata['source'].

    Entrada: dict de metadata de un Document.
    Salida: nombre de archivo (ej. 'faq_agenda_cultural.md').
    """
    source = metadata.get("source", "desconocido")
    return Path(str(source)).name


def calcular_stats_ingesta(
    crudos: list[Document],
    limpios: list[Document],
    chunks: list[Document],
) -> dict:
    """Calcula conteos del pipeline para el JSON y la consola.

    Entrada: documentos en cada etapa (carga, limpieza, chunking).
    Salida: dict con totales y desglose por archivo fuente.
    """
    return {
        "documentos_cargados": len(crudos),
        "documentos_tras_limpieza": len(limpios),
        "chunks_generados": len(chunks),
        "documentos_por_fuente": dict(
            Counter(_nombre_fuente(d.metadata) for d in crudos)
        ),
        "chunks_por_fuente": dict(
            Counter(_nombre_fuente(c.metadata) for c in chunks)
        ),
    }


def documentos_a_dicts(documentos: list[Document]) -> list[dict]:
    """Convierte Documents de LangChain al formato JSON del proyecto.

    Entrada: lista de Document (page_content + metadata).
    Salida: lista de dicts con claves 'text' y 'metadata'.
    """
    return [
        {"text": doc.page_content, "metadata": dict(doc.metadata)}
        for doc in documentos
    ]


def guardar_chunks_json(chunks: list[Document], ruta: Path, stats: dict) -> Path:
    """Escribe chunks.json con la configuración usada y estadísticas.

    Entrada: chunks finales, ruta de salida y stats de ingesta.
    Salida: ruta del archivo guardado.
    """
    ruta.parent.mkdir(parents=True, exist_ok=True)
    payload = {
        "chunk_size_config": {
            "chunk_size": CHUNK_SIZE,
            "chunk_overlap": CHUNK_OVERLAP,
        },
        "total_chunks": len(chunks),
        "ingesta_stats": stats,
        "chunks": documentos_a_dicts(chunks),
    }

    ruta.write_text(
        json.dumps(payload, ensure_ascii=False, indent=2),
        encoding="utf-8",
    )
    return ruta


def _mostrar_chunk_ejemplo(titulo: str, chunk: Document) -> None:
    """Imprime un fragmento de texto y su metadata (máx. 350 caracteres)."""
    print(f"\n--- {titulo} ---")
    print(chunk.page_content[:350].strip(), "...")
    print("Metadata:", chunk.metadata)


def imprimir_resumen_consola(chunks: list[Document], stats: dict) -> None:
    """Muestra en consola un resumen legible tras la ingesta.

    Entrada: chunks generados y estadísticas calculadas.
    Salida: impresión por pantalla (no devuelve valor).
    """
    print("\n--- Resumen ingesta ---")
    print(f"  Documentos cargados:      {stats['documentos_cargados']}")
    print(f"  Tras limpieza:            {stats['documentos_tras_limpieza']}")
    print(f"  Chunks generados:         {stats['chunks_generados']}")
    print("  Chunks por fuente:")
    for fuente, n in sorted(stats["chunks_por_fuente"].items()):
        print(f"    {fuente}: {n}")

    if not chunks:
        return

    # Primer chunk del corpus (suele ser FAQ o guía)
    _mostrar_chunk_ejemplo("Muestra: primer chunk", chunks[0])

    # Primer evento del CSV, si existe
    for chunk in chunks:
        if chunk.metadata.get("tipo") == "agenda_evento":
            _mostrar_chunk_ejemplo("Muestra: evento de agenda", chunk)
            break


def ejecutar_ingesta() -> tuple[list[Document], Path, dict]:
    """Ejecuta load → clean → chunk y guarda output/chunks.json.

    Lee documentos desde config.DATA_DIR y escribe en config.CHUNKS_JSON.
    Salida: (chunks, ruta del JSON, estadísticas de ingesta).
    """
    print(f"Ingesta: cargando documentos desde {DATA_DIR} ...")
    crudos = cargar_documentos()
    print(f"  Documentos cargados: {len(crudos)}")

    limpios = limpiar_documentos(crudos)
    print(f"  Tras limpieza: {len(limpios)}")

    chunks = fragmentar_documentos(limpios)
    print(f"  Chunks generados: {len(chunks)}")

    stats = calcular_stats_ingesta(crudos, limpios, chunks)
    ruta = guardar_chunks_json(chunks, CHUNKS_JSON, stats)
    print(f"  Guardado: {ruta}")

    imprimir_resumen_consola(chunks, stats)

    return chunks, ruta, stats
