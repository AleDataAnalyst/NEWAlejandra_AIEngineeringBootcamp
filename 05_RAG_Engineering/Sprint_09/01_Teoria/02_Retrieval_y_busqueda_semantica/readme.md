![Cabecera](../../assets/cabecera_rag.png)

# 📘 Sprint 09 · Bloque 02

## Retrieval y búsqueda semántica

Con el corpus **indexado en ChromaDB** (Bloque 1), ahora implementas el **retriever**: dada una pregunta, devuelve los fragmentos más relevantes.

> **¿Cómo recupero automáticamente los chunks más útiles para una consulta?**

Salida de este bloque: función `recuperar(pregunta)` que devuelve top-K chunks con scores y contexto formateado. **Sin llamar al LLM.**

---

## 📂 Contenido de la teoría (orden de lectura)

### 🧭 0. Introducción

🔗 [Abrir](./00_introduccion_retrieval.md)

* Pasos 1–5 del pipeline online
* Retrieval ≠ generation

---

### 🔍 1. Retrieval y similarity search

🔗 [Abrir](./01_retrieval_y_similarity_search.md)

* Qué es retrieval; top-K; distancias en Chroma

---

### 📎 2. Recuperación, embeddings y contexto

🔗 [Abrir](./02_recuperacion_embeddings_y_contexto.md)

* Embed de la pregunta; construir el contexto recuperado

---

### ⚙️ 3. Configuración del retriever

🔗 [Abrir](./03_configuracion_del_retriever.md)

* `TOP_K`, filtros; retriever modular vs wrapper LangChain

---

## Workout

| Recurso | Cubre |
|---------|--------|
| [01_implementar_retriever.ipynb](../../02_Workout/02_Retrieval_y_busqueda_semantica/01_implementar_retriever.ipynb) | Similarity search + contexto |
