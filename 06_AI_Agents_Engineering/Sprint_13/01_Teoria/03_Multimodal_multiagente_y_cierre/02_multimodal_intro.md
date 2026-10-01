![Cabecera](../../../Sprint_11/assets/cabecera_thebridge.png)

# Multimodal — introducción

## Idea

El modelo recibe **más de un tipo de entrada** (texto + imagen).  
En el workout lo montamos **dentro de LangGraph**: un nodo lee imagen + pregunta y escribe texto en el **estado**.

```text
START → leer_imagen → END
            │
            ▼
   [imagen] + [texto] → Gemini → State.respuesta
```

## Ejemplo de uso en agentes

- Usuario sube la foto de un cartel → el nodo resume → otro nodo / tool busca evento.
- En un ReAct, la misma lógica puede ser una **tool** `describir_imagen`.

## Límites en el bootcamp

- Intro: grafo **lineal** (un nodo multimodal).
- No montamos pipeline de visión completo ni almacenamiento de media.

## En este sprint

Notebook: LangGraph + Gemini multimodal (`google-genai` dentro del nodo).  
El proyecto cultural del hito sigue centrado en **texto + tools**; multimodal es el patrón para ampliar la entrada.

📁 Workout: [`02_multimodal_imagen_texto.ipynb`](../../02_Workout/03_Multimodal_multiagente_y_cierre/02_multimodal_imagen_texto.ipynb)
