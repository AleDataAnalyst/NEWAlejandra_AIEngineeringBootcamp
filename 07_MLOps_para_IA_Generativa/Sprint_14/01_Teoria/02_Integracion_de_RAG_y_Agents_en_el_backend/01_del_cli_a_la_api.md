![Cabecera](../../../../06_AI_Agents_Engineering/Sprint_11/assets/cabecera_thebridge.png)

# Del CLI a la API

Imagina que ya tienes:

```python
def procesar_turno(mensaje: str, estado: dict | None = None) -> dict:
    ...
    return {"respuesta": "...", "estado": estado, "done": False}
```

o, en estilo RAG:

```python
def responder(pregunta: str) -> dict:
    return {"respuesta": "...", "fuentes": [...]}
```

## Antes

```bash
python main.py --ask "¿Hay jazz este viernes?"
```

## Ahora

```python
from src.agent import procesar_turno  # o from src.logic import responder

@app.post("/ask")
def ask(body: AskIn) -> AskOut:
    out = procesar_turno(body.pregunta)
    return AskOut(respuesta=out["respuesta"], thread_id=body.thread_id)
```

## Checklist de migración

| Paso | Hecho si… |
|------|-----------|
| 1 | La lógica está en un módulo importable (`src/…`), no solo en el notebook. |
| 2 | Devuelve un **dict** (o modelo) estable. |
| 3 | FastAPI solo traduce HTTP ↔ ese dict. |
| 4 | Streamlit/CLI pueden seguir llamando a la misma función **o** pasar a HTTP. |

No hace falta reescribir el grafo LangGraph para este sprint: lo envuelves.

---

## Resumen

- Extrae la función e impórtala en la ruta.
- Si la función no es importable, primero modulariza; luego API.
