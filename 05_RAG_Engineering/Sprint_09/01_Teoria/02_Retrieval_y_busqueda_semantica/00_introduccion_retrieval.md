![Cabecera](../../assets/cabecera_rag.png)

# Introducción: retrieval

El **retrieval** es la fase en la que el sistema **busca** en el índice vectorial los fragmentos más relevantes para la pregunta del usuario. Es el corazón de la «R» en RAG.

> **Retriever** = componente que transforma una pregunta en una lista ordenada de chunks candidatos.

![retrieval](../../assets/rag2.avif)

---

## Objetivos del bloque

Al terminar, deberías poder:

- Explicar qué hace el retriever en el pipeline RAG.
- Embeddear una **consulta** con el mismo modelo que el índice.
- Ejecutar **similarity search** y seleccionar **top-K** resultados.
- **Formatear el contexto** recuperado para inspección (y para S10, para el prompt).

---

## Pasos 1–5 del pipeline online

Cuando el índice ya está creado, cada consulta sigue:

```text
  1. Entrada del usuario     →  pregunta en lenguaje natural
  2. Embedding de consulta   →  mismo modelo que al indexar
  3. Búsqueda en el índice   →  collection.query()
  4. Top-K                   →  K fragmentos más cercanos
  5. Contexto recuperado     →  texto concatenado con fuentes
```

En **Sprint 9** practicas hasta el paso 5. En **Sprint 10** añades:

```text
  6. Prompt al LLM           →  instrucciones + contexto + pregunta
  7. Generación              →  respuesta de Gemini
```

---

## Analogía con Sprint 5

```text
S5 (manual)                 S9 (automático)
───────────                 ───────────────
consulta                    consulta
   │                           │
   ▼                           ▼
seleccionar_faq()          retriever (Chroma + embeddings)
   │                           │
   ▼                           ▼
build_chat_prompt()        formatear_contexto()   ← S10: build_rag_prompt()
```

La diferencia no es el LLM final (aún no lo usas): es **cómo eliges el contexto**. En el Sprint 5 el contexto se seleccionaba manualmente, mientras que en el Sprint 9 se selecciona automáticamente utilizando retrieval.
