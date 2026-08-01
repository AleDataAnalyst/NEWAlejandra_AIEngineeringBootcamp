![Cabecera](../../assets/cabecera_rag.png)

# Configuración básica del retriever

## Objetivos

- Centralizar parámetros del retriever en `config.py`.
- Diseñar un **retriever modular** (función/clase propia, no caja negra).
- Conocer el wrapper LangChain como alternativa, sin depender de él.

---

## 1) Parámetros en `config.py`

Mostramos un ejemplo de configuración del retriever, que podría ir en tu proyecto en el fichero `config.py`:

| Variable | Valor por defecto | Efecto |
|----------|-------------------|--------|
| `TOP_K` | `3` | Fragmentos devueltos por consulta |
| `COLLECTION_NAME` | `agenda_cultural_madrid` | Colección Chroma |
| `CHROMA_DIR` | `output/chroma_db` | Persistencia |
| `EMBEDDING_MODEL` | `gemini-embedding-2` | Debe coincidir con el índice |

Cambiar `TOP_K` no requiere reindexar. Cambiar `CHUNK_SIZE` o el corpus **sí**.

---

## 2) Interfaz del retriever

Podemos ver el ejemplo de la función python `recuperar()`, que representará el retriever en tu proyecto:

Contrato mínimo del módulo `retriever.py`:

```python
def recuperar(pregunta: str, top_k: int | None = None) -> list[dict]:
    """Devuelve chunks ordenados por relevancia."""
```

Cada item incluye `text`, `metadata`, `distance`, `id`.

Ejemplo de retorno de la función `recuperar()`:

```python
[
    {
        "text": "Texto del chunk",
        "metadata": {"distrito": "RETIRO"},
        "distance": 0.123
    },
    {
        "text": "Texto del chunk",
        "metadata": {"distrito": "HORTALEZA"},
        "distance": 0.124
    },
    {
        "text": "Texto del chunk",
        "metadata": {"distrito": "MORATALAZ"},
        "distance": 0.125
    },
]
```
Ventajas de este diseño:

- **Testeable** sin LLM.
- **Sustituible** (otro vector store, otro embedder).
- **Legible** en code reviews de AI Engineering.

---

## 3) Filtros por metadata (opcional)

Chroma permite `where` en `query()`:

```python
collection.query(
    query_embeddings=[vector],
    n_results=k,
    where={"distrito": "RETIRO"},
)
```

Útil cuando la pregunta menciona un distrito concreto. Cuidado: un filtro demasiado estricto puede devolver **cero** resultados si la metadata no coincide exactamente (mayúsculas, tildes).

El filtro es **opcional**; el camino principal es búsqueda semántica sin filtro. Se usa el filtro para buscar los chunks más relevantes para la pregunta, pero en el Sprint 10 se puede usar también para buscar los chunks que tengan una metadata específica, por ejemplo, el distrito.

---

## 4) LangChain como referencia (no como camino principal)

Vemos un ejemplo conceptual de código de cómo se podría usar LangChain para el retriever. 

LangChain ofrece abstracciones como:

```python
# Referencia conceptual — no es el código del proyecto
from langchain_chroma import Chroma
from langchain_google_genai import GoogleGenerativeAIEmbeddings

vectorstore = Chroma(persist_directory="...", embedding_function=embeddings)
retriever = vectorstore.as_retriever(search_kwargs={"k": 3})
docs = retriever.invoke("¿Hay cine gratuito?")
```

Lo importante es **entender cada paso** del proceso de retrieval en el curso. En producción puedes envolver tu `recuperar()` o adoptar LangChain si el equipo ya lo estandariza.

---

## 5) CLI del proyecto

Vemos un ejemplo de cómo se podría usar la línea de comandos para ejecutar el retriever.

```bash
python main.py --query "¿Hay cine gratuito en agosto?" --top-k 5
```

| Flag | Acción |
|------|--------|
| `--query` | Ejecuta retrieval + muestra contexto |
| `--top-k` | Sobrescribe `TOP_K` de config |

---

## Resumen

- Configura K, colección y modelo en un solo sitio.
- El retriever es una función con contrato claro: pregunta → lista de chunks.
- LangChain existe como atajo; aquí dominas la API directa primero.
