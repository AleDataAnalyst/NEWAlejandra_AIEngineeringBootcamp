![Cabecera](../../assets/cabecera_rag.png)

# 📘 Sprint 10 · Bloque 01

## Generación aumentada con contexto

En el Sprint 9 recuperaste **contexto** relevante para cada pregunta. Ahora aprendes a **generar respuestas** con un LLM apoyándote en ese contexto.

> **¿Cómo convierto chunks recuperados en una respuesta útil?**

Salida de este bloque: un pipeline online que devuelve **respuesta + fuentes** (Gemini como camino principal).

---

## 📂 Contenido de la teoría (orden de lectura)

### 🧭 0. Introducción

🔗 [Abrir](./00_introduccion_generacion_rag.md)

* Puente desde Sprint 9
* Pasos 6–7 del pipeline RAG
* Objetivo del bloque

---

### 🔗 1. Del retrieval a la respuesta

🔗 [Abrir](./01_del_retrieval_a_la_respuesta.md)

* `pregunta → retriever → contexto → LLM → respuesta`
* Qué es RAG de verdad
* La función `responder(pregunta)`

---

### 📝 2. Prompt con contexto recuperado

🔗 [Abrir](./02_prompt_con_contexto_recuperado.md)

* Separar instrucciones, contexto y pregunta
* Grounding: responder solo con el contexto
* Citas y abstención

---

### 🤖 3. Generación con Gemini y alternativas

🔗 [Abrir](./03_generacion_con_gemini_y_alternativas.md)

* Llamada a Gemini (`generate_content`)
* Hugging Face como alternativa (misma arquitectura)
* Intercambiabilidad del proveedor

---

## Workout (vídeo guiado)

| Recurso | Cubre |
|---------|--------|
| [01_del_retrieval_a_la_respuesta_rag.ipynb](../../02_Workout/01_Generacion_aumentada_con_contexto/01_del_retrieval_a_la_respuesta_rag.ipynb) | Generación RAG completa |

El **proyecto modular** completo está en el [Bloque 3 — Interfaces y aplicaciones](../03_Interfaces_y_aplicaciones_rag/readme.md).
