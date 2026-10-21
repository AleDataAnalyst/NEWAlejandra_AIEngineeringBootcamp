![Cabecera](../../../../06_AI_Agents_Engineering/Sprint_11/assets/cabecera_thebridge.png)

# ORM y SQLModel (paso a paso)

Docs oficiales: [SQLModel](https://sqlmodel.tiangolo.com/) · [FastAPI + SQL databases](https://fastapi.tiangolo.com/tutorial/sql-databases/)

> **Mínimo para practicar:** modelo con `table=True` → `create_engine` → `create_all` → `Session` → `add`/`commit` → `select`.

---

## 1) ¿Qué es un ORM?

Un **ORM** (Object-Relational Mapping) traduce entre:

```text
Clases / objetos Python  ↔  Tablas / filas SQL
```

Sin ORM:

```sql
SELECT * FROM message WHERE thread_id = 'demo-aire';
```

Con ORM (idea):

```python
session.exec(select(Message).where(Message.thread_id == "demo-aire")).all()
```

**Ventajas para este curso**

- Menos SQL a mano.
- Mismos tipos que Pydantic / FastAPI.
- Cambiar de SQLite a otro RDBMS suele ser cambiar la URL.

SQLModel se apoya en **SQLAlchemy** (motor ORM maduro) y en **Pydantic** (validación). Vosotros usáis SQLModel; no hace falta aprender SQLAlchemy “a pelo” en este sprint.

---

## 2) Instalar

```bash
pip install sqlmodel
```

(En los proyectos del sprint ya viene en `requirements.txt`.)

---

## 3) Definir un modelo (= una tabla)

```python
from typing import Optional

from sqlmodel import Field, SQLModel


class Message(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    thread_id: str = Field(max_length=100)
    role: str = Field(max_length=20)
    content: str
```

- `table=True` → esta clase es una **tabla** real.
- `Field(...)` → PK, longitudes, FK, etc.
- `id: Optional[int] = Field(default=None, primary_key=True)` → PK autoincremental (SQLite asigna el número al guardar).

---

## 4) Conectar y crear tablas

```python
from sqlmodel import SQLModel, create_engine

engine = create_engine("sqlite:///historial.db", echo=False)

# Crea las tablas si no existen (según las clases con table=True)
SQLModel.metadata.create_all(engine)
```

- `sqlite:///historial.db` → fichero en disco (este sprint).
- `echo=True` imprime el SQL en consola (útil para aprender; en demos suele ir `False`).

---

## 5) Sesión: insertar

```python
from sqlmodel import Session

with Session(engine) as session:
    msg = Message(thread_id="demo-aire", role="user", content="Hola")
    session.add(msg)
    session.commit()
```

- `add` prepara el insert.
- `commit` lo escribe en la DB.
- Sin `commit`, al cerrar la sesión se pierde.

---

## 6) Sesión: consultar (estilo actual)

Preferid `select` + `session.exec` (API recomendada con SQLModel reciente):

```python
from sqlmodel import Session, select

with Session(engine) as session:
    rows = session.exec(
        select(Message).where(Message.thread_id == "demo-aire")
    ).all()
    for m in rows:
        print(m.role, m.content)
```

> En tutoriales antiguos veréis `session.query(Message).filter(...)`. Funciona, pero en material nuevo usamos `select`.

---

## 7) Mini flujo completo (sin FastAPI)

```python
from typing import Optional

from sqlmodel import Field, Session, SQLModel, create_engine, select


class Message(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    thread_id: str
    role: str
    content: str


engine = create_engine("sqlite:///demo_teoria.db")
SQLModel.metadata.create_all(engine)

with Session(engine) as session:
    session.add(
        Message(thread_id="demo", role="user", content="¿Qué es SQLite?")
    )
    session.add(
        Message(thread_id="demo", role="assistant", content="Un RDBMS en un fichero.")
    )
    session.commit()

    for m in session.exec(select(Message).where(Message.thread_id == "demo")):
        print(m.id, m.role, m.content)
```

Podéis pegarlo en un script o celda y abrir `demo_teoria.db` con *SQLite Viewer*.

---

## 8) Cómo encaja con FastAPI

| Pieza | Dónde |
|-------|--------|
| Modelos (`Conversation`, `Message`) | `src/models.py` |
| `engine`, `save_turn`, `list_messages` | `src/db.py` |
| Tras `/ask` | la ruta llama a `save_turn` |
| GET historial | la ruta llama a `list_messages` |

Los siguientes docs del bloque aplican esto al **historial del agente**.

---

## Resumen

- ORM = objetos Python ↔ tablas SQL.
- SQLModel = ORM cómodo con FastAPI/Pydantic.
- Ciclo: modelo → engine → `create_all` → `Session` → `add`/`commit` → `select`.
