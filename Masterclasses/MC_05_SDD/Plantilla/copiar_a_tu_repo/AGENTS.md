# AGENTS.md — <Nombre de vuestro RAG>

<!-- Plantilla. Rellénala con /sdd-contexto: el agente sustituye los [COMPLETAR] leyendo vuestro código. Revisa el resultado antes de aprobarlo. -->

## Proyecto
[COMPLETAR: qué es, en 2-3 frases. Dominio, corpus (formatos y fuentes), pipeline offline (carga → chunking → embeddings → ChromaDB) y online (pregunta → retriever → prompt → LLM), e interfaces (CLI y Streamlit).]

## Mapa del código
| Archivo | Responsabilidad |
|---|---|
| `config.py` | [COMPLETAR] |
| `main.py` | [COMPLETAR: comandos de la CLI] |
| `app.py` | [COMPLETAR: app Streamlit] |
| `src/...` | [COMPLETAR: una fila por módulo] |
| `tests/` | Tests con pytest y dobles de prueba (sin API) |

## Comandos
- Instalar: `pip install -r requirements.txt`
- Tests: `pytest` (no necesita API key)
- Preparar e indexar: [COMPLETAR] ⚠️ gasta API
- Preguntar: [COMPLETAR] ⚠️ gasta API
- Web: `streamlit run app.py` ⚠️ gasta API

## Flujo SDD de este repositorio
- Constitución: `docs/constitution.md`. Léela siempre.
- Specs: `specs/NNN-nombre/` con `spec.md`, `plan.md`, `tasks.md` y `validacion.md`. La spec activa es la de número más alto, salvo que se indique otra.
- Plantillas: `docs/plantillas/`. Chuleta de EARS: `docs/chuleta_ears.md`. Cómo testear sin API: `docs/tests_sin_api.md`.
- Comandos por fase: `.github/prompts/` (`/sdd-contexto`, `/sdd-constitucion`, `/sdd-spec`, `/sdd-clarificar`, `/sdd-plan`, `/sdd-tareas`, `/sdd-implementar`, `/sdd-validar`, `/sdd-cambio`, `/sdd-spec-inversa`).

## Reglas
- Lee `docs/constitution.md` y la spec activa antes de tocar nada.
- Respeta la fase en la que estamos. En spec, clarificación, plan y tareas NO se escribe código.
- En implementación: una sola tarea de `tasks.md` cada vez, tests primero, y te paras al terminarla.
- No modifiques `specs/` salvo que la fase lo pida.
- No añadas dependencias ni cambies el contrato de la función principal (p. ej. `responder()` o `rag_ask()`) si la spec no lo dice.
- No ejecutes comandos marcados con ⚠️ salvo que te lo pida: cuestan dinero y tiempo. Para verificar, usa `pytest`.
- Nunca leas ni muestres el contenido de `.env`.

## Al terminar cualquier tarea
- Ejecuta `pytest` y pega el resumen del resultado.
- Indica qué RF de la spec cubre lo que has hecho.
