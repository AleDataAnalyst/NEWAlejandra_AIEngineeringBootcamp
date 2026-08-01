# Reflexión — Retrieval calidad del aire (Live Review Sprint 09)

Ejemplo de entregable rellenado (SOLUTION). Los números concretos dependen de `MAX_CHUNKS_EMBED` y del corpus.

## 1. Setup del índice

- Chunks embeddeados (`MAX_CHUNKS_EMBED`): 50
- Vectores en Chroma tras `--index`: 50
- `COLLECTION_NAME`: calidad_aire_madrid

## 2. Resultados de `--eval` (ejemplo ilustrativo)

| Pregunta | Fuente esperada (orientativa) | Mejor fuente K=1 | Distancia K=1 | Mejor fuente K=3 | Distancia K=3 |
|----------|-------------------------------|------------------|---------------|------------------|---------------|
| q1 magnitud 83 | FAQ | faq_calidad_aire.md | ~0.35 | faq_calidad_aire.md | ~0.35 |
| q2 validación V | FAQ | faq_calidad_aire.md | ~0.32 | faq_calidad_aire.md | ~0.32 |
| q4 temperatura estación | CSV | …csv | ~0.40 | …csv | ~0.40 |
| q6 capital de Francia | (ninguna) | (irrelevante) | alta / similar | (ruido) | alta |

*(Sustituye por tus distancias reales al revisar en clase.)*

## 3. Análisis

1. **FAQ vs CSV:** Las preguntas conceptuales (magnitud, validación V, columnas hXX) suelen recuperar `faq_calidad_aire.md` o la guía. Las preguntas tipo “temperatura en una estación” acercan chunks con `tipo=meteo_medicion` del CSV.
2. **Efecto de K:** K=1 basta para q1 si el FAQ está bien indexado. K=3 aporta contexto útil; K=5 a veces mete mediciones poco relacionadas. Por defecto K=3 es un buen compromiso.
3. **Distance:** En q1 el hit #1 suele destacar. En q6 las distancias son peores o muy parecidas entre sí: señal de que no hay evidencia en el corpus.
4. **Puente Sprint 10:** Falta el LLM: ensamblar prompt (instrucciones + contexto + pregunta) y generar la respuesta citando fuentes.
