![Cabecera](../../../assets/cabecera_gemini.png)

# Proyecto ejemplo: Context Engineering (Smart Study Assistant)

Demo ejecutable que integra **uso de prompts**, **selección de contexto**, **historial**, **perfil de usuario**, **presupuesto de tokens** y **resumen periódico**. 

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
├── config.py           # MODEL, WINDOW, RESUMIR_CADA, MAX_TOKENS_INPUT
├── prompts.py          # build_study_prompt, build_resumen_prompt
├── gemini_auth.py      # load_dotenv + getpass
├── gemini_client.py    # llamadas, count_tokens, safe_generate
├── context.py          # cargar FAQ, seleccionar entradas (sin embeddings)
├── state.py            # historial, summary, user_profile
├── logic.py            # turnos, resumen, respuesta_ok/error
├── data/
│   └── faq.json
└── main.py
```

---

## Qué hace la demo

1. **Selecciona FAQ** — dada una consulta, elige 1 entrada relevante en Python (no inyecta todo el JSON).
2. **Chat con memoria** — perfil persistente + últimos turnos; responde “¿cómo me llamo?”.
3. **Compresión** — tras varios turnos genera `summary` y sigue con `summary + ventana`; imprime métricas de tokens y latencia.

---

## Orden recomendado al explorar el código

1. `data/faq.json` — datos de referencia.
2. `context.py` — cómo se elige qué entra al prompt.
3. `state.py` — qué se guarda entre turnos.
4. `prompts.py` — cómo se ensambla el contexto final.
5. `gemini_client.py` — llamada + métricas + guardia de tokens.
6. `logic.py` — cuándo resumir y cómo procesar un turno.
7. `main.py` — las tres escenas de la demo.

---

## Experimentar

- Cambia `WINDOW` y `RESUMIR_CADA` en `config.py` y observa tokens en consola.
- Añade una entrada en `faq.json` y prueba una consulta nueva.
- En `main.py`, pregunta algo que no esté en el FAQ y mira qué pasa en la escena 1.
- Baja `MAX_TOKENS_INPUT` para forzar el error de presupuesto.
