![Cabecera](../../../../06_AI_Agents_Engineering/Sprint_11/assets/cabecera_thebridge.png)

# Conectar desde FastAPI (SQLModel)

## URL del motor

En este sprint usáis SQLite. La misma app puede apuntar a otro RDBMS cambiando la URL:

```text
# Este sprint (default)
sqlite:///historial.db

# Más adelante (producción / PaaS), por ejemplo Postgres:
DATABASE_URL=postgresql+psycopg://usuario:password@localhost:5432/ia_demo
```

En `config.py`:

```python
import os

DATABASE_URL = os.getenv("DATABASE_URL", "sqlite:///historial.db").strip()
```

## Engine + crear tablas

```python
from sqlmodel import SQLModel, Session, create_engine

from src.models import Conversation, Message  # noqa: F401 — registran las tablas

engine = create_engine(DATABASE_URL, echo=False)


def ensure_schema() -> None:
    SQLModel.metadata.create_all(engine)


def get_session() -> Session:
    return Session(engine)
```

Llamad a `ensure_schema()` al arrancar la app (`lifespan`).

## Dependencias

```text
sqlmodel
# psycopg[binary]   # solo si más adelante usáis Postgres
```

## SQLite vs otro RDBMS

| | SQLite (este sprint) | PostgreSQL u otro (producción) |
|--|----------------------|--------------------------------|
| Infra | Sin instalar servidor | Docker, servicio local o PaaS |
| Datos | Fichero `historial.db` | Servidor + `DATABASE_URL` |
| Código | SQLModel | El mismo SQLModel |

---

## Resumen

- Una URL → `create_engine` → `Session`.
- `create_all` al arranque crea las tablas si no existen.
