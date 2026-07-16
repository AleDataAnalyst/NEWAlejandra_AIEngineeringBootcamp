![Cabecera](../../assets/cabecera_rag.png)

# Comparación de modelos de embedding

Igual que en el Sprint 7 comparaste **LLMs** con latencia y calidad, aquí comparas **modelos de embedding** con similitud semántica en frases controladas.

> **No elijas un embedding porque suena bien; elige el que separa bien tus pares de prueba en tu dominio.**

---

## Objetivos

- Diseñar un mini-set de **frases de prueba**.
- Comparar similitudes intra-pares (sinónimos) vs inter-pares (temas distintos).
- Documentar una **decisión preliminar** antes de indexar en Chroma.

---

## 1) Frases de prueba sugeridas (bootcamp)

| ID | Frase |
|----|-------|
| A1 | Live Review del bootcamp |
| A2 | Sesión en vivo de dos horas del sprint |
| B1 | ¿Cuándo entregar la práctica obligatoria? |
| B2 | Plazo de entrega de la práctica antes de la Live Review |
| C1 | Receta tradicional de tortilla española |

**Expectativa:**

- A1–A2 → similitud **alta**
- B1–B2 → similitud **alta**
- A1–C1 → similitud **baja**

---

## 2) Matriz de similitud (concepto)

```text
              A1    A2    B1    B2    C1
         A1  1.00  0.85  0.40  0.45  0.10
         A2  0.85  1.00  ...
         ...
```

Diagonal = 1.0 (consigo mismo). Bloques A y B deberían correlacionar; fila A vs C debería ser baja.

---

## 3) Criterios de evaluación (estilo Sprint 7)

| Criterio | Qué mirar |
|----------|-----------|
| **Separación semántica** | ¿A1–C1 claramente menor que A1–A2? |
| **Dimensiones** | ¿768 vs 384 afecta almacenamiento? |
| **Latencia** | Tiempo por batch de 10 chunks |
| **Operativa** | ¿API key, cuotas, offline? |
| **Coherencia stack** | ¿Mismo proveedor que el LLM (Gemini)? |

---

## 4) Tabla de decisión (plantilla)

Rellena tras ejecutar el notebook [`02_comparar_modelos_embedding.ipynb`](../../02_Workout/03_Embeddings/02_comparar_modelos_embedding.ipynb):

| Par frases | Similitud Gemini | Similitud HF | ¿Correcto? |
|------------|------------------|--------------|------------|
| A1 – A2 | | | |
| B1 – B2 | | | |
| A1 – C1 | | | |

**Decisión preliminar para el proyecto del módulo:**

```text
Modelo elegido: text-embedding-004 (Gemini)
Motivo: coherencia con stack bootcamp + dimensión adecuada para Chroma en S9
```

---

## 5) Qué hacer si dos modelos empatan

1. Embeddea **3 chunks reales** de `chunks.json` con ambos.
2. Simula una pregunta: «¿Qué es la Live Review?»
3. Mira cuál modelo pone el chunk FAQ **más arriba** (similitud manual con numpy).
4. En Sprint 9 formalizarás esto con top-K en Chroma.

---

## 6) Límites de esta comparación

- No sustituye un benchmark de retrieval completo (Sprint 9).
- 5 frases no representan todo tu corpus.
- Embeddings multilingües pueden variar si mezclas idiomas.

---

## Resumen

- Compara embeddings con **pares controlados** + matriz de similitud.
- Elige **un modelo** para indexar y consultar.
- Siguiente sprint: indexar `embeddings.json` en ChromaDB.
