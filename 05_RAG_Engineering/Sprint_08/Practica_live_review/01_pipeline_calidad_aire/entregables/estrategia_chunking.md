# Estrategia de chunking — calidad del aire Madrid

Documenta **tus decisiones** tras ejecutar el pipeline (Fase 1). Incluye **números reales** de tu consola o de `output/chunks.json`.

## 1. Unidad de documento en el CSV

¿Usaste **1 fila = 1 documento** u otra estrategia?

TODO — explica tu elección en 2–4 frases.

## 2. Parámetros de chunking (configuración inicial)

| Parámetro | Valor usado | ¿Por qué? |
|-----------|-------------|-----------|
| CHUNK_SIZE | TODO | |
| CHUNK_OVERLAP | TODO | |

## 3. Observación en consola

Tras `python main.py`, ¿cuántos chunks generó cada fuente?

| Fuente | Chunks |
|--------|--------|
| faq_calidad_aire.md | TODO |
| guia_calidad_aire.txt | TODO |
| PDF documentación | TODO |
| CSV mediciones | TODO |

## 4. Experimento con parámetros

Cambia **solo** `CHUNK_SIZE` y/o `CHUNK_OVERLAP` en `config.py` (no modifiques `chunk.py`), vuelve a ejecutar `python main.py` y compara.

| | Valores iniciales | Tras el cambio |
|--|-------------------|----------------|
| CHUNK_SIZE | TODO | TODO |
| CHUNK_OVERLAP | TODO | TODO |
| Total chunks | TODO | TODO |
| Chunks del PDF | TODO | TODO |

TODO — ¿Qué cambió y por qué? (2–4 frases)

## 5. Muestra de chunks

Copia **2–3 líneas** de texto (sin pegar chunks enteros) de:

- Un chunk del **FAQ**
- Un chunk del **CSV** (magnitud 83 si puedes)

TODO — ¿Qué tipo de pregunta encajaría con cada uno?

## 6. Riesgo o mejora

TODO — ¿Qué cambiarías si el corpus fuera 10 veces más grande?
