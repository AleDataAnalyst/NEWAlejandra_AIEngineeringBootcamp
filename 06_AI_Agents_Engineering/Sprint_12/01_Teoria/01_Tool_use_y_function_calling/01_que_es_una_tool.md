![Cabecera](../../assets/cabecera_agentes.png)

# Qué es una tool

Una **tool** (herramienta) es una **función de Python** que el agente puede invocar para obtener información o hacer algo que el modelo no debería fingir.

![Tool Use](../../assets/Agent_Tool_Loop.png)

Ejemplos del sprint:

| Tool | Por qué no “inventarla” en prosa |
|------|-----------------------------------|
| `hora_actual` | La hora cambia; el modelo no tiene reloj fiable |
| `RAG_buscar_en_guia` | Debe salir del corpus, no de la memoria del LLM |
| `API_consultar_eventos_madrid` | Eventos reales (o fallback local), no inventados |

---

## Ejemplos de tools

Ponemos algunos ejemplos de tools que el agente puede usar para obtener información o hacer algo que el modelo no debería fingir. Esto es algo orientativo para que te hagas una idea de lo que puede hacer un agente. Recuerda que al final son llamadas a funciones que el agente no puede ejecutar directamente, sino que debe delegar.

| Tool                 | Para qué sirve                                         |
|----------------------|-------------------------------------------------------|
| `hora_actual`        | Consultar la hora real del sistema                     |
| `obtener_clima`      | Saber el clima actual de una ciudad                    |
| `buscar_wikipedia`   | Obtener un resumen corto sobre un tema concreto        |
| `enviar_email`       | Mandar un correo automático a alguien                  |
| `traducir_texto`     | Traducir frases o palabras entre idiomas               |

## Anatomía de una tool

Para el modelo, una tool es un **contrato**:

1. **Nombre** — identificador estable (`hora_actual`).
2. **Descripción** — cuándo usarla (el LLM lee esto).
3. **Parámetros** — schema JSON (tipos, obligatorios).
4. **Implementación** — código Python que **tú** controlas.

```text
Declaración (lo que ve el LLM)     Implementación (lo que corre Python)
─────────────────────────────     ──────────────────────────────────
name: hora_actual                 def hora_actual() -> str:
description: "Devuelve la hora…"      return datetime.now()...
parameters: {} (sin args)
return: "12:00:00"
```

El LLM **no ejecuta** el código. Solo dice: *“quiero `hora_actual` con estos args”*.

---

## Qué no es una tool

- Un prompt largo (“actúa como si buscaras…”).
- Pegar todo un PDF en el contexto y fingir “retrieval”.
- Dejar que el modelo escriba `done=True` o invente URLs.

Si no hay función real detrás, no hay tool use: hay teatro.

---

## En resumen

> El modelo **decide** (¿hace falta una tool?).  
> Python **ejecuta** y **valida** (¿está en la lista? ¿args OK?).

En este sprint veremos cómo crear una tool y cómo usarla en un agente.
