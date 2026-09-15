![Cabecera](../../assets/cabecera_agentes.png)

# De CLI a Streamlit

Mismo mensaje que en Sprint 10 (`02_de_script_a_aplicacion.md`): la UI es un **cliente**.

---

## Contrato del agente

```python
def procesar_turno(estado: dict, mensaje: str) -> dict:
    """
    Un mensaje de usuario → LLM → actualizar_estado → calcular_done.
    Returns:
        objetivo, preferencias, plan, respuesta,
        done, error, traza, ...
    """
```

| Cliente | Cómo llama |
|---------|------------|
| CLI demo | `run_demo(max_turns=…)` — guion de varios turnos |
| CLI interactivo | `procesar_turno(estado, input())` en bucle |
| Streamlit `app.py` | Tras cada `chat_input`: **`procesar_turno(agent_state, prompt)`** |

---

## Qué reutilizar del miniproyecto S10

| S10 miniproyecto | S11 agente |
|------------------|------------|
| `st.chat_input` + `messages` | Misma UI: burbujas user/assistant |
| Sidebar (nombre, limpiar) | Sidebar: `max_turns`, «Nueva conversación» |
| `.streamlit/config.toml` | Mismo tema si quieres |
| `responder(pregunta)` por turno | **`procesar_turno(estado, mensaje)`** por turno |

Diferencia clave: además de `messages`, guardas **`agent_state`** en `st.session_state` para que el estado de la tarea persista entre mensajes.

Opcional: expander con preferencias, `plan`, `done` y **traza** (no confundir con el historial de chat).

---

## Anti-patrón

```python
# ❌ Llamada a Gemini copiada dentro de app.py
if prompt := st.chat_input(...):
    client.models.generate_content(...)
```

```python
# ✅
estado = procesar_turno(st.session_state.agent_state, prompt)
st.session_state.agent_state = estado
st.markdown(estado.get("respuesta") or "(Sin respuesta)")
```

---

## Historial vs estado (recordatorio)

- **`messages`**: lo que el usuario ve en el hilo (texto de burbujas).
- **`agent_state`**: la tarea en curso (`preferencias`, `plan`, `done`, `traza`).

Puedes mostrar el plan en la burbuja del asistente cuando `done` sea True, sin meter el dict entero en cada mensaje.

---

## Para llevarte

Si mañana cambias Streamlit por una API (Sprints 14–16), **`procesar_turno` no se toca** — solo cambias el cliente.
