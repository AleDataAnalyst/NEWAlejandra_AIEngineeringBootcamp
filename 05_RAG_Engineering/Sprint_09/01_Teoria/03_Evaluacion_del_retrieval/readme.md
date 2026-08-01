![Cabecera](../../assets/cabecera_rag.png)

# 📘 Sprint 09 · Bloque 03

## Evaluación del retrieval

Un retriever que «parece funcionar» en una demo puede fallar con otras preguntas. Este bloque enseña a **medir, comparar y mejorar** la recuperación **antes** de enganchar con un LLM para responder preguntas (Sprint 10).

> **¿Cómo sé si estoy recuperando el contexto correcto?**

Salida de este bloque: criterios y herramientas para evaluar retrieval + proyecto **motor de búsqueda semántica** completo.

---

## 📂 Contenido de la teoría (orden de lectura)

### 🧭 0. Introducción

🔗 [Abrir](./00_introduccion_evaluacion_retrieval.md)

* Por qué evaluar retrieval por separado del LLM

---

### ✅ 1. Evaluar calidad y fallos

🔗 [Abrir](./01_evaluar_calidad_y_fallos.md)

* Preguntas de prueba; casos típicos de fallo

---

### 🔧 2. Ajuste, logging y depuración

🔗 [Abrir](./02_ajuste_logging_y_depuracion.md)

* Chunking, top-K, trazas de depuración

---

### 📋 3. Comparación de resultados

🔗 [Abrir](./03_comparacion_de_resultados.md)

* Tablas comparativas; elegir configuración para S10

---

## Proyecto modular

📁 [`05_proyecto_rag_retrieval_busqueda_semantica/`](./05_proyecto_rag_retrieval_busqueda_semantica/)

Pipeline acumulativo S8 + S9: ingesta → embeddings → Chroma → retrieve → eval.

## Workout

| Recurso | Cubre |
|---------|--------|
| [01_evaluar_y_ajustar_retrieval.ipynb](../../02_Workout/03_Evaluacion_del_retrieval/01_evaluar_y_ajustar_retrieval.ipynb) | Evaluación práctica |
| [02_proyecto_rag_retrieval_busqueda_semantica.md](../../02_Workout/03_Evaluacion_del_retrieval/02_proyecto_rag_retrieval_busqueda_semantica.md) | Guía al repositorio del proyecto |
