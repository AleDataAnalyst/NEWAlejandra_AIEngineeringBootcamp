![Cabecera](../../assets/cabecera_rag.png)

# Flujo de indexación

## Objetivos

- Entender qué significa **indexar** embeddings en una base vectorial.
- Conocer los pasos del pipeline: vectores ya calculados → colección persistente.
- Manejar IDs, lotes (batches), metadatos válidos y cuándo **reindexar**.

---

## 1) Qué es indexar (en RAG)

En el Sprint 8 convertiste documentos en **chunks** y cada chunk en un **embedding**. Indexar es el paso siguiente:

> Guardar cada `(vector + texto + metadata)` en un almacén optimizado para búsqueda por similitud.

Sin indexación tienes un archivo (p. ej. JSON) con vectores: útil para inspeccionar, **inútil** como motor de búsqueda a escala. Con indexación, la BD vectorial construye estructuras internas (p. ej. HNSW) para responder rápido a «¿qué vectores están cerca de esta consulta?».

```text
  Documentos  →  chunks  →  embeddings  →  ÍNDICE vectorial  →  (más adelante) retrieval
       (S8)         (S8)         (S8)            (este bloque)         (Bloque 2)
```

**Importante:** indexar **no** vuelve a llamar al modelo de embeddings si los vectores ya existen. Solo los **persiste** y los hace consultables. Si cambias el chunking, el corpus o el modelo de embedding, hay que **regenerar** embeddings y **volver a indexar**.

---

## 2) Diagrama del flujo

Entrada típica: una lista de items (desde un JSON, una base, o memoria), cada uno con texto, vector y metadata.

```text
  Artefacto de embeddings
  ├── embedding_model   (p. ej. "gemini-embedding-2")
  ├── dimensions        (p. ej. 3072)
  └── items[]
        ├── text
        ├── vector[]
        └── metadata{}
              │
              ▼
         Proceso de indexación
              │
              ├─► abrir cliente persistente
              ├─► abrir / crear colección
              ├─► asignar id único por item
              ├─► sanitizar metadatas
              ├─► collection.add() (a menudo en lotes)
              └─► índice en disco (p. ej. carpeta chroma_db/)
```

En Chroma, cada `add` escribe cuatro listas **alineadas**:

| Campo Chroma | Contenido |
|--------------|-----------|
| `ids` | Identificador único del chunk en la colección |
| `embeddings` | Vector numérico |
| `documents` | Texto del chunk (lo que leerás luego como contexto) |
| `metadatas` | Fuente, índice, filtros… (`str` / `int` / `float` / `bool`) |

---

## 3) Pasos lógicos para indexar

Este sería el flujo general de indexación:

1. **Cliente** — conexión a la BD (en local: cliente persistente apuntando a una carpeta).
2. **Colección** — “cajón” del corpus con una métrica (p. ej. distancia coseno).
3. **Cargar items** — leer los embeddings ya calculados.
4. **Preparar listas** — `ids`, `embeddings`, `documents`, `metadatas` en el mismo orden.
5. **Insertar** — `collection.add(...)`, normalmente por **lotes**.
6. **Verificar** — `count()` (o equivalente) para comprobar cuántos vectores quedaron.

Si quieres partir de cero (corpus o modelo nuevos), **borra** la colección o la carpeta del índice y vuelve a indexar. Reindexar encima sin limpiar suele provocar **IDs duplicados**.

---

## 4) Generación de IDs

Cada registro necesita un **id único** dentro de la colección.

Buenas prácticas:

- Que sea **estable** entre ejecuciones si más adelante quieres actualizar o borrar un chunk concreto.
- Evitar colisiones (no reutilizar el mismo id para textos distintos).

Ejemplo habitual en pipelines de chunking:

```python
id = f"chunk_{metadata.get('chunk_index', i)}"
```

Otras convenciones válidas: hash del texto, `source + chunk_index`, UUID (menos cómodo si quieres idempotencia).

---

## 5) Indexación por lotes

Insertar miles de vectores de golpe puede ser lento o agotar memoria. Por eso se indexa en **batches** (p. ej. 50–200 items):

```python
BATCH_SIZE = 100

for inicio in range(0, len(ids), BATCH_SIZE):
    fin = inicio + BATCH_SIZE
    collection.add(
        ids=ids[inicio:fin],
        embeddings=embeddings[inicio:fin],
        documents=documents[inicio:fin],
        metadatas=metadatas[inicio:fin],
    )
```

El tamaño del lote es un detalle de ingeniería: prioriza estabilidad; ajústalo si el corpus crece.

---

## 6) Errores frecuentes

| Situación | Síntoma típico | Qué hacer |
|-----------|----------------|-----------|
| Reindexar sin limpiar | Error de ID duplicado | Borrar colección / carpeta del índice y volver a indexar |
| Dimensiones distintas | Error al `add` | Mismo modelo (y dimensión) en todo el pipeline |
| Metadata con `None` o listas | Error de tipo | Sanitizar: solo `str`, `int`, `float`, `bool` |
| Índice vacío | `count() == 0` | Comprobar que hay items de entrada y que el `add` se ejecutó |
| Cambiaste chunking o corpus | Retrieval raro / desactualizado | Regenerar embeddings **y** reindexar |

---

## 7) Qué sigue

Con la colección indexada, el siguiente bloque es el **retrieval**:

1. Embeddear la **pregunta** del usuario (mismo modelo que al indexar).
2. Ejecutar similarity search (`query`) sobre la colección.
3. Devolver los top-K fragmentos más cercanos.

Todavía **no** construyes el prompt ni generas la respuesta con un LLM: eso es la fase de generación (más adelante en el módulo).

---

## Resumen

- **Indexar** = persistir vectores + texto + metadata en una BD vectorial para poder buscar por similitud.
- El flujo es genérico: cliente → colección → listas alineadas → `add` (en lotes) → verificar.
- Usa IDs únicos, metadatos válidos y reindexa cuando cambien corpus, chunking o modelo de embedding.
