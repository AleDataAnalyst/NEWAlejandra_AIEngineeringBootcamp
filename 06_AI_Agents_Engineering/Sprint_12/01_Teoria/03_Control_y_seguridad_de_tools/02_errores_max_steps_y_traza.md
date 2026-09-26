![Cabecera](../../../Sprint_11/assets/cabecera_thebridge.png)

# Errores, max_steps y traza

Tres piezas de control que ya intuiste en S11 (`max_turns`, `error`, `traza`) y aquí aplicas al **loop interno de tools**.

---

## max_steps

Tope de vueltas **modelo ↔ tool** dentro de un mismo mensaje de usuario.

```text
step 1: LLM pide RAG
step 2: LLM pide API
step 3: LLM responde texto  → fin
…
step N == max_steps → cortas con mensaje claro
```

Sin `max_steps`, un mal prompt puede quemar cuota en bucle.

Diferencia con S11:

| Concepto | Cuenta |
|----------|--------|
| `max_turns` | Mensajes de **usuario** |
| `max_steps` | Llamadas / vueltas de **tools** dentro de un turno |

---

## Errores de tool

Si `requests` falla o el RAG no encuentra fichero:

1. **No** dejes que la excepción tumbe Streamlit sin captura.
2. Devuelve un string de error en la function response **o** rellena `estado["error"]`.
3. Prefiere fallback (API → JSON local) antes de abortar.

---

## Traza

Cada step deja huella legible:

```json
{
  "step": 1,
  "tool": "RAG_buscar_en_guia",
  "args": {"consulta": "museos gratis"},
  "status": "ok",
  "preview": "Según la guía, el primer domingo…"
}
```

Útil para debug en el expander de Streamlit y para live review.

No mandes la traza completa al LLM en cada prompt (ruido); guárdala en el estado de Python.

---

## done (sigue siendo de Python)

Tras el loop de tools, puedes sintetizar `preferencias` / `plan` (JSON) y calcular `done` como en S11.  
El LLM **no** debe tener una tool `marcar_done`.
