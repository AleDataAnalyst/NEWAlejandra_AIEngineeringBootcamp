![Cabecera](../../../../06_AI_Agents_Engineering/Sprint_11/assets/cabecera_thebridge.png)

# Introducción — De la demo local al servicio

Hasta ahora el sistema de IA se demostraba en **local**:

- un notebook,
- una CLI (`python main.py --ask "..."`),
- o Streamlit en `localhost`.

Eso vale para aprender. En un entorno real, otros programas (front, móvil, otro backend) necesitan llamar al sistema por **HTTP**.

```text
Antes (S10–13)              Ahora (S14)
─────────────────           ─────────────────
Cliente y lógica            Cliente ──HTTP──► API ──► lógica
en el mismo proceso         (Streamlit, curl, otro servicio)
```

## Una idea por capa

| Capa | Responsabilidad |
|------|-----------------|
| **Cliente** | Pregunta y muestra resultado (UI, curl, Postman, Swagger). |
| **API** | Traduce HTTP ↔ Python (rutas, schemas, errores). |
| **Lógica** | `responder` / `procesar_turno` (RAG, agente, tools). |

La API **no** reescribe el RAG ni el grafo. Solo los expone.

## Mapa de este bloque (teoría de sobra)

| Doc | Contenido |
|-----|-----------|
| [01](./01_que_es_una_api_para_ia.md) | Internet, HTTP, códigos, CRUD, REST, CORS, APIs y GenAI |
| [02](./02_fastapi_basico.md) | FastAPI, uvicorn, Swagger, métodos, middleware, errores |
| [03](./03_pydantic_y_contratos.md) | Path, Query, Body, Pydantic, `response_model` |
| [04](./04_health_errores_y_env.md) | `/health`, errores HTTP, `.env`, `config.py` |
| [05](./05_primera_api_fastapi.md) | Workout: primera API (repo GitHub) |

**Workout:** [`05_primera_api_fastapi`](./05_primera_api_fastapi.md) → [Sprint14_API_FastAPI](https://github.com/aie-online-tb/Sprint14_API_FastAPI) — CRUD + Pydantic en `/docs` (sin IA; eso es el bloque 2).

**Fuera de este bloque (a propósito):** plantillas Jinja2, subida de ficheros, Flask, JWT. Docker → Sprint 15.

---

## Resumen

- Streamlit/CLI = buen MVP; API = mismo cerebro, otro “enchufe”.
- Leed la teoría con calma: es material de estudio, no solo “para la clase”.
- El hilo GenAI llega fuerte en el Bloque 2 (`procesar_turno` detrás de `/ask`).
