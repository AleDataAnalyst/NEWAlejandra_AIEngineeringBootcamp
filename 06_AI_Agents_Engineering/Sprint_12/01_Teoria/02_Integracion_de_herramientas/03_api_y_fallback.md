![Cabecera](../../../Sprint_11/assets/cabecera_thebridge.png)

# API y fallback

La tercera tool habla con el mundo exterior:

> `API_consultar_eventos_madrid(limite: int = 5) -> str`

La API de Madrid devuelve un catálogo **grande** (`@graph`). Esta tool no implementa un buscador: solo trae los **primeros N** eventos y los resume. Si el usuario quiere filtrar por tema o zona, el modelo lo hace en lenguaje natural con ese resumen (o usa la guía RAG).

---

## Fuente

Open data del Ayuntamiento de Madrid — agenda de eventos culturales (JSON):

`https://datos.madrid.es/egob/catalogo/206974-0-agenda-eventos-culturales-100.json`

La tool debe:

1. Hacer `GET` con timeout.
2. Quedarse con los **primeros `limite`** eventos.
3. Devolver título, lugar y fecha, no el JSON crudo.

---

## Fallback local

Si la red falla → `data/eventos_fallback.json` y el mismo recorte/resumen.

```text
GET API  ──ok──► primeros N ► resumen (str)   Fuente: api
    │
    └──fail──► JSON local ► primeros N ► resumen   Fuente: fallback
```

Así la demo no depende de que Madrid responda en ese segundo.

---

## Dónde se practica

En el **workout del Bloque 2** (`tools/api_eventos.py` + notebook).  
En el Bloque 3 se reutiliza el mismo patrón dentro del proyecto (carpeta independiente) con más control y UI.

---

## Qué no hacer

- Devolver el `@graph` entero al LLM.
- Inventar eventos si fallan API **y** fallback.
- Mezclar “error de red” con “no hay resultados”.
