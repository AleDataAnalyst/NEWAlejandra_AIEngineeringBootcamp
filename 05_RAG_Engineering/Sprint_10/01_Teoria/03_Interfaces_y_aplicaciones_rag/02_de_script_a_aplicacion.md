![Cabecera](../../assets/cabecera_rag.png)

# De script a aplicación

Ya sabes montar una UI con Streamlit. El siguiente paso es **enganchar tu lógica existente** sin reimplementarla dentro de `app.py`.

## Objetivos

- Definir un **contrato** de backend (función pública → resultado estructurado).
- Reutilizar esa función desde CLI, notebook y Streamlit.
- Evitar duplicar pipeline / modelo dentro de la UI.
- Preparar el proyecto del sprint para `streamlit run app.py`.

---

## 1) Contrato del backend (idea general)

Cualquier sistema expuesto debería tener una entrada clara, por ejemplo:

```python
def predict(x): ...
def run(payload: dict) -> dict: ...
def responder(pregunta: str) -> dict: ...
```

La interfaz **solo** llama a esa función y renderiza el resultado. Si mañana cambias Streamlit por Gradio o por una API, no tocas el núcleo.

---

## 2) Contrato en el proyecto de este sprint

En `src/logic.py`:

```python
def responder(pregunta: str, top_k: int | None = None) -> dict:
    """
    Returns:
        respuesta, contexto, chunks, fuentes, error
    """
```

| Clave | Uso en UI |
|-------|-----------|
| `respuesta` | Texto principal para el usuario |
| `fuentes` | Lista bajo la respuesta |
| `contexto` | Expander de depuración (opcional) |
| `error` | `st.error(...)` si no es `None` |
| `chunks` | Opcional (debug avanzado) |

---

## 3) Varios clientes, un backend

```text
                    logic.responder()
                           ▲
         ┌─────────────────┼─────────────────┐
         │                 │                 │
    main.py --ask     app.py (Streamlit)   (futura API)
    (consola)         (navegador)          POST /ask
```

CLI, Streamlit y una hipotética API son **clientes** del mismo contrato.

---

## 4) Anti-patrón

```python
# ❌ Dentro de app.py: volver a hacer query a Chroma + generate_content
# Duplicas lógica, olvidas validators, rompes el contrato único.
```

```python
# ✅
resultado = responder(pregunta)
```

La UI no debe conocer detalles internos (vector store, embedding, prompt) salvo que quieras un panel de debug avanzado.

---

## 5) Checklist antes de abrir Streamlit

1. Corpus en `data/`.
2. `python main.py --prepare --index` (índice listo).
3. `python main.py --ask "…"` funciona en consola.
4. Entonces: `streamlit run app.py`.

Si la consola falla, la UI también fallará: **arregla el backend primero**.

---

## Resumen

- Un contrato: función pública → estructura de resultado.
- CLI y Streamlit son dos caras del mismo sistema.
- No reimplementes el pipeline dentro de la UI.