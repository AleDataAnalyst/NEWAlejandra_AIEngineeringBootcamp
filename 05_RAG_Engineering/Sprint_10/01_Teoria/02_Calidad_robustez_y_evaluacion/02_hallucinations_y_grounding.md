![Cabecera](../../assets/cabecera_rag.png)

# Alucinaciones y grounding

## Objetivos

- Entender qué es una alucinación en un sistema RAG.
- Reducir invenciones con prompt restrictivo y temperatura baja.
- Saber cuándo la respuesta correcta es **abstenerse**.

---

## 1) Qué son las alucinaciones en RAG

**Alucinación** = afirmar hechos que **no están en el contexto recuperado** (ni, en sentido estricto, en el corpus indexado), presentándolos como si vinieran de ahí.

Es decir, una alucinación es una respuesta que no está justificada por el contexto recuperado. En otras palabras, es una respuesta que se inventó.

No es lo mismo que:

- responder «no lo sé» (abstención correcta),
- resumir mal un chunk (error de comprensión),
- recuperar un chunk irrelevante y basarse en él (fallo de retrieval + generación).

---

## 2) Tipos de fallo frecuentes

| Tipo | Ejemplo |
|------|---------|
| **Inventar** | Añadir un evento que no está en el CSV |
| **Mezclar** | Combinar dos chunks irrelevantes en una historia coherente pero falsa |
| **Ignorar abstención** | Responder París a q5 aunque el contexto sea de agenda cultural |
| **Sobre-confianza** | Afirmar «según el corpus» sin que el hecho aparezca |

---

## 3) Grounding: anclar al contexto

Grounding es "poner los pies a tierra". Es decir, asegurar que la respuesta está justificada por el contexto recuperado.

El prompt es tu primera línea de defensa. En el proyecto:

```text
- Responde ÚNICAMENTE con la información del contexto proporcionado.
- Si el contexto no contiene información suficiente, indícalo explícitamente.
- No inventes eventos, fechas ni datos que no estén en el contexto.
```

Complementos útiles:

- **Temperatura baja** (`GENERATION_TEMPERATURE = 0.2`) → menos creatividad, más apego al texto.
- **Mostrar fuentes** al usuario → obliga a contrastar.
- **Inspeccionar el contexto** antes de confiar en la respuesta (`--query` o expander a otras capas de la aplicación la alucinación).

---

## 4) Prompt permisivo vs restrictivo

Misma pregunta fuera de corpus (q5):

| Prompt | Resultado típico |
|--------|------------------|
| «Responde lo mejor que puedas» | «La capital de Francia es París.» (🛑) |
| «Solo con el contexto; si no basta, dilo» | «No hay información en el contexto sobre…» (⏸️) |

Lo mejor es que hagas tu mismo este experimento para **comparar ambos** con la misma pregunta, así puedes ver el efecto del prompt sin tocar el índice.

---

## 5) Cuándo abstenerse

Abstente (o fuerza abstención) cuando:

- la pregunta está **fuera del dominio** del corpus,
- el top-K es **irrelevante** (distancias altas / fuentes absurdas),
- el contexto está **vacío** (`validators.validar_contexto`).

Abstenerse no es un fallo del sistema: es un **comportamiento deseable** en un asistente grounded. Es decir, un asistente que no alucina y admite que no sabe la respuesta.

---

## Resumen

- Alucinar = inventar respecto al contexto.
- Prompt restrictivo + temperatura baja + fuentes visibles.
- Es importante abstenerse cuando no hay suficiente información en el contexto. Esto es fundamental para garantizar que el asistente no alucine y se comporte de forma ética y responsable.
