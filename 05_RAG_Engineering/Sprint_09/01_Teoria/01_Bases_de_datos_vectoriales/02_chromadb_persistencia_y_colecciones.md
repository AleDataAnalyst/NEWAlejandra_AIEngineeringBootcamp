![Cabecera](../../assets/cabecera_rag.png)

# ChromaDB: persistencia, colecciones y metadatos

## Objetivos

- Instalar y configurar **ChromaDB** en modo persistente.
- Entender **cliente**, **colección** y carpeta en disco.
- Saber qué tipos de datos acepta Chroma en `metadatas`.

---

## 1) Por qué ChromaDB

![chroma_db](../../assets/chromaDB.webp)

ChromaDB es una base vectorial **ligera** y **local**: no necesitas servidor ni cuenta en la nube para practicar. Encaja con el enfoque modular del curso: ves exactamente qué entra en `collection.add()` y qué sale de `collection.query()`.

En producción podrías usar Pinecone, Weaviate o pgvector; el **patrón** (indexar → consultar) es el mismo.

> **Nota sobre LangChain:** existe `langchain_chroma.Chroma` como wrapper. En este sprint usamos la **API directa** de `chromadb` para no ocultar el flujo. En teoría del Bloque 2 verás cuándo un wrapper puede simplificar el código. 

![chromadb_langchain](../../assets/chromaDB_langchain.png)

---

## 2) Instalación

```bash
pip install chromadb
```
---

## 3) Cliente persistente

```python
import chromadb

client = chromadb.PersistentClient(path="output/chroma_db")
```

| Modo | Comportamiento |
|------|----------------|
| `PersistentClient` | Guarda el índice en `output/chroma_db/` entre ejecuciones |
| `EphemeralClient` | Solo en memoria; desaparece al cerrar el proceso |

Para RAG offline/online en local, **persistencia** es lo habitual: indexas una vez y consultas muchas.

---

## 4) Colecciones

Una **colección** agrupa vectores del mismo corpus y la misma configuración de distancia.

```python
collection = client.get_or_create_collection(
    name="agenda_cultural_madrid",
    metadata={"hnsw:space": "cosine"},
)
```

| Concepto | Analogía |
|----------|----------|
| Cliente | Conexión a la «base de datos» |
| Colección | Tabla / índice de un corpus concreto |
| `hnsw:space: cosine` | Métrica de similitud (coherente con embeddings normalizados) |

Convención del proyecto: **una colección** por corpus de agenda cultural. Si mañana indexas otro dominio, crea otra colección o borra y recrea la existente.

---

## 5) Añadir documentos indexados

```python
collection.add(
    ids=["chunk_0", "chunk_1"],
    embeddings=[[0.1, 0.2, ...], [0.3, -0.1, ...]],
    documents=["Texto del chunk 0", "Texto del chunk 1"],
    metadatas=[
        {"source": "data/faq_agenda_cultural.md", "chunk_index": 0},
        {"source": "data/guia_agenda_cultural.txt", "chunk_index": 1},
    ],
)
```

Reglas importantes:

- **`ids`** deben ser únicos dentro de la colección.
- **`embeddings`** y **`documents`** van en el mismo orden que `ids`.
- **`metadatas`**: solo valores `str`, `int`, `float` o `bool`. Convierte `None` u otros tipos a string antes de indexar.
---

## 6) Inspeccionar la colección

```python
print(collection.count())          # cuántos vectores hay
print(collection.peek(limit=2))    # muestra de ids, documents, metadatas
```

Útil tras indexar para verificar que el número de chunks coincide con `embeddings.json`.

---

## 7) Estructura en disco

Tras indexar verás algo como:

```text
output/chroma_db/
  ├── chroma.sqlite3
  └── ... (segmentos del índice HNSW)
```

No edites estos archivos a mano. Para **reindexar** desde cero, borra `chroma_db/` o usa `client.delete_collection()` y vuelve a ejecutar el script de indexación.

---

## Referencias

### ChromaDB

- [Documentación Chroma (inicio)](https://docs.trychroma.com/docs/overview/introduction) — visión general del producto y conceptos
- [Clients (`PersistentClient`, etc.)](https://docs.trychroma.com/docs/run-chroma/clients) — cliente local persistente (lo que usamos en el curso)
- [Gestionar colecciones](https://docs.trychroma.com/docs/collections/manage-collections) — `create` / `get` / `get_or_create` / `delete`
- [Añadir datos (`add`)](https://docs.trychroma.com/docs/collections/add-data) — `ids`, `embeddings`, `documents`, `metadatas`
- [Consultar (`query`)](https://docs.trychroma.com/docs/querying-collections/query-and-get) — similarity search (lo verás en el Bloque 2)
- [Cookbook — clients](https://cookbook.chromadb.dev/core/clients/) — ejemplos prácticos de clientes Python
- [Repo `chroma-core/chroma`](https://github.com/chroma-core/chroma) — código fuente e issues
- [PyPI `chromadb`](https://pypi.org/project/chromadb/) — versiones del paquete `pip install chromadb`

### LangChain + Chroma (referencia / alternativa)

- [Integración Chroma (Python)](https://docs.langchain.com/oss/python/integrations/vectorstores/chroma) — wrapper `langchain_chroma.Chroma` (persistencia, query, retriever)
- [Provider Chroma en LangChain](https://docs.langchain.com/oss/python/integrations/providers/chroma) — instalación `langchain-chroma` y overview
- [Vector stores en LangChain](https://docs.langchain.com/oss/python/integrations/vectorstores) — contexto: Chroma como una integración más entre muchas
- [PyPI `langchain-chroma`](https://pypi.org/project/langchain-chroma/) — paquete del wrapper (si lo pruebas por tu cuenta)

---

## Resumen

- ChromaDB persiste embeddings + texto + metadata en una carpeta local.
- Una **colección** = un índice vectorial de tu corpus.
- `collection.add()` es el corazón de la indexación; controlas cada campo.
