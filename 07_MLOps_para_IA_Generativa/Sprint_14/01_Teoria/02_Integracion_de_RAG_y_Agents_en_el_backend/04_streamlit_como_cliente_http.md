![Cabecera](../../../../06_AI_Agents_Engineering/Sprint_11/assets/cabecera_thebridge.png)

# Streamlit como cliente HTTP

En sprints anteriores Streamlit (o la CLI) **importaba** `procesar_turno` / `responder` en el mismo proceso: la UI y el cerebro iban juntos.

```text
Antes
[Browser] → Streamlit ──import──► procesar_turno() / agente
```

Eso sirve para demos. **Ya no es el modelo de este sprint:** el **core** de la aplicación es la **API FastAPI** (contrato HTTP + lógica). Streamlit deja de estar ligado a ese core.

```text
Ahora (S14)
Cliente (Swagger, curl, Postman, un front…)
        ↓  HTTP
     FastAPI  →  procesar_turno() / agente
```

## Por qué lo dejamos así

| Motivo | Detalle |
|--------|---------|
| Core = API | Validación, rutas, secrets y (más adelante) historial viven en el backend. |
| UI desacoplada | Cualquier cliente habla HTTP; no hace falta que Streamlit “posea” el agente. |
| Práctica del sprint | En workouts y Live Review usáis `/docs` (Swagger), o **Postman**, no una app Streamlit. |

Ahora Streamlit **ya no forma parte del núcleo** del sistema de IA que estáis construyendo aquí.

## Si algún día un front llama a la API (idea, no práctica)

Cualquier UI (Streamlit, React, móvil…) sería solo un **cliente HTTP**:

```text
[Browser] → UI → httpx/fetch → FastAPI → procesar_turno
```

Ejemplo de una llamada a tu API:

```python
import httpx

API_URL = "http://127.0.0.1:8000"
r = httpx.post(
    f"{API_URL}/ask",
    json={"pregunta": "Hola", "thread_id": "demo"},
    timeout=120.0,
)
r.raise_for_status()
print(r.json()["respuesta"])
```

---

## Resumen

- Streamlit deja de ser el dueño del cerebro: el **core** es la API.
- En este sprint practicáis el backend con FastAPI + Swagger.
- Un front futuro solo cambia de URL/cliente, no reescribe la lógica.
