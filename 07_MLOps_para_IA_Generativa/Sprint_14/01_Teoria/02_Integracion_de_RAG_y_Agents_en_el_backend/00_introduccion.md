![Cabecera](../../../../06_AI_Agents_Engineering/Sprint_11/assets/cabecera_thebridge.png)

# Introducción — El backend es el contrato

En S10–13 aprendisteis a **no** meter la lógica dentro de la UI:

```text
Streamlit / CLI  →  procesar_turno() / responder()
```

En S14 el dibujo es el mismo, con un eslabón HTTP:

```text
Cliente (Swagger, curl, Postman…)
        ↓  HTTP
     FastAPI   ← core de la app en este sprint
        ↓  Python
  procesar_turno() / responder()
        ↓
  RAG · agente · tools · LLM
```

## Qué integra este bloque

1. Reutilizar el contrato del agente/RAG detrás de FastAPI.
2. Definir `POST /ask` (o `/chat`) con body estable.
3. Límites y secrets en el servidor.
4. Entender por qué **dejamos Streamlit** como núcleo: la UI ya no va ligada al core (ver [04](./04_streamlit_como_cliente_http.md)).
5. Practicar en el workout: [05](./05_api_fastAPI_sobre_agente.md) → [repo](https://github.com/aie-online-tb/Sprint14_API_FastAPI_Proyecto_MultiAgente_LangGraph_tarde_cultural).

En el workout de este bloque la API adapta un **agente ya dado** (grafo + tools) detrás de FastAPI.
Si en otro proyecto aún no tenéis el agente, un stub con `respuesta` / `done` sirve para practicar el cableado; la firma es la misma.

---

## Resumen

- La API es un adaptador, no un segundo cerebro.
- Mismo contrato → varios clientes.
