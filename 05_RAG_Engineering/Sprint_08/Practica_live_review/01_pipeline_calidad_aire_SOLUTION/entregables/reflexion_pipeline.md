# Reflexión del pipeline — Sprint 08 Live Review

Completa tras generar `output/embeddings.json` (Fase 2). Apoya las respuestas con **datos de tus artefactos** (`chunks.json`, `embeddings.json`, consola).

## 1. Inspección de artefactos

Abre un item de `output/chunks.json` y el correspondiente en `output/embeddings.json`.

El **item 0** de ambos archivos coincide: mismo texto («Medición: Velocidad del viento (código 81)…») y misma metadata (`magnitud: "81"`, `municipio: "102"`, `estacion: "1"`, `tipo: "meteo_medicion"`). El vector tiene **3072 dimensiones** y el JSON raíz indica el modelo **`gemini-embedding-2`**. La correspondencia texto ↔ vector ↔ metadata es 1:1 por índice en la lista `items`.

## 2. Metadata útil para retrieval

En el CSV guardé `tipo`, `magnitud`, `municipio`, `estacion`, `punto_muestreo` y `source`. Ejemplo de pregunta filtrable: *«¿Qué temperaturas hubo en julio en la estación 1 del municipio 102?»* — se puede filtrar por `magnitud = 83`, `estacion = 1` y `municipio = 102` antes o después de la búsqueda vectorial.

## 3. Fuentes distintas

El **FAQ** explica códigos, columnas h01–h24 y validaciones (V/N/T) de forma general. El **CSV** trae valores numéricos hora a hora con su validación (p. ej. `12:00 → 32,8 (validación V)` para temperatura).

- Pregunta **conceptual** («¿Qué significa validación T?», «¿Qué mide el código 86?») → **FAQ** o **PDF**.
- Pregunta con **valores concretos** («¿Cuánto llovió a las 18:00?», «¿Temperatura máxima del día?») → **CSV**.

## 4. Embeddings: modelo y límites

| Campo | Valor en tu `embeddings.json` |
|-------|-------------------------------|
| Modelo | gemini-embedding-2 |
| Dimensiones | 3072 |
| Chunks embeddeados vs total en `chunks.json` | 50 / 112 |

`MAX_CHUNKS_EMBED = 50` limita cuántos chunks se envían a la API en la práctica (coste, tiempo y cuota). En un sistema real embeddearías **todo** el corpus indexado o aplicarías filtros por metadata para no vectorizar datos que nunca se consultarán. Si solo indexas 50 de 112 chunks, las preguntas sobre filas no embeddeadas no tendrían contexto recuperable.

## 5. Puente al retrieval

Faltan tres piezas: (1) **indexar** los vectores de `embeddings.json` en un vector store (ChromaDB en Sprint 9); (2) **embeddear la pregunta** del usuario con el **mismo** modelo (`gemini-embedding-2`); (3) **recuperar top-k** chunks por similitud coseno y pasarlos a un LLM para generar la respuesta. Este pipeline solo produce los artefactos offline; aún no hay retrieval ni generación.

## 6. Experimento opcional — otro proveedor

Si quieres ir más allá: prueba un modelo de embeddings de **Hugging Face** (p. ej. `sentence-transformers/all-MiniLM-L6-v2`) con el mismo texto de un chunk y anota dimensiones y diferencias respecto a Gemini.

(Opcional) `all-MiniLM-L6-v2` devuelve **384 dimensiones**, frente a **3072** de Gemini. **No** mezclaría índices de distintos proveedores: el embedder al indexar y al consultar debe ser el mismo, o los vectores no son comparables en el mismo espacio semántico.
