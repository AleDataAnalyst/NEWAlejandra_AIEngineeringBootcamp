![Cabecera](../../assets/cabecera_rag.png)

# Cómo evaluar respuestas RAG

## Objetivos

- Definir criterios prácticos para evaluar respuestas generadas por un sistema.
- Utilizar un conjunto de preguntas de prueba con campos relevantes para la evaluación (ejemplo: evaluar_respuestas.json)
- Registrar y analizar los resultados de forma manual en una primera etapa, sin depender de herramientas totalmente automatizadas.

---

## 1) Criterios prácticos

| Criterio | Pregunta que te haces |
|----------|------------------------|
| **Exactitud** | ¿Lo dicho está en el contexto / corpus? |
| **Relevancia** | ¿Responde a la pregunta formulada? |
| **Coherencia** | ¿Está bien redactado y es consistente? |
| **Trazabilidad** | ¿Puedes vincular afirmaciones a una fuente? |
| **Formato** *(si pides JSON)* | ¿Parsea? ¿Respeta el esquema? |

Un JSON **válido** no implica respuesta correcta: puede parsear y aun así alucinar. Evalúa formato y contenido por separado.

No necesitas LLM-as-judge ni métricas académicas para empezar. Sí necesitas **rigor manual** con un set fijo de preguntas. 

Es importante observar el comportamiento del sistema con un conjunto de preguntas fijo y no depender de herramientas totalmente automatizadas.

---

## 2) Ejemplo de rúbrica orientativa para evaluar respuestas RAG

Para cada pregunta, marca un veredicto:

| Símbolo | Significado |
|---------|-------------|
| ✅ | Acierto: correcta y basada en el contexto |
| ⚠️ | Parcial: algo útil pero incompleto o ruidoso |
| ❌ | Fallo: no responde bien (sin inventar necesariamente) |
| 🛑 | Alucinación: inventa hechos no presentes |
| ⏸️ | Debería abstenerse (y lo hace, o debería) |

Ejemplo con el JSON del sprint:

| id | Pregunta | Qué esperas |
|----|----------|-------------|
| q1 | ¿Qué significa GRATUITO? | Explicación FAQ (1 vs 0) |
| q2 | ¿Hay cine gratuito en verano? | Eventos del CSV, con fuentes |
| q3 | ¿Actividades en el Retiro? | Eventos RETIRO / Retiro |
| q4 | ¿Para qué sirve el PDF? | Documentación, no listado de eventos |
| q5 | ¿Capital de Francia? | Abstención (`deberia_abstenerse: true`) |

---

## 3) Procedimiento recomendado

1. Indexa el corpus con el mismo `MAX_CHUNKS_EMBED` / config que uses en demo.
2. Para cada pregunta: ejecuta el proceso de evaluación con la herramienta o script que utilices (puede ser desde línea de comandos, un notebook, o la interfaz seleccionada). Ejemplo: `python main.py --ask "…"` (o el notebook).
3. Anota: veredicto, fuentes mostradas, si el contexto recuperado era bueno.
4. Si falla, **separa capas**:
   - ¿El contexto ya era malo? → vuelve a S9 (K, chunking, índice).
   - ¿El contexto era bueno y la respuesta mala? → prompt / temperatura / validación.

---

## 4) Ejemplo de Tabla de resultados (plantilla)

- q1, q2.... son las preguntas del dataset de evaluación.

| id | Veredicto | ¿Contexto OK? | ¿Fuentes OK? | Acción |
|----|-----------|---------------|--------------|--------|
| q1 | ✅ | Sí | Sí | — |
| q2 | ⚠️ | Sí | Parcial | Subir K o mejorar prompt de citas |
| q5 | 🛑 | Irrelevante | — | Endurecer prompt / abstención |

Guarda esta tabla en tus notas o en el notebook: es tu **baseline** antes de tocar parámetros.

---

## Resumen

- Criterios: exactitud, relevancia, coherencia, trazabilidad.
- Rúbrica manual + set fijo de preguntas.
- Separa fallos de retrieval y fallos de generación.