![Cabecera](../../assets/cabecera_rag.png)

# Prompt con contexto recuperado

## Objetivos

- Separar **instrucciones**, **contexto** y **pregunta del usuario**.
- Diseñar prompts que obliguen a **grounding** (responder solo con el contexto).
- Incluir reglas de **citas** y **abstención** cuando no hay evidencia.

---

## 1) Por qué el prompt importa tanto

Con el mismo top-K, dos prompts distintos producen sistemas muy diferentes:

| Prompt | Efecto típico |
|--------|---------------|
| Permisivo («responde lo mejor que puedas») | Completa con conocimiento del modelo → más alucinaciones |
| Restrictivo («solo con el contexto; si no, dilo») | Más abstenciones honestas, menos invenciones |

El retrieval decide **qué lee** el modelo. El prompt decide **cómo lo usa**.

![Prompt RAG](../../assets/context_promt_rag.webp)

---

## 2) Estructura recomendada

```text
[Instrucciones fijas]
  - Rol / dominio (agenda cultural Madrid)
  - Responde solo con el contexto
  - Si no hay info suficiente, dilo
  - Cita la fuente cuando puedas

[Contexto recuperado]
  --- Fragmento 1 ---
  Fuente: faq_agenda_cultural.md
  ...

  --- Fragmento 2 ---
  Fuente: …csv
  ...

[Pregunta del usuario]
  ¿Hay cine gratuito en verano?

[Respuesta]
  (el modelo escribe aquí)
```

En el proyecto, `prompts.py` lo ensambla así:

```python
def build_rag_prompt(contexto: str, pregunta: str) -> str:
    return (
        f"{INSTRUCCIONES_RAG}\n\n"
        f"--- CONTEXTO RECUPERADO ---\n"
        f"{contexto.strip()}\n\n"
        f"--- PREGUNTA ---\n"
        f"{pregunta.strip()}\n\n"
        f"--- RESPUESTA ---"
    )
```

El `contexto` viene de `formatear_contexto(chunks)` — el mismo formateo que ya usabas en S9 para inspeccionar.

---

## 3) Separar claramente las partes del prompt

| Componente   | Quién lo define                  | ¿Debe cambiar en cada consulta?         |
|--------------|----------------------------------|-----------------------------------------|
| Instrucciones| Quien diseña el sistema/prompt   | No (salvo experimentación o ajustes)    |
| Contexto     | Mecanismo de recuperación de info | Sí                                     |
| Pregunta     | Usuario final                    | Sí                                     |

Un error común es mezclar instrucciones **dentro** del bloque de contexto, lo que puede llevar al modelo a confundir directivas con evidencia.

Otro error es no delimitar claramente los fragmentos del contexto. Si se añade texto sin separar fuentes o partes, se dificulta identificar qué información concreta se utilizó y el proceso de análisis resulta menos transparente y más difícil de depurar.

---

## 4) Grounding y abstención

Grounding es el proceso de asegurar que el modelo solo use la información del contexto para generar la respuesta.

Abstención es el proceso de no generar una respuesta cuando no hay suficiente información en el contexto.

Reglas útiles en las instrucciones:

- Responde **únicamente** con la información del contexto.
- Si el contexto no contiene la respuesta, dilo explícitamente (no inventes).
- Cuando cites un hecho, menciona la **fuente** si aparece en el contexto.

Ejemplo de pregunta fuera de corpus (q5 en `preguntas_eval.json`):

> «¿Cuál es la capital de Francia?»

Con un buen prompt, el sistema debería **abstenerse** aunque el modelo «sepa» que es París. En un RAG de agenda cultural, París no está en el corpus.

---

## 5) Texto libre vs JSON

A veces conviene pedir **salida estructurada** (como vimos en el Sprint 5):

```json
{
  "respuesta": "…",
  "hay_evidencia": true,
  "fuentes_citadas": ["faq_agenda_cultural.md"]
}
```

Con la misma información recuperada (contexto), puedes optar por diferentes formatos de salida. El programa puede analizar la respuesta estructurada (por ejemplo, usando `json.loads`) y tomar decisiones según los campos devueltos (por ejemplo, si `hay_evidencia` es falso, mostrar un mensaje de abstención en la interfaz).

Reglas útiles en el prompt:

- Responde **solo** con JSON válido (sin markdown alrededor, si puedes).
- Define el esquema de campos.
- Si no hay evidencia, `hay_evidencia: false`.

---

## 6) Errores frecuentes

| Error | Consecuencia |
|-------|--------------|
| Mezclar instrucciones dentro del contexto | El modelo confunde qué es evidencia |
| No delimitar fragmentos | Difícil saber qué chunk usó |
| Prompt demasiado permisivo | Alucinaciones |
| Contexto muy largo (K alto) | Ruido, coste y dilución de la evidencia útil |
| Olvidar la pregunta al final | El modelo resume el contexto sin responder |
| Pedir JSON sin validar en Python | Fallos silenciosos o crashes al parsear |

---

## Resumen

- Estructura: instrucciones + contexto + pregunta.
- El prompt controla el **grounding**; el retriever controla la **evidencia**.
- Abstenerse es a veces la respuesta correcta.
- Texto libre o JSON: elige según si un programa debe **consumir** la salida.
