![Cabecera](../../assets/cabecera_gemini.png)

# Introducción: benchmarking con Python

Anteriormente vimos cómo comparar modelos de manera manual con un **criterio** y **comparación manual**. Aquí **automatizas** el pipeline:

```text
dataset (preguntas) → runs por modelo → log (CSV) → informe
```

---

## Objetivos

- Estructurar un evaluador mínimo con módulos (`config`, cliente, `benchmark`, `report`, `main`).
- Medir latencia y tokens de forma reproducible.
- Guardar resultados para comparar ejecuciones en el tiempo.
- Generar un informe Markdown legible para stakeholders técnicos.

---

## Convención para nuestro proyecto

```text
proyecto_evaluador/
├── config.py         # modelos, temperatura, rutas
├── gemini_auth.py    # .env + getpass
├── gemini_client.py  # llamada + métricas
├── benchmark.py      # bucle pregunta × modelo
├── report.py         # CSV + report.md
├── data/preguntas.json
└── main.py
```
