![Cabecera](../../assets/cabecera_rag.png)

# Introducción: interfaces y aplicaciones

Hasta ahora el trabajo del módulo vive en **consola** y notebooks. Este bloque añade una **capa de exposición**: cómo hacer que un sistema ya construido (modelo ML, pipeline RAG, agente, script de negocio…) sea usable por otras personas o por otros sistemas.

> La lógica de negocio **no se reescribe**; cambia cómo entra la petición y cómo se muestra o se consume la salida.

---

## Objetivos del bloque

Al terminar, deberías poder:

- Explicar las vías habituales para exponer un sistema: **interfaz de usuario** o una **API**.
- Montar una app **Streamlit** mínima (MVP) sobre una función ya existente.
- Conectar esa UI a un software previamente creado.
- Mostrar resultado, trazas útiles y errores básicos.
- Entender que existen diferentes opciones para exponer un sistema: Frontend, Backend (API) y Cliente a medida.

---

## Desarrollo de interfaces y APIs para exponer un tu software: MVP

Hasta el momento, nos hemos dedicado a desarrollar un sistema backend Python que **ya funciona** en terminal o notebook, pero que solo puede usar quien conoce el repo. Falta **demostrabilidad** e **integración**:

```text
Antes                          Ahora
─────                          ────
python main.py --ask "…"       Usuario abre la app en el navegador
Solo tú lo usas                Otras personas pueden probarlo
Salida en terminal o notebook  Resultado + estado + errores visibles en una interfaz o un cliente REST
```

Eso cambia la percepción: de «scripts sueltos» a **producto mínimo viable** (MVP).

El caso de uso de este sprint es un **RAG**, pero el patrón sirve igual para un clasificador, un agente o cualquier función Python que recibas una entrada y devuelva un resultado estructurado.

---

## Vías para exponer un sistema

De forma esquemática:

| Vía | Tecnología | Cuándo encaja |
|-----|--------|----------------|
| **Interfaz de prototipo (Python)** | Streamlit, Gradio… | MVP, Demos para clientes, herramientas internas de empresa, bootcamp, POC |
| **API** | FastAPI, Flask… | Otros sistemas o frontends consumen HTTP |
| **Cliente a medida** | Web (HTML/CSS/JS), React, Angular, Kotlin, Swift... | Producto con UX propia para desarrollar productos empresariales; suele ir **detrás** de una API |

Las tres no se excluyen: muchas veces la API es el contrato estable y la UI (Streamlit o un front) es un cliente más.

### Qué hacemos en este curso

- El foco es **interfaces / MVP** con **Streamlit** para desarrollar una **interfaz + conexión limpia + UX mínima**.
- **No** es el foco construir un frontend a medida con HTML, CSS y JavaScript.
- Más adelante verás cómo desarrollar una API RESTful con FastAPI y otras opciones.
- También veremos cómo la misma UI puede apuntar a otro backend (p. ej. un agente).

---

## Diagrama esquemático de la arquitectura de la aplicación con Streamlit + RAG

```text
Usuario
   ↓
Streamlit (app.py)
   ↓
logic.responder(pregunta)     ← misma función que la CLI
   ↓
Retriever → Contexto → Prompt → Gemini
   ↓
Respuesta + fuentes (+ contexto debug)
```

No hay un segundo pipeline dentro de Streamlit. Solo hay **una** función de entrada. Si hemos estructurado bien los módulos del proyecto, será más sencillo conectar la UI a la función de entrada.

## Resumen

- Exponer un sistema = UI y/o API; la lógica se reutiliza.
- En el bootcamp: MVP con Streamlit; el RAG del sprint será nuestro ejemplo.
