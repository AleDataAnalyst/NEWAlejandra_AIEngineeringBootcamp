"""Orquestación del pipeline de ingesta — Sprint 8.

Flujo: load → clean → chunk → guardar chunks.json

Prepara los fragmentos de texto que embed.py convertirá en vectores.
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
    """Nombre de archivo a partir de metadata['source'] (p. ej. faq_agenda_cultural.md)."""
    source = metadata.get("source", "desconocido")
    return Path(str(source)).name


def calcular_stats_ingesta(
    crudos: list[Document],
    limpios: list[Document],
    chunks: list[Document],
) -> dict:
    """Resumen numérico para consola y para ingesta_stats en chunks.json."""
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
    """Convierte Document de LangChain a dict serializable en JSON."""
    return [
        {"text": doc.page_content, "metadata": dict(doc.metadata)}
        for doc in documentos
    ]


def guardar_chunks_json(chunks: list[Document], ruta: Path, stats: dict) -> Path:
    """Escribe output/chunks.json con configuración usada y estadísticas."""
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
    print(f"\n--- {titulo} ---")
    print(chunk.page_content[:350].strip(), "...")
    print("Metadata:", chunk.metadata)


def imprimir_resumen_consola(chunks: list[Document], stats: dict) -> None:
    """Muestra conteos por fuente y una muestra de chunks (FAQ/evento CSV)."""
    print("\n--- Resumen ingesta ---")
    print(f"  Documentos cargados:      {stats['documentos_cargados']}")
    print(f"  Tras limpieza:            {stats['documentos_tras_limpieza']}")
    print(f"  Chunks generados:         {stats['chunks_generados']}")
    print("  Chunks por fuente:")
    for fuente, n in sorted(stats["chunks_por_fuente"].items()):
        print(f"    {fuente}: {n}")

    if not chunks:
        return

    _mostrar_chunk_ejemplo("Muestra: primer chunk", chunks[0])

    for chunk in chunks:
        if chunk.metadata.get("tipo") == "agenda_evento":
            _mostrar_chunk_ejemplo("Muestra: evento de agenda", chunk)
            break


def ejecutar_ingesta() -> tuple[list[Document], Path, dict]:
    """Paso a paso de la ingesta hasta generar chunks.json."""
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
