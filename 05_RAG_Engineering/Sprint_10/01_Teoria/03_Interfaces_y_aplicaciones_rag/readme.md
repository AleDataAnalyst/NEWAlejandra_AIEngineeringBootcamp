![Cabecera](../../assets/cabecera_rag.png)

# Sprint 10 · Bloque 03

## Interfaces y aplicaciones

El sistema ya funciona en consola o notebook. Este bloque lo convierte en algo **demostrable**: una interfaz (MVP) o, más adelante, una API — sin reescribir la lógica de negocio.

> **¿Cómo expongo un sistema ya construido (modelo, RAG, agente…) de forma usable?**

Caso de uso del sprint: app **Streamlit** sobre el pipeline RAG (`responder(pregunta)` → respuesta + fuentes).

---

## Contenido de la teoría (orden de lectura)

### 0. Introducción

🔗 [Abrir](./00_introduccion_interfaces.md)

* Por qué exponer un sistema
* UI vs API (y clientes a medida)
* MVP con Streamlit en este curso

---

### 1. Streamlit

🔗 [Abrir](./01_streamlit.md)

* Frontend clásico vs interfaz en Python
* Chat básico: [`06_miniproyecto_streamlit/`](./06_miniproyecto_streamlit/)
* Referencias oficiales

---

### 2. De script a aplicación

🔗 [Abrir](./02_de_script_a_aplicacion.md)

* Contrato de backend (`responder()` en el proyecto)
* No rehacer el pipeline en la UI

---

### 3. Resultado, estado y errores

🔗 [Abrir](./03_mostrar_fuentes_estado_y_errores.md)

* Qué mostrar al usuario vs debug
* Spinner, errores, fuentes (caso RAG)

---

### 4. Opciones de mercado: web, móvil y APIs

🔗 [Abrir](./04_otras_opciones_de_interfaz.md)

* Interfaces web (Streamlit, Gradio, React, Vue…)
* Apps móviles (nativo, Flutter, React Native…)
* APIs (FastAPI, Flask, DRF, Express…)
* Por qué Streamlit en el bootcamp

---

## Workout (vídeo guiado)

| Recurso | Cubre |
|---------|--------|
| [01_crear_interfaz_streamlit_rag.ipynb](../../02_Workout/03_Interfaces_y_aplicaciones_rag/01_crear_interfaz_streamlit_rag.ipynb) | Interfaz Streamlit |
| [02_proyecto_rag_aplicacion.md](../../02_Workout/03_Interfaces_y_aplicaciones_rag/02_proyecto_rag_aplicacion.md) | Repo del proyecto completo |

📁 Miniproyecto Streamlit (demo): [`06_miniproyecto_streamlit/`](./06_miniproyecto_streamlit/)
📁 Proyecto RAG ejecutable: [`05_proyecto_rag_aplicacion/`](./05_proyecto_rag_aplicacion/)
