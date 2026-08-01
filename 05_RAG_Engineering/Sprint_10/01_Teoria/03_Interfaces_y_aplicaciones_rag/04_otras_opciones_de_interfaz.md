![Cabecera](../../assets/cabecera_rag.png)

# Opciones de mercado: interfaces web, móviles y APIs

## Objetivos

- Distinguir **cliente** (web, móvil…) de **API** (contrato HTTP).
- Conocer opciones habituales del mercado en interfaces web, apps móviles y APIs.
- Situar **Streamlit** (interfaces MVP) y **FastAPI** (APIs) como las opciones del bootcamp dentro del panorama de mercado.

---

## 1) Clientes y API

```text
Usuario
   ├── Interfaz web
   ├── App móvil
   └── Otro sistema
            ↓
         API (HTTP)   ← a menudo el contrato estable
            ↓
     lógica de negocio (p. ej. responder())
```


Para un MVP suele bastar la interfaz (Streamlit llama directo a Python). En un **producto**, lo habitual es: API estable + uno o varios clientes (web, móvil, otro servicio).

| Capa | Pregunta que responde | Ejemplos |
|------|----------------------|----------|
| **Interfaz web** | ¿Cómo interactúa una persona desde el navegador? | Streamlit, Gradio, React, Vue… |
| **App móvil** | ¿Cómo interactúa desde el teléfono/tablet? | Swift/Kotlin nativo, Flutter, React Native… |
| **API** | ¿Cómo lo consumen esos clientes u otros programas? | FastAPI, Flask, Django REST, Express… |


---

## 2) Opciones para desarrollar interfaces web

### A) Prototipo / MVP en Python (sin front a medida)

Ideal para demos, herramientas internas y POC: escribes widgets en Python y la librería genera la UI.

| Opción | Encaje típico | Docs / tutoriales |
|--------|---------------|-------------------|
| **Streamlit** | Demos rápidas, dashboards, chat/LLM, bootcamp | [Docs](https://docs.streamlit.io/) · [Tutoriales](https://docs.streamlit.io/develop/tutorials) · [Chat LLM](https://docs.streamlit.io/develop/tutorials/chat-and-llm-apps/build-conversational-apps) |
| **Gradio** | Demos de modelos ML, ecosistema Hugging Face | [Docs](https://www.gradio.app/docs/) · [Quickstart](https://www.gradio.app/guides/quickstart) · [Chatbot](https://www.gradio.app/guides/creating-a-chatbot-fast) |
| **Dash** (Plotly) | Apps analíticas / visualización | [Docs](https://dash.plotly.com/) · [Tutorial](https://dash.plotly.com/tutorial) |
| **Panel** / **NiceGUI** | Dashboards o UIs Python más flexibles | [Panel](https://panel.holoviz.org/) · [NiceGUI](https://nicegui.io/) |

En este sprint implementamos **Streamlit**. Gradio es la alternativa más cercana en espíritu.

### B) Frontend web «de producto»

HTML/CSS/JS (o un framework) + suele consumir una **API**. Más control de UX, más stack y equipo. Requiere un desarrollo a medida. 

| Opción | Encaje típico | Docs / tutoriales |
|--------|---------------|-------------------|
| **HTML + CSS + JS** | Bases de la web; páginas simples | [MDN Web Docs](https://developer.mozilla.org/es/docs/Learn_web_development) |
| **React** | SPAs y productos a escala; ecosistema grande | [react.dev](https://react.dev/) · [Learn React](https://react.dev/learn) |
| **Next.js** | React + routing, SSR/SSG, apps full-stack | [nextjs.org/docs](https://nextjs.org/docs) · [Learn](https://nextjs.org/learn) |
| **Vue** | SPAs con curva más suave para muchos equipos | [vuejs.org](https://vuejs.org/) · [Tutorial](https://vuejs.org/tutorial/) |
| **Angular** | Apps empresariales grandes, opinión fuerte del framework | [angular.dev](https://angular.dev/) · [Tutorials](https://angular.dev/tutorials) |
| **Svelte / SvelteKit** | UI reactiva con menos boilerplate | [svelte.dev](https://svelte.dev/) · [Tutorial](https://svelte.dev/tutorial) |

**No** es el foco de este módulo construir un front a medida; sí conviene saber que existen y que, en producción, suelen ir **detrás de una API**.

---

## 3) Opciones para desarrollar aplicaciones móviles

El móvil es **otro cliente** de la misma API: no reescribe el RAG; llama a endpoints (`POST /ask`, etc.) y muestra la respuesta.

### Nativo (una app por plataforma)

| Opción | Plataforma | Encaje típico | Docs / tutoriales |
|--------|------------|---------------|-------------------|
| **Swift + SwiftUI** | iOS / iPadOS | App nativa Apple; mejor integración con el ecosistema | [SwiftUI](https://developer.apple.com/xcode/swiftui/) · [Tutorials](https://developer.apple.com/tutorials/swiftui) |
| **Kotlin + Jetpack Compose** | Android | App nativa Android moderna | [Compose](https://developer.android.com/compose) · [Curso Android](https://developer.android.com/courses) |

### Multiplataforma (un código → iOS y Android)

| Opción | Encaje típico | Docs / tutoriales |
|--------|---------------|-------------------|
| **Flutter** (Dart) | UI rica multiplataforma; muy usado en producto | [flutter.dev](https://flutter.dev/) · [Get started](https://docs.flutter.dev/get-started/install) · [Codelabs](https://docs.flutter.dev/codelabs) |
| **React Native** | Equipos que ya saben React; código JS/TS compartido | [reactnative.dev](https://reactnative.dev/) · [Intro](https://reactnative.dev/docs/getting-started) |
| **.NET MAUI** | Stack Microsoft; C# compartido | [MAUI docs](https://learn.microsoft.com/dotnet/maui/) · [Tutorial](https://learn.microsoft.com/dotnet/maui/get-started/first-app) |
| **Kotlin Multiplatform** | Lógica compartida en Kotlin; UI nativa o Compose Multiplatform | [KMP](https://kotlinlang.org/docs/multiplatform.html) |

---

## 4) Opciones para desarrollar una API

Una API expone endpoints HTTP (`GET`, `POST`…) que llaman a la misma lógica de negocio. Cualquier cliente (web, móvil, otro backend, Postman) puede consumirla.

### En Python tenemos estas opciones

| Opción | Encaje típico | Docs / tutoriales |
|--------|---------------|-------------------|
| **FastAPI** ✅ | Camino del bootcamp: tipado, OpenAPI/Swagger; muy usado con ML/LLM | [Docs](https://fastapi.tiangolo.com/) · [Tutorial](https://fastapi.tiangolo.com/tutorial/) · [Request body](https://fastapi.tiangolo.com/tutorial/body/) |
| **Flask** | APIs y microservicios ligeros; ecosistema maduro | [flask.palletsprojects.com](https://flask.palletsprojects.com/) · [Quickstart](https://flask.palletsprojects.com/en/stable/quickstart/) |
| **Django + Django REST Framework** | Apps completas (admin, ORM, auth) + API REST | [Django](https://docs.djangoproject.com/) · [DRF](https://www.django-rest-framework.org/) · [Tutorial DRF](https://www.django-rest-framework.org/tutorial/1-serialization/) |
| **Litestar** / **Starlette** | ASGI de alto rendimiento (familia cercana a FastAPI) | [Litestar](https://litestar.dev/) · [Starlette](https://www.starlette.io/) |

Idea mínima con FastAPI (misma `responder()` que la CLI o Streamlit):

```python
# Conceptual — no se implementa en este sprint
from fastapi import FastAPI
from pydantic import BaseModel

app = FastAPI()

class Pregunta(BaseModel):
    pregunta: str

@app.post("/ask")
def ask(body: Pregunta):
    return responder(body.pregunta)
```

Al arrancar la API, la documentación interactiva suele estar en `http://127.0.0.1:8000/docs` (Swagger).

### Fuera de Python (panorama)

| Opción | Lenguaje | Docs |
|--------|----------|------|
| **Express** | Node.js | [expressjs.com](https://expressjs.com/) |
| **NestJS** | Node.js (estructura tipo Angular) | [docs.nestjs.com](https://docs.nestjs.com/) |
| **Spring Boot** | Java | [spring.io/projects/spring-boot](https://spring.io/projects/spring-boot) |
| **ASP.NET Core** | C# / .NET | [learn.microsoft.com — ASP.NET Core](https://learn.microsoft.com/aspnet/core/) |

---

## 5) Cómo se combinan en la práctica

| Escenario | Cliente(s) | API | Cuándo |
|-----------|------------|-----|--------|
| Este sprint (MVP RAG) | Streamlit | No hace falta: llama a `responder()` en Python | Demo / POC en clase |
| APIs | Postman, curl, otro servicio o un front | **FastAPI** | Exponer el sistema por HTTP |
| Producto web | React / Next / Vue… | FastAPI (u otra del mercado) | UX propia en navegador |
| Producto móvil | Flutter / RN / nativo | FastAPI (misma API) | App en tiendas o PWA |
| Web + móvil | Front web **y** app | FastAPI (un backend, varios clientes) | Producto multiplataforma |
| Solo integración | — | FastAPI + otro servicio | Backends que hablan entre sí |

En el bootcamp, la vía elegida para APIs es **FastAPI**, que veremos más adelante

La regla del bloque no cambia: **el cliente (web o móvil) o la API no reimplementan el RAG**; llaman a `responder()` (u otro contrato limpio).

---

## 6) Por qué Streamlit en este sprint

- Encaja con el stack Python del bootcamp.
- Pocas líneas hasta una URL usable en local.
- Suficiente para enseñar **UI vs lógica**.
- Objetivo de este sprint: MVP demostrable con interfaz; las APIs con **FastAPI** se ven en el bootcamp como capa aparte.

Streamlit no es «la única opción del mercado»: es la **decisión pedagógica** para interfaces en este bloque. Para APIs, la decisión pedagógica del bootcamp es **FastAPI**, que veremos más adelante.

---

## 7) Evolución del backend (Sprint 11+)

```text
Sprint 10                     Sprint 11+
─────────                     ──────────
Streamlit / FastAPI           Misma UI / app / mismos endpoints
   ↓                             ↓
logic.responder()             Agente (u otro orquestador)
   ↓                             ↓
RAG directo                   Tools (RAG, búsqueda, APIs…)
```

El cliente o la API no tienen por qué rehacerse: cambia **quién** orquesta la lógica por detrás.

---

## Resumen

- **Web**, **móvil** y **API** son capas/clientes distintos; a menudo se combinan alrededor de un mismo contrato HTTP.
- En el bootcamp: **Streamlit** para MVP de interfaz; **FastAPI** para APIs.
- En el mercado hay más opciones (Gradio, React, Flutter, Flask, Express…); el contrato limpio (`responder()`) permite cambiar de cliente o añadir API sin reescribir el pipeline.
