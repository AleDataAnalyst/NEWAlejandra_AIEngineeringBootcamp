# Práctica live review — Sprint 12

## Enunciado (45–60 min)

Partiendo del proyecto `01_proyecto_agente_tools_tarde_cultural/`:

1. Lanza un turno que obligue a **al menos dos tools** (p. ej. guía + eventos o hora + guía).
2. En la traza, identifica `tool`, `args`, `status`, `preview`.
3. Fuerza o simula el **fallback** de la API (timeout / Wi‑Fi off) y comprueba `Fuente: fallback`.
4. Explica en 3 frases: allowlist, `max_steps`, por qué `done` no es una tool.

## Checklist de revisión

- [ ] No hay tool fuera del registro
- [ ] El RAG no inventa párrafos ajenos a la guía
- [ ] La API no vuelca el JSON completo al modelo
- [ ] Streamlit muestra estado + traza
- [ ] Errores no tumban la app sin mensaje

## Entregable sugerido

Captura o pegado de un `traza` de un turno + párrafo de reflexión (qué controlaríaís en producción).
