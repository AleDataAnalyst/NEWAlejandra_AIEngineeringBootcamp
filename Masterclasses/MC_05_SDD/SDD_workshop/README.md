# Taller SDD · Spec-Driven Development sobre un RAG

Este repositorio aplica **Spec-Driven Development (SDD)** a un proyecto real: el asistente RAG de la **agenda cultural de Madrid**. El código ya existía; aquí le ponemos encima un sistema de specs para que un agente de IA (GitHub Copilot en VS Code) lo amplíe de forma controlada, en vez de a base de prompts sueltos.

> **Idea central:** la especificación es la fuente de verdad. Primero se acuerda **qué** hay que construir y **cómo se comprueba**; después el agente escribe el código, una tarea cada vez, y se valida contra la spec.

---

## El flujo en una línea

**Constitución → Spec → Clarificación → Plan → Tareas → Implementación (una tarea, tests primero) → Validación → Cambio (primero la spec)**

| Fase | Comando en Copilot Chat | Artefacto que deja |
|---|---|---|
| 1. Constitución y contexto | `/sdd-constitucion` · `/sdd-contexto` | `docs/constitution.md` · `AGENTS.md` |
| 0. Línea base (proyecto ya existente) | `/sdd-spec-inversa` | `specs/000-sistema-actual/spec.md` |
| 2. Especificación | `/sdd-spec <idea>` | `specs/NNN-nombre/spec.md` |
| 3. Clarificación | `/sdd-clarificar` | la misma `spec.md`, sin dudas abiertas |
| 4. Plan | `/sdd-plan` | `specs/NNN-nombre/plan.md` |
| 5. Tareas | `/sdd-tareas` | `specs/NNN-nombre/tasks.md` |
| 6. Implementación | `/sdd-implementar T1` | código + tests, tarea marcada `[x]` |
| 7. Validación | `/sdd-validar` | `specs/NNN-nombre/validacion.md` |
| Cambio | `/sdd-cambio <requisito nuevo>` | diff de la `spec.md` (sin tocar código) |

Los comandos son *prompt files* de VS Code: están en `.github/prompts/`. **Si no te aparecen al escribir `/` en el chat**, abre el archivo de la fase, copia el texto que hay debajo de la cabecera `---` y pégalo en el chat en modo **Agent**, añadiendo al final tu idea o la tarea.

---

## Qué hay en el repositorio

```text
.
├── AGENTS.md                 # Contexto fijo para el agente: qué es el proyecto, mapa, comandos, reglas
├── .github/
│   ├── copilot-instructions.md   # Apunta a AGENTS.md y a la constitución
│   └── prompts/                  # Un comando /sdd-* por fase
├── .vscode/settings.json     # Activa AGENTS.md y los prompt files en Copilot
├── docs/
│   ├── constitution.md       # Principios innegociables del proyecto
│   ├── chuleta_ears.md       # Cómo escribir requisitos verificables
│   └── plantillas/           # spec.md · plan.md · tasks.md · validacion.md
├── specs/
│   └── 000-sistema-actual/   # Spec inversa: lo que el RAG ya hacía (línea base)
├── tests/                    # pytest con dobles de prueba: no llaman a ninguna API
│
├── config.py · main.py · app.py · src/   # El RAG (CLI + Streamlit)
└── data/ · queries/ · output/            # Corpus, preguntas de evaluación e índice generado
```

---

## Puesta en marcha

Vale Python 3.9 o superior.

```bash
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
cp .env.example .env
```

En Windows, activa el entorno con `.venv\Scripts\activate`. Abre `.env` y pega tu `GEMINI_API_KEY`. Después:

```bash
pytest
python main.py --prepare --index
python main.py --ask "¿Hay cine de verano gratuito en Hortaleza?"
streamlit run app.py
```

`pytest` no usa la API y debe salir en verde. `--prepare --index` prepara e indexa el corpus (este sí usa la API).

`MAX_CHUNKS_EMBED` (en `config.py`) limita cuántos fragmentos se indexan. Si lo cambias, regenera el índice con `python main.py --prepare --index --recreate-index`.

---

## Cómo usar Copilot con este repo

1. Abre **esta carpeta** como raíz en VS Code. Si no, Copilot no encuentra `AGENTS.md` ni los comandos.
2. Abre Copilot Chat y elige el modo **Agent**.
3. Escribe `/sdd-` y elige la fase. Cada comando lee la constitución, `AGENTS.md` y la spec activa antes de actuar.
4. Una fase por conversación. Revisa y aprueba lo que genera antes de pasar a la siguiente: **tú decides, el agente ejecuta**.

---

## Para aplicarlo a tu proyecto

La carpeta [`../Plantilla`](../Plantilla), junto a esta, trae este mismo sistema en versión genérica, lista para copiar en tu propio RAG, con una guía paso a paso.

## Recursos
- [mouredev/hello-sdd](https://github.com/mouredev/hello-sdd): curso de SDD desde cero (plantillas y proyecto completo).
- [GitHub Spec Kit](https://github.com/github/spec-kit): el toolkit de referencia de SDD, con comandos `/speckit.*`.
- [EARS, guía de Alistair Mavin](https://alistairmavin.com/ears/): la notación de requisitos que usamos.
- [Prompt files en VS Code](https://code.visualstudio.com/docs/agent-customization/prompt-files) · [Instrucciones personalizadas y AGENTS.md](https://code.visualstudio.com/docs/agent-customization/custom-instructions).
