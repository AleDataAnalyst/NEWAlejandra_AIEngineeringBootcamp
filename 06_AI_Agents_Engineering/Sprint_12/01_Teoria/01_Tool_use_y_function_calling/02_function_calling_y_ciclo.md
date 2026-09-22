![Cabecera](../../../Sprint_11/assets/cabecera_thebridge.png)

# Function calling y ciclo

**Function calling** (a veces *tool calling*) es el mecanismo de la API del LLM para:

1. Recibir la lista de tools disponibles.
2. Responder con un **function call** estructurado (nombre + args), no solo texto.
3. Recibir después el **resultado** de la tool y continuar.

Por ejemlo, en Gemini lo haces con el SDK `google-genai`: declaras `FunctionDeclaration` / `Tool` y pasas `tools=` en la config.

---

## Ciclo de funcionamiento de un agente con function calling

Podemos ver cómo funciona el ciclo de funcionamiento de un agente con function calling. El agente recibe una pregunta del usuario y debe responderla. Para ello, el agente puede usar las tools disponibles.

```text
Usuario: "¿Qué hora es ahora?"
        │
        ▼
   [LLM + tools declaradas]
        │
        ├── function_call: hora_actual()
        │         │
        │         ▼
        │   Python ejecuta hora_actual()
        │         │
        │         ▼
        │   "2026-08-06T15:04:12"
        │         │
        │         ▼
        └── [LLM ve el resultado]
                  │
                  ▼
            Texto final: "Son las 15:04…"
```

Puede haber **varias** vueltas (varias tools) antes del texto final. Esto se suele limitar con un parámetro `max_steps` en tu script. Este parámetro es un límite para evitar que el agente use demasiadas tools y se quede en un bucle infinito.

---

## Manual vs automático

El SDK de Python puede **ejecutar tools solo** (*automatic function calling*). Este sería el modo automático de funcionamiento de un agente con function calling:

1. Llamada al modelo → ¿pide tool?
2. Si sí: ejecutas tú la función.
3. Devuelves el resultado como `Part.from_function_response` (en Google Gemini) o equivalente según el SDK.
4. Vuelves a llamar al modelo con el historial.

El modo automático es un atajo; **el control** (allowlist, validación, traza) sigue siendo tuyo. Si no quieres usar el modo automático, puedes hacerlo manualmente.

El modo manual es el que te permite tener más control sobre el funcionamiento del agente. En este modo, el agente debe:

1. Detectar cuándo el modelo pide una tool.
2. Ejecutar la función en Python.
3. Devolver el resultado al modelo en el formato esperado (`Part.from_function_response` o equivalente según el SDK).
4. Vuelves a llamar al modelo con el historial.

---

## Contenidos que hay que encadenar

En cada paso el historial crece:

| Rol | Qué lleva |
|-----|-----------|
| `user` | Pregunta del humano |
| `model` | El `function_call` (o el texto final) |
| `tool` | El resultado de Python |

Sin ese encadenamiento, el modelo “olvida” que pidió la tool.

---

## Errores frecuentes

1. **No devolver el resultado** al modelo → se queda a medias o inventa.
2. **Nombre distinto** en declaración vs función Python → fallos silenciosos.
3. **Meter dumps enormes** como resultado de tool → ruido y coste; resume.
4. **Confiar en el LLM para la hora** sin tool → demos que “funcionan” pero mienten.

---

## En resumen

Function calling no es magia: es un **protocolo** (pedir → ejecutar → observar → responder). Debemos tener claros estos pasos para poder hacer un agente con function calling.
