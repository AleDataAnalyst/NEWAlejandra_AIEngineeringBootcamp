![Cabecera](../../assets/cabecera_rag.png)

# Embeddings con Gemini

En este bootcamp el hilo principal de embeddings es **Google Gemini** vía el SDK `google-genai`, el mismo ecosistema que ya usaste para generación en Sprints 4–7.

---

## Objetivos

- Llamar a `client.models.embed_content` con tu API key.
- Embeddear **un texto** y una **lista de chunks**.
- Configurar el **modelo** y entender las **dimensiones** de salida.
- Integrar la llamada en el módulo `embed.py` del proyecto.

---

## 1) Modelo y configuración

En `config.py` del proyecto:

```python
EMBEDDING_MODEL = "text-embedding-004"
```

Consulta [Google AI Studio](https://aistudio.google.com/) por modelos de embedding disponibles en tu cuenta. Nombres habituales:

| Modelo | Notas |
|--------|-------|
| `text-embedding-004` | Texto; ampliamente usado en ejemplos recientes |
| `gemini-embedding-001` | Alternativa estable de la familia Gemini |

**Importante:** si cambias de modelo, debes **re-generar todos los embeddings** antes de indexar de nuevo.

---

## 2) Autenticación

Mismo patrón que en S7:

```python
from gemini_auth import configurar_gemini_api_key

configurar_gemini_api_key()
```

`.env`:

```bash
GEMINI_API_KEY=tu_clave_aqui
```

---

## 3) Embeddear un texto

```python
from google import genai

from gemini_auth import configurar_gemini_api_key

configurar_gemini_api_key()
client = genai.Client()

texto = "La Live Review es una sesión en vivo de 2 horas."

result = client.models.embed_content(
    model="text-embedding-004",
    contents=texto,
)

vector = list(result.embeddings[0].values)
print(f"Dimensiones: {len(vector)}")
print(f"Primeros valores: {vector[:5]}")
```

La respuesta expone `result.embeddings`: una lista; cada elemento tiene `.values` con los floats.

---

## 4) Embeddear varios chunks (batch)

Para N chunks del pipeline de ingesta:

```python
textos = [item["text"] for item in chunks_data["chunks"]]

result = client.models.embed_content(
    model="text-embedding-004",
    contents=textos,
)

for i, emb in enumerate(result.embeddings):
    vector = list(emb.values)
    print(i, len(vector))
```

En el proyecto, `embed.py` recorre los chunks y guarda texto + vector + metadata en JSON.

**Consejo:** durante desarrollo puedes limitar a los **3 primeros chunks** en `config.py` (`MAX_CHUNKS_EMBED = 3`) para no saturar cuota de API.

---

## 5) task_type (opcional avanzado)

Algunos modelos aceptan `EmbedContentConfig` con `task_type`:

| Valor | Uso |
|-------|-----|
| `RETRIEVAL_DOCUMENT` | Al indexar chunks |
| `RETRIEVAL_QUERY` | Al embeddear la pregunta del usuario |

En Sprint 9 puedes usar tipos distintos para documento vs consulta. En S8 usamos el **default** para simplificar.

---

## 6) Coste y límites (orientación)

| Factor | Implicación |
|--------|-------------|
| Número de chunks | Una llamada por batch o por texto según implementación |
| Dimensión alta | Más almacenamiento en Chroma |
| Re-indexar | Cada cambio de chunking obliga a re-embeddear |

Registra cuántos chunks embeddeas (como registrabas tokens en S7).

---

## 7) Integración en el proyecto

Flujo en `embed.py`:

```text
chunks.json  →  leer items  →  embed_content  →  embeddings.json
```

Comandos:

```bash
python main.py    # ingesta + embeddings → chunks.json y embeddings.json
```

---

## Errores frecuentes

| Error | Causa | Solución |
|-------|-------|----------|
| 401 / API key | Clave ausente o inválida | Revisar `.env` |
| Modelo no encontrado | Nombre incorrecto | Verificar en AI Studio |
| Vector vacío | Texto vacío tras clean | Revisar chunks en JSON |
| Dimensión distinta entre runs | Cambiaste modelo | Re-embeddear todo |

---

## Resumen

- Gemini embeddea con `client.models.embed_content`.
- Un **mismo modelo** para chunks y consultas en producción.
- El proyecto persiste vectores en `output/embeddings.json`.
- ChromaDB llega en Sprint 9.
