![Cabecera](../../assets/cabecera_rag.png)

# Introducción: evaluación de respuestas generadas

En el Sprint 9 evaluaste **si el retrieval devolvía buenos chunks**. En este bloque evalúas **si la respuesta final es correcta, útil y fiable**.

> Un retrieval perfecto **no garantiza** una buena respuesta: el LLM puede ignorar el contexto, mezclar ruido o inventar.

---

## Objetivos del bloque

Al terminar, deberías poder:

- Diferenciar evaluación de **retrieval** vs evaluación de **generación**.
- Aplicar criterios: exactitud, relevancia, coherencia, trazabilidad.
- Detectar alucinaciones y casos donde debe **abstenerse**.
- Proponer ajustes (prompt, top-K, chunking) según el tipo de fallo.

---

## Retrieval vs generación

| | Sprint 9 | Sprint 10 |
|--|----------|-------------------------|
| **Qué miras** | Chunks recuperados | Texto de la respuesta |
| **Pregunta clave** | ¿Llegó la evidencia correcta? | ¿El LLM usó bien esa evidencia? |
| **Herramienta** | Evaluación automática, análisis de fuentes | Evaluación manual, criterios cualitativos, conjunto de preguntas |
| **Fallo típico** | Top-K malo, chunking, índice incompleto | Alucinación, ruido, prompt permisivo |

Puedes tener:

- Retrieval **bueno** + respuesta **mala** (prompt flojo o modelo que inventa).
- Retrieval **malo** + respuesta «bonita» pero **incorrecta** (alucinación con estilo).

Por eso se evalúan **por separado** y después juntos. Un retrieval bueno no garantiza una respuesta buena.

---

## Dataset de evaluación

En un archivo de dataset de evaluación, cada pregunta puede incluir campos como:

| Campo                | Uso                                              |
|----------------------|--------------------------------------------------|
| `fuente_esperada`    | Fuente esperada de la evidencia                  |
| `respuesta_esperada` | Respuesta esperada para comprobar la corrección   |
| `deberia_abstenerse` | Indica si se espera abstención por falta de evidencia (`true`/`false`) |
| `notas`              | Observaciones o aclaraciones sobre el caso        |

Ejemplo típico: una pregunta sin evidencia en el corpus sirve para comprobar el correcto funcionamiento de la abstención.

---

## Salida del bloque

Un hábito de ingeniero RAG:

1. Ejecutar un set fijo de preguntas.
2. Clasificar cada respuesta (acierto / parcial / fallo / alucinación / abstención).
3. Decidir **qué capa tocar** (retrieval, prompt, validación, datos).

---

## Resumen

- S9 midió contexto; S10 mide **respuesta**.
- Un buen chunk no basta si el prompt no obliga a grounding.
- Evaluación de retrieval y generación por separado.
- Un retrieval bueno no garantiza una respuesta buena.
- Un prompt bueno no garantiza una respuesta buena.
- Un modelo de LLM bueno no garantiza una respuesta buena.
- Un dataset de evaluación bien diseñado puede ayudar a mejorar la calidad de nuestros RAGs.