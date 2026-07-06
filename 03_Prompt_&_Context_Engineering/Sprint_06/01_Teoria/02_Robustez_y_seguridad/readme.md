# 📘 Sprint 06 · Unidad 02

## Robustez y seguridad del asistente

En **Unidad 01** construiste un asistente con estado, configuración y flujo conversacional.

Aquí el foco cambia:

> **El modelo no cambia; cambia el sistema que lo envuelve.**

Aprenderás a reducir riesgos de **prompt injection**, acotar el **dominio**, **validar inputs** antes de gastar tokens y **controlar outputs** (JSON + parseo en Python).

---

## 📂 Contenido de la teoría (orden de lectura)

---

### 📄 0. Introducción a robustez y seguridad

🔗 [Abrir](./00_introduccion_robustez_y_seguridad.md)

**¿Qué aprenderás?**

* Objetivos de la unidad y mapa de documentos
* Qué es prompt injection (visión práctica, sin paranoia)
* Mentalidad “defensa en capas”

---

### 🛡️ 1. Prompt injection y defensas de prompt

🔗 [Abrir](./01_Prompt_injection_y_defensas_de_prompt.md)

**¿Qué aprenderás?**

* Asistente vulnerable vs separación sistema / usuario
* `SYSTEM_PROMPT` y delimitadores
* Restricción de dominio (tutor Python)
* Inputs maliciosos típicos en demos

---

### ✅ 2. Validación, outputs controlados y defensa en capas

🔗 [Abrir](./02_Validacion_outputs_y_defensa_en_capas.md)

**¿Qué aprenderás?**

* `validate_input()` en Python (vacío, largo, sospechoso)
* Salida JSON forzada y `json.loads()` + validación
* Comparativa final vulnerable vs seguro
* Checklist de capas antes de llamar al modelo

---

## Demos ejecutables

| Demo | Tipo 
|------|------
| [01_asistente_vulnerable.ipynb](../../02_Workout/02_Robustez_y_seguridad/01_asistente_vulnerable.ipynb) | Notebook 
| [02_defensas_prompt_y_dominio.ipynb](../../02_Workout/02_Robustez_y_seguridad/02_defensas_prompt_y_dominio.ipynb) | Notebook 
| [03_proyecto_asistente_seguro/](./03_proyecto_asistente_seguro_ejemplo/) | Proyecto `.py` 

**Proyecto:** desde [`03_proyecto_asistente_seguro_ejemplo/`](./03_proyecto_asistente_seguro_ejemplo/), `.venv`, `pip install -r requirements.txt`, `python main.py`.
