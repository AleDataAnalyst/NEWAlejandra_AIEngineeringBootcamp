# Live Review — API agente calidad del aire + historial

Práctica: **FastAPI + Pydantic + SQLModel** detrás de un **agente LangGraph de calidad del aire** (grafo dado). Foco: contratos HTTP, modelos SQL, `save_turn` y rutas `/ask` + GET messages.

| Carpeta | Contenido |
|---------|-----------|
| [`01_api_backend_calidad_aire/`](01_api_backend_calidad_aire/) | Proyecto alumno (5 TODOs) |
| [`01_api_backend_calidad_aire_SOLUTION/`](01_api_backend_calidad_aire_SOLUTION/) | Referencia del profesor |

## Contrato HTTP

```text
POST /ask { pregunta, thread_id?, auto_aprobar? }
  → procesar_turno (grafo, dado)
  → save_turn si el turno cierra (sin HITL pendiente)

POST /approve { thread_id, aprobado }   # dado en alumno
GET  /health
GET  /threads/{thread_id}/messages      # TODO alumno
```

## Qué se da / qué se pide

| Dado | TODO alumno |
|------|-------------|
| Agente (`src/agent.py`, `graph.py`, `tools/`, `data/`) | **1.** `schemas.py` (AskIn/AskOut/ApproveIn/MessageOut) |
| `engine`, `ensure_schema`, `list_messages` | **2.** `src/models.py` (Conversation, Message) |
| `/health`, lifespan, `/approve` | **3.** `save_turn` en `src/db.py` |
| Helpers `_estado_sesion`, `_persistir_si_hay_respuesta` | **4.** Completar `POST /ask` |
| | **5.** Completar `GET /threads/{id}/messages` |

Ver README del proyecto alumno y `verificar.py`.
