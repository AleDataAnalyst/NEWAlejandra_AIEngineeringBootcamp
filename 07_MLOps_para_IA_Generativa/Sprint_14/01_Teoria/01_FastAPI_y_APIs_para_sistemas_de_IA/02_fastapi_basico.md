![Cabecera](../../../../06_AI_Agents_Engineering/Sprint_11/assets/cabecera_thebridge.png)

# FastAPI

[FastAPI](https://fastapi.tiangolo.com/) es el framework del bootcamp para APIs en Python: tipado, validación con Pydantic y documentación OpenAPI automática. Está basado en **Starlette** (ASGI) y **Pydantic**.

Aquí podéis encontrar bastantes conceptos teóricos que podéis usar para apoyaros para la comprensión del desarrollo de una API de IA generativa con FastAPI.

---

## 1) Características principales

1. **Alto rendimiento** (Starlette + Pydantic).
2. **Documentación automática** (Swagger UI y ReDoc).
3. **Validación de datos** con modelos Pydantic.
4. **Tipos de Python modernos** (`str`, `int`, `BaseModel`…).
5. Soporte **async** / `await` para programación asíncrona.

Docs oficiales: [fastapi.tiangolo.com](https://fastapi.tiangolo.com/) · Uvicorn: [uvicorn.org](https://www.uvicorn.org/)

---

## 2) Instalación

```bash
pip install fastapi "uvicorn[standard]"
```

| Paquete | Rol |
|---------|-----|
| `fastapi` | Framework de la API |
| `uvicorn` | Servidor ASGI que ejecuta la app |

---

## 3) App mínima

```python
from fastapi import FastAPI

app = FastAPI(title="Demo IA")

@app.get("/")
def read_root():
    return {"message": "¡Hola, FastAPI!"}

@app.get("/health")
def health():
    return {"status": "ok"}

# GET http://127.0.0.1:8000/items/42?q=example
@app.get("/items/{item_id}")
def read_item(item_id: int, q: str | None = None):
    return {"item_id": item_id, "query": q}
```

### Arrancar

```bash
uvicorn app:app --reload --port 8000
```

| Parte | Significado |
|-------|-------------|
| `app:app` | fichero `app.py`, variable `app` |
| `--reload` | reinicia al guardar (solo desarrollo) |
| puerto `8000` | base `http://127.0.0.1:8000` |

### Documentación interactiva

| UI | URL |
|----|-----|
| **Swagger** | `http://127.0.0.1:8000/docs` |
| **ReDoc** | `http://127.0.0.1:8000/redoc` |

Swagger es vuestro primer cliente de pruebas: no hace falta front.

---

## 4) Primer contrato con Pydantic. Validación de datos recibidos en la request

En el siguie ejemplo vemos cómo se valida el JSON del body contra el modelo Pydantic `Item`, que tiene tres campos: `name`, `price` e `is_offer`. Si no se cumple la validación, FastAPI responderá con un código de estado 422.

```json
{
    "name": "Laptop",
    "price": 1200.99,
    "is_offer": true
}
```


```python
from fastapi import FastAPI
from pydantic import BaseModel

app = FastAPI()

class Item(BaseModel):
    name: str
    price: float
    is_offer: bool | None = None

@app.post("/items/")
def create_item(item: Item):
    return {"item": item}
```

FastAPI valida el JSON del body contra `Item`. Si falla → **422** automático.
---

## 5) Métodos HTTP en FastAPI

| Decorador | Uso típico |
|-----------|------------|
| `@app.get()` | Lectura (`/health`, listados) |
| `@app.post()` | Crear / lanzar acción (`/ask`) |
| `@app.put()` | Sustituir recurso |
| `@app.patch()` | Actualizar parcial |
| `@app.delete()` | Borrar |

```python
@app.put("/items/{item_id}")
def update_item(item_id: int, item: Item):
    return {"item_id": item_id, "item": item}
```

---

## 6) Middleware (concepto + ejemplos)

Un **middleware** intercepta peticiones y respuestas **antes/después** de las rutas. Sirve para CORS, logs, auth global, compresión, etc.

### CORS (muy habitual con front)

```python
from fastapi.middleware.cors import CORSMiddleware

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # en serio: restringid orígenes
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
```

### Logging de latencia

El logging de la latencia es útil para monitorizar el rendimiento de la API. Es importante tener en cuenta que el logging de la latencia puede afectar al rendimiento de la API si se hace de forma excesiva. Es una buena práctica hacer logging de la latencia de forma selectiva, por ejemplo, solo en endpoints críticos o solo en modo de desarrollo.

```python
import time
from starlette.middleware.base import BaseHTTPMiddleware

class LoggingMiddleware(BaseHTTPMiddleware):
    async def dispatch(self, request, call_next):
        start = time.time()
        response = await call_next(request)
        print(f"{request.method} {request.url} {time.time() - start:.3f}s")
        return response

app.add_middleware(LoggingMiddleware)
```

### Auth por header (idea; JWT serio → más adelante)

Es importante tener en cuenta que la autenticación por header es una buena práctica para proteger nuestras APIs. Sin embargo, en un entorno de producción, es recomendable usar un sistema de autenticación más robusto, como JWT.

```python
from fastapi import HTTPException
from starlette.middleware.base import BaseHTTPMiddleware

class AuthMiddleware(BaseHTTPMiddleware):
    async def dispatch(self, request, call_next):
        # Ejemplo didáctico — no uses un token fijo en producción
        if request.url.path in ("/health", "/docs", "/openapi.json", "/redoc"):
            return await call_next(request)
        token = request.headers.get("Authorization")
        if token != "Bearer mysecrettoken":
            raise HTTPException(status_code=401, detail="No autorizado")
        return await call_next(request)
```

### GZip (opcional)

Gzip sirve para comprimir la respuesta de la API para reducir el tamaño del payload y mejorar el rendimiento. Esto no es obligatorio, pero es una buena práctica para mejorar el rendimiento de la API en producción.

```python
from starlette.middleware.gzip import GZipMiddleware

app.add_middleware(GZipMiddleware, minimum_size=1000)
```

---

## 7) Manejo de errores

El manejo de errores es importante para proporcionar una buena experiencia al usuario y para poder depurar la API. Es importante tener en cuenta que el manejo de errores debe ser consistente y debe proporcionar una respuesta clara y útil al usuario.

### `HTTPException`

```python
from fastapi import FastAPI, HTTPException

app = FastAPI()

@app.get("/items/{item_id}")
def read_item(item_id: int):
    if item_id == 0:
        raise HTTPException(status_code=404, detail="Item no encontrado")
    return {"item_id": item_id}
```

### Validación automática → 422

Si el body no cumple el modelo Pydantic, FastAPI responde **422** sin que escribáis el `if`.

### Handler personalizado (estudio)

Cuando queremos personalizar la respuesta de errores, podemos hacerlo creando un handler personalizado para el `RequestValidationError`. Este handler se encargará de devolver una respuesta JSON con el mensaje de error y el detalle de los errores de validación.

```python
from fastapi import Request
from fastapi.exceptions import RequestValidationError
from fastapi.responses import JSONResponse

@app.exception_handler(RequestValidationError)
async def validation_exception_handler(request: Request, exc: RequestValidationError):
    return JSONResponse(
        status_code=422,
        content={"message": "Error de validación", "details": exc.errors()},
    )
```

### Buenas prácticas

1. Códigos HTTP adecuados (400, 404, 422, 500…).
2. Mensajes claros al cliente.
3. **No** filtrar API keys ni tracebacks completos.
4. Registrar el detalle en logs del servidor (S16 profundiza).

---

## 8) Mini CRUD resumen de todos los conceptos HTTP y FastAPI vistos hasta ahora

Útil para consolidar rutas + Pydantic. Puedes probar a reproducirlo en tu entorno local para asegurarte de que lo has entendido bien.

```python
from typing import List

from fastapi import FastAPI, HTTPException
from pydantic import BaseModel

app = FastAPI(title="CRUD estudio")

class Item(BaseModel):
    id: int
    name: str
    description: str | None = None
    price: float
    on_offer: bool = False

items_db: List[Item] = [
    Item(id=1, name="Laptop", description="Potente", price=1200.99, on_offer=True),
    Item(id=2, name="Phone", price=899.99, on_offer=False),
]

@app.get("/items", response_model=List[Item])
def list_items():
    return items_db

@app.get("/items/{item_id}", response_model=Item)
def get_item(item_id: int):
    for item in items_db:
        if item.id == item_id:
            return item
    raise HTTPException(status_code=404, detail="No encontrado")

@app.post("/items", response_model=Item, status_code=201)
def create_item(item: Item):
    if any(i.id == item.id for i in items_db):
        raise HTTPException(status_code=409, detail="Ya existe")
    items_db.append(item)
    return item

@app.delete("/items/{item_id}", status_code=204)
def delete_item(item_id: int):
    for i, item in enumerate(items_db):
        if item.id == item_id:
            del items_db[i]
            return
    raise HTTPException(status_code=404, detail="No encontrado")
```

---

## 9) Puente al sistema de IA

En este ejemplo vemos cómo se define el endpoint `/ask` que es el encargado de procesar la pregunta del usuario y devolver la respuesta. El endpoint `/ask` recibe un body de tipo `AskIn` y devuelve un body de tipo `AskOut`.

```python
# Conceptual — se cablea de verdad en el Bloque 2
@app.post("/ask")
def ask(body: AskIn) -> AskOut:
    out = procesar_turno(body.pregunta)  # misma lógica que CLI/Streamlit
    return AskOut(respuesta=out["respuesta"], thread_id=body.thread_id or "default")
```

La API es el adaptador; el cerebro sigue siendo `procesar_turno` / `responder`.

---

## Resumen

- `FastAPI()` + decoradores + `uvicorn` + `/docs`.
- Pydantic valida; middlewares envuelven; `HTTPException` comunica errores.
- Conviene tener claro cómo funcionan los distintos métodos HTTP y cómo se pueden usar para construir una API RESTful con FastAPI. Revisar las demos de la unidad para ver ejemplos de uso.
