![Cabecera](../../../assets/cabecera_rag.png)

# Proyecto ejemplo: RAG. Retrieval y búsqueda semántica

Pipeline **acumulativo** de RAG: documentos → chunks → embeddings → ChromaDB → retrieval.

Extiende el proyecto de ingesta del Sprint 8: el corpus queda **indexado** y, dada una pregunta, devuelve los fragmentos más relevantes. Todavía **no** genera respuestas con un LLM. Esto lo veremos más adelante.

**Requisitos:** Python 3.10+ y `GEMINI_API_KEY` en `.env`.

**Corpus:** agenda cultural de Madrid. Cuatro fuentes en `data/`:

| Archivo | Formato | Contenido |
|---------|---------|-----------|
| `faq_agenda_cultural.md` | Markdown | Preguntas frecuentes |
| `guia_agenda_cultural.txt` | Texto | Guía del dataset |
| `206974-3-agenda-eventos-culturales-100.pdf` | PDF | Documentación oficial |
| `206974-4-agenda-eventos-culturales-100-csv.csv` | CSV | Eventos (una fila = un documento) |

**Modelo de embedding:** `gemini-embedding-2` (3072 dimensiones). Configurable en `config.py` → `EMBEDDING_MODEL`.

**Retrieval:** `TOP_K = 3` por defecto (`config.py` → `TOP_K`).

---

## Instalación

```bash
python -m venv .venv
source .venv/bin/activate          # Git Bash / macOS / Linux
# .venv\Scripts\Activate.ps1       # Windows PowerShell

pip install -r requirements.txt
cp .env.example .env               # define GEMINI_API_KEY
```

---

## Ejecución

```bash
# Primera vez: pipeline offline + indexación
python main.py --prepare --index

# Consulta de prueba
python main.py --query "¿Hay cine gratuito en verano?"

# Evaluación con preguntas fijas
python main.py --eval
```

Por defecto `MAX_CHUNKS_EMBED = 5` en `config.py` (demo rápida). Pon `None` para embeddear todo el corpus antes de indexar.

**Secuencia recomendada:**

```text
python main.py --prepare     →  output/chunks.json + embeddings.json
python main.py --index       →  output/chroma_db/
python main.py --query "…"   →  contexto en consola
python main.py --eval        →  barrido K = 1, 3, 5
```

---

## Estructura

```text
.
├── .env.example           # plantilla; copiar a .env con tu GEMINI_API_KEY
├── config.py              # chunking, Chroma, TOP_K, rutas
├── gemini_auth.py         # carga GEMINI_API_KEY desde .env
│
│   # Sprint 8 — preparación
├── load.py
├── clean.py
├── chunk.py
├── pipeline.py
├── embed.py
│
│   # Sprint 9 — index + retrieve + eval
├── index.py
├── retriever.py
├── context.py
├── eval_retrieval.py
│
├── main.py                # CLI (--prepare, --index, --query, --eval)
├── data/
├── queries/preguntas_eval.json
└── output/
    ├── chunks.json
    ├── embeddings.json
    └── chroma_db/
```

---

## Orden recomendado al explorar el código

1. `data/` — qué documentos entran al pipeline.
2. `config.py` — `CHUNK_SIZE`, `EMBEDDING_MODEL`, `TOP_K`, `COLLECTION_NAME`.
3. **Sprint 8:** `load.py` → `clean.py` → `chunk.py` → `pipeline.py` → `embed.py`.
4. **Sprint 9:** `index.py` → `retriever.py` → `context.py` → `eval_retrieval.py`.
5. `main.py` — cómo se encadenan los comandos.
6. Tras ejecutar: inspecciona consola, `chunks.json`, `embeddings.json` y una consulta `--query`.

---

## Flujo del pipeline

```text
SPRINT 8 — preparación offline
──────────────────────────────────────────────────────────────────
  data/  →  load  →  clean  →  chunk  →  pipeline  →  chunks.json
                                              │
                                              ▼
                                         embed.py ──► Gemini
                                              │
                                              ▼
                                      embeddings.json

SPRINT 9 — indexación y búsqueda
──────────────────────────────────────────────────────────────────
  embeddings.json  →  index.py  →  chroma_db/
                                       ▲
  Pregunta  →  retriever.py ───────────┘  (embed pregunta + similarity search)
                    │
                    ▼
               context.py
```

**Idea clave:** los chunks se embeddean **una vez** al indexar; en cada consulta solo embeddeas la **pregunta** (mismo modelo) y buscas vecinos en Chroma.

---

## Qué mirar tras ejecutar

### `python main.py --prepare` (ingesta + embeddings)

| Qué mirar | Dónde |
|-----------|--------|
| Archivos cargados | Consola → `Cargado: …` |
| Chunks por fuente | Consola → «Resumen ingesta» o `ingesta_stats` en `chunks.json` |
| Modelo y dimensiones | Consola y raíz de `embeddings.json` |
| Texto + metadata + vector | `items[0]` en `embeddings.json` (debe coincidir con un chunk) |

### `python main.py --index`

| Qué mirar | Dónde |
|-----------|--------|
| Vectores indexados | Consola → `Indexando N vectores…` |
| Índice en disco | Carpeta `output/chroma_db/` |

### `python main.py --query "¿Hay cine gratuito en verano?"`

| Qué mirar | Dónde |
|-----------|--------|
| Hits y **distance** (menor = más parecido) | Consola → `[RETRIEVAL] #1 …` |
| Texto recuperado | Consola → «Contexto recuperado» |
| Fuente (FAQ, CSV, PDF…) | Cabecera de cada fragmento |

### `python main.py --eval`

| Qué mirar | Dónde |
|-----------|--------|
| Mejor fuente por pregunta y K | Consola → `K=3 → mejor=… distance=…` |
| `fuente_esperada` en el JSON | Orientativa; no es corrección automática |

---

## Experimentar

Cambios que puedes probar **re-ejecutando** comandos:

- **`TOP_K`** y **`--top-k N`** — ¿cuántos fragmentos recuperar por consulta?
- **`TOP_K_CANDIDATES`** en `config.py` — qué valores de K usa `--eval` (por defecto 1, 3, 5).
- **`MAX_CHUNKS_EMBED = None`** — embeddear todo el corpus antes de indexar.
- **`--recreate-index`** — tras un nuevo `--prepare`, borra y recrea la colección Chroma.
- **Preguntas propias** — añade entradas en `queries/preguntas_eval.json` y vuelve a ejecutar `--eval`.
- **`CHUNK_SIZE` / `CHUNK_OVERLAP`** — cambia troceo (requiere `--prepare` + `--recreate-index`).

---

## Conclusiones y siguientes pasos

Este proyecto **recupera contexto**, pero **no redacta respuestas**. Es la fase de **búsqueda semántica**: embeddear la pregunta, consultar Chroma y devolver los chunks más cercanos.

| Fase | Módulo | Salida |
|------|--------|--------|
| Carga | `load.py` | Documentos desde `data/` |
| Limpieza | `clean.py` | Texto normalizado |
| Chunking | `chunk.py` | Fragmentos con metadata |
| Embeddings | `embed.py` | Vectores Gemini en `embeddings.json` |
| Indexación | `index.py` | Vectores persistidos en `chroma_db/` |
| Retrieval | `retriever.py` | Top-K chunks por similitud |
| Contexto | `context.py` | Texto formateado para inspección (y para S10) |

**Artefactos en disco:** `chunks.json`, `embeddings.json` y `chroma_db/`. Tras `--query`, compara el contexto impreso con los JSON: el texto del hit #1 debe existir en el índice.

### Conclusiones que deberías poder explicar

- **Indexar vs consultar** — los chunks se embeddean al preparar/indexar; la pregunta se embeddea en cada `--query`.
- **Mismo modelo siempre** — `EMBEDDING_MODEL` al indexar y al consultar debe coincidir.
- **Distance** — menor distancia coseno ≈ chunk más relevante para la pregunta.
- **TOP_K** — pocos chunks → contexto escaso; muchos → más ruido en el prompt futuro.
- **Metadata útil** — `source`, `distrito`, `id_evento` viajan hasta Chroma para filtrar o citar fuentes.

### Reflexionar tras `--eval` (no son experimentos de config)

Después de `--eval`, responde mentalmente (o en tus notas):

- ¿Recupera FAQ/PDF para preguntas conceptuales y CSV para eventos concretos?
- ¿Con K=1 se queda corto? ¿Con K=5 entra ruido?
- ¿La distance del primer hit destaca claramente sobre el resto?

Son **criterios de calidad del retrieval**, no cambios de parámetros: te ayudan a decidir si el índice está listo para Sprint 10.

### Hoja de ruta hacia un RAG completo

| Etapa | Estado en este proyecto | Qué aporta |
|-------|-------------------------|------------|
| Ingesta + chunking | Hecho | Corpus troceado |
| Embeddings | Hecho | Vectores por fragmento |
| Indexación vectorial | Hecho | ChromaDB persistente |
| Retrieval | Hecho | Top-K por similitud |
| Generación (LLM) | Pendiente | Respuesta con contexto recuperado |

### Siguiente paso técnico

Con un retrieval que devuelve contexto útil, el paso inmediato es **`prompts.py` + LLM** (Sprint 10): pasar el texto de `context.py` a un LLM y generar la respuesta final citando fuentes.
