# Live Review — API agente calidad del aire + historial

**Qué practicáis:** **FastAPI + Pydantic + SQLModel** detrás de un agente LangGraph de **calidad del aire** (el grafo y las tools vienen **dados**). Foco: contratos HTTP, modelos SQL y cablear `/ask` + GET messages → historial.

```text
/docs → FastAPI → procesar_turno → save_turn (historial.db)
                 → GET /threads/{id}/messages
```

**Requisitos:** Python 3.10+ y `GEMINI_API_KEY` en `.env`.

`assets/imagen_demo.jpg` es la imagen demo de la tool `describir_imagen`.

---

## Estructura

```text
.
├── app.py                 # FastAPI: /health, /ask + GET messages (TODO), /approve
├── schemas.py             # TODO 1: AskIn / AskOut / ApproveIn / MessageOut
├── config.py              # paths + DATABASE_URL → historial.db
├── gemini_auth.py         # carga GEMINI_API_KEY al importar app
├── src/
│   ├── agent.py           # procesar_turno, aprobar_plan (dado)
│   ├── graph.py           # LangGraph multiagente + HITL (dado)
│   ├── tools/             # RAG, API aire, hora, imagen (dado)
│   ├── models.py          # TODO 2: Conversation, Message
│   └── db.py              # TODO 3: save_turn | list_messages (dado)
├── data/                  # guía + fallback API
├── assets/                # imagen_demo.jpg
├── verificar.py
└── README.md
```

Ejecuta siempre **desde esta carpeta** (donde está `app.py`).

---

## Instalación y arranque

```bash
python -m venv .venv
source .venv/bin/activate          # Git Bash / macOS / Linux
# .venv\Scripts\Activate.ps1       # Windows PowerShell

pip install -r requirements.txt
cp .env.example .env               # pega GEMINI_API_KEY
uvicorn app:app --reload --port 8000
```

Al arrancar se crea `historial.db` si no existe.

> Si completáis `models.py` **después** de haber arrancado una vez, **borrad `historial.db`** y reiniciad `uvicorn` para recrear las tablas.

---

## Swagger (`/docs`)

**http://127.0.0.1:8000/docs**

---

## Rutas

| Método | Ruta | Estado |
|--------|------|--------|
| GET | `/health` | Dado |
| POST | `/ask` | **TODO 4** |
| POST | `/approve` | Dado |
| GET | `/threads/{thread_id}/messages` | **TODO 5** |

---

## TODOs (5)

1. **`schemas.py` (Pydantic)** — Completar `AskIn.pregunta` con `Field(..., min_length=1)`, `AskOut`, `ApproveIn`, `MessageOut`.
2. **`src/models.py` (SQLModel)** — Completar `Conversation` y `Message` (PK, FK `thread_id`, `role`, `content`, `created_at`).
3. **`src/db.py` → `save_turn`** — Crear `Conversation` si falta; guardar mensajes `user` + `assistant`; `commit`.
4. **`app.py` → `POST /ask`** — Validar, `_estado_sesion`, `procesar_turno`, `auto_aprobar` + `aprobar_plan`; si `not pendiente_hitl`, `_persistir_si_hay_respuesta`.
5. **`app.py` → `GET /threads/{thread_id}/messages`** — Llamar `db.list_messages` y devolver `list[MessageOut]`.

Orden recomendado: schemas → models → `save_turn` → `/ask` → GET messages.

---

## Comprobar

```bash
python verificar.py
python verificar.py --check   # solo GET /health (sin llamar a Gemini)
```

---

## Práctica con mensajes de aire

Usad el mismo `thread_id` (p. ej. `demo-aire`) en varios turnos.

> **Tiempo de `/ask`:** el agente multiagente llama al LLM y a tools (guía, API Madrid, etc.). **Cada `/ask` puede tardar del orden de 1–3 minutos.** `/health` y `GET …/messages` son rápidos.
>
> Para acortar demos: en `config.py` bajad `MAX_STEPS_DEFAULT` / `MAX_ITER` (menos vueltas del grafo) o probad otro modelo en `GEMINI_MODEL` (p. ej. uno más ligero/rápido de la familia Flash). Reiniciad `uvicorn` tras el cambio.

### Ejemplo 1 — primer `/ask`

```json
{
  "pregunta": "Zona centro, contaminante NO2. Consulta la guía y datos de la API de Madrid. Propón un plan breve.",
  "thread_id": "demo-aire",
  "auto_aprobar": true
}
```

### Ejemplo 2 — segundo turno

```json
{
  "pregunta": "¿Qué significa un pico de PM2.5 en hora punta?",
  "thread_id": "demo-aire",
  "auto_aprobar": true
}
```

### Historial

GET `http://127.0.0.1:8000/threads/demo-aire/messages` → filas `user` / `assistant` en SQLite.

Abrid `historial.db` con *SQLite Viewer* en el editor y contrastad tablas `conversation` / `message`.

Tras reiniciar `uvicorn`, el historial SQL **sigue**; la sesión del grafo en RAM no.

---

## Checklist

- [ ] `.env` con key y `/docs` abre.
- [ ] `python verificar.py` sin pendientes.
- [ ] Dos `/ask` + GET messages → al menos 4 mensajes.
- [ ] Reinicio de uvicorn: historial intacto.
- [ ] Entiendo schemas → models → `save_turn` → `/ask` → GET messages.

---

## Fuera de alcance

Streamlit, CLI, reescribir el grafo, Docker/deploy.
