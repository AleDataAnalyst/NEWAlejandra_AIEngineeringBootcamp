![Cabecera](../../assets/cabecera_rag.png)

# Carga y lectura de documentos

El primer paso del pipeline RAG es **leer** tus fuentes: archivos en disco que contienen el conocimiento que quieres recuperar después.

Usaremos la librería **LangChain document loaders**: wrappers que devuelven objetos estándar `Document` listos para limpiar y trocear.

---

## Objetivos

- Entender el objeto **`Document`** (`page_content` + `metadata`).
- Cargar archivos **.txt**, **.md** y **.pdf** desde una carpeta.
- Procesar **múltiples documentos** en un solo flujo.

---

## 1) El objeto `Document`

LangChain representa cada trozo de texto cargado así:

| Atributo | Contenido |
|----------|-----------|
| `page_content` | Texto extraído del archivo (string) |
| `metadata` | Diccionario con info de procedencia (`source`, `page` en PDFs…) |

```python
from langchain_core.documents import Document

doc = Document(
    page_content="Cada fila del CSV incluye el campo GRATUITO: 1 si la actividad es gratuita.",
    metadata={"source": "data/faq_agenda_cultural.md"},
)

print(doc.page_content)
print(doc.metadata)
```

**Idea clave:** el loader **no trocea** ni genera embeddings; solo **lee** y devuelve documentos (a menudo uno por página en PDFs).

---

## 2) Cargar un archivo de texto (.txt, .md)

```python
from langchain_community.document_loaders import TextLoader

loader = TextLoader("data/faq_agenda_cultural.md", encoding="utf-8")
documentos = loader.load()

print(f"Documentos cargados: {len(documentos)}")
print(documentos[0].page_content[:200])
print(documentos[0].metadata)
```

Para Markdown y TXT el loader suele devolver **un documento por archivo** con todo el contenido en `page_content`.

---

## 3) Cargar un PDF

```python
from langchain_community.document_loaders import PyPDFLoader

loader = PyPDFLoader("data/206974-3-agenda-eventos-culturales-100.pdf")
paginas = loader.load()

for i, pagina in enumerate(paginas[:3]):
    print(f"--- Página {i + 1} ---")
    print(pagina.page_content[:300])
    print(pagina.metadata)  # suele incluir 'page', 'source'
```

`PyPDFLoader` devuelve **una lista de Document por página**. Los metadatos típicos incluyen:

- `source`: ruta del PDF
- `page`: número de página (0-indexed)

**Limitación:** PDFs escaneados (imagen) o con maquetación compleja pueden extraer texto mal. En producción a veces hace falta algún proceso de OCR (reconocimiento óptico de caracteres) para extraer el texto; en este sprint asumimos PDFs con texto seleccionable.

---

## 4) Cargar una carpeta entera

Patrón habitual en proyectos modulares: leer todo lo que hay en `data/`:

```python
from pathlib import Path
from langchain_community.document_loaders import PyPDFLoader, TextLoader

def cargar_archivo(ruta: Path) -> list:
    sufijo = ruta.suffix.lower()
    if sufijo == ".pdf":
        return PyPDFLoader(str(ruta)).load()
    if sufijo in {".txt", ".md"}:
        return TextLoader(str(ruta), encoding="utf-8").load()
    return []

def cargar_carpeta(carpeta: Path) -> list:
    documentos = []
    for ruta in sorted(carpeta.rglob("*")):
        if ruta.is_file():
            documentos.extend(cargar_archivo(ruta))
    return documentos
```

En el [proyecto ejemplo](../03_Embeddings/05_proyecto_ingesta_chunking_embedding/load.py) esta lógica vive en `load.py` (incluye `.csv` de agenda — ver §5).

---

## 5) CSV tabular → `Document` (patrón manual)

Un CSV **no** se carga con `TextLoader`: obtendrías una tabla ilegible para el LLM.

**Patrón RAG:** leer con **pandas**, convertir **cada fila** en texto en lenguaje natural y crear un `Document` con `page_content` + `metadata`.

En el workout lo practicas paso a paso; en el proyecto está en `load.py` → `cargar_agenda_csv`:

- Encoding `latin-1` (común en open data español).
- Metadatos útiles: `source`, `distrito`, `tipo: agenda_evento`.
- Una fila sin título se omite.

Workout detallado: [`01_carga_documentos_y_chunking.ipynb`](../../02_Workout/02_Ingesta_y_procesamiento_de_documentos/01_carga_documentos_y_chunking.ipynb) (§3).

---

## 6) Múltiples documentos: qué esperar

| Formato | Documentos típicos por archivo |
|---------|-------------------------------|
| `.txt` / `.md` | 1 (archivo completo) |
| `.pdf` de 10 páginas | 10 (una por página) |
| `.csv` de eventos | 1 por fila (evento) |

Antes del chunking conviene saber **cuántos Document** tienes:

```python
documentos = cargar_carpeta(Path("data"))
print(f"Total documentos LangChain: {len(documentos)}")
print(f"Caracteres totales: {sum(len(d.page_content) for d in documentos)}")
```

---

## 7) Errores frecuentes

| Error | Causa | Solución |
|-------|-------|----------|
| `FileNotFoundError` | Ruta incorrecta | Usar `Path` desde `config.DATA_DIR` |
| Texto con `` | Encoding incorrecto | `encoding="utf-8"` en TextLoader |
| PDF vacío | PDF escaneado o protegido | Probar otro PDF; revisar extracción manual |
| Mezclar formatos sin filtrar | Extensiones no soportadas | Ignorar archivos desconocidos o loguear aviso |

---

## Resumen

- Un **loader** lee archivos y devuelve `Document` con texto + metadatos.
- **TXT/MD:** un documento por archivo; **PDF:** uno por página; **CSV:** uno por fila (construido a mano).
- Carga **toda la carpeta** `data/` en un bucle o función reutilizable.
- El chunking viene **después** — no cargues manualmente trozos pequeños a mano.