<<<<<<< HEAD
![Cabecera](../../assets/cabecera_agentes.png)
=======
![Cabecera](../../assets/cabecera_thebridge.png)
>>>>>>> main

# Práctica Sprint 11 — Agente calidad del aire

**Práctica integradora (Live Review)** del Sprint 11 — Agent Foundations.

Crearemos un agente básico sobre **calidad del aire**. El agente mantiene estado, conversa y decide cuándo parar. **Sin RAG ni tools** en este ejercicio.

Contrato público del agente:

```text
mensaje → procesar_turno(estado, mensaje) → AgentState (+ done + traza)
```

> El foco es el **loop de agente**: estado, `max_turns` y Streamlit como cliente.

> **Aviso — warning de AFC al ejecutar**  
> Es posible que veáis un mensaje del SDK tipo *“Direct use of automatic function calling (AFC) in Models.generate_content is not recommended…”*.  
> **No es un error de vuestro código.** Este proyecto **no usa tools** ni function calling; es un aviso del SDK de Gemini al llamar a `generate_content`. Podéis ignorarlo; el agente sigue funcionando.

### Flujo de un turno (`procesar_turno`)

```text
mensaje del usuario
        │
        ▼
¿vacío? ──sí──► respuesta amigable (sin LLM) ──► return
        │ no
        ▼
preguntar_al_modelo(estado, mensaje)   ← Gemini → JSON (sin "done")
        │
        ▼
actualizar_estado(...)                 ← preferencias, plan, respuesta
        │
        ▼
calcular_done(...)                     ← Python decide done
        │
        ▼
traza.append(...)                      ← ok | error
        │
        ▼
return estado
```

Clientes del mismo contrato: `main.py` (CLI) y `app.py` (Streamlit). El detalle de la UI está en la **Fase 3**.

---

## Empieza aquí

Sigue este orden **de arriba a abajo**:

### Fase 0 — Entorno

- [ ] **1.** Crea el venv, instala dependencias y copia `.env.example` → `.env` con tu `GEMINI_API_KEY`
- [ ] **2.** `python main.py --check` → debe marcar `[FAIL]` en `procesar_turno` / `run_demo` (aún no implementados)

### Fase 1 — Un turno (`procesar_turno`)

- [ ] **3.** Completa `procesar_turno` en `src/agent.py` (LLM → `actualizar_estado` → `calcular_done` → traza + manejo de error)
- [ ] **4.** `python main.py --interactivo` → escribe 1–2 mensajes y mira preferencias / `done` / traza

### Fase 2 — Demo con `max_turns` (`run_demo`)

- [ ] **5.** Completa `run_demo` en `src/agent.py`
- [ ] **6.** `python main.py` → `done: true`, plan ≥2 ítems, varios turnos en traza
- [ ] **7.** `python main.py --max-turns 2` → corte por `max_turns` (aviso en respuesta)
- [ ] **8.** `python main.py --check` → todo `[OK]`

### Fase 3 — Streamlit (app dada)

- [ ] **9.** `streamlit run app.py` (la UI ya llama a `procesar_turno`; no la reimplementes)
- [ ] **10.** Comprueba: chat multi-turno, expander con `agent_state`, slider `max_turns`, «Nueva conversación»

### Archivos que **no debes modificar**

En `src/`: `state.py`, `llm.py`, `__init__.py`.

En la raíz: `main.py`, `app.py`, `verificar.py`, `config.py` (puedes cambiar valores como `MAX_TURNS_DEFAULT` / `GEMINI_MODEL`), `gemini_auth.py`.

`app.py` viene **dado**. No metas ahí la lógica del agente.

---

## Requisitos

- Python 3.10+
- `GEMINI_API_KEY` en [Google AI Studio](https://aistudio.google.com/apikey)

```bash
cd Practica_live_review/01_agente_calidad_aire_SOLUTION
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
├── config.py              ← dado (modelo, max_turns, DEMO_MENSAJES)
├── gemini_auth.py         ← dado
├── main.py                ← dado (CLI + --check)
├── app.py                 ← dado (Streamlit; cliente de procesar_turno)
├── verificar.py           ← dado
├── .streamlit/config.toml
└── src/
    ├── __init__.py        ← dado
    ├── state.py           ← dado (crear / actualizar / calcular_done)
    ├── llm.py             ← dado (preguntar_al_modelo; JSON sin done)
    └── agent.py           ← TU IMPLEMENTACIÓN (TODO)
```

---

## Consultas del agente

El agente **aclara** una consulta sobre calidad del aire y cierra con un **plan de consulta** genérico.

| Preferencia | Ejemplo |
|-------------|---------|
| `zona` | centro, Escuelas Aguirre |
| `contaminante` | NO2, PM10, magnitud 83 |
| `tipo_consulta` | `que_mide` / `interpretar` / `comparar` / `general` |

`done=true` (lo decide **Python**) cuando hay las tres preferencias y `plan` con ≥2 ítems.

**No** inventes mediciones ni umbrales oficiales: este ejercicio no tiene datos ni corpus.

### Ejemplo para `--interactivo` (y Streamlit)

Mismo guion que `DEMO_MENSAJES` en `config.py`. Cópialo turno a turno:

```text
1. Quiero orientarme sobre calidad del aire en Madrid.
2. Me interesa el NO2 o la magnitud 83.
3. Zona centro, cerca de Escuelas Aguirre.
4. Quiero entender qué significa un valor alto.
5. Sí, adelante con el plan de consulta.
```

**Aclaración:** el guion tiene **5** mensajes a propósito. Si en el turno 4 el modelo ya rellena `plan` (≥2) y hay las tres preferencias, Python pone `done=true` y **el mensaje 5 no se llega a enviar**. No es un tope de 4 turnos (`MAX_TURNS_DEFAULT` es 8): es el guardrail de éxito temprano. El guion propone pasos; el estado decide si se consumen. Contrasta con `--max-turns 2` (corte por tope, no por `done`).

Salir: Enter vacío o `salir`. Con `python main.py` (sin `--interactivo`) el CLI usa este guion solo.

---

## Secuencia recomendada

```text
python main.py --check
# Completa procesar_turno
python main.py --interactivo
# Completa run_demo
python main.py
python main.py --max-turns 2
python main.py --check
streamlit run app.py
```

---

## FASE 1 — `procesar_turno`

### Objetivo

Un mensaje → LLM → estado actualizado → `done` en Python → `traza`. Si falla API/JSON, `error` sin tumbar.

### Pistas

- Early-return de mensaje vacío ya está (no llames al LLM).
- Flujo feliz: `preguntar_al_modelo` → `actualizar_estado` → `calcular_done` → `traza.append(...)`.
- El LLM **no** devuelve `done`.

### Criterios de aceptación

- [ ] `--interactivo` responde turno a turno
- [ ] Tras zona + contaminante + tipo + confirmación → `done: true`
- [ ] Mensaje vacío → respuesta amigable **sin** traza nueva

---

## FASE 2 — `run_demo`

### Objetivo

Recorrer `DEMO_MENSAJES` con tope `max_turns`.

### Criterios de aceptación

- [ ] `python main.py` → `done: true`, plan ≥2
- [ ] `python main.py --max-turns 2` → `corte: max_turns`
- [ ] `python main.py --check` → todo `[OK]`

---

## FASE 3 — Streamlit (`app.py` dado)

No reimplementes la UI: solo arráncala cuando `procesar_turno` funcione.

```bash
streamlit run app.py
```

En el chat de la web prueba **los mismos mensajes** del guion de arriba (o de `DEMO_MENSAJES` en `config.py`):

```text
1. Quiero orientarme sobre calidad del aire en Madrid.
2. Me interesa el NO2 o la magnitud 83.
3. Zona centro, cerca de Escuelas Aguirre.
4. Quiero entender qué significa un valor alto.
5. Sí, adelante con el plan de consulta.
```

**Misma aclaración:** si en el 4 ya hay `done`, el chat se bloquea y el 5 no se escribe (éxito temprano, no límite oculto). Mira el expander (preferencias / plan / `done` / traza). Con el slider `max_turns` bajo (p. ej. 2) verás el otro corte: tope sin `done`.

### Criterios de aceptación

- [ ] Preferencias crecen en el expander
- [ ] Con `max_turns` bajo, el chat se bloquea al tope
- [ ] «Nueva conversación» reinicia chat y estado

### Flujo de `app.py`

Streamlit **vuelve a ejecutar todo el script** en cada interacción (mensaje, slider, botón). Por eso la memoria vive en `st.session_state`, no en variables normales.

**Dos memorias (importante):**

| Clave | Qué guarda | Para qué |
|-------|------------|----------|
| `messages` | Lista `{role, content}` | Pintar el historial del chat |
| `agent_state` | Preferencias, plan, `done`, `error`, `traza` | Que el agente “recuerde” la tarea |

```text
streamlit run app.py
        │
        ▼
┌───────────────────────────────────────┐
│ 1. Sidebar                            │
│    · slider max_turns                 │
│    · botón «Nueva conversación»       │
│      → resetea messages + agent_state │
│      → st.rerun()                     │
└───────────────────────────────────────┘
        │
        ▼
┌───────────────────────────────────────┐
│ 2. Si no existen aún:                 │
│    · messages  ← saludo inicial       │
│    · agent_state ← crear_estado("")   │
└───────────────────────────────────────┘
        │
        ▼
┌───────────────────────────────────────┐
│ 3. Pintar el historial (messages)     │
└───────────────────────────────────────┘
        │
        ▼
┌───────────────────────────────────────┐
│ 4. ¿Bloquear el input?                │
│    · done o error  → chat cerrado     │
│    · len(traza) >= max_turns → aviso  │
└───────────────────────────────────────┘
        │
        ▼  (solo si el usuario escribe)
┌───────────────────────────────────────┐
│ 5. Un turno                           │
│    · guarda el mensaje del usuario    │
│      en messages                      │
│    · estado = procesar_turno(…)       │  ← TU código en src/agent.py
│    · guarda agent_state               │
│    · muestra respuesta (+ plan)       │
│    · guarda la respuesta del agente   │
│      en messages                      │
└───────────────────────────────────────┘
        │
        ▼
┌───────────────────────────────────────┐
│ 6. Expander debug                     │
│    preferencias / plan / done / traza │
└───────────────────────────────────────┘
```

Idea clave: **`app.py` es un cliente**. La lógica del agente está en `procesar_turno`; la UI solo muestra y guarda estado entre reruns.

---

## Qué probar en el proyecto

| Caso | Comando / acción | Éxito cuando… |
|------|------------------|---------------|
| Interactivo | `python main.py --interactivo` + guion de arriba | Preferencias → plan → `done: true` (a menudo en el turno 4; el 5 puede no enviarse) |
| Demo completa | `python main.py` | `done: true`, plan ≥2; traza con 4–5 turnos (5 no siempre) |
| Corte | `python main.py --max-turns 2` | Para sin `done`; aviso de `max_turns` |
| Mensaje vacío | Early-return | Respuesta amigable sin LLM |
| Check | `python main.py --check` | Todo `[OK]` |
| Streamlit | Chat con el guion de 5 msgs + expander | `agent_state` ≠ solo el historial; si `done` en el 4, chat bloqueado |

---

## Pistas (no leer antes de intentar)

<details>
<summary>Spoiler — esqueleto de procesar_turno</summary>

```python
traza_actual = estado.get("traza", [])
n = len(traza_actual) + 1
try:
    cambios = preguntar_al_modelo(estado, mensaje)
    estado = actualizar_estado(estado, cambios)
    estado = calcular_done(estado)
    estado.setdefault("traza", []).append(
        {"turno": n, "mensaje": mensaje, "status": "ok", "done": estado.get("done")}
    )
except Exception as e:
    estado = dict(estado)
    estado["error"] = str(e)
    # … respuesta amigable + traza error …
return estado
```

</details>

<details>
<summary>Spoiler — esqueleto de run_demo</summary>

```python
if mensajes is not None:
    msgs = list(mensajes)
else:
    msgs = list(config.DEMO_MENSAJES)

if max_turns is not None:
    limit = max_turns
else:
    limit = config.MAX_TURNS_DEFAULT

estado = crear_estado(msgs[0] if msgs else "")

for mensaje in msgs[:limit]:
    if estado.get("done") or estado.get("error"):
        break
    estado = procesar_turno(estado, mensaje)

# Si cortaste por max_turns (sin done/error): aviso en respuesta
return estado
```

</details>

---

## Criterio de cierre

Puedes explicar en voz alta:

1. Qué hace **`procesar_turno(estado, mensaje)`** y qué devuelve.
2. Quién decide **`done`** — el LLM o Python (`calcular_done`).
3. Por qué hace falta **`max_turns`** además de `done`.
4. Qué vive en **`messages`** vs **`agent_state`** en Streamlit.
5. Por qué este agente **no** inventa mediciones.

---

## Experimentos opcionales (si sobra tiempo)

Si te sobra tiempo en la sesión (o quieres practicar en casa), prueba **1 o 2**. Anota en 2–3 líneas qué viste.

### Control y parada

- [ ] **`max_turns = 1`** — En CLI (`--max-turns 1`) o en el slider de Streamlit. ¿Qué queda en `plan` / `preferencias`? ¿Aparece el aviso de corte?
- [ ] **Sin confirmación** — Da zona + contaminante + tipo, pero **no** digas “sí / adelante”. ¿`done` sigue `false`? ¿El plan se queda vacío?
- [ ] **Preferencias a medias** — Solo zona, o solo contaminante. ¿El agente pregunta y no cierra?

### Estado y traza

- [ ] **Inspeccionar la traza** — Tras 3–4 turnos, mira `traza` en el JSON o en el expander: ¿cuántas entradas? ¿`status` ok/error?
- [ ] **Dos memorias** — En Streamlit, escribe 2 mensajes. Compara el historial del chat (`messages`) con el expander (`agent_state`: preferencias, plan, `done`).
- [ ] **Nueva conversación** — Cierra un plan (`done`) y pulsa «Nueva conversación». ¿Se resetean chat **y** estado?

### Robustez

- [ ] **Mensaje vacío** — En interactivo, Enter vacío (o el early-return). ¿Respuesta amigable **sin** nueva entrada en `traza`?
- [ ] **API key inválida** — Pon una clave mala en `.env`, reinicia y manda un mensaje. ¿`error` en estado + mensaje usable, sin tumbar CLI/Streamlit?

### Dominio (sin inventar datos)

- [ ] **Pedir un número concreto** — “¿Cuál es el valor de NO₂ ahora en Escuelas Aguirre?” ¿El agente se niega a inventar y ofrece plan de consulta?
- [ ] **Otro contaminante** — Repite la demo con PM10 o “magnitud 83”. ¿Se rellenan bien `preferencias`?

### Extra (si quieres practicar más)

- [ ] **Cambiar `DEMO_MENSAJES`** — En `config.py`, acorta o reordena el guion y ejecuta `python main.py`. ¿Sigue llegando a `done` con tu guion?
- [ ] **Temperatura** — Sube `TEMPERATURE` en `config.py` (p. ej. 0.7) y compara 2 demos: ¿más creativo o más inconsistente el JSON?
