![Cabecera](../../assets/cabecera_rag.png)

# Metadatos y pipeline modular

Un pipeline de ingesta mantenible separa **responsabilidades** en módulos pequeños — la misma mentalidad que en proyectos anteriores.

Además, cada chunk debe llevar **metadatos** para saber de dónde vino cuando el retrieval lo devuelva en Sprint 9 o cuando cites fuentes en Sprint 10.

---

## Objetivos

- Definir **metadatos útiles** por chunk.
- Organizar el código en **`load` → `clean` → `chunk` → `pipeline`**.
- Persistir chunks en **JSON** inspectable en `output/`.

---

## 1) Metadatos recomendados

| Campo | Uso |
|-------|-----|
| `source` | Ruta o nombre del archivo origen |
| `page` | Número de página (PDFs; si existe) |
| `chunk_index` | Índice del chunk dentro del pipeline (0, 1, 2…) |
| `chunk_size` | Caracteres del fragmento (debug) |
| `distrito` | Distrito de Madrid (eventos del CSV) |
| `tipo` | p. ej. `agenda_evento` para filtrar en retrieval |

LangChain ya trae `source` y `page` en muchos loaders. Al trocear, **copia** los metadatos del documento padre y **añade** campos propios:

```python
from langchain_core.documents import Document


def enriquecer_metadata(chunks: list[Document]) -> list[Document]:
    enriquecidos = []
    for i, chunk in enumerate(chunks):
        meta = dict(chunk.metadata)
        meta["chunk_index"] = i
        meta["chunk_size"] = len(chunk.page_content)
        enriquecidos.append(
            Document(page_content=chunk.page_content, metadata=meta)
        )
    return enriquecidos
```

En Sprint 9 podrás filtrar por `source` o `tipo` (p. ej. solo eventos `agenda_evento`) si Chroma lo soporta en tu configuración.

---

## 2) Arquitectura del proyecto ejemplo

```text
05_proyecto_ingesta_chunking_embedding/
├── config.py       # DATA_DIR, CHUNK_SIZE, CHUNK_OVERLAP, OUTPUT_DIR
├── load.py         # cargar .txt, .md, .pdf y .csv desde data/
├── clean.py        # normalizar_texto, limpiar_documentos
├── chunk.py        # split + enriquecer metadatos
├── pipeline.py     # ejecutar_ingesta() orquesta todo
├── main.py         # CLI: python main.py
├── data/           # documentos fuente
└── output/         # chunks.json generado
```

```text
main.py
   └── pipeline.ejecutar_ingesta()
           ├── load.cargar_documentos()
           ├── clean.limpiar_documentos()
           ├── chunk.fragmentar_documentos()
           └── guardar JSON en output/
```
---

## 3) config.py centraliza parámetros

```python
from pathlib import Path

CHUNK_SIZE = 800
CHUNK_OVERLAP = 100

DATA_DIR = Path(__file__).parent / "data"
OUTPUT_DIR = Path(__file__).parent / "output"
CHUNKS_JSON = OUTPUT_DIR / "chunks.json"
```

Cambiar el tamaño de chunk para experimentar = **editar un solo archivo**.

---

## 4) Persistencia en JSON

Formato legible para juniors y para diff en Git (ejemplos fijos):

```python
import json
from langchain_core.documents import Document


def documentos_a_dicts(documentos: list[Document]) -> list[dict]:
    return [
        {"text": doc.page_content, "metadata": dict(doc.metadata)}
        for doc in documentos
    ]


def guardar_chunks_json(chunks: list[Document], ruta: Path) -> None:
    ruta.parent.mkdir(parents=True, exist_ok=True)
    payload = {
        "total_chunks": len(chunks),
        "chunks": documentos_a_dicts(chunks),
    }
    ruta.write_text(
        json.dumps(payload, ensure_ascii=False, indent=2),
        encoding="utf-8",
    )
```

En el Bloque 3 leerás este JSON para generar embeddings sin re-ejecutar load/chunk (útil mientras iteras en embed).

---

## 5) Salida esperada al ejecutar

```bash
python main.py
```

```text
Ingesta: cargando documentos desde data/ ...
  Documentos cargados: 760
  Tras limpieza: 760
  Chunks generados: 820
  Guardado: output/chunks.json
Listo. Revisa output/chunks.json antes del Bloque 3 (embeddings).
```

*(Cifras orientativas con el corpus de agenda: ~757 eventos CSV + FAQ + guía + páginas del PDF.)*

---

## 6) Puente al proyecto acumulativo del módulo

Este proyecto es la **primera pieza** de `proyecto_rag_bootcamp_ejemplo/`:

| Sprint / Bloque | Módulos |
|-----------------|---------|
| S8 Bloque 2 | `load`, `clean`, `chunk`, `pipeline` |
| S8 Bloque 3 | `embed` (lee `chunks.json` o encadena) |
| S9 | `index`, `retriever` |
| S10 | `prompts`, `logic`, `validators` |

No reescribes la ingesta cada semana: **la extiendes**.

---

## 7) Buenas prácticas

| Práctica | Motivo |
|----------|--------|
| Revisar `chunks.json` a mano | Detectar errores antes de embeddear |
| Versionar `data/` de ejemplo | Reproducibilidad |
| No versionar `output/` generado en cada run | Artefactos locales (`chunks.json`, `embeddings.json`) |
| Logs claros por etapa | Depurar load vs clean vs chunk |


