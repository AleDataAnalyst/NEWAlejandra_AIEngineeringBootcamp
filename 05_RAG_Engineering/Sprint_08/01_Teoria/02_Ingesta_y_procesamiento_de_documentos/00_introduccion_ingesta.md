![Cabecera](../../assets/cabecera_rag.png)

# Introducción: ingesta y procesamiento

En el Bloque 1 viste la **arquitectura RAG** completa. En este bloque implementas la **primera mitad de la fase offline**:

> **Documentos en bruto → fragmentos limpios listos para vectorizar.**

Todavía no llamas a Gemini ni creas embeddings. El objetivo es dominar **carga, limpieza y chunking** como un pipeline modular y reproducible.

---

## Objetivos del bloque

Al terminar, deberías poder:

- Cargar documentos desde una carpeta (`data/`) con LangChain loaders.
- Normalizar texto antes de fragmentarlo.
- Dividir documentos en **chunks** con tamaño y solapamiento configurables.
- Añadir **metadatos** útiles para trazabilidad (`source`, índice de chunk…).
- Orquestar el flujo en módulos separados y guardar el resultado en **JSON**.

---

## Dónde encaja en el pipeline RAG

```text
  [ Bloque 2 — este bloque ]
  ─────────────────────────
  data/*.txt, *.md, *.pdf, *.csv
           │
           ▼
        LOAD ──► CLEAN ──► CHUNK ──► output/chunks.json
                                           │
  [ Bloque 3 — siguiente ]                 │
  ────────────────────────                 ▼
                                    EMBED ──► vectores
                                           │
  [ Sprint 9 ]                             ▼
  ────────────                        INDEX (Chroma)
```

---

## Qué es un «chunk» y un «embedding»

Un **chunk** es un fragmento de texto que se puede usar para buscar semánticamente en la base de datos vectorial.

Un **embedding** es un vector de números que representa un texto. Es una representación numérica del texto que se puede usar para buscar semánticamente en la base de datos vectorial. Por ejemplo, si tenemos un texto "La capital de Francia es París", su embedding sería un vector de números que representa ese texto.

Un **chunk** es un fragmento de texto **suficientemente pequeño** para:

1. Generar un **embedding** representativo.
2. Recuperarse como unidad en búsqueda semántica (Sprint 9).
3. Caber en el **contexto del LLM** junto con otros chunks (Sprint 10).

Si el chunk es **demasiado grande**, mezcla temas y empeora la precisión del retrieval. Si es **demasiado pequeño**, pierde contexto necesario para responder. Hay que encontrar el equilibrio perfecto para que el chunk sea lo suficientemente grande como para contener el contexto necesario para responder la pregunta, pero lo suficientemente pequeño como para que no sea demasiado grande y mezcle temas.


---

## Salida concreta de este bloque

Tras ejecutar el [proyecto ejemplo](../03_Embeddings/05_proyecto_ingesta_chunking_embedding/) (Bloque 3):

```text
output/chunks.json
```

Cada entrada tendrá forma similar a:

```json
{
  "text": "No. Cada fila del CSV incluye el campo GRATUITO: 1 → actividad gratuita...",
  "metadata": {
    "source": "data/faq_agenda_cultural.md",
    "chunk_index": 0
  }
}
```

Inspeccionar ese JSON es parte del aprendizaje: **antes de automatizar, mira qué estás indexando**.

---

## Documentos de ejemplo

Corpus del sprint: **agenda cultural de Madrid** ([datos.madrid.es](https://datos.madrid.es)) — cuatro archivos en `data/`:

| Archivo | Rol |
|---------|-----|
| `faq_agenda_cultural.md` | Preguntas frecuentes sobre el dataset |
| `guia_agenda_cultural.txt` | Guía de uso y campos del CSV |
| `206974-3-agenda-eventos-culturales-100.pdf` | Documentación técnica del fichero |
| `206974-4-agenda-eventos-culturales-100-csv.csv` | Un evento por fila (carga manual → `Document`) |

El [proyecto ejemplo](../03_Embeddings/05_proyecto_ingesta_chunking_embedding/) y el [workout](../../02_Workout/02_Ingesta_y_procesamiento_de_documentos/01_carga_documentos_y_chunking.ipynb) usan el mismo corpus.

---

## Tabla guía de lectura

| # | Documento | Enfoque |
|---|-----------|---------|
| 1 | [Carga y lectura](./01_carga_y_lectura_documentos.md) | Loaders LangChain |
| 2 | [Limpieza](./02_limpieza_y_normalizacion.md) | Normalización de texto |
| 3 | [Chunking](./03_chunking_estrategias.md) | Estrategias y parámetros |
| 4 | [Metadatos y pipeline](./04_metadatos_y_pipeline_modular.md) | Arquitectura del código |

**Proyecto (Bloque 3):** [05_proyecto_ingesta_chunking_embedding/](../03_Embeddings/05_proyecto_ingesta_chunking_embedding/)
