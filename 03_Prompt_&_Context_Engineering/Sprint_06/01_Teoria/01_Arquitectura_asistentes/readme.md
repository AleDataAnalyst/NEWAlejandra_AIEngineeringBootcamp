# 📘 Sprint 06 · Unidad 01

## Assistant Engineering — Asistentes conversacionales

En **Sprint 5** aprendiste a **organizar código**, **construir prompts**, **elegir contexto** y **gestionar historial y tokens**.

En **esta unidad** el foco cambia:

> **Dejar de pensar en “una llamada a Gemini” y empezar a pensar en un asistente como sistema.**

Un asistente no es un prompt largo: es **arquitectura** (módulos), **estado** (qué recuerda la sesión), **configuración** (cómo se comporta) y un **flujo** que une prompts, contexto y respuesta en cada turno.

Prerrequisitos: Sprint 5 (Unidades 01–03), Sprint 4 (Gemini API, `getpass` / `.env`).

---

## 📂 Contenido de la teoría (orden de lectura)

---

### 📄 0. Introducción a Assistant Engineering

🔗 [Abrir](./00_introduccion_assistant_engineering.md)

**¿Qué aprenderás?**

* Objetivos del sprint y mapa de documentos
* Diferencia entre prompt aislado y asistente estructurado
* Convenciones de código y continuidad con Sprint 5

---

### 🏗️ 1. Conceptos y arquitectura del asistente

🔗 [Abrir](./01_Conceptos_y_arquitectura.md)

**¿Qué aprenderás?**

* Qué es un asistente conversacional (vs una sola llamada al LLM)
* Arquitectura básica: capas y responsabilidades (`config`, `state`, `prompts`, `logic`, `main`)
* Estado de sesión (`user_state`, historial)
* Configuración del asistente (`assistant_config`)
* Personalización por perfiles (junior / senior / mentor)

---

### 🔁 2. Flujos conversacionales e integración

🔗 [Abrir](./02_Flujos_e_integracion.md)

**¿Qué aprenderás?**

* Flujo de un turno: input → contexto → prompt → Gemini → respuesta → estado
* Función unificada `build_assistant_prompt(...)` (prompts + contexto de Sprint 5)
* Patrones de orquestación en `logic.py`
* Errores frecuentes al pasar de demo a producto

---

## Demos ejecutables

| Demo | Tipo 
|------|------
| [01_de_prompt_suelto_a_asistente.ipynb](../../02_Workout/01_Arquitectura_asistentes/01_de_prompt_suelto_a_asistente.ipynb) | Notebook 
| [02_estado_y_configuracion.ipynb](../../02_Workout/01_Arquitectura_asistentes/02_estado_y_configuracion.ipynb) | Notebook 
| [03_proyecto_asistente_estudio_ejemplo/](./03_proyecto_asistente_estudio_ejemplo/) | Proyecto `.py` 

**Proyecto:** desde [`03_proyecto_asistente_estudio_ejemplo/`](./03_proyecto_asistente_estudio_ejemplo/), crea `.venv`, `pip install -r requirements.txt` y `python main.py` (`.env` o `getpass`, como Sprint 4).


