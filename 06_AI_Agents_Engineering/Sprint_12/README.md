![Cabecera](../Sprint_11/assets/cabecera_thebridge.png)

# 📘 Sprint 12 — Tool-Using Agents

En el Sprint 11 el agente mantuvo **estado** y decidió `done` sin herramientas. Aquí el modelo **elige y usa tools**: RAG, API de eventos y utilidades. Al final practicáis la API básica de **LangGraph** (sin sustituir el proyecto).

> **¿Cómo dejo que el agente use herramientas (RAG, API, utilidades) y vuelva con un resultado, sin perder el control?**

---

## Mapa del módulo (Sprints 11–13)

| Sprint | Pregunta | Fase |
|--------|----------|------|
| **11** | ¿Qué es un agente y cómo mantiene estado? | Fundamentos |
| **12** (este) | ¿Cómo actúa con herramientas (+ RAG)? | Tool use + LangGraph básico |
| **13** | ¿Cómo planifica con autonomía controlada? | LangGraph (proyecto) + HITL + multimodal / multi-agente intro |

```text
S11  mensaje → estado + done (sin tools)
 ↓
S12  pedido → function calling → tools → plan (+ max_steps)
     + notebooks LangGraph (State, edges, condicionales)
 ↓
S13  migrar agente a LangGraph + HITL + multimodal / multi-agente intro
```

---

## Tools del sprint

| Tool | Rol |
|------|-----|
| `RAG_buscar_en_guia` | RAG sobre guía/FAQ (copia mínima S10) |
| `API_consultar_eventos_madrid` | Open data Madrid + fallback JSON local |
| `hora_actual` | Fecha/hora |

---

## 🧭 Tool Use y Function Calling

📁 [`01_Teoria/01_Tool_use_y_function_calling/`](./01_Teoria/01_Tool_use_y_function_calling/)

> Qué es una tool, cómo se declara y el ciclo agente → tool → resultado → agente.

| Workout | Descripción |
|---------|-------------|
| [01_tool_use_hora_actual.ipynb](./02_Workout/01_Tool_use_y_function_calling/01_tool_use_hora_actual.ipynb) | Notebook: solo `hora_actual` |

---

## 🔧 Integración de herramientas

📁 [`01_Teoria/02_Integracion_de_herramientas/`](./01_Teoria/02_Integracion_de_herramientas/)

> Varias tools en Python; RAG como tool; API + fallback.

| Workout | Descripción |
|---------|-------------|
| [01_multi_tool_con_rag.ipynb](./02_Workout/02_Integracion_de_herramientas/01_multi_tool_con_rag.ipynb) | `tools/` local: hora + RAG + API (+ fallback) |
| Proyecto (continúa) | Ver control y seguridad — mismo patrón |

---

## 🛡️ Control y seguridad de tools

📁 [`01_Teoria/03_Control_y_seguridad_de_tools/`](./01_Teoria/03_Control_y_seguridad_de_tools/)

> Validación, allowlist, errores, `max_steps`. Teoría LangGraph: **continuación** del panorama S11 + puente a los notebooks.

| Workout | Descripción |
|---------|-------------|
| [01_proyecto_agente_tools_tarde_cultural/](./02_Workout/03_Control_y_seguridad_de_tools/01_proyecto_agente_tools_tarde_cultural/) | 3 tools + control + Streamlit (**hito** del sprint / Live Review) |
| [02_proyecto_agente_tools_tarde_cultural.md](./02_Workout/03_Control_y_seguridad_de_tools/02_proyecto_agente_tools_tarde_cultural.md) | Stub repo (opcional) |

---

## 📐 LangGraph básico

📁 Workout: [`02_Workout/04_LangGraph_basico/`](./02_Workout/04_LangGraph_basico/)

📁 Teoría puente: [`03_panorama_langgraph.md`](./01_Teoria/03_Control_y_seguridad_de_tools/03_panorama_langgraph.md)

> **Obligatorio** ejecutar los dos notebooks **después** del proyecto con tools. No sustituyen ese proyecto. No hay Live Review de LangGraph en este sprint (pasa a Sprint 13).

| Notebook | Contenido |
|----------|-----------|
| [01_primer_grafo_langgraph.ipynb](./02_Workout/04_LangGraph_basico/01_primer_grafo_langgraph.ipynb) | State, nodos, edges, compile/invoke (tarde cultural) |
| [02_condicionales_langgraph.ipynb](./02_Workout/04_LangGraph_basico/02_condicionales_langgraph.ipynb) | Conditional edges / router de intención |

Stack de estos notebooks: `langgraph` + `langchain-google-genai` (misma `GEMINI_API_KEY`).

---

## Escalera pedagógica

```text
notebook 1 tool (hora) + FC
    ↓
notebook multi-tool + RAG + API
    ↓
proyecto 3 tools + control + Streamlit   ← hito / Live Review S12
    ↓
notebooks LangGraph (lineal + condicionales)  ← obligatorio consumir
```

## Fuera de alcance

HITL formal · multi-agente · multimodal · LangGraph como orquestador del proyecto Streamlit · seguridad avanzada.

## Estado

Teoría, notebooks de tools, proyecto con control + Streamlit, notebooks LangGraph y live review (tools): **contenidos**.
