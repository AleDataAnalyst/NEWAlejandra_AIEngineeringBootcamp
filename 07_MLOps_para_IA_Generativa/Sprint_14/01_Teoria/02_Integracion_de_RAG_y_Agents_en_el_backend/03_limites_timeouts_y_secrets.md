![Cabecera](../../../../06_AI_Agents_Engineering/Sprint_11/assets/cabecera_thebridge.png)

# Límites, timeouts y secrets

La API es un buen sitio para **guardrails de borde**. Los del agente (`max_turns`, `done`) siguen en Python dentro de la lógica.

## Quién decide qué

| Control | Dónde |
|---------|--------|
| Longitud de `pregunta` | Pydantic / ruta |
| Timeout HTTP al LLM | Cliente HTTP o wrapper del LLM |
| `max_turns` / `done` | Lógica del agente (como en S11–13) |
| API keys | Variables de entorno |

El LLM **no** debería decidir “¿paro ya?” si Python puede calcularlo.

## Timeouts

Una llamada al modelo puede colgarse. Define un tope razonable en el cliente del LLM o en la capa que llama a `procesar_turno`. Si falla, responde 502/504 con mensaje corto y deja traza en el log del servidor.

## Secrets

```python
import os

API_KEY = os.getenv("GEMINI_API_KEY")
if not API_KEY:
    # Mejor fallar al arrancar o en /ask con 503, no silenciar
    ...
```

Nunca:

- pegues la key en el repo,
- ni la devuelvas en el JSON de error,
- ni la imprimas en logs de alumno compartidos.

## Rate limit (como idea para una API en producción)

Más adelante: limitar peticiones por IP o por API key de cliente. En este curso basta con no exponer el LLM en demos públicas sin control.

---

## Resumen

- Hay dos sitios de control: la **API** (valida la petición) y el **agente** (`max_turns`, `done`).
- Las claves van solo en variables de entorno; nunca en el JSON de error ni en el repo.
