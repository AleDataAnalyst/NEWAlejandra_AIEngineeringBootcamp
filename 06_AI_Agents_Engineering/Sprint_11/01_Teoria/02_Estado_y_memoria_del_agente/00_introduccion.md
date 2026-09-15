![Cabecera](../../assets/cabecera_agentes.png)

# Introducción: estado y memoria del agente

Sin un estado explícito, cada mensaje del usuario sería una llamada suelta al LLM. Aquí formalizas **qué se guarda entre turnos** y lo distingues del historial del chat.

> **Estado de ejecución** = datos estructurados que dicen *qué sabemos ya de la tarea*.

---

## Objetivos del bloque

Al terminar, deberías poder:

- Definir un `AgentState` (dict) con campos claros.
- Explicar la diferencia entre historial de chat, estado de ejecución y long-term.
- Actualizar el estado tras cada mensaje del usuario (JSON → Python).
- Usar el estado para decidir: preguntar más o cerrar con un plan (`done`).

---

## De conversación a estado

| Sin estado tipado | Con `AgentState` |
|-------------------|------------------|
| Solo texto libre / historial | `preferencias`, `plan`, `respuesta`, `done` |
| Difícil saber qué falta | Python comprueba si hay intereses, presupuesto, zona |
| “Creo que hemos terminado” en prosa | `done=True` **calculado** en código |

---

## Salida concreta

Workout con una conversación de **4 turnos** (pedido vago → aclaraciones → plan) donde cada paso imprime el estado actualizado.
