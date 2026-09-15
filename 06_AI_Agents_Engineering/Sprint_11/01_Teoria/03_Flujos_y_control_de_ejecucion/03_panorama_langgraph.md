![Cabecera](../../assets/cabecera_thebridge.png)

# Panorama LangGraph (sin código aún)

En la industria muchos equipos orquestan agentes con **grafos de estado**. [LangGraph](https://langchain-ai.github.io/langgraph/) es una opción habitual sobre el ecosistema LangChain.

En Sprint 11 **no lo implementas**. Solo necesitas el mapa mental para que S12 no sea un salto a ciegas.

---

## Ideas clave

| Concepto | Analogía con lo que ya haces |
|----------|------------------------------|
| **State** | Tu `AgentState` |
| **Node** | Una función: “extraer preferencias”, “proponer plan”, “cerrar” |
| **Edge** | La decisión de ir al siguiente nodo o al END |
| **Graph** | El `while` + condiciones de parada, dibujado como diagrama |

```text
[START] → [razonar/actualizar] → ¿done o max_turns?
                ↑_________|               |
                                          ▼
                                        [END]
```

Con tools (S12) aparecen nodos del estilo “llamar tool” y “procesar resultado”.

---

## Por qué no en S11

1. Primero debes **entender** loop + estado a mano.
2. Si empiezas por el framework, confundes API de LangGraph con la idea de agente.
3. El tiempo de la semana junior no da para framework + fundamentos.

---

## Qué haréis en S12

- Añadir **tools** con function calling (RAG, API, utilidades) y control (`max_steps`).
- Ver LangGraph solo como **panorama** (el core del proyecto sigue siendo el loop en Python).
- Seguir usando Gemini.

---

## Para llevarte

LangGraph **no reemplaza** la necesidad de diseñar buen estado y buenas paradas: las exige de forma más explícita.
