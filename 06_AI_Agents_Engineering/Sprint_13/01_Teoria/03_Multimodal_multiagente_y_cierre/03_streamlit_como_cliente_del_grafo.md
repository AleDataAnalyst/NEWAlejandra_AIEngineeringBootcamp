![Cabecera](../../../Sprint_11/assets/cabecera_thebridge.png)

# Streamlit como cliente del grafo

Streamlit **no** es el agente. Es un cliente:

```text
UI (messages)  ──►  procesar_turno(agent_state, mensaje)
                    │
                    ▼
              grafo LangGraph + JSON + done/HITL
                    │
                    ▼
              agent_state actualizado ──► pinta chat + sidebar
```

## Dos memorias (igual que S11/S12)

| session_state | Qué es |
|---------------|--------|
| `messages` | Solo UI del chat |
| `agent_state` | Preferencias, plan, done, HITL, traza |

## HITL en la UI

Si `pendiente_hitl`:

1. Bloquear el chat input (o avisar).
2. Mostrar plan + botones Aprobar / Rechazar.
3. Llamar a `aprobar_plan(estado, True/False)` sin nuevo mensaje de usuario.

## Contrato estable

Mientras `procesar_turno(estado, mensaje, max_steps) -> estado` exista, podéis cambiar el grafo por dentro sin reescribir toda la UI.
