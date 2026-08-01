![Cabecera](../../assets/cabecera_rag.png)

# 📘 Sprint 10 · Bloque 02

## Calidad, robustez y evaluación

Un RAG que «responde bien» en una demo puede fallar con otras preguntas, inventar datos o ignorar el corpus. Este bloque enseña a **evaluar respuestas generadas** y a hacer el sistema más fiable.

> **¿Cómo sé si la respuesta es buena — y qué hago cuando falla?**

Salida de este bloque: criterios claros para juzgar respuestas y ajustar prompt, top-K o retrieval.

---

## 📂 Contenido de la teoría (orden de lectura)

### 🧭 0. Introducción

🔗 [Abrir](./00_introduccion_evaluacion_generacion.md)

* Eval retrieval (S9) vs eval respuesta (S10)
* Por qué un buen top-K no basta

---

### 📊 1. Cómo evaluar respuestas RAG

🔗 [Abrir](./01_como_evaluar_respuestas_rag.md)

* Exactitud, relevancia, coherencia
* Trazabilidad a fuentes

---

### ⚠️ 2. Alucinaciones y grounding

🔗 [Abrir](./02_hallucinations_y_grounding.md)

* Qué es alucinar en RAG
* Prompt restrictivo y abstención

---

### 🛡️ 3. Prompt injection y validación de fuentes

🔗 [Abrir](./03_prompt_injection_y_validacion_de_fuentes.md)

* Inyección en documentos recuperados
* Validación de metadata y fuentes

---

### 📋 4. Buenas prácticas y limitaciones

🔗 [Abrir](./04_buenas_practicas_y_limitaciones_rag.md)

* Límites del corpus, chunking, top-K
* Qué no puede hacer un RAG

---

## Workout (vídeo guiado)

| Recurso | Cubre |
|---------|--------|
| [01_evaluar_respuestas_rag.ipynb](../../02_Workout/02_Calidad_robustez_y_evaluacion/01_evaluar_respuestas_rag.ipynb) | Evaluación práctica de respuestas |
