![Cabecera](../../../Sprint_11/assets/cabecera_thebridge.png)

# Multiagente — overview básico

## Idea

Un **supervisor** decide a qué **especialista** pasar el turno según el **estado compartido**.  
Cada especialista es un nodo (prompt distinto) que **lee y escribe** en ese estado. El flujo **vuelve** al supervisor hasta `FINISH` (con tope de iteraciones en Python).

```text
START → supervisor ──┬── especialista A ──┐
                     ├── especialista B ──┼──► supervisor → … → FINISH → END
                     └── sintetizar ──────┘
```

## Piezas que debes reconocer

| Pieza | Para qué |
|-------|----------|
| Estado compartido | Canal entre agentes |
| Supervisor | Orquesta; no hace el trabajo del especialista |
| `add_conditional_edges` | Router tras el supervisor |
| Bucle | Especialista → supervisor otra vez |
| `FINISH` + `MAX_ITER` | Parada explícita |
| `MemorySaver` + `thread_id` | Checkpoints por hilo (misma idea que HITL) |

## Cuándo tiene sentido

- Dominios distintos (p. ej. “ideas culturales” vs “logística” vs “cierre”).
- Equipos que quieren aislar prompts (y, más adelante, tools) por rol.

## Cuándo no

- Un solo flujo claro (agente cultural ReAct + HITL del sprint) → **un** grafo basta.
- Multiagente no arregla mal estado, mala allowlist ni falta de límites.

## En este sprint

Workout: overview junior con bucle supervisor ↔ especialistas (sin tools complejas).  
El **proyecto cultural** del sprint **no** es multiagente: es ReAct + HITL.

📁 Workout: [`01_multiagente_supervisor.ipynb`](../../02_Workout/03_Multimodal_multiagente_y_cierre/01_multiagente_supervisor.ipynb)
