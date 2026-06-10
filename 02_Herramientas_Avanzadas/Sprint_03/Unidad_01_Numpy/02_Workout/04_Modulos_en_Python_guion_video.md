# Guión / escaleta — Módulos en Python

**Notebook de referencia:** `04_Modulos_en_Python_SOLUTION.ipynb`  
**Duración objetivo:** ~5 minutos  
**Enfoque:** importar y reutilizar código (`import`, `from … import`, alias `as`), módulos propios (`mini_stats`, `saludos`), `__name__` y docstrings. Donde pone «Otros ejemplos», ejecuta la celda y comenta la salida (el código extra ya está en el notebook de solución).

---

## 0. Apertura (≈ 25 s)

- Saludo y título: **módulos** en Python — organizar y reutilizar código sin copiar y pegar.
- Idea central: la librería estándar, paquetes como NumPy y tus propios `.py` se **importan** con nombres claros.
- Objetivos del intro del notebook: `import` / `from`, alias, `__name__`, y (si lo mencionas en una frase) **`importlib.reload`** cuando editas un `.py` en sesiones largas en Jupyter — en este workout no hay celda de demo de `reload`, pero encaja con el texto de objetivos.

**Frase de cierre:** «Hoy conectamos el notebook con código que ya vive en archivos `.py`.»

---

## 1. Preparación (≈ 15 s)

**Qué decir:** en la carpeta `02_Workout` ya existen `mini_stats.py` y `saludos.py`; el ejercicio es **importarlos** desde el notebook, no reimplementarlos.

---

## 2. Ejercicio 1 — `math` (módulo estándar) (≈ 45 s)

**Qué mostrar:** `import math`, `math.pi`, `math.sqrt(81)`, `dir(math)[:15]`.

**Ideas clave:**

- `import math` carga el **módulo**; accedes con el prefijo `math.`.
- `dir(math)` lista nombres definidos en el módulo; el slice `[:15]` solo acorta la salida para el vídeo.

**Bloque «Otros ejemplos» (ya en solución; ejecuta y comenta ~20 s):**

- `from math import pi as PI, sqrt as raiz_cuadrada` — import **selectivo** con **alias** de símbolo (útil si quieres nombres cortos o evitar choques de nombres).

---

## 3. Ejercicio 2 — NumPy: alias y `from` (≈ 50 s)

**Qué mostrar:** `import numpy as np`, `from numpy import array`, creación de `a` y `b`, `dtype`.

**Ideas clave:**

- `as np` es la convención de la comunidad para NumPy.
- `from numpy import array` trae **solo** `array` al espacio de nombres actual: puedes escribir `array([...])` sin prefijo.
- Mismo tipo lógico de datos (`ndarray`); `dtype` confirma el tipo de los elementos.

**Truco oral:** «`import paquete as alias` reduce teclado; `from … import` trae nombres concretos — útil, pero no abuses o el lector no sabrá de dónde sale cada función.»

---

## 4. Ejercicio 3 — `mini_stats` (módulo propio) (≈ 55 s)

**Qué mostrar:** `import mini_stats`, lista `nums`, `mini_stats.media`, `mini_stats.desv_std`, `mini_stats.__name__`.

**Ideas clave:**

- Un `.py` en el path se importa como módulo; el nombre suele ser el del archivo (sin `.py`).
- `__name__` como atributo del módulo importado suele ser el string `'mini_stats'`.

**Pregunta Markdown (`if __name__ == "__main__"`):**

- Ese bloque se ejecuta **solo** si corres el archivo con `python mini_stats.py`, no cuando haces `import mini_stats` desde otro sitio — sirve para demos, tests rápidos o un `main()` sin “ensuciar” quien te importa.

---

## 5. Ejercicio 4 — `saludos` y docstrings (≈ 50 s)

**Qué mostrar:** `import saludos`, `saluda`, `despide`, `saludos.saluda.__doc__`.

**Ideas clave:**

- Las **docstrings** documentan la función; `.__doc__` las muestra como texto.
- `help(saludos.saluda)` (si lo enseñas en el bloque extra) abre la ayuda interactiva con más contexto.

**Bloque «Otros ejemplos» (ya en solución; ~15 s):**

- Una línea con `help(saludos.saluda)` para contrastar con `__doc__`.

---

## 6. Cierre (≈ 20 s)

- Resumen: `import` vs `from`, alias, módulos propios, `__name__` para no ejecutar demos al importar, y docstrings para documentar.
- **Opcional (10 s):** si editas un `.py` mientras Jupyter sigue abierto, a veces hace falta `from importlib import reload` y `reload(modulo)` para ver cambios sin reiniciar el kernel.

**Frase final:** «Modularizar es la base para que tu proyecto crezca sin volverse ilegible.»

---

## Variante «menos de 5 minutos» (~4 min)

Recorta o acelera:

- Apertura y preparación en **una sola frase** (~15 s).
- En ej. 1, **omite** el bloque «Otros ejemplos» de `from math import … as …`.
- En ej. 2, **solo** alias `np` + una línea sobre `from numpy import array` (sin insistir en convenciones).
- En ej. 3, resume `__name__` en **dos frases** sin leer el párrafo entero del markdown.
- En ej. 4, **solo** `__doc__` (sin `help`).
- Cierre sin mencionar `reload`.

---

## Notas de producción

- **Kernel:** Python con `numpy` instalado; ejecutar desde la carpeta del notebook para que encuentre `mini_stats.py` y `saludos.py`.
- **Zoom:** celdas cortas; zoom 125–150 % si grabas pantalla pequeña.
- **Errores típicos:** `ModuleNotFoundError` si el kernel no tiene el cwd correcto; `ImportError` si falta NumPy.

---

## Guión hablado (teleprompter, ~5 min)

Hola. En esta sesión hablamos de **módulos en Python**: cómo traer a tu notebook funciones y constantes que ya están escritas en otros sitios — la librería estándar, librerías como NumPy, o tus propios archivos `.py`.

En esta carpeta ya tienes dos módulos listos, `mini_stats` y `saludos`. El objetivo es **importarlos y usarlos**, no volver a escribir esa lógica aquí.

Empezamos con el módulo estándar **`math`**. Con `import math` cargas el módulo y lo usas con el prefijo `math`: por ejemplo `math.pi` y `math.sqrt(81)`. Si quieres explorar qué trae el módulo, `dir(math)` lista nombres; en el notebook solo mostramos las primeras entradas para que no sea un scroll infinito.

En la solución hay un bloque extra: puedes hacer un import selectivo con alias de símbolo, por ejemplo importar `pi` como `PI` y `sqrt` como `raiz_cuadrada`. Así ves que no siempre hace falta escribir `math.` delante de todo.

Segundo bloque: **NumPy**. Lo habitual es `import numpy as np` y crear arrays con `np.array`. También puedes hacer `from numpy import array` y entonces llamas directamente a `array([...])`. Fíjate en los `dtype` de `a` y `b`: son arrays de NumPy, no listas Python.

Tercer bloque: un módulo **propio**, `mini_stats`. Con `import mini_stats` usas `mini_stats.media` y `mini_stats.desv_std` sobre una lista de números. Si imprimes `mini_stats.__name__`, verás el nombre del módulo tal como lo ve Python.

La pregunta del notebook es importante: ¿para qué sirve `if __name__ == "__main__"`? Sirve para que un trozo de código se ejecute **solo** cuando lanzas ese archivo como programa principal, por ejemplo con `python mini_stats.py`, y **no** cuando alguien hace `import mini_stats`. Así puedes dejar pruebas o una demo al final del archivo sin que se ejecuten cada vez que te importan.

Último bloque: **`saludos`**. Importas el módulo y llamas a `saludos.saluda` y `saludos.despide`. Para leer la documentación de la función, `saludos.saluda.__doc__` muestra la docstring. En la solución también añadimos `help(saludos.saluda)` para que veas la ayuda interactiva.

Cierro con dos ideas. Primero: combina `import` largo para claridad y `from … import` cuando quieras nombres cortos en un script pequeño, pero no abuses para no perder el rastro de dónde viene cada función. Segundo: en objetivos del notebook aparece **recargar** módulos con `reload` de `importlib` cuando cambias un `.py` en una sesión larga; no está en una celda de este workout, pero es el truco típico en Jupyter cuando editas código importado.

Eso es todo por hoy: ya sabes enlazar tu notebook con módulos estándar, externos y propios. Nos vemos en el siguiente vídeo.
