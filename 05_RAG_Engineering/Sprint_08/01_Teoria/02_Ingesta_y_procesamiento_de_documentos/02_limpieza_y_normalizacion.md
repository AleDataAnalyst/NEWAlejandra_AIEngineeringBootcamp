![Cabecera](../../assets/cabecera_rag.png)

# Limpieza y normalización de texto

Los loaders devuelven texto **tal como está en el archivo**. Ese texto suele traer ruido: saltos de línea excesivos, espacios dobles, caracteres raros de copiar/pegar desde PDFs.

La limpieza **no** tiene que ser perfecta. En RAG buscas un **mínimo viable** que mejore chunks y embeddings sin destruir el contenido.

---

## Objetivos

- Identificar **ruido típico** tras cargar documentos.
- Aplicar normalizaciones simples en Python.
- Mantener la limpieza en un módulo **`clean.py`** separado del loader.

---

## 1) Por qué limpiar antes del chunking

| Problema en texto bruto | Efecto en RAG |
|-----------------------|---------------|
| `\n\n\n\n` repetidos | Chunks con huecos vacíos; embeddings pobres |
| Espacios múltiples | Fragmentos artificialmente largos |
| Guiones de final de línea (`palabra-\ncontinuación`) | Palabras partidas en dos chunks |
| Headers/footers repetidos en PDF | Chunks duplicados irrelevantes |

Chunking sobre texto sucio → retrieval peor en Sprint 9, aunque el LLM sea bueno.

---

## 2) Normalizaciones mínimas recomendadas

```python
import re


def normalizar_texto(texto: str) -> str:
    """Limpieza básica: espacios, saltos de línea, strip."""
    if not texto:
        return ""

    # Unificar saltos de línea Windows/Mac
    t = texto.replace("\r\n", "\n").replace("\r", "\n")

    # Colapsar más de 2 saltos seguidos en 2 (conserva párrafos)
    t = re.sub(r"\n{3,}", "\n\n", t)

    # Colapsar espacios/tabs múltiples en uno (excepto saltos de línea)
    t = re.sub(r"[ \t]+", " ", t)

    # Quitar espacios al inicio/fin de cada línea
    t = "\n".join(linea.strip() for linea in t.split("\n"))

    return t.strip()
```

**No sobre-limpies:** quitar toda puntuación o pasar a minúsculas puede empeorar la recuperación de nombres propios o códigos.

---

## 3) Aplicar limpieza a una lista de Document

Patrón: **inmutabilidad razonable** — devuelves nuevos documentos o modificas `page_content` conservando metadatos:

```python
from langchain_core.documents import Document


def limpiar_documentos(documentos: list[Document]) -> list[Document]:
    limpios = []
    for doc in documentos:
        contenido = normalizar_texto(doc.page_content)
        if not contenido:
            continue  # omitir páginas vacías tras limpiar
        limpios.append(
            Document(page_content=contenido, metadata=dict(doc.metadata))
        )
    return limpios
```

Omitir páginas vacías evita chunks inútiles en el índice.

---

## 4) Ruido específico de PDFs

| Síntoma | Qué hacer (básico) |
|---------|-------------------|
| Palabras cortadas con guión al final de línea | Unir `-\n` → `` (opcional, según corpus) |
| Numeración de página en cada hoja | Difícil sin reglas; a veces se filtra en post-proceso |
| Columnas mezcladas | Requiere parsers avanzados; fuera de alcance inicial |

Ejemplo opcional de unir palabras partidas:

```python
def unir_guiones_de_linea(texto: str) -> str:
    return re.sub(r"(\w)-\n(\w)", r"\1\2", texto)
```

Prueba **con y sin** esta regla en tu corpus antes de activarla siempre.

---

## 5) Markdown y TXT de la agenda

Archivos como `faq_agenda_cultural.md` y `guia_agenda_cultural.txt` suelen estar más limpios que PDFs exportados. Aun así conviene:

- Normalizar saltos de línea.
- Eliminar líneas vacías excesivas.
- Conservar encabezados `#` — ayudan al contexto semántico.

---

## 6) Dónde vive en el proyecto

```text
load.py   →  devuelve Document[] bruto
clean.py  →  devuelve Document[] normalizado
chunk.py  →  recibe solo texto limpio
```

Si la limpieza falla, depuras **`clean.py`** sin tocar loaders ni splitters.

---

## Resumen

- Limpieza = **normalización mínima**, no reescritura del contenido.
- Colapsa espacios/saltos excesivos; omite páginas vacías.
- Implementa en **`clean.py`** entre load y chunk.
- PDFs reales pueden necesitar reglas extra más adelante.