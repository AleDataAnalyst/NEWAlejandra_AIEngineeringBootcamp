# Proyecto ejemplo: Asistente de estudio (Assistant Engineering)

Demo ejecutable que integra **configuración del asistente** (`assistant_config`), **estado de sesión** (`user_state`), **perfiles** (junior / senior / mentor), **selección de FAQ** y el flujo `procesar_turno` con Gemini.

En esta demo puedes ver un **Smart Study Assistant** con **arquitectura de asistente** explícita. Se hace uso de Context Engineering para seleccionar el contexto de la FAQ.

**Requisitos:** Python 3.10+.

**API key:** créala en [Google AI Studio](https://aistudio.google.com/).

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

Si no creas `.env`, `gemini_auth.py` pide la clave con `getpass` al arrancar (entrada oculta, solo esa sesión).

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
├── config.py           # MODEL, ASSISTANT_CONFIG_DEFAULT, PERFILES
├── prompts.py          # build_assistant_prompt
├── gemini_auth.py      # load_dotenv + getpass
├── gemini_client.py    # llamadas, count_tokens, safe_generate
├── context.py          # cargar FAQ, seleccionar entradas (sin embeddings)
├── state.py            # user_profile, historial, actualizar perfil
├── logic.py            # procesar_turno, respuesta_ok/error
├── data/
│   └── faq.json
└── main.py
```

---

## Qué hace la demo

1. **Perfiles** — misma pregunta con `junior`, `senior` y `mentor` (cambia solo `perfil_activo` en la config).
2. **Memoria** — presentación del usuario + “¿cómo me llamo y qué estoy estudiando?”.
3. **FAQ** — selecciona 1 entrada relevante en Python y responde con ese contexto (no inyecta todo el JSON).

---

## Orden recomendado al explorar el código

1. `config.py` — `ASSISTANT_CONFIG_DEFAULT` y diccionario `PERFILES`.
2. `state.py` — qué se guarda entre turnos (`user_profile`, `messages`).
3. `prompts.py` — cómo se ensambla `build_assistant_prompt(...)`.
4. `context.py` — selección de FAQ por keywords.
5. `logic.py` — pipeline `procesar_turno` (validar → prompt → Gemini → actualizar estado).
6. `gemini_client.py` — llamada y guardia de tokens.
7. `main.py` — las tres escenas de la demo.

---

## Experimentar

- Cambia `perfil_activo` en `ASSISTANT_CONFIG_DEFAULT` y vuelve a ejecutar `main.py`.
- Añade un perfil nuevo en `PERFILES` (p. ej. `exam_prep`) y úsalo en la escena 1.
- Edita los turnos de `demo_memoria()` en `main.py` con tu nombre y tema.
- Añade una entrada en `data/faq.json` y prueba una consulta en la escena 3.
- Baja `MAX_TOKENS_INPUT` en `config.py` para forzar el error de presupuesto.