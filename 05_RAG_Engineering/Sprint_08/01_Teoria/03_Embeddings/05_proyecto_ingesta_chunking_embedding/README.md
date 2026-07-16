![Cabecera](../../../assets/cabecera_rag.png)

# Proyecto ejemplo: RAG ingesta + chunking + embeddings

Pipeline **offline** de RAG: documentos → chunks → vectores.

En este ejemplo verás las fases de ingesta, chunking y embeddings en una sola ejecución. El corpus queda representado como vectores listos para indexar en una base vectorial.

**Requisitos:** Python 3.10+ y `GEMINI_API_KEY` en `.env`.

**Corpus:** agenda cultural de Madrid. Cuatro fuentes en `data/`:

| Archivo | Formato | Contenido |
|---------|---------|-----------|
| `faq_agenda_cultural.md` | Markdown | Preguntas frecuentes |
| `guia_agenda_cultural.txt` | Texto | Guía del dataset |
| `206974-3-agenda-eventos-culturales-100.pdf` | PDF | Documentación oficial |
| `206974-4-agenda-eventos-culturales-100-csv.csv` | CSV | Eventos (una fila = un documento) |

**Modelo de embedding:** `gemini-embedding-2` (3072 dimensiones). Configurable en `config.py` → `EMBEDDING_MODEL`.

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
python main.py
```

Genera `output/chunks.json` y `output/embeddings.json`, e imprime un resumen en consola.

Por defecto `MAX_CHUNKS_EMBED = 5` en `config.py` (demo rápida). Pon `None` para embeddear todo el corpus.

---

## Estructura

```text
.
├── .env.example           # plantilla; copiar a .env con tu GEMINI_API_KEY
├── .env                   # clave API (local, no se sube al repo)
├── .gitignore             # ignora .env, output generado, etc.
├── config.py              # rutas, chunking, modelo, límites de demo
├── load.py                # lectura .txt, .md, .pdf, .csv
├── clean.py               # normalización de texto
├── chunk.py               # Chunking con RecursiveCharacterTextSplitter
├── pipeline.py            # orquesta ingesta → chunks.json
├── embed.py               # vectores Gemini
├── gemini_auth.py         # carga GEMINI_API_KEY desde .env
├── main.py                # punto de entrada (pipeline completo)
├── data/                  # corpus de entrada
└── output/                # chunks.json y embeddings.json (generados)
```

---

## Orden recomendado al explorar el código

1. `data/` — qué documentos entran al pipeline para la ingesta.
2. `config.py` — `CHUNK_SIZE`, `CHUNK_OVERLAP`, `EMBEDDING_MODEL`, `MAX_CHUNKS_EMBED`.
3. Ingesta: `load.py` → `clean.py` → `chunk.py` → `pipeline.py`.
4. Embeddings: `embed.py` → `output/embeddings.json`.
5. Tras ejecutar: inspecciona `chunks.json` y `embeddings.json`.

---

## Experimentar

- Cambia `CHUNK_SIZE` / `CHUNK_OVERLAP` y vuelve a ejecutar.
- `MAX_CHUNKS_EMBED = None` para embeddear todos los chunks.
- Añade un `.md` en `data/` y observa cómo `load.py` lo detecta.

---

## Conclusiones y siguientes pasos

Este proyecto **no es un asistente que responde preguntas todavía**. Es la fase de **preparación del índice**: convertir documentos reales en fragmentos con metadata y en vectores numéricos. Eso es normal en un pipeline RAG: primero se indexa, después se consulta.

| Fase | Módulo | Salida |
|------|--------|--------|
| Carga | `load.py` | Documentos unificados desde `data/` (FAQ, guía, PDF, CSV) |
| Limpieza | `clean.py` | Texto normalizado, sin ruido de formato |
| Chunking | `chunk.py` | Fragmentos con `chunk_index` y metadata (`source`, `id_evento`, …) |
| Embeddings | `embed.py` | Un vector de 3072 números por chunk (`gemini-embedding-2`) |

**Artefactos en disco:** `output/chunks.json` (texto) y `output/embeddings.json` (texto + vector + metadata). Abre un `item` en ambos y verifica que el texto y la metadata coinciden; en `embeddings.json` aparece además el vector.

**Ejemplos de output:** `puedes ver los ficheros en la carpeta output/chunks_ejemplo.json` (texto) y `output/embeddings_ejemplo.json` (texto + vector + metadata). Puedes borrarlos y volver a ejecutar el pipeline para generar estos ejemplos.

### Conclusiones que deberías poder explicar

- **Varias fuentes, un pipeline** — el mismo flujo trata markdown, PDF y CSV de eventos.
- **El chunk es la unidad de búsqueda** — en retrieval no se recuperan archivos enteros, sino fragmentos como los de `chunks.json`.
- **La metadata viaja hasta el vector** — `distrito`, `id_evento`, `tipo` siguen en `embeddings.json` (sirve para filtrar o citar fuentes más adelante).
- **Un modelo, un espacio vectorial** — todos los vectores salen del mismo `EMBEDDING_MODEL`; la pregunta del usuario deberá embeddearse con el **mismo** modelo cuando hagas búsqueda.
- **Latencia y coste existen** — la consola muestra cuántos ms tardó el embed; a mayor corpus, más llamadas o más chunks.

Si al terminar echas en falta *hacer una pregunta y ver una respuesta*, es señal de que entendiste el pipeline: **falta la capa de búsqueda**, no que algo esté roto.

### Hoja de ruta hacia un RAG completo

| Etapa | Estado en este proyecto | Qué aporta |
|-------|-------------------------|------------|
| Ingesta + chunking | Hecho | Corpus troceado y con metadata |
| Embeddings | Hecho | Representación numérica de cada fragmento |
| Indexación vectorial | Pendiente | Persistir vectores (p. ej. ChromaDB) y buscar a escala |
| Retrieval | Pendiente | Embed de la pregunta + top-k chunks por similitud |
| Generación (LLM) | Pendiente | El modelo responde usando los chunks recuperados como contexto |

### Siguiente paso técnico

Con `embeddings.json` el corpus está **listo para indexar**. El paso inmediato es cargar esos vectores en una **base vectorial** (p. ej. ChromaDB, Pinecone o pgvector), embeddear la pregunta del usuario con el mismo modelo y recuperar los chunks más similares. Ahí empieza el retrieval; después vendrá enganchar un LLM para generar la respuesta final.
