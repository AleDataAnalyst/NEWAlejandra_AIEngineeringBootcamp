![Cabecera](../../../../06_AI_Agents_Engineering/Sprint_11/assets/cabecera_thebridge.png)

# Qué es una API para IA Generativa

Este documento mezcla **fundamentos de backend** (HTTP, REST, CRUD) con el uso que les damos en un **sistema de IA**. Anteriormente ya vimos los conceptos de cliente y servidor, peticiones y respuestas, y códigos de estado HTTP. Ahora vamos a profundizar en estos conceptos y ver cómo se aplican en un sistema de IA. El objetivo es desarrollar nuestras propias APIs para sistemas de IA.

---

## 1) Cliente y servidor

Internet, en lo esencial, es una **red de redes**. En la base:

- tu programa (o el navegador) actúa como **cliente**,
- otro ordenador actúa como **servidor**,
- se establece un diálogo por pasos: **petición** y **respuesta**.

```text
Cliente                          Servidor
   |                                |
   |----- petición HTTP ----------->|
   |                                |  (ejecuta lógica)
   |<---- respuesta HTTP -----------|
```

En este sprint el **servidor** es vuestra app FastAPI; el **cliente** puede ser Swagger, `curl`, Streamlit, Postman u otro servicio.

**Para ampliar (opcionales):**

- [How the Internet Works in 5 Minutes](https://www.youtube.com/watch?v=7_LPdttKXPc)
- [How Does the Internet Actually Work?](https://www.youtube.com/watch?v=bjrDGZvpkDI)

---

## 2) Protocolo HTTP

HTTP define cómo se formulan peticiones y respuestas.

### Partes típicas de una petición

- **Método:** GET, POST, PUT, DELETE…
- **URL / path:** `/ask`, `/health`, `/v1/books/3`
- **Headers:** tipo de contenido, autorización, etc.
- **Body (opcional):** JSON en POST/PUT

### Partes típicas de una respuesta

- **Código de estado** (200, 404, 422…)
- **Headers**
- **Body:** casi siempre JSON en nuestras APIs

Especificación clásica: [RFC 2616 §10](https://tools.ietf.org/html/rfc2616#section-10) · [Códigos HTTP (Wikipedia)](https://es.wikipedia.org/wiki/Anexo:C%C3%B3digos_de_estado_HTTP)

### Familias de códigos

| Familia | Significado | Ejemplos en este sprint |
|---------|-------------|-------------------------|
| **1xx** | Informativas | Raras en APIs JSON |
| **2xx** | OK | 200 respuesta, 201 creado |
| **3xx** | Redirección | Poco típicas aquí |
| **4xx** | Error del cliente | 400, 404, 422 validación |
| **5xx** | Error del servidor | 500, 502, 503 |

HTTPS (HTTP + TLS) cifra el canal. En local usaréis `http://127.0.0.1`; en la nube (S15) el PaaS suele dar HTTPS.

---

## 3) ¿Qué es una API?

> Una **API** (Application Programming Interface) es un conjunto de reglas que permite a un programa usar funciones de otro sin conocer su implementación interna.

En la web, una **API HTTP** expone **endpoints**: URLs + métodos que aceptan y devuelven datos (casi siempre JSON).

Para GenAI el patrón típico es:

```text
Cliente
  POST /ask  { "pregunta": "...", "thread_id": "..." }
       ↓
  FastAPI valida el body (Pydantic)
       ↓
  Llama a responder() / procesar_turno()
       ↓
  Devuelve { "respuesta": "...", "thread_id": "...", "done": false }
```

### Conceptos clave de una API

| Concepto | Qué es |
|-------|--------|
| **Endpoint** | Ruta + método (`GET /health`, `POST /ask`). |
| **Request** | Lo que envía el cliente. |
| **Response** | Status + JSON (u otro cuerpo). |
| **OpenAPI / Swagger** | Documentación generada del contrato. |

---

## 4) CRUD

**CRUD** = Create, Read, Update, Delete: operaciones básicas sobre un recurso.

| Operación | Método HTTP | Códigos habituales |
|-----------|-------------|--------------------|
| Create | **POST** | 201 (o 200), 409 si ya existe |
| Read | **GET** | 200, 404 |
| Update | **PUT** / **PATCH** | 200, 404 |
| Delete | **DELETE** | 200 / 204, 404 |

Ejemplo clásico (películas / usuarios):

```text
GET    /users
GET    /users/123
POST   /users
PUT    /users/123
DELETE /users/123
```

En GenAI el “recurso” principal no es un libro: es una **pregunta/turno**. Por eso el endpoint más usado para nuestras apps probablemente será `POST /ask`. Aun así, el vocabulario CRUD os sirve para historial (`GET /threads/{id}/messages`) y para entender APIs ajenas.

---

## 5) REST (idea práctica)

**REST** (Representational State Transfer) es un estilo de diseño sobre HTTP:

- recursos identificados por URLs,
- operaciones con métodos HTTP,
- respuestas con representación (JSON),
- sin “sesión mágica” en el servidor para cada clic (el cliente manda lo necesario; en nuestro caso, `thread_id` si hay hilos).

Más lectura (opcional):

- [Guía HTTP y REST](https://code.tutsplus.com/es/tutorials/a-beginners-guide-to-http-and-rest--net-16340)
- [Métodos HTTP en APIs REST](https://restfulapi.net/http-methods/)

### Ejemplos de URLs REST

```text
GET  /users
GET  /users?size=20&page=5
GET  /users/123
POST /users
PUT  /users/123
DELETE /users/123
```

En el bootcamp:

```text
GET  /health
POST /ask
GET  /threads/{thread_id}/messages
```

---

## 6) CORS

**CORS** (Cross-Origin Resource Sharing) controla si un navegador en el dominio A puede llamar a una API en el dominio B.

- En Swagger/`curl` en local casi no lo notáis.
- Cuando Streamlit (u otro front) llame a la API desde otro origen, puede hacer falta `CORSMiddleware`.

Referencia: [MDN — CORS](https://developer.mozilla.org/es/docs/Web/HTTP/CORS)

---

## 7) Por qué sirve en GenAI

- El mismo backend sirve a **varios clientes** (Streamlit, web, tests, otro microservicio).
- Podéis poner **límites** en la puerta (tamaño de body, timeouts).
- Más adelante desplegáis **un** servicio, no “abre este notebook”.
- El contrato (`AskIn` / `AskOut`) documenta qué espera el sistema de IA.

## Lo que nuestra API no es aún

- No es un front HTML.
- No es auth completa (JWT/OAuth).
- No es el sitio para pegar el prompt: el prompt vive en la **lógica**.

---

## 8) APIs públicas para practicar (lectura / curl)

Útiles para practicar GET/JSON **sin** montar servidor:

| API | URL |
|-----|-----|
| JSONPlaceholder | https://jsonplaceholder.typicode.com/guide/ |
| PokéAPI | https://pokeapi.co/ |
| Open-Meteo / clima | (varias; también usáis APIs en agents) |
| Datos abiertos Madrid | https://datos.madrid.es/ |

Listados: [public-apis](https://github.com/public-apis/public-apis)

En el bootcamp ya consumís APIs como **tools** del agente; ahora **vosotros** publicáis una.

---

## Resumen

- Cliente ↔ servidor vía HTTP; códigos 2xx/4xx/5xx.
- API REST = recursos + métodos + JSON.
- CRUD es el vocabulario; en GenAI el verbo estrella es **preguntar** (`POST /ask`).
- Siguiente doc: montarlo con **FastAPI**.
