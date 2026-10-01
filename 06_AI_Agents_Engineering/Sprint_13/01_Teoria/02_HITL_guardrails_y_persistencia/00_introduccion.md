![Cabecera](../../../Sprint_11/assets/cabecera_thebridge.png)

# Introducción — HITL, guardrails y persistencia

En el bloque 1 el grafo ReAct **corre de punta a punta** en un `invoke`.  
Aquí añadís dos piezas de producto:

1. **Persistencia** — el grafo recuerda entre turnos (`MemorySaver` + `thread_id`).
2. **HITL** — el humano **aprueba** (o rechaza) antes de un paso sensible (p. ej. “cerrar plan”).

Los **guardrails** (allowlist, `max_steps`, `done` en Python) siguen siendo vuestros: el grafo no los sustituye; los **encaja** en nodos y routers.

## Objetivos

- Compilar con checkpointer y usar `thread_id`.
- Ver que dos hilos no se mezclan.
- Pausar el grafo antes de un nodo y reanudar tras una decisión humana.
- Relacionar esto con Streamlit (cliente) + `procesar_turno`.

## Workouts

| Notebook | Qué practicar |
|----------|----------------|
| [01_memoria_y_checkpoints](../../02_Workout/02_HITL_guardrails_y_persistencia/01_memoria_y_checkpoints.ipynb) | MemorySaver, thread_id |
| [02_hitl_aprobar_plan](../../02_Workout/02_HITL_guardrails_y_persistencia/02_hitl_aprobar_plan.ipynb) | interrupt_before + reanudar |
