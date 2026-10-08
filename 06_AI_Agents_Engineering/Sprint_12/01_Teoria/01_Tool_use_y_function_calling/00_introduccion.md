![Cabecera](../../assets/cabecera_agentes.png)

# Introducción — Tool Use y Function Calling

En el Sprint 11 el agente **conversaba** y guardaba estado (`preferencias`, `plan`, `done`), pero **no ejecutaba acciones externas**: no consultaba una API, no buscaba en una guía, no leía la hora real.

Aquí empieza el salto: el modelo **elige** una herramienta y **Python la ejecuta**.

> **Tool use** = el agente pide una acción; el código la hace; el resultado vuelve al modelo.

![Tool Use](../../assets/how_ai_agents_works.jpg)

---

## Objetivos del bloque

Al terminar, deberías poder:

- Explicar qué es una *tool* frente a “el LLM inventa la respuesta”.
- Dibujar el ciclo **agente → tool → resultado → agente**.
- Declarar una tool sencilla (`hora_actual`) para Gemini.
- Ejecutar un loop mínimo de function calling a mano (sin que el SDK lo oculte).

---

## Dos bucles (no los mezcles)

| Loop | Quién da el siguiente paso | Ejemplo |
|------|----------------------------|---------|
| **Conversación (S11)** | El **usuario** escribe otro mensaje | “Zona centro” → el agente actualiza estado |
| **Tool use (S12)** | El **agente** pide tools **dentro** de un turno | “¿Qué hora es?” → `hora_actual` → responde |

En este bloque practicas solo el segundo, con **una** tool.

---

## Salida concreta

Notebook: un agente que, cuando hace falta, llama a `hora_actual` y responde con la hora **real** (no inventada).
