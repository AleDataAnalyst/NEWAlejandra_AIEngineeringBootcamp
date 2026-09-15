![Cabecera](../../assets/cabecera_agentes.png)

# Errores y logging de pasos

Cada **turno** de conversación puede fallar. La traza registra qué pasó en cada uno.

---

## Errores frecuentes

| Error | Causa típica | Respuesta junior |
|-------|--------------|------------------|
| API key / cuota | `.env` mal o límite Gemini | Guardar `error`, no reintentar en bucle ciego |
| JSON inválido | El modelo añade prosa o fences | `leer_json` limpia fences; luego abortar el turno |
| Campos faltantes | Patch incompleto | `actualizar_estado` con defaults; no tumbar |
| Timeout / red | Transitorio | Un reintento con backoff simple (opcional) |

---

## Traza mínima (por turno)

Guarda una lista legible para debug y para la live review:

```python
traza = [
    {"turno": 1, "mensaje": "Quiero una tarde cultural.", "status": "ok", "done": False},
    {"turno": 2, "mensaje": "Cine o música, barato.", "status": "ok", "done": False},
    {"turno": 3, "mensaje": "Zona centro.", "status": "error", "detail": "..."},
]
```

`procesar_turno` añade una entrada tras cada llamada al LLM (éxito o error). En Streamlit puedes mostrar `st.expander("Estado / traza")` con preferencias, `plan` y la lista (como el expander de contexto en el RAG de S10).

---

## Abortar vs reintentar

```text
error de parseo  →  reintentar 1 vez con prompt “SOLO JSON”
sigue fallando   →  state["error"] = ... ; entrada traza con status "error"

error de auth    →  no reintentar; mensaje claro en respuesta
```

HITL (“¿apruebas esta acción?”) llega en **Sprint 13**. Aquí basta con no tragarte el fallo en silencio.

---

## Logging vs print

En workouts, `print` / celdas bastan. En el proyecto, centraliza la traza en el estado para que CLI y UI lean lo mismo.

---

## Para llevarte

Si en la live review no puedes enseñar **qué turnos dio** el agente, el diseño aún no es demostrable.
