![cabecera](../../assets/cabecera_API.png)

## Introducción a la IA generativa

En esta unidad veremos una **introducción teórica a la IA generativa:** qué es, cómo funciona, capacidades, límites y riesgos. 

### Objetivos de aprendizaje

- Entender qué significa “generar” contenido y en qué se diferencia de otros enfoques de IA.
- Reconocer los tipos de modelos y modalidades (texto, imagen, audio, vídeo, código).
- Conocer capacidades, limitaciones y riesgos (fiabilidad, sesgos, privacidad, desinformación).
- Adquirir criterio para usarla de forma responsable en contextos académicos y profesionales.

### 1) ¿Qué es la IA generativa?

La **inteligencia artificial generativa** es una rama de la IA que puede **crear contenido nuevo** a partir de patrones aprendidos en datos (por ejemplo: **texto**, **imágenes**, **audio**, **vídeo** o **código**).

En términos sencillos:

- La IA “clásica” suele **clasificar o predecir** (por ejemplo: “¿es spam o no?”).
- La IA generativa puede **producir** una salida nueva (por ejemplo: “redacta un email”, “resume este documento”, “genera una imagen”).

Una forma útil de pensarlo es que la IA generativa automatiza parte del **trabajo de creación y síntesis** (borradores, propuestas, alternativas), pero **no sustituye** la revisión humana cuando el resultado importa.

- [AWS | what is generative ai](`https://aws.amazon.com/es/what-is/generative-ai/`)
- [Microsoft AI-101 | what is generative ai](`https://www.microsoft.com/es-es/ai/ai-101/what-is-generative-ai`)
- [Wikipedia | what is generative ai](`https://es.wikipedia.org/wiki/Inteligencia_artificial_generativa`)
- [Oracle | what is generative ai](`https://www.oracle.com/es/artificial-intelligence/generative-ai/what-is-generative-ai`)

### 2) IA generativa vs IA “tradicional”

Aunque comparten fundamentos (aprendizaje automático y redes neuronales), a alto nivel:

- La IA tradicional suele estar diseñada para tareas concretas (detección de fraude, predicción, clasificación).
- La IA generativa se centra en **generar** contenido que se parece a los datos con los que aprendió, pero que no es una copia directa.

### 3) ¿Qué puede generar? Modalidades

Según el tipo de datos:

- **Texto**: chat, resumen, traducción, extracción de datos, redacción.
- **Código**: ayuda para programar, explicar, refactorizar, documentar.
- **Imágenes**: generación a partir de texto (text-to-image), edición.
- **Audio**: voz sintética, música.
- **Vídeo**: generación/edición (campo aún más reciente y exigente).
- **Multimodal**: combina varios tipos (por ejemplo texto+imagen).

En la práctica educativa, lo más frecuente es empezar por **texto** y **código**, porque son fáciles de probar, copiar y evaluar.

### 4) Ejemplos de productos

- Chatbots (conversación).
- Generadores de imagen a partir de texto.
- Asistentes en editores/IDEs para código.
- Herramientas para resumen, traducción y reescritura.

### 5) Cómo funciona

Sin entrar en matemáticas, la idea central es:

- El modelo aprende **patrones** en grandes cantidades de datos.
- En uso, recibe un **contexto** (instrucciones + datos) y produce una salida que sigue esos patrones.

En modelos de lenguaje (LLMs), el mecanismo habitual es generar la respuesta **paso a paso** (por “tokens”), eligiendo en cada paso qué token es más probable dado el contexto.

#### Modelos fundacionales

Muchos sistemas modernos se basan en **modelos fundacionales**: modelos grandes entrenados con datos generales que luego se pueden adaptar a múltiples tareas (a veces con ajustes o instrucciones).

### 6) Intuición clave: “predecir el siguiente token”

En modelos de lenguaje, una explicación intuitiva habitual es:

- El modelo aprende a **predecir el siguiente token** dada una secuencia previa.
- Al repetir ese proceso muchas veces, puede producir respuestas largas y coherentes.

Esto explica por qué puede “sonar” convincente incluso cuando se equivoca: no está verificando hechos, está generando texto plausible.

### 7) Familias de modelos

Hay varias aproximaciones históricas y técnicas. A nivel divulgativo:

- **Transformers**: muy usados para lenguaje (y base de muchos LLMs).
- **GAN / VAE**: han sido relevantes en generación (especialmente en imagen) y en la evolución de la tecnología.
- **Difusión**: muy usada en generación de imágenes de alta calidad.

No necesitas dominar estas familias para empezar, pero sí entender que existen y que el “tipo de modelo” condiciona el tipo de salida (texto vs imagen, etc.).

### 8) Transformers

Los **transformers** se convirtieron en una arquitectura central porque permiten modelar dependencias complejas en secuencias y funcionan muy bien en tareas de lenguaje.

### 9) GAN y VAE (dos ideas históricas)

- **GAN**: Redes Generativas Antagónicas. Dos redes compiten (generador vs discriminador) para producir muestras cada vez más realistas.
- **VAE**: Autoencoders Variacionales. comprime datos a un espacio latente y luego genera a partir de esa representación.

### 10) Difusión (intuición)

En muchos modelos de imagen, la difusión se entiende como un proceso de:

- añadir ruido gradualmente (en entrenamiento) y
- aprender a revertirlo para generar una muestra coherente.

### 11) Capacidades típicas

Casos de uso comunes:

- **Resumir** y sintetizar información.
- **Reescribir** con un estilo/tono (más formal, más breve, etc.).
- **Clasificar** (temas, intención, sentimiento).
- **Extraer** datos estructurados desde texto (por ejemplo, JSON).
- **Generar borradores** (emails, documentación, ideas).
- **Asistencia al desarrollo** (explicar código, proponer tests, etc.).

### 12) Beneficios habituales

En organizaciones suele aportar valor por:

- **Productividad**: acelerar borradores, resúmenes, clasificación, documentación.
- **Síntesis de conocimiento**: encontrar patrones y condensar información no estructurada.
- **Creatividad asistida**: proponer alternativas, variaciones y enfoques.

### 13) Limitaciones

La IA generativa no es un “oráculo”:

- **Alucinaciones**: puede inventar información o mezclar hechos con falsedades, con un tono convincente.
- **Conocimiento no actualizado**: si el modelo no tiene acceso a datos recientes, puede quedarse obsoleto.
- **Sensibilidad al prompt**: pequeños cambios en instrucciones o contexto pueden cambiar el resultado.
- **No es un verificador**: si algo importa, hay que **validar** o contrastar por otras vías.

Consecuencia práctica: en tareas críticas (médicas, legales, financieras, seguridad), la IA generativa debe usarse con controles, revisión y fuentes verificables.

### 14) Riesgos y preocupaciones

Aspectos relevantes (ética y seguridad) en un entorno profesional:

- **Sesgos**: el modelo puede reflejar o amplificar sesgos presentes en los datos de entrenamiento.
- **Privacidad y datos sensibles**: no debes enviar información confidencial a servicios externos sin políticas claras.
- **Propiedad intelectual y derechos de autor**: cuidado con introducir material protegido o reutilizar outputs sin revisión.
- **Desinformación y deepfakes**: el contenido sintético puede usarse mal (suplantación, fraude, etc.).
- **Seguridad**: riesgo de *prompt injection* en aplicaciones que mezclan instrucciones del sistema con inputs de usuarios.

Regla práctica: IA generativa se usa mejor como **asistente** bajo supervisión, no como “decisor final” sin control.

### 15) Riesgos típicos en la práctica

- **Desinformación**: generar contenido falso con alta fluidez.
- **Deepfakes**: suplantación visual o de voz.
- **Fuga de datos**: pegar información sensible en una herramienta externa.
- **Plagio accidental**: usar outputs sin verificar fuentes, citas o licencias.

### 16) Buenas prácticas conceptuales

Antes de programar, para usar IA generativa de forma “ingenieril”:

- Define el **objetivo** exacto de la salida.
- Decide si necesitas **texto libre** (para leer) o **salida estructurada (JSON)** (para automatizar).
- Piensa en el output como un **contrato**: qué formato esperas y cómo lo validarás.

Buenas prácticas para estudiantes:

- Si la usas para estudiar, pide **explicaciones + ejemplos** y luego compruébalo con fuentes.
- Si la usas para un trabajo, deja claro qué partes son tuyas y cuáles han sido asistidas.
- Evita usarla como “autoridad”: úsala como **ayuda para pensar**, no como juez final.

