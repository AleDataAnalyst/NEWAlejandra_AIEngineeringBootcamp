![Cabecera](../../../assets/cabecera_rag.png)

# Proyecto ejemplo: RAG + Streamlit - Chatbot web

Pipeline **acumulativo** S8 + S9 + S10: documentos → chunks → embeddings → ChromaDB → retrieval → **respuesta generada** → app Streamlit (chatbot web). 

En este proyecto, extendemos el pipeline de RAG completo de los sprints anteriores y lo integramos con una UI Streamlit para que puedas ver un ejemplo de cómo se podría integrar un chatbot web en una aplicación.

**Requisitos:** Python 3.10+ y `GEMINI_API_KEY` en `.env`.

**Corpus:** agenda cultural de Madrid.

| Archivo | Formato |
|---------|---------|
| `faq_agenda_cultural.md` | FAQ |
| `guia_agenda_cultural.txt` | Guía |
| `206974-3-agenda-eventos-culturales-100.pdf` | PDF |
| `206974-4-agenda-eventos-culturales-100-csv.csv` | CSV eventos |

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

## Ejecución (CLI)

Antes de la web, deja el índice listo y comprueba el backend en consola:

```bash
# Primera vez: pipeline offline + indexación. Cargar los documentos en ChromaDB
python main.py --prepare --index

# RAG completo en consola (respuesta generada) 
python main.py --ask "¿Hay cine gratuito en verano?"

# Solo retrieval + contexto (S9)
python main.py --query "¿Hay cine gratuito en verano?"
```

Si `--ask` falla, la UI también fallará: arregla el backend primero.

### Cuántos chunks se indexan (`config.py`)

En `config.py`, `MAX_CHUNKS_EMBED` limita cuántos chunks se embeddean e indexan (por defecto un valor bajo para demos rápidas y baratas).

| Valor | Efecto |
|-------|--------|
| `5`, `20`, `50`… | Solo los **primeros N** chunks entran en Chroma (el resto del corpus no está disponible al preguntar) |
| `None` | Se embeddean **todos** los chunks |

**Por qué importa:** si el límite es muy bajo, preguntas como «¿Hay cine gratuito en verano?» pueden fallar aunque la respuesta esté en la FAQ o la guía: el retrieval solo busca dentro de lo indexado (a menudo trozos del PDF).

**Qué consume al subir N (o poner `None`):**

- Más coste y tiempo de API de **embeddings** en `--prepare`
- `embeddings.json` y Chroma más grandes; `--index` tarda más
- Cada pregunta (`--ask` / Streamlit) **no** re-embeddea el corpus: sigue recuperando solo `TOP_K` chunks

Tras cambiar `MAX_CHUNKS_EMBED`, vuelve a construir el índice:

```bash
python main.py --prepare --index --recreate-index
```

---

## App Streamlit (cómo usar la web)

### Arranque

Desde la carpeta del proyecto (con el `.venv` activo y el índice creado):

```bash
streamlit run app.py
```

Se abre el navegador en `http://localhost:8501` (si no, usa la URL que imprime la terminal). Deja la terminal abierta mientras usas la app.

### Qué verás en pantalla

1. **Chat** — escribe en el campo inferior (`chat_input`) y pulsa Enter.
2. **Respuesta** — aparece con streaming (palabra a palabra) tras consultar el corpus.
3. **Fuentes** — lista de documentos usados bajo la respuesta.
4. **Contexto recuperado (debug)** — expander cerrado; ábrelo para ver el texto que entró al prompt.
5. **Sidebar**
   - **Nombre del bot** — cambia el título de la página.
   - **Top-K** — cuántos chunks recupera el retriever (1–5).
   - **Limpiar chat** — reinicia el hilo con el mensaje de bienvenida.

### Pruebas sugeridas

| Prueba | Ejemplo | Qué observar |
|--------|---------|--------------|
| Pregunta del dominio | `¿Hay cine gratuito en verano?` | Respuesta + fuentes |
| Campo / FAQ | `¿Qué significa el campo GRATUITO?` | Retrieval útil |
| Fuera de corpus | `¿Cuál es la capital de Francia?` | Abstención / mensaje controlado |
| Top-K | Cambia el slider y repite la misma pregunta | Más/menos contexto en el expander |
| Error de índice | Sin `output/chroma_db/` | Mensaje amigable (no stack trace) |

### Notas importantes

- El **historial es solo de interfaz**: cada mensaje llama otra vez a `src.logic.responder(pregunta)`. El modelo no “recuerda” turnos anteriores.
- Tema visual: `.streamlit/config.toml`. Aquí puedes cambiar los colores y la tipografía de la página. Estilos básicos.
- Para parar la app: `Ctrl+C` en la terminal.

### Si algo no carga

| Síntoma | Qué hacer |
|---------|-----------|
| Error de API key | Revisa `.env` → `GEMINI_API_KEY` |
| Índice vacío / no existe | `python main.py --prepare --index` |
| Puerto ocupado | Streamlit ofrecerá otro (p. ej. 8502) o cierra la instancia anterior |

---

## Estructura

Raíz = entradas + config + datos. Lógica del pipeline en `src/` (importar como `from src.logic import responder`).

```text
.
├── app.py                 # Streamlit (UI)
├── main.py                # CLI
├── config.py              # rutas data/output + TOP_K, modelos…
├── requirements.txt
├── .env.example
├── .streamlit/config.toml
│
├── src/                   # lógica del pipeline
│   ├── __init__.py
│   ├── load.py, clean.py, chunk.py, pipeline.py, embed.py   # S8
│   ├── index.py, retriever.py, context.py, eval_retrieval.py # S9
│   ├── prompts.py, generate.py, validators.py, logic.py      # S10
│   └── gemini_auth.py
│
├── data/                  # corpus
├── queries/
└── output/                # chunks, embeddings, chroma_db
```

Ejecuta siempre desde la raíz del proyecto (`python main.py …`, `streamlit run app.py`).

---

## Flujo completo

```text
OFFLINE (S8–S9)
  data/ → load → clean → chunk → embed → index → chroma_db/

ONLINE (S10)
  Pregunta → retriever → context → prompts → generate → respuesta
                ↑                              ↑
           src.logic.responder()          app.py (Streamlit chat)
```

---

## Qué mirar en el código

| Archivo | Rol en la demo web |
|---------|-------------------|
| `app.py` | UI Streamlit (chat → `responder`) |
| `src/logic.py` | Contrato único CLI + Streamlit |
| `src/validators.py` | Errores que verás como `st.error` |
| `config.py` | Parámetros y rutas (`data/`, `output/`) |
| `.streamlit/config.toml` | Colores / tipografía |

---
