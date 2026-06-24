![Cabecera](../../../assets/cabecera_gemini.png)

# Modularización de proyectos - Ejemplo

Demo en Python de un **sistema pequeño pero bien organizado**: validar registros de tareas, decidir si son correctos, guardar en sesión solo lo válido y consultar un historial. **No usa API de IA**; el objetivo es la **estructura del código** antes de conectar un LLM.

> **Idea clave:** no se trata de “tener muchos archivos”. Se trata de que **cada pieza tenga un trabajo claro** y puedas cambiar una sin romper todo.

---

## Qué vas a aprender

- Separar un script en módulos: `config`, `prompts`, `logic`, `state`, `main`.
- Entender **separación de responsabilidades** (reglas, textos, decisiones, memoria, orquestación).
- Devolver respuestas estructuradas (`status`, `mensaje`, `data`) en lugar de mezclar lógica y `print`.
- Mantener un **historial en memoria** y guardar **solo** registros que pasaron validación.
- Saber **quién importa a quién** sin dependencias circulares.

---

## Historia del dominio (de qué va la demo)

Imagina un asistente interno que recibe **tickets de trabajo** para tareas de IA futuras:

- **summary** — resumir texto  
- **translate** — traducir  
- **qa** — preguntas y respuestas  

Cada registro tiene:

```python
{
    "nombre": "Ana",
    "codigo": "TKT-1234",       # formato TKT-####
    "tipo": "summary",          # summary | translate | qa
    "prioridad": 3,             # entero del 1 al 5
}
```

El programa **no hace** aún esas tareas con un modelo; solo valida, responde “qué haríamos” y guarda los válidos en historial.

---

## Estructura del repositorio

```text
.
├── README.md       ← este documento
├── config.py       ← reglas fijas (límites, listas válidas, regex)
├── prompts.py      ← mensajes y plantillas de texto
├── logic.py        ← validar + procesar (sin print)
├── state.py        ← historial y operaciones de sesión
└── main.py         ← orquestación y salida por consola
```

---

## Qué hace cada archivo

### `config.py` — reglas del juego

Constantes que casi no cambian en tiempo de ejecución:

- `VALID_TIPOS`, `PRIORIDAD_MIN`, `PRIORIDAD_MAX`
- `PATRON_CODIGO` (regex `TKT-1234`)
- `MODEL` (placeholder para cuando conectes una API)

**Si mañana cambias el rango de prioridad o los tipos permitidos, tocas aquí.**

### `prompts.py` — textos

Mensajes y plantillas (`MSG_ERROR_INPUT`, `PLANTILLA_TAREA`, etc.).

**Si cambias el tono de un error o un prompt, tocas aquí — no busques strings repartidos por `logic.py`.**

### `logic.py` — cerebro (sin imprimir)

- `validar_registro(datos)` → lista de errores (vacía = OK)
- `procesar_registro(datos)` → dict con `status: "ok"` o `"error"`
- Helpers `respuesta_ok` / `respuesta_error`

**Regla:** recibe datos, devuelve dicts. **Sin `print`.** Así puedes testear o reutilizar desde otro sitio.

### `state.py` — memoria de la sesión

- `inicializar_estado()` → `historial`, `contadores`, `ultima_accion`
- `guardar_si_ok(...)` → `append` **solo** si `resultado["status"] == "ok"`
- `listar_historial`, `filtrar_por_tipo`, `contar_por_tipo`, `ultimos_n`, etc.

**Regla:** `logic` decide; `state` recuerda. No metas validaciones largas en `state.py`.

### `main.py` — director de orquesta

Importa módulos, ejecuta el flujo, **imprime** resultados (`imprimir_respuesta`).

**Regla:** no redefinas `VALID_TIPOS` ni `validar_registro` aquí.

---

## Flujo del programa (orden importante)

```text
  datos (dict)
       │
       ▼
  logic.procesar_registro()  ──► valida + devuelve { status, mensaje, data }
       │
       ├── status == "error"  ──► main imprime errores (NO se guarda)
       │
       └── status == "ok"     ──► main imprime OK
                │
                ▼
         state.guardar_si_ok()  ──► historial.append(...)
                │
                ▼
         al final: listar / filtrar / contar / ultimos_n
```

En `main.py`, los tres casos de prueba son:

1. Ana — válida (`summary`, prioridad 3)  
2. Luis — válida (`qa`, prioridad 5)  
3. Registro vacío / tipo incorrecto — **inválido** (no entra en historial)

---

## Quién puede importar a quién

```text
main.py  ──►  logic.py, state.py, prompts.py (opcional)

logic.py ──►  config.py, prompts.py

state.py ──►  config.py (opcional; en esta demo no es obligatorio)

config.py, prompts.py  ──►  no importan logic ni main
```

Evita que `logic.py` importe `main.py` (dependencia circular).

---

## Contrato de respuesta

Toda decisión de negocio devuelve un dict homogéneo:

```python
{
  "status": "ok" | "error",
  "mensaje": "...",
  "data": { ... }   # en error: {"errores": ["...", ...]}
}
```

`main.py` solo **muestra** ese dict; no reescribe las reglas de validación.

---

## Requisitos

- **Python 3.10+** (se usan anotaciones como `dict | None`).
- Terminal (PowerShell, cmd, Git Bash, macOS Terminal, etc.).
- **No** hace falta instalar paquetes externos (`pip install` no necesario para esta demo).

Comprueba la versión:

```bash
python --version
# o en Windows:
py -3 --version
```

---

## Cómo ejecutarlo

Clona el repo y abre la terminal **en la carpeta raíz del proyecto** (donde está `main.py`):

```bash
python main.py
```

Windows, si `python` no funciona:

```bash
py -3 main.py
```

### Error frecuente: `ModuleNotFoundError: No module named 'logic'`

Significa que ejecutaste el comando **desde otra carpeta**. El directorio de trabajo debe ser el que contiene `logic.py` y `main.py` juntos.

---

## Salida esperada

Deberías ver algo como:

```text
[OK] Registro válido
  → Tarea 'summary' con prioridad 3.
[OK] Registro válido
  → Tarea 'qa' con prioridad 5.
[ERROR] Input inválido
 - Nombre inválido: no puede estar vacío.
 - Tipo inválido. Usa una de: ['summary', 'translate', 'qa']
 - Prioridad inválida: debe ser un entero 1-5.

--- Historial (solo OK) ---
  1. Ana · summary · prioridad 3
  2. Luis · qa · prioridad 5

--- Solo tipo 'summary' ---
  Ana TKT-1234

--- Contadores por tipo --- {'summary': 1, 'qa': 1}
--- Últimos 2 (borrador de contexto) --- [...]
```

Si tu salida coincide en **dos OK, un ERROR y historial con 2 entradas**, el proyecto está bien configurado.

---

## Orden recomendado al explorar el código

1. Lee la **estructura** y la tabla “qué hace cada archivo” (arriba).  
2. Abre `config.py` y `prompts.py` — datos fijos y textos.  
3. Abre `logic.py` — validación y respuestas (sin `print`).  
4. Abre `state.py` — historial y `guardar_si_ok`.  
5. Abre `main.py` y ejecuta `python main.py`.  
6. Compara tu terminal con la **salida esperada** y prueba los **experimentos** siguientes.

---

## Experimentos sugeridos

1. En `config.py`, cambia `PRIORIDAD_MAX` a `10` y añade un caso con `prioridad: 8` en `main.py`.  
2. En `prompts.py`, cambia `MSG_ERROR_INPUT` y vuelve a ejecutar.  
3. Añade un cuarto registro inválido (código `ABC-1`) y comprueba que no entra en historial.  
4. En `state.py`, llama a `vaciar_historial(state)` al final de `main` y observa contadores vacíos.  

---

## Tabla rápida: “quiero cambiar X, ¿dónde?”

| Quiero cambiar… | Archivo |
|-----------------|---------|
| Tipos permitidos o rango de prioridad | `config.py` |
| Texto de error o plantilla de tarea | `prompts.py` |
| Regla “nombre obligatorio” o formato código | `logic.py` |
| Qué se guarda en historial | `state.py` (`guardar_si_ok`) |
| Cómo se ve la consola | `main.py` |
