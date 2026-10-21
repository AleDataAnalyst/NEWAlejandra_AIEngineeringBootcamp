![Cabecera](../../../../06_AI_Agents_Engineering/Sprint_11/assets/cabecera_thebridge.png)

# Health, errores y variables de entorno

Tres piezas que convierten un demo en un servicio usable en clase y, más adelante, en la nube.

---

## 1) `GET /health`

Este endpoint sirve para comprobar si la API está funcionando correctamente.

```python
@app.get("/health")
def health():
    return {"status": "ok"}
```

- **No** llama al LLM.
- Más adelante lo usaremos para comprobar si la API está funcionando correctamente en producción.
- Podéis añadir metadatos no sensibles: `{"status": "ok", "storage": "sqlite"}`.

| Ruta | ¿LLM? | Uso |
|------|-------|-----|
| `GET /health` | No | Pulso del servicio |
| `POST /ask` | Sí (o stub) | Negocio |

---

## 2) Errores HTTP claros

| Situación | Status típico |
|-----------|----------------|
| Body inválido (Pydantic) | **422** (automático) |
| Pregunta vacía tras `strip` | **400** |
| Recurso no encontrado | **404** |
| Falta config / API key | **503** o **500** con mensaje seguro |
| Fallo LLM / dependencia | **502** / **500**; loguead el detalle en servidor |

```python
from fastapi import HTTPException

if not body.pregunta.strip():
    raise HTTPException(status_code=400, detail="pregunta vacía")
```

### No exponer secretos

Nunca devolváis en el JSON:

- `GEMINI_API_KEY`,
- connection strings con password,
- tracebacks completos al cliente público.

El detalle fino → logs del servidor (S16).

### Handler global para manejar errores

Este ejemplo muestra cómo se puede usar un handler global para manejar errores.

```python
import logging
from fastapi import Request
from fastapi.responses import JSONResponse

logger = logging.getLogger(__name__)

@app.exception_handler(Exception)
async def global_exception_handler(request: Request, exc: Exception):
    logger.error("Error en %s: %s", request.url, exc)
    return JSONResponse(
        status_code=500,
        content={"message": "Ocurrió un error inesperado"},
    )
```

---

## 3) Variables de entorno

Las variables de entorno guardan **configuración sensible** (API keys, URL de base de datos, flags) **fuera** del código fuente.

Ees importante tener en cuenta que las variables de entorno no son seguras y pueden ser accedidas por cualquier usuario del sistema. Por lo tanto, es importante protegerlas adecuadamente.

### Crear `.env`

En la raíz del proyecto:

```env
DATABASE_URL=sqlite:///historial.db
GEMINI_API_KEY=pon_tu_clave_aqui
DEBUG=True
```

En producción podéis apuntar a otro RDBMS (p. ej. Postgres) cambiando la URL:

```env
DATABASE_URL=postgresql+psycopg://user:password@localhost:5432/ia_demo
```

### Instalar y cargar

```bash
pip install python-dotenv
```

```python
from dotenv import load_dotenv
import os

load_dotenv()  # lee .env en el cwd / proyecto

database_url = os.getenv("DATABASE_URL")
api_key = os.getenv("GEMINI_API_KEY")
```

### Centralizar en `config.py` (recomendado)

```python
import os
from pathlib import Path

from dotenv import load_dotenv

load_dotenv(Path(__file__).resolve().parent / ".env")

class Settings:
    DATABASE_URL: str = os.getenv("DATABASE_URL", "sqlite:///historial.db")
    GEMINI_API_KEY: str | None = os.getenv("GEMINI_API_KEY") or None
    DEBUG: bool = os.getenv("DEBUG", "False").lower() in ("true", "1", "t")

settings = Settings()
```

Uso:

```python
from config import settings

# settings.DATABASE_URL
# settings.GEMINI_API_KEY
```

### `.gitignore` y `.env.example`

```gitignore
.env
```

Subid un **`.env.example`** sin secretos:

```env
DATABASE_URL=sqlite:///historial.db
GEMINI_API_KEY=
```

Así quien descargue vuestro proyecto pueda crear las variables de entorno necesarias.

### Para poner la aplicación en producción

En el PaaS las variables se configuran en el panel / CLI del servicio (**no** se sube el `.env` al repo). El código solo hace `os.getenv(...)`.

---

## 4) Checklist rápido antes de enseñar / entregar

- [ ] `/health` responde 200 sin LLM
- [ ] Body malo → 422
- [ ] Pregunta vacía controlada → 400
- [ ] `.env` en `.gitignore`
- [ ] `.env.example` en el repo
- [ ] Ninguna key hardcodeada en `app.py`

---

## Resumen

- `/health` = pulso; `/ask` = negocio.
- Errores con código HTTP + mensaje corto al cliente.
- Secrets solo en entorno; `config.py` + `.env.example` = higiene de proyecto.
