# Spec 000 — Sistema actual (línea base)

> Estado: Aprobada · Tipo: spec inversa. Documenta lo que el RAG ya hacía **antes** de trabajar con SDD. No añade nada: describe el código tal como está, para tener una línea base sobre la que especificar cambios.

## Contexto y objetivo
Asistente que responde preguntas sobre la agenda cultural de Madrid a partir de un corpus de datos abiertos (CSV de eventos, PDF de documentación del dataset, FAQ y guía). Evita que la persona tenga que bucear en un CSV de cientos de filas: pregunta en lenguaje natural y recibe una respuesta anclada a los documentos, con sus fuentes.

## Usuarios / actores
- **Persona usuaria**: pregunta por la CLI o por el chat web.
- **Equipo que mantiene el RAG**: prepara el índice, ajusta parámetros y evalúa el retrieval.

## Historias de usuario
- H1: Como equipo, quiero preparar e indexar el corpus una vez, para que las preguntas no tengan que reprocesar los documentos.
- H2: Como persona usuaria, quiero preguntar desde la terminal y ver la respuesta con sus fuentes.
- H3: Como persona usuaria, quiero un chat web donde ver la respuesta, las fuentes y el contexto usado.
- H4: Como equipo, quiero comparar el retrieval con distintos K sobre un conjunto fijo de preguntas.

## Requisitos funcionales (EARS)

### Ingesta (offline)
- RF-1: CUANDO se ejecute la preparación (`--prepare`), EL SISTEMA cargará todos los archivos `.txt`, `.md`, `.pdf` y `.csv` de `data/`, incluidos los de subcarpetas.
- RF-2: SI un archivo de `data/` tiene una extensión no soportada, ENTONCES EL SISTEMA lo omitirá y lo indicará por consola.
- RF-3: CUANDO se cargue el CSV de la agenda, EL SISTEMA convertirá cada fila en un texto legible con evento, descripción, actividad, lugar, distrito, fecha, hora y si es gratuita.
- RF-4: SI una fila del CSV no tiene título, ENTONCES EL SISTEMA la descartará.
- RF-5: EL SISTEMA normalizará el texto (saltos de línea y espacios) y descartará los documentos que queden vacíos.
- RF-6: EL SISTEMA fragmentará los documentos con tamaño y solapamiento configurables y añadirá a cada fragmento su posición y su tamaño.
- RF-7: EL SISTEMA guardará los fragmentos y las estadísticas de la ingesta en un archivo de salida.

### Embeddings e índice (offline)
- RF-8: CUANDO se ejecute la preparación, EL SISTEMA generará embeddings solo para los primeros N fragmentos, siendo N un límite configurable (todos si no hay límite).
- RF-9: CUANDO se ejecute la indexación (`--index`), EL SISTEMA guardará los fragmentos, sus embeddings y sus metadatos (incluido el archivo de origen) en una colección persistente con distancia coseno.
- RF-10: CUANDO se indique `--recreate-index`, EL SISTEMA borrará la colección antes de indexar.

### Recuperación (online)
- RF-11: CUANDO llegue una pregunta, EL SISTEMA recuperará los K fragmentos más cercanos (K configurable, o el indicado en la llamada), cada uno con su distancia y sus metadatos.
- RF-12: SI la colección está vacía, ENTONCES EL SISTEMA abortará con un mensaje que indica ejecutar `--index`.
- RF-13: EL SISTEMA presentará el contexto como un bloque por fragmento con su número, su distancia y su archivo de origen.

### Generación (online)
- RF-14: SI la pregunta está vacía, supera 2000 caracteres o contiene un patrón sospechoso de inyección, ENTONCES EL SISTEMA la rechazará con un mensaje de error sin recuperar ni llamar al LLM.
- RF-15: SI no se recupera ningún fragmento, ENTONCES EL SISTEMA devolverá un error sin llamar al LLM.
- RF-16: EL SISTEMA construirá el prompt con tres bloques delimitados: instrucciones (responder solo con el contexto, reconocer si falta información, citar la fuente y no inventar), contexto recuperado y pregunta.
- RF-17: CUANDO la pregunta sea válida y haya contexto, EL SISTEMA devolverá un resultado con la respuesta, el contexto, los fragmentos, las fuentes (archivos sin repetir, en orden de aparición) y un error vacío.

### Interfaces
- RF-18: CUANDO se ejecute `--ask`, EL SISTEMA mostrará la respuesta y sus fuentes, o el error si lo hay.
- RF-19: CUANDO se ejecute `--query`, EL SISTEMA mostrará solo el contexto recuperado, sin generar respuesta.
- RF-20: CUANDO la persona escriba en el chat web, EL SISTEMA mostrará la respuesta con efecto de escritura, las fuentes y un desplegable con el contexto recuperado.
- RF-21: EL SISTEMA tratará cada mensaje del chat web de forma independiente, sin memoria de la conversación.
- RF-22: EL SISTEMA permitirá elegir K entre 1 y 5 desde la barra lateral del chat web.
- RF-23: CUANDO se ejecute `--eval`, EL SISTEMA recorrerá las preguntas de evaluación con cada K candidato y mostrará la fuente y la distancia del mejor fragmento.

## Requisitos no funcionales
- Python 3.9+. Embeddings y generación con Gemini; clave en `.env`.
- Mensajes a la persona usuaria en español.

## Fuera de alcance (del sistema actual)
Memoria de conversación, filtros por metadatos (distrito, gratuidad, fechas), reranking, búsqueda híbrida y despliegue.

## Trazabilidad
| RF | Implementado en | Test |
|---|---|---|
| RF-1, RF-2 | `src/load.py` · `cargar_documentos`, `cargar_archivo` | sin test |
| RF-3 | `src/load.py` · `fila_a_texto` | `tests/test_ingesta.py::test_fila_csv_se_convierte_en_texto_legible`, `::test_fila_de_pago_indica_gratuito_no` |
| RF-4 | `src/load.py` · `fila_a_texto` | `tests/test_ingesta.py::test_fila_sin_titulo_se_descarta` |
| RF-5 | `src/clean.py` | `tests/test_ingesta.py::test_normalizar_texto_colapsa_saltos_y_espacios`, `::test_limpieza_descarta_documentos_vacios` |
| RF-6 | `src/chunk.py` · `fragmentar_documentos` | `tests/test_ingesta.py::test_fragmentos_llevan_indice_y_tamano` |
| RF-7 | `src/pipeline.py` · `guardar_chunks_json` | sin test |
| RF-8 | `src/embed.py` · `ejecutar_embeddings` (`MAX_CHUNKS_EMBED`) | sin test (usa API) |
| RF-9, RF-10 | `src/index.py` · `ejecutar_indexacion`, `borrar_coleccion` | sin test |
| RF-11, RF-12 | `src/retriever.py` · `recuperar` | sin test (usa API) |
| RF-13 | `src/context.py` · `formatear_contexto` | `tests/test_prompt_y_contexto.py::test_contexto_incluye_numero_distancia_y_fuente`, `::test_contexto_vacio_tiene_marcador` |
| RF-14 | `src/validators.py` · `validar_pregunta` + `src/logic.py` | `tests/test_prompt_y_contexto.py::test_validar_pregunta_rechaza_vacia_larga_y_sospechosa`, `tests/test_logic.py::test_pregunta_invalida_no_recupera_ni_llama_al_llm` |
| RF-15 | `src/validators.py` · `validar_contexto` + `src/logic.py` | `tests/test_logic.py::test_sin_contexto_no_llama_al_llm` |
| RF-16 | `src/prompts.py` · `build_rag_prompt` | `tests/test_prompt_y_contexto.py::test_prompt_tiene_tres_bloques_delimitados` |
| RF-17 | `src/logic.py` · `responder` | `tests/test_logic.py::test_pregunta_valida_devuelve_contrato_completo` |
| RF-18, RF-19, RF-23 | `main.py` | manual |
| RF-20, RF-21, RF-22 | `app.py` | manual |

## Huecos detectados
Salen de leer el código con la constitución delante. Son candidatos a specs nuevas.

1. **La abstención depende solo del LLM.** Aunque los fragmentos no tengan nada que ver con la pregunta ("¿Cuál es la capital de Francia?"), el sistema siempre llama al modelo y confía en que obedezca la instrucción de no inventar. Gasta una llamada, añade latencia y no es determinista. → **Spec 001.**
2. **Errores sin capturar.** El README promete un mensaje amigable si no hay índice, pero `responder()` no captura las excepciones del retriever ni de la API: la CLI y la web muestran la traza de Python.
3. **Índice parcial sin avisar.** Con `MAX_CHUNKS_EMBED = 20` solo se indexan los 20 primeros fragmentos en orden alfabético de archivo: 13 del PDF y 7 del CSV. La FAQ y la guía no llegan al índice, así que preguntas como "¿Qué significa el campo GRATUITO?" dependen de lo que diga el PDF.
4. **`data/README.md` entra en el corpus.** Se indexa como un documento más.
5. **La evaluación no puntúa.** `--eval` imprime la mejor fuente y su distancia, pero no la compara con `fuente_esperada` ni calcula un acierto.
6. **Validación de inyección mínima.** Solo cuatro patrones literales; cualquier variación los esquiva.
