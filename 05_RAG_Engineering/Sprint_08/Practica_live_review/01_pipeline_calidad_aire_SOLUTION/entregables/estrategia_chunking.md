# Estrategia de chunking — calidad del aire Madrid

Documenta **tus decisiones** tras ejecutar el pipeline (Fase 1). Incluye **números reales** de tu consola o de `output/chunks.json`.

## 1. Unidad de documento en el CSV

Usé **1 fila = 1 documento**. Cada fila del CSV ya agrupa un parámetro concreto (p. ej. temperatura, código 83) en una estación y un día, con las 24 horas en el mismo registro. Convertirla en un párrafo legible mantiene la coherencia semántica: una pregunta como «¿qué temperatura hubo a mediodía el 1 de julio en la estación 1?» recupera un solo chunk con contexto completo.

## 2. Parámetros de chunking (configuración inicial)

| Parámetro | Valor usado | ¿Por qué? |
|-----------|-------------|-----------|
| CHUNK_SIZE | 800 | Caben enteras la mayoría de filas CSV (~760–800 caracteres) y párrafos del FAQ/PDF sin partir de más |
| CHUNK_OVERLAP | 100 | Mantiene continuidad cuando un texto supera 800 caracteres (FAQ, PDF) y evita cortes bruscos entre trozos |

## 3. Observación en consola

Tras `python main.py`, ¿cuántos chunks generó cada fuente?

| Fuente | Chunks |
|--------|--------|
| faq_calidad_aire.md | 4 |
| guia_calidad_aire.txt | 2 |
| PDF documentación | 6 |
| CSV mediciones | 100 |

**Total:** 112 chunks · 105 documentos cargados (100 CSV + 3 PDF + 1 FAQ + 1 guía).

El CSV aporta casi todo el volumen porque `MAX_FILAS_CSV = 100` y cada fila cabe en un solo chunk con `CHUNK_SIZE = 800`. El FAQ y la guía se parten en varios trozos al superar el tamaño configurado.

## 4. Experimento con parámetros

Cambia **solo** `CHUNK_SIZE` y/o `CHUNK_OVERLAP` en `config.py` (no modifiques `chunk.py`), vuelve a ejecutar `python main.py` y compara.

| | Valores iniciales | Tras el cambio |
|--|-------------------|----------------|
| CHUNK_SIZE | 800 | 400 |
| CHUNK_OVERLAP | 100 | 50 |
| Total chunks | 112 | ~218 |
| Chunks del PDF | 6 | ~10 |

Al bajar `CHUNK_SIZE` a 400, las filas CSV (~780 caracteres) pasan de 1 chunk a ~2 por fila, duplicando en la práctica los chunks del CSV (100 → ~200). El PDF y el FAQ también se fragmentan más (6 → ~10 y 4 → ~7). El CSV apenas cambiaba con 800/100 porque ya cabía entero; el experimento demuestra que el chunking **sí importa** cuando el texto supera el tamaño configurado.

## 5. Muestra de chunks

Copia **2–3 líneas** de texto (sin pegar chunks enteros) de:

- Un chunk del **FAQ**
- Un chunk del **CSV** (magnitud 83 si puedes)

**FAQ:** «En el fichero CSV, la columna **magnitud** indica qué parámetro se ha medido… | **83** | Temperatura | °C |» — Encaja con preguntas conceptuales: «¿Qué mide el código 83?» o «¿Qué unidad usa la temperatura?».

**CSV (magnitud 83):** «Medición: Temperatura (código 83)… 12:00 → 32,8 (validación V)… 15:00 → 34,4 (validación V)» — Encaja con preguntas de valor concreto: «¿Cuál fue la temperatura máxima el 1 de julio a mediodía en el municipio 102?».

## 6. Riesgo o mejora

Con un corpus 10× más grande mantendría `MAX_FILAS_CSV` bajo en desarrollo, añadiría la **fecha** (`YYYY-MM-DD`) en metadata para filtrar antes de embeddear, y en producción indexaría por `magnitud` + `estacion` para no embeddear mediciones irrelevantes a cada consulta. También revisaría si conviene agrupar varias horas o varios días en un documento cuando el retrieval sea por rangos temporales amplios.
