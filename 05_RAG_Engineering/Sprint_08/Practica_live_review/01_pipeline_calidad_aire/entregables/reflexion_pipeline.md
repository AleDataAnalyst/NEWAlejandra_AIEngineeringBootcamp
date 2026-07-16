# Reflexión del pipeline — Sprint 08 Live Review

Completa tras generar `output/embeddings.json` (Fase 2). Apoya las respuestas con **datos de tus artefactos** (`chunks.json`, `embeddings.json`, consola).

## 1. Inspección de artefactos

Abre un item de `output/chunks.json` y el correspondiente en `output/embeddings.json`.

TODO — ¿Coinciden el texto y la metadata? ¿Cuántas dimensiones tiene el vector? ¿Qué modelo de embedding aparece en el JSON?

## 2. Metadata útil para retrieval

¿Qué campos guardaste en metadata del CSV (`magnitud`, `municipio`, …)?

TODO — Pon un **ejemplo concreto** de pregunta de usuario que podrías filtrar con esa metadata.

## 3. Fuentes distintas

Compara el FAQ con una medición del CSV (magnitud 83, por ejemplo).

TODO — ¿Qué fuente usarías para una pregunta conceptual (códigos V/N/T) y cuál para una pregunta con valores horarios concretos?

## 4. Embeddings: modelo y límites

| Campo | Valor en tu `embeddings.json` |
|-------|-------------------------------|
| Modelo | TODO |
| Dimensiones | TODO |
| Chunks embeddeados vs total en `chunks.json` | TODO / TODO |

TODO — ¿Por qué `MAX_CHUNKS_EMBED` puede ser menor que el total de chunks? ¿Qué implicación tiene en un sistema real?

## 5. Puente al retrieval

TODO — En 3 frases: qué falta para poder hacer una pregunta y recuperar contexto relevante (ChromaDB u otro vector store).

## 6. Experimento opcional — otro proveedor

Si quieres ir más allá: prueba un modelo de embeddings de **Hugging Face** (p. ej. `sentence-transformers`) con el mismo texto de un chunk y anota dimensiones y diferencias respecto a Gemini.

TODO — (Opcional) ¿Mismo número de dimensiones? ¿Mezclarías índices de distintos proveedores? ¿Por qué sí o no?
