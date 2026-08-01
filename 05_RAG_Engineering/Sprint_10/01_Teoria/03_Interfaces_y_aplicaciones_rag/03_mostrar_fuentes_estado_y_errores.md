![Cabecera](../../assets/cabecera_rag.png)

# Resultado, estado y errores en la UI

## Objetivos

- Separar qué ve el usuario (resultado) de qué queda en debug.
- Usar **spinner** y mensajes de error claros.
- En el caso RAG del sprint: mostrar **fuentes** y, opcionalmente, el contexto recuperado.

---

## 1) Qué debe ver el usuario (idea general)

Al exponer cualquier sistema, conviene distinguir:

| Capa | Ejemplos | ¿Visible siempre? |
|------|----------|-------------------|
| Resultado principal | Respuesta, predicción, informe | Sí |
| Metadatos de confianza / trazabilidad | Fuentes, score, versión del modelo | Recomendado si aporta confianza |
| Debug | Prompt interno, contexto crudo, IDs | Opcional / expander |
| Error | Mensaje accionable | Solo si falla |

### Caso del sprint (RAG)

| Elemento | ¿Visible siempre? | Motivo |
|----------|-------------------|--------|
| Respuesta | Sí | Objetivo de la app |
| Fuentes | Sí (recomendado) | Confianza y trazabilidad |
| Contexto completo | Opcional / debug | Útil para depurar, ruidoso para demos |
| Distances / IDs | Solo debug | Demasiado técnico |

En `app.py` del proyecto (dentro del mensaje del asistente en el chat):

```python
if resultado.get("fuentes"):
    st.markdown("**Fuentes**")
    for fuente in resultado["fuentes"]:
        st.write(f"- `{fuente}`")

with st.expander("Contexto recuperado (debug)"):
    st.text(resultado.get("contexto", ""))
```

El expander **cerrado por defecto** evita abrumar en una demo, pero permite enseñar el retrieval en vivo.

---

## 2) Estados de carga

Las llamadas a modelos o APIs tardan segundos. Sin feedback, parece que la app se ha colgado. En el chat del proyecto se usa `st.status` mientras corre `responder()`, y luego streaming del texto:

```python
with st.status("Consultando el corpus…"):
    resultado = responder(pregunta, top_k=top_k)

escrito = st.write_stream(stream_palabras(resultado["respuesta"]))
```

Mensajes claros > indicadores sin texto.

---

## 3) Errores habituales

| Situación | Qué mostrar |
|-----------|-------------|
| Falta `GEMINI_API_KEY` | Mensaje de configuración (`.env`) |
| Índice Chroma vacío | «Ejecuta `python main.py --prepare --index`» |
| Pregunta vacía | Validación en UI o en `validators.py` |
| Error de `validators` | `st.error(resultado["error"])` |
| Timeout / error de API | Mensaje amigable + reintentar |

```python
if resultado.get("error"):
    st.error(resultado["error"])
else:
    st.markdown(resultado["respuesta"])
```

No muestres stack traces crudos al usuario final; en desarrollo, sí puedes loguearlos en consola.

---

## 4) Buenas prácticas UX (mínimas)

- Una petición → un resultado claro.
- Trazabilidad (fuentes, etc.) debajo del resultado, no escondida.
- Evitar pedirle al usuario que «mire la terminal».
- Si el sistema se abstiene, el mensaje debe leerse como **respuesta válida**, no como crash.

---

## Resumen

- Resultado + trazabilidad = mínimo viable útil; debug en expander.
- Spinner y errores claros = app usable.
- En RAG: fuentes visibles; contexto recuperado como puente pedagógico con S9.