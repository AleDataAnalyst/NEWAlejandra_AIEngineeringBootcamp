# Menú de funcionalidades para la práctica

Elige **una**. Todas caben en una spec pequeña, se pueden testear sin API y **no obligan a regenerar el índice**. Copia la idea detrás del comando: `/sdd-spec <idea>`.

| # | Funcionalidad | Tamaño | Se prueba sin API | Idea para `/sdd-spec` |
|---|---|---|---|---|
| 1 | **Errores amigables** | S | Sí | Que cualquier fallo del índice o de la API se devuelva como un mensaje claro para la persona usuaria, sin trazas de Python, tanto en la CLI como en la web. |
| 2 | **`rag_ask()` para Agentes** | S | Sí | Una función que reciba una consulta y devuelva un único texto con la respuesta y sus fuentes, pensada para usarse como tool de un agente. |
| 3 | **Citas explícitas** | S | Sí | Que cada respuesta termine con una línea de fuentes que coincida exactamente con los documentos usados como contexto. |
| 4 | **Validación de entrada reforzada** | S | Sí | Que el sistema rechace, sin llamar al LLM, las preguntas demasiado cortas, las formadas solo por signos y las que intentan inyectar instrucciones con las variantes más habituales. |
| 5 | **Registro de consultas** | M | Sí (archivo temporal) | Que cada consulta quede registrada en un archivo con la pregunta, K, el número de fragmentos, el tiempo, el modelo y si hubo abstención. |
| 6 | **Tabla de métricas en Streamlit** | M | En parte (la web, a mano) | Que la app web muestre bajo cada respuesta una tabla con K, el número de fragmentos usados, el tiempo de respuesta y el modelo. |
| 7 | **Abstención por baja relevancia** (la de la demo) | M | Sí | Que el asistente se abstenga sin llamar al LLM cuando los fragmentos recuperados no sean relevantes para la pregunta. |
| 8 | **Evaluación con puntuación** | M | Sí (retriever falso) | Que la evaluación del retrieval compare la mejor fuente recuperada con la fuente esperada de cada pregunta y dé el porcentaje de aciertos para cada K. |
| 9 | **Feedback 👍 / 👎** | M | En parte (la web, a mano) | Que la persona usuaria pueda valorar cada respuesta con 👍 o 👎 en la app web y ver un recuento de las valoraciones de la sesión. |

**S** ≈ la spec sale con 4-6 RF · **M** ≈ 7-10 RF.

## ¿Tu propia idea?
Adelante si cumple las tres condiciones:
1. Cabe en **una** spec de 8 RF como mucho.
2. Se puede comprobar con tests **sin llamar a ninguna API**.
3. **No** obliga a regenerar embeddings ni el índice (gasta API y tiempo). Los filtros por metadatos nuevos, cambiar el chunking o el modelo de embeddings quedan para después de clase.

## Consejo
Si tu proyecto aún no cumple algo del checklist del Project Break (logging, métricas, abstención, `rag_ask()`…), elige eso. Así la práctica te deja una mejora real en tu repo.
