![Cabecera](../../../../06_AI_Agents_Engineering/Sprint_11/assets/cabecera_thebridge.png)

# Introducción — Persistencia en el backend de IA

Sin base de datos, cada reinicio de `uvicorn` **borra** el historial que solo vivía en memoria (o en el `MemorySaver` del proceso).

En este bloque guardáis lo justo con **SQL** + **SQLModel** (ORM):

- un hilo (`thread_id`),
- los mensajes usuario / asistente.

**Motor en este sprint:** SQLite (`historial.db`). Es un RDBMS más; en producción podréis usar PostgreSQL u otro sin reescribir los modelos.

## Cómo leer este bloque

| # | Doc | Para qué |
|---|-----|----------|
| 1 | [SQL, SQLModel y RDBMS](./01_sql_sqlmodel_y_rdbms.md) | Mapa: capas y motores |
| 2 | [SQL mínimo](./02_sql_minimo.md) | Tablas, PK/FK, SELECT/INSERT |
| 3 | [ORM y SQLModel](./03_orm_y_sqlmodel.md) | Modelo → Session → consultas |
| 4 | [Modelo mínimo](./04_modelo_minimo.md) | `Conversation` / `Message` del historial |
| 5 | [Conectar desde FastAPI](./05_conectar_desde_fastapi.md) | `engine` + `DATABASE_URL` |
| 6 | [Escribir y leer en el turno](./06_escribir_y_leer_en_el_turno.md) | `save_turn` + GET messages |
| 7 | [API + historial SQLModel](./07_api_agente_historial_SQL_model.md) | Stub → [repo](https://github.com/aie-online-tb/Sprint14_API_FastAPI_SQLModel_Proyecto_MultiAgente_LangGraph_tarde_cultural) |

Si vais justos de tiempo: **02 → 03 → 04 → 06** (lo imprescindible para el workout / Live Review).

## Qué sí / qué no

| Sí (este sprint) | No (fuera o más adelante) |
|------------------|---------------------------|
| Historial de preguntas/respuestas | Checkpoints completos de LangGraph en la DB |
| `thread_id` estable | Auth de usuarios con JWT |
| Una o dos tablas con SQLModel | Relaciones complejas, migraciones Alembic |

Los checkpoints de LangGraph (`MemorySaver`) son **otra capa**. Aquí persistís el **historial de negocio** que la API expone.

## Enlace con lo ya visto

Si ya practicasteis SQL a mano: aquí el SQL queda **debajo** del ORM; vosotros trabajáis con modelos Python y una `Session`.

---

## Resumen

- SQLModel = modelos + tablas + sesión.
- Objetivo: que `/ask` deje rastro entre reinicios.
- SQLite ahora; otros RDBMS (p. ej. Postgres) cuando despleguéis.
