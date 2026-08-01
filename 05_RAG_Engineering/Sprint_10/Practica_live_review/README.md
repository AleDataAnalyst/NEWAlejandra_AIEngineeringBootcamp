# Live Review — Sprint 10

Práctica integradora de **generación RAG** y **evaluación de respuestas** (continuación del corpus calidad del aire de Sprints 8–9). Streamlit se usa como **demo** (`app.py` dado).

| Carpeta | Contenido |
|---------|-----------|
| [`01_rag_generacion_calidad_aire/`](01_rag_generacion_calidad_aire/) | Proyecto alumno (TODOs en `src/prompts` / `src/generate` / `src/logic` / `src/eval_generation`) |
| [`01_rag_generacion_calidad_aire_SOLUTION/`](01_rag_generacion_calidad_aire_SOLUTION/) | Referencia del profesor |

## Resumen

- **Dominio:** calidad del aire / meteorología Madrid (mismo corpus que Live S8–S9)
- **Código S8–S9:** dado en `src/` (ingesta → embeddings → Chroma → retrieval)
- **Implementación del alumno:** `src/prompts.py`, `src/generate.py`, `src/logic.py`, `src/eval_generation.py` + entregable
- **`app.py`:** dado (cliente de `from src.logic import responder`)
- **Pipeline tras el ejercicio:**  
  `… → retrieval → prompt → Gemini → respuesta → eval respuestas → Streamlit`
