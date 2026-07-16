![Cabecera](../../assets/cabecera_rag.png)

# Introducción: embeddings en RAG

Anteriormente hemos visto cómo hacer ingesta de datos, pasarlo a formato de texto y generar **chunks**. Ahora nos encargaremos de **vectorizar** los datos para poder usarlos en la búsqueda semántica con RAG. Haremos lo que se llama **Embeddings**.

> **Embedding** = representación numérica densa de un fragmento de texto, de forma que textos parecidos en significado tengan vectores cercanos.

---

## Objetivos del bloque

Al terminar, deberías poder:

- Explicar qué es un **vector de embedding** y por qué sirve en RAG.
- Calcular **similitud del coseno** entre dos vectores (intuición, sin álgebra avanzada).
- Generar embeddings con la **API de Gemini** (`embed_content`).
- Conocer la alternativa **Hugging Face** local para comparación.
- Elegir criterios básicos para un modelo de embedding en tu pipeline.
- Persistir `{text, vector, metadata}` listo para el Sprint 9.

---

## Dónde encaja en el pipeline

```text
  [ Bloque 2 ]
  chunks.json
       │
       ▼
  [ Bloque 3 — este bloque ]
  embed.py  ──►  embeddings.json
       │
       ▼
  [ Sprint 9 ]
  ChromaDB.index()
```

---

## Puente desde Sprint 7

En el Sprint7 hablamos de familias de modelos:

```text
  Pregunta → Embedding → índice vectorial → top-K chunks → LLM
```

En este sprint **implementaremos** la caja «Embedding» sobre tus chunks del bootcamp.

---

## Puente desde Sprint 5

En el Sprint 5 hablamos de **keywords**:

`seleccionar_faq()` comparaba **keywords** (coincidencia literal). Los embeddings comparan **significado**:

| Método | «live review» vs «sesión en vivo del sprint» |
|--------|-----------------------------------------------|
| Keywords | Puede no coincidir si no comparten palabras |
| Embeddings | Suele detectar similitud semántica |

---

## Salida concreta de lo que saldría de ejemplos embeddings

Archivo `output/embeddings.json`:

```json
{
  "embedding_model": "text-embedding-004",
  "total": 3,
  "items": [
    {
      "text": "La Live Review es una sesión en vivo...",
      "vector": [0.012, -0.034, "..."],
      "metadata": { "source": "data/faq_agenda_cultural.md", "chunk_index": 0 }
    }
  ]
}
```

En Sprint 9 cargarás estos vectores en **ChromaDB**. Todavía **no** haremos búsqueda ni generación con LLM.

---

## Tabla guía de lectura

| # | Documento | Enfoque |
|---|-----------|---------|
| 1 | [Vectores y similitud](./01_vectores_y_similitud_semantica.md) | Intuición matemática mínima |
| 2 | [Embeddings Gemini](./02_embeddings_gemini.md) | API y código |
| 3 | [Hugging Face](./03_embeddings_huggingface.md) | Alternativa local |
| 4 | [Comparación](./04_comparacion_modelos_embedding.md) | Elegir modelo |