"""Limpieza y normalización de texto antes del chunking.

Quita ruido del texto (espacios de más, saltos de línea raros) para que
el chunking produzca fragmentos más uniformes.
"""

import re

from langchain_core.documents import Document


def normalizar_texto(texto: str) -> str:
    """Aplica limpieza básica a una cadena de texto.

    Entrada: texto crudo de un documento.
    Salida: texto normalizado (sin espacios extra ni líneas vacías repetidas).
    """
    if not texto:
        return ""

    t = texto.replace("\r\n", "\n").replace("\r", "\n")
    t = re.sub(r"\n{3,}", "\n\n", t)
    t = re.sub(r"[ \t]+", " ", t)
    t = "\n".join(linea.strip() for linea in t.split("\n"))
    return t.strip()


def limpiar_documentos(documentos: list[Document]) -> list[Document]:
    """Normaliza el texto de cada Document y descarta los vacíos.

    Entrada: documentos cargados desde data/.
    Salida: documentos con page_content limpio (metadata se conserva).
    """
    limpios: list[Document] = []
    for doc in documentos:
        contenido = normalizar_texto(doc.page_content)
        if not contenido:
            continue
        limpios.append(
            Document(page_content=contenido, metadata=dict(doc.metadata))
        )
    return limpios
