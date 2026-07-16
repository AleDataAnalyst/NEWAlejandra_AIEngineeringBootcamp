![Cabecera](./assets/cabecera_rag.png)

# 📘 Sprint 08 — Data Ingestion & Embeddings

En el Sprint 7 aprendiste a **elegir y evaluar modelos** con datos. En este sprint empiezas el **Módulo 4 — RAG Engineering**: convertir documentos en conocimiento que un sistema pueda recuperar después.

El sprint responde a una pregunta central:

> **¿Cómo convierto documentos en conocimiento recuperable?**

Todavía **no** construyes un chatbot RAG completo. Primero preparas el pipeline offline: ingesta, chunking y embeddings.

---

## Mapa del módulo (Sprints 8–10)

| Sprint | Pregunta | Fase |
|--------|----------|------|
| **08** (este) | ¿Cómo convierto documentos en conocimiento? | Preparar |
| **09** | ¿Cómo recupero ese conocimiento? | Recuperar |
| **10** | ¿Cómo uso ese conocimiento para responder? | Generar + aplicación |

Al final del módulo tendrás un proyecto acumulativo (`proyecto_rag_bootcamp_ejemplo/`) que reutilizarás en el Módulo 5 (AI Agents).

---

## 🧭 Bloque 1 — Introducción a RAG y arquitectura

📁 [`01_Teoria/01_Introduccion_a_RAG_y_arquitectura/`](./01_Teoria/01_Introduccion_a_RAG_y_arquitectura/)

> **Conceptual, sin programar el pipeline:** qué problema resuelve RAG, arquitectura en dos etapas (recuperación + generación) y stack del módulo.

*Prerrequisitos: Sprint 4 (Gemini API), Sprint 5–6 (prompts, contexto, proyectos modulares), Sprint 7 (familia embeddings).*

### Contenido de teoría

| # | Documento | Qué aprenderás |
|---|-----------|----------------|
| 0 | [Introducción a RAG](./01_Teoria/01_Introduccion_a_RAG_y_arquitectura/00_introduccion_rag.md) | Mapa del sprint y del módulo. |
| 1 | [Qué es RAG y limitaciones del LLM](./01_Teoria/01_Introduccion_a_RAG_y_arquitectura/01_que_es_rag_y_limitaciones_llm.md) | Casos de uso; PE vs fine-tuning vs RAG. |
| 2 | [Arquitectura y componentes](./01_Teoria/01_Introduccion_a_RAG_y_arquitectura/02_arquitectura_y_componentes.md) | Pipeline offline/online; retrieval ≠ generation. |
| 3 | [Tecnologías del módulo](./01_Teoria/01_Introduccion_a_RAG_y_arquitectura/03_tecnologias_del_modulo.md) | Gemini, LangChain, ChromaDB (S9), convenciones. |

*Bloque conceptual — solo teoría en markdown. El primer workout en vídeo del sprint es [carga de documentos y chunking](./02_Workout/02_Ingesta_y_procesamiento_de_documentos/01_carga_documentos_y_chunking.ipynb) (Bloque 2).*

Índice detallado: [`01_Teoria/01_Introduccion_a_RAG_y_arquitectura/readme.md`](./01_Teoria/01_Introduccion_a_RAG_y_arquitectura/readme.md)

---

## 📄 Bloque 2 — Ingesta y procesamiento de documentos

📁 [`01_Teoria/02_Ingesta_y_procesamiento_de_documentos/`](./01_Teoria/02_Ingesta_y_procesamiento_de_documentos/)

> **Del documento al chunk:** carga, limpieza, fragmentación y metadatos en un pipeline modular.

*Prerrequisito: Bloque 1.*

### Contenido de teoría

| # | Documento | Qué aprenderás |
|---|-----------|----------------|
| 0 | [Introducción a ingesta](./01_Teoria/02_Ingesta_y_procesamiento_de_documentos/00_introduccion_ingesta.md) | Objetivos y salida del bloque. |
| 1 | [Carga y lectura de documentos](./01_Teoria/02_Ingesta_y_procesamiento_de_documentos/01_carga_y_lectura_documentos.md) | Loaders LangChain, PDF, CSV y carpeta `data/`. |
| 2 | [Limpieza y normalización](./01_Teoria/02_Ingesta_y_procesamiento_de_documentos/02_limpieza_y_normalizacion.md) | Ruido típico y `clean.py`. |
| 3 | [Chunking — estrategias](./01_Teoria/02_Ingesta_y_procesamiento_de_documentos/03_chunking_estrategias.md) | `RecursiveCharacterTextSplitter`, size/overlap. |
| 4 | [Metadatos y pipeline modular](./01_Teoria/02_Ingesta_y_procesamiento_de_documentos/04_metadatos_y_pipeline_modular.md) | Arquitectura load → clean → chunk → JSON. |

### Workout

| Notebook / guía | Cubre teoría |
|-----------------|--------------|
| [01_carga_documentos_y_chunking.ipynb](./02_Workout/02_Ingesta_y_procesamiento_de_documentos/01_carga_documentos_y_chunking.ipynb) | 1 + 2 + 3 |

Índice detallado: [`01_Teoria/02_Ingesta_y_procesamiento_de_documentos/readme.md`](./01_Teoria/02_Ingesta_y_procesamiento_de_documentos/readme.md)

---

## 🔢 Bloque 3 — Embeddings

📁 [`01_Teoria/03_Embeddings/`](./01_Teoria/03_Embeddings/)

> **Texto → vectores:** similitud semántica, embeddings con Gemini y comparación con Hugging Face.

*Prerrequisito: Bloque 2.*

### Contenido de teoría

| # | Documento | Qué aprenderás |
|---|-----------|----------------|
| 0 | [Introducción a embeddings en RAG](./01_Teoria/03_Embeddings/00_introduccion_embeddings_rag.md) | Puente S7; salida del bloque. |
| 1 | [Vectores y similitud semántica](./01_Teoria/03_Embeddings/01_vectores_y_similitud_semantica.md) | Coseno; intuición sin álgebra. |
| 2 | [Embeddings con Gemini](./01_Teoria/03_Embeddings/02_embeddings_gemini.md) | `embed_content`, batch, config. |
| 3 | [Embeddings con Hugging Face](./01_Teoria/03_Embeddings/03_embeddings_huggingface.md) | MiniLM local; cuándo usarlo. |
| 4 | [Comparación de modelos](./01_Teoria/03_Embeddings/04_comparacion_modelos_embedding.md) | Matriz de decisión estilo S7. |

📁 Proyecto ejecutable: [`05_proyecto_ingesta_chunking_embedding/`](./01_Teoria/03_Embeddings/05_proyecto_ingesta_chunking_embedding/) — `pip install -r requirements.txt`, `.env` con `GEMINI_API_KEY` y `python main.py`.

### Workout

| Notebook / guía | Cubre teoría |
|-----------------|--------------|
| [01_embeddings.ipynb](./02_Workout/03_Embeddings/01_embeddings.ipynb) | 2 |
| [02_comparar_modelos_embedding.ipynb](./02_Workout/03_Embeddings/02_comparar_modelos_embedding.ipynb) | 1 + 3 + 4 |
| [03_proyecto_rag_ingesta_chunking_embeddings.md](./02_Workout/03_Embeddings/03_proyecto_rag_ingesta_chunking_embeddings.md) | Proyecto modular (Bloques 2 + 3) |

Índice detallado: [`01_Teoria/03_Embeddings/readme.md`](./01_Teoria/03_Embeddings/readme.md)

---

## ⚙️ Convenciones del sprint

- Teoría en `01_Teoria/` (markdown + proyectos ejemplo ejecutables).
- Workouts en `02_Workout/` (notebooks guiados + guías al proyecto; guiones en `guiones_video/`).
- API: **Google Gemini** (`google-genai`) como hilo principal; LangChain para loaders y splitters.
- Cabeceras markdown: `assets/cabecera_gemini.png`. Si la carpeta `assets/` está vacía, copia la imagen desde otro sprint (ver [`assets/README.md`](./assets/README.md)).

**Consejo:** en S8 terminas con **vectores listos para indexar**. ChromaDB y retrieval llegan en el Sprint 9; la generación con contexto, en el Sprint 10.
