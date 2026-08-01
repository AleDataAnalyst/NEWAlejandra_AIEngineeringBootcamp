![Cabecera](../../assets/cabecera_rag.png)

# Buenas prácticas y limitaciones de un RAG

## Objetivos

- Enumerar buenas prácticas para trabajar en un proyecto RAG.
- Enumerar limitaciones reales: corpus, chunking, top-K, modelo, latencia.

---

## 1) Buenas prácticas

| Práctica | Por qué |
|----------|---------|
| Evaluar **retrieval y generación** por separado | Sabes qué capa falló |
| Centralizar config (`TOP_K`, modelos, temperatura) | Experimentar sin tocar lógica |
| Prompt con **grounding** y abstención | Menos alucinaciones |
| Validar **antes** del LLM | Menos coste y más robustez |
| Mostrar **fuentes** al usuario | Confianza y depuración |
| Loguear / inspeccionar contexto en desarrollo | `--query` antes de confiar en `--ask` |
| Set fijo de preguntas | Comparar cambios de config |

---

## 2) Limitaciones a tener en cuenta

| Limitación | Ejemplo |
|------------|---------|
| **Corpus incompleto** | Pregunta sobre un evento no indexado |
| **Chunking** | La respuesta está partida entre dos chunks y K=1 no basta |
| **Top-K bajo** | Falta evidencia; K alto → ruido |
| **Índice parcial** | `MAX_CHUNKS_EMBED = 5` en demo → cobertura pobre |
| **Modelo** | Resume mal, ignora instrucciones o inventa |
| **Latencia / coste** | Cada consulta = embed + generate (+ UI) |
| **No es un buscador perfecto** | Semántica ≠ verdad absoluta |

Un RAG **no** sustituye:

- bases de datos transaccionales en tiempo real,
- reglas de negocio críticas sin validación,
- un experto humano en dominios sensibles.

---

## 3) Checklist para sistemas RAG

Antes de desplegar un sistema de recuperación aumentada por generación, revisa:

- [ ] El corpus y el índice están correctamente construidos y accesibles
- [ ] El sistema responde adecuadamente a preguntas típicas y sencillas
- [ ] Puede manejar preguntas fuera del dominio previsto mediante abstención o errores controlados
- [ ] Las fuentes utilizadas en la respuesta son visibles y comprobables
- [ ] Conoces las causas y posibles soluciones para los fallos más frecuentes

---

## Resumen

- Buenas prácticas = evaluar por capas, grounding, validar, citar.
- Las limitaciones son del corpus, del chunking, del K y del modelo — no «magia del LLM».
- Es importante tener en cuenta las limitaciones de un sistema RAG para garantizar que el sistema se comporte de forma ética y responsable.
