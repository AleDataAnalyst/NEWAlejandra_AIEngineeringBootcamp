# Guión / escaleta — Conversión de listas a arrays (NumPy)

**Notebook de referencia:** `03_Conversion_listas_a_arrays_SOLUTION.ipynb`  
**Duración objetivo:** ~5 minutos  
**Enfoque:** celdas ya rellenas; el vídeo explica **qué hace cada línea** y **por qué** importa el tipo de dato y la homogeneidad. Donde pone «Otros ejemplos», ejecuta la celda y comenta la salida (el código extra ya está en el notebook).

---

## 0. Apertura (≈ 25 s)

- Saludo y título: de **listas** Python a **`ndarray`** de NumPy.
- Idea central: los datos suelen llegar como listas; NumPy los mete en un bloque de memoria homogéneo para ir rápido.
- Objetivos del vídeo: `np.array` 1D y 2D, `dtype` / `astype`, listas heterogéneas con cuidado, y `np.asarray` frente a `np.array`.

**Frase de cierre:** «Hoy vemos el puente entre “tengo una lista” y “tengo un array listo para calcular”.»

---

## 1. Lista 1D → array (sección 1) (≈ 35 s)

**Qué mostrar:** celda con `datos` y `arr = np.array(datos)`.

**Ideas clave:**

- `np.array` **copia** el contenido (en general) a un nuevo `ndarray`.
- `print(arr, arr.dtype)` — mismo orden que la lista; `dtype` te dice el tipo **unificado** que eligió NumPy (aquí suele ser `int64` según plataforma).

**Opcional (5 s):** «Si la lista es enorme, igual quieres `dtype` explícito para ahorrar memoria; lo vemos en el siguiente bloque.»

---

## 2. Lista de listas → matriz 2D (sección 2) (≈ 40 s)

**Qué mostrar:** `tabla`, `M`, `shape`, `ndim`.

**Ideas clave:**

- Cada **lista interior = una fila** cuando la estructura es rectangular.
- `shape` = `(filas, columnas)`; `ndim` = número de dimensiones (2 = matriz).

**Truco oral:** «Piensa en la lista de listas como las filas de una tabla en Excel.»

---

## 3. `dtype` y `astype` (sección 3) (≈ 55 s)

**Qué mostrar:** `enteros`, `flotantes`, `de_nuevo_enteros`.

**Ideas clave:**

- Al crear: `dtype=np.int32` **fija** el tipo.
- `enteros.astype(np.float64)` devuelve un **nuevo** array en float; el original sigue siendo entero.
- `np.array([1.7, 2.2, 3.9]).astype(np.int32)` — **truncado** hacia cero (no redondeo bancario); avisa de “pérdida de información”.

**Frase de cierre:** «`astype` es útil, pero tú eres responsable de lo que se pierde al convertir.»

---

## 4. Listas heterogéneas (sección 4 + **Otros ejemplos**) (≈ 1 min)

**Parte fija:** `mezcla = np.array([1, 2, "tres"])`.

- NumPy **promueve** a un tipo común: aquí todo acaba como **strings** Unicode (`<U…>`).
- Si todo fuera numérico mezclando int y float, promovería a float.

**Bloque “Otros ejemplos” (ya en el notebook; ejecuta y comenta ~25–35 s):**

- `nums_mezcla = np.array([1, 2, 3.5])` — int + float → **todo float** (reglas de promoción).
- `bool_int = np.array([True, False, 2])` — bool se interpreta como 0/1 y convive con int.
- `M_tipo = np.array([[1, 2], [3.0, 4]])` — en 2D, un solo float en la tabla hace que **toda la matriz** sea float.

**Mensaje pedagógico:** «Para cálculo numérico, evita `dtype=object` y mezclas raras; limpia datos antes o fuerza `dtype` con criterio.»

---

## 5. `np.asarray` vs `np.array` (sección 5) (≈ 45 s)

**Qué mostrar:** `x`, `y = np.asarray(x)`, `z = np.array(x)`, `np.shares_memory`.

**Ideas clave:**

- `np.asarray(x)`: si `x` **ya** es `ndarray`, **no copia** (misma memoria) — `shares_memory` True con `y`.
- `np.array(x)`: en la práctica del curso, **suele** crear copia — `shares_memory` False con `z`.
- Útil cuando pasas datos a una función que no quieres duplicar sin necesidad.

**Opcional (10 s):** «Si modificas elementos de `y`, estás tocando `x`; con `z` no.»

---

## 6. Cierre (≈ 15 s)

- Resumen: lista → `np.array`; cuidado con **tipos** y **heterogeneidad**; `astype` con ojo; `asarray` para evitar copias cuando el origen ya es array.
- Puente: «En el siguiente workout seguiremos con operaciones o integración con el resto del curso.»

---

## Notas para producción

- Resolución: mostrar `dtype` en pantalla grande; los alumnos suelen perderse en `<U21>` vs `float64`.
- Los «Otros ejemplos» de la sección 4 están **precodificados**; no hace falta improvisar en vivo salvo que quieras un caso más (por ejemplo `dtype=object` con listas anidadas: solo si el grupo es avanzado).
- Duración real: si te pasas de 5 min, acorta la sección 3 o el monólogo de cierre.

---

## Guión hablado (teleprompter)

Hola. En este vídeo corto vamos a ver cómo pasar **datos en listas** de Python a **arrays de NumPy**, y por qué eso importa para calcular rápido y sin sorpresas.

Abre el notebook de solución: ya viene el código para que podamos **ejecutar y mirar la salida**, sin perder tiempo tecleando.

**[Sección 1 — lista 1D]**

Primero, una lista simple: diez, veinte, treinta, cuarenta. Con `np.array(datos)` creamos un `ndarray` unidimensional. Fíjate en el `print`: ves los valores y el `dtype`. NumPy ha elegido un tipo **único** para todo el vector, porque internamente el array es **homogéneo**: todas las celdas del mismo tipo, alineadas en memoria. Esa homogeneidad es la base de la velocidad frente a listas Python.

**[Sección 2 — 2D]**

Ahora una **lista de listas**: cada lista interior la vamos a leer como una **fila**. `np.array(tabla)` nos da una matriz dos dimensiones. El `shape` te dice filas por columnas, y `ndim` confirma que estamos en 2D. Visualmente: es como pegar filas una debajo de otra.

**[Sección 3 — dtype y astype]**

Aquí forzamos enteros con `dtype=int32` y luego hacemos `astype` a `float64`. Lo importante: `astype` **no “convierte en sitio”** el array original de forma mágica: te devuelve una **representación nueva** en otro tipo; el array de enteros sigue siendo entero. Luego creamos floats y los pasamos a `int32`: verás **truncado**, no redondeo al alza. Eso es una fuente típica de bugs si alguien espera redondeo “matemático”. Coméntalo con los alumnos: antes de castear, piensa qué significa perder decimales.

**[Sección 4 — heterogéneos + Otros ejemplos]**

El caso `[1, 2, "tres"]` es deliberadamente “malo” para cálculo numérico: NumPy **sube** todo a un tipo común, y aquí acaba en texto. Ya no puedes sumar como si fueran números sin pasos extra. Por eso en datos reales conviene **limpiar** o **parsear** antes.

En la misma celda, debajo del comentario de ampliación, hay **otros ejemplos** ya listos. Ejecuta y comenta: cuando mezclas enteros y un float, todo el array pasa a **float** — es la regla de promoción. Si mezclas booleanos y un entero, obtienes un array **numérico** donde `True` y `False` se interpretan como uno y cero. Y en dos dimensiones, basta un `3.0` para que **toda la matriz** sea float: una sola celda “flota” y arrastra el tipo de toda la tabla. Con eso se entiende por qué conviene ser explícito con `dtype` cuando importa la memoria o la precisión.

**[Sección 5 — asarray vs array]**

Por último, la diferencia práctica entre `np.asarray` y `np.array`. Creamos `x`, luego `y = np.asarray(x)` y `z = np.array(x)`. Con `shares_memory` comprobamos: `x` e `y` **comparten memoria**; `x` y `z` no. Traducción didáctica: `asarray` intenta **reutilizar** el buffer si ya era un ndarray; `np.array` en este patrón suele **duplicar**. Eso importa si pasas arrays grandes a funciones y quieres evitar copias innecesarias — pero ojo: si compartes memoria, un cambio en una vista afecta al original.

**[Cierre]**

En resumen: `np.array` te lleva de listas a arrays homogéneos; el **`dtype`** cuenta; las **mezclas raras** te pueden convertir todo a texto u `object`; y **`asarray`** vs **`array`** controla si copias o no cuando el origen ya es ndarray. Con eso estás listo para el resto del workout. Nos vemos en el siguiente.
