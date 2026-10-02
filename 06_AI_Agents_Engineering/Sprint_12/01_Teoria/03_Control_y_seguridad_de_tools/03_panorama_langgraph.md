![Cabecera](../../../Sprint_11/assets/cabecera_thebridge.png)

# LangGraph en Sprint 12 — panorama práctico

En Sprint 11 viste el **mapa mental** del ecosistema (qué es LangGraph, State / Node / Edge, por qué existe).

🔗 Repaso amplio: [`Sprint_11/.../03_panorama_langgraph.md`](../../../Sprint_11/01_Teoria/03_Flujos_y_control_de_ejecucion/03_panorama_langgraph.md)

Este documento es el **resumen de lo que vais a probar y ejecutar ahora** en dos notebooks correspondientes a los workouts.

📁 Workout: [`02_Workout/04_LangGraph_basico/`](../../02_Workout/04_LangGraph_basico/)

> LangGraph **orquesta** el flujo. No sustituye diseñar buen estado, buenas tools ni buenas paradas (`done`, `max_steps`).

---

## Resumen del grafo LangGraph

Montáis un **grafo**: estado compartido + nodos (funciones) + flechas (edges).  
Compiláis (`compile`) y ejecutáis (`invoke`). Primero un tubo lineal; luego un **router** con ramas.

---

## De tu agente con tools al grafo

Con function calling y `max_steps` ya tienes programado algo así:

```text
[START]
   │
   ▼
[llamar LLM]
   │
   ├── ¿function_call? ──► [ejecutar tool] ──► (vuelve al LLM)
   │
   └── texto / plan listo ──► [actualizar estado / done] ──► [END]
```

En LangGraph eso serían nodos (`agent`, `tools`, …) y un **edge condicional** (“¿hay tool calls?”).  
Misma idea: **decisión (LLM) ≠ ejecución (Python)**; el grafo solo **encadena** pasos.

La migración completa con agentes LangGraph llega en **Sprint 13**, donde migraréis el agente del sprint a LangGraph como orquestador, con HITL y el cierre del módulo.

---

## Partes que vamos a estudiar sobre LangGraph

| Pieza | Qué es | En código (idea) |
|-------|--------|------------------|
| **State** | Dict tipado que atraviesa el grafo | `TypedDict` (`pedido`, `respuesta`, …) |
| **Node** | Un paso = una función `estado → cambios` | `add_node("nombre", fn)` |
| **Edge fija** | Siempre A → B | `add_edge("A", "B")` |
| **Edge condicional** | A → ? según una función | `add_conditional_edges(...)` |
| **START / END** | Entrada y salida del grafo | `from langgraph.graph import START, END` |
| **compile** | Congela el grafo en una app ejecutable | `app = grafo.compile()` |
| **invoke** | Corre el grafo con un estado inicial | `app.invoke({...})` |

Detalle útil en los notebooks: `texto_del_llm(...)` — Gemini a veces devuelve `.content` como `str` y a veces como `list`; unificamos a texto.

---

## Notebook 1 — Grafo lineal

**Archivo:** [`01_primer_grafo_langgraph.ipynb`](../../02_Workout/04_LangGraph_basico/01_primer_grafo_langgraph.ipynb)

**Idea:** dos nodos en secuencia (sin ramas).

```text
[START] → [normalizar pedido] → [proponer tarde] → [END]
```

**Qué practicáis**

1. Definir el **State** (`TypedDict`).
2. Escribir nodos que leen el estado y devuelven un **patch** (campos a actualizar).
3. `add_node` + `add_edge` fijas.
4. `compile` + `invoke` con un pedido de ejemplo.
5. Ver el estado **final** (y, si el notebook lo muestra, el recorrido).

**Analogía:** un pipeline. Siempre el mismo camino.

---

## Notebook 2 — Edges condicionales (router)

**Archivo:** [`02_condicionales_langgraph.ipynb`](../../02_Workout/04_LangGraph_basico/02_condicionales_langgraph.ipynb)

**Idea:** un nodo **clasifica** la intención; el grafo elige la rama.

```text
                         ┌→ [preferencias] → [END]
                         ├→ [eventos]      → [END]
[START] → [clasificar] ──┤
                         ├→ [horario]      → [END]
                         └→ [general]      → [END]
```

**Qué practicáis**

1. Nodo `clasificar` que escribe p. ej. `estado["intencion"]`.
2. Función **`router(estado) → etiqueta`** (elige la siguiente rama).
3. `add_conditional_edges` (con `path_map` o forma corta si la etiqueta = nombre del nodo).
4. Cada rama termina en `END`.
5. Probar varios pedidos y ver qué camino toma el grafo.

**Analogía:** un `if / elif` dibujado: la decisión es código (o un LLM que rellena un campo); el grafo solo enruta.

---

## Cómo se monta (orden mental)

En ambos notebooks el orden es el mismo:

```text
1. State (TypedDict)
2. Nodos (funciones)
3. StateGraph(State)
4. add_node(...)
5. add_edge / add_conditional_edges
6. compile()
7. invoke(estado_inicial)
```

```text
        ┌─────────────┐
        │   State     │  ← dict compartido
        └──────┬──────┘
               │
        ┌──────▼──────┐
        │  Nodos      │  ← funciones
        └──────┬──────┘
               │
        ┌──────▼──────┐
        │  Edges      │  ← fijas o condicionales
        └──────┬──────┘
               │
        ┌──────▼──────┐
        │  compile    │
        └──────┬──────┘
               │
        ┌──────▼──────┐
        │  invoke     │  → estado final
        └─────────────┘
```

---

## Qué sí / qué no en este sprint

| Sí (S12) | No (aún) |
|----------|----------|
| StateGraph, nodos, edges fijas | Sustituir el proyecto Streamlit / Live Review por LangGraph |
| Edges condicionales + `router` | HITL, multi-agente, multimodal |
| `compile` + `invoke` | Checkpointing / persistencia avanzada |
| Ver que tu `while` + tools **es** ese grafo dibujado | Montar el agente cultural/aire completo en grafo |

Los notebooks van **después** del proyecto con tools (+ Live Review si la hacéis). Son **obligatorios** de leer y ejecutar. No sustituyen ese trabajo.

---

## Puente a Sprint 13

En S13 migraréis el agente del sprint (mismas ideas de tools y control; el dominio concreto lo fijaréis en ese material) a LangGraph como orquestador, con HITL y el cierre del módulo.

Si mañana te piden “pásalo a LangGraph”, tu `procesar_turno` + loop de tools ya definen los nodos: solo cambia el orquestador, no la idea.

---

## Para llevarnos

1. **Grafo** = State + nodos + edges + `compile` / `invoke`.
2. **Lineal** (NB1) → siempre el mismo camino.
3. **Condicional** (NB2) → `router` elige la rama.
4. LangGraph **no** inventa tu agente: lo hace **explícito** y dibujable.
