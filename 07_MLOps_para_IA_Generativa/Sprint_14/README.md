![Cabecera](../../06_AI_Agents_Engineering/Sprint_11/assets/cabecera_thebridge.png)

# 📘 Sprint 14 — AI APIs & Backend Services

En los Sprints 10–13 el sistema de IA vivía detrás de **CLI** o **Streamlit**: la lógica (`responder`, `procesar_turno`) y el cliente compartían proceso.

Aquí el salto: esa lógica se expone como **API HTTP** con FastAPI. Después la conectáis a **RAG/agente** y añadís **persistencia** con SQL + SQLModel (SQLite en este sprint).

> **¿Cómo expongo RAG/agente como servicio HTTP y guardo lo necesario, sin mezclar UI y lógica?**

---

## Mapa del módulo (Sprints 14–16)

| Sprint | Pregunta | Fase |
|--------|----------|------|
| **14** (este) | ¿Cómo expongo el sistema como API y persisto datos? | Backend |
| **15** | ¿Cómo empaqueto y publico el servicio? | Deploy |
| **16** | ¿Cómo lo opero (logs, seguridad light, informe)? | Operar |

```text
S10–13  CLI / Streamlit → responder() / procesar_turno()
 ↓
S14     FastAPI (/health, /ask) → misma lógica
        + SQLModel (historial; SQLite en este sprint)
 ↓
S15     Docker + PaaS (URL pública)
 ↓
S16     Observabilidad light + informe → Project Break 3
```

**Prerrequisito:** haber cerrado el ciclo agentes (S11–13) o, como mínimo, tener una función clara tipo `responder(pregunta)` / `procesar_turno(mensaje, estado)`.  
**No repetimos** Docker, PaaS ni CI/CD (van en S15–16).

---

## Stack y dominio

- **Stack:** Python · FastAPI · Pydantic · **SQLModel** · SQLite (este sprint; otros RDBMS en producción) · Gemini (si el backend llama al LLM)
- **Proyecto (workout):** tarde cultural — API + persistencia
- **Live Review:** calidad del aire — FastAPI + SQLModel + historial

---

## 🧭 Bloque 1 — FastAPI y APIs para sistemas de IA

| Doc | Contenido |
|-----|-----------|
| [Introducción](./01_Teoria/01_FastAPI_y_APIs_para_sistemas_de_IA/00_introduccion.md) | Puente CLI/Streamlit → API |
| [Qué es una API / HTTP / REST](./01_Teoria/01_FastAPI_y_APIs_para_sistemas_de_IA/01_que_es_una_api_para_ia.md) | HTTP, códigos, CRUD, REST, CORS, GenAI |
| [FastAPI básico](./01_Teoria/01_FastAPI_y_APIs_para_sistemas_de_IA/02_fastapi_basico.md) | uvicorn, Swagger, middleware, errores, mini-CRUD |
| [Pydantic y contratos](./01_Teoria/01_FastAPI_y_APIs_para_sistemas_de_IA/03_pydantic_y_contratos.md) | Path/Query/Body, `AskIn`/`AskOut`, validación |
| [Health, errores y env](./01_Teoria/01_FastAPI_y_APIs_para_sistemas_de_IA/04_health_errores_y_env.md) | `/health`, HTTPException, `.env`, `config.py` |
| [Primera API FastAPI](./01_Teoria/01_FastAPI_y_APIs_para_sistemas_de_IA/05_primera_api_fastapi.md) | Stub → repo workout CRUD + Pydantic |

| Workout | Descripción |
|---------|-------------|
| [01_primera_api_fastapi](./02_Workout/01_FastAPI_y_APIs_para_sistemas_de_IA/01_primera_api_fastapi.md) | [Repo](https://github.com/aie-online-tb/Sprint14_API_FastAPI) — CRUD GET/POST/PUT/DELETE + Pydantic |

---

## 🔌 Bloque 2 — Integración de RAG y Agents en el backend

| Doc | Contenido |
|-----|-----------|
| [Introducción](./01_Teoria/02_Integracion_de_RAG_y_Agents_en_el_backend/00_introduccion.md) | UI = cliente; backend = contrato limpio |
| [Del CLI a la API](./01_Teoria/02_Integracion_de_RAG_y_Agents_en_el_backend/01_del_cli_a_la_api.md) | Mismo contrato, otro transporte |
| [Endpoint ask / chat](./01_Teoria/02_Integracion_de_RAG_y_Agents_en_el_backend/02_endpoint_ask_o_chat.md) | `POST /ask`, body y response |
| [Límites, timeouts y secrets](./01_Teoria/02_Integracion_de_RAG_y_Agents_en_el_backend/03_limites_timeouts_y_secrets.md) | Guardrails en Python; keys en env |
| [Dejamos Streamlit como núcleo](./01_Teoria/02_Integracion_de_RAG_y_Agents_en_el_backend/04_streamlit_como_cliente_http.md) | Core = API; UI desacoplada |
| [API FastAPI sobre agente](./01_Teoria/02_Integracion_de_RAG_y_Agents_en_el_backend/05_api_fastAPI_sobre_agente.md) | Stub → repo workout cultural |

| Workout | Descripción |
|---------|-------------|
| [01_api_sobre_agente](./02_Workout/02_Integracion_de_RAG_y_Agents_en_el_backend/01_api_sobre_agente.md) | [Repo](https://github.com/aie-online-tb/Sprint14_API_FastAPI_Proyecto_MultiAgente_LangGraph_tarde_cultural) — FastAPI + agente (`/ask` + `/approve`) |

---

## 🗄️ Bloque 3 — Persistencia de datos con SQL y SQLModel

| Doc | Contenido |
|-----|-----------|
| [Introducción](./01_Teoria/03_Persistencia_de_datos_con_SQL_y_SQLModel/00_introduccion.md) | Qué persistir; mapa de lectura |
| [SQL, SQLModel y RDBMS](./01_Teoria/03_Persistencia_de_datos_con_SQL_y_SQLModel/01_sql_sqlmodel_y_rdbms.md) | Capas + SQLite ahora / otros motores después |
| [SQL mínimo](./01_Teoria/03_Persistencia_de_datos_con_SQL_y_SQLModel/02_sql_minimo.md) | Tablas, PK/FK, SELECT/INSERT |
| [ORM y SQLModel](./01_Teoria/03_Persistencia_de_datos_con_SQL_y_SQLModel/03_orm_y_sqlmodel.md) | Modelo → Session → select |
| [Modelo mínimo](./01_Teoria/03_Persistencia_de_datos_con_SQL_y_SQLModel/04_modelo_minimo.md) | `Conversation` / `Message` |
| [Conectar desde FastAPI](./01_Teoria/03_Persistencia_de_datos_con_SQL_y_SQLModel/05_conectar_desde_fastapi.md) | `create_engine`, `Session` |
| [Escribir y leer en el turno](./01_Teoria/03_Persistencia_de_datos_con_SQL_y_SQLModel/06_escribir_y_leer_en_el_turno.md) | Guardar tras `/ask`; listar por hilo |
| [API + historial SQLModel](./01_Teoria/03_Persistencia_de_datos_con_SQL_y_SQLModel/07_api_agente_historial_SQL_model.md) | Stub → repo workout cultural + SQLite |

| Workout | Descripción |
|---------|-------------|
| [01_intro_sqlmodel.ipynb](./02_Workout/03_Persistencia_de_datos_con_PostgreSQL/01_sqlmodel_demo/01_intro_sqlmodel.ipynb) | Intro SQLModel (notebook) |
| [02_api_agente_historial](./02_Workout/03_Persistencia_de_datos_con_PostgreSQL/02_api_agente_historial.md) | [Repo](https://github.com/aie-online-tb/Sprint14_API_FastAPI_SQLModel_Proyecto_MultiAgente_LangGraph_tarde_cultural) — API + historial SQLite (`save_turn`) |

---

## 🎯 Practica live review

📁 [`Practica_live_review/`](./Practica_live_review/) — **agente LangGraph de calidad del aire** expuesto con **FastAPI** + **SQLModel** (`historial.db`). El grafo viene dado; practicáis Pydantic, modelos SQL, `save_turn` y rutas HTTP (`/ask`, GET messages).

| Entrega | Rol |
|---------|-----|
| Agente, tools, `data/`, `list_messages`, `/health`, `/approve` | Dado |
| **TODO 1** `schemas.py` | AskIn / AskOut / ApproveIn / MessageOut |
| **TODO 2** `src/models.py` | Conversation / Message (SQLModel) |
| **TODO 3** `save_turn` | Persistir user + assistant |
| **TODO 4** `POST /ask` | Sesión, `procesar_turno`, `auto_aprobar`, persistir al cerrar |
| **TODO 5** `GET …/messages` | Listar historial con `list_messages` → `MessageOut` |

Referencia: [`01_api_backend_calidad_aire_SOLUTION/`](./Practica_live_review/01_api_backend_calidad_aire_SOLUTION/).

---

## Escalera pedagógica

```text
CRUD FastAPI + Pydantic (demo inicial)
    ↓
API sobre agente cultural (`/ask` + `/approve`)
    ↓
Intro SQLModel → API + historial SQLite
    ↓
Live Review: FastAPI + SQLModel + agente calidad del aire (schemas, models, save_turn, /ask, GET messages)
    ↓
Sprint 15 (Docker + PaaS)
```

---

## Fuera de alcance

Docker · PaaS / Heroku / Render · CI/CD · JWT / OAuth · Kubernetes · relaciones SQLModel avanzadas · Alembic · checkpoints LangGraph en Postgres (otra capa).

---

## Convenciones

- Teoría en `01_Teoria/` (markdown + proyecto ejemplo en B3).
- Workouts en `02_Workout/` — apps pequeñas autocontenidas; guiones en `guiones_video/` cuando existan.
- **Python decide** límites (`max_turns`, timeouts). El LLM solo propone datos.
- Dominio workouts / proyecto: **agenda cultural**. Live Review: **calidad del aire**.
