![Cabecera](../../assets/cabecera_rag.png)

# Generación con Gemini y alternativas

## Objetivos

- Generar respuestas con un LLM
- Entender que el **proveedor del LLM** puede cambiar sin rehacer retrieval.
- Conocer una **alternativa con Hugging Face** a nivel conceptual.

---

## 1) Camino principal: Gemini

- Necesitamos nuestra API key de Gemini (`GEMINI_API_KEY`).
- Modelo generativo. p. ej. `gemini-2.0-flash`
- Temperatura baja (`GENERATION_TEMPERATURE ≈ 0.2`) para respuestas más fieles al contexto.

En el módulo python que se encarga de generar la respuesta con el LLM (por ejemplo `generate.py`), podríamos tener algo como:

```python
from google import genai

def generar_respuesta(prompt: str) -> str:
    configurar_gemini_api_key()
    client = genai.Client()
    response = client.models.generate_content(
        model=GEMINI_MODEL,
        contents=prompt,
        config={"temperature": GENERATION_TEMPERATURE},
    )
    return (response.text or "").strip()
```

Nota: el modelo de **embedding** (`gemini-embedding-2`) y el de **generación** (`gemini-2.0-flash`) son distintos. No los mezcles en la misma variable de config. 

Diferencias entre un modelo de Embedding y un modelo de generación LLM:

| Diferencias Clave | Propósito principal | Cómo funcionan | Salida del modelo |
|------------------|---------------------|----------------|------------------|
| Embedding        | Convierte palabras o textos en listas de números (vectores) para medir qué tan parecidos son. | Mide la cercanía de los significados en un espacio matemático. | Da una serie de números (un vector). |
| LLM              | Lee texto, entiende el contexto y genera respuestas nuevas o texto coherente. | Predice y escribe la siguiente palabra o frase basándose en patrones gigantescos. | Da texto completo o una respuesta conversacional. |

El de embedding suele ser un modelo más pequeño y rápido, mientras que el de generación suele ser un modelo más grande y potente.

---

## 2) Misma arquitectura, otro backend

```text
contexto + pregunta  →  build_rag_prompt()  →  generar_respuesta()
                                                      ↓
                                              Gemini  |  Hugging Face
```

Lo intercambiable es la **función de generación**, no el retriever ni Chroma. Si mañana cambias el LLM, `logic.responder()` sigue siendo:

```text
validar → recuperar → formatear → prompt → generar
```

Solo cambia la implementación de `generar`. Estamos  **cambiando el LLM**, pero el proceso de recuperación de contexto y el prompt siguen siendo los mismos.

---

## 3) Alternativa: Hugging Face

Como en embeddings (Sprint 8), HF sirve para **comparar enfoques**, no para sustituir el camino principal del sprint.

| Modo | Idea | Cuándo |
|------|------|--------|
| **Nube** (Inference API) | Envías el prompt a un modelo hospedado en HF (`HF_TOKEN`) | Probar otro LLM sin instalar pesos |
| **Local** (`transformers`) | Cargas un modelo en tu máquina | Offline / demos sin cuota de API |

Ejemplo conceptual (nube, esqueleto):

```python
# Alternativa ilustrativa — no es el camino principal del proyecto
from huggingface_hub import InferenceClient

client = InferenceClient(token=os.environ["HF_TOKEN"])
texto = client.text_generation(
    prompt,
    model="mistralai/Mistral-7B-Instruct-v0.2",  # ejemplo
    max_new_tokens=512,
)
```

En local, con `transformers` / pipelines de chat, el patrón es el mismo: **mismo prompt RAG**, distinta llamada.

### Reglas si experimentas con HF

- No mezcles el índice Gemini con embeddings HF en el mismo índice sin re-indexar (eso es tema de embeddings, no de generación).
- Para **generación**, el índice puede seguir siendo Gemini: solo cambia el LLM final.
- Marca claramente en el notebook qué celdas son «alternativa opcional».

---

## Resumen

- Hemos visto que podemos usar diferentes LLMs para generar la respuesta final de nuestros RAGs.
- Lo importante no es el logo del proveedor: es **retrieval + prompt + generación** con un contrato claro (`generar_respuesta(prompt)`).
- Temperatura baja ayuda al grounding.
- HF es alternativa de la capa de generación.


