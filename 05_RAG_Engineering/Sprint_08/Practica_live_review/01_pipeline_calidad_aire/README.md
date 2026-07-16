![Cabecera](../../assets/cabecera_rag.png)

# Práctica Sprint 08 — Pipeline calidad del aire Madrid

**Práctica integradora (Live Review)** del Sprint 8 — Data Ingestion & Embeddings.

Adaptarás la **ingesta** del pipeline RAG al dominio de **datos meteorológicos** de Madrid. El chunking y los embeddings **ya están implementados**: el código principal de Fase 1 va en `load.py`; el resto del trabajo es **ejecutar, inspeccionar y documentar** resultados.

> Todavía **no** hay retrieval ni respuestas con LLM. Esto vendrá más adelante.

---

## Empieza aquí

### Fase 1 — Ingesta y análisis de chunks

- [ ] **1.** `load.py` → `nombre_magnitud()`
- [ ] **2.** `load.py` → `fila_meteo_a_texto()`
- [ ] **3.** `load.py` → `cargar_meteo_csv()`
- [ ] **4.** Ejecuta `python main.py` → demo 0: `[OK] load.py` y demo 1 genera `output/chunks.json`
- [ ] **5.** Inspecciona chunks en consola y en `output/chunks.json`
- [ ] **6.** Experimento: cambia `CHUNK_SIZE` / `CHUNK_OVERLAP` en `config.py`, re-ejecuta y anota diferencias
- [ ] **7.** Completa `entregables/estrategia_chunking.md` (con números reales)

### Fase 2 — Embeddings y reflexión

- [ ] **8.** Configura `GEMINI_API_KEY` en `.env`
- [ ] **9.** Ejecuta `python main.py` → demo 2 genera `output/embeddings.json`
- [ ] **10.** Inspecciona `embeddings.json` (modelo, dimensiones, correspondencia con chunks)
- [ ] **11.** Completa `entregables/reflexion_pipeline.md`
- [ ] **12.** Demo 0 muestra `[OK] entregables/`

### Archivos que **no debes modificar**

`main.py`, `config.py`, `clean.py`, `chunk.py`, `embed.py`, `pipeline.py`, `gemini_auth.py`, `verificar.py`

Puedes **editar valores** en `config.py` (p. ej. `CHUNK_SIZE`) para experimentar; no reescribas `chunk.py` ni `embed.py`.

---

## Corpus en `data/`

| Archivo | Rol |
|---------|-----|
| `faq_calidad_aire.md` | Preguntas frecuentes (estilo proveedor de datos) |
| `guia_calidad_aire.txt` | Resumen de campos |
| `descripcion-fichero-open-data-meteorologico-v2.pdf` | Documentación oficial |
| `calidad_aire_datos_meteo_mes.csv` | Mediciones horarias |

---

## Requisitos

- Python 3.10+
- `GEMINI_API_KEY` en [Google AI Studio](https://aistudio.google.com/apikey)

## Entorno virtual

**Linux / macOS / Git Bash:**

```bash
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
cp .env.example .env
python main.py
```

**Windows (PowerShell):**

```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
pip install -r requirements.txt
copy .env.example .env
python main.py
```

---

## Estructura del proyecto

```text
.
├── README.md
├── requirements.txt
├── config.py              # CHUNK_SIZE, MAX_FILAS_CSV, MAX_CHUNKS_EMBED, MAGNITUDES
├── load.py                # ← Fase 1: ingesta del CSV
├── clean.py, chunk.py     # dados
├── pipeline.py, embed.py  # dados
├── main.py, verificar.py
├── data/
├── entregables/
│   ├── estrategia_chunking.md
│   └── reflexion_pipeline.md
└── output/
```

---

## FASE 1 — Implementar `load.py`

### Objetivo

Convertir filas del CSV meteorológico en `Document` legibles, con metadata útil.

### Pistas

**`nombre_magnitud(codigo)`** — consulta `MAGNITUDES` en `config.py` (81=viento, 83=temperatura…).

**`fila_meteo_a_texto(fila)`** — ejemplo de salida esperada:

```text
Medición: Temperatura (código 83)
Municipio: 102
Estación: 1
Punto de muestreo: 28102001_83_89
Fecha: 2026-7-1
Valores horarios:
  01:00 → 2,8 (validación V)
  02:00 → 3,3 (validación V)
  ...
```

**`cargar_meteo_csv(ruta)`**:

- `pd.read_csv(ruta, sep=";", encoding="utf-8")`
- Limita filas con `MAX_FILAS_CSV` (100 por defecto)
- Un `Document` por fila válida
- `metadata`: `tipo="meteo_medicion"`, `magnitud`, `municipio`, `estacion`, `punto_muestreo`, `source`

### Estudiar resultados (sin tocar `chunk.py`)

Tras la ingesta, revisa en consola y en `output/chunks.json`:

- Cuántos chunks sale de **FAQ**, **PDF** y **CSV**
- Un fragmento de FAQ vs uno de CSV (magnitud 83)
- Efecto de cambiar **`CHUNK_SIZE`** / **`CHUNK_OVERLAP`** en `config.py` (obligatorio en el entregable)

### Criterios de aceptación (Fase 1)

- [ ] Demo 0: `[OK] load.py`
- [ ] `output/chunks.json` con chunks de FAQ, PDF y CSV
- [ ] `estrategia_chunking.md` con experimento de parámetros y muestras de chunks

---

## FASE 2 — Embeddings y entregables

### Objetivo

Generar vectores con el pipeline dado y **reflexionar** sobre los artefactos.

### Qué inspeccionar

- Modelo y dimensiones en `embeddings.json`
- Correspondencia texto ↔ vector ↔ metadata
- Por qué `MAX_CHUNKS_EMBED` puede ser menor que el total de chunks

### Criterios de aceptación (Fase 2)

- [ ] `output/embeddings.json` generado
- [ ] `reflexion_pipeline.md` con datos concretos de tus JSON
- [ ] Demo 0: `[OK] entregables/`

---

## Qué ver en consola

### Con load.py pendiente

```text
0) Verificación (sin API)
  [PENDIENTE — load.py]
    - Implementa fila_meteo_a_texto() en load.py
  [PENDIENTE — entregables] (Fase 2)
```

### Fase 1 completa

```text
  [OK] load.py (ingesta CSV meteorológico)
1) Pipeline ingesta → output/chunks.json
  Cargado: faq_calidad_aire.md (1 documento(s))
  ...
  Chunks generados: ...
  Chunks por fuente:
    faq_calidad_aire.md: 1
    ...
```

---

## Errores frecuentes

| Lo que ves | Qué hacer |
|------------|-----------|
| Falta CSV en `data/` | Comprueba que `calidad_aire_datos_meteo_mes.csv` está en `data/` |
| CSV vacío / 0 docs | Revisa `sep=";"` y encoding |
| Decimales raros | El CSV usa coma decimal; no conviertas a float si no hace falta |
| 429 en embeddings | Baja `MAX_CHUNKS_EMBED` en `config.py` |
| API 401 | Revisa `GEMINI_API_KEY` en `.env` |

---

## Qué NO tienes que hacer

- Implementar `chunk.py` ni `embed.py`
- Indexar el JSON del workout
- ChromaDB ni retrieval
- Generar respuestas con LLM

---

## Experimentos opcionales

- Sube `MAX_FILAS_CSV` a `None` y compara tiempo de ingesta
- Añade en metadata la fecha como string `YYYY-MM-DD`
- **Otro proveedor (Hugging Face):** embeddea el mismo texto de un chunk con un modelo de [Hugging Face](https://huggingface.co/sentence-transformers) y compara dimensiones con Gemini
