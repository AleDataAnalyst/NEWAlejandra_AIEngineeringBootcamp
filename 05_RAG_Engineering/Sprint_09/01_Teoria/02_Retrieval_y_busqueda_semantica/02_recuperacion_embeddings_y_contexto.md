![Cabecera](../../assets/cabecera_rag.png)

# Recuperación basada en embeddings y construcción del contexto

## Objetivos

- Embeddear la **pregunta del usuario** con el mismo modelo que el índice.
- Mapear la respuesta de Chroma a una estructura usable en Python.
- **Formatear el contexto** recuperado con fuentes y delimitadores.

---

## 1) Mismo modelo, mismo espacio vectorial

Regla de oro del RAG:

> El vector de la pregunta debe salir del **mismo** `EMBEDDING_MODEL` que los vectores indexados.

Por ejemplo, si indexaste con `gemini-embedding-2` y consultas con otro modelo (ya sea en la nube o local), las distancias **no tienen sentido**.

Es decir, se debe usar el mismo modelo de embedding que se usó para indexar los chunks. Esto es importante para que las distancias tengan sentido.


---

## 2) De `query()` a objetos Python

Chroma devuelve listas anidadas (una consulta → varios resultados):

```python
{
  "ids": [["chunk_12", "chunk_3", ...]],
  "documents": [["texto...", "texto...", ...]],
  "metadatas": [[{...}, {...}, ...]],
  "distances": [[0.21, 0.34, ...]],
}
```

`retriever.py` las **aplana** a una lista de diccionarios:

```python
[
  {
    "id": "chunk_12",
    "text": "...",
    "metadata": {"source": "data/faq...", "chunk_index": 12},
    "distance": 0.21,
  },
  ...
]
```

Así el resto del pipeline no depende del formato interno de Chroma.

---

## 3) Construcción del contexto recuperado

El LLM (que trabajaremos en el Sprint 10) no recibe chunks sueltos: recibe un **bloque de contexto** estructurado en lenguaje natural. En Sprint 9 lo imprimes para **evaluar** si el retrieval es bueno. Esto es importante para que el LLM pueda entender el contexto y responder la pregunta.

Ejemplo con `context.py`:

```text
--- Fragmento 1 (distancia=0.21) ---
Fuente: faq_agenda_cultural.md
¿Todos los eventos son gratuitos?
No. Cada fila del CSV incluye el campo GRATUITO: 1 → gratuita, 0 → puede tener precio...

--- Fragmento 2 (distancia=0.34) ---
Fuente: 206974-4-agenda-eventos-culturales-100-csv.csv
Evento: Cine de verano en Hortaleza
Gratuito: sí
...
```

Buenas prácticas:

- **Delimitadores claros** (`---`) entre fragmentos.
- **Citar fuente** (`metadata.source`) para trazabilidad.
- **Incluir distance** en logs o en modo debug (no siempre en el prompt final).

---

## 4) Orden de los chunks

Chroma devuelve resultados **ordenados por relevancia** (distancia ascendente con coseno). Mantén ese orden al formatear: el fragmento más relevante primero.

En Sprint 10 podrás decidir si el prompt menciona «prioriza el fragmento 1» o si todos tienen el mismo peso. Esto es importante para que el LLM pueda entender el contexto y responder la pregunta. Si el contexto es muy largo, se puede priorizar el fragmento más relevante.

---

## 5) Inspección sin LLM

Comando del proyecto (tras completar los workouts o en paralelo):

```bash
python main.py --query "¿Qué actividades hay en El Retiro?"
```

En el Workout 2 verás el mismo flujo inline sobre `02_Workout/output/chroma_db/`.

Salida esperada:

1. Pregunta recibida
2. Top-K chunks con distancia y metadata
3. Bloque de contexto formateado

Si el contexto **ya responde** la pregunta con texto literal del corpus, el retrieval funciona. Si no, ajusta K o chunking (Bloque 3) antes de culpar al modelo generativo. Normalmente el problema es que el contexto no es suficiente o que el chunking no es suficiente y el modelo no puede entender la pregunta.

---

## Resumen

- Embed la consulta con el mismo modelo que el índice.
- Normaliza la salida de Chroma a una lista de chunks en Python.
- Formatea el contexto con fuentes y delimitadores para evaluar y, en S10, para el prompt.