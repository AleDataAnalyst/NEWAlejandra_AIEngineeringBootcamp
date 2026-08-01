# Escaleta — Proveedores de IA (Sprint 07, 16/07)

Uso interno, solo profe. Duración total ~60 min. Intercalado guía ↔ notebook.

| # | Duración | Bloque | Archivo / sección | Notas |
|---|----------|--------|--------------------|-------|
| 0 | — (antes de empezar) | Setup | — | Recordar por Slack: traer API key de Cohere. Tú lanza la descarga del modelo local (`EJECUTAR_LOCAL=True`) en tu propio notebook nada más entrar, para tenerlo listo cuando llegues al bloque 3 y no perder los 1-2 min de descarga en directo. |
| 1 | 5 min | Panorama | HTML → `#panorama` | Diagrama app→API→LLM + tabla de tipos de proveedor. Rápido, es solo para situar. |
| 2 | ~18 min | Cohere — concepto | HTML → `#cohere` | Roles system/user/assistant, slider de `temperature` (interactivo, déjales tocarlo 1 min). Como ya conocen Gemini, no te detengas mucho aquí. |
|   | | Cohere — práctica | Notebook: Instalación → Configura clave → Ejemplo 1, 2, 3 → 🧪 Ahora tú | Aquí es donde pueden atascarse por la API key — ten a mano el paso a paso de `dashboard.cohere.com` de la guía por si alguien no la trajo. |
| 3 | ~10 min | Tour Hugging Face | HTML → `#hf-tour` | Analogía del aeropuerto, glosario en acordeón. Deja que cada uno complete la misión de exploración (checklist) individualmente, tú circula por el chat/breakout resolviendo dudas. |
|   | | Autocomprobación | Notebook: Bloque 2 (sin código) | Las 3 preguntas del notebook — puedes lanzarlas en voz alta como check rápido antes de seguir. |
| 4 | ~18 min | HF local — concepto | HTML → `#hf-local` | Tabla nube vs. local, analogía de cuantización (comprimir una foto). |
|   | | HF local — práctica | Notebook: Instalación → Caché → Cargar modelo → Ejemplo 1, 2 → 🧪 Ahora tú | Punto crítico de tiempo: la descarga (~1GB). Como ya la lanzaste al principio, aquí solo tienen que ejecutar. Si alguien no la lanzó a tiempo, que siga en modo lectura (`EJECUTAR_LOCAL=False`) y lo pruebe después de clase. |
| 5 | ~5-8 min | Cierre | HTML → `#comparativa` y `#decide` | Tabla comparativa + botones del "ayudante de decisión" — bien para cerrar con algo interactivo y dejar sensación de repaso. |
| 🎁 | si sobra | Bonus | Notebook: streaming Cohere / HF nube | Solo si vais sobrados de tiempo. Si no, mencionar que está ahí para que lo prueben por su cuenta. |

## Riesgos a vigilar

- **Sin API key de Cohere:** pueden sacarla en 2 min desde el móvil mientras el resto avanza (no bloquea al grupo).
- **Descarga del modelo local lenta/con problemas de red:** por eso se lanza al principio de la clase, no en el bloque 3.
- **`scan_cache_dir()` en máquina nueva:** ya está arreglado en el notebook (mensaje amigable en vez de error), no debería generar dudas.
