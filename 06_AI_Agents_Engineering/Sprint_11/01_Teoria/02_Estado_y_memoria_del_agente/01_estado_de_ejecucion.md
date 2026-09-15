![Cabecera](../../assets/cabecera_thebridge.png)

# Estado de ejecución (`AgentState`)

El estado es la **fuente de verdad** del agente durante la conversación / corrida. El LLM sugiere cambios; tu código los valida y escribe.

---

## Campos recomendados (S11 · tarde cultural)

```python
from typing import Any

AgentState = dict[str, Any]

# Ejemplo de forma:
{
    "objetivo": "Planificar una tarde cultural",
    "pedido_original": "Quiero una tarde cultural.",
    "preferencias": {
        "intereses": ["cine", "musica"],   # o None al inicio
        "presupuesto": "gratis_o_barato",
        "zona": "centro",
        "duracion_horas": 3,               # opcional; si falta, el LLM puede sugerirla
    },
    "plan": [],              # ítems del plan (vacío hasta poder cerrar)
    "respuesta": "",         # último texto para el usuario
    "done": False,
}
```

No hace falta un campo `faltantes`: se **deduce** mirando `preferencias` (p. ej. `tenemos_datos_minimos`).

Puedes usar `@dataclass` si te resulta más claro; en workouts usamos dict por simplicidad.

---

## Reglas de diseño

1. **Campos con nombre estable** — el prompt y el código deben hablar el mismo idioma.
2. **El LLM no “es” la memoria** — si no lo escribes en el estado, en el siguiente turno se pierde (salvo que lo reinyectes entero en el prompt).
3. **`done` (y en Bloque 3, `error` / `max_steps`) lo controla el código** — el LLM rellena preferencias, plan y respuesta; Python calcula `done`.

---

## Inicialización

```python
def crear_estado(pedido: str) -> dict:
    return {
        "objetivo": "Planificar una tarde cultural",
        "pedido_original": pedido,
        "preferencias": {
            "intereses": None,
            "presupuesto": None,
            "zona": None,
            "duracion_horas": None,
        },
        "plan": [],
        "respuesta": "",
        "done": False,
    }
```

---

## Actualización (idea)

```python
def actualizar_estado(estado: dict, cambios: dict) -> dict:
    nuevo = copy.deepcopy(estado)
    prefs_nuevas = cambios.get("preferencias") or {}
    for clave, valor in prefs_nuevas.items():
        if valor is not None:
            nuevo["preferencias"][clave] = valor
    if isinstance(cambios.get("plan"), list):
        nuevo["plan"] = cambios["plan"]
    if "respuesta" in cambios:
        nuevo["respuesta"] = cambios["respuesta"]
    # `done` no se copia del LLM: lo calcula Python (ver `calcular_done`)
    return nuevo
```

El detalle del parseo JSON está en el documento 3 de este bloque.

---

## Para llevarte

`AgentState` es un **contrato interno**, igual que `responder() → dict` era el contrato externo en S10. Si el estado es confuso, el agente será confuso.
