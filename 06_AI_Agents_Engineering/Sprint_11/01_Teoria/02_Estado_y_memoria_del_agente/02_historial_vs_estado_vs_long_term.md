![Cabecera](../../assets/cabecera_thebridge.png)

# Historial UI vs estado vs long-term

En Sprint 10 practicaste un chat con:

```python
st.session_state.messages = [{"role": "user"|"assistant", "content": "..."}, ...]
```

Eso **no** es el estado del agente. Son tres ideas distintas:

---

## Tres capas (vocabulario del módulo)

| Capa | Qué es | Dónde vive en S11 | ¿Persiste entre días? |
|------|--------|-------------------|------------------------|
| **A. Historial de chat (UI)** | Mensajes para pintar la conversación | `st.session_state.messages` | No (salvo que lo guardes tú) |
| **B. Estado de ejecución** | Dónde va la **tarea** actual | `AgentState` en el loop | Solo durante `run_agent` (RAM) |
| **C. Long-term memory** | Preferencias / hechos entre sesiones | Extra opcional: JSON en disco | Sí, si lo implementas |

```text
Usuario escribe en Streamlit
        │
        ▼
  messages (A)  ←── solo presentación / hilo
        │
        ▼
  run_agent(pedido)
        │
        ▼
  AgentState (B)  ←── dirige pasos
        │
        ▼  (opcional, preview)
  preferencias.json (C)
```

---

## Errores típicos de juniors

1. **Meter todo el plan solo en `messages`** y creer que el agente “se acuerda”.
2. **Duplicar** el mismo dato en messages y en estado sin una fuente de verdad.
3. **Llamar “memoria”** a cualquier dict — luego long-term y estado se confunden en S12/S13.

---

## Short-term en este sprint

“Short-term” aquí = lo que dura **la corrida** (y, en la UI, la sesión del navegador).  
El historial de chat es short-term de **conversación**; el `AgentState` es short-term de **tarea**.

---

## Preview long-term (extra, no bloque)

Al final del workout (celda opcional) puedes persistir preferencias en un JSON:

```python
# guardar
json.dump(state["preferencias"], open("preferencias.json", "w"), ensure_ascii=False, indent=2)

# cargar en la siguiente sesión
preferencias = json.load(open("preferencias.json"))
```

Eso es long-term **mínimo**. No hace falta vector store de memorias. Lo ampliaremos más adelante; en S11 basta con saber que **existe** la distinción.

---

## Para llevarte

Frase del sprint:

> **`messages` pinta el chat; `AgentState` dirige la tarea.**
