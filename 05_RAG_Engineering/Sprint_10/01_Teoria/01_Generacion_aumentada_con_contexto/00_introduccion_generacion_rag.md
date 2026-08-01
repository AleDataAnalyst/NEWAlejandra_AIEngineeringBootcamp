![Cabecera](../../assets/cabecera_rag.png)

# Introducción: generación RAG

En el Sprint 9 el pipeline terminaba en **contexto recuperado**: chunks ordenados, con fuentes y distancias. El LLM **aún no redactaba** la respuesta final. En este bloque **cierras el ciclo RAG**: usas ese contexto para **generar** una respuesta al usuario.

> **Generación aumentada** = el modelo responde apoyándose en fragmentos recuperados del corpus, no solo en su memoria interna.

---

## Objetivos del bloque

Al terminar, deberías poder:

- Explicar la diferencia entre **retrieval** y **generación**.
- Describir los pasos 6–7 del pipeline online (prompt + LLM).
- Construir un prompt que separe **instrucciones**, **contexto** y **pregunta**.
- Generar una respuesta con Gemini a partir del contexto de `context.py`.
- Entender que el proveedor del LLM puede cambiar (p. ej. Hugging Face) sin rehacer el retriever.

![Pipeline RAG](../../assets/rag3.gif)

---

## Puente desde Sprint 9

```text
Sprint 9                          Sprint 10 (este bloque)
────────                          ───────────────────────
pregunta → retriever → contexto   pregunta → retriever → contexto
                                              ↓
                                         prompt + LLM
                                              ↓
                                          respuesta
```

El módulo `context.py` del proyecto S9 **no se tira**: el mismo texto formateado entra al prompt. Lo que añades es:

| Módulo | Qué hace |
|--------|----------|
| `prompts.py` | Ensambla instrucciones + contexto + pregunta |
| `generate.py` | Llama al LLM (Gemini) |
| `logic.py` | Orquesta: `responder(pregunta)` |

---

## Pasos 6–7 del pipeline online

En Sprint 8–9 viste los pasos 1–5. Aquí cierras el ciclo:

```text
  1. Entrada del usuario
  2. Embedding de la consulta
  3. Búsqueda en el índice
  4. Top-K
  5. Contexto recuperado          ← hasta aquí S9
  6. Prompt al LLM                ← este bloque
  7. Generación de la respuesta   ← este bloque
```

Sin el paso 6–7 tienes un **motor de búsqueda semántica**. Con ellos tienes un pipeline completo de **RAG**. En los últimos sprints hemos ido viendo por piezas cada paso de este pipeline.

---

## Salida del bloque

Un pipeline online que, dada una pregunta, devuelve:

- una **respuesta** en lenguaje natural,
- **fuentes** (archivos de los chunks usados),
- el **contexto** recuperado (para depurar).


---

## Resumen

- S9 recupera contexto; S10 **genera** con ese contexto.
- RAG = retrieval + generación, no solo uno de los dos.
- Reutilizas `context.py`; añades prompt + LLM.
