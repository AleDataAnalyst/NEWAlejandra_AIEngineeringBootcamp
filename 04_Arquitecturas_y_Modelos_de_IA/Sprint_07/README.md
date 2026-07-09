![Cabecera](./assets/cabecera_gemini.png)

# 📘 Sprint 07 — Arquitecturas y Modelos de IA

En el Sprint 6 aprendiste a **diseñar asistentes como sistemas** y a **endurecerlos** frente a entradas arbitrarias del usuario.

En este sprint damos el salto de **construir asistentes** a **elegir y evaluar modelos** con criterio de ingeniería: qué familia de modelo usar, qué arquitectura hay detrás, y cómo comparar varios modelos con datos en lugar de intuición.

El sprint se organiza en tres bloques que se construyen uno sobre otro:

---

## 🧩 Bloque 1 — Familias de modelos y arquitecturas

📁 [`01_Teoria/01_Modelos_y_arquitecturas_de_IA/`](./01_Teoria/01_Modelos_y_arquitecturas_de_IA/)
📁 [`02_Workout/01_Modelos_y_arquitecturas_de_IA/`](./02_Workout/01_Modelos_y_arquitecturas_de_IA/)

> **Criterio visual, sin matemáticas:** familias de modelos (texto, embeddings, multimodal), arquitecturas conceptuales (RNN, CNN, Transformer), y cuándo cada una tiene sentido.

### Contenido de teoría

| # | Documento | Qué aprenderás |
|---|-----------|----------------|
| 0 | [Introducción a modelos y arquitecturas](./01_Teoria/01_Modelos_y_arquitecturas_de_IA/00_introduccion_modelos_y_arquitecturas.md) | Panorama del bloque y tabla guía. |
| 1 | [Familias y tipos de modelos](./01_Teoria/01_Modelos_y_arquitecturas_de_IA/01_Familias_y_tipos_de_modelos.md) | Modelos de texto, embeddings, multimodales y casos de uso por familia. |
| 2 | [Arquitecturas de IA (conceptual)](./01_Teoria/01_Modelos_y_arquitecturas_de_IA/02_Arquitecturas_de_IA_conceptual.md) | RNN, CNN, Transformer, y por qué dominan los Transformers. |
| 3 | [Capacidades, limitaciones y coste](./01_Teoria/01_Modelos_y_arquitecturas_de_IA/03_Capacidades_limitaciones_y_coste.md) | Cuándo no usar un modelo, coste asociado y checklist de decisión. |

### Workout

| Notebook / guía | Cubre teoría |
|-----------------|--------------|
| [01_comparacion_conceptual_modelos.ipynb](./02_Workout/01_Modelos_y_arquitecturas_de_IA/01_comparacion_conceptual_modelos.ipynb) | 0 + 1 + 2 + 3 |

Índice detallado de la unidad: [`01_Teoria/01_Modelos_y_arquitecturas_de_IA/readme.md`](./01_Teoria/01_Modelos_y_arquitecturas_de_IA/readme.md)

---

## ⚖️ Bloque 2 — Trade-offs y evaluación de modelos

📁 [`01_Teoria/02_Trade_offs_y_evaluacion_de_modelos/`](./01_Teoria/02_Trade_offs_y_evaluacion_de_modelos/)
📁 [`02_Workout/02_Trade_offs_y_evaluacion_de_modelos/`](./02_Workout/02_Trade_offs_y_evaluacion_de_modelos/)

> **Comparar con datos, no a ojo:** latencia, tokens y criterios de calidad, lanzando las mismas preguntas a distintos modelos bajo las mismas condiciones.

### Contenido de teoría

| # | Documento | Qué aprenderás |
|---|-----------|----------------|
| 0 | [Introducción a trade-offs y evaluación](./01_Teoria/02_Trade_offs_y_evaluacion_de_modelos/00_introduccion_tradeoffs_y_evaluacion.md) | Panorama del bloque. |
| 1 | [Latencia, coste y precisión](./01_Teoria/02_Trade_offs_y_evaluacion_de_modelos/01_Latencia_coste_y_precision.md) | Trade-offs operativos al elegir modelo. |
| 2 | [Robustez, métricas y benchmarks](./01_Teoria/02_Trade_offs_y_evaluacion_de_modelos/02_Robustez_metricas_y_benchmarks.md) | Métricas de evaluación y benchmarks de referencia. |

### Workout

| Notebook / guía | Cubre teoría |
|-----------------|--------------|
| [01_comparar_modelos_mismas_preguntas.ipynb](./02_Workout/02_Trade_offs_y_evaluacion_de_modelos/01_comparar_modelos_mismas_preguntas.ipynb) | 0 + 1 + 2 |

Índice detallado de la unidad: [`01_Teoria/02_Trade_offs_y_evaluacion_de_modelos/readme.md`](./01_Teoria/02_Trade_offs_y_evaluacion_de_modelos/readme.md)

---

## 🛠️ Bloque 3 — Benchmarking y análisis técnico con Python

📁 [`01_Teoria/03_Benchmarking_y_analisis_tecnico_con_Python/`](./01_Teoria/03_Benchmarking_y_analisis_tecnico_con_Python/)
📁 [`02_Workout/03_Benchmarking_y_analisis_tecnico_con_Python/`](./02_Workout/03_Benchmarking_y_analisis_tecnico_con_Python/)

> **Automatizar la comparación:** registrar latencia y tokens en CSV, generar un informe en Markdown y empaquetar todo en un proyecto modular.

### Contenido de teoría

| # | Documento | Qué aprenderás |
|---|-----------|----------------|
| 0 | [Introducción a benchmarking con Python](./01_Teoria/03_Benchmarking_y_analisis_tecnico_con_Python/00_introduccion_benchmarking_python.md) | Pipeline de benchmark y convenciones del bloque. |
| 1 | [Logging, informes y automatización](./01_Teoria/03_Benchmarking_y_analisis_tecnico_con_Python/01_Logging_informes_y_automatizacion.md) | Registro en CSV, generación de informe y automatización del flujo. |

📁 Proyecto ejecutable: [`03_proyecto_evaluador_modelos_ejemplo/`](./02_Workout/03_Benchmarking_y_analisis_tecnico_con_Python/03_proyecto_evaluador_modelos_ejemplo/) — `.venv`, `pip install -r requirements.txt` y `python main.py`.

### Workout

| Notebook / guía | Cubre teoría |
|-----------------|--------------|
| [01_benchmark_y_latencia_ejemplos.ipynb](./02_Workout/03_Benchmarking_y_analisis_tecnico_con_Python/01_benchmark_y_latencia_ejemplos.ipynb) | 0 |
| [02_logging_resultados_ejemplos.ipynb](./02_Workout/03_Benchmarking_y_analisis_tecnico_con_Python/02_logging_resultados_ejemplos.ipynb) | 1 |
| [03_proyecto_evaluador_modelos_ejemplo/](./02_Workout/03_Benchmarking_y_analisis_tecnico_con_Python/03_proyecto_evaluador_modelos_ejemplo/) | 0 + 1 + proyecto |

Índice detallado de la unidad: [`01_Teoria/03_Benchmarking_y_analisis_tecnico_con_Python/readme.md`](./01_Teoria/03_Benchmarking_y_analisis_tecnico_con_Python/readme.md)

---

## ⚙️ Convenciones del sprint

- Teoría y demos en `01_Teoria/` de cada unidad (sin subcarpeta `demos`).
- API: **Google Gemini** (`google-genai`), con varios modelos en las comparativas.
- Las cabeceras de los markdown usan `assets/cabecera_gemini.png` a nivel sprint. Si la carpeta `assets/` está vacía, copia las imágenes desde otro sprint del bootcamp (p. ej. `03_Prompt_&_Context_Engineering/Sprint_05/assets/`).

**Consejo:** durante el desarrollo del proyecto evaluador puedes reducir el número de modelos en `config.py` para no saturar la API; antes de cerrar la práctica, ejecuta `python main.py` con la configuración completa.
