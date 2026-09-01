"""Limpieza de texto antes del chunking — Sprint 8 (dado)."""

import re

from langchain_core.documents import Document


def normalizar_texto(texto: str) -> str:
    """Deja el texto listo para fragmentar: menos ruido, mismas frases."""
    if not texto:
        return ""

    t = texto.replace("\r\n", "\n").replace("\r", "\n")
    t = re.sub(r"\n{3,}", "\n\n", t)
    t = re.sub(r"[ \t]+", " ", t)
    t = "\n".join(linea.strip() for linea in t.split("\n"))
    return t.strip()


def limpiar_documentos(documentos: list[Document]) -> list[Document]:
    """Aplica normalizar_texto a cada documento; omite los que quedan vacíos."""
    limpios: list[Document] = []
    for doc in documentos:
        contenido = normalizar_texto(doc.page_content)
        if not contenido:
            continue
        limpios.append(
            Document(page_content=contenido, metadata=dict(doc.metadata))
        )
    return limpios
