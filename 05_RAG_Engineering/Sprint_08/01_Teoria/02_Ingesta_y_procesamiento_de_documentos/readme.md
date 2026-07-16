![Cabecera](../../assets/cabecera_rag.png)

# 📘 Sprint 08 · Bloque 02

## Ingesta y procesamiento de documentos

Tras entender **qué es RAG** (Bloque 1), aquí empiezas a **programar la fase offline**:

> **¿Cómo preparo los documentos para convertirlos en conocimiento recuperable?**

Salida de este bloque: **fragmentos (chunks) con metadatos**, guardados en un archivo inspectable (`output/chunks.json`). Todavía **sin embeddings** (Bloque 3) ni ChromaDB (Sprint 9).

---

## 📂 Contenido de la teoría (orden de lectura)

---

### 🧭 0. Introducción

🔗 [Abrir](./00_introduccion_ingesta.md)

* Objetivos del bloque y salida esperada
* Del documento al chunk en el pipeline RAG

---

### 📥 1. Carga y lectura de documentos

🔗 [Abrir](./01_carga_y_lectura_documentos.md)

* Objeto `Document` de LangChain
* `TextLoader`, `PyPDFLoader`, CSV → `Document`, carga de carpetas
* Múltiples formatos (.txt, .md, .pdf, .csv)

---

### 🧹 2. Limpieza y normalización

🔗 [Abrir](./02_limpieza_y_normalizacion.md)

* Ruido típico en PDFs y textos exportados
* Normalización mínima en Python

---

### ✂️ 3. Chunking: estrategias

🔗 [Abrir](./03_chunking_estrategias.md)

* Por qué fragmentar
* `RecursiveCharacterTextSplitter`
* `chunk_size` y `chunk_overlap`

---

### 🏗️ 4. Metadatos y pipeline modular

🔗 [Abrir](./04_metadatos_y_pipeline_modular.md)

* Metadatos (`source`, `page`, `chunk_id`)
* Capas `load` / `clean` / `chunk` / `pipeline`
* Persistencia en JSON

---

## Workout (vídeo guiado)

| Recurso | Cubre |
|---------|--------|
| [01_carga_documentos_y_chunking.ipynb](../../02_Workout/02_Ingesta_y_procesamiento_de_documentos/01_carga_documentos_y_chunking.ipynb) | Carga, limpieza y chunking con LangChain |

El **proyecto modular** (`05_proyecto_ingesta_chunking_embedding`) y la guía al código están en el [Bloque 3 — Embeddings](../03_Embeddings/readme.md).
