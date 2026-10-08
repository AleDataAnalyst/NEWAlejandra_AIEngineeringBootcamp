![Cabecera](../../assets/cabecera_agentes.png)

# Validación y allowlist

El modelo puede pedir **cualquier** nombre de función que se le ocurra. Tu código solo debe ejecutar las que **tú** registraste.

---

## Allowlist

```python
if nombre not in TOOL_REGISTRY:
    # No ejecutes. Devuelve error al modelo o márcalo en traza.
    return f"Error: tool '{nombre}' no está permitida."
```

Opciones pedagógicas:

| Estrategia | Efecto |
|------------|--------|
| Devolver error como `function_response` | El LLM puede disculparse / seguir sin esa tool |
| Subir `estado["error"]` y cortar | Más estricto; útil si el fallo es grave |

Consejo práctico: **mensaje de error a la tool response** + seguir el loop suele bastar.

---

## Validar parámetros

Antes de `fn(**args)`:

1. ¿Keys esperadas? (ignora extras o recházalos).
2. ¿Tipos básicos? (`limite` → `int`, acotado 1…10).
3. ¿Strings vacíos? (`consulta` en RAG no puede ir vacía).

```python
def _validar_eventos(args: dict) -> dict:
    limite = int(args.get("limite") or 5)
    limite = max(1, min(limite, 10))
    return {"limite": limite}
```

No hace falta Pydantic en este sprint: validación explícita y corta.

---

## Qué queda fuera (a propósito)

- Sandboxing OS, autenticación OAuth de tools, prompt-injection duro.
- Eso es seguridad avanzada; aquí el mensaje es: **solo corro lo registrado y con args saneados**.
