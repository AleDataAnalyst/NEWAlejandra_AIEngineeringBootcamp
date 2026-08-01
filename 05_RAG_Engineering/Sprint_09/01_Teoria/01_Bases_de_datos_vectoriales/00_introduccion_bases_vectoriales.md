![Cabecera](../../assets/cabecera_rag.png)

# Introducción: bases de datos vectoriales

En el Sprint 8 terminaste con `output/embeddings.json`: cada chunk del corpus tiene un **vector numérico** y metadatos. Ese archivo viene bien para hacer inspección y depuración, pero **no es un motor de búsqueda**.

En este bloque das el siguiente paso: **indexar** esos vectores en **ChromaDB**, una base de datos vectorial persistente.

> **Base de datos vectorial** = almacén optimizado para guardar embeddings y encontrar los más cercanos a una consulta.

![bbdd_vectoriales](../../assets/bbdd_vectoriales.png)

---

## Objetivos del bloque

Al terminar, deberías poder:

- Explicar qué es una BD vectorial y en qué se diferencia de una BD relacional.
- Crear una **colección** en ChromaDB con documentos, vectores y metadatos.
- Persistir el índice en disco (`output/chroma_db/`).
- Describir el **flujo de indexación** desde `embeddings.json`.

---

## Dónde encaja en el pipeline

```text
  [ Sprint 8 ]
  chunks.json  →  embeddings.json
                         │
                         ▼
  [ Bloque 1 — indexar en ChromaDB ]
  index.py  →  ChromaDB (colección indexada)
                         │
                         ▼
  [ Bloque 2 - retrieval  desde ChromaDB]
  retriever.py  →  similarity search + top-K
```

Todavía **no** embeddeas la pregunta del usuario ni llamas al LLM. Solo **almacenas** el conocimiento de forma recuperable.

---

## Puente desde Sprint 8

| Artefacto S8 | Qué contiene | Uso en S9 |
|--------------|--------------|-----------|
| `chunks.json` | Texto + metadata por fragmento | Referencia; Chroma guarda el texto en `documents` |
| `embeddings.json` | Texto + vector + metadata | Entrada directa de `index.py` |
| `config.EMBEDDING_MODEL` | p. ej. `gemini-embedding-2` | Debe coincidir al embeddear consultas (Bloque 2) |

Si ejecutaste el proyecto de S8 con `MAX_CHUNKS_EMBED = 5`, tu índice tendrá 5 vectores. Para un retrieval más realista, pon `MAX_CHUNKS_EMBED = None` y reindexa.

---

## Salida concreta

Carpeta `output/chroma_db/` con una colección (p. ej. `agenda_cultural_madrid` o `calidad_aire_madrid` que son los que veremos en los proyectos) que contiene:

- **ids** — identificador único por chunk
- **embeddings** — vectores de 3072 dimensiones (con `gemini-embedding-2`)
- **documents** — texto del chunk
- **metadatas** — `source`, `chunk_index`, `distrito`, etc.