![Cabecera](../../assets/cabecera_gemini.png)

# Familias de modelos

Clasificamos por **qué entra** y **qué sale** — no por el nombre comercial del proveedor.

---

## Vista general (mapa mental)

```text
                    MODELOS DE IA (visión ingeniería)
                              │
        ┌─────────────────────┼─────────────────────┐
        ▼                     ▼                     ▼
   TEXTO (LLM)          EMBEDDINGS            MULTIMODAL
   genera texto          vectoriza             texto + imagen/audio…
        │                     │                     │
   chat, resumen          búsqueda              OCR, descripción
   código, JSON           semántica, RAG        foto + pregunta
```

---

## 1. Modelos de texto (LLM generativos)

| | |
|---|---|
| **Entrada** | Texto (instrucciones + contexto) |
| **Salida** | Texto (respuesta, código, JSON si lo pides) |
| **Arquitectura habitual** | **Transformer** (decoder o encoder-decoder) |

**Casos de uso de la familia:**

| Caso | Por qué encaja |
|------|----------------|
| Chatbot / asistente | Lenguaje natural bidireccional |
| Resumen o traducción | Reformular y condensar texto |
| Generación de código | Secuencias con sintaxis |
| Clasificación por prompt | Una etiqueta si acotas la salida |

**Limitación clave:** no conocen tu empresa por defecto → necesitan **contexto** (FAQ, RAG, historial).

---

## 2. Modelos de embeddings

| | |
|---|---|
| **Entrada** | Texto (frase, párrafo, chunk) |
| **Salida** | Vector numérico (lista de números) |
| **Arquitectura habitual** | Transformer encoder u otros modelos de representación |

**Casos de uso de la familia:**

| Caso | Por qué encaja |
|------|----------------|
| Búsqueda semántica | Textos parecidos → vectores cercanos |
| RAG (recuperación) | Encontrar chunks relevantes antes del LLM |
| Deduplicación | Detectar documentos casi iguales |
| Clustering de tickets | Agrupar problemas similares |

**No generan** respuestas largas: **buscan**. El LLM **redacta** después.

```text
  Pregunta del usuario
         │
         ▼
  Embedding ──────► índice vectorial ──────► top-K chunks
         │
         ▼
  LLM de texto (Transformer) con contexto recuperado
```

---

## 3. Modelos multimodales

| | |
|---|---|
| **Entrada** | Texto + imagen / audio / vídeo (según modelo) |
| **Salida** | Texto (descripción, respuesta, extracción) |
| **Arquitectura habitual** | **Transformer** multimodal |

**Casos de uso de la familia:**

| Caso | Por qué encaja |
|------|----------------|
| OCR + interpretación | Leer captura y explicar contenido |
| “¿Qué hay en esta foto?” | Descripción o detección en lenguaje natural |
| Diagrama + pregunta | Entender imagen y texto juntos |
| Accesibilidad | Alt-text automático |

**Alternativa:** pipeline **CNN/OCR clásico + LLM de texto** — a veces más barato que un multimodal único.

---

## 4. Tabla problema → familia (criterio rápido)

| Problema | Familia principal | Nota |
|----------|-------------------|------|
| Chatbot | Texto (LLM) | + contexto / RAG si hace falta |
| Búsqueda semántica | Embeddings | Casi nunca solo LLM |
| Clasificación de imágenes | Visión (CNN / ViT) | No uses un LLM de texto puro |
| OCR multimodal | Multimodal | O OCR + texto en dos pasos |
| Solo etiquetar emails | Texto (LLM) o ML clásico | LLM si pocas clases y poco dato |
| Recomendación por similitud | Embeddings | Vectores de productos/usuarios |

---

## 5. Generalista vs especializado (dentro de una familia)

| Generalista | Especializado |
|-------------|---------------|
| Un LLM para muchas tareas | Modelo entrenado/afinado para un dominio |
| Rápido de prototipar | Mejor si la tarea es repetitiva y medible |
| Depende del contexto que le des | Depende de datos y evaluación propios |

---

## 6. Modelo abierto vs cerrado. Dependiendo de dónde se ejecute

| | Abierto (pesos publicados) | Cerrado (API) |
|---|---------------------------|---------------|
| **Dónde corre** | Tu servidor / cloud elegido | Infra del proveedor |
| **Arranque** | Más lento (ops, GPU) | Rápido (API key) |
| **Privacidad** | Alta si on-prem | Según contrato |
| **Quién lo usa** | Equipos con infra | La mayoría de MVPs y productos |

Dependiendo de la situación y costes, las empresas usan **API en producción** y **abierto** para experimentar o en local para evitar costes.
