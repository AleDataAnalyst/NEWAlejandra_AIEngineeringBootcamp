![Cabecera](../../assets/cabecera_rag.png)

# Comparación de resultados y decisión del retrieval

## Objetivos

- Documentar una **comparación estructurada** entre configuraciones.
- Elegir parámetros de retrieval antes de enganchar un LLM.

---

## 1) Tabla comparativa (plantilla)

Se muestra una tabla comparativa de las configuraciones de retrieval que se han probado. Normalmente se harán varias pruebas con diferentes valores de chunking y se elegirá el valor que mejor funcione. Esta tabla se debe rellenar tras ejecutar `--eval` con cada configuración. Una fila por pregunta y experimento. La rellenarías con la información de la tabla de resultados de la evaluación del retrieval.

Esta tabla es importante para documentar las configuraciones de retrieval que se han probado y elegir la mejor configuración antes de enganchar un LLM.

| Config | CHUNK_SIZE | TOP_K | Pregunta | ¿Relevante #1? | Mejor fuente | Notas |
|--------|------------|-------|----------|----------------|--------------|-------|
| experimento_1 | 800 | 3 | ¿GRATUITO? | Sí | FAQ | OK |
| experimento_2 | 800 | 3 | cine gratis | Parcial | CSV | Subir K a 5 |
| experimento_3 | 400 | 3 | cine gratis | Sí | CSV | Más chunks, reindexar |

Los nombres `experimento_1`, `experimento_2`, `experimento_3`, etc. son nombres que tú le pones a cada experimento. Normalmente se harán varias pruebas con diferentes valores de chunking y se elegirá el valor que mejor funcione.

Rellena tras ejecutar `--eval` con cada configuración. Una fila por pregunta y experimento.

---

## 2) Criterios de decisión

Se muestra una tabla de criterios de decisión para elegir la mejor configuración de retrieval. Normalmente se harán varias pruebas con diferentes valores de chunking y se elegirá el valor que mejor funcione.

El peso es un valor que tú le pones a cada criterio. Normalmente se harán varias pruebas con diferentes valores de chunking y se elegirá el valor que mejor funcione.

| Criterio | Peso |
|----------|------------------|
| Chunk #1 relevante en preguntas frecuentes | Alto |
| Información presente en top-K (aunque no sea #1) | Alto |
| Poco ruido (chunks off-topic) | Medio |
| Latencia embed + query aceptable | Medio |
| Tamaño del prompt resultante | Medio |

No busques perfección: busca **entender el trade-off** antes de enganchar un LLM. El objetivo es que el contexto recuperado sea lo suficientemente bueno para que el LLM pueda responder la pregunta.

---

## 3) Entregable del sprint

Al cerrar el Sprint 9 deberíamos comprender sistemas que ejecuten el siguiente flujo:

```text
PDF / CSV / MD  →  chunks  →  embeddings  →  ChromaDB
                                                    │
Pregunta del usuario ───────────────────────────────┘
                    similarity search → top-K → contexto
```

Todo ello **sin** respuesta generada por un LLM todavía. El objetivo es que el contexto recuperado sea lo suficientemente bueno para que el LLM pueda responder la pregunta.

Ejemplos de comandos que podrías ejecutar por consola en tu propio proyecto:

```bash
python main.py --prepare --index
python main.py --query "¿Qué actividades hay en El Retiro?"
python main.py --eval
```

---

## 4) Conclusiones que deberíamos poder explicar llegado a este punto

- Por qué existe una BD vectorial y qué hace Chroma en tu pipeline.
- Cómo una pregunta se convierte en vector y en top-K chunks.
- Qué efecto tiene K y el chunking en los resultados.
- Cómo depurar retrieval sin invocar al LLM.
- Por qué un RAG no es «documento → LangChain → respuesta», sino capas separadas.

---

## Resumen

- Compara configuraciones con tabla y preguntas fijas.
- Documenta K y chunking elegidos.
- El producto que se podría desarrollar hasta este punto es un motor de búsqueda semántica completo y auditable.
