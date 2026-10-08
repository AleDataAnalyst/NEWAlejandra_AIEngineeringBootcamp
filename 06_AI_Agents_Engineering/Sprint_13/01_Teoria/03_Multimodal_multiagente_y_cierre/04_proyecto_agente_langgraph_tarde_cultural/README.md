![Cabecera](../../../assets/cabecera_agentes.png)

# Proyecto: Agente multiagente LangGraph — tarde cultural

Demo de un **planificador cultural multiagente** con LangChain/LangGraph: un **supervisor** reparte el trabajo entre especialistas (`cultura`, `practico`, `sintetizar`), los especialistas pueden usar **tools**, y un humano **aprueba o rechaza** el plan antes de cerrar (`interrupt_before` + checkpointer).

```text
mensaje → procesar_turno(estado, mensaje, thread_id)
       → grafo multiagente (MemorySaver)
       → pausa antes de aplicar → humano aprueba / rechaza
CLI / Streamlit = clientes (mismo thread_id)
```

| Tool | Rol |
|------|-----|
| `hora_actual` | Fecha/hora local |
| `RAG_buscar_en_guia` | Retrieval léxico sobre `data/guia_cultural.txt` |
| `API_consultar_eventos_madrid` | Open data Madrid + fallback JSON |
| `describir_cartel` | Multimodal: lee `assets/cartel_demo.jpg` (Rolling Stones · Vicente Calderón, Madrid) → texto |

**Requisitos:** Python 3.10+ y `GEMINI_API_KEY` en `.env`.

---

## Estructura

```text
.
├── main.py                # CLI (cliente)
├── app.py                 # Streamlit (cliente)
├── config.py              # paths, modelo, defaults, DEMO_MENSAJES
├── gemini_auth.py         # carga GEMINI_API_KEY
├── src/
│   ├── __init__.py
│   ├── agent.py           # procesar_turno, aprobar_plan, run_demo
│   ├── graph.py           # StateGraph multiagente + MemorySaver + HITL
│   ├── llm.py             # ChatGoogleGenerativeAI
│   ├── state.py           # estado de producto (UI / resumen)
│   └── tools/
│       ├── __init__.py    # allowlist (@tool) + ejecutar_tool
│       ├── hora_actual.py
│       ├── rag_guia.py
│       ├── api_eventos.py
│       └── describir_cartel.py
├── data/
│   ├── guia_cultural.txt
│   └── eventos_fallback.json
├── assets/
│   └── cartel_demo.jpg    # Rolling Stones · Vicente Calderón (describir_cartel)
├── requirements.txt
├── .env.example
└── .streamlit/config.toml
```

En la raíz: clientes y configuración. En `src/`: lógica del agente. Ejecuta siempre **desde la raíz del proyecto**.

---

## Instalación

```bash
python -m venv .venv
source .venv/bin/activate          # Git Bash / macOS / Linux
# .venv\Scripts\Activate.ps1       # Windows PowerShell

pip install -r requirements.txt
cp .env.example .env               # define GEMINI_API_KEY
```

La imagen de demo multimodal ya está en `assets/cartel_demo.jpg` (cartel Rolling Stones en el Vicente Calderón, Madrid).

---

## Ejecución (CLI)

```bash
# Demo (mensaje(s) de config.DEMO_MENSAJES; HITL auto-aprobado)
python main.py

# Sin auto-aprobar: la demo queda en pausa HITL (útil para inspeccionar el plan)
python main.py --sin-auto-aprobar

# Límites
python main.py --max-turns 1 --max-steps 4

# Chat en terminal (tú escribes; si hay plan pendiente: aprobar / rechazar)
python main.py --interactivo
```

Al terminar, la CLI imprime un **resumen** (`done`, HITL, `thread_id`, log) y el JSON del estado.

Si la CLI falla (API key, red, deps), la UI también fallará: arregla el backend primero.

---

## Mensajes de prueba (copiar / pegar)

Sirven igual en **`python main.py --interactivo`** (tras `Tú:`) y en el **chat de Streamlit**.

### Pedido completo (guía + eventos)

```text
Quiero una tarde cultural barata en el centro de Madrid: museo o exposición y algo de música si encaja. Consulta la guía y el catálogo de eventos.
```

Qué mirar: log con `supervisor` → `cultura` / `practico` → `sintetizar`; tools `RAG_buscar_en_guia` y/o `API_consultar_eventos_madrid`; plan pendiente HITL.

### Solo guía

```text
¿Qué museos gratuitos o baratos recomienda la guía en el centro?
```

### Solo eventos / API

```text
Busca eventos culturales en Madrid para esta tarde o esta semana.
```

### Cartel multimodal (Rolling Stones)

```text
Mira el cartel de demo y úsalo si encaja con una tarde cultural en Madrid.
```

Qué mirar: en la traza debe salir `describir_cartel` leyendo `assets/cartel_demo.jpg` (Rolling Stones · Vicente Calderón).

### Tras el plan (HITL)

| Dónde | Qué escribir / pulsar |
|-------|------------------------|
| CLI `--interactivo` | `aprobar` o `rechazar` |
| Streamlit | Sidebar → **Aprobar** / **Rechazar** |

En CLI, `salir` (o Enter vacío) termina la sesión.

**Evitar:** monólogos enormes o pedir cosas fuera de Madrid/guía.

---

## Web App Streamlit

```bash
streamlit run app.py
```

Se abre el navegador en `http://localhost:8501` (o la URL que imprima la terminal).

### Qué verás

1. **Chat** — pega uno de los mensajes de la sección anterior; suele lanzar el grafo hasta el plan.
2. **HITL** — si hay plan pendiente, el input se bloquea y en la **sidebar** aparecen **Aprobar** / **Rechazar**.
3. **Sidebar** — `max_turns`, `max_steps` (tools por especialista), `thread_id`, «Nueva conversación».
4. **Expander debug** — plan, log del supervisor, traza, `done`, errores.

### Dos memorias (+ hilo del grafo)

| Clave | Qué guarda |
|-------|------------|
| `st.session_state.messages` | Burbujas del chat (UI) |
| `st.session_state.agent_state` | Plan, log, traza, flags HITL/`done` |
| `st.session_state.thread_id` | Hilo del checkpointer (`MemorySaver`) |

«Nueva conversación» reinicia chat, estado y **nuevo** `thread_id`.

### Guión rápido en Streamlit

| # | Qué hacer | Qué observar |
|---|-----------|--------------|
| 1 | Pegar el **pedido completo** | Log multiagente; plan pendiente |
| 2 | Sidebar → **Aprobar** | `done=true`; mensaje de cierre |
| 3 | «Nueva conversación» → otro pedido → **Rechazar** | Plan limpio; puedes mandar otro mensaje |
| 4 | Pegar el mensaje del **cartel** | Traza con `describir_cartel` |

---

## Cómo leer el código

Orden sugerido:

1. **`config.py`** — modelo, `MAX_ITER`, `max_steps` / `max_turns`, demo.
2. **`src/tools/__init__.py`** — allowlist de `@tool` y `ejecutar_tool`.
3. **`src/graph.py`** — nodos supervisor / especialistas / `aplicar`; `MemorySaver`; `interrupt_before`.
4. **`src/agent.py`** — `procesar_turno`, `aprobar_plan`, `run_demo`.
5. **`src/state.py`** — forma del estado que ven CLI / Streamlit.
6. **`main.py` / `app.py`** — clientes.

Idea clave: **el supervisor orquesta; los especialistas trabajan (con tools); Python + HITL controlan el cierre**.

---

## Flujo de un pedido

```text
Usuario escribe un mensaje (+ thread_id)
        │
        ▼
procesar_turno → app.invoke(...)     ← src/agent.py / graph.py
        │
        ├─ supervisor  → elige cultura | practico | sintetizar | FINISH
        ├─ cultura / practico  → mini-bucle con @tool (max_steps)
        ├─ sintetizar  → plan en texto + lista `plan`
        └─ (antes de aplicar) interrupt  → pendiente HITL

Humano aprueba / rechaza
        │
        ▼
aprobar_plan → update_state + invoke(None) → nodo aplicar → done o reset
```

Parada cuando: plan aprobado (`done=True`), hay `error`, o se alcanza `max_turns` / `MAX_ITER` en el supervisor.

---

## HITL (human-in-the-loop)

1. Tras sintetizar un plan, el grafo se **pausa** antes del nodo `aplicar` (`interrupt_before`).
2. El checkpointer (`MemorySaver`) guarda el hilo (`thread_id`).
3. CLI o Streamlit llaman a `aprobar_plan(thread_id, True/False, estado)`.
4. Eso hace `update_state` + `invoke(None)` y ejecuta `aplicar`.

Sin checkpointer no habría dónde “recordar” la pausa.

---

## Control útil

| Concepto | Qué limita |
|----------|------------|
| `max_steps` | Vueltas modelo↔tools **dentro de un especialista** |
| `max_turns` | Mensajes de usuario en la conversación (clientes) |
| `MAX_ITER` | Vueltas del **supervisor** (evita bucles infinitos) |
| Allowlist | Solo tools de `src/tools/__init__.py` |

---

## Rol de ficheros

| Fichero | Responsabilidad |
|---------|-----------------|
| `config.py` | Modelo, paths, límites, `DEMO_MENSAJES` |
| `gemini_auth.py` | Carga de `GEMINI_API_KEY` |
| `src/graph.py` | Grafo multiagente + memoria + interrupt |
| `src/agent.py` | Orquestación de turno y HITL |
| `src/llm.py` | Factory del chat model LangChain |
| `src/state.py` | Estado visible en UI / JSON final |
| `src/tools/*` | Tools `@tool` (RAG, API, hora, cartel) |
| `main.py` / `app.py` | Clientes CLI y Streamlit |
| `data/guia_cultural.txt` | Corpus del mini-RAG |
| `data/eventos_fallback.json` | Fallback si falla la API |
| `assets/cartel_demo.jpg` | Cartel Rolling Stones (Vicente Calderón) para `describir_cartel` |

---

## Qué NO hace

- No es un multiagente de producción (colas, muchos equipos, A2A…).
- No usa embeddings ni base vectorial (el RAG es léxico a propósito).

---

## Mini glosario

| Término | Qué significa aquí |
|---------|-------------------|
| **Supervisor** | Nodo que elige el siguiente rol; no escribe el plan al usuario. |
| **Especialista** | Nodo con prompt propio; puede llamar tools. |
| **Allowlist** | Lista blanca de tools ejecutables. |
| **MemorySaver** | Checkpoints en RAM por `thread_id`. |
| **interrupt_before** | Pausa el grafo antes de un nodo sensible (`aplicar`). |
| **HITL** | Una persona aprueba o rechaza antes de cerrar. |

---

## Experimentos

1. **Demo completa** — `python main.py`. Mira `log` (supervisor → especialistas) y `done` tras auto-aprobar.
2. **HITL manual** — `python main.py --sin-auto-aprobar` o Streamlit: inspecciona el plan y pulsa Aprobar/Rechazar.
3. **Modo interactivo** — `python main.py --interactivo` con `aprobar` / `rechazar`.
4. **Tools en traza** — Un pedido que pida guía + eventos; en el JSON/`traza` deberían salir `RAG_buscar_en_guia` y/o `API_consultar_eventos_madrid`.
5. **Fallback API** — Sin red (o bloqueando la URL): la tool debe indicar `Fuente: fallback`.
6. **`max_steps` bajo** — `--max-steps 1` (o slider en Streamlit) y un pedido que fuerce tools.
7. **Nueva conversación** — En Streamlit, tras `done`, «Nueva conversación» debe cambiar `thread_id` y limpiar chat/estado.
8. **Cartel multimodal** — Pide mirar el cartel de demo; en la traza debe salir `describir_cartel` leyendo `assets/cartel_demo.jpg`.
9. **Error controlado** — API key inválida: mensaje amigable y `error` en el estado (sin tumbar Streamlit).
