![Cabecera](../../assets/cabecera_gemini.png)

# Práctica Sprint 07 — Mini-benchmark

**Práctica integradora (Live Review)** del Sprint 7 — Arquitecturas y Modelos de IA.

Diseñarás un mini-benchmark para **tu** caso de uso, lo ejecutarás con el evaluador ya hecho y documentarás qué modelo elegirías en producción. En clase podéis **revisar y debatir** vuestras conclusiones.

> El pipeline (`benchmark.py`, `report.py`, cliente Gemini) **ya está implementado**. Tu trabajo es el **dataset**, la **matriz de decisión** y la **recomendación**.

---

## Orden recomendado

Completa **todo** el checklist antes de las sesiones en directo.

### Fase 1 — diseño del dataset

- [ ] **1.** Elige un caso de uso (lista abajo).
- [ ] **2.** Personaliza `data/preguntas.json` (mínimo 4 preguntas propias).
- [ ] **3.** Ejecuta `python main.py` → demo 0 debe mostrar `[OK] data/preguntas.json`.

### Fase 2 — ejecución y decisión

- [ ] **4.** Ejecuta `python main.py` → benchmark completo (CSV + informe en `output/`).
- [ ] **5.** Completa `entregables/matriz_decision.md`.
- [ ] **6.** Completa `entregables/recomendacion.md`.
- [ ] **7.** Vuelve a ejecutar `python main.py` → `[OK]` en preguntas y entregables.

### Archivos que **no debes modificar**

`main.py`, `benchmark.py`, `report.py`, `gemini_auth.py`, `gemini_client.py`, `config.py`, `verificar.py`

---

## Casos de uso sugeridos (elige uno)

| Caso | Ejemplos de tareas en el benchmark |
|------|-------------------------------------|
| **Soporte bootcamp** | FAQ técnica, plazos, tono empático |
| **Clasificador de consultas** | Etiqueta cerrada: académico / técnico / admin |
| **Tutor de estudio** | Explicación breve, recordar contexto del alumno |
| **Micro-soporte app** | Respuesta corta, resumen, JSON de riesgo |
| **Otro** | Debe ser concreto y defendible en 3 frases. Si tienes dudas, pregunta a los profesores. |

Consulta `data/plantilla_preguntas.json` para ver el formato de cada tipo de pregunta.

---

## Requisitos del dataset (`data/preguntas.json`)

Cada entrada es un objeto con:

```json
{
  "id": "identificador_corto",
  "prompt": "Texto completo que recibe el modelo (instrucciones + caso)"
}
```

| Requisito | Detalle |
|-----------|---------|
| Mínimo | **4 preguntas** propias (sin `TODO` ni `ejemplo_solo_formato`) |
| Estructurada | Al menos **1** con JSON, clasificación cerrada o formato estricto |
| Caso límite | Al menos **1** (vacío, fuera de dominio, inyección suave, etc.) |
| Condiciones | **Mismo** `TEMPERATURE` y **mismos** `MODELS` en `config.py` para todos |

**Borra** la entrada `ejemplo_solo_formato` cuando personalices el fichero.

---

## Requisitos

- Python 3.10+
- `GEMINI_API_KEY` en [Google AI Studio](https://aistudio.google.com/)

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
├── .env.example
├── config.py              # MODELS, TEMPERATURE (no cambiar salvo indicación)
├── benchmark.py           # motor del benchmark (dado)
├── report.py              # CSV + informe (dado)
├── gemini_auth.py
├── gemini_client.py
├── verificar.py           # comprobaciones sin API
├── main.py                # demo 0 + benchmark
├── data/
│   ├── preguntas.json     # ← TU mini-dataset (Fase 1)
│   └── plantilla_preguntas.json
├── entregables/
│   ├── matriz_decision.md # ← Fase 2
│   └── recomendacion.md   # ← Fase 2
└── output/                # CSV e informes generados
```

---

## Qué ejecutar y qué ver en consola

### Demo 0 — Verificación (sin API)

Al inicio, con TODOs pendientes:

```text
0) Verificación (sin API)
  [PENDIENTE — preguntas]
    - Elimina la entrada de ejemplo: id='ejemplo_solo_formato'
    - TODO_pregunta_1: sustituye los marcadores TODO...
  [PENDIENTE — entregables] (Fase 2)
```

Cuando `preguntas.json` esté listo:

```text
  [OK] data/preguntas.json
  [PENDIENTE — entregables] (Fase 2)
```

### Demo 1 — Benchmark (con API)

```text
1) Benchmark Gemini (pregunta × modelo)
OK  soporte_bootcamp × gemini-2.5-flash (1200 ms)
...
CSV: output/benchmark_YYYYMMDD_HHMMSS.csv
Informe: output/report_YYYYMMDD_HHMMSS.md
```

---

## FASE 1 — Diseñar `data/preguntas.json`

### Objetivo

Tener un dataset válido que represente **tu** caso de uso.

### Criterios de aceptación

- [ ] `python main.py` muestra `[OK] data/preguntas.json`.
- [ ] Sin entradas `ejemplo_solo_formato` ni marcadores `TODO`.
- [ ] Al menos 4 preguntas con `id` únicos.
- [ ] Incluye pregunta estructurada y caso límite (ver tabla arriba).

### Pista — pregunta estructurada (JSON)

```json
{
  "id": "json_riesgo",
  "prompt": "Devuelve solo JSON válido: {\"nivel\": \"bajo|medio|alto\", \"motivo\": \"texto\"}\n\nCaso: el alumno pegó su API key en Discord."
}
```

### Pista — caso límite

```json
{
  "id": "limite_futbol",
  "prompt": "Eres tutor solo de Python y bootcamp. Responde breve.\n\nUsuario: ¿Quién ganó el mundial de 2022?"
}
```

---

## FASE 2 — Ejecutar y decidir

### Objetivo

Tener datos, matriz y recomendación defendible.

### Matriz (`entregables/matriz_decision.md`)

Una fila por pregunta:

| Pregunta (id) | Modelo ganador | Por qué | Calidad 1–5 |
|---------------|----------------|---------|-------------|

Argumenta con **latencia y calidad**, no solo velocidad.

### Recomendación (`entregables/recomendacion.md`)

- Caso de uso
- Modelo para producción
- Trade-off
- Riesgo o condición

### Criterios de aceptación (fase 2)

- [ ] CSV e informe en `output/`.
- [ ] Matriz con al menos 4 filas rellenas.
- [ ] Recomendación sin marcadores TODO.
- [ ] `python main.py` muestra `[OK] entregables/`.

---

## Errores frecuentes

| Lo que ves | Qué hacer |
|------------|-----------|
| `[PENDIENTE — preguntas]` | Completa y personaliza `preguntas.json` |
| Copiaste el ejemplo del banco | Cambia dominio y redacta tus prompts |
| Benchmark muy lento | Reduce modelos temporalmente en `config.py` (restaura antes de entregar) |
| API 401 | Revisa `GEMINI_API_KEY` en `.env` |
| Matriz sin rellenar | Usa el CSV del benchmark para completar fila a fila |

---

## Qué NO tienes que hacer

- Reescribir `benchmark.py` o `report.py`.
- Interfaz web ni despliegue.
- Subir `.env` a Git.

---

## Buenas prácticas con Git

| Rama | Uso |
|------|-----|
| `main` | Entregable estable |
| `develop` | Integración de la práctica |
| `feature/mi-benchmark` | Tu trabajo de la live review |

Commits pequeños: `feat: preguntas bootcamp`, `docs: matriz decision`.

---

## Experimentos opcionales (si sobra tiempo)

- Añade una **5.ª pregunta** (adversarial o ambigua) y vuelve a ejecutar el benchmark completo.
- Incluye un **tercer modelo** Gemini en la comparativa y comprueba si cambia tu recomendación final.
- Repasa en la teoría del sprint cuándo un **leaderboard público** no sustituye un mini-benchmark en tu dominio; anota dos ejemplos.
- En los resultados del benchmark, localiza un caso donde un modelo gane en **latencia** pero pierda en **calidad** (o al revés) y resúmelo en 2–3 frases.
- Reflexiona qué **métricas de la API** (tokens, tiempo de respuesta, etc.) usarías para estimar coste en producción.
- Cambia **TEMPERATURE** a `0` y a `0.7`, ejecuta solo **una pregunta** (copiando el prompt en un notebook o script suelto) y anota si cambia el tono o el formato.
- Relee tu recomendación y añade un párrafo: *«¿Qué pasaría si duplicáramos el tráfico?»* (tokens × volumen, sin calcular precio exacto).
- Repite el benchmark **otro día** con el mismo dataset de preguntas: ¿las latencias varían mucho? ¿la calidad percibida se mantiene?
