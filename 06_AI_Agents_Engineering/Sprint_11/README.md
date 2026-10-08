![Cabecera](./assets/cabecera_agentes.png)

# 📘 Sprint 11 — Agent Foundations

En el Sprint 10 cerraste el ciclo **RAG**: `responder(pregunta) → dict`, evaluación de respuestas e interfaz Streamlit. En este sprint das el salto a **agentes**: un sistema que planifica en **varios pasos**, mantiene **estado de ejecución** y sabe **cuándo parar**.

Todavía **no** usas tools ni el RAG como herramienta. Eso llega en el Sprint 12.

El sprint responde a una pregunta central:

> **Si ya sé responder con RAG en una llamada, ¿cómo planifico en varios pasos con estado y control?**

---

## Mapa del módulo (Sprints 11–13)

| Sprint | Pregunta | Fase |
|--------|----------|------|
| **11** (este) | ¿Qué es un agente y cómo mantiene estado? | Fundamentos |
| **12** | ¿Cómo actúa con herramientas (+ RAG)? | Tool use + LangGraph básico |
| **13** | ¿Cómo planifica con autonomía controlada? | LangGraph (proyecto) + HITL |

```text
S10  pregunta → responder() → una respuesta (+ fuentes)
 ↓
S11  mensaje  → procesar_turno() → conversación + AgentState → resultado
 ↓
S12  + tools (incluida búsqueda RAG) + notebooks LangGraph (API básica)
 ↓
S13  agente en LangGraph + HITL (+ multimodal / multi-agente intro)
```

---

## 🧭 Bloque 1 — Fundamentos de los agentes

📁 [`01_Teoria/01_Fundamentos_de_los_agentes/`](./01_Teoria/01_Fundamentos_de_los_agentes/)

> Entender **qué** es un agente y **cuándo** usarlo, frente a una sola llamada al LLM o un pipeline RAG.

*Prerrequisito: Sprint 10 (`responder()`, Streamlit básico).*

### Contenido de teoría

| # | Documento | Qué aprenderás |
|---|-----------|----------------|
| 0 | [Introducción](./01_Teoria/01_Fundamentos_de_los_agentes/00_introduccion_Agentes_IA.md) | Agente vs RAG; LLM/chatbot/asistente; objetivos. |
| 1 | [Arquitectura y ciclo](./01_Teoria/01_Fundamentos_de_los_agentes/01_arquitectura_y_ciclo_de_ejecucion.md) | Piezas del agente; one-shot vs multi-paso. |

### Workout

Este bloque es **solo teoría** (sin workout propio). La práctica empieza en el Bloque 2.

Índice: [`01_Teoria/01_Fundamentos_de_los_agentes/readme.md`](./01_Teoria/01_Fundamentos_de_los_agentes/readme.md)

---

## 🧠 Bloque 2 — Estado y memoria del agente

📁 [`01_Teoria/02_Estado_y_memoria_del_agente/`](./01_Teoria/02_Estado_y_memoria_del_agente/)

> El estado **dirige** la tarea; el historial del chat solo la **pinta**.

*Prerrequisito: Bloque 1 (conceptos de agente).*

### Contenido de teoría

| # | Documento | Qué aprenderás |
|---|-----------|----------------|
| 0 | [Introducción](./01_Teoria/02_Estado_y_memoria_del_agente/00_introduccion.md) | Por qué hace falta estado. |
| 1 | [Estado de ejecución](./01_Teoria/02_Estado_y_memoria_del_agente/01_estado_de_ejecucion.md) | `AgentState`: campos y actualización. |
| 2 | [Historial UI vs estado vs long-term](./01_Teoria/02_Estado_y_memoria_del_agente/02_historial_vs_estado_vs_long_term.md) | `messages` (S10) ≠ `AgentState`. |
| 3 | [Actualizar estado con estructura](./01_Teoria/02_Estado_y_memoria_del_agente/03_actualizar_estado_con_estructura.md) | JSON del LLM → actualizar estado. |

### Workout

| Recurso | Cubre teoría |
|---------|--------------|
| [01_estado_y_memoria_del_agente.ipynb](./02_Workout/02_Estado_y_memoria_del_agente/01_estado_y_memoria_del_agente.ipynb) | Conversación 4 turnos + AgentState + `done` calculado en Python |

Índice: [`01_Teoria/02_Estado_y_memoria_del_agente/readme.md`](./01_Teoria/02_Estado_y_memoria_del_agente/readme.md)

---

## 🛡️ Bloque 3 — Flujos y control de ejecución

📁 [`01_Teoria/03_Flujos_y_control_de_ejecucion/`](./01_Teoria/03_Flujos_y_control_de_ejecucion/)

> Un agente sin límites es un bucle caro. Aquí añades parada, traza y la UI de S10.

*Prerrequisito: Bloque 2 (`AgentState`).*

### Contenido de teoría

| # | Documento | Qué aprenderás |
|---|-----------|----------------|
| 0 | [Introducción](./01_Teoria/03_Flujos_y_control_de_ejecucion/00_introduccion.md) | De demo a sistema controlable. |
| 1 | [Condiciones de parada](./01_Teoria/03_Flujos_y_control_de_ejecucion/01_condiciones_de_parada.md) | Objetivo, sin progreso, `max_turns`. |
| 2 | [Errores y logging de pasos](./01_Teoria/03_Flujos_y_control_de_ejecucion/02_errores_y_logging_de_pasos.md) | API/parseo; abortar vs reintentar; traza. |
| 3 | [Panorama LangGraph](./01_Teoria/03_Flujos_y_control_de_ejecucion/03_panorama_langgraph.md) | Nodos, estado, edges (mapa mental; práctica en S12). |
| 4 | [De CLI a Streamlit](./01_Teoria/03_Flujos_y_control_de_ejecucion/04_de_cli_a_streamlit.md) | Contrato `procesar_turno`; UI = cliente. |

📁 Proyecto ejecutable: [`05_proyecto_agentes_tarde_cultural_streamlit/`](./01_Teoria/03_Flujos_y_control_de_ejecucion/05_proyecto_agentes_tarde_cultural_streamlit/)

### Workout

| Recurso | Cubre teoría |
|---------|--------------|
| [05_proyecto_agentes_tarde_cultural_streamlit/](./01_Teoria/03_Flujos_y_control_de_ejecucion/05_proyecto_agentes_tarde_cultural_streamlit/) | 1 + 2 + 4 (proyecto en teoría) |
| Guion vídeo | [guiones_video/…](./02_Workout/03_Flujos_y_control_de_ejecucion/guiones_video/01_proyecto_agentes_tarde_cultural_streamlit.md) |
| [02_proyecto_agentes_tarde_cultural_streamlit.md](./02_Workout/03_Flujos_y_control_de_ejecucion/02_proyecto_agentes_tarde_cultural_streamlit.md) | Enlace al repo externo (opcional) |

Índice: [`01_Teoria/03_Flujos_y_control_de_ejecucion/readme.md`](./01_Teoria/03_Flujos_y_control_de_ejecucion/readme.md)

---

## 🎯 Practica live review

📁 [`Practica_live_review/`](./Practica_live_review/) — [`01_agente_calidad_aire/`](./Practica_live_review/01_agente_calidad_aire/) (+ [`_SOLUTION`](./Practica_live_review/01_agente_calidad_aire_SOLUTION/))

**Mismo patrón** que el proyecto de tarde cultural (`procesar_turno`, `calcular_done`, `max_turns`, Streamlit cliente). **Otro dominio:** calidad del aire (preferencias `zona` / `contaminante` / `tipo_consulta`; sin RAG). El alumno completa **`procesar_turno`** y **`run_demo`** en `src/agent.py`.

---

## ⚙️ Convenciones del sprint

- Teoría en `01_Teoria/` (markdown + proyecto ejemplo).
- Workouts en `02_Workout/` — notebooks / apps autocontenidos; guiones en `guiones_video/`. El proyecto Streamlit del Bloque 3 vive en `01_Teoria/.../05_proyecto_…`.
- **Gemini** para el razonamiento del agente (misma API key que S10).
- **Streamlit** solo al final (Bloque 3), reutilizando el patrón del miniproyecto de S10.
- Dominio workouts / proyecto B3: **agenda cultural**. Live Review: **calidad del aire** (sin RAG) — mismos contratos, otros campos de estado.
- En S11 el tope se llama **`max_turns`** (no `max_steps`).
- **No** function calling ni proyecto LangGraph en este sprint (**no** Bedrock). LangGraph en código empieza con notebooks en S12.

**Consejo:** al terminar S11 deberías poder explicar en voz alta la diferencia entre `responder()` (S10) y `procesar_turno()` (S11), mostrar un `AgentState` que evoluciona turno a turno y exponerlo en Streamlit.
