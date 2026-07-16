# Live Review — Sprint 08

Práctica integradora de **ingesta, chunking y embeddings** (RAG offline).

| Carpeta | Contenido |
|---------|-----------|
| [`01_pipeline_calidad_aire/`](01_pipeline_calidad_aire/) | Proyecto de la práctica |
| [`01_pipeline_calidad_aire_SOLUTION/`](01_pipeline_calidad_aire_SOLUTION/) | Mismo enunciado; `load.py` y entregables completos |
| [`README_profes.md`](README_profes.md) | Guion de sesiones |

## Resumen

- **Dominio:** datos meteorológicos Madrid (open data)
- **Corpus:** incluido en `data/` (CSV, PDF, FAQ, guía)
- **Implementación principal:** `load.py` (ingesta del CSV)
- **Análisis:** experimento con `config.py`, inspección de `chunks.json` / `embeddings.json`, entregables
- **No incluye:** ChromaDB, retrieval ni generación con LLM
