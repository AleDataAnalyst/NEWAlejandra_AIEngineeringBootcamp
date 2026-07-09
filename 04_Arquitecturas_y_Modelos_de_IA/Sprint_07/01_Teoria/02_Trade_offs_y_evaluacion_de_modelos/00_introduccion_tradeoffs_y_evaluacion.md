![Cabecera](../../assets/cabecera_gemini.png)

# Introducción: trade-offs y evaluación de modelos

Ahora aprenderemos a **medir** criterios de calidad en lugar de confiar en impresiones.

> **Evaluar un modelo = mismo input, mismas condiciones, métricas comparables.**

**No elijas el modelo que brilla en un ejemplo; elige el que gana en tu matriz de evaluación con tus preguntas y tus límites de coste y latencia.**

---

## Objetivos de la unidad

Al terminar, deberías poder:

- Explicar trade-offs entre **calidad**, **latencia** y **coste**.
- Leer `usage_metadata` y tiempo de respuesta en llamadas Gemini.
- Diseñar un mini-benchmark con **3–5 preguntas fijas**.
- Interpretar benchmarks públicos con **cautela** (no sustituyen tu caso de uso).
- Rellenar una **matriz de evaluación** antes de elegir modelo en producción.

---

## Qué significa “evaluar” en producción

| En bootcamp / MVP | En producción |
|-------------------|---------------|
| 3–5 prompts manuales | Dataset de evaluación + regresiones |
| Latencia en tu portátil | p50 / p95 en tu región |
| Tokens de una llamada | Coste mensual agregado |
| “Me gusta más esta respuesta” | Rubric + revisión humana o tests automáticos |

El espíritu es el mismo: **decisiones con datos**, no con un chat suelto.

---

## Las tres dimensiones

```text
        Calidad / precisión
              ▲
              │
              │   ← sueles sacrificar una al empujar otra
              │
Coste ◄───────┼───────► Latencia
```

No existe el triángulo perfecto. Existe el **equilibrio aceptable** para tu producto.
