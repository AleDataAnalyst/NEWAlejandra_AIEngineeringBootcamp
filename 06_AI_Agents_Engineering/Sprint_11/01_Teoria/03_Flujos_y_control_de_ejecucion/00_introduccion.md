![Cabecera](../../assets/cabecera_agentes.png)

# Introducción: flujos y control de ejecución

Un agente que “casi siempre” termina en la demo pero a veces gasta turnos de más o traga errores de JSON **no está listo** para enseñar en vivo ni para el Project Break.

En el Bloque 2 ya viste la conversación turno a turno: el LLM devuelve un patch (`preferencias`, `plan`, `respuesta`) y **Python calcula `done`**. Este bloque cierra Sprint 11 empaquetando ese patrón en módulos y añadiendo tres capas:

1. **Parada** — cuándo dejar de aceptar turnos (`done`, `max_turns`, `error`).
2. **Errores + traza** — qué pasó en cada turno.
3. **UI** — Streamlit como cliente de `procesar_turno` (no como sitio donde vive la lógica).

LangGraph aparece solo como **mapa mental**: en S12 lo programaréis.

---

## Objetivos del bloque

Al terminar, deberías poder:

- Aplicar `max_turns` y otras condiciones de parada en una conversación.
- Registrar una traza mínima por turno.
- Reaccionar a fallos de API o de parseo sin tumbar todo en silencio.
- Exponer el agente en Streamlit con chat multi-turno y `AgentState` en sesión.
- Situar LangGraph (nodos / estado / edges) sin implementarlo aún.

---

## Salida concreta

- Función **`procesar_turno(estado, mensaje) → dict`** (+ `run_demo()` para la demo CLI)
- App `streamlit run app.py`
- Proyecto en `05_proyecto_agentes_tarde_cultural_streamlit/`
