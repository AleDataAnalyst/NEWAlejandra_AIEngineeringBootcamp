![Cabecera](../../assets/cabecera_gemini.png)

# Latencia, coste y precisión

Tres números (y una valoración cualitativa) dominan la mayoría de decisiones de modelo en APIs.

---

## 1. Precisión / calidad

**Qué es:** qué tan bien responde el modelo **en tu tarea**, no en un examen genérico.

**Cómo medirlo:**

- Mismas preguntas para todos los modelos.
- Rubric simple: 1–5 en claridad, corrección, tono, formato.
- Tests automáticos cuando la salida es estructurada (JSON válido, etiqueta en whitelist).

**Cuidado:** una respuesta más larga no es necesariamente mejor.

---

## 2. Latencia

**Qué es:** tiempo desde que envías la petición hasta que recibes la respuesta útil.

| Métrica | Significado |
|---------|-------------|
| **Tiempo total** | Lo que percibe el usuario en chat |
| **TTFT** (time to first token) | Importante en streaming |
| **p95** | El 5 % peor de peticiones — crítico en SLAs |

**Factores:** tamaño del modelo, longitud del prompt, región, carga del proveedor, streaming vs no streaming.

```python
import time

t0 = time.time()
response = client.models.generate_content(model=MODEL, contents=prompt)
elapsed_ms = int((time.time() - t0) * 1000)
```

En la demo compararás `elapsed_ms` entre modelos con el **mismo prompt**.

---

## 3. Coste computacional (vía tokens)

En APIs comerciales el coste suele derivarse de **tokens**:

| Concepto | Impacto |
|----------|---------|
| Tokens de **input** | Contexto largo, RAG mal filtrado |
| Tokens de **output** | Respuestas verbosas, `max_output_tokens` alto |
| Llamadas por sesión | Chat con historial completo cada turno |

```python
um = response.usage_metadata
prompt_tokens = um.prompt_token_count
output_tokens = um.candidates_token_count
total_tokens = um.total_token_count
```

**Coste aproximado** = tokens × precio por millón (consulta la tarifa actual del proveedor).

---

## 4. Tabla de trade-offs (orientativa)

| Prioridad producto | Suele ganar | Suele perder |
|--------------------|-------------|--------------|
| Chat en tiempo real | Modelo flash, prompt corto | Matices en tareas muy difíciles |
| Análisis profundo offline | Tier pro, más contexto | Latencia y factura |
| Alto volumen batch | Modelo barato + pipeline | Último % de calidad |
| Salida JSON estricta | Temperatura baja + validación | Creatividad |

---

## 5. Misma pregunta, distintos modelos

Patrón de evaluación justa:

```text
PREGUNTAS_FIJAS = [q1, q2, q3, q4, q5]
MODELOS = [flash, otro_tier, ...]

para cada q en PREGUNTAS_FIJAS:
    para cada m en MODELOS:
        medir(latencia, tokens, respuesta)
        anotar calidad (humano o rubric)
```

**Misma temperatura** y mismos límites salvo que quieras estudiar explícitamente ese hiperparámetro.

---

## 6. Plantilla de matriz (para el notebook)

| Pregunta | Modelo | ms | in | out | Calidad 1-5 | Notas |
|----------|--------|-----|-----|-----|-------------|-------|
| q1 | gemini-3-flash-preview | | | | | |
| q1 | gemini-2.5-pro | | | | | |

Copia esta tabla en tu cuaderno o en un documento de decisión.
