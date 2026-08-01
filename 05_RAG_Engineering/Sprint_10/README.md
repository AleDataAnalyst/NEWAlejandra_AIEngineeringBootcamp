![Cabecera](./assets/cabecera_rag.png)

# 📘 Sprint 10 — RAG Generation, Evaluation & Interfaces

En el Sprint 9 construiste el **motor de búsqueda semántica**: indexaste el corpus, recuperaste chunks y evaluaste el contexto. En este sprint **cierras el ciclo RAG**: conviertes ese contexto en **respuestas generadas**, aprendes a **evaluarlas** y montas una **interfaz** para demostrar el sistema.

El sprint responde a una pregunta central:

> **¿Cómo uso el conocimiento recuperado para responder de forma útil, fiable y visible?**

---

## Mapa del módulo (Sprints 8–10)

| Sprint | Pregunta | Fase |
|--------|----------|------|
| **08** | ¿Cómo convierto documentos en conocimiento? | Preparar |
| **09** | ¿Cómo recupero ese conocimiento? | Recuperar |
| **10** (este) | ¿Cómo uso ese conocimiento para responder? | Generar + aplicación |

```text
PDF / CSV / MD  →  chunks  →  embeddings  →  ChromaDB  →  similarity search
                                                              ↓
                                                    contexto + prompt + LLM
                                                              ↓
                                                         respuesta + app
                                                              (Sprint 10)
```

Al final del sprint tendrás un **proyecto RAG completo** listo para evolucionar hacia agentes (Módulo 5).

---

## 🤖 Bloque 1 — Generación aumentada con contexto

📁 [`01_Teoria/01_Generacion_aumentada_con_contexto/`](./01_Teoria/01_Generacion_aumentada_con_contexto/)

> **Generar** respuestas a partir del contexto recuperado, con Gemini como camino principal.

*Prerrequisito: Sprint 9 (retriever + contexto formateado).*

### Contenido de teoría

| # | Documento | Qué aprenderás |
|---|-----------|----------------|
| 0 | [Introducción](./01_Teoria/01_Generacion_aumentada_con_contexto/00_introduccion_generacion_rag.md) | Puente S9→S10; pasos 6–7 del pipeline. |
| 1 | [Del retrieval a la respuesta](./01_Teoria/01_Generacion_aumentada_con_contexto/01_del_retrieval_a_la_respuesta.md) | `pregunta → contexto → LLM → respuesta`. |
| 2 | [Prompt con contexto recuperado](./01_Teoria/01_Generacion_aumentada_con_contexto/02_prompt_con_contexto_recuperado.md) | Instrucciones / contexto / pregunta; grounding. |
| 3 | [Generación con Gemini y alternativas](./01_Teoria/01_Generacion_aumentada_con_contexto/03_generacion_con_gemini_y_alternativas.md) | Gemini principal; Hugging Face como alternativa. |
| 4 | [Pipeline online y modularización](./01_Teoria/01_Generacion_aumentada_con_contexto/04_pipeline_online_y_modularizacion.md) | `prompts.py`, `generate.py`, `logic.py`, `--ask`. |

### Workout

| Notebook | Cubre teoría |
|----------|--------------|
| [01_del_retrieval_a_la_respuesta_rag.ipynb](./02_Workout/01_Generacion_aumentada_con_contexto/01_del_retrieval_a_la_respuesta_rag.ipynb) | 1 + 2 + 3 + 4 |

Índice detallado: [`01_Teoria/01_Generacion_aumentada_con_contexto/readme.md`](./01_Teoria/01_Generacion_aumentada_con_contexto/readme.md)

---

## 🛡️ Bloque 2 — Calidad, robustez y evaluación

📁 [`01_Teoria/02_Calidad_robustez_y_evaluacion/`](./01_Teoria/02_Calidad_robustez_y_evaluacion/)

> **Evaluar** respuestas generadas y reducir fallos típicos (alucinaciones, ruido, abstención).

*Prerrequisito: Bloque 1 (pipeline que genera respuestas).*

### Contenido de teoría

| # | Documento | Qué aprenderás |
|---|-----------|----------------|
| 0 | [Introducción](./01_Teoria/02_Calidad_robustez_y_evaluacion/00_introduccion_evaluacion_generacion.md) | Eval retrieval (S9) vs eval respuesta (S10). |
| 1 | [Cómo evaluar respuestas RAG](./01_Teoria/02_Calidad_robustez_y_evaluacion/01_como_evaluar_respuestas_rag.md) | Exactitud, relevancia, coherencia, fuentes. |
| 2 | [Alucinaciones y grounding](./01_Teoria/02_Calidad_robustez_y_evaluacion/02_hallucinations_y_grounding.md) | Reducir invenciones; cuándo abstenerse. |
| 3 | [Prompt injection y validación](./01_Teoria/02_Calidad_robustez_y_evaluacion/03_prompt_injection_y_validacion_de_fuentes.md) | Riesgos en docs/usuario; validar metadata. |
| 4 | [Buenas prácticas y limitaciones](./01_Teoria/02_Calidad_robustez_y_evaluacion/04_buenas_practicas_y_limitaciones_rag.md) | Límites del corpus, chunking, top-K, modelo. |

### Workout

| Notebook | Cubre teoría |
|----------|--------------|
| [01_evaluar_respuestas_rag.ipynb](./02_Workout/02_Calidad_robustez_y_evaluacion/01_evaluar_respuestas_rag.ipynb) | 1 + 2 + 3 + 4 |

Índice detallado: [`01_Teoria/02_Calidad_robustez_y_evaluacion/readme.md`](./01_Teoria/02_Calidad_robustez_y_evaluacion/readme.md)

---

## 🖥️ Bloque 3 — Interfaces y aplicaciones

📁 [`01_Teoria/03_Interfaces_y_aplicaciones_rag/`](./01_Teoria/03_Interfaces_y_aplicaciones_rag/)

> **Exponer** un sistema ya construido con una interfaz MVP (Streamlit), sin rehacer la lógica. Caso de uso del sprint: RAG.

*Prerrequisito: Bloques 1–2 (RAG funcional y evaluable).*

### Contenido de teoría

| # | Documento | Qué aprenderás |
|---|-----------|----------------|
| 0 | [Introducción](./01_Teoria/03_Interfaces_y_aplicaciones_rag/00_introduccion_interfaces.md) | UI vs API; MVP en este curso. |
| 1 | [Streamlit](./01_Teoria/03_Interfaces_y_aplicaciones_rag/01_streamlit.md) | Widgets, app mínima, ejecución local. |
| 2 | [De script a aplicación](./01_Teoria/03_Interfaces_y_aplicaciones_rag/02_de_script_a_aplicacion.md) | Contrato `responder()`; UI vs lógica. |
| 3 | [Resultado, estado y errores](./01_Teoria/03_Interfaces_y_aplicaciones_rag/03_mostrar_fuentes_estado_y_errores.md) | Spinner, errores, fuentes, contexto expandible. |
| 4 | [Otras opciones de interfaz](./01_Teoria/03_Interfaces_y_aplicaciones_rag/04_otras_opciones_de_interfaz.md) | Gradio, FastAPI (panorama). |

📁 Miniproyecto Streamlit (demo): [`06_miniproyecto_streamlit/`](./01_Teoria/03_Interfaces_y_aplicaciones_rag/06_miniproyecto_streamlit/)
📁 Proyecto RAG ejecutable: [`05_proyecto_rag_aplicacion/`](./01_Teoria/03_Interfaces_y_aplicaciones_rag/05_proyecto_rag_aplicacion/) — pipeline S8 + S9 + generación + Streamlit.

### Workout

| Notebook / guía | Cubre teoría |
|-----------------|--------------|
| [01_crear_interfaz_streamlit_rag.ipynb](./02_Workout/03_Interfaces_y_aplicaciones_rag/01_crear_interfaz_streamlit_rag.ipynb) | 1 + 2 + 3 |
| [02_proyecto_rag_aplicacion.md](./02_Workout/03_Interfaces_y_aplicaciones_rag/02_proyecto_rag_aplicacion.md) | Proyecto completo + repo externo |

Índice detallado: [`01_Teoria/03_Interfaces_y_aplicaciones_rag/readme.md`](./01_Teoria/03_Interfaces_y_aplicaciones_rag/readme.md)

---

## ⚙️ Convenciones del sprint

- Teoría en `01_Teoria/` (markdown + proyecto ejemplo ejecutable).
- Workouts en `02_Workout/` — **notebooks autocontenidos** (`data/`, `output/` y `queries/` compartidos; guiones en `guiones_video/`).
- Proyecto en teoría (`05_proyecto_rag_aplicacion/`) = ejemplo ejecutable en `.py` (evolución del proyecto S9).
- **Gemini** para generación; **Hugging Face** como alternativa documentada en teoría.
- **Streamlit** para la interfaz del Bloque 3.
- Corpus en `02_Workout/data/` — coloca aquí los ficheros de entrada (mismo dataset que S9).

**Consejo:** al terminar S10 deberías poder hacer una pregunta, obtener una **respuesta fundamentada en el corpus**, explicar **por qué** confías (o no) en ella y **mostrarla en una app**. Ese mismo backend será la base del Módulo 5 (agentes).
