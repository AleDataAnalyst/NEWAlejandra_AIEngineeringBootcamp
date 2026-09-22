![Cabecera](../../../Sprint_11/assets/cabecera_thebridge.png)

# LangGraph — continuación (después de tools)

En Sprint 11 ya viste el **panorama** del ecosistema LangGraph (qué es, State / Node / Edge, qué aporta, glosario y enlaces).

🔗 Repaso: [`Sprint_11/.../03_panorama_langgraph.md`](../../../Sprint_11/01_Teoria/03_Flujos_y_control_de_ejecucion/03_panorama_langgraph.md)

Aquí no repetimos ese mapa. Solo enlazamos lo que **acabas de codear** (loop de tools a mano) con el grafo, y apuntamos a la práctica.

---

## Tu loop de tools = este grafo

Con function calling y `max_steps` ya tienes algo así:

```text
[START]
   │
   ▼
[llamar LLM]
   │
   ├── function_call ──► [ejecutar tool] ──► (vuelve al LLM)
   │
   └── texto / plan listo ──► [actualizar estado / done] ──► [END]
```

En LangGraph eso serían nodos (`agent`, `tools`) y un **edge condicional** (“¿hay tool calls?”).  
Misma idea: **decisión (LLM) ≠ ejecución (Python)**; el grafo solo **orquesta**.

---

## Qué haces ahora en este sprint

| Sí | No (aún) |
|----|----------|
| Entender el diagrama de arriba | Sustituir el proyecto Streamlit por LangGraph |
| Practicar la API básica en **dos notebooks** (State, edges, condicionales) | HITL, multi-agente, multimodal |
| Ver que tu `while` + tools **es** ese grafo dibujado | Montar el agente cultural completo en grafo |

Los notebooks van **después** del proyecto con tools + control + Streamlit. Son **obligatorios** de leer y ejecutar. No sustituyen ese proyecto: el hito con tools sigue siendo el agente en Python. La práctica evaluable “en serio” con LangGraph llega en **Sprint 13**.

📁 Workout: [`02_Workout/04_LangGraph_basico/`](../../../02_Workout/04_LangGraph_basico/)

---

## Puente a Sprint 13

En S13 migraréis el agente (mismas tools, mismo dominio) a LangGraph como orquestador, con HITL y el cierre del módulo.

---

## Para llevarnos

Si mañana te piden “pásalo a LangGraph”, tu `procesar_turno` + loop de tools ya definen los nodos: solo cambia el orquestador, no la idea.
