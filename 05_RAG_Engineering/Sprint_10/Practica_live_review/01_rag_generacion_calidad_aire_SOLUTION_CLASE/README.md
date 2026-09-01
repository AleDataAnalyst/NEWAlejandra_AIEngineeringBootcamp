![Cabecera](../../assets/cabecera_rag.png)

# Práctica Sprint 10 — Generación RAG · calidad del aire Madrid

**Práctica integradora (Live Review)** del Sprint 10 — RAG Generation, Evaluation & Interfaces.

Continúa el pipeline de los Live Review de Sprints 8 y 9 (calidad del aire): la **ingesta, chunking, embeddings, indexación en ChromaDB y retrieval ya están dados**. Aquí implementas **prompt + generación con Gemini** y **evaluación de respuestas**. La interfaz Streamlit (`app.py`) **viene dada**: solo tienes que arrancarla cuando `responder()` funcione.

Esta será el pipeline de RAG que tendremos tras finalizar el ejercicio:

```text
ingesta → chunking → embeddings → ChromaDB → retrieval
    → prompt → Gemini → respuesta → evaluación de respuestas → Streamlit
```

> En Sprint 9 recuperabas contexto. Ahora **generas** la respuesta, compruebas si es fiable (abstención) y la **muestras** en una app sin reescribir el pipeline.

---

## Empieza aquí

### Fase 0 — Código completado con conceptos de Sprints 8–9. Prepara el índice.

- [ ] **1.** `python main.py --prepare --index` → `output/chunks.json`, `embeddings.json`, `chroma_db/` (si ya indexaste y cambias modelo/límites en `config.py`, usa `--prepare --index --recreate-index`)
- [ ] **2.** (opcional) `python main.py --query "¿Qué mide la magnitud 83?"` → solo retrieval (debug)

### Fase 1 — Generar (`src/prompts.py`, `src/generate.py`, `src/logic.py`)

- [ ] **3.** `build_rag_prompt()` en `src/prompts.py`
- [ ] **4.** `generar_respuesta()` en `src/generate.py`
- [ ] **5.** `responder(pregunta)` en `src/logic.py`
- [ ] **6.** `python main.py --ask "¿Qué mide la magnitud 83?"`
- [ ] **7.** `python main.py --ask "¿Cuál es la capital de Francia?"` → debe abstenerse
- [ ] **8.** `python main.py --check` muestra `[OK]` en prompts / generate / logic

### Fase 2 — Evaluación de respuestas (`src/eval_generation.py` + entregable)

- [ ] **9.** `evaluar_pregunta()` y `ejecutar_evaluacion()`
- [ ] **10.** `python main.py --eval`
- [ ] **11.** Completa `entregables/reflexion_generacion.md`
- [ ] **12.** `python main.py --check` muestra `[OK] src/eval_generation.py` y entregable

### Fase 3 — Demo Streamlit (`app.py` dado)

- [ ] **13.** `streamlit run app.py` (la UI ya llama a `responder`; no la reimplementes)
- [ ] **14.** Comprueba pregunta in-corpus + fuentes; prueba también un caso fuera de corpus
- [ ] **15.** `python main.py --check` muestra todo `[OK]`

### Archivos que **no debes modificar** (ejercicio obligatorio)

En `src/`: `load.py`, `clean.py`, `chunk.py`, `pipeline.py`, `embed.py`, `index.py`, `retriever.py`, `context.py`, `gemini_auth.py`.

En la raíz: `main.py`, `verificar.py`, `config.py` (puedes **cambiar valores** como `TOP_K` / `MAX_CHUNKS_EMBED` / `GEMINI_MODEL` para experimentar).

`app.py` viene **dado** para la demo. Solo tócalo si haces los **experimentos opcionales de UI** (más abajo); no metas ahí retrieval ni llamadas a Gemini.

---

## Corpus en `data/`

| Archivo | Rol |
|---------|-----|
| `faq_calidad_aire.md` | Preguntas frecuentes |
| `guia_calidad_aire.txt` | Resumen de campos |
| `descripcion-fichero-open-data-meteorologico-v2.pdf` | Documentación oficial |
| `calidad_aire_datos_meteo_mes.csv` | Mediciones horarias |

---

## Cuotas Gemini (free tier) y `config.py`

Al ejecutar `--prepare` se llaman embeddings de Gemini. En el **nivel gratuito** es fácil recibir `429 RESOURCE_EXHAUSTED` si se satura el límite **por minuto**.

### Qué limitan

| Límite | Significado aproximado |
|--------|------------------------|
| **RPM** | Peticiones por minuto a la API de embeddings |
| **TPM** | Tokens por minuto (el texto de los chunks) |
| **RPD** | Peticiones por día (suele sobrar; el cuello de botella suele ser RPM/TPM) |

El CSV aporta la mayor parte de los tokens. Los chunks se generan en orden de fichero: **primero el CSV**. Por eso `MAX_CHUNKS_EMBED = 50` suele indexar solo mediciones y **dejar fuera** FAQ/PDF/guía.

### Parámetros relevantes

| Parámetro | Rol |
|-----------|-----|
| `EMBEDDING_MODEL` | Modelo de vectores (`gemini-embedding-2` o `gemini-embedding-001`). Si cambias de modelo, regenera con `--recreate-index` (los espacios de embedding no son compatibles). |
| `MAX_CHUNKS_EMBED` | Cuántos chunks se embeddean. `None` = todos los generados. Un valor bajo (p. ej. 50) puede excluir FAQ/PDF. |
| `EMBED_BATCH_SIZE` | Cuántos chunks van en **cada** llamada a la API. Más alto → menos RPM, más TPM por request. Más bajo → al revés. |
| `MAX_FILAS_CSV` | Cuántas filas del CSV se convierten en documentos. Es el mando más útil para no disparar el TPM. |

`EMBED_BATCH_SIZE` pequeño **no evita** saturar el RPM por sí solo: hace **más** peticiones. Sirve sobre todo para no mandar demasiado texto de golpe (TPM).

### Config conservadora (recomendada para free tier)

Para indexar **PDF + FAQ + guía + parte del CSV** sin reventar la cuota al primer intento:

```python
EMBEDDING_MODEL = "gemini-embedding-2"
MAX_CHUNKS_EMBED = None      # no cortar el corpus (entra FAQ/PDF/TXT)
EMBED_BATCH_SIZE = 20        # compromiso RPM vs TPM
MAX_FILAS_CSV = 40           # el CSV es lo que más pesa en tokens
```

Si esa pasada va bien, sube poco a poco `MAX_FILAS_CSV` (50 → 60…). No subas primero el batch a 50 con muchas filas de CSV.

### Qué hace `--recreate-index`

`--index` solo escribe vectores en ChromaDB. Si la colección ya existe, **no** la borra: puedes mezclar embeddings viejos con nuevos (modelo distinto, otro `MAX_FILAS_CSV`, etc.).

`--recreate-index` (junto a `--index`) **borra la colección** y la vuelve a crear desde `embeddings.json`. Úsalo cuando regeneres el índice “de cero”.

| Situación | Comando |
|-----------|---------|
| Primera vez / no hay `chroma_db` | `python main.py --prepare --index` |
| Cambias `EMBEDDING_MODEL`, `MAX_CHUNKS_EMBED`, `MAX_FILAS_CSV`, etc. | `python main.py --prepare --index --recreate-index` |
| Solo quieres reindexar lo ya embeddeado (sin llamar otra vez a Gemini) | `python main.py --index --recreate-index` |

### Cómo lanzarlo sin quemar la ventana del minuto

```powershell
python main.py --prepare --index --recreate-index
```

- Ejecuta **una sola vez**; si sale `429`, espera **1–2 minutos** antes de reintentar (el error suele indicar `retry in ~Ns`).
- Varias ejecuciones seguidas (p. ej. 50 chunks y luego 200) suman en la misma ventana de RPM/TPM.
- Una API key **nueva en el mismo proyecto** de Google AI **comparte** la misma cuota. Cupo aparte = otra cuenta / otro proyecto.
- `--ask` y `--eval` gastan cuota del **modelo de generación** (`GEMINI_MODEL`), distinta de la de embeddings.

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

Raíz = entradas + config + datos. Lógica del pipeline en `src/` (importar como `from src.logic import responder`).

```text
.
├── README.md
├── requirements.txt
├── .env.example              # plantilla de variables
├── .env                      # tu clave (no se sube a git)
├── .gitignore
├── config.py                 # CHUNK_*, CHROMA_*, TOP_K, GEMINI_MODEL, …
├── main.py, verificar.py
├── app.py                    # Streamlit (dado; cliente de responder)
├── .streamlit/config.toml    # configuración de los estilos de la app streamlit
│
├── src/                      # lógica del pipeline
│   ├── __init__.py
│   ├── load.py, clean.py, chunk.py, pipeline.py, embed.py   # S8 (dados)
│   ├── index.py, retriever.py, context.py                   # S9 (dados)
│   ├── gemini_auth.py                                       # auth Gemini (dado)
│   ├── prompts.py, generate.py, logic.py                    # ← Fase 1
│   └── eval_generation.py                                   # ← Fase 2
│
├── queries/preguntas_eval.json
├── entregables/reflexion_generacion.md
├── data/
└── output/
```

---

## Secuencia recomendada

```text
python main.py --prepare --index
# Si regeneras embeddings (cambio de modelo o de MAX_*): añade --recreate-index
# python main.py --prepare --index --recreate-index
python main.py --ask "¿Qué mide la magnitud 83?"
python main.py --ask "¿Cuál es la capital de Francia?"
python main.py --eval
# Completa entregables/reflexion_generacion.md
streamlit run app.py
python main.py --check
```

---

## FASE 1 — Generar respuesta (`src/prompts.py`, `src/generate.py`, `src/logic.py`)

### Objetivo

Con el contexto del retriever, montar un prompt restrictivo, llamar a Gemini y devolver un dict estable desde `responder()`.

### Pistas

- `build_rag_prompt(contexto, pregunta)`: instrucciones + `--- CONTEXTO ---` + `--- PREGUNTA ---`
- `generar_respuesta(prompt)`: `genai.Client()` + `GEMINI_MODEL` + temperatura baja
- `responder(pregunta)`: validar pregunta → `recuperar` → `formatear_contexto` → prompt → generate → `{respuesta, contexto, chunks, fuentes, error}`
- Fuera de corpus: el modelo debe **indicar** que no hay evidencia (no inventar)

### Criterios de aceptación

- [ ] `python main.py --check` → `[OK]` prompts, generate, logic
- [ ] `--ask` in-corpus devuelve texto + fuentes
- [ ] `--ask` “capital de Francia” se abstiene / no inventa París desde el corpus

---

## FASE 2 — Evaluación de respuestas (`src/eval_generation.py`)

### Objetivo

Barrido de `queries/preguntas_eval.json` (incluye `deberia_abstenerse`) y reflexión escrita.

### Pistas

- `evaluar_pregunta`: llama a `responder` y resume id, respuesta, fuentes, flag de abstención
- `ejecutar_evaluacion`: recorre el JSON e imprime un resumen legible por pregunta
- `deberia_abstenerse: true` es **orientativo** para tu juicio (no un assert automático)

### Criterios de aceptación

- [ ] `python main.py --eval` recorre todas las preguntas
- [ ] `reflexion_generacion.md` sin TODO y con observaciones reales

---

## FASE 3 — Demo Streamlit (`app.py` dado)

### Objetivo

Comprobar que la misma lógica de `--ask` se ve en el navegador. **No implementas la UI**: `app.py` ya importa `from src.logic import responder`.

### Qué hacer

1. Con `responder()` funcionando: `streamlit run app.py`
2. Pregunta in-corpus → respuesta + fuentes
3. Pregunta fuera de corpus → mensaje de abstención / sin inventar
4. Opcional: mueve el slider Top-K y observa el efecto

### Criterios de aceptación

- [ ] La app arranca y muestra respuesta + fuentes sin errores de import
- [ ] `python main.py --check` → `[OK] app.py`

---

## Experimentos opcionales (si sobra tiempo)

### Prompt / generación

- [ ] **Prompt permisivo vs restrictivo** — quita (temporalmente) la regla “solo contexto” y repite “¿Cuál es la capital de Francia?”. ¿Se inventa la respuesta?
- [ ] **Temperatura** — en `config.py`, prueba `GENERATION_TEMPERATURE = 0.0` vs `0.7`. ¿Cómo afecta a la respuesta?

### Retrieval ↔ respuesta

- [ ] **Citas explícitas** — añade al prompt: “menciona el nombre del fichero fuente”. ¿Cuadra con la lista de `fuentes`?
- [ ] **Variar `TOP_K`** — `1`, `3` y `5` en la misma pregunta. ¿Mejora o mete ruido?
- [ ] **Pregunta ambigua** — p. ej. “¿qué es la validación?” con K bajo vs alto.
- [ ] **Menos chunks en el índice** — baja `MAX_CHUNKS_EMBED`, vuelve a `--prepare --index` y mira si retrieval/respuesta empeoran.

### Evaluación / robustez

- [ ] **Añade 1 pregunta** a `queries/preguntas_eval.json` (una in-corpus y, si puedes, otra fuera) y pasa `--eval`.
- [ ] **Dos runs** de la misma pregunta — ¿la respuesta es estable?
- [ ] **Pregunta vacía** — `--ask "   "` (o equivalente): ¿devuelve `error` sin llamar al modelo?

### UI Streamlit

- [ ] **Misma pregunta en `--ask` y en Streamlit** — ¿mismo resultado? (contrato `responder`)
- [ ] **Slider Top-K** en la sidebar — anota el efecto en fuentes / expander de contexto.

### UI Streamlit (modificaciones en `app.py`)

`app.py` viene dado, pero puedes **tocarlo solo para estos experimentos**. No reimplementes retrieval ni Gemini en la UI: sigue llamando a `responder()`.

- [ ] **Chat en lugar de formulario** — cambia `text_input` + botón por `st.chat_input` / `st.chat_message`. ¿Más usable?
- [ ] **Control extra en la sidebar** — p. ej. checkbox “Mostrar contexto (debug)” que oculte/enseñe el expander; o un `st.selectbox` con 2–3 preguntas de ejemplo.
- [ ] **Feedback del usuario** — tras la respuesta, botones 👍 / 👎 (o “útil / no útil”) que guarden algo simple en `st.session_state` (no hace falta persistir en disco).

Si haces experimentos, añade al final de `reflexion_generacion.md`: *qué cambiaste → qué observaste → qué cambiarías en un sistema real*.
