![Cabecera](../../../assets/cabecera_gemini.png)

# Proyecto ejemplo: Prompt Engineering (datos externos + JSON)

En esta demo hablaremos sobre:
- Inyección de datos
- Salidas estructuradas
- Organización de código (`config`, `prompts`, `logic`, `main`).

**Requisitos:** Python 3.10+.

**API key:** créala en [Google AI Studio](https://aistudio.google.com/). No la pegues en el código ni la subas a Git.

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

# 3) API key — copia la plantilla y edita tu clave
# Windows: copy .env.example .env
# macOS/Linux/Git Bash:
cp .env.example .env

# 4) Ejecutar
python main.py
```

Si no creas `.env`, `gemini_auth.py` pide la clave con `getpass` al arrancar (entrada oculta, solo esa sesión), igual que en Sprint 4.

En Windows, si `python` no funciona: `py -3 main.py`.

---

## Estructura

```text
.
├── README.md
├── requirements.txt    # google-genai, python-dotenv
├── .gitignore          # .venv, .env, __pycache__
├── .env.example        # plantilla (sí va al repo)
├── .env                # tu clave real (lo creas tú; no en Git)
├── config.py           # modelo, listas válidas, límites
├── prompts.py          # plantillas y build_*_prompt
├── gemini_auth.py      # load_dotenv + getpass (Sprint 4)
├── gemini_client.py    # llamadas texto / JSON
├── logic.py            # parseo, CSV, clasificación
├── data/
│   └── productos.csv
└── main.py
```

---

## Qué hace la demo

1. **Clasifica** tres mensajes de incidencia → JSON (`category`, `priority`, `summary`) con validación en Python.
2. **Genera ficha** de producto leyendo una fila de `data/productos.csv`.
3. **Recomendaciones** usando un `dict` de clima inyectado en el prompt.

---

## Experimentar

- Cambia un mensaje en `main.py` → `demo_clasificacion()`.
- Añade una fila en `data/productos.csv` y usa otro SKU.
- Edita plantillas en `prompts.py` sin tocar `logic.py`.
