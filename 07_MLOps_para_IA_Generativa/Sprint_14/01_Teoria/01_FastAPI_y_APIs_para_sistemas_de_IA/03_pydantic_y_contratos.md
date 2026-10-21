![Cabecera](../../../../06_AI_Agents_Engineering/Sprint_11/assets/cabecera_thebridge.png)

# Pydantic, validación y contratos

FastAPI valida **rutas**, **query params** y **body** usando anotaciones de tipo y [Pydantic](https://docs.pydantic.dev/latest/). Si los datos no cumplen el contrato → **HTTP 422** con detalle.

---

## 1) Tres sitios donde se valida

| Sitio | Ejemplo | Herramienta |
|-------|---------|-------------|
| **Path** | `/items/{item_id}` | tipo + `Path(...)` |
| **Query** | `?q=jazz&page=1` | tipo + `Query(...)` |
| **Body** | JSON POST | `BaseModel` |

Swagger muestra esas restricciones automáticamente.

---

## 2) Validación de path

```python
from fastapi import FastAPI, Path

app = FastAPI()

@app.get("/items/{item_id}")
async def read_item(
    item_id: int = Path(..., title="ID del ítem", ge=1, le=1000),
):
    return {"item_id": item_id}
```

- `...` = obligatorio.
- `ge` / `le` = mayor/menor o igual.

### Regex en path (estudio)

```python
@app.get("/users/{username}")
async def get_user(
    username: str = Path(
        ...,
        pattern=r"^[a-zA-Z0-9_-]{3,16}$",
        title="Nombre de usuario",
        description="3–16 caracteres: letras, números, _ o -",
    ),
):
    return {"username": username}
```

(En Pydantic v2 / FastAPI reciente se usa `pattern=`; en ejemplos antiguos veréis `regex=`.)

---

## 3) Validación de query params

```python
from fastapi import FastAPI, Query

app = FastAPI()

@app.get("/search/")
async def search_items(
    q: str = Query(..., min_length=3, max_length=50, title="Término de búsqueda"),
    page: int = Query(1, ge=1, title="Número de página"),
    size: int = Query(10, ge=1, le=100, title="Tamaño de página"),
):
    return {"q": q, "page": page, "size": size}
```

Probad: `http://127.0.0.1:8000/search/?q=python&page=2&size=20`

Si `q` tiene 1 carácter → 422.

Query simple sin `Query()`:

```python
@app.get("/items/")
async def read_items(skip: int = 0, limit: int = 10):
    return {"skip": skip, "limit": limit}
```

---

## 4) Validación del body (Pydantic)

```python
from pydantic import BaseModel, Field

class AskIn(BaseModel):
    pregunta: str = Field(min_length=1, max_length=2000)
    thread_id: str | None = Field(default=None, max_length=100)

class AskOut(BaseModel):
    respuesta: str
    thread_id: str
    done: bool = False
```

```python
from fastapi import FastAPI

app = FastAPI()

@app.post("/ask", response_model=AskOut)
def ask(body: AskIn) -> AskOut:
    return AskOut(
        respuesta=f"Eco: {body.pregunta.strip()}",
        thread_id=body.thread_id or "default",
        done=False,
    )
```

### Modelo genérico de estudio

```python
from pydantic import BaseModel

class Item(BaseModel):
    name: str
    price: float
    is_offer: bool | None = None

@app.post("/items/")
async def create_item(item: Item):
    return {"item_name": item.name, "item_price": item.price}
```

Validación fuera de FastAPI:

```python
user_data = {"id": 1, "name": "Ada", "email": "ada@example.com"}

class User(BaseModel):
    id: int
    name: str
    email: str

user = User(**user_data)  # valida / convierte
```

---

## 5) Validación avanzada con Pydantic

```python
from pydantic import BaseModel, Field, EmailStr, field_validator

class User(BaseModel):
    username: str
    email: EmailStr
    age: int = Field(..., gt=0, description="La edad debe ser > 0")

    @field_validator("username")
    @classmethod
    def validate_username(cls, value: str) -> str:
        if len(value) < 3:
            raise ValueError("El nombre de usuario debe tener al menos 3 caracteres")
        return value
```

(`EmailStr` requiere el extra `email-validator` en muchos entornos: `pip install email-validator`.)

---

## 6) `response_model`

Fija qué sale al cliente (filtra campos extra, documenta Swagger):

```python
@app.get("/items/{item_id}", response_model=Item)
async def read_item(item_id: int):
    return {"name": "Sample", "price": 10.5, "secret": "no sale si no está en Item"}
```

---

## 7) Error 422: forma típica

```json
{
  "detail": [
    {
      "loc": ["body", "price"],
      "msg": "value is not a valid float",
      "type": "type_error.float"
    }
  ]
}
```

Interpretad `loc`: dónde falló (`body`, `query`, `path` + nombre del campo).

---

## 8) Ejemplo completo de estudio: CRUD usuarios

A continuación, podéis ver un ejemplo completo de CRUD de usuarios con FastAPI y Pydantic.

```python
from typing import List

from fastapi import FastAPI, HTTPException
from pydantic import BaseModel, EmailStr, Field
import uvicorn

app = FastAPI()

class User(BaseModel):
    id: int
    name: str = Field(..., min_length=3, max_length=50)
    email: EmailStr
    age: int = Field(..., gt=0)

fake_db: List[User] = [
    User(id=1, name="Alice Smith", email="alice@example.com", age=30),
    User(id=2, name="Bob Johnson", email="bob@example.com", age=25),
]
last_id = max(u.id for u in fake_db)

@app.post("/users/", response_model=User, status_code=201)
async def create_user(user: User):
    global last_id
    if any(u.email == user.email for u in fake_db):
        raise HTTPException(status_code=400, detail="Email ya registrado")
    last_id += 1
    user.id = last_id
    fake_db.append(user)
    return user

@app.get("/users/", response_model=List[User])
async def read_users():
    return fake_db

@app.get("/users/{user_id}", response_model=User)
async def read_user(user_id: int):
    for user in fake_db:
        if user.id == user_id:
            return user
    raise HTTPException(status_code=404, detail="Usuario no encontrado")

@app.put("/users/{user_id}", response_model=User)
async def update_user(user_id: int, updated: User):
    for i, user in enumerate(fake_db):
        if user.id == user_id:
            fake_db[i] = updated
            return updated
    raise HTTPException(status_code=404, detail="Usuario no encontrado")

@app.delete("/users/{user_id}", status_code=204)
async def delete_user(user_id: int):
    for i, user in enumerate(fake_db):
        if user.id == user_id:
            del fake_db[i]
            return
    raise HTTPException(status_code=404, detail="Usuario no encontrado")

if __name__ == "__main__":
    uvicorn.run("app:app", host="127.0.0.1", port=8000, reload=True)
```

---

## 9) Regla del bootcamp (GenAI)

| Quién | Qué decide |
|-------|------------|
| **Pydantic / Python** | Forma del JSON, longitudes, tipos, 422 |
| **Lógica del agente** | Contenido de la respuesta, `done`, `max_turns` |
| **LLM** | Texto / JSON de negocio; no banderas de control si Python puede calcularlas |

---

## Resumen

- Path / Query / Body = tres capas de validación.
- `AskIn` / `AskOut` = contrato del sistema de IA.
- 422 = el cliente mandó mal el JSON; no es un fallo del LLM.
- El CRUD de usuarios sirve para consolidar los conceptos de FastAPI y Pydantic vistos hasta ahora.
