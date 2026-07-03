![Cabecera](./assets/cabecera_gemini.png)

# 📘 Sprint 06 — Assistant Engineering & Robustez

En el Sprint 5 aprendiste a **organizar código**, **construir prompts**, **elegir contexto** y **gestionar historial y tokens**.

En este sprint damos el salto de “llamadas sueltas a Gemini” a **diseñar asistentes como sistemas** y **endurecerlos** cuando el usuario puede escribir cualquier cosa.

El sprint se organiza en dos bloques que se construyen uno sobre otro:

---

## 🏗️ Bloque 1 — Arquitectura de asistentes

📁 [`01_Teoria/01_Arquitectura_asistentes/`](./01_Teoria/01_Arquitectura_asistentes/)
📁 [`02_Workout/01_Arquitectura_asistentes/`](./02_Workout/01_Arquitectura_asistentes/)

> **Dejar de pensar en “un prompt” y empezar a pensar en un asistente como producto:** capas (`config`, `state`, `prompts`, `logic`, `main`), estado de sesión, perfiles y un flujo por turno.

*Prerrequisitos: Sprint 5 (lógica, prompts y contexto) y Sprint 4 (Gemini API, `.env` / `getpass`).*

### Contenido de teoría

| # | Documento | Qué aprenderás |
|---|-----------|----------------|
| 0 | [Introducción a Assistant Engineering](./01_Teoria/01_Arquitectura_asistentes/00_introduccion_assistant_engineering.md) | Objetivos, mapa del sprint, prompt aislado vs asistente estructurado. |
| 1 | [Conceptos y arquitectura](./01_Teoria/01_Arquitectura_asistentes/01_Conceptos_y_arquitectura.md) | Capas del asistente, `assistant_config`, perfiles, estado de sesión. |
| 2 | [Flujos e integración](./01_Teoria/01_Arquitectura_asistentes/02_Flujos_e_integracion.md) | Pipeline por turno, `build_assistant_prompt`, orquestación en `logic.py`. |

📁 Proyecto ejecutable: [`03_proyecto_asistente_estudio_ejemplo/`](./01_Teoria/01_Arquitectura_asistentes/03_proyecto_asistente_estudio_ejemplo/) — `.venv`, `pip install -r requirements.txt` y `python main.py`.

### Workout

| Notebook / guía | Cubre teoría |
|-----------------|--------------|
| [01_de_prompt_suelto_a_asistente.ipynb](./02_Workout/01_Arquitectura_asistentes/01_de_prompt_suelto_a_asistente.ipynb) | 0 + 1 |
| [02_estado_y_configuracion.ipynb](./02_Workout/01_Arquitectura_asistentes/02_estado_y_configuracion.ipynb) | 1 |
| [03_proyecto_asistentes_conversacionales.md](./02_Workout/01_Arquitectura_asistentes/03_proyecto_asistentes_conversacionales.md) | 2 + proyecto |

Índice detallado de la unidad: [`01_Teoria/01_Arquitectura_asistentes/readme.md`](./01_Teoria/01_Arquitectura_asistentes/readme.md)

---

## 🛡️ Bloque 2 — Robustez y seguridad

📁 [`01_Teoria/02_Robustez_y_seguridad/`](./01_Teoria/02_Robustez_y_seguridad/)
📁 [`02_Workout/02_Robustez_y_seguridad/`](./02_Workout/02_Robustez_y_seguridad/)

> **El modelo no cambia; cambia el sistema que lo envuelve:** validación en Python, dominio acotado, prompts con delimitadores y salidas controladas (JSON + parseo).

*Prerrequisito: Bloque 1 (arquitectura de asistente).*

### Contenido de teoría

| # | Documento | Qué aprenderás |
|---|-----------|----------------|
| 0 | [Introducción a robustez y seguridad](./01_Teoria/02_Robustez_y_seguridad/00_introduccion_robustez_y_seguridad.md) | Prompt injection, mentalidad “defensa en capas”. |
| 1 | [Prompt injection y defensas de prompt](./01_Teoria/02_Robustez_y_seguridad/01_Prompt_injection_y_defensas_de_prompt.md) | Vulnerable vs seguro, `SYSTEM_PROMPT`, delimitadores, dominio. |
| 2 | [Validación, outputs y defensa en capas](./01_Teoria/02_Robustez_y_seguridad/02_Validacion_outputs_y_defensa_en_capas.md) | `validate_input`, JSON forzado, comparativa vulnerable/seguro. |

📁 Proyecto ejecutable: [`03_proyecto_asistente_seguro_ejemplo/`](./01_Teoria/02_Robustez_y_seguridad/03_proyecto_asistente_seguro_ejemplo/) — `.venv`, `pip install -r requirements.txt` y `python main.py`.

### Workout

| Notebook / guía | Cubre teoría |
|-----------------|--------------|
| [01_asistente_vulnerable.ipynb](./02_Workout/02_Robustez_y_seguridad/01_asistente_vulnerable.ipynb) | 0 + 1 |
| [02_defensas_prompt_y_dominio.ipynb](./02_Workout/02_Robustez_y_seguridad/02_defensas_prompt_y_dominio.ipynb) | 1 |
| [03_proyecto_asistente_seguro.md](./02_Workout/02_Robustez_y_seguridad/03_proyecto_asistente_seguro.md) | 2 + proyecto |

Índice detallado de la unidad: [`01_Teoria/02_Robustez_y_seguridad/readme.md`](./01_Teoria/02_Robustez_y_seguridad/readme.md)

---

## 🎯 Práctica Live Review — Tutor del bootcamp

📁 [`Practica_live_review/01_tutor_bootcamp/`](./Practica_live_review/01_tutor_bootcamp/)

Práctica integradora en **dos sesiones** que une Bloque 1 y Bloque 2:

1. **Fase 1 — Arquitectura:** tutor con perfiles, memoria de sesión y `procesar_turno`.
2. **Fase 2 — Seguridad:** validación, dominio y comparativa vulnerable vs seguro.

Enunciado completo: [`Practica_live_review/01_tutor_bootcamp/README.md`](./Practica_live_review/01_tutor_bootcamp/README.md)

**Consejo:** durante el desarrollo puedes **comentar demos** en `main.py` para no saturar la API; antes de cerrar la práctica, ejecuta `python main.py` con todas las demos activas.
