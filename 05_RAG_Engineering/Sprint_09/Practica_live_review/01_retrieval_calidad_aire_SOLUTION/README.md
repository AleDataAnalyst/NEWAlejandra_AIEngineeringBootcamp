![Cabecera](../../assets/cabecera_rag.png)

# Práctica Sprint 09 — Retrieval calidad del aire Madrid

**Práctica integradora (Live Review)** del Sprint 9 — Retrieval & Vector Search.

Continúa el pipeline del Live Review de Sprint 8 (calidad del aire): la **ingesta, chunking y embeddings ya están dados**. Aquí implementas **indexación en ChromaDB**, **retrieval** y **evaluación del retrieval**.

Esta será el pipeline de RAG que tendremos tras finalizar el ejercicio:

ingesta -> chunking -> embeddings -> indexación en ChromaDB -> retrieval -> evaluación del retrieval

> Todavía **no** generas respuestas con un LLM. Esta última parte la veremos más adelante.

---

## Empieza aquí

### Fase 0 —  Código completado con conceptos vistos en el Sprint 8. Ejecutar el siguiente comando para preparar los artefactos necesarios para el ejercicio.

- [ ] **1.** `python main.py --prepare` → `output/chunks.json` + `output/embeddings.json`

### Fase 1 — Indexar en Chroma (`index.py`)

- [ ] **2.** `obtener_cliente_chroma()`
- [ ] **3.** `obtener_coleccion()`
- [ ] **4.** `ejecutar_indexacion()`
- [ ] **5.** `python main.py --index` → `output/chroma_db/`
- [ ] **6.** `python main.py --check` muestra `[OK] index.py`

### Fase 2 — Retrieval (`retriever.py`)

- [ ] **7.** `recuperar(pregunta, top_k)`
- [ ] **8.** `python main.py --query "¿Qué mide la magnitud 83?"`
- [ ] **9.** `python main.py --check` muestra `[OK] retriever.py`

### Fase 3 — Evaluación (`eval_retrieval.py` + entregable)

- [ ] **10.** `evaluar_pregunta()` y `ejecutar_evaluacion()`
- [ ] **11.** `python main.py --eval`
- [ ] **12.** Completa `entregables/reflexion_retrieval.md`
- [ ] **13.** `python main.py --check` muestra todo `[OK]`

### Archivos que **no debes modificar**

`load.py`, `clean.py`, `chunk.py`, `pipeline.py`, `embed.py`, `gemini_auth.py`, `context.py`, `main.py`, `verificar.py`, `config.py` (puedes **cambiar valores** como `TOP_K` / `MAX_CHUNKS_EMBED` para experimentar).

---

## Corpus en `data/`

| Archivo | Rol |
|---------|-----|
| `faq_calidad_aire.md` | Preguntas frecuentes |
| `guia_calidad_aire.txt` | Resumen de campos |
| `descripcion-fichero-open-data-meteorologico-v2.pdf` | Documentación oficial |
| `calidad_aire_datos_meteo_mes.csv` | Mediciones horarias |

---

## Requisitos

- Python 3.10+
- `GEMINI_API_KEY` en [Google AI Studio](https://aistudio.google.com/apikey)

## Entorno virtual

**Linux / macOS / Git Bash:**

```bash
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
cp .env.example .env
python main.py --check
```

**Windows (PowerShell):**

```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
pip install -r requirements.txt
copy .env.example .env
python main.py --check
```

---

## Estructura del proyecto

```text
.
├── README.md
├── requirements.txt
├── .env.example              # plantilla de variables
├── .env                      # tu clave (no se sube a git)
├── .gitignore
├── config.py                 # CHUNK_*, CHROMA_*, TOP_K, …
├── load.py … embed.py        # Sprint 8 (dado)
├── context.py                # formatear contexto (dado)
├── index.py                  # ← Fase 1
├── retriever.py              # ← Fase 2
├── eval_retrieval.py         # ← Fase 3
├── main.py, verificar.py
├── queries/preguntas_eval.json
├── entregables/reflexion_retrieval.md
├── data/
└── output/
```

---

## Secuencia recomendada

```text
python main.py --prepare
python main.py --index
python main.py --query "¿Qué mide la magnitud 83?"
python main.py --eval
# Completa entregables/reflexion_retrieval.md
python main.py --check
```

---

## FASE 1 — Indexar en ChromaDB (`index.py`)

### Objetivo

Pasar de `embeddings.json` a una colección Chroma persistente en `output/chroma_db/`.

### Pistas

- `PersistentClient(path=str(CHROMA_DIR))`
- `get_or_create_collection(name=COLLECTION_NAME, metadata={"hnsw:space": "cosine"})`
- Por cada item: `ids`, `embeddings` (= `item["vector"]`), `documents` (= `item["text"]`), `metadatas` (sanitizadas)
- Inserta en lotes con `INDEX_BATCH_SIZE`
- Usa `cargar_embeddings_json()`, `_generar_id()` y `_sanitizar_metadata()` (ya dados)

### Criterios de aceptación

- [ ] `python main.py --check` → `[OK] index.py`
- [ ] `python main.py --index` crea `output/chroma_db/` y muestra un total > 0

---

## FASE 2 — Retrieval (`retriever.py`)

### Objetivo

Dada una pregunta, devolver los top-K chunks más similares.

### Pistas

- Mismo modelo: `embeddear_consulta(client, pregunta)` (en `embed.py`)
- `obtener_coleccion(client, crear=False)`
- `collection.query(query_embeddings=[vector], n_results=min(k, collection.count()), include=["documents", "metadatas", "distances"])`
- Convierte el resultado con `_resultados_a_chunks()` e imprime con `_imprimir_hits()` (dados)

### Criterios de aceptación

- [ ] `python main.py --query "¿Qué mide la magnitud 83?"` imprime hits con distance y fuente
- [ ] El contexto formateado aparece bajo `--- Contexto recuperado ---`

---

## FASE 3 — Evaluación del retrieval (`eval_retrieval.py`)

### Objetivo

Barrido de `queries/preguntas_eval.json` con K ∈ `{1, 3, 5}` y reflexión escrita.

### Pistas

- `evaluar_pregunta`: llama a `recuperar`, toma el mejor hit (`chunks[0]`) y arma el dict resumen
- `ejecutar_evaluacion`: recorre preguntas × valores de `TOP_K_CANDIDATES` e imprime filas `K=… → mejor=… distance=…`
- `fuente_esperada` es **orientativa**, no un test automático

### Criterios de aceptación

- [ ] `python main.py --eval` recorre todas las preguntas
- [ ] `reflexion_retrieval.md` sin TODO y con números reales
