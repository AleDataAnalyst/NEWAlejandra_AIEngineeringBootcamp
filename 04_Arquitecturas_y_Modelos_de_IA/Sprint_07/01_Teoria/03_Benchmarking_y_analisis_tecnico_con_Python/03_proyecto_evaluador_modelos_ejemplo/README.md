![Cabecera](../../assets/cabecera_gemini.png)

# Proyecto ejemplo: evaluador de modelos

Demo ejecutable que integra **dataset de preguntas**, **benchmark multi-modelo**, **log CSV** e **informe Markdown**.

**Requisitos:** Python 3.10+.

**API key:** [Google AI Studio](https://aistudio.google.com/). No la pegues en el código ni la subas a Git.

---

## Instalación y ejecución

Desde esta carpeta (donde está `main.py`):

```bash
# 1) (Opcional) entorno virtual
python -m venv .venv

# Windows (PowerShell)
.venv\Scripts\Activate.ps1

# macOS / Linux / Git Bash
source .venv/bin/activate

# 2) Dependencias
pip install -r requirements.txt

# 3) API key
cp .env.example .env   # edita tu clave

# 4) Ejecutar benchmark
python main.py
```

Si no creas `.env`, `gemini_auth.py` pide la clave con `getpass` al arrancar.

En Windows, si `python` no funciona: `py -3 main.py`.

---

## Estructura

```text
.
├── README.md
├── requirements.txt
├── .gitignore          # excluye .env, .venv, output/, etc.
├── .env.example
├── config.py           # MODELS, TEMPERATURE, rutas
├── gemini_auth.py
├── gemini_client.py    # llamada + métricas por modelo
├── benchmark.py        # bucle pregunta × modelo
├── report.py           # CSV + report.md
├── data/
│   └── preguntas.json
├── output/             # generado (no en Git)
└── main.py
```

---

## Qué hace la demo

1. Carga preguntas desde `data/preguntas.json`.
2. Para cada pregunta ejecuta todos los modelos en `config.MODELS`.
3. Registra latencia, tokens y respuesta (o error) en CSV.
4. Genera `report_*.md` con medias por modelo.

---

## Orden recomendado al explorar el código

1. `data/preguntas.json` — dataset fijo.
2. `config.py` — modelos candidatos.
3. `gemini_client.py` — métricas por llamada.
4. `benchmark.py` — orquestación.
5. `report.py` — persistencia e informe.
6. `main.py` — punto de entrada.
7. `output/` — resultados del benchmark. Encontrarás unos resultados de ejemplo, pero puedes volver a ejecutar el benchmark para generar nuevos resultados.

---

## Experimentar

- Añade una pregunta al JSON y vuelve a ejecutar.
- Quita un modelo de `MODELS` para acortar el benchmark.
- Compara dos ejecuciones mirando los CSV en `output/`.

## Matriz de decisión (lo que deberías rellenar con tus conclusiones de ejecutar varios modelos)

Resultados del benchmark `benchmark_ejemplo_20260629_103902.csv` (temperatura 0.3, sin errores). Puedes reejecutar el benchmark para generar nuevos resultados.

| Pregunta | Modelo ganador | Por qué | Calidad 1-5 |
|----------|----------------|---------|-------------|
| soporte | gemini-3.1-flash-lite | Responde con empatía y explica el plazo de 48 h; el otro solo pide datos. **641 ms** vs 2 276 ms. | 4 |
| clasificar | gemini-3.1-flash-lite | Ambos aciertan (`TECNICO`), pero lite responde en **399 ms** frente a 1 970 ms. | 5 |
| resumen | gemini-3.1-flash-lite | Las tres viñetas están completas en ambos; lite es igual de claro y **~6× más rápido** (753 ms vs 4 299 ms). | 4 |
| json | gemini-3.1-flash-lite | Devuelve JSON puro; `gemini-2.5-flash` lo envuelve en bloque markdown (```json), incumpliendo el prompt. Lite: **532 ms** vs 1 615 ms. | 5 |
| limite | gemini-3.1-flash-lite | Definición correcta en una frase en ambos; lite responde en **544 ms** vs 3 967 ms. | 4 |

**Medias del informe:** `gemini-2.5-flash` → 2 825 ms / 35,6 tokens salida · `gemini-3.1-flash-lite` → 574 ms / 36,0 tokens salida.

### Conclusión global

En esta ejecución, **`gemini-3.1-flash-lite` es la opción preferida para la aplicación orientada al cliente**: latencia media ~**5× menor** (574 ms vs 2 825 ms) con calidad de respuesta equivalente o superior en las cinco tareas.

- **Velocidad:** lite gana en todas las preguntas; la mayor brecha está en resumen y explicación técnica (4–6× más rápido).
- **Calidad:** clasificación y JSON estructurado salen impecables en lite; en soporte aporta contexto útil (plazo de liquidación) sin alargar la respuesta.
- **Formato:** el único fallo relevante de `gemini-2.5-flash` es no respetar “solo JSON” al añadir fences markdown — crítico si el cliente parsea la salida automáticamente.
- **Recomendación:** usar **`gemini-3.1-flash-lite`** por defecto en flujos interactivos (soporte, clasificación, resúmenes, salidas JSON). Reservar `gemini-2.5-flash` solo si en pruebas futuras aporta ventaja clara en calidad en tareas concretas que compensen el coste de latencia.

