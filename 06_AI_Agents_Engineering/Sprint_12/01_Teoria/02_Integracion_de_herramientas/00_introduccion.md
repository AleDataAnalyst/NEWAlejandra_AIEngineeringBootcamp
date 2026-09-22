![Cabecera](../../../Sprint_11/assets/cabecera_thebridge.png)

# Introducción — Integración de herramientas

En el Bloque 1 viste **una** tool y el ciclo de function calling. Aquí pasas a **varias** tools reales del dominio:

| Tool | Qué aporta |
|------|------------|
| `hora_actual` | Utilidad |
| `RAG_buscar_en_guia` | Retrieve mínimo reutilizado como tool |
| `API_consultar_eventos_madrid` | API externa + fallback |

> El reto ya no es “¿funciona el ciclo?”, sino “¿cómo organizo tools en Python y qué le devuelvo al LLM?”.

---

## Objetivos del bloque

- Modularizar tools (`tools/` + registro por nombre).
- Envolver un **retrieve mínimo** como `RAG_buscar_en_guia`.
- Llamar a una **API** con fallback local.
- Gestionar respuestas y errores básicos (allowlist, mensajes de error).
- Practicar un loop multi-tool en notebook.

---

## Escalera

```text
B1  hora_actual (FC manual / AFC)
B2  tools/ + hora + RAG + API     ← este bloque
B3  mismo patrón + control + UI
```

---

## Idea clave

Cada tool debe devolver un **string corto y útil**.  
Si le pasas al modelo un JSON de 1 MB, no has integrado una tool: has inundado el contexto.
