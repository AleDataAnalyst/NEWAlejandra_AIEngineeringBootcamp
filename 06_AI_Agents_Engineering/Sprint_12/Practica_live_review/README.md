# Live Review — Sprint 12

Práctica integradora de **agentes con tools** (function calling, allowlist, `max_steps`, traza, API + fallback).

**Dominio:** calidad del aire.

| Carpeta | Contenido |
|---------|-----------|
| [`01_agente_tools_calidad_aire/`](01_agente_tools_calidad_aire/) | Proyecto alumno (TODOs) |
| [`01_agente_tools_calidad_aire_SOLUTION/`](01_agente_tools_calidad_aire_SOLUTION/) | Referencia del profesor |

## Resumen

- **Dominio:** orientar una consulta sobre calidad del aire en Madrid **usando tools**
- **Código dado:** `state.py`, parte de `llm.py`, `hora_actual`, `RAG_buscar_en_guia`, `API_consultar_calidad_aire` (+ fallback), `main.py`, `app.py`, `verificar.py`
- **Implementación del alumno:** allowlist / `validar_args` / `ejecutar_tool`, hueco del loop FC (`run_tool_loop`), `procesar_turno` + `run_demo`
- **`app.py`:** dado (cliente de `procesar_turno`)
- **Contrato:**

```text
mensaje → procesar_turno(estado, mensaje, max_steps)
       → run_tool_loop (FC) → sintetizar_estado (JSON)
       → actualizar_estado → calcular_done → traza (con tools)
CLI / Streamlit = clientes
```
