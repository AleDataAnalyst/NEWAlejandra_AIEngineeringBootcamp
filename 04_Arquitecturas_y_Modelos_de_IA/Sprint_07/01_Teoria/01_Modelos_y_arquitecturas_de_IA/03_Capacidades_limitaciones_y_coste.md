![Cabecera](../../assets/cabecera_gemini.png)

# Capacidades, limitaciones y coste

Elegir modelo es elegir **qué puede hacer bien**, **qué no debe hacer** y **cuánto pagas** por ello.

---

## 1. Qué problemas resuelve cada tipo

| Tipo | Resuelve bien | No es su trabajo principal |
|------|---------------|----------------------------|
| **LLM de texto** (Transformer) | Chat, resumen, código, razonamiento con contexto | Búsqueda en millones de docs sin índice |
| **Embeddings** | Similitud semántica, recuperación para RAG | Redactar respuestas largas |
| **Multimodal** | Imagen + pregunta, OCR integrado | Solo tablas numéricas masivas |
| **CNN (visión)** | Clasificar/detectar en imágenes | Conversación abierta |
| **RNN (secuencias)** | Series cortas, modelos legacy | Chat generalista actual |

---

## 2. Casos donde un modelo NO es adecuado

| Quieres hacer… | Error común | Mejor enfoque |
|----------------|-------------|---------------|
| Búsqueda en 100k documentos | Meter todo en el prompt del LLM | **Embeddings** + top-K + LLM |
| Clasificar fotos de producto | Solo prompt de texto | **CNN** / modelo de visión |
| Chat con datos siempre actualizados | Confiar en memoria del modelo | RAG, API, base de datos |
| Verdad matemática/legal crítica | Una sola respuesta sin revisar | Validación, fuentes, humano |
| Latencia < 200 ms en móvil | Tier “pro” enorme | Modelo **flash** + prompt corto |
| 10 M de clasificaciones/día baratas | Mismo LLM caro en cada fila | Modelo pequeño, batch, reglas |
| Privacidad estricta sin contrato | API pública sin revisar política | On-prem, anonimización, legal |

**Regla:** si la fila de “error común” te suena familiar, cambia de **familia** o de **arquitectura**, no solo de prompt.

---

## 3. Limitaciones transversales de todos los LLM

```text
  ┌─────────────────────────────────────────┐
  │  El modelo NO es una base de datos        │
  │  El modelo NO garantiza verdad           │
  │  El modelo NO lee tu mente (sin contexto) │
  │  Más contexto ≠ siempre mejor respuesta   │
  └─────────────────────────────────────────┘
```

| Limitación | Qué hacer en tu sistema |
|------------|-------------------------|
| Alucinaciones | RAG, citas, “no sé”, validación |
| Ventana finita | Resumir, recortar, menos chunks |
| Coste por token | Filtrar contexto en Python |
| Variabilidad | Temperatura baja, tests, JSON schema |

---

## 4. Coste de utilizar modelos avanzados

**“Avanzado”** suele significar: tier **pro**, contexto **largo**, **multimodal**, o **mucho volumen**.

### De qué depende el coste (sin fórmulas raras)

```text
  COSTE ≈ (tokens entrada + tokens salida) × precio del tier × número de llamadas
```

| Palanca | Efecto |
|---------|--------|
| Tier flash vs pro | Pro suele ser **más caro y lento**, mejor en tareas duras |
| Prompt largo (RAG sin filtrar) | Dispara tokens de **entrada** |
| Respuestas verbosas | Dispara tokens de **salida** |
| Chat con historial completo | Cada turno reenvía todo el historial |
| Multimodal | Suele costar más que texto solo |
| Muchas llamadas en batch | El total mensual importa más que una demo |

### Ejemplo mental

| Escenario | Modelo típico | Comentario de coste |
|-----------|---------------|---------------------|
| Soporte chat, miles/día | flash | Mantener si calidad suficiente |
| Informe legal complejo, pocos/día | pro | Pocos calls → coste aceptable |
| Etiquetar 1 M filas | flash o ML clásico | Pro en 1 M calls → inviable |
| Foto + pregunta ocasional | multimodal | OK; en volumen, evaluar OCR+CNN+texto |

---

## 5. Escenarios de producto

### Soporte (chat)

- **Familia:** texto (Transformer).
- **Evitar:** pro en cada “hola”; contexto FAQ sin filtrar.

### RAG documentación

- **Familia:** embeddings + texto.
- **Evitar:** solo LLM sin recuperación.

### Clasificación imágenes

- **Arquitectura:** CNN / visión — no LLM de chat.

### OCR multimodal

- **Familia:** multimodal (Transformer) u OCR + texto.

### Batch nocturno

- **Criterio:** el tier **más barato** que pase tu umbral de calidad medido en U2.

---

## 6. Checklist antes de elegir

```text
□ ¿Qué familia encaja? (texto / embeddings / multimodal / visión)
□ ¿Qué arquitectura es la referencia? (Transformer / CNN / …)
□ ¿Hay caso donde NO sirve? (tabla §2)
□ ¿Volumen y latencia aceptables?
□ ¿Tier flash basta? (probar antes de subir)
□ ¿Cómo mido en U2? (mismas preguntas, varios modelos)
```

---

## 7. Errores comunes

| Error | Problema |
|-------|----------------|
| LLM para todo | Coste y calidad peores que el enfoque correcto |
| Ignorar embeddings en búsqueda | “No encuentra” o prompt gigante |
| Pro porque suena mejor | Factura y latencia sin ganancia real |
| Benchmark ajeno (MMLU) como única prueba | No refleja tu FAQ ni tu dominio |
