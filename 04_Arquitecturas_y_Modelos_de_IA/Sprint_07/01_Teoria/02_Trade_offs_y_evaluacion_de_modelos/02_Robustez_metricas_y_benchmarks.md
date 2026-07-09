![Cabecera](../../assets/cabecera_gemini.png)

# Robustez, métricas y benchmarks

“Robusto” aquí significa: **comportamiento estable** ante variación de inputs y condiciones — no solo una respuesta bonita en el demo.

---

## 1. Robustez en apps con LLM

| Aspecto | Pregunta |
|---------|----------|
| **Formato** | ¿Devuelve JSON válido cuando lo pides? |
| **Dominio** | ¿Se sale del tema con preguntas límite? |
| **Consistencia** | ¿Misma pregunta → misma categoría (con temp baja)? |
| **Errores** | ¿Qué pasa con input vacío, muy largo o ambiguo? |

La robustez del **sistema** (validación, reintentos, fallbacks) complementa la del modelo — ya trabajaste capas en Sprint 6.

---

## 2. Métricas útiles para cada tarea

| Tarea | Métricas |
|-------|----------|
| Clasificación | Accuracy, F1 por clase, tasa de “OTRO” |
| QA con contexto | % respuestas con cita correcta, alucinaciones |
| Generación libre | Rubric humana, checklist |
| Código | Tests que pasan, lint |
| Chat | CSAT, escalado a humano, longitud media |

En nuestro caso, empezamos con **rúbrica 1–5** + **latencia** + **tokens**.

---

## 3. Benchmarks públicos (MMLU, HumanEval, etc.)

Los leaderboards miden tareas **estandarizadas**. Sirven para:

- Orientación grosso modo (tier pro vs flash).
- Detectar modelos obsoletos.

**No sirven** para sustituir evaluación en tu dominio:

- Tu FAQ no está en MMLU.
- Tu política de tono no está en el benchmark.
- Tu mezcla input/output de tokens es distinta.

> Usa benchmarks como **contexto**, no como veredicto final.

---

## 4. Diseño de un mini-benchmark propio

1. **Elige 5–20 preguntas** representativas (no solo las fáciles).
2. Incluye **casos límite** (vacío, jerga, intento de injection).
3. **Congela** prompt plantilla y temperatura.
4. Ejecuta todos los modelos candidatos.
5. Registra métricas automáticas + revisión humana en muestra.
6. **Documenta** la decisión (aunque sea “nos quedamos con flash por p95 < 2s”).

---

## 5. Errores al evaluar

| Error | Corrección |
|-------|------------|
| Cambiar el prompt entre modelos | Un solo template |
| Una sola pregunta “wow” | Conjunto fijo |
| Ignorar coste en producción | Proyectar tokens × volumen |
| Evaluar solo una vez | Repetir en otro día / región si es crítico |
