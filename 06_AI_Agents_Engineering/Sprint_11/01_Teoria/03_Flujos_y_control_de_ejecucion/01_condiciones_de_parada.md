![Cabecera](../../assets/cabecera_agentes.png)

# Condiciones de parada

Cada turno cuesta tokens y tiempo. El agente debe **dejar de aceptar mensajes** por una razón explícita.

---

## Motivos habituales en S11

| Condición | Quién la decide | Ejemplo |
|-----------|-----------------|---------|
| Objetivo cumplido | **Solo código** | `calcular_done`: intereses + presupuesto + zona y `len(plan) >= 2` |
| `max_turns` | **Solo código** | Tope de mensajes de usuario → LLM; parar aunque `done` sea False |
| Error irrecuperable | Código | JSON inválido; API key ausente |
| Sin progreso | Código (opcional) | Estado idéntico dos turnos seguidos |

El LLM **no** devuelve `done` en el JSON: lo calcula Python con `calcular_done`.

---

## `max_turns` es obligatorio

En una conversación, el bucle lo controla quien llama a `procesar_turno` (CLI, `run_demo` o Streamlit):

```python
def procesar_turno(estado: dict, mensaje: str) -> dict:
    # ... LLM → actualizar_estado → calcular_done → traza
    return estado


def run_demo(mensajes: list[str], max_turns: int = 8) -> dict:
    estado = crear_estado(mensajes[0] if mensajes else "")
    for mensaje in mensajes[:max_turns]:
        if estado.get("done") or estado.get("error"):
            break
        estado = procesar_turno(estado, mensaje)
    if not estado.get("done") and not estado.get("error"):
        estado["respuesta"] = (
            estado.get("respuesta")
            or "He parado por max_turns; esto es lo que llevo del plan."
        )
    return estado
```

Nunca confíes solo en que el modelo “cierre” la conversación con palabras.

**Éxito temprano ≠ tope:** un guion (`DEMO_MENSAJES`) puede tener 5 mensajes y el bucle parar en el 4 si `done=true`. Eso es el guardrail de objetivo cumplido, no un `max_turns` oculto. Contrasta con cortar por `max_turns` (tope sin `done`). Lo veréis en el proyecto y en la Live Review.

---

## Eco de Sprint 10

En S10 controlabas alucinaciones con prompt restrictivo y abstención.  
Aquí controlas **cuántos turnos** puede durar la tarea. Misma idea: el sistema tiene límites, no solo “buena voluntad” del LLM.

---

## Para llevarte

**Parar es una feature**, no un fallo. Un agente que se detiene con un plan parcial y un mensaje claro es mejor que uno que gasta 30 llamadas.
