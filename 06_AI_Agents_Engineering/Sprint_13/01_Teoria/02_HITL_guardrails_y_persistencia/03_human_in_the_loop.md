![Cabecera](../../../Sprint_11/assets/cabecera_thebridge.png)

# Human-in-the-loop (HITL)

## Idea

Antes de un paso **sensible** (cerrar plan, “reservar”, publicar), el grafo **se para**.  
Un humano aprueba o rechaza; luego el grafo **reanuda** con el mismo `thread_id`.

```text
[proponer_plan] → (PAUSA) → [aplicar_si_aprobado] → [END]
```

## Mecanismo sencillo (notebook)

```python
app = grafo.compile(
    checkpointer=MemorySaver(),
    interrupt_before=["aplicar"],  # no ejecuta ese nodo hasta que reanudéis
)
```

1. `invoke` con el pedido → corre hasta **antes** de `aplicar` y se detiene.
2. Revisáis `app.get_state(config)` (plan propuesto).
3. Actualizáis el State (`aprobado=True/False`) y volvéis a `invoke(None, config)` (o el API de resume de vuestra versión).

> HITL **exige** checkpointer: sin él no hay dónde “guardar la pausa”.

## En el producto (Streamlit)

- El cliente detecta “pendiente de aprobación” (flag en State o mensaje).
- Muestra botones Aprobar / Rechazar.
- El siguiente `procesar_turno` reanuda el hilo con la decisión.

## Qué no es HITL

Pedir al LLM “¿debo continuar?” **no** es HITL serio: la decisión humana va por **UI / API**, no por otra llamada al modelo.
