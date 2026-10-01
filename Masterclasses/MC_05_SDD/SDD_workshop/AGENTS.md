# AGENTS.md — RAG de la agenda cultural de Madrid

## Proyecto
Asistente RAG que responde preguntas sobre la agenda cultural de Madrid (datos abiertos del Ayuntamiento).
- **Offline:** `data/` → carga → limpieza → chunking → embeddings (Gemini) → ChromaDB persistente en `output/chroma_db/`.
- **Online:** pregunta → validación → retriever (top-K) → contexto → prompt → Gemini → respuesta con fuentes.
- Dos interfaces sobre el mismo contrato, `src.logic.responder(pregunta, top_k) -> dict`: CLI (`main.py`) y chat web (`app.py`, Streamlit).

## Mapa del código
| Archivo | Responsabilidad |
|---|---|
| `config.py` | Parámetros y rutas: chunking, modelos, `MAX_CHUNKS_EMBED`, `TOP_K`, colección Chroma |
| `src/load.py` | Carga `.txt`, `.md`, `.pdf` y `.csv` de `data/` como `Document` (una fila del CSV = un documento) |
| `src/clean.py` · `src/chunk.py` | Normalización del texto y fragmentación con metadatos (`chunk_index`, `chunk_size`) |
| `src/pipeline.py` | Orquesta la ingesta y guarda `output/chunks.json` |
| `src/embed.py` | Embeddings con Gemini → `output/embeddings.json` |
| `src/index.py` | Indexación en ChromaDB (distancia coseno) |
| `src/retriever.py` | Pregunta → top-K fragmentos con `distance` y `metadata` |
| `src/context.py` | Formatea los fragmentos como bloque de contexto |
| `src/validators.py` | Validación de la pregunta y del contexto antes de llamar al LLM |
| `src/prompts.py` · `src/generate.py` | Prompt con bloques delimitados y llamada a Gemini |
| `src/logic.py` | `responder()`: el contrato único que usan CLI y web |
| `src/eval_retrieval.py` | Evaluación del retrieval con `queries/preguntas_eval.json` |
| `main.py` · `app.py` | Interfaces (CLI y Streamlit): solo presentan, no deciden |
| `tests/` | Tests con pytest y dobles de prueba (sin API) |

## Comandos
- Instalar: `pip install -r requirements.txt`
- Tests: `pytest` (no necesita API key)
- Preparar e indexar: `python main.py --prepare --index` ⚠️ gasta API
- Preguntar: `python main.py --ask "¿Hay cine gratuito en verano?"` ⚠️ gasta API
- Solo retrieval: `python main.py --query "..."` ⚠️ gasta API
- Evaluar retrieval: `python main.py --eval` ⚠️ gasta API
- Web: `streamlit run app.py` ⚠️ gasta API

## Flujo SDD de este repositorio
- Constitución: `docs/constitution.md`. Léela siempre.
- Specs: `specs/NNN-nombre/` con `spec.md`, `plan.md`, `tasks.md` y `validacion.md`. La spec activa es la de número más alto, salvo que se indique otra.
- `specs/000-sistema-actual/` documenta lo que el sistema ya hacía antes de usar SDD (línea base).
- Plantillas: `docs/plantillas/`. Chuleta de EARS: `docs/chuleta_ears.md`.
- Comandos por fase: `.github/prompts/` (`/sdd-constitucion`, `/sdd-contexto`, `/sdd-spec`, `/sdd-clarificar`, `/sdd-plan`, `/sdd-tareas`, `/sdd-implementar`, `/sdd-validar`, `/sdd-cambio`, `/sdd-spec-inversa`).

## Reglas
- Lee `docs/constitution.md` y la spec activa antes de tocar nada.
- Respeta la fase en la que estamos. En spec, clarificación, plan y tareas NO se escribe código.
- En implementación: una sola tarea de `tasks.md` cada vez, tests primero, y te paras al terminarla.
- No modifiques `specs/` salvo que la fase lo pida (redactar, aclarar, planificar, desglosar, marcar tarea, validar, cambio).
- No añadas dependencias ni cambies el contrato de `responder()` o el formato del índice si la spec no lo dice.
- El proyecto debe funcionar en Python 3.9: todo módulo de Python empieza por `from __future__ import annotations` (tras su docstring).
- No ejecutes comandos marcados con ⚠️ salvo que te lo pida: cuestan dinero y tiempo. Para verificar, usa `pytest`.
- No leas ni uses la carpeta `Profes/`: es material docente, no forma parte del proyecto.
- Nunca leas ni muestres el contenido de `.env`.

## Al terminar cualquier tarea
- Ejecuta `pytest` y pega el resumen del resultado.
- Indica qué RF de la spec cubre lo que has hecho.
