![Cabecera](../../assets/cabecera_thebridge.png)

# Actualizar estado con estructura (JSON)

En Sprint 10 pediste al modelo un JSON con `respuesta`, `hay_evidencia`, `fuentes_citadas`. Aquí reutilizas el mismo hábito: **salida estructurada → código**.

---

## Por qué no actualizar solo con prosa

Si el modelo responde:

> “He apuntado que te gusta el cine y propongo el Cine Doré…”

tu código tiene que **parsear lenguaje natural** (frágil). Mejor:

```json
{
  "preferencias": {
    "intereses": ["cine"],
    "presupuesto": "gratis_o_barato",
    "zona": null,
    "duracion_horas": null
  },
  "plan": [],
  "respuesta": "¿En qué zona te viene mejor?"
}
```

El campo `done` **no** viene del LLM: lo calcula Python.

---

## Prompt mínimo (idea)

```text
Eres un planificador cultural. Dado el ESTADO actual y el MENSAJE del usuario,
devuelve SOLO un JSON válido con:
preferencias, plan, respuesta.

Si faltan intereses, presupuesto o zona: pregunta y plan=[].
duracion_horas es opcional (si falta al cerrar, el LLM puede sugerirla).
Solo rellena el plan (2–4 ítems) cuando haya datos mínimos y el usuario confirme.
No incluyas "done": lo calcula el código.
```

Concatenas `json.dumps(estado)` y el mensaje del turno.

---

## Parseo simple (eco S10)

```python
import json

def leer_json(texto: str) -> dict:
    texto = texto.strip()
    if texto.startswith("```"):
        lineas = texto.splitlines()
        texto = "\n".join(lineas[1:-1]).strip()
    return json.loads(texto)
```

Si falla: en Bloque 3 verás cómo capturar el error y parar o reintentar.

---

## Bucle conversacional con estado

```python
estado = crear_estado("Quiero una tarde cultural.")
for mensaje in turnos_usuario:
    if estado["done"]:
        break
    cambios = preguntar_al_modelo(estado, mensaje)
    estado = actualizar_estado(estado, cambios)
    estado = calcular_done(estado)  # Python decide done
```

En el workout usas un guion de 4 turnos. En Bloque 3 formalizas límites, errores y la UI.

---

## Continuidad con S10

| S10 | S11 |
|-----|-----|
| JSON de **respuesta RAG** | JSON de **cambios de estado** |
| `hay_evidencia: false` → abstenerse | `done: true` → fin de la tarea (**calculado en código**) |
| Consumidor: UI / eval | Consumidor: `actualizar_estado` + `calcular_done` |

---

## Para llevarte

El agente junior sólido: **LLM propone estructura; Python escribe el estado y decide `done`.**
