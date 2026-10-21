# Bloque 3 — Persistencia de datos con SQL y SQLModel

Guardar el historial del turno con **SQL** (tablas) y **SQLModel** (ORM en Python).

En este sprint practicáis con **SQLite** (fichero local). Hay otros RDBMS (PostgreSQL, MySQL, etc.); más adelante, en producción, podéis migrar cambiando sobre todo la `DATABASE_URL` — el código SQLModel se mantiene.

| # | Documento | Qué aprenderás |
|---|-----------|----------------|
| 0 | [Introducción](./00_introduccion.md) | Qué persistir; mapa de lectura |
| 1 | [SQL, SQLModel y RDBMS](./01_sql_sqlmodel_y_rdbms.md) | Capas + SQLite ahora / otros motores después |
| 2 | [SQL mínimo](./02_sql_minimo.md) | Tablas, PK/FK, SELECT/INSERT |
| 3 | [ORM y SQLModel](./03_orm_y_sqlmodel.md) | Modelo → engine → Session → select |
| 4 | [Modelo mínimo](./04_modelo_minimo.md) | `Conversation` / `Message` |
| 5 | [Conectar desde FastAPI](./05_conectar_desde_fastapi.md) | `create_engine`, `Session` |
| 6 | [Escribir y leer en el turno](./06_escribir_y_leer_en_el_turno.md) | Tras `/ask` |
| 7 | [API + historial SQLModel](./07_api_agente_historial_SQL_model.md) | Stub → [repo workout](https://github.com/aie-online-tb/Sprint14_API_FastAPI_SQLModel_Proyecto_MultiAgente_LangGraph_tarde_cultural) |

**Atajo (mínimo para practicar):** 02 → 03 → 04 → 06.

**Workout:**

1. [`01_intro_sqlmodel.ipynb`](../../02_Workout/03_Persistencia_de_datos_con_PostgreSQL/01_sqlmodel_demo/01_intro_sqlmodel.ipynb) — intro SQLModel  
2. [`02_api_agente_historial`](../../02_Workout/03_Persistencia_de_datos_con_PostgreSQL/02_api_agente_historial.md) — mismo repo  
