![Cabecera](../../../assets/cabecera_agentes.png)

# Proyecto: Agente con tools — tarde cultural

> **Esto no es la Live Review.** Es el proyecto de referencia del bloque (dominio **tarde cultural**).  
> La Live Review del Sprint 12 está en [`Practica_live_review/`](../../../Practica_live_review/) (calidad del aire: mismas mecánicas, otras tools / prefs).

Agente que usa **function calling** con tres tools. El propio agente (el código en este proyecto) valida, ejecuta y limita (`max_steps`, allowlist, traza) para que el LLM no pueda ejecutar tools no permitidas. El LLM decide *qué* tool pedir; el agente decide lo que se debe ejecutar.

| Tool | Rol |
|------|-----|
| `hora_actual` | Fecha/hora local |
| `RAG_buscar_en_guia` | Retrieval léxico sobre `data/guia_cultural.txt` |
| `API_consultar_eventos_madrid` | Open data Madrid + fallback JSON |

Tras el loop de tools, una segunda llamada **sin tools** sintetiza `preferencias` / `plan` / `respuesta` (JSON). El agente calcula `done` True/False para decidir si el plan está listo o debe seguir pidiendo más información. El LLM no tiene una tool para marcarlo por si sólo.

**Requisitos:** Python 3.10+ y `GEMINI_API_KEY` en `.env`.

> **Aviso — warning de AFC al ejecutar**  
> Es posible que veáis un mensaje del SDK tipo *“Direct use of automatic function calling (AFC) in Models.generate_content is not recommended…”*.  
> **No es un error de vuestro código.** Este proyecto hace el loop de tools **a mano**  para que veamos cómo funciona por dentro (`run_tool_loop`) y desactiva el AFC del SDK con `disable=True` en `src/llm.py`. Podéis ignorar ese aviso; el agente sigue funcionando.

---

## Estructura

```text
.
├── main.py                # CLI (cliente)
├── app.py                 # Streamlit (cliente)
├── config.py              # paths, modelo, defaults
├── gemini_auth.py         # carga GEMINI_API_KEY
├── src/                   # backend del agente (paquete Python)
│   ├── __init__.py
│   ├── agent.py           # procesar_turno + run_demo
│   ├── llm.py             # loop Function Calling + síntesis JSON
│   ├── state.py           # AgentState + calcular_done
│   └── tools/
│       ├── __init__.py    # registro / allowlist / validar_args
│       ├── hora_actual.py
│       ├── rag_guia.py
│       └── api_eventos.py
├── data/
│   ├── guia_cultural.txt
│   └── eventos_fallback.json
├── requirements.txt
├── .env.example
└── .streamlit/config.toml
```

En la raíz: clientes, configuración y datos (`.env`, `data/`). En `src/`: lógica del agente. Ejecuta siempre **desde la raíz del proyecto**.

---

## Instalación

```bash
python -m venv .venv
source .venv/bin/activate          # Git Bash / macOS / Linux
# .venv\Scripts\Activate.ps1       # Windows PowerShell

pip install -r requirements.txt
cp .env.example .env               # define GEMINI_API_KEY
```

---

## Ejecución (CLI)

```bash
# Demo completa (usa los 5 mensajes de config.DEMO_MENSAJES, defaults de config)
python main.py

# Ejecución normal con flags explícitos (2 turnos, steps holgados)
python main.py --max-turns 2 --max-steps 6

# Corte por max_turns: solo 2 de 5 mensajes → se ve el aviso de corte
python main.py --max-turns 2

# Corte por max_steps: 1 mensaje que fuerza tools + cupo 1 vuelta
# → en respuesta / resumen: "He parado por max_steps=1"
python main.py --max-turns 1 --max-steps 1

# Chat en terminal
python main.py --interactivo
```

Al terminar, la CLI imprime un **resumen** (turnos, tools del último turno, tipo de corte) y después el JSON completo (incluye `traza`).

`DEMO_MENSAJES` tiene 5 turnos. El **primero** ya pide guía + eventos (así `--max-steps 1` puede cortar tras tools). Los siguientes afinan el plan. Con `--max-turns 2` solo corren 2 de 5 y se nota el corte.

## Ejecución app web con Streamlit

```bash
streamlit run app.py
```

En el sidebar puedes ajustar `max_turns` y `max_steps`. El expander **Estado / traza de tools** muestra el dict interno del agente.

Para ver bien el corte por **max_steps** en Streamlit: pon el slider a `1` y escribe un mensaje que force tools, p. ej. *“Consulta la guía y los eventos de Madrid y propon un plan”*.

### Guión de chat (Streamlit o `python main.py --interactivo`)

Usa frases **cortas y acotadas**. Así se ve bien preferencias → tools → plan → `done`.

| # | Escribe tú | Qué mirar |
|---|------------|-----------|
| 1 | `Quiero una tarde cultural barata en el centro de Madrid.` | Pregunta o empieza a rellenar prefs; `done=false` |
| 2 | `Consulta la guía y algún evento del catálogo.` | En traza: `RAG_buscar_en_guia` y/o `API_consultar_eventos_madrid` |
| 3 | `Propón un plan concreto con 2 o 3 actividades.` | Aparece plan (borrador o final) |
| 4 | `Perfecto, adelante.` | Si hay prefs + plan ≥2 → `done=true` y el chat se cierra (Streamlit) |

**Solo prefs (sin forzar tools aún):**

1. `Quiero algo cultural en Madrid.`
2. `Presupuesto barato.`
3. `Zona centro.`

**Forzar tools en un solo mensaje** (útil con `max_steps=1` para ver el corte):

`Tarde cultural barata en centro. Usa la guía RAG y la API de eventos y propon un plan.`

**Evitar** (poco acotado): monólogos largos, pedir cosas fuera de Madrid/guía, o “haz lo que quieras”.

---

## Cómo leer el código

Orden sugerido:

1. **`config.py`** — paths, modelo, límites por defecto.
2. **`src/tools/__init__.py`** — allowlist (`TOOL_REGISTRY`), `validar_args`, `ejecutar_tool`.
3. **`src/llm.py`** — declaraciones Gemini, `run_tool_loop` (FC manual, AFC off), `sintetizar_estado` (JSON sin tools).
4. **`src/agent.py`** — `procesar_turno`: une loop + síntesis + `calcular_done` + traza por turno.
5. **`src/state.py`** — contrato de estado y reglas de `done`.
6. **`main.py` / `app.py`** — clientes (CLI y chat).

Es importante entender que: **decisión (LLM) ≠ ejecución (Agente)**.

---

## Flujo de un turno

```text
mensaje usuario
  → run_tool_loop (Gemini FC, max_steps, allowlist)
  → sintetizar_estado (JSON sin tools)
  → actualizar_estado + calcular_done
  → append en traza (tools de este turno)
```

### Historial dentro de `run_tool_loop` (roles)

El loop no es un chat libre: es una lista `historial` de mensajes con **rol**.
Cada elemento es un `types.Content` con `parts` (texto, petición de tool o resultado).

El **rol** significa el tipo de mensaje que es: user, model, tool.

```text
historial
  │
  ├─ [user]   instrucciones + mensaje del usuario
  │              ↓
  ├─ [model]  pide tool(s)          ← response.function_calls
  │              ↓
  ├─ [tool]   resultados            ← Part.from_function_response
  │              ↓
  ├─ [model]  más tools…  o  texto final
  │              ↓
  └─ (se repite hasta texto final o max_steps)
```

Pasos en código (`src/llm.py`):

1. **Pedir** al modelo con el `historial`.
2. Si hay `llamadas` → **ejecutar** tools (allowlist) y guardar en `traza`.
3. **Añadir** al historial la petición del modelo y los resultados (`role="tool"`).
4. Si no hay llamadas → devolver el texto; eso cierra la Fase 1.

`types.Content` = un turno del historial (`role` + `parts`).  
`types.Part` = un trozo de ese turno (texto, function call o function response).

En Streamlit hay **dos memorias**:

| Memoria | Dónde | Para qué |
|---------|-------|----------|
| `st.session_state.messages` | Chat | Lo que ve el usuario |
| `st.session_state.agent_state` | Dict interno | preferencias, plan, done, traza |

No confundas el historial del chat con la traza de tools.

---

## Control y seguridad

### Allowlist

Solo se ejecutan tools registradas en `TOOL_REGISTRY`. Si el modelo pide otra, no se ejecutará la función: se devuelve error al modelo y en la traza verás `status: "blocked"`.

Hay dos capas: comprobación en `llm.run_tool_loop` (para marcar `blocked`) y en `ejecutar_tool` (última barrera).

### Validación de args (`validar_args`)

Antes de `fn(**args)`:

- `hora_actual` → ignora args extra.
- `RAG_buscar_en_guia` → `consulta` como string; vacía → error.
- `API_consultar_eventos_madrid` → `limite` entero entre 1 y 10.

### Status en la traza para cada tool

| status | Significado |
|--------|-------------|
| `ok` | Tool permitida y respuesta sin prefijo `Error` |
| `error` | Tool permitida pero falló (excepción o mensaje de error) |
| `blocked` | Nombre fuera del registro |

### Límites: `max_steps` vs `max_turns`

| Concepto | Cuenta | Dónde |
|----------|--------|-------|
| `max_steps` | Vueltas modelo ↔ tools **dentro de un mensaje** | `llm.run_tool_loop`, flags CLI, slider Streamlit |
| `max_turns` | Mensajes de **usuario** en la conversación | `run_demo`, modo interactivo, slider Streamlit |

Sin `max_steps`, un bucle de tools puede quemar cuota del LLM.

### `done`

El agente lo calcula en `state.calcular_done` cuando hay datos mínimos (intereses, presupuesto, zona) y un plan con al menos 2 actividades. No existe tool `marcar_done`.

---

## Traza de cada turno

Cada **turno** (mensaje de usuario) añade una entrada en `estado["traza"]`. Dentro, `tools` lista cada **step** del loop FC:

```json
{
  "turno": 1,
  "mensaje": "Quiero una tarde cultural en Madrid…",
  "status": "ok",
  "done": false,
  "tools": [
    {
      "step": 1,
      "tool": "RAG_buscar_en_guia",
      "args": {"consulta": "museos gratis centro"},
      "status": "ok",
      "preview": "Según la guía, el primer domingo…"
    },
    {
      "step": 1,
      "tool": "hora_actual",
      "args": {},
      "status": "ok",
      "preview": "2026-08-19T18:30:00"
    }
  ]
}
```

Varias tools en el mismo `step` es normal (el modelo las pide en paralelo). `preview` es un recorte del resultado. No se manda la traza entera al LLM en cada prompt para no quemar cuota porque es muy largo y puede ser innecesario.

### Ejemplo de cómo se ve la traza

1. El usuario mandó el mensaje del `turno` 1.
2. En el **step 1** el modelo pidió dos tools a la vez: `RAG_buscar_en_guia` (con una consulta) y `hora_actual`.
3. El agente las ejecutó (`status: ok`) y guardó un `preview` del resultado.
4. Después (no se ve en este JSON) el modelo recibió esos resultados, escribió un texto, y la **Fase 2** (`sintetizar_estado`) rellenó preferencias / plan / respuesta.
5. `done: false` aquí significa: aún faltan datos o el plan no cumple las reglas de `calcular_done` — el chat puede seguir.

---

## Rol de ficheros

| Fichero | Responsabilidad |
|---------|-----------------|
| `config.py` | Modelo, paths a `data/`, defaults |
| `gemini_auth.py` | Carga de `GEMINI_API_KEY` |
| `src/tools/*` | Implementación pura (sin Gemini) |
| `src/tools/__init__.py` | Allowlist + validación + punto único de ejecución |
| `src/llm.py` | Protocolo Function Calling + prompt JSON |
| `src/agent.py` | Orquestación / errores por turno |
| `src/state.py` | Contrato de estado + `calcular_done` |
| `main.py` / `app.py` | Clientes |
| `data/guia_cultural.txt` | Corpus de `RAG_buscar_en_guia` |
| `data/eventos_fallback.json` | Fallback si falla la API de Madrid |

URL de la API en `config.MADRID_EVENTOS_URL`.

---

## Mini glosario

| Término | Qué significa aquí |
|---------|-------------------|
| **Function calling** | El modelo no ejecuta código: *pide* una tool (nombre + args). Vuestro código decide si la corre. |
| **Allowlist** | Lista blanca (`TOOL_REGISTRY`): solo esas tools se pueden ejecutar. |
| **Traza** | Registro de lo que pasó (por turno y por step de tools) para depurar y enseñar el flujo. |
| **max_steps** vs **max_turns** | `max_steps` = vueltas modelo↔tools *dentro de un mensaje*. `max_turns` = mensajes de usuario en la conversación. |
| **done** | Flag del agente: “ya hay plan usable”. Lo calcula el código (`calcular_done`), no el LLM. |


---

## Experimentos

1. **Multi-tool** — Pide una tarde con guía + eventos; comprueba ≥2 entradas en `tools`.
2. **`max_steps` bajo** — `python main.py --max-turns 1 --max-steps 1` (o Streamlit con slider `1` + prompt que pida guía y eventos). Mira el **resumen** (`corte: max_steps`) y la frase en `respuesta`.
3. **Fallback API** — Desconecta la red o bloquea la URL; en la respuesta de la tool debe aparecer `Fuente: fallback` (lee `data/eventos_fallback.json`).
4. **Plan intermedio** — En Streamlit, si hay ítems en `plan` pero `done=false`, verás **Plan (borrador):** en el chat.
5. **`done` incompleto** — Di solo “quiero algo cultural” (sin presupuesto ni zona). El agente debe preguntar; `done` sigue `false`.
6. **`done` completo** — Da intereses + presupuesto + zona y deja que use tools. Con plan ≥2 actividades, `done` pasa a `true` y el chat se cierra (Streamlit).
7. **`max_turns` bajo** — `python main.py --max-turns 2` (hay 5 msgs en la demo → solo corre 2). Resumen: `corte: max_turns`. En Streamlit: slider `max_turns=1` y un mensaje.
8. **Allowlist** — Quita temporalmente una tool de `TOOL_REGISTRY` en `src/tools/__init__.py`, reinicia y fuerza al modelo a pedirla: en la traza debe salir `status: "blocked"` (luego restaura el registro).
9. **RAG vacío** — Pregunta algo que no esté en `data/guia_cultural.txt` (p. ej. “ópera en Marte”). La tool debe decir que no encontró nada; el modelo no debería inventar el corpus.
10. **Editar la guía** — Añade una sección `##` falsa en `guia_cultural.txt`, pregunta por ella y verifica que sale en el `preview` de la traza.
11. **Modo interactivo** — `python main.py --interactivo`: varios mensajes seguidos y mira cómo crece `traza` turno a turno en el JSON final.
12. **Nueva conversación** — En Streamlit, cierra un plan (`done`) y pulsa «Nueva conversación»: chat y `agent_state` deben resetearse.
