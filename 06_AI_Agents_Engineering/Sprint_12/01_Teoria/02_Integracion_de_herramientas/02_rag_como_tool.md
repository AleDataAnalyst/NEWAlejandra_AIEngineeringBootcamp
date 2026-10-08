![Cabecera](../../assets/cabecera_agentes.png)

# RAG como tool

En Sprint 10 construiste un pipeline RAG (cargar → chunk → embed → recuperar → generar).  
En Sprint 12 **no reimportas** esas carpetas: **reutilizas la idea del retrieve** con un código mínimo y lo envuelves en una función.

> Tool: `RAG_buscar_en_guia(consulta: str) -> str`

---

## Qué ve el LLM

| Mal | Bien |
|-----|------|
| 20 chunks crudos de 2 páginas | 2–3 pasajes cortos |
| Dump del vector store | Texto usable |
| Silencio si no hay hits | Mensaje claro: “No hay nada en la guía sobre X” |

La tool **recupera**; el modelo **genera** la respuesta al usuario después.

---

## Retrieve mínimo de este sprint

1. Cargar `data/guia_cultural.txt`.
2. Partir en trozos (secciones `##`).
3. Puntuar por **solapamiento de términos**.
4. Devolver top‑k unidos.

Es el mismo código mínimo de retrieval del material, **empaquetado como tool**.  
Si más adelante cambias el interior (embeddings/Chroma), el contrato del agente no cambia.

---

## Analogía con “bases de datos”

| En S10 | En este workout |
|--------|-----------------|
| Vector store (Chroma) | Fichero guía (o podría ser una BBDD) |
| `recuperar(pregunta)` | `RAG_buscar_en_guia(consulta)` |

La tool es la **puerta**; la fuente de datos es un detalle de implementación.

---

## Cuándo usarla

- Normas, tips, FAQ de la guía.
- **No** sustituye el catálogo de eventos en vivo (eso es la API).
