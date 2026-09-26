![Cabecera](../../../Sprint_11/assets/cabecera_thebridge.png)

# Introducción — Control y seguridad de tools

Ya sabes declarar tools y ejecutarlas. Sin **límites**, un agente puede:

- pedir tools en bucle infinito,
- llamar a una función que no existe,
- tumbarse si la API falla,
- llenar el contexto con basura.

Este bloque cierra la parte de **tools**: **validación**, **allowlist**, **`max_steps`**, **errores** y **traza**. La práctica es el proyecto CLI + Streamlit. Después vienen los notebooks de LangGraph (API básica; no sustituyen este proyecto).

> Decisión (LLM) ≠ ejecución (Python). El control vive en Python.

---

## Objetivos

- Validar nombre y args antes de ejecutar.
- Cortar el loop con `max_steps`.
- Registrar cada tool call en `traza`.
- Relacionar el loop de tools con nodos/edges (continuación LangGraph + notebooks).
- Servir el mismo `procesar_turno` en CLI y Streamlit.
