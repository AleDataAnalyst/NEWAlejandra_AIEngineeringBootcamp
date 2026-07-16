![Cabecera](../../assets/cabecera_rag.png)

# 📘 Sprint 08 · Bloque 01

## Introducción a RAG y arquitectura

En los Sprints 5 y 6 construiste **asistentes** que inyectaban contexto (FAQ, historial, perfil). En el Sprint 7 viste que los **embeddings** sirven para búsqueda semántica y RAG.

Aquí la pregunta cambia:

> **¿Qué es un sistema RAG y cómo fluye la información antes de programar el pipeline?**

Este bloque es **conceptual**: entiendes el problema, la arquitectura y las herramientas. El código empieza en el Bloque 2 (ingesta).

---

## 📂 Contenido de la teoría (orden de lectura)

---

### 🧭 0. Introducción

🔗 [Abrir](./00_introduccion_rag.md)

* Mapa del Sprint 08 y del Módulo 4 (S8 → S9 → S10)
* Objetivos del bloque
* Puente desde Context Engineering (S5)

---

### 💡 1. Qué es RAG y limitaciones del LLM

🔗 [Abrir](./01_que_es_rag_y_limitaciones_llm.md)

* Limitaciones de un LLM sin contexto privado
* Casos de uso reales de RAG
* Prompt engineering vs fine-tuning vs RAG

---

### 🏗️ 2. Arquitectura y componentes

🔗 [Abrir](./02_arquitectura_y_componentes.md)

* Componentes del pipeline RAG
* Flujo offline (preparar) vs online (consultar)
* Recuperación ≠ generación

---

### 🛠️ 3. Tecnologías del módulo

🔗 [Abrir](./03_tecnologias_del_modulo.md)

* Stack: Gemini, LangChain, ChromaDB
* Convenciones de proyectos modulares en este módulo
* Qué verás en cada sprint

*Bloque conceptual: sin workout en vídeo. Los escenarios «¿RAG o no?» y el diagrama del flujo están en los `.md` de arriba.*
