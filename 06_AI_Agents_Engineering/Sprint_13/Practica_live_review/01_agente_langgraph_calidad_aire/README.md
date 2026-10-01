![Cabecera](../../../Sprint_11/assets/cabecera_thebridge.png)

# Práctica Sprint 13 — Agente LangGraph · calidad del aire

**Live Review** del Sprint 13: orquestar el ciclo tools con **LangGraph** + HITL ligero.

Dominio: **calidad del aire** (mismo que S12 LR). Lo nuevo: el `while`/`run_tool_loop` pasa a un **StateGraph** (`agent` ↔ `tools`).

```text
mensaje → procesar_turno(estado, mensaje, max_steps)
       → invoke_tools_loop (grafo LangGraph)
       → sintetizar_estado → calcular_done / HITL → traza
CLI / Streamlit = clientes
```

> Tools + allowlist vienen **dadas** (ya las practicasteis en S12). Aquí el foco es el **grafo** y cablear `procesar_turno`.

---

## Empieza aquí

### Fase 0 — Entorno

- [ ] **1.** venv + `pip install -r requirements.txt` + `.env` con `GEMINI_API_KEY`
- [ ] **2.** `python main.py --check` → varios `[FAIL]` (TODOs)

### Fase 1 — Grafo ReAct (`src/graph.py`)

- [ ] **3.** Completa `_router` y `_router_tras_tools`
- [ ] **4.** Completa `build_graph` (nodos + edges)
- [ ] **5.** Completa `invoke_tools_loop` (`app.invoke`)

### Fase 2 — Orquestación (`src/agent.py`)

- [ ] **6.** Completa `procesar_turno` (usa `invoke_tools_loop` + `_aplicar_hitl`)
- [ ] **7.** Completa `run_demo` (con `auto_aprobar` HITL)
- [ ] **8.** `python main.py --check` → todo `[OK]`

### Fase 3 — Demostrar

- [ ] **9.** `python main.py` → tools en traza; plan; HITL auto-aprobado en demo
- [ ] **10.** `python main.py --max-turns 1 --max-steps 1`
- [ ] **11.** `streamlit run app.py` + botones Aprobar/Rechazar

### Archivos que **no** debes modificar

`state.py`, `llm.py`, `tools/*`, `main.py`, `app.py`, `verificar.py`, `config.py` (salvo defaults), `gemini_auth.py`, `data/*`.

**Sí implementas:** `src/graph.py` (TODOs), `src/agent.py` (`procesar_turno`, `run_demo`).

---

## Requisitos

```bash
cd Practica_live_review/01_agente_langgraph_calidad_aire
python -m venv .venv
# activar venv
pip install -r requirements.txt
cp .env.example .env
python main.py --check
```

---

## Estructura

```text
src/
  graph.py     ← TU IMPLEMENTACIÓN (routers + edges + invoke)
  agent.py     ← TU IMPLEMENTACIÓN (procesar_turno + run_demo)
  llm.py       ← dado
  state.py     ← dado (+ HITL fields)
  tools/       ← dado (allowlist completa)
app.py         ← dado (cliente + botones HITL)
main.py / verificar.py ← dados
```

---

## Preferencias y done

| Preferencia | Ejemplo |
|-------------|---------|
| `zona` | centro, Escuelas Aguirre |
| `contaminante` | NO2, PM10 |
| `tipo_consulta` | `que_mide` / `interpretar` / `comparar` / `general` |

`done=true` cuando hay las tres prefs, `plan` ≥2 **y** `plan_aprobado` (HITL).

### Guion demo (`DEMO_MENSAJES`)

```text
1. Quiero info de calidad del aire.
2. Quiero que te centres en la hora actual para contextualizar.
3. Zona centro, contaminante NO2. Consulta la guía y datos de la API de Madrid. El tipo de consulta es interpretar un valor alto.
4. Añade otro paso al plan si falta.
5. Perfecto, adelante con ese plan.
```

En CLI demo, `auto_aprobar=True` aprueba el plan solo. En Streamlit usas los botones.

---

## FASE 1 — Grafo

### Objetivo

```text
START → agent ──tool_calls?──► tools ──pasos < max?──► agent → …
                    └── no / max_steps ──► END
```

### Criterios

- [ ] `--check` marca `[OK]` en routers, `build_graph`, `invoke_tools_loop`
- [ ] `invoke_tools_loop` usa `.invoke(`

---

## FASE 2 — `procesar_turno` / `run_demo`

### Criterios

- [ ] Llama a `invoke_tools_loop` (no un `while` manual)
- [ ] Tras JSON: `_aplicar_hitl`
- [ ] Traza con `tools`
- [ ] Mensaje vacío → sin traza nueva
- [ ] `run_demo` auto-aprueba si `pendiente_hitl` y `auto_aprobar`

---

## Pistas (spoilers)

<details>
<summary>Router tras agent</summary>

```python
if int(estado.get("pasos") or 0) >= int(estado.get("max_steps") or 1):
    return "__end__"
if estado.get("pending_calls"):
    return "tools"
return "__end__"
```

</details>

<details>
<summary>build_graph (esqueleto)</summary>

```python
grafo = StateGraph(LoopState)
grafo.add_node("agent", _nodo_agent)
grafo.add_node("tools", _nodo_tools)
grafo.add_edge(START, "agent")
grafo.add_conditional_edges("agent", _router, {"tools": "tools", "__end__": END})
grafo.add_conditional_edges(
    "tools", _router_tras_tools, {"agent": "agent", "__end__": END}
)
return grafo.compile()
```

</details>

<details>
<summary>procesar_turno (núcleo)</summary>

```python
texto_tools, traza_tools = invoke_tools_loop(mensaje, max_steps=max_steps)
cambios = sintetizar_estado(estado, mensaje, texto_tools)
estado = actualizar_estado(estado, cambios)
...
estado = calcular_done(estado)
estado = _aplicar_hitl(estado)
```

</details>

---

## Criterio de cierre

Explica en voz alta:

1. Qué sustituye el grafo respecto a `run_tool_loop` de S12.
2. Qué decide el router tras `agent` y tras `tools`.
3. Diferencia `max_steps` vs `max_turns`.
4. Por qué `done` exige `plan_aprobado` (HITL).
5. Qué miras en `traza[].tools`.
6. `messages` vs `agent_state` en Streamlit.
