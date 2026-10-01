![Cabecera](../../../Sprint_11/assets/cabecera_thebridge.png)

# De while a grafo

En S12 (proyecto / Live Review) el loop se parece a esto:

```text
[START]
   │
   ▼
[llamar LLM]
   │
   ├── ¿function_call? ──► [ejecutar tool] ──► (vuelve al LLM)
   │
   └── texto listo ──► [actualizar estado / done] ──► [END]
```

En LangGraph es el **mismo dibujo**, con nombres de nodos:

```text
[START] → [agent] ──┬── tool_calls? sí ──► [tools] ──► [agent]
                    │
                    └── no ──► [END]
```

| En el `while` (S12) | En el grafo (S13) |
|---------------------|-------------------|
| `generate_content` / LLM | Nodo `agent` |
| `ejecutar_tool(...)` | Nodo `tools` (o `ToolNode`) |
| `if function_calls` | `add_conditional_edges` + router |
| `for step in range(max_steps)` | Bucle del grafo (+ tope en estado o config) |
| historial de mensajes | State con lista de mensajes |

## Idea clave

No cambiáis **qué** hace el agente (pedir tools, ejecutarlas, responder).  
Cambiáis **quién encadena** los pasos: de un script a un `StateGraph` compilado.

Repaso S12: [`03_panorama_langgraph.md`](../../../Sprint_12/01_Teoria/03_Control_y_seguridad_de_tools/03_panorama_langgraph.md)
