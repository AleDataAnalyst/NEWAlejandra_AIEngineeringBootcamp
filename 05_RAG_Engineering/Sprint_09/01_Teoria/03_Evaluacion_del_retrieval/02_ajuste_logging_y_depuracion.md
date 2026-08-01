![Cabecera](../../assets/cabecera_rag.png)

# Ajuste de chunking y top-K, logging y depuración

## Objetivos

- Saber **cuándo reindexar** tras cambiar chunking.
- Barrer valores de **K** con método.
- Registrar trazas útiles para depurar retrieval.

Veremos cómo ajustar el chunking y el top-K, cómo registrar trazas útiles para depurar el retrieval y cómo depurar el retrieval.

Cuando se cambia el chunking o el top-K, se debe reindexar el índice para que los cambios tengan efecto. Si no lo hacemos, los cambios no tendrán efecto y el retrieval seguirá usando el índice anterior. El resultado de esto sería que el retrieval no funcionaría correctamente y el LLM no podría entender el contexto y responder la pregunta.

---

## 1) Ajustar chunking 

Ejemplo de parámetros lo puedes encontrar en los proyectos de prueba en `config.py`:

```python
CHUNK_SIZE = 800
CHUNK_OVERLAP = 100
```

| Cambio | Efecto en retrieval |
|--------|---------------------|
| ↑ `CHUNK_SIZE` | Más contexto por chunk; menos fragmentos; riesgo de ruido |
| ↓ `CHUNK_SIZE` | Fragmentos más precisos; riesgo de cortar ideas |
| ↑ `CHUNK_OVERLAP` | Mejor continuidad entre chunks vecinos |

**Flujo de reexperimentación:**

Se muestra un ejemplo de flujo de reexperimentación para ajustar el chunking en tu propio proyecto. Normalmente se harán varias pruebas con diferentes valores de chunking y se elegirá el valor que mejor funcione. 

Puedes ver comandos típicos para reindexar el índice y evaluar el retrieval en tu propio proyecto que podrías ejecutar por consola.

```text
  Cambiar CHUNK_SIZE / OVERLAP en config.py
       │
       ▼
  python main.py --prepare      # regenera chunks + embeddings
       │
       ▼
  python main.py --index --recreate-index  # reindexa el índice
       │
       ▼
  python main.py --eval  # evalúa el retrieval
``` 

Cambiar solo `TOP_K` **no** requiere `--prepare` ni `--index`.

---

## 2) Barrido de top-K

Prueba la misma pregunta con K = 1, 3, 5, 10:

Se podría ejecutar por consola de la siguiente manera:

```bash
python main.py --query "¿Hay cine gratuito?" --top-k 1
python main.py --query "¿Hay cine gratuito?" --top-k 5
```

O podrías usar tu propio script de evaluación con `eval_retrieval.py` con lista `TOP_K_CANDIDATES = [1, 3, 5]` en config.

Preguntas que deberíamos hacernos para elegir el valor de K:

- ¿Aparece el chunk útil solo con K alto?
- ¿A partir de qué K entra mucho ruido?

Documenta el K elegido para S10 en una nota o en tu informe de sprint.

---

## 3) Logging básico

Ejemplo de lo que el proyecto podría imprimir en consola:

```text
[RETRIEVAL] query="¿Hay cine gratuito?"
[RETRIEVAL] top_k=3 collection=agenda_cultural_madrid
[RETRIEVAL] #1 id=chunk_42 distance=0.18 source=...csv
```

Buenas prácticas de logging en retrieval:

| Campo | Por qué |
|-------|---------|
| Pregunta exacta | Reproducir el caso para depurar |
| K y colección | Config activa para el retrieval |
| id + distance + source | Auditar cada chunk recuperado |
| Tiempo de embed + query | Detectar latencia de recuperación de chunks |

En producción guardarías esto en JSON o un sistema de trazas. Como mínimo deberías tener un sistema de logging en **consola estructurada**.

---

## 4) Estrategias de depuración

Se muestra un ejemplo de estrategias de depuración para depurar el retrieval. Normalmente se harán varias pruebas con diferentes valores de chunking y se elegirá el valor que mejor funcione.

```text
  ¿El resultado es malo?
        │
        ├─► ¿Existe la info en chunks.json? ──No──► ingesta / datos (añadir más datos al corpus)
        │         │
        │        Sí
        │         ▼
        ├─► ¿Está en embeddings.json / Chroma? ──No──► prepare + index (reindexar el índice)
        │         │
        │        Sí
        │         ▼
        ├─► ¿Subir K mejora? ──Sí──► K bajo (reducir el número de chunks recuperados)
        │         │
        │        No
        │         ▼
        └─► ¿Cambiar chunk_size mejora? ──Sí──► chunking (reducir el tamaño de los chunks)
                  │
                 No
                  ▼
             pregunta ambigua o fuera de corpus (pregunta que no se puede responder con el contexto disponible)
```

Lo importante es que **No pases al LLM** hasta agotar esta checklist. Si no se puede responder la pregunta con el contexto disponible, se debe cambiar el chunking o el top-K.

---

## 5) Script de evaluación del retrieval (`eval_retrieval.py`)

Dentro de tu proyecto podrías tener un script de evaluación (`preguntas_eval.json`) que ejecute todas las preguntas de `preguntas_eval.json` y opcionalmente varios valores de K.

Ejemplo de ejecución de script de evaluación de tu propio proyecto:

```bash
python main.py --eval
```

o bien:

```bash
python eval_retrieval.py
```

Salida: tabla resumen por pregunta con el mejor chunk, su fuente y distancia.

---

## Resumen

- Chunking → requiere regenerar embeddings e índice.
- Top-K → ajuste rápido; compara con barrido sistemático.
- Logging y checklist de depuración evitan culpar al modelo generativo demasiado pronto.
