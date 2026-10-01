# Constitución — RAG de la agenda cultural de Madrid

Principios innegociables. Toda spec, plan, tarea y línea de código debe cumplirlos. Si una petición choca con alguno, el agente se detiene y lo dice.

1. **La spec manda.** No se implementa ningún comportamiento que no esté en una spec aprobada de `specs/`. Si falta una decisión, se para y se pregunta. Si cambia el comportamiento, primero se cambia la spec y después el código.
2. **Anclado al corpus.** El asistente responde solo con información recuperada de `data/`. Si no hay evidencia, se abstiene. Ninguna funcionalidad puede relajar esta regla.
3. **Lógica separada de las interfaces.** Preparar e indexar nunca se mezcla con preguntar. La lógica vive en `src/`. `main.py` (CLI) y `app.py` (Streamlit) son capas finas que usan el mismo contrato, `src.logic.responder()`, y muestran lo mismo.
4. **Tests como puerta, sin API.** Cada tarea termina con `pytest` en verde. Los tests no llaman a Gemini ni a una ChromaDB real: usan dobles de prueba. Prohibido avanzar con tests en rojo.
5. **Configuración en un solo sitio.** Rutas, modelos, K y umbrales van en `config.py`. Las claves van solo en `.env` y nunca en el código ni en el repositorio.
6. **Stack cerrado.** Python 3.9+, LangChain, Gemini, ChromaDB, Streamlit y pytest. No se añaden dependencias sin actualizar antes la spec y el plan.
7. **Idioma.** Identificadores, mensajes y documentación en español, como el resto del proyecto.
