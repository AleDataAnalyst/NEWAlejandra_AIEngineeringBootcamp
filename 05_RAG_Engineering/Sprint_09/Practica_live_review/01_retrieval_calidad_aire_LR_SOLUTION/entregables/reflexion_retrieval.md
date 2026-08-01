# Reflexión — Retrieval calidad del aire (Live Review Sprint 09)

Completa **después** de `python main.py --eval`. Sustituye los `TODO` con datos reales de tu ejecución.

## 1. Setup del índice

- Chunks embeddeados (`MAX_CHUNKS_EMBED`): TODO
- Vectores en Chroma tras `--index`: TODO
- `COLLECTION_NAME`: TODO

## 2. Resultados de `--eval` (rellena con tu salida)

| Pregunta | Fuente esperada (orientativa) | Mejor fuente K=1 | Distancia K=1 | Mejor fuente K=3 | Distancia K=3 |
|----------|-------------------------------|------------------|---------------|------------------|---------------|
| q1 magnitud 83 | faq | TODO | TODO | TODO | TODO |
| q2 validación V | FAQ | TODO | TODO | TODO | TODO |
| q4 temperatura estación | CSV | TODO | TODO | TODO | TODO |
| q6 capital de Francia | (ninguna) | TODO | TODO | TODO | TODO |

## 3. Análisis

1. **FAQ vs CSV:** ¿Las preguntas conceptuales (q1–q3, q5) recuperan FAQ/guía/PDF y las de mediciones (q4) el CSV? Justifica con 1 ejemplo.
   - TODO

2. **Efecto de K:** ¿Con K=1 te quedas corto? ¿Con K=5 entra ruido? ¿Qué K usarías por defecto y por qué?
   - TODO

3. **Distance:** ¿El mejor hit destaca claramente sobre el 2.º? ¿En q6 las distancias son peores/más parecidas?
   - TODO

4. **Puente Sprint 10:** Con el contexto de una `--query` buena, ¿qué le faltaría aún al sistema para **responder** al usuario?
   - TODO
