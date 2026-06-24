![Cabecera](../../assets/cabecera_gemini.png)

# 📘 Sprint 05 · Unidad 01

## Lógica y modularización en Python (para sistemas IA mantenibles)

En esta unidad el foco no es “aprender Python desde cero”, sino **empezar a programar como alguien que construye sistemas mantenibles**: validar datos, controlar el flujo, separar responsabilidades y gestionar estado.

---

## 📂 Contenido de la teoría

---

### 🧠 0. Mentalidad: de script a sistema mantenible

🔗 [Abrir](./00_Mentalidad_sistemas_mantenibles.md)

**¿Qué aprenderás?**

* Qué separar y por qué (`config`, `prompts`, `logic`, `state`, `main`)
* Qué problemas evita (fragilidad, prompts hardcodeados, deuda técnica)

---

### ✅ 1. Condicionales complejos y validación de inputs

🔗 [Abrir](./01_Condicionales_y_validacion.md)

**¿Qué aprenderás?**

* `and`, `or`, `not`, comparaciones encadenadas
* Validación de strings, rangos, whitelists
* Regex básicas con `re.fullmatch` (email/IDs sencillos)

📓 Notebook (ejemplos): [`01_Condicionales_y_validacion_ejemplos.ipynb`](./01_Condicionales_y_validacion_ejemplos.ipynb)

---

### 🔀 2. Manejo de múltiples respuestas posibles

🔗 [Abrir](./02_Multiples_respuestas_y_flujo.md)

**¿Qué aprenderás?**

* Responder distinto según el caso (OK / error / tipo de tarea)
* `if/elif/else` vs “tabla de handlers” con `dict`

📓 Notebook (ejemplos): [`02_Multiples_respuestas_y_flujo_ejemplos.ipynb`](./02_Multiples_respuestas_y_flujo_ejemplos.ipynb)

---

### 🧩 3–4. Estructura modular y estado en memoria

🔗 [Abrir](./03_Modularización_de_proyectos.md) — incluye **Parte A** (módulos) y **§5** (persistencia en memoria, temario bloque 4)

**¿Qué aprenderás?**

* Separar `config`, `prompts`, `logic` y `state`
* Orquestar desde un `main` mínimo
* Reglas de imports y refactor desde script monolítico
* Historial en memoria: guardar solo si OK, listar, filtrar y contar

📁 Proyecto ejecutable: [`03_Modularización_de_proyectos_ejemplo/`](./03_Modularización_de_proyectos_ejemplo/) — ver su `README.md` (repo independiente en vídeo)

**Bloque 4 del temario:** mismo documento, sección [§5 Persistencia](./03_Modularización_de_proyectos.md#5-persistencia-en-memoria).
