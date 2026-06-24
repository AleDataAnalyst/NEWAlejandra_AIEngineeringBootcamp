![Cabecera](../../assets/cabecera_gemini.png)

# 📘 Sprint 05 · Unidad 03

## Context Engineering

En la Unidad 02 aprendimos a **construir** prompts. Aquí cambiamos la pregunta:

> **¿Qué información merece la pena enviar al modelo para que responda mejor?**

Un LLM no “recuerda” nada entre llamadas. La calidad depende muchísimo de **qué contexto seleccionas**, cuánto **ruido** quitas, cómo gestionas **historial**, y cómo controlas el **presupuesto** (tokens, coste, latencia).

---

## 📂 Contenido de la teoría (orden de lectura)

---

### 🧠 1. Contexto y relevancia (incluye ruido)

🔗 [Abrir](./01_Contexto_y_relevancia.md)

**¿Qué aprenderás?**

* Qué es “contexto” en una llamada a un LLM
* Señal vs ruido: por qué “más texto” puede empeorar la respuesta
* Cómo delimitar datos y evitar mezclar instrucciones con contenido
* Mini-demos en Python (mismo prompt, distinto contexto)

---

### 💬 2. Historial y memoria (corta vs larga)

🔗 [Abrir](./02_Historial_y_memoria.md)

**¿Qué aprenderás?**

* Historial conversacional: reenviar mensajes para “memoria aparente”
* Ventana corta: últimos N turnos / últimos N elementos
* Memoria “larga” simple (sin embeddings): perfil del usuario / estado persistente
* Patrones Python con `state.py` (continuidad Unidad 01)

---

### 💸 3. Coste y presupuesto de contexto

🔗 [Abrir](./03_Coste_y_presupuesto_de_contexto.md)

**¿Qué aprenderás?**

* Tokens como recurso: input + output
* Cómo medir y registrar: `count_tokens` y `usage_metadata`
* Estrategias de recorte: top‑N, filtros, campos mínimos
* Reglas prácticas para apps reales (coste/latencia/calidad)

---

### 🗜️ 4. Resumen y compresión de contexto

🔗 [Abrir](./04_Resumen_y_compresion_de_contexto.md)

**¿Qué aprenderás?**

* Por qué el historial crece y cómo se degrada la calidad
* Resumen como “memoria comprimida”
* Estrategia simple: `summary + últimos mensajes`
* Implementación en Python (resumen periódico y control de tamaño)

---

## Demos ejecutables (teoría)

| Demo | Tipo | Cubre teoría |
|------|------|----------------|
| [01_contexto_y_relevancia_ejemplos.ipynb](./01_contexto_y_relevancia_ejemplos.ipynb) | Notebook | 01 |
| [02_historial_memoria_y_resumen_ejemplos.ipynb](./02_historial_memoria_y_resumen_ejemplos.ipynb) | Notebook | 02 + 04 |
| [03_coste_y_presupuesto_ejemplos.ipynb](./03_coste_y_presupuesto_ejemplos.ipynb) | Notebook | 03 |
| [04_proyecto_context_engineering_ejemplo/](./04_proyecto_context_engineering_ejemplo/) | Proyecto `.py` | 01–04 integrado |

**Proyecto:** desde `04_proyecto_context_engineering_ejemplo/`, crea `.venv`, `pip install -r requirements.txt` y `python main.py` (`.env` o `getpass`, como Sprint 4).

