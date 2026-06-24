![Cabecera](./assets/cabecera_gemini.png)

# 📘 Sprint 05 — Prompt & Context Engineering

En este sprint damos el salto de "llamar a un LLM" a **construir sistemas IA mantenibles**: código bien estructurado, prompts que realmente controlan al modelo, y gestión inteligente del contexto que le pasas.

El sprint se organiza en tres bloques temáticos que se construyen uno sobre otro:

---

## 🧱 Bloque 1 — Lógica y modularización en Python

📁 [`01_Teoria/01_Logica_y_modularizacion/`](./01_Teoria/01_Logica_y_modularizacion/)
📁 [`02_Workout/01_Logica_y_modularizacion/`](./02_Workout/01_Logica_y_modularizacion/)

El foco no es "aprender Python desde cero", sino **programar como alguien que construye sistemas mantenibles**: validar datos, controlar el flujo, separar responsabilidades y gestionar estado.

### Contenido de teoría

| # | Documento | Qué aprenderás |
|---|-----------|----------------|
| 0 | [Mentalidad: de script a sistema mantenible](./01_Teoria/01_Logica_y_modularizacion/00_Mentalidad_sistemas_mantenibles.md) | Qué separar y por qué (`config`, `prompts`, `logic`, `state`, `main`). Qué problemas evita. |
| 1 | [Condicionales complejos y validación de inputs](./01_Teoria/01_Logica_y_modularizacion/01_Condicionales_y_validacion.md) | `and`, `or`, `not`, comparaciones encadenadas, validación de strings, rangos, whitelists, regex básicas. |
| 2 | [Manejo de múltiples respuestas posibles](./01_Teoria/01_Logica_y_modularizacion/02_Multiples_respuestas_y_flujo.md) | Responder distinto según el caso, `if/elif/else` vs tabla de handlers con `dict`. |
| 3–4 | [Estructura modular y estado en memoria](./01_Teoria/01_Logica_y_modularizacion/03_Modularización_de_proyectos.md) | Separar `config`, `prompts`, `logic` y `state`. Orquestar desde un `main` mínimo. Historial en memoria. |

📁 Proyecto ejecutable: [`03_Modularización_de_proyectos_ejemplo/`](./01_Teoria/01_Logica_y_modularizacion/03_Modularización_de_proyectos_ejemplo/)

### Workout

| Notebook | Cubre teoría |
|----------|--------------|
| [01_Condicionales_y_validacion.ipynb](./02_Workout/01_Logica_y_modularizacion/01_Condicionales_y_validacion.ipynb) | Bloque 1 |
| [02_Multiples_respuestas_y_flujo.ipynb](./02_Workout/01_Logica_y_modularizacion/02_Multiples_respuestas_y_flujo.ipynb) | Bloque 2 |
| [03_Modularización_de_proyectos.md](./02_Workout/01_Logica_y_modularizacion/03_Modularización_de_proyectos.md) | Bloques 3–4 |

---

## ✍️ Bloque 2 — Prompt Engineering

📁 [`01_Teoria/02_Prompt_Engineering/`](./01_Teoria/02_Prompt_Engineering/)
📁 [`02_Workout/02_Prompt_Engineering/`](./02_Workout/02_Prompt_Engineering/)

**Ya sabemos llamar a un LLM. Ahora aprendemos a controlarlo:** rol, tarea, plantillas en Python, datos de usuario y externos, y salidas estructuradas (JSON).

*Prerrequisitos: Bloque 1 (lógica y modularización) y Sprint 04 (Gemini API, `.env`).*

### Contenido de teoría

| # | Documento | Qué aprenderás |
|---|-----------|----------------|
| 0 | [Introducción a Prompt Engineering](./01_Teoria/02_Prompt_Engineering/00_introduccion_prompt_engineering.md) | Objetivos, mapa de documentos, convenciones Gemini, función `build_prompt`. |
| 1 | [Rol del modelo](./01_Teoria/02_Prompt_Engineering/01_rol_del_modelo.md) | Qué es un rol, instrucción vs pregunta suelta, `ROLES` en Python. |
| 2 | [Definición clara de tareas](./01_Teoria/02_Prompt_Engineering/02_definicion_de_tareas.md) | Prompts ambiguos vs específicos, `build_prompt` con rol + tarea. |
| 3 | [Prompts dinámicos desde Python](./01_Teoria/02_Prompt_Engineering/03_prompts_dinamicos.md) | f-strings, plantillas, `.format()`, funciones `build_*_prompt`. |
| 4 | [Inputs de usuario](./01_Teoria/02_Prompt_Engineering/04_inputs_usuario.md) | Separar datos / prompt / llamada, validación con whitelist, perfiles. |
| 5 | [Inyección de datos externos](./01_Teoria/02_Prompt_Engineering/05_inyeccion_datos_externos.md) | Dict, JSON, CSV en el prompt, límites de tamaño, puente hacia Context Engineering. |
| 6 | [Salidas estructuradas](./01_Teoria/02_Prompt_Engineering/06_salidas_estructuradas.md) | Texto libre vs JSON, `response_mime_type` en Gemini, `json.loads`, clasificador de incidencias. |

📁 Proyecto ejecutable: [`06_proyecto_prompt_engineering_ejemplo/`](./01_Teoria/02_Prompt_Engineering/06_proyecto_prompt_engineering_ejemplo/) — `pip install google-genai python-dotenv` y `python main.py`.

### Workout

| Notebook | Cubre teoría |
|----------|--------------|
| [01_comparar_rol_y_tarea.ipynb](./02_Workout/02_Prompt_Engineering/01_comparar_rol_y_tarea.ipynb) | 1 + 2 |
| [02_prompts_dinamicos_y_usuario.ipynb](./02_Workout/02_Prompt_Engineering/02_prompts_dinamicos_y_usuario.ipynb) | 3 + 4 |
| [03_proyecto_prompt_engineering.md](./02_Workout/02_Prompt_Engineering/03_proyecto_prompt_engineering.md) | 5 + 6 |

---

## 🧠 Bloque 3 — Context Engineering

📁 [`01_Teoria/03_Context_Engineering/`](./01_Teoria/03_Context_Engineering/)
📁 [`02_Workout/03_Context_Engineering/`](./02_Workout/03_Context_Engineering/)

En el Bloque 2 aprendimos a **construir** prompts. Aquí cambiamos la pregunta:

> **¿Qué información merece la pena enviar al modelo para que responda mejor?**

Un LLM no "recuerda" nada entre llamadas. La calidad depende de **qué contexto seleccionas**, cuánto **ruido** quitas, cómo gestionas el **historial**, y cómo controlas el **presupuesto** (tokens, coste, latencia).

### Contenido de teoría

| # | Documento | Qué aprenderás |
|---|-----------|----------------|
| 1 | [Contexto y relevancia](./01_Teoria/03_Context_Engineering/01_Contexto_y_relevancia.md) | Qué es "contexto", señal vs ruido, cómo delimitar datos. |
| 2 | [Historial y memoria](./01_Teoria/03_Context_Engineering/02_Historial_y_memoria.md) | Historial conversacional, ventana corta (últimos N turnos), memoria larga simple. |
| 3 | [Coste y presupuesto de contexto](./01_Teoria/03_Context_Engineering/03_Coste_y_presupuesto_de_contexto.md) | Tokens como recurso, `count_tokens`, `usage_metadata`, estrategias de recorte. |
| 4 | [Resumen y compresión de contexto](./01_Teoria/03_Context_Engineering/04_Resumen_y_compresion_de_contexto.md) | Por qué el historial se degrada, resumen como memoria comprimida, implementación en Python. |

📁 Proyecto ejecutable: [`04_proyecto_context_engineering_ejemplo/`](./01_Teoria/03_Context_Engineering/04_proyecto_context_engineering_ejemplo/) — crea `.venv`, `pip install -r requirements.txt` y `python main.py`.

### Workout

| Notebook | Cubre teoría |
|----------|--------------|
| [01_contexto_y_relevancia.ipynb](./02_Workout/03_Context_Engineering/01_contexto_y_relevancia.ipynb) | 1 |
| [02_historial_memoria_y_resumen.ipynb](./02_Workout/03_Context_Engineering/02_historial_memoria_y_resumen.ipynb) | 2 + 4 |
| [03_coste_y_presupuesto.ipynb](./02_Workout/03_Context_Engineering/03_coste_y_presupuesto.ipynb) | 3 |
| [04_proyecto_context_engineering.md](./02_Workout/03_Context_Engineering/04_proyecto_context_engineering.md) | 1–4 integrado |
