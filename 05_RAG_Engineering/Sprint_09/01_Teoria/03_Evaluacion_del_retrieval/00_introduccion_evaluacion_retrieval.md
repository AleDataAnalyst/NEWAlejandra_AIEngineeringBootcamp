![Cabecera](../../assets/cabecera_rag.png)

# Introducción: evaluación del retrieval

Si solo pruebas una pregunta que «sale bien», no sabes si tu RAG es robusto. La **evaluación del retrieval** mira exclusivamente la capa de búsqueda: ¿los chunks correctos aparecen en el top-K?

> Evaluaremos el **contexto recuperado**. En el Sprint 10 evaluaremos **respuestas generadas**.

---

## Objetivos del bloque

Al terminar, deberías poder:

- Definir un **conjunto de preguntas de prueba** para tu corpus.
- Detectar **fallos típicos** (chunk partido, K bajo, pregunta fuera de corpus).
- Ajustar **chunking** y **top-K** con criterio.
- Usar **logging** para depurar sin culpar al LLM.
- Comparar configuraciones y documentar una decisión.

---

## Por qué antes del LLM

```text
  Retrieval malo  +  LLM bueno  →  respuesta convincente pero incorrecta
  Retrieval bueno +  LLM malo    →  al menos el contexto era útil
```

Si el contexto no contiene la respuesta, ningún prompt salvará el sistema. Evaluar retrieval primero es **más barato** (sin tokens de generación) y **más claro** (ves el texto exacto recuperado).