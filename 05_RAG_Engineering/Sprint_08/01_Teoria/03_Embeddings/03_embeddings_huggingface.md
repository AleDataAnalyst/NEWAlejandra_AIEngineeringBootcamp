![Cabecera](../../assets/cabecera_rag.png)

# Embeddings con Hugging Face

[**Hugging Face**](https://huggingface.co/) es un hub de modelos open source. En embeddings, la familia [**sentence-transformers**](https://huggingface.co/sentence-transformers) convierte texto en vectores numéricos.

En este bootcamp puedes usar HF de **dos formas**:

| Modo | Cómo | API key | Cuándo |
|------|------|---------|--------|
| **Nube** | [Inference API](https://huggingface.co/docs/api-inference/index) vía [`huggingface_hub`](https://huggingface.co/docs/huggingface_hub) | Sí (`HF_TOKEN`) | Workout de comparación; sin instalar pesos en tu máquina |
| **Local** | [`sentence-transformers`](https://huggingface.co/docs/sentence-transformers/index) en CPU/GPU | No | Offline, prototipos sin internet, sección opcional del notebook |

HF es **otra opción** frente a Gemini: sirve para **comparar** enfoques, no para mezclar con el índice principal de Gemini sin re-indexar.

---

## Objetivos

- Diferenciar **HF en nube** (Inference API) y **HF local** (`sentence-transformers`).
- Generar embeddings con cada modo en pocas líneas.
- Decidir cuándo HF tiene sentido frente a Gemini.

---

## 1) Dos caminos, mismo Hub

```text
                    Hugging Face Hub
              (modelos sentence-transformers)
                           │
           ┌───────────────┴───────────────┐
           ▼                               ▼
    HF en la nube                    HF local
 huggingface_hub                  sentence-transformers
 InferenceClient                  SentenceTransformer
 HF_TOKEN en .env                  descarga pesos (~120 MB)
 servidores HF                     CPU o GPU de tu máquina
```

Modelo de referencia en el workout (español + multilingüe, **384 dimensiones**):

[`sentence-transformers/paraphrase-multilingual-MiniLM-L12-v2`](https://huggingface.co/sentence-transformers/paraphrase-multilingual-MiniLM-L12-v2)

En ejemplos locales más simples también verás [`all-MiniLM-L6-v2`](https://huggingface.co/sentence-transformers/all-MiniLM-L6-v2) (384D, centrado en inglés).

---

## 2) HF en la nube — Inference API

Es el camino que usa el notebook [`02_comparar_modelos_embedding.ipynb`](../../02_Workout/03_Embeddings/02_comparar_modelos_embedding.ipynb) **antes** de la sección local opcional.

### Instalación

```bash
pip install huggingface_hub python-dotenv
```

### Token

1. Cuenta gratuita en [huggingface.co](https://huggingface.co).
2. Token en [huggingface.co/settings/tokens](https://huggingface.co/settings/tokens).
3. En `.env` (nunca en Git):

```bash
HF_TOKEN=hf_...
```

### Uso básico

```python
import os
from huggingface_hub import InferenceClient

MODELO_HF = "sentence-transformers/paraphrase-multilingual-MiniLM-L12-v2"

client = InferenceClient(provider="hf-inference", api_key=os.environ["HF_TOKEN"])

texto = "Live Review del bootcamp"
vector = client.feature_extraction(texto, model=MODELO_HF)

# La API devuelve una matriz; para una frase suele ser (1, 384) o lista anidada
import numpy as np
arr = np.array(vector)
print(arr.shape)  # p. ej. (1, 384) o (384,)
```

**Flujo:** tu código → `InferenceClient` → servidores de Hugging Face → vector.

Ventajas: no descargas pesos, no necesitas GPU local, mismo patrón mental que Gemini (llamada remota). Inconvenientes: dependes de red, cuota/rate limits del plan gratuito, necesitas `HF_TOKEN`.

---

## 3) HF local — `sentence-transformers`

Ejecutas el modelo **en tu máquina**. Es la sección **opcional** al final del notebook de comparación y la opción típica en la Live Review si pruebas HF sin API.

### Instalación

```bash
pip install sentence-transformers
```

La primera ejecución **descarga pesos** del modelo (~90–120 MB). No requiere API key.

### Uso básico

```python
from sentence_transformers import SentenceTransformer

model = SentenceTransformer("sentence-transformers/all-MiniLM-L6-v2")

frases = [
    "Live Review del bootcamp",
    "Sesión en vivo del sprint",
    "Receta de tortilla de patatas",
]

vectores = model.encode(frases, normalize_embeddings=True)

print(vectores.shape)  # (3, 384) — 3 frases, 384 dimensiones
```

`normalize_embeddings=True` facilita comparar con similitud del coseno (vectores unitarios).

Ventajas: gratis, offline tras la descarga, control total de la versión del modelo. Inconvenientes: CPU lenta con corpus grande, RAM/GPU limitadas, tú mantienes el runtime.

---

## 4) HF nube vs HF local (mismo modelo)

| Criterio | HF nube | HF local |
|----------|---------|----------|
| Librería | `huggingface_hub` | `sentence-transformers` |
| API key | `HF_TOKEN` | No |
| Descarga de pesos | No (en tu disco) | Sí, la primera vez |
| Latencia | Red + cola HF | Tu CPU/GPU |
| Offline | No | Sí (tras descargar) |
| Mismo vector si es el mismo modelo | Sí (salvo diferencias numéricas mínimas) | Sí |

Si comparas **HF nube vs HF local** con el **mismo** `model_id`, el contraste semántico (p. ej. frases parecidas vs distintas) debería ser muy similar. Lo que cambia es **cómo** ejecutas el modelo, no el espacio vectorial (siempre que sea el mismo checkpoint).

---

## 5) Comparación con Gemini

| Criterio | Gemini (API) | HF nube | HF local |
|----------|--------------|---------|----------|
| API key | `GEMINI_API_KEY` | `HF_TOKEN` | No |
| Coste | Cuota Google | Plan HF (free tier) | Gratis (tu hardware) |
| Dimensiones | p. ej. 3072 (`gemini-embedding-2`) | 384 (MiniLM multilingüe) | 384 (MiniLM) |
| Latencia | Red + API Google | Red + API HF | Tu máquina |
| Proyecto acumulativo bootcamp | **Camino principal** | Comparación didáctica | Comparación / offline |

---

## 6) Comparación práctica en el workout

La comparación entre proveedores (Gemini, **HF nube**, Cohere, **HF local** opcional) está en el notebook [`02_comparar_modelos_embedding.ipynb`](../../02_Workout/03_Embeddings/02_comparar_modelos_embedding.ipynb).

Ahí verás matrices de similitud y gráficos PCA **por proveedor** — sin mezclar espacios vectoriales distintos.

Orden recomendado en el notebook:

1. Gemini (`GEMINI_API_KEY`)
2. Hugging Face **nube** (`HF_TOKEN`)
3. Cohere (opcional, `COHERE_API_KEY`)
4. Hugging Face **local** (opcional, `sentence-transformers`)

---

## 7) Cuándo usar cada modo (orientación)

| Escenario | Recomendación |
|-----------|---------------|
| Pipeline del módulo / proyecto acumulativo | **Gemini** (coherencia S4–S10) |
| Comparar proveedores en clase | HF **nube** + Gemini en el notebook |
| Sin internet o sin instalar pesos pesados | HF **local** |
| Corpus muy grande, coste API sensible | Evaluar HF local o batch en nube |
| Bootcamp, misma API key que ya usas para Gemini | Prefiere **Gemini** para indexar |

---

## 8) Advertencia: no mezclar espacios vectoriales

```text
Índice Chroma creado con Gemini 3072D
Consulta embeddeada con MiniLM 384D      →  ❌ NO válido

Índice Chroma creado con HF nube MiniLM
Consulta embeddeada con Gemini           →  ❌ NO válido
```

Reglas:

- Mismo **modelo y mismo modo** (nube o local) para **indexar y consultar**.
- HF nube vs HF local con el **mismo** `model_id` → sí compatible en principio.
- Gemini vs HF (nube o local) → **no** mezclar en el mismo índice.
- Si comparas modelos en clase, hazlo sobre **matrices de similitud separadas**, no en el mismo índice Chroma.

---

## Resumen

- Hugging Face ofrece **nube** (`huggingface_hub` + `HF_TOKEN`) y **local** (`sentence-transformers`).
- En el workout, HF **nube** es el camino principal de comparación; HF **local** es opcional.
- Útil para **aprender y comparar** similitud semántica frente a Gemini.
- El pipeline principal del módulo sigue usando **Gemini**.
- Mismo proveedor y mismo modelo siempre para indexar y consultar.
