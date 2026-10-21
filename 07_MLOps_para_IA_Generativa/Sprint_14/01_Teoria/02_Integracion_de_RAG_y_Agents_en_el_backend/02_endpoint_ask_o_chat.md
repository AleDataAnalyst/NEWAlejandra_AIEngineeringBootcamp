![Cabecera](../../../../06_AI_Agents_Engineering/Sprint_11/assets/cabecera_thebridge.png)

# Endpoint `/ask` (o `/chat`)

Para crear nuestra API de IA generativa, vamos a usar un endpoint principal de negocio:

```text
POST /ask
```

(` /chat` es el mismo patrón con otro nombre; elige uno y sé consistente.)

## Contrato sugerido

**Request**

```json
{
  "pregunta": "¿Qué eventos hay en Lavapiés?",
  "thread_id": "demo-1"
}
```

**Response**

```json
{
  "respuesta": "…",
  "thread_id": "demo-1",
  "done": false
}
```

Campos extra (`fuentes`, `estado`) solo si el cliente los necesita. Empieza **corto**.

## Código de referencia

```python
@app.post("/ask", response_model=AskOut)
def ask(body: AskIn) -> AskOut:
    out = procesar_turno(body.pregunta)
    return AskOut(
        respuesta=out["respuesta"],
        thread_id=body.thread_id,
        done=out.get("done"),
    )
```

## `/health` vs `/ask`

| Ruta | Llama al LLM | Uso |
|------|--------------|-----|
| `GET /health` | No | ¿Proceso vivo? |
| `POST /ask` | Sí (o stub) | Pregunta de negocio |

Cuando tengamos la API en producción, si `/health` falla, no haremos aún la llamada al LLM con `/ask`.

---

## Resumen

- Un `POST` de negocio con `/ask` o `/chat` + un `GET` de salud con `/health` para comprobar si la API está funcionando correctamente.
- Body mínimo: `pregunta` (+ `thread_id` si hay hilos / DB).
