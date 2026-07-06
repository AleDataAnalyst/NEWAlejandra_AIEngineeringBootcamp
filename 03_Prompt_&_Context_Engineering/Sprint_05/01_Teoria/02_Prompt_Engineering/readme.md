![Cabecera](../../assets/cabecera_gemini.png)

# 📘 Sprint 05 · Unidad 02

## Prompt Engineering

**Ya sabemos llamar a un LLM. Ahora aprendemos a controlarlo:** rol, tarea, plantillas en Python, datos de usuario y externos, y salidas estructuradas (JSON).

Prerrequisitos: Unidad 01 (lógica y modularización) y Sprint 4 (Gemini API, `.env`).

---

## 📂 Contenido de la teoría (orden de lectura)

---

### 📄 0. Introducción a Prompt Engineering

🔗 [Abrir](./00_introduccion_prompt_engineering.md)

**¿Qué aprenderás?**

* Objetivos de la unidad y mapa de documentos
* Convenciones Gemini y organización `prompts.py` / `config.py`
* Función mental `build_prompt(role, task, user_input, additional_data)`

---

### 🎭 1. Rol del modelo

🔗 [Abrir](./01_rol_del_modelo.md)

**¿Qué aprenderás?**

* Qué es un rol y cómo condiciona la respuesta
* Instrucción vs pregunta suelta
* Rol, objetivo, audiencia, restricciones
* `ROLES` en Python y comparación con Gemini

---

### ✅ 2. Definición clara de tareas

🔗 [Abrir](./02_definicion_de_tareas.md)

**¿Qué aprenderás?**

* Prompts ambiguos vs específicos
* Buenas prácticas del syllabus
* Entregables, delimitación, tareas por tipo (`summary` / `translate` / `qa`)
* `build_prompt` con rol + tarea

---

### 🔧 3. Prompts dinámicos desde Python

🔗 [Abrir](./03_prompts_dinamicos.md)

**¿Qué aprenderás?**

* f-strings, plantillas, `.format()`
* De hardcode a funciones `build_*_prompt`
* Generador de resúmenes con Gemini
* Depuración del prompt antes de enviar

---

### 👤 4. Inputs de usuario

🔗 [Abrir](./04_inputs_usuario.md)

**¿Qué aprenderás?**

* Separar datos / prompt / llamada
* Idioma, tono, objetivo (generador de emails)
* Validación con whitelist
* Perfiles de usuario

---

### 📦 5. Inyección de datos externos

🔗 [Abrir](./05_inyeccion_datos_externos.md)

**¿Qué aprenderás?**

* Dict, JSON, CSV en el prompt
* Instrucciones vs datos de referencia vs petición
* Límites de tamaño (introducción)
* Puente hacia Context Engineering (Unidad 3)

---

### 📋 6. Salidas estructuradas

🔗 [Abrir](./06_salidas_estructuradas.md)

**¿Qué aprenderás?**

* Texto libre vs JSON
* `response_mime_type` en Gemini
* `json.loads`, whitelist, `respuesta_ok` / error
* Clasificador de incidencias

---

## Demos ejecutables (teoría)

| Demo | Tipo | Cubre teoría |
|------|------|----------------|
| [01_comparar_rol_y_tarea_ejemplos.ipynb](./01_comparar_rol_y_tarea_ejemplos.ipynb) | Notebook | 01 + 02 |
| [02_prompts_dinamicos_y_usuario_ejemplos.ipynb](./02_prompts_dinamicos_y_usuario_ejemplos.ipynb) | Notebook | 03 + 04 |
| [proyecto_prompt_engineering_ejemplo/](./proyecto_prompt_engineering_ejemplo/) | Proyecto `.py` | 05 + 06 |

**Proyecto:** desde `proyecto_prompt_engineering_ejemplo/`, `pip install google-genai python-dotenv` y `python main.py` (`.env` o `getpass`, como Sprint 4).
