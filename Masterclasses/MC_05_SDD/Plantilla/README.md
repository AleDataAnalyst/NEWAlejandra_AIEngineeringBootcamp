# Plantilla SDD para tu Project Break de RAG

Con esta plantilla vas a aplicar **Spec-Driven Development** a tu propio RAG para añadir **una funcionalidad pequeña**: la especificas, la aclaras, la planificas, la divides en tareas y dejas implementada la primera, con sus tests.

Es el mismo sistema que viste en la demo (`SDD_workshop`), en versión genérica.

---

## Qué necesitas
- VS Code con **GitHub Copilot**, sesión iniciada y el chat en modo **Agent**.
- Tu repo del Project Break de RAG clonado, con el entorno virtual activo y las dependencias instaladas.
- `pip install pytest` dentro del entorno virtual.
- Una rama para el taller: `git switch -c feature/sdd`.

## Qué hay en la plantilla

```text
Plantilla/
├── README.md               # esta guía
├── ideas_de_features.md    # menú de funcionalidades para elegir
└── copiar_a_tu_repo/       # ← lo que copias en la raíz de tu proyecto
    ├── AGENTS.md               # contexto del agente (con huecos [COMPLETAR])
    ├── .github/
    │   ├── copilot-instructions.md
    │   └── prompts/            # comandos /sdd-* para Copilot Chat
    ├── .vscode/settings.json   # activa AGENTS.md y los comandos
    ├── docs/
    │   ├── constitution.md     # propuesta de principios (con huecos [COMPLETAR])
    │   ├── chuleta_ears.md
    │   ├── tests_sin_api.md    # cómo testear un RAG con dobles de prueba
    │   └── plantillas/         # spec · plan · tasks · validacion
    ├── specs/README.md
    └── pytest.ini
```

---

## Paso 0 · Copia la plantilla en tu repo (durante la pausa)

Desde la carpeta `MC_05_SDD` del repo del bootcamp, en macOS, Linux o **Git Bash** en Windows:

```bash
cp -Rn Plantilla/copiar_a_tu_repo/. /ruta/a/tu-repo-rag/
```

- `-n` **no sobrescribe** nada que ya exista. Si ya tenías `.vscode/settings.json` o `pytest.ini`, copia a mano las líneas que falten.
- `.github` y `.vscode` son carpetas **ocultas**: si copias desde el Finder o el Explorador, activa "ver archivos ocultos".

Abre **tu repo como carpeta raíz** en VS Code (no la carpeta del bootcamp): si no, Copilot no encuentra ni `AGENTS.md` ni los comandos. Si tu proyecto vive en una subcarpeta del repo, copia la plantilla en la carpeta donde están `main.py` y `src/` y abre esa.

**Comprueba:** en el chat de Copilot, en modo **Agent**, escribe `/sdd-`. Deben salir los comandos.

> **¿No salen?** Abre `.github/prompts/sdd-<fase>.prompt.md`, copia el texto que hay **debajo** de la cabecera `---`, pégalo en el chat (modo Agent) y añade al final tu idea o tu tarea. Funciona igual.

---

## Paso 1 · Contexto y constitución (10′)

1. `/sdd-contexto` → rellena `AGENTS.md` leyendo tu código. **Revísalo**: ¿el mapa de archivos y los comandos son los tuyos? Corrige lo que no cuadre y apruébalo.
2. `/sdd-constitucion` → completa la propuesta de `docs/constitution.md` y te dice qué principios no cumple hoy tu código. Ajusta y apruébala.

> Que tu código no cumpla algún principio no es un problema: es un candidato a spec (por ejemplo, "no hay tests").

## Paso 2 · Elige la funcionalidad (2′)
Mira [`ideas_de_features.md`](ideas_de_features.md) y quédate con **una**. Si dudas, la 1 (errores amigables) o la 2 (`rag_ask()`).

## Paso 3 · Spec (8′)

```text
/sdd-spec <la idea de la funcionalidad>
```

El agente te hará hasta 5 preguntas, **de una en una**. Contesta pensando en la persona que usa tu asistente. Después, revisa la `spec.md` con esta lista:

- [ ] Cada RF es **una frase en EARS** (CUANDO…, SI… ENTONCES…, MIENTRAS…, DONDE…, EL SISTEMA…).
- [ ] Cada RF se puede **comprobar** (se te ocurre el test).
- [ ] **No hay implementación**: ni nombres de archivos, ni funciones, ni librerías.
- [ ] Hay **Fuera de alcance**.
- [ ] Lo que no sabías está marcado como `[NECESITA ACLARACIÓN]`, no inventado.

## Paso 4 · Clarificación (5′)

```text
/sdd-clarificar
```

Te devolverá una lista de ambigüedades, contradicciones y casos límite. Contesta **todas en un mismo mensaje** y deja que actualice la spec. Apunta la pregunta que más te haya sorprendido: la compartiremos al final.

## Paso 5 · Plan y tareas (10′)

```text
/sdd-plan
```
Revisa que cada RF tiene su parte del plan y su test, y que los tests usan **dobles de prueba** (ver `docs/tests_sin_api.md`). Aprueba y:

```text
/sdd-tareas
```
Cada tarea debe tener una línea **"Hecho cuando:"** que se pueda comprobar.

## Paso 6 · Implementa UNA tarea (10′)

```text
/sdd-implementar T1
```

Vigila que:
1. escribe los **tests primero** y los ve fallar,
2. escribe el código mínimo y `pytest` sale en **verde**,
3. marca `[x]` en `tasks.md` y **se para**.

Si intenta seguir con la siguiente tarea, dile que pare.

## Si te sobra tiempo
- `/sdd-implementar T2` y siguientes, de una en una.
- `/sdd-validar` cuando estén todas: deja `validacion.md` con el veredicto.
- `/sdd-cambio <requisito nuevo>` para ver cómo un cambio empieza en la spec.
- En casa: `/sdd-spec-inversa` documenta lo que tu RAG ya hacía como `specs/000-sistema-actual` y saca a la luz sus huecos.

## Para cerrar
```bash
git status
```

Comprueba que **no** aparecen `.env` ni `output/`. Después:

```bash
git add -A
git commit -m "SDD: spec 001 + T1"
git push -u origin feature/sdd
```

---

## Problemas frecuentes

| Problema | Solución |
|---|---|
| No salen los comandos `/sdd-*` | ¿Has abierto tu repo como raíz? ¿Estás en modo Agent? Si aun así no salen, copia y pega el texto del `.prompt.md` (ver paso 0). |
| El agente escribe código en la spec o en el plan | Dile: "Estamos en la fase de spec: no escribas código, sigue AGENTS.md". Pídele que lo quite. |
| Hace varias tareas seguidas | Páralo. Revisa con `git diff` y descarta lo que sobre (`git restore <archivo>`). |
| Los tests llaman a la API o tardan mucho | No cumplen la constitución. Pídele que use dobles de prueba como en `docs/tests_sin_api.md`. |
| Mi proyecto no tiene tests | Normal. La primera tarea que toque lógica creará `tests/`. `pytest.ini` ya está preparado. |
| Se me ha acabado el cupo de Copilot | Sigue la fase a mano con la plantilla de `docs/plantillas/`: la spec y las tareas se pueden escribir sin agente. Es la mejor forma de ver qué aporta cada fase. |

## Para seguir aprendiendo
- [mouredev/hello-sdd](https://github.com/mouredev/hello-sdd): curso de SDD desde cero, con un proyecto completo.
- [GitHub Spec Kit](https://github.com/github/spec-kit): el toolkit de referencia (`/speckit.*`).
- [EARS, guía de Alistair Mavin](https://alistairmavin.com/ears/).
- [Prompt files en VS Code](https://code.visualstudio.com/docs/agent-customization/prompt-files).
