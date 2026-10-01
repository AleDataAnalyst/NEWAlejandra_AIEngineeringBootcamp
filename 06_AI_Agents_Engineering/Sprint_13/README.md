![Cabecera](../Sprint_11/assets/cabecera_thebridge.png)

# 📘 Sprint 13 — Autonomous Agent Systems

En el Sprint 11 el agente mantuvo **estado** y `done`. En el Sprint 12 usó **tools** con control y practicasteis la **API básica** de LangGraph (grafo lineal + condicionales).

Aquí el salto: el bucle de tools pasa a un grafo ReAct (bloque 1), añadís **persistencia / HITL** (bloque 2) y cerráis con un **supervisor** (proyecto cultural y Live Review de aire) más una intro **multimodal**.

> **¿Cómo orquesto el agente con LangGraph, con autonomía controlada (HITL + límites), sin perder lo aprendido en S11–S12?**

---

## Mapa del módulo (Sprints 11–13)

| Sprint | Pregunta | Fase |
|--------|----------|------|
| **11** | ¿Qué es un agente y cómo mantiene estado? | Fundamentos |
| **12** | ¿Cómo actúa con herramientas (+ RAG)? | Tool use + LangGraph básico |
| **13** (este) | ¿Cómo orquesto con autonomía controlada? | ReAct + HITL + supervisor |

```text
S11  mensaje → procesar_turno → estado + done + max_turns
 ↓
S12  + tools (allowlist, max_steps) + notebooks LangGraph (lineal / router)
 ↓
S13  while de tools → grafo ReAct (notebook)
     + checkpoints + HITL
     + supervisor (proyecto cultural y Live Review aire)
     + intro multimodal
     → Project Break 2
```

**Prerrequisito:** haber hecho S12 (proyecto tools y/o Live Review + notebooks `04_LangGraph_basico`).  
**No repetimos** en este sprint los notebooks 01/02 de LangGraph básico (ya están en S12).

---

## Stack y dominio

- **Stack:** Python + Gemini + LangGraph · Streamlit
- **Proyecto:** tarde cultural multiagente (supervisor + tools + HITL)
- **Live Review:** calidad del aire (mismo grafo, otro dominio)

---

## 🧭 Bloque 1 — Orquestación LangGraph con tools

| Doc | Contenido |
|-----|-----------|
| [ReAct con tools](./01_Teoria/01_Orquestacion_LangGraph_con_tools/01_react_con_tools.md) | Ciclo agent ↔ tools, reducer, tope |
| [Migración desde S12](./01_Teoria/01_Orquestacion_LangGraph_con_tools/02_migracion_desde_s12.md) | Del `while` al grafo ReAct o al supervisor |

| Workout | Descripción |
|---------|-------------|
| [01_agente_tools_en_langgraph.ipynb](./02_Workout/01_Orquestacion_LangGraph_con_tools/01_agente_tools_en_langgraph.ipynb) | ReAct en LangGraph |

---

## 🛡️ Bloque 2 — HITL, guardrails y persistencia

| Doc | Contenido |
|-----|-----------|
| [Persistencia y HITL](./01_Teoria/02_HITL_guardrails_y_persistencia/01_persistencia_y_hitl.md) | Checkpoints, `thread_id`, pausa humana, límites |

| Workout | Descripción |
|---------|-------------|
| [01_memoria_y_checkpoints.ipynb](./02_Workout/02_HITL_guardrails_y_persistencia/01_memoria_y_checkpoints.ipynb) | MemorySaver + thread_id |
| [02_hitl_aprobar_plan.ipynb](./02_Workout/02_HITL_guardrails_y_persistencia/02_hitl_aprobar_plan.ipynb) | HITL aprobar plan |

---

## 🧩 Bloque 3 — Multi-agente / multimodal (intro) + proyecto

| Doc | Contenido |
|-----|-----------|
| [Multiagente](./01_Teoria/03_Multimodal_multiagente_y_cierre/01_multiagente.md) | Supervisor, especialistas, `FINISH` |
| [Multimodal](./01_Teoria/03_Multimodal_multiagente_y_cierre/02_multimodal.md) | Imagen + texto dentro de un nodo |

📁 Proyecto: [`04_proyecto_agente_langgraph_tarde_cultural/`](./01_Teoria/03_Multimodal_multiagente_y_cierre/04_proyecto_agente_langgraph_tarde_cultural/)

| Workout | Descripción |
|---------|-------------|
| [01_multiagente_supervisor.ipynb](./02_Workout/03_Multimodal_multiagente_y_cierre/01_multiagente_supervisor.ipynb) | Overview multiagente (bucle + MemorySaver) |
| [02_multimodal_imagen_texto.ipynb](./02_Workout/03_Multimodal_multiagente_y_cierre/02_multimodal_imagen_texto.ipynb) | LangGraph + imagen → texto |
| [03_proyecto_agente_langgraph_tarde_cultural.md](./02_Workout/03_Multimodal_multiagente_y_cierre/03_proyecto_agente_langgraph_tarde_cultural.md) | Stub → repo del proyecto multiagente |

---

## 🎯 Practica live review

📁 [`Practica_live_review/`](./Practica_live_review/) — multiagente LangGraph · **calidad del aire** (alumno + SOLUTION).

Mismo patrón que el proyecto cultural (supervisor + HITL + MemorySaver); otro dominio. TODOs: `_fallback_siguiente`, `build_graph`, `procesar_turno`.

---

## Escalera pedagógica

```text
Notebook: tools en LangGraph (ReAct)
    ↓
Notebook: memoria / checkpoints
    ↓
Notebook: HITL (aprobar plan)
    ↓
Notebook: multiagente + multimodal
    ↓
Proyecto cultural multiagente (LangChain + HITL + RAG)
    ↓
Live Review calidad del aire (mismo patrón, 3 TODOs)
    ↓
Project Break 2
```

---

## Fuera de alcance

ciberseguridad avanzada · multi-agente de producción · repetir grafos lineales/condicionales básicos de S12.
