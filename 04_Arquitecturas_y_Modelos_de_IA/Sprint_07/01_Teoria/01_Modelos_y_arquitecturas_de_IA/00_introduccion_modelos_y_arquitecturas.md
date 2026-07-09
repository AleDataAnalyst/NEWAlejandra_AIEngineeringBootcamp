![Cabecera](../../assets/cabecera_gemini.png)

# Introducción: familias de modelos y arquitecturas

Hasta ahora has construido **asistentes**: prompts, contexto, validación, seguridad. En esta unidad cambiamos el foco:

> **¿Qué familia de modelo y qué arquitectura encajan en cada problema?**

No necesitas derivadas ni ecuaciones. Necesitas **criterio**: leer un problema de producto y traducirlo a “texto / embeddings / multimodal” y, cuando toque, “Transformer / CNN / RNN”.

---

## Objetivos de la unidad

Al terminar, deberías poder:

- Distinguir **familias** de modelos: texto, embeddings, multimodal.
- Nombrar **arquitecturas** a nivel conceptual: Transformer, RNN, CNN.
- Explicar **por qué los Transformers dominan** la IA generativa actual (sin matemáticas).
- Usar tablas **problema → tipo de modelo** para decidir.
- Reconocer **limitaciones** y **cuándo un modelo no sirve**.
- Entender el **coste** de usar tiers avanzados (orientación, no factura exacta).

---

## Tabla guía

| Problema | Familia / enfoque | Arquitectura típica |
|----------|-------------------|---------------------|
| Chatbot | Modelo de **texto** (LLM) | **Transformer** |
| Búsqueda semántica | **Embeddings** + índice vectorial | Transformer (encoder) u otros |
| Clasificación de imágenes | Visión | **CNN** (o ViT, variante Transformer) |
| OCR / foto + pregunta | **Multimodal** | Transformer multimodal |
| Series temporales cortas (clásico) | Secuencias | **RNN** / LSTM (menos habitual en GenAI hoy) |
| RAG (docs + respuesta) | Embeddings **+** LLM | Embeddings + Transformer |

En la práctica muchos productos **combinan** filas (p. ej. RAG = embeddings + chat Transformer).

---

## Modelo ≠ producto

```text
Problema de negocio
        │
        ▼
┌───────────────────┐
│ Familia           │  texto / embedding / multimodal
└─────────┬─────────┘
          ▼
┌───────────────────┐
│ Arquitectura      │  Transformer, CNN, RNN… (criterio, no implementación)
└─────────┬─────────┘
          ▼
┌───────────────────┐
│ Tu sistema        │  prompts, RAG, validación, logging
└───────────────────┘
```
