![Cabecera](../../../Sprint_11/assets/cabecera_thebridge.png)

# De CLI a Streamlit

Igual que en S11: **un backend**, dos clientes.

```text
procesar_turno(estado, mensaje)  ← contrato
        ▲
   ┌────┴────┐
 main.py    app.py
  (CLI)    (Streamlit)
```

---

## Dos memorias en la UI

| Memoria | Dónde | Para qué |
|---------|-------|----------|
| `st.session_state.messages` | Chat | Lo que ve el usuario |
| `st.session_state.agent_state` | Dict | preferencias, plan, done, **traza de tools** |

No confundas el historial del chat con la traza interna de tools.

---

## Flujo en un mensaje

1. Usuario escribe en el chat.
2. `procesar_turno` puede hacer **varios** tool calls (`max_steps`).
3. La UI muestra la `respuesta` (y el plan si `done`).
4. El expander de debug enseña `traza` (tools usadas).

---

## Checklist de paridad CLI ↔ web

- Misma API key / mismo modelo.
- Mismos límites (`max_steps`, `max_turns` si aplica).
- Mismos campos de estado.
- Errores visibles (no stack trace crudo al alumno en Streamlit).

El proyecto en teoría ([`05_proyecto_agente_tools_tarde_cultural/`](./05_proyecto_agente_tools_tarde_cultural/)) implementa exactamente este patrón. La Live Review ([`Practica_live_review/`](../../Practica_live_review/)) reutiliza el mismo contrato con dominio calidad del aire.
