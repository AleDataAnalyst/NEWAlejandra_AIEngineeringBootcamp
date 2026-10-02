![Cabecera](../../../Sprint_11/assets/cabecera_thebridge.png)

# Práctica Sprint 12 — Agente con tools · calidad del aire

**Práctica integradora (Live Review)** del Sprint 12 — tool use, integración y control de tools.

Crearemos un agente sobre **calidad del aire** que **usa tools** (hora, mini-RAG, API Madrid) con allowlist, `max_steps` y traza de tools.

Contrato público del agente:

```text
mensaje → procesar_turno(estado, mensaje, max_steps)
       → run_tool_loop → sintetizar_estado → calcular_done → traza (con tools)
```

> El foco es el **ciclo de tools**: el LLM pide, Python ejecuta (allowlist), y el agente limita (`max_steps`) y registra (traza).

> **Aviso — warning de AFC al ejecutar**  
> Es posible que veáis un mensaje del SDK tipo *“Direct use of automatic function calling (AFC)…”*.  
> **No es un error de vuestro código.** Este proyecto desactiva el AFC y hace el loop **a mano** (`run_tool_loop`) para ver allowlist, traza y `max_steps`. Podéis ignorar el aviso.

### Flujo de un turno (`procesar_turno`) con ciclo de tools

```text
mensaje del usuario
        │
        ▼
¿vacío? ──sí──► respuesta amigable (sin LLM / sin tools) ──► return
        │ no
        ▼
run_tool_loop(...)          ← Gemini FC + tools (max_steps, allowlist)
        │
        ▼
sintetizar_estado(...)      ← Gemini JSON (preferencias / plan / respuesta; sin "done")
        │
        ▼
actualizar_estado(...)
        │
        ▼
calcular_done(...)          ← Python decide done
        │
        ▼
traza.append(..., tools=…)  ← ok | error (+ lista de tools del turno)
        │
        ▼
return estado
```

---

## Empieza aquí

Sigue este orden **de arriba a abajo**:

### Fase 0 — Entorno

- [ ] **1.** Crea el venv, instala dependencias y copia `.env.example` → `.env` con tu `GEMINI_API_KEY`
- [ ] **2.** `python main.py --check` → debe marcar varios `[FAIL]` (aún hay TODOs)

### Fase 1 — Allowlist y validación

- [ ] **3.** Completa `TOOL_REGISTRY`, `validar_args` y `ejecutar_tool` en `src/tools/__init__.py`

### Fase 2 — Loop Function Calling (FC) + orquestación

- [ ] **4.** Completa el TODO de allowlist / `ejecutar_tool` en `src/llm.py` (`run_tool_loop`)
- [ ] **5.** Completa `procesar_turno` y `run_demo` en `src/agent.py`
- [ ] **6.** `python main.py --check` → todo `[OK]`

### Fase 3 — Demostrar tools (CLI)

- [ ] **7.** `python main.py` → mira `traza[].tools` (≥1 tool; ideal ≥2)
- [ ] **8.** `python main.py --max-turns 1 --max-steps 1` → corte por `max_steps`
- [ ] **9.** (Opcional) Wi‑Fi off / bloquear URL → `Fuente: fallback` en el preview

### Fase 4 — Streamlit (app dada)

- [ ] **10.** `streamlit run app.py` (la UI ya llama a `procesar_turno`; no la reimplementes)
- [ ] **11.** Comprueba: chat, expander con traza de tools, sliders `max_turns` / `max_steps`, «Nueva conversación»

### Archivos que **no debes modificar**

En `src/`: `state.py`, `tools/hora_actual.py`, `tools/rag_guia.py`, `tools/api_calidad_aire.py`, `__init__.py` del paquete `src` (sí tocas `tools/__init__.py`).

En la raíz: `main.py`, `app.py`, `verificar.py`, `config.py` (puedes cambiar defaults como `MAX_TURNS_DEFAULT` / `MAX_STEPS_DEFAULT` / `GEMINI_MODEL`), `gemini_auth.py`, `data/*`.

`app.py` viene **dado**. No metas ahí la lógica del agente.

Sí implementas: `src/tools/__init__.py`, el TODO de `src/llm.py`, `src/agent.py`.

---

## Requisitos

- Python 3.10+
- `GEMINI_API_KEY` en [Google AI Studio](https://aistudio.google.com/apikey)

```bash
cd Practica_live_review/01_agente_tools_calidad_aire
python -m venv .venv
source .venv/bin/activate          # Git Bash / macOS / Linux
# .venv\Scripts\Activate.ps1       # Windows PowerShell
pip install -r requirements.txt
cp .env.example .env               # edita tu clave
python main.py --check
```

---

## Estructura

```text
.
├── README.md
├── requirements.txt
├── .env.example
├── config.py              ← dado (modelo, max_turns, max_steps, DEMO_MENSAJES, URL API)
├── gemini_auth.py         ← dado
├── main.py                ← dado (CLI + --check)
├── app.py                 ← dado (Streamlit; cliente de procesar_turno)
├── verificar.py           ← dado
├── .streamlit/config.toml
├── data/
│   ├── guia_calidad_aire.txt   ← corpus del mini-RAG
│   └── aire_fallback.json      ← fallback de la API
└── src/
    ├── __init__.py        ← dado
    ├── state.py           ← dado (crear / actualizar / calcular_done)
    ├── llm.py             ← casi dado (TODO allowlist en el loop)
    ├── agent.py           ← TU IMPLEMENTACIÓN (TODO)
    └── tools/
        ├── __init__.py    ← TU IMPLEMENTACIÓN (allowlist)
        ├── hora_actual.py ← dado
        ├── rag_guia.py    ← dado (mini-RAG léxico)
        └── api_calidad_aire.py  ← dado (API Madrid + fallback)
```

---

## Consultas del agente (y tools)

El agente **aclara** una consulta sobre calidad del aire y cierra con un **plan de consulta**. Para datos usa tools:

| Tool | Rol |
|------|-----|
| `hora_actual` | Fecha/hora local |
| `RAG_buscar_en_guia` | Mini-RAG léxico sobre `guia_calidad_aire.txt` |
| `API_consultar_calidad_aire` | Open data Madrid (tiempo real) + fallback JSON |

| Preferencia | Ejemplo |
|-------------|---------|
| `zona` | centro, Escuelas Aguirre |
| `contaminante` | NO2, PM10, magnitud 8 |
| `tipo_consulta` | `que_mide` / `interpretar` / `comparar` / `general` |

`done=true` (lo decide **Python**) cuando hay las tres preferencias y `plan` con ≥2 ítems. **No** existe tool `marcar_done`.

**No** inventes mediciones ni umbrales oficiales si la tool no los aportó.

### Ejemplo para `--interactivo` (y Streamlit)

Mismo guion que `DEMO_MENSAJES` en `config.py`. Cópialo turno a turno:

**Nota:** el mensaje 1 es corto a propósito (abre el diálogo). El 2 empuja
`hora_actual`; el 3 pide guía + API + preferencias. A partir de ahí el modelo
puede rellenar un `plan` ≥2 → Python pone `done=true` y Streamlit/CLI bloquean.
Si pasa, pulsa **«Nueva conversación»** (o reinicia). El éxito temprano es válido.

```text
1. Quiero info de calidad del aire.
2. Quiero que te centres en la hora actual para contextualizar.
3. Zona centro, contaminante NO2. Consulta la guía y datos de la API de Madrid. El tipo de consulta es interpretar un valor alto.
4. Añade otro paso al plan si falta.
5. Perfecto, adelante con ese plan.
```

**Aclaración:** el guion tiene **5** mensajes a propósito. Si antes del 5 ya hay prefs + plan ≥2, Python pone `done=true` y **el mensaje 5 puede no enviarse**. Eso es éxito temprano, no un tope oculto. Contrasta con `--max-turns 2` (corte por turnos) y `--max-steps 1` (corte de tools **dentro** de un mensaje).

Salir en interactivo: Enter vacío o `salir`. Con `python main.py` (sin `--interactivo`) el CLI usa este guion solo.

---

## Secuencia recomendada

```text
python main.py --check
# Completa allowlist + TODO de llm + agent
python main.py --check
python main.py
python main.py --max-turns 1 --max-steps 1
python main.py --interactivo
streamlit run app.py
```

---

## FASE 1 — Allowlist (`src/tools/__init__.py`)

### Objetivo

Solo se ejecutan tools registradas. Antes de `fn(**args)`, sanear argumentos.

### Pistas

- `TOOL_REGISTRY` debe incluir exactamente: `hora_actual`, `RAG_buscar_en_guia`, `API_consultar_calidad_aire`.
- `validar_args`: hora → `{}`; RAG → `consulta` string; API → `limite` entero 1..10.
- `ejecutar_tool`: si no está en el registro → mensaje de error (no llames a la función).

### Criterios de aceptación

- [ ] `python main.py --check` marca `[OK]` en `TOOL_REGISTRY`, `validar_args`, `ejecutar_tool`
- [ ] `validar_args(..., {"limite": 99})` → `limite` = 10

---

## FASE 2 — Loop FC + `procesar_turno` / `run_demo`

### Objetivo

1. En `run_tool_loop`: si la tool no está en allowlist → `status: "blocked"`; si sí → `ejecutar_tool` y `ok`/`error`.
2. En `procesar_turno`: tools → JSON → `calcular_done` → traza con `tools`.
3. En `run_demo`: recorrer mensajes con `max_turns` (y pasar `max_steps`).

### Pistas

- Early-return de mensaje vacío ya está (no llames al LLM).
- El LLM **no** devuelve `done`.
- La traza del turno debe incluir la lista `tools` que devolvió `run_tool_loop`.
- La tool `API_consultar_calidad_aire` viene **dada** (HTTP + fallback); no la reescribas.

### Criterios de aceptación

- [ ] `--check` → todo `[OK]`
- [ ] `python main.py` → hay entradas en `traza[].tools`
- [ ] Mensaje vacío → respuesta amigable **sin** traza nueva

---

## FASE 3 — Demostrar en CLI

### Objetivo

Ver tools, límites y fallback en la práctica.

### Criterios de aceptación

- [ ] Demo completa: preferencias / plan / `done` razonables; tools visibles en el resumen o JSON
- [ ] `--max-turns 1 --max-steps 1` → en respuesta o resumen aparece corte por `max_steps` (o tools muy limitadas)
- [ ] (Opcional) Fallback visible con `Fuente: fallback`

---

## FASE 4 — Streamlit (`app.py` dado)

No reimplementes la UI: solo arráncala cuando `procesar_turno` funcione.

```bash
streamlit run app.py
```

Prueba el guion de arriba. Mira el expander (**Estado / traza de tools**). Con slider `max_steps=1` y un mensaje que pida guía + API verás el freno de tools. Con `max_turns` bajo verás el freno de mensajes.

### Criterios de aceptación

- [ ] Preferencias / plan / `done` / traza crecen en el expander
- [ ] Sliders `max_turns` y `max_steps` afectan al comportamiento
- [ ] «Nueva conversación» reinicia chat y estado

### Flujo de `app.py`

Streamlit **vuelve a ejecutar todo el script** en cada interacción. La memoria vive en `st.session_state`.

**Dos memorias (importante):**

| Clave | Qué guarda | Para qué |
|-------|------------|----------|
| `messages` | Lista `{role, content}` | Pintar el historial del chat |
| `agent_state` | Preferencias, plan, `done`, `error`, `traza` (con tools) | Que el agente “recuerde” la tarea |

```text
streamlit run app.py
        │
        ▼
┌───────────────────────────────────────┐
│ 1. Sidebar                            │
│    · slider max_turns                 │
│    · slider max_steps                 │
│    · botón «Nueva conversación»       │
└───────────────────────────────────────┘
        │
        ▼
┌───────────────────────────────────────┐
│ 2. Init messages + agent_state        │
└───────────────────────────────────────┘
        │
        ▼
┌───────────────────────────────────────┐
│ 3. Pintar historial (messages)        │
└───────────────────────────────────────┘
        │
        ▼
┌───────────────────────────────────────┐
│ 4. ¿Bloquear input?                   │
│    · done / error / max_turns         │
└───────────────────────────────────────┘
        │
        ▼  (si el usuario escribe)
┌───────────────────────────────────────┐
│ 5. procesar_turno(..., max_steps)     │
│    → agent_state + respuesta (+ plan) │
└───────────────────────────────────────┘
        │
        ▼
┌───────────────────────────────────────┐
│ 6. Expander: prefs / plan / traza     │
└───────────────────────────────────────┘
```

Idea clave: **`app.py` es un cliente**. La lógica está en `procesar_turno` y en las tools.

---

## Qué probar en el proyecto

| Caso | Comando / acción | Éxito cuando… |
|------|------------------|---------------|
| Check | `python main.py --check` | Todo `[OK]` |
| Demo | `python main.py` | Tools en traza; plan / prefs; a menudo `done` |
| Corte steps | `python main.py --max-turns 1 --max-steps 1` | Aviso / corte por `max_steps` |
| Corte turns | `python main.py --max-turns 2` | Para sin terminar el guion; aviso `max_turns` |
| Interactivo | `python main.py --interactivo` + guion | Prefs → tools → plan → `done` |
| Mensaje vacío | Early-return | Sin LLM ni traza nueva |
| Fallback | Sin red o URL rota | `Fuente: fallback` |
| Streamlit | Guion + expander | `agent_state` con `traza[].tools` |

---

## Pistas (no leer antes de intentar)

<details>
<summary>Spoiler — validar_args / ejecutar_tool</summary>

```python
TOOL_REGISTRY = {
    "hora_actual": hora_actual,
    "RAG_buscar_en_guia": RAG_buscar_en_guia,
    "API_consultar_calidad_aire": API_consultar_calidad_aire,
}

# validar_args: ramas por nombre; limite = max(1, min(limite, 10))
# ejecutar_tool: if nombre not in TOOL_REGISTRY → Error; else fn(**validar_args(...))
```

</details>

<details>
<summary>Spoiler — hueco en run_tool_loop</summary>

```python
if nombre not in TOOL_REGISTRY:
    resultado = f"Error: tool '{nombre}' no está permitida."
    status = "blocked"
else:
    resultado = ejecutar_tool(nombre, args)
    status = "error" if resultado.startswith("Error") else "ok"
```

</details>

<details>
<summary>Spoiler — esqueleto de procesar_turno</summary>

```python
n = len(estado.get("traza") or []) + 1
try:
    texto_tools, traza_tools = run_tool_loop(mensaje, max_steps=max_steps)
    cambios = sintetizar_estado(estado, mensaje, texto_tools)
    estado = actualizar_estado(estado, cambios)
    if not estado.get("respuesta"):
        estado = {**estado, "respuesta": texto_tools}
    estado = calcular_done(estado)
    estado.setdefault("traza", []).append(
        {
            "turno": n,
            "mensaje": mensaje,
            "status": "ok",
            "done": estado.get("done"),
            "tools": traza_tools,
        }
    )
except Exception as e:
    # error + respuesta amigable + traza status "error", tools=[]
return estado
```

</details>

<details>
<summary>Spoiler — esqueleto de run_demo</summary>

```python
msgs = list(mensajes) if mensajes is not None else list(config.DEMO_MENSAJES)
limit = max_turns if max_turns is not None else config.MAX_TURNS_DEFAULT
estado = crear_estado(msgs[0] if msgs else "")

for mensaje in msgs[:limit]:
    if estado.get("done") or estado.get("error"):
        break
    estado = procesar_turno(estado, mensaje, max_steps=max_steps)

# Si cortaste por max_turns (sin done/error): aviso en respuesta
return estado
```

</details>

---

## Criterio de cierre

Puedes explicar en voz alta:

1. Qué hace **`procesar_turno(estado, mensaje, max_steps)`** y qué devuelve.
2. Quién **pide** la tool y quién la **ejecuta**.
3. Para qué sirve la **allowlist** y el status `blocked`.
4. Diferencia **`max_steps`** vs **`max_turns`**.
5. Por qué **`done`** lo calcula Python (no es una tool).
6. Qué miras en **`traza[].tools`** (`step`, `tool`, `args`, `status`, `preview`).
7. Qué vive en **`messages`** vs **`agent_state`** en Streamlit.

---

## Experimentos opcionales (si sobra tiempo)

Si te sobra tiempo en la sesión (o quieres practicar en casa), prueba **1 o 2**. Anota en 2–3 líneas qué viste.

### Control de tools

- [ ] **`max_steps = 1`** — CLI o slider Streamlit + mensaje que pida guía y API. ¿Cuántas tools en la traza? ¿Sale el aviso de `max_steps`?
- [ ] **Allowlist** — Quita temporalmente una tool de `TOOL_REGISTRY`, reinicia y fuerza al modelo a pedirla. ¿`status: "blocked"`? (luego restaura)
- [ ] **Fallback API** — Desconecta la red o pon una URL mala en `config.MADRID_AIRE_URL`. ¿`Fuente: fallback`?

### Estado y traza

- [ ] **Inspeccionar tools** — Tras un turno con tools, mira `traza[-1]["tools"]`: `step`, `args`, `preview`.
- [ ] **Multi-tool** — Un mensaje que pida guía + API (+ hora). ¿≥2 entradas en `tools`?
- [ ] **Dos memorias** — En Streamlit, compara el chat (`messages`) con el expander (`agent_state`).

### Robustez

- [ ] **Mensaje vacío** — Enter vacío en interactivo. ¿Sin traza nueva?
- [ ] **API key inválida** — Clave mala en `.env`. ¿`error` usable sin tumbar CLI/Streamlit?
- [ ] **RAG vacío** — Pregunta algo que no esté en la guía (p. ej. “ópera en Marte”). ¿La tool dice que no encontró nada?

### Extra

- [ ] **Cambiar `DEMO_MENSAJES`** — Reordena el guion en `config.py` y ejecuta `python main.py`.
- [ ] **Nueva conversación** — Cierra un plan (`done`) y resetea en Streamlit. ¿Chat y estado limpios?
