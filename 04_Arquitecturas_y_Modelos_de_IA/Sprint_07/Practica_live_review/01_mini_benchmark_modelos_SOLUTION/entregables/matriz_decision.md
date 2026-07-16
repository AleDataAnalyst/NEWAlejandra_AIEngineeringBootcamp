# Matriz de decisión — mini-benchmark (ejecución 2026-07-07)

Benchmark: `output/benchmark_20260707_114645.csv` · Temperatura 0.3 · Modelos: `gemini-2.5-flash`, `gemini-3.1-flash-lite`

| Pregunta (id) | Modelo ganador | Por qué (latencia + calidad) | Calidad 1–5 |
|---------------|----------------|------------------------------|-------------|
| soporte_bootcamp | gemini-3.1-flash-lite | Tono cercano y menciona la plataforma; además es ~25 % más rápido (1548 ms vs 2066 ms) | 4 |
| clasificar_consulta | gemini-2.5-flash | Ambos aciertan `TÉCNICO`, pero 2.5-flash tarda la mitad (4077 ms vs 8132 ms) con la misma salida de una palabra | 5 |
| resumen_sprint | gemini-3.1-flash-lite | Tres viñetas completas en ambos; lite es ~4× más rápido (983 ms vs 3951 ms) y el contenido es igual de preciso | 5 |
| json_perfil | gemini-3.1-flash-lite | JSON válido sin markdown en ambos; lite responde en 548 ms frente a 2916 ms (~5× más ágil) | 5 |
| limite_futbol | gemini-3.1-flash-lite | Rechaza el dominio en una sola frase, como pide el prompt; latencia ligeramente menor (1185 ms vs 1296 ms) | 5 |

**Conclusión en una frase:** `gemini-3.1-flash-lite` gana en 4 de 5 tareas (soporte, resumen, JSON y caso límite) con mejor o igual calidad y menor latencia; solo en clasificación cerrada `gemini-2.5-flash` fue claramente más rápido con el mismo acierto.
