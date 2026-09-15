![Cabecera](../../../assets/cabecera_thebridge.png)

# Proyecto ejemplo: Agente tarde cultural

Agente conversacional con `AgentState`: el LLM propone JSON, Python actualiza el estado y decide `done`. El mismo backend sirve para **CLI** y **Streamlit**.

**Requisitos:** Python 3.10+ y `GEMINI_API_KEY` en `.env`.

Dominio de la demo: planificar una tarde cultural con un agente conversacional.

> **Aviso — warning de AFC al ejecutar**  
> Es posible que veáis un mensaje del SDK tipo *“Direct use of automatic function calling (AFC) in Models.generate_content is not recommended…”*.  
> **No es un error de vuestro código.** Este proyecto **no usa tools** ni function calling; es un aviso del SDK de Gemini al llamar a `generate_content`. Podéis ignorarlo; el agente sigue funcionando.

---

## Estructura

En la raíz: clientes y configuración. En `src/`: lógica del agente. Ejecuta siempre **desde la raíz del proyecto**.

```text
.
├── main.py                # CLI (cliente)
├── app.py                 # Streamlit (cliente)
├── config.py              # modelo, max_turns, guion demo
├── gemini_auth.py         # carga GEMINI_API_KEY
├── src/                   # backend del agente (módulo Python)
│   ├── __init__.py
│   ├── agent.py           # procesar_turno + run_demo
│   ├── llm.py             # Prompt + llamada a Gemini → JSON
│   └── state.py           # AgentState: crear / actualizar / calcular_done
├── requirements.txt
├── .env.example
└── .streamlit/config.toml
```

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
# Demo completa (5 mensajes de config.DEMO_MENSAJES)
python main.py

# Corte por max_turns: solo 2 de 5 mensajes → se ve el aviso de corte
python main.py --max-turns 2

# Chat por terminal (tú escribes cada mensaje)
python main.py --interactivo
```

Al terminar, la CLI imprime un **resumen** (turnos, `done`, tipo de corte) y después el JSON completo (incluye `traza`).

`DEMO_MENSAJES` tiene 5 turnos. Con `--max-turns 2` solo corren 2 de 5 y se nota el corte.

Si la CLI falla (API key, JSON, red), la UI también fallará: arregla el backend primero.

---

## Web App Streamlit (chatbot conversacional)

### Arranque

Desde la carpeta del proyecto (con el `.venv` activo):

```bash
streamlit run app.py
```

Se abre el navegador en `http://localhost:8501` (si no, usa la URL que imprime la terminal). Deja la terminal abierta mientras usas la app.

### Qué verás en pantalla

1. **Chat** — escribe en el campo inferior (`chat_input`) y pulsa Enter.
2. **Respuesta** — el agente pregunta o cierra con un plan (2–4 ítems). Si hay plan parcial, verás **Plan (borrador):**; si `done=true`, **Plan:**.
3. **Estado / traza (debug)** — expander: preferencias, plan, `done`, `error`, turnos.
4. **Sidebar**
   - **max_turns** — tope de mensajes de usuario → LLM.
   - **Nueva conversación** — reinicia chat + `AgentState`.

### Pruebas sugeridas

| Prueba | Ejemplo | Qué observar |
|--------|---------|--------------|
| Pedido vago | `Quiero una tarde cultural.` | Pregunta; `plan` vacío; `done=false` |
| Preferencias | `Cine o música, barato.` | Se rellenan intereses / presupuesto |
| Zona | `Zona centro.` | Ya hay datos mínimos; aún puede pedir confirmación |
| Cierre | `Sí, adelante, unas 3 horas.` | `plan` con ≥2 ítems; `done=true` |
| Tope | Baja `max_turns` a 2 y conversa | Aviso / bloqueo al alcanzar el límite |
| Error | API key inválida en `.env` | `error` en estado + mensaje amigable |

### Dos memorias (importante)

Streamlit guarda datos entre reruns en `st.session_state`. En esta app hay **dos** claves distintas:

| Clave | Dónde vive | Qué guarda | Para qué sirve |
|-------|------------|------------|----------------|
| `st.session_state.messages` | Frontend (UI) | Lista de burbujas `{role, content}` | Pintar el chat |
| `st.session_state.agent_state` | Backend (tarea) | Preferencias, plan, `done`, `error`, `traza` | Que el agente “recuerde” la tarea |

- **`messages`** = historial de conversación visible.
- **`agent_state`** = `AgentState` del agente. Es lo que entra al prompt en cada turno y lo que actualiza `procesar_turno`.

«Nueva conversación» reinicia **las dos**. El expander de debug muestra el `agent_state`, no el hilo del chat.

### Notas

- Cada mensaje llama a **`procesar_turno(estado, mensaje)`** una vez (un turno = una llamada al LLM).
- Tema visual: `.streamlit/config.toml`.
- Para parar la app: `Ctrl+C` en la terminal.

### Si algo no carga

| Síntoma | Qué hacer |
|---------|-----------|
| Error de API key | Revisa `.env` → `GEMINI_API_KEY` |
| JSON inválido | Mira `traza` / `error` en el expander |
| Puerto ocupado | Streamlit ofrecerá otro (p. ej. 8502) o cierra la instancia anterior |

---

## Cómo leer el código

Orden sugerido:

1. **`config.py`** — modelo, `MAX_TURNS_DEFAULT`, mensajes de la demo.
2. **`src/state.py`** — forma del estado, `actualizar_estado`, `calcular_done` (Python decide `done`).
3. **`src/llm.py`** — prompt + Gemini → JSON de preferencias/plan/respuesta (sin `done`).
4. **`src/agent.py`** — `procesar_turno`: une LLM + estado + traza; `run_demo` con `max_turns`.
5. **`main.py` / `app.py`** — clientes (CLI y chat). Misma función `procesar_turno`.

Mensaje clave: **el LLM propone datos; Python decide `done` y los límites**.

---

## Flujo completo

```text
Usuario escribe un mensaje
        │
        ▼
procesar_turno(estado, mensaje)     ← src/agent.py
        │
        ├─► preguntar_al_modelo()   ← src/llm.py   (Gemini → JSON sin "done")
        ├─► actualizar_estado()     ← src/state.py (preferencias, plan, respuesta)
        ├─► calcular_done()         ← src/state.py (Python decide done)
        └─► traza.append(...)       (ok | error)

Clientes:
  main.py  → run_demo() o --interactivo
  app.py   → chat; guarda agent_state en st.session_state
```

Parada cuando: `done=True`, hay `error`, o se alcanza `max_turns`.

---

## Rol de ficheros

| Fichero | Responsabilidad |
|---------|-----------------|
| `config.py` | Modelo, `max_turns`, guion `DEMO_MENSAJES` |
| `gemini_auth.py` | Carga de `GEMINI_API_KEY` (`.env` o prompt) |
| `src/__init__.py` | Marca `src/` como módulo (`from src.agent import …`) |
| `src/state.py` | Contrato de estado + `calcular_done` |
| `src/llm.py` | Prompt + llamada a Gemini → JSON (sin `done`) |
| `src/agent.py` | Orquestación / errores por turno (`procesar_turno`) |
| `main.py` | Cliente CLI (demo, `--max-turns`, `--interactivo`) |
| `app.py` | Cliente Streamlit (chat + expander debug) |
| `.streamlit/config.toml` | Tema visual de la app |

---

## Qué NO hace

- No consulta bases de datos ni RAG.
- No usa tools / function calling (eso viene después).
- No usa LangGraph en código.
- No HITL formal ni multi-agente.

---

## Repasar conceptos

1. *¿Para qué sirven `max_turns` y la `traza`?*
2. *¿Quién decide `done` — el LLM o Python?*
3. *¿Qué vive en `messages` de Streamlit y qué en `agent_state`?*

## Experimentos

1. **Demo completa** — `python main.py`. Mira el resumen (`done`, `corte`) y luego la `traza` en el JSON.
2. **`max_turns` bajo** — `python main.py --max-turns 2` (hay 5 msgs en la demo → solo corre 2). Resumen: `corte: max_turns`. En Streamlit: slider `max_turns=1` y un mensaje.
3. **`done` incompleto** — Di solo “quiero algo cultural” (sin presupuesto ni zona). El agente debe preguntar; `done` sigue `false`.
4. **`done` completo** — Da intereses + presupuesto + zona y confirma (“sí, adelante”). Con plan ≥2 actividades, `done` pasa a `true` y el chat se cierra (Streamlit).
5. **Plan intermedio** — En Streamlit, si hay ítems en `plan` pero `done=false`, verás **Plan (borrador):** en el chat.
6. **Modo interactivo** — `python main.py --interactivo`: varios mensajes seguidos y mira cómo crece `traza` turno a turno en el JSON final.
7. **Dos memorias** — En Streamlit, escribe 2–3 mensajes. Compara el historial del chat (`messages`) con el expander (`agent_state`: preferencias, plan, traza).
8. **Nueva conversación** — Cierra un plan (`done`) y pulsa «Nueva conversación»: chat y `agent_state` deben resetearse.
9. **Error controlado** — Pon una API key inválida en `.env`, reinicia y manda un mensaje: debe aparecer `error` en el estado y un mensaje amigable (sin tumbar la app).

