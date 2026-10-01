![Cabecera](../../../Sprint_11/assets/cabecera_thebridge.png)

# Guardrails en el grafo

LangGraph orquesta; **Python sigue decidiendo** los límites.

| Guardrail | Dónde encaja |
|-----------|----------------|
| Allowlist / `validar_args` | Nodo `tools` |
| `max_steps` | Contador en State + router (bloque 1) |
| `calcular_done` | Tras el grafo o nodo final |
| HITL | `interrupt_before` / `interrupt()` en paso sensible |
| Traza `ok` / `error` / `blocked` | Al ejecutar tools |

## Anti-patrones

- Tool `marcar_done` controlada solo por el LLM.
- Confiar en que el modelo “pare solo” sin tope.
- Mezclar aprobación HITL con “el LLM dice que está bien”.

## Relación con S12

Los mismos principios de [`03_Control_y_seguridad_de_tools`](../../../Sprint_12/01_Teoria/03_Control_y_seguridad_de_tools/readme.md): ahora viven **dentro** del grafo, no solo en el `while`.
