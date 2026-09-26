![Cabecera](../../../Sprint_11/assets/cabecera_thebridge.png)

# Tools en Python

En el workout las tools no viven sueltas en el notebook: viven en módulos y se **registran** por nombre.

---

## Contrato de una tool

```python
def nombre_tool(arg1: str, arg2: int = 5) -> str:
    """Descripción clara."""
    ...
    return "texto corto para el LLM"
```

| Regla | Por qué |
|-------|---------|
| Devuelve `str` (o JSON **pequeño**) | Fácil de meter en `function_response` |
| Args tipados y pocos | El modelo falla menos |
| Nombre estable | Coincide con la declaración Gemini |
| Sin side-effects peligrosos | No borrar ficheros, no `eval`, etc. |

---

## Registro / allowlist

```python
TOOL_REGISTRY = {
    "hora_actual": hora_actual,
    "RAG_buscar_en_guia": RAG_buscar_en_guia,
    "API_consultar_eventos_madrid": API_consultar_eventos_madrid,
}

def ejecutar_tool(nombre: str, args: dict) -> str:
    if nombre not in TOOL_REGISTRY:
        return f"Error: tool '{nombre}' no está permitida."
    ...
```

Ventajas: el modelo no puede inventar `borrar_disco`; un solo sitio para validar y devolver errores.

---

## Estructura del workout (Bloque 2)

```text
02_Integracion_de_herramientas/
  tools/
    __init__.py
    hora_actual.py
    rag_guia.py
    api_eventos.py
  data/
  01_multi_tool_con_rag.ipynb
```

El notebook importa y orquesta; los `.py` ejecutan.  
El proyecto del Bloque 3 **repite el patrón** (carpeta propia, independiente).
