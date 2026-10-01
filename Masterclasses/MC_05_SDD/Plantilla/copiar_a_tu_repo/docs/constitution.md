# Constitución — <Nombre de vuestro RAG>

<!-- Propuesta de partida. Revisadla con /sdd-constitucion: os dirá qué principios no cumple hoy vuestro código. Ajustad lo que haga falta y borrad este comentario. -->

Principios innegociables. Toda spec, plan, tarea y línea de código debe cumplirlos. Si una petición choca con alguno, el agente se detiene y lo dice.

1. **La spec manda.** No se implementa ningún comportamiento que no esté en una spec aprobada de `specs/`. Si falta una decisión, se para y se pregunta. Si cambia el comportamiento, primero se cambia la spec y después el código.
2. **Anclado al corpus.** El asistente responde solo con información recuperada del corpus. Si no hay evidencia, se abstiene. Ninguna funcionalidad puede relajar esta regla.
3. **Lógica separada de las interfaces.** Indexar nunca se mezcla con preguntar. La lógica vive en `src/`. La CLI y Streamlit son capas finas que usan la misma función principal ([COMPLETAR: `responder()` / `rag_ask()`]) y muestran lo mismo.
4. **Tests como puerta, sin API.** Cada tarea termina con `pytest` en verde. Los tests no llaman al LLM, a los embeddings ni a una ChromaDB real: usan dobles de prueba (`docs/tests_sin_api.md`). Prohibido avanzar con tests en rojo.
5. **Configuración en un solo sitio.** Rutas, modelos, K y límites van en `config.py`. Las claves van solo en `.env` y nunca en el código ni en el repositorio.
6. **Stack cerrado.** [COMPLETAR: Python 3.10+, LangChain, vuestro proveedor de LLM y embeddings, ChromaDB, Streamlit y pytest.] No se añaden dependencias sin actualizar antes la spec y el plan.
7. **Idioma.** [COMPLETAR: idioma de identificadores, mensajes y documentación.]
