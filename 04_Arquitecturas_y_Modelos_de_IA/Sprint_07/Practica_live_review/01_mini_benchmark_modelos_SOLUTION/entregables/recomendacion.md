# Recomendación — mini-benchmark (ejecución 2026-07-07)

## Caso de uso elegido

Soporte y tutoría del bootcamp AI Engineering: respuestas cortas con tono empático, clasificación de consultas de alumnos, resúmenes de contenido y salidas JSON para perfiles de aprendizaje.

## Modelo recomendado para producción

`gemini-3.1-flash-lite` como modelo por defecto en los flujos interactivos del bootcamp (chat de soporte, resúmenes y generación de JSON).

## Trade-off principal

En la ejecución del benchmark, lite tuvo una latencia media de **2479 ms** frente a **2861 ms** de `gemini-2.5-flash` (~13 % más rápido de media), con ventajas muy marcadas en resumen (~4×) y JSON (~5×). La excepción es la clasificación en una palabra: ahí `gemini-2.5-flash` fue ~2× más rápido con el mismo resultado (`TÉCNICO`). A cambio de esa latencia puntual mayor en clasificación, lite ofrece mejor UX en la mayoría de tareas sin pérdida de calidad percibida.

## Riesgo o condición

Si el clasificador de consultas es un paso crítico en tiempo real (p. ej. enrutado automático con mucho volumen), valorar `gemini-2.5-flash` solo para esa tarea o re-ejecutar el benchmark con más ejemplos de clasificación. En salidas JSON, validar siempre con un parser en Python: en esta ejecución ambos modelos cumplieron el formato, pero no conviene confiar solo en el prompt.
