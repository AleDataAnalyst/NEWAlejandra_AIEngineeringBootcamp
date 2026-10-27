![Cabecera](../../../../06_AI_Agents_Engineering/Sprint_11/assets/cabecera_thebridge.png)

# SQL, SQLModel y RDBMS

## Dos capas

| Capa | Rol |
|------|-----|
| **SQLModel** | Cómo habláis vosotros con la DB (clases Python, `Session`). |
| **RDBMS** (SQLite, PostgreSQL, MySQL…) | Dónde viven los datos y quién ejecuta el SQL. |

Misma API de código; cambia sobre todo la **URL del motor** (`DATABASE_URL`).

## Hay varios RDBMS

Un RDBMS (Relational Database Management System) guarda datos en tablas con SQL. Ejemplos:

| Motor | Cómo lo usamos aquí |
|-------|---------------------|
| **SQLite** | Fichero local, sin servidor. **Default en este sprint** (clase, workouts, Live Review). |
| **PostgreSQL** | Servidor / PaaS. Candidato típico cuando paséis a producción. |
| Otros (MySQL, etc.) | Misma idea: cambiáis driver + URL si el proyecto lo pide. |

No hace falta dominar todos. Importa: **SQLModel habla SQL; el motor es intercambiable** a nivel de conexión.

## Alternativas rápidas (qué NO sustituye el historial)

| Opción | Pros | En este sprint |
|--------|------|----------------|
| Solo RAM | Simple | Se pierde al reiniciar |
| **SQLite** (fichero) | Cero servidor; ideal en clase | **Lo que usáis** |
| **PostgreSQL** (u otro RDBMS en servidor) | Estándar en PaaS / producción | Más adelante (deploy) |
| Chroma / vector DB | Embeddings del RAG | No sustituye historial tabular |

## Dos almacenes distintos

```text
Pregunta del usuario
        │
        ├─► SQLModel → RDBMS (SQLite / Postgres / …)   (quién preguntó qué)
        │
        └─► Vector DB                                  (chunks del corpus — RAG)
```

## Por qué SQLModel

SQLModel es un ORM (Object-Relational Mapping): mapea clases Python a tablas SQL.

- Encaja con FastAPI / Pydantic (mismo estilo).
- Debajo sigue habiendo SQL.

Relaciones avanzadas, JWT y roles → fuera de este sprint.

---

## Resumen

- **Ahora:** SQLite + SQLModel.
- **Después (producción):** misma app, `DATABASE_URL` → PostgreSQL u otro RDBMS que elijáis.
