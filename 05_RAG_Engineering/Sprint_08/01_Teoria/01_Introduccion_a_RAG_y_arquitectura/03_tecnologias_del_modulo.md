![Cabecera](../../assets/cabecera_rag.png)

# Tecnologías del módulo RAG

En este bootcamp construirás pipelines RAG con herramientas concretas. No necesitas dominar cada librería al completo: necesitas saber **qué pieza resuelve qué problema** y cómo encajan en tu proyecto modular.

---

## Objetivos

- Conocer el **stack** del Módulo 4: Gemini, LangChain, ChromaDB.
- Entender **qué usa LangChain** en este curso (y qué no).
- Revisar **convenciones** de proyectos (config, capas, `.env`, `output/`).
- Tener claro el calendario tecnológico por sprint.

---

## 1) Stack principal

| Tecnología | Rol en el pipeline | Sprint |
|------------|-------------------|--------|
| [**Python 3.10+**](https://www.python.org/) | Lenguaje base | 8–10 |
| [**google-genai**](https://github.com/googleapis/python-genai) | LLM ([Gemini](https://ai.google.dev/)) y embeddings Gemini | 8–10 |
| [**LangChain**](https://python.langchain.com/) | Loaders de documentos, text splitters, integración Chroma | 8–9 |
| [**ChromaDB**](https://docs.trychroma.com/) | Base de datos vectorial persistente | 9 |
| [**Hugging Face**](https://huggingface.co/) ([`sentence-transformers`](https://huggingface.co/sentence-transformers)) | Embeddings locales o remotos (comparación opcional) | 8 |
| [**Streamlit**](https://streamlit.io/) *(opcional)* | Interfaz sencilla para la app RAG | 10 |

```text
         LangChain                    ChromaDB
    (load / split / chain)         (almacenar / buscar)
              │                           │
              └─────────┬─────────────────┘
                        ▼
                   tu proyecto
                   modular Python
                        │
                        ▼
                   google-genai
                   (embed + generate)
```

---

## 2) Google Gemini ([`google-genai`](https://github.com/googleapis/python-genai))

Ya usaste Gemini en Sprints 4–7. En RAG aparece en **dos papeles**:

| Papel | Uso |
|-------|-----|
| **Embedding model** | Convertir chunks y consultas en vectores (S8) |
| **LLM generativo** | Redactar la respuesta con contexto recuperado (S10) |

Convenciones que mantenemos:

- API key en `.env` (`GEMINI_API_KEY`), nunca en el código. Obtén la clave en [Google AI Studio](https://aistudio.google.com/apikey).
- Módulo `gemini_auth.py` o equivalente para centralizar la clave.
- Modelo generativo por defecto alineado con sprints recientes (p. ej. `gemini-3-flash-preview`).
- Modelo de embeddings según documentación actual de [Google AI Studio](https://aistudio.google.com/) y la [API de embeddings](https://ai.google.dev/gemini-api/docs/embeddings).

**Importante:** usa el **mismo proveedor de embeddings** para indexar y para consultar. Mezclar embeddings de Gemini al indexar y de Hugging Face al consultar rompe la comparación vectorial.

---

## 3) [LangChain](https://python.langchain.com/) — alcance en este bootcamp

LangChain es un ecosistema grande. Aquí lo usamos de forma **acotada**:

| Sí usamos | No usamos (en esta fase) |
|-----------|--------------------------|
| [`PyPDFLoader`](https://python.langchain.com/docs/integrations/document_loaders/pypdf/), [`DirectoryLoader`](https://python.langchain.com/docs/integrations/document_loaders/directory/) | Cadenas monolíticas opacas tipo `RetrievalQA` sin entender capas |
| [`RecursiveCharacterTextSplitter`](https://python.langchain.com/docs/how_to/recursive_text_splitter/) | Agentes LangChain completos (Módulo 5) |
| Integración con Chroma ([`langchain-chroma`](https://python.langchain.com/docs/integrations/vectorstores/chroma/)) | Despliegue en cloud |

LangChain **no sustituye** tu arquitectura modular: envuelve loaders y splitters para no reinventar lectura de PDFs. La lógica de negocio vive en **tus** módulos (`load.py`, `chunk.py`, `retriever.py`…).

Ejemplo de responsabilidades:

```text
load.py     → usa PyPDFLoader (LangChain) + guarda Document en tu formato
chunk.py    → usa RecursiveCharacterTextSplitter + añade metadatos
index.py    → usa Chroma.from_documents (S9)
logic.py    → orquesta retrieve + prompt + Gemini (S10)
```

---

## 4) [ChromaDB](https://docs.trychroma.com/) (Sprint 9)

**Chroma** es una base de datos vectorial **local y persistente**, ideal para aprender y prototipar. Documentación: [Getting started](https://docs.trychroma.com/docs/overview/getting-started).

| Concepto | Significado |
|----------|-------------|
| **Colección** | Conjunto de documentos/chunks indexados |
| **Embedding function** | Función que vectoriza texto al insertar y al consultar |
| **persist_directory** | Carpeta en disco donde se guarda el índice |
| **similarity_search** | Busca los vectores más cercanos a la query |

En S8 **no** instalas Chroma todavía: preparas los artefactos (chunks, vectores) que indexarás en S9.

---

## 5) [Hugging Face](https://huggingface.co/) (Sprint 8)

Modelos como [`sentence-transformers/all-MiniLM-L6-v2`](https://huggingface.co/sentence-transformers/all-MiniLM-L6-v2) permiten generar embeddings **en local o en la nube** sin llamada a API. Librería: [`sentence-transformers`](https://huggingface.co/docs/sentence-transformers/index).


---

## 6) Convenciones de proyectos modulares

Mismas reglas que S5–S7:

```text
proyecto_rag_bootcamp_ejemplo/
├── config.py           # rutas, chunk_size, modelos, top_k
├── gemini_auth.py      # carga API key
├── load.py             # S8
├── clean.py            # S8
├── chunk.py            # S8
├── embed.py            # S8
├── index.py            # S9
├── retriever.py        # S9
├── prompts.py          # S10
├── logic.py            # S10
├── validators.py       # S10
├── main.py             # CLI / demos
├── data/               # documentos fuente (PDFs cuando existan)
├── output/             # chunks, logs, chroma… (gitignored)
├── requirements.txt
├── .env.example
└── README.md
```

| Regla | Motivo |
|-------|--------|
| `config.py` centraliza parámetros | Cambiar `CHUNK_SIZE` sin tocar lógica |
| `output/` fuera de Git | Artefactos generados, índices locales |
| `main.py` delgado | Orquesta; no contiene toda la lógica |
| Validación antes del LLM (S10) | Continuidad con S6 |

---

## 7) Dependencias orientativas (por sprint)

**Sprint 8**:

| Paquete | Enlace |
|---------|--------|
| [`google-genai`](https://pypi.org/project/google-genai/) | [Documentación Gemini API](https://ai.google.dev/gemini-api/docs) |
| [`python-dotenv`](https://pypi.org/project/python-dotenv/) | [GitHub](https://github.com/theskumar/python-dotenv) |
| [`langchain-community`](https://pypi.org/project/langchain-community/) | [Document loaders](https://python.langchain.com/docs/integrations/document_loaders/) |
| [`langchain-text-splitters`](https://pypi.org/project/langchain-text-splitters/) | [Text splitters](https://python.langchain.com/docs/how_to/#text-splitters) |
| [`pypdf`](https://pypi.org/project/pypdf/) | [Documentación](https://pypdf.readthedocs.io/) |

**Sprint 9**:

| Paquete | Enlace |
|---------|--------|
| [`langchain-chroma`](https://pypi.org/project/langchain-chroma/) | [Integración Chroma](https://python.langchain.com/docs/integrations/vectorstores/chroma/) |
| [`chromadb`](https://pypi.org/project/chromadb/) | [ChromaDB docs](https://docs.trychroma.com/) |

**Sprint 10**:

| Paquete | Enlace |
|---------|--------|
| [`streamlit`](https://pypi.org/project/streamlit/) *(opcional)* | [Documentación](https://docs.streamlit.io/) |

Fijaremos versiones en `requirements.txt` de cada proyecto cuando implementemos el código.

---

## 8) Calendario tecnológico

| Sprint | Implementas | No implementas aún |
|--------|-------------|-------------------|
| **8** | Load, clean, chunk, embed | Chroma, retriever, LLM con contexto |
| **9** | Index, similarity_search, eval retrieval | Respuesta final al usuario |
| **10** | Prompt RAG, generate, robustez, app | — |

---

## Resumen

- [**Gemini**](https://ai.google.dev/) para embed (S8) y generate (S10).
- [**LangChain**](https://python.langchain.com/) para loaders, splitters e integración Chroma — no para esconder la arquitectura.
- [**ChromaDB**](https://docs.trychroma.com/) en S9 para persistir y buscar vectores.
- **Proyecto modular** acumulativo, misma filosofía que S5–S7.
- PDFs de `data/` se definirán más adelante; el pipeline está pensado para crecer con ellos.
