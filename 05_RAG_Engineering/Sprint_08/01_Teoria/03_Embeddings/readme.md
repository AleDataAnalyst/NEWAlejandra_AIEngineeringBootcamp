![Cabecera](../../assets/cabecera_rag.png)

# 📘 Sprint 08 · Bloque 03

## Embeddings

Tras convertir documentos en **chunks** (Bloque 2), el siguiente paso es transformarlos en **vectores numéricos** que capturen su significado semántico.

> **¿Cómo convierto esos fragmentos en conocimiento recuperable?**

Salida de este bloque: **`output/embeddings.json`** con `{text, vector, metadata}` por chunk. Listo para indexar en ChromaDB (Sprint 9).

---

## 📂 Contenido de la teoría (orden de lectura)

---

### 🧭 0. Introducción

🔗 [Abrir](./00_introduccion_embeddings_rag.md)

* Puente desde Sprint 7 (familia embeddings)
* Objetivos y salida del bloque

---

### 📐 1. Vectores y similitud semántica

🔗 [Abrir](./01_vectores_y_similitud_semantica.md)

* Representación vectorial del texto
* Similitud del coseno (intuición; diagramas en teoría)

---

### ✨ 2. Embeddings con Gemini

🔗 [Abrir](./02_embeddings_gemini.md)

* API `embed_content` con `google-genai`
* Batch, dimensiones, buenas prácticas

---

### 🤗 3. Embeddings con Hugging Face

🔗 [Abrir](./03_embeddings_huggingface.md)

* `sentence-transformers` en local
* Cuándo usarlo vs Gemini

---

### ⚖️ 4. Comparación de modelos

🔗 [Abrir](./04_comparacion_modelos_embedding.md)

* Misma frase, paráfrasis, otro idioma
* Criterios de elección (estilo Sprint 7)

---

**Proyecto:** [05_proyecto_ingesta_chunking_embedding/](./05_proyecto_ingesta_chunking_embedding/) — pipeline load → clean → chunk → embed.

**Workout (vídeo):**

| Recurso | Cubre |
|---------|--------|
| [01_embeddings.ipynb](../../02_Workout/03_Embeddings/01_embeddings.ipynb) | API Gemini |
| [02_comparar_modelos_embedding.ipynb](../../02_Workout/03_Embeddings/02_comparar_modelos_embedding.ipynb) | HF vs Gemini (incluye similitud real) |
| [03_proyecto_rag_ingesta_chunking_embeddings.md](../../02_Workout/03_Embeddings/03_proyecto_rag_ingesta_chunking_embeddings.md) | Proyecto modular |
