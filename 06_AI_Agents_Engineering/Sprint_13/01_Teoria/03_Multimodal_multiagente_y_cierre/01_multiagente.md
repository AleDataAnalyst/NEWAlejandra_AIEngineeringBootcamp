![Cabecera](../../../Sprint_11/assets/cabecera_thebridge.png)

# Multiagente: supervisor y especialistas

Un solo nodo con un solo prompt acaba mezclando oficios (proponer ideas, mirar datos, cerrar un plan). Un grafo **multiagente** parte el trabajo en roles. Un **supervisor** elige el siguiente. Cada **especialista** lee y escribe un estado compartido. El flujo vuelve al supervisor hasta una salida explícita.

```text
START → supervisor ──┬── especialista A ──┐
                     ├── especialista B ──┼──► supervisor → … → FINISH → END
                     └── sintetizar ──────┘
```

No son procesos en paralelo ni equipos desplegados. Son nodos del mismo grafo, con prompts distintos, unidos por el State.

Aquí puedes ver distintas configuraciones de multiagente:

![Multiagente](../../assets/multiagente.avif)

[Más info detallada sobre multiagentes en LangChain](https://langchain-opentutorial.gitbook.io/langchain-opentutorial/17-langgraph/02-structures/08-langgraph-multi-agent-structures-01)    

---

## Piezas

| Pieza | Rol |
|-------|-----|
| **Estado compartido** | Canal. Pedido, notas de cada rol, plan, quién sigue, iteración, log. |
| **Supervisor** | Mira el estado y escribe el siguiente rol. No redacta el trabajo del especialista. |
| **Especialista** | Un nodo, un oficio. Lee lo que necesita y escribe su campo. |
| **Router** | Traduce `siguiente` a un nombre de nodo (`add_conditional_edges`). |
| **Vuelta** | Cada especialista tiene un edge fijo de regreso al supervisor. Eso es el bucle. |
| **`FINISH` + tope** | Salida explícita. El tope de iteraciones lo aplica Python si el modelo no cierra. |

```python
import operator

class Estado(TypedDict):
    pedido: str
    notas_a: str
    notas_b: str
    plan: str
    siguiente: str       # "a" | "b" | "sintetizar" | "FINISH"
    iteracion: int
    log: Annotated[list, operator.add]
```

El log lleva un reducer de acumulación. `siguiente` e `iteracion` se sustituyen.

---

## Supervisor y router

```python
MAX_ITER = 8

def nodo_supervisor(estado: Estado) -> dict:
    it = int(estado.get("iteracion") or 0) + 1
    if it >= MAX_ITER:
        return {"iteracion": it, "siguiente": "FINISH"}
    siguiente = pedir_al_modelo(estado)  # un rol, o FINISH
    if siguiente not in {"a", "b", "sintetizar", "FINISH"}:
        siguiente = regla_de_respaldo(estado)  # Python, si la salida no es válida
    return {"iteracion": it, "siguiente": siguiente, "log": [f"{it}: {siguiente}"]}

def router(estado: Estado) -> str:
    if estado["siguiente"] == "FINISH":
        return "__end__"
    return estado["siguiente"]
```

```python
grafo.add_edge(START, "supervisor")
grafo.add_conditional_edges("supervisor", router)
grafo.add_edge("a", "supervisor")
grafo.add_edge("b", "supervisor")
grafo.add_edge("sintetizar", "supervisor")
```

Si el modelo contesta algo que no es un nodo, una regla en Python elige (por ejemplo: a quién todavía le faltan notas). El grafo no debe quedarse sin destino.

---

## Dónde encajan las tools

El especialista puede ser un nodo “simple” (solo texto) o llevar **dentro** el ciclo de tools: el modelo pide, Python ejecuta, con un máximo de vueltas. Ese ciclo no tiene por qué ser otro par de nodos `agent` / `tools` en el grafo de roles. El grafo de fuera sigue enrutando oficios.

El cierre sensible (publicar, dar el plan por bueno) puede ser un nodo posterior, con una pausa declarada al compilar, justo antes de ese nodo.

---

## Cuándo usarlo

Tiene sentido cuando los oficios se separan de verdad: uno mira fuentes, otro encaja restricciones, otro redacta el cierre. Cada uno con su prompt.

Un solo ciclo agent ↔ tools basta cuando no hay roles distintos. Partir en especialistas no arregla un estado pobre ni una allowlist floja.

---

## Errores típicos

- Supervisor que también escribe el plan: deja de ser un enrutador y el estado se pisa.
- Especialista que no vuelve al supervisor: el bucle no existe y nadie decide `FINISH`.
- Sin tope de iteraciones: el modelo puede alternar roles sin cerrar.
- Estado sin campos por rol: todos escriben en el mismo texto y no se sabe quién aportó qué.

---

## Leer más

| Tema | Doc |
|------|-----|
| Bucles y edges condicionales | https://docs.langchain.com/oss/python/langgraph/use-graph-api |
| Subgrafos (otro modo de partir el trabajo) | https://docs.langchain.com/oss/python/langgraph/use-subgraphs |
| Agentes y workflows | https://docs.langchain.com/oss/python/langgraph/workflows-agents |

La documentación también muestra especialistas envueltos como **tools** de un agente principal (el enrutador llama a una tool y esa tool invoca al otro agente). Es el mismo reparto de oficios, dibujado como tool calling. Este texto usa nodos y un router porque el flujo se ve en el grafo.

El paquete `langgraph-supervisor` ya no se mantiene. El patrón de aquí es un `StateGraph` escrito a mano.

---

## Objetivos

- [ ] Dibujo supervisor, especialistas y la vuelta.
- [ ] Explico qué escribe el supervisor y qué escribe un especialista.
- [ ] Sé por qué hacen falta `FINISH` y un tope en Python.
- [ ] Distingo este grafo de un ciclo agent ↔ tools.

## Para llevarnos

1. Un estado compartido, varios prompts, un nodo que elige el siguiente.
2. El bucle es “especialista → supervisor”, no un `while` escondido.
3. Python guarda la salida (`FINISH` o el máximo de iteraciones).
