![Cabecera](../../../Sprint_11/assets/cabecera_thebridge.png)

# Nodos agent y tools

## Nodo `agent`

- Recibe el State (sobre todo la lista de mensajes).
- Llama al LLM **con tools enlazadas** (`bind_tools` o declaraciones equivalentes).
- Devuelve un mensaje del modelo:
  - con **`tool_calls`** → quiere usar tools, o
  - solo **texto** → respuesta final.

## Nodo `tools`

Dos estilos (el notebook usa el del ecosistema LangChain):

| Estilo | Idea |
|--------|------|
| **`ToolNode(tools)`** | Prebuilt: lee `tool_calls` y ejecuta `@tool` |
| **Nodo propio** | Llama a `ejecutar_tool(nombre, args)` de S12 (allowlist) |

En el **proyecto** del sprint preferimos el segundo (misma allowlist que S12).  
En el **notebook** veréis `ToolNode` para conocer el patrón oficial.

## Router ReAct

```python
def router(estado) -> Literal["tools", "__end__"]:
    ultimo = estado["messages"][-1]
    if getattr(ultimo, "tool_calls", None):
        return "tools"
    return "__end__"
```

- Tras `agent` → condicional a `tools` o `END`
- Tras `tools` → **siempre** vuelve a `agent` (cierra el ciclo)

## Decisión ≠ ejecución

El LLM **elige** qué tool y con qué args.  
Python (**nodo tools** / allowlist) **ejecuta** o bloquea. Igual que en S12.
