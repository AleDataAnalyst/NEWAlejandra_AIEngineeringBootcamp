"""Fragmentación (chunking) de documentos con metadatos enriquecidos.

Divide textos largos en fragmentos más pequeños (chunks) que caben en el
contexto del modelo y son más fáciles de recuperar en un sistema RAG.
"""

from langchain_core.documents import Document
from langchain_text_splitters import RecursiveCharacterTextSplitter

from config import CHUNK_OVERLAP, CHUNK_SIZE


def _crear_splitter() -> RecursiveCharacterTextSplitter:
    """Configura el troceador con CHUNK_SIZE y CHUNK_OVERLAP de config.py."""
    return RecursiveCharacterTextSplitter(
        chunk_size=CHUNK_SIZE,
        chunk_overlap=CHUNK_OVERLAP,
        length_function=len,
    )


def fragmentar_documentos(documentos: list[Document]) -> list[Document]:
    """Divide documentos en chunks y añade metadatos de posición.

    Entrada: documentos limpios (texto completo de cada fuente).
    Salida: lista de chunks; cada uno lleva chunk_index (orden global)
    y chunk_size (longitud en caracteres).

    chunk_overlap hace que fragmentos vecinos compartan algo de texto
    para no cortar ideas a la mitad.
    """
    if not documentos:
        return []

    splitter = _crear_splitter()
    chunks = splitter.split_documents(documentos)

    enriquecidos: list[Document] = []
    for i, chunk in enumerate(chunks):
        meta = dict(chunk.metadata)
        meta["chunk_index"] = i
        meta["chunk_size"] = len(chunk.page_content)
        enriquecidos.append(
            Document(page_content=chunk.page_content, metadata=meta)
        )
    return enriquecidos
