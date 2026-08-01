# Live Review — Sprint 09

Práctica integradora de **indexación vectorial, retrieval y evaluación del retrieval** (continuación del corpus calidad del aire de Sprint 8).

| Carpeta | Contenido |
|---------|-----------|
| [`01_retrieval_calidad_aire/`](01_retrieval_calidad_aire/) | Proyecto de la práctica (stubs S9) |
| [`01_retrieval_calidad_aire_SOLUTION/`](01_retrieval_calidad_aire_SOLUTION/) | Mismo enunciado; `index.py`, `retriever.py`, `eval_retrieval.py` y entregable completos |
| [`README_profes.md`](README_profes.md) | Guion de sesiones |

## Resumen

- **Dominio:** datos meteorológicos Madrid (open data) — mismo corpus que Live Review S8
- **Corpus:** incluido en `data/` (FAQ, guía, PDF, CSV)
- **Código S8:** dado (`load` → `chunk` → `embed`); el alumno no lo reimplementa
- **Pipeline tras el ejercicio:**  
  `ingesta → chunking → embeddings → indexación en ChromaDB → retrieval → evaluación del retrieval`
- **Implementación principal:** `index.py`, `retriever.py`, `eval_retrieval.py` + `entregables/reflexion_retrieval.md`
- **No incluye:** generación de respuestas con LLM (más adelante / Sprint 10)

## Flujo CLI (resumen)

```text
python main.py --prepare
python main.py --index
python main.py --query "¿Qué mide la magnitud 83?"
python main.py --eval
python main.py --check
```

Flags útiles para experimentar: `--recreate-index`, `--top-k` (también se puede variar `TOP_K` / `TOP_K_CANDIDATES` en `config.py`).
