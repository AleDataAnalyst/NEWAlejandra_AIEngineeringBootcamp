# Guión / escaleta — Arrays y operaciones con NumPy

**Notebook de referencia:** `02_Arrays_y_operaciones_Numpy_SOLUTION.ipynb`  
**Duración objetivo:** ~5 minutos  
**Enfoque:** el alumno ve las celdas ya ejecutadas (o las ejecutas tú en directo); el peso está en **qué hace cada línea** y **por qué**, no en teclear desde cero.

---

## 0. Apertura (≈ 30 s)

- Saludo y título: arrays en NumPy y operaciones vectorizadas.
- Recordatorio breve: NumPy = arrays homogéneos + operaciones rápidas en C; hoy: crear, operar, agregar, trocear y condicionar sin bucles `for`.
- Indica que el notebook ya trae el código para seguir el hilo visual mientras explicas.

---

## 1. Crear arrays — celdas markdown + código (sección 1) (≈ 1 min)

**Qué mostrar:** celda con `v`, `w`, `z`.

**Ideas clave (guión oral):**

- `np.arange(0, 10, 2)` — “como `range` pero ya es array”; fin habitualmente **excluido** (comprueba con `v` en pantalla).
- `np.linspace(0, 1, 5)` — **número fijo de puntos** entre dos extremos; útil para gráficas o mallas; ambos extremos incluidos por defecto.
- `np.zeros((3, 4))` — forma `(filas, columnas)`; `shape` describe dimensiones.

**Frase de cierre de bloque:** “La idea es no construir a mano listas enormes: NumPy genera la forma que necesitas.”

---

## 2. Operaciones vectorizadas — sección 2 (≈ 45 s)

**Qué mostrar:** vector `a` y las cuatro salidas.

**Ideas clave:**

- `+`, `*`, `**` van **elemento a elemento**; no es multiplicación matricial (eso es otro tema / `@`).
- `np.sqrt` pide tipos adecuados: comenta el `.astype(float)` si aparece en la solución — “evitamos sorpresas con enteros”.

**Opcional (5 s):** un valor fuera de pantalla, por ejemplo “si sumo dos arrays de la misma forma, se suman posición a posición”.

---

## 3. Agregaciones y `axis` — sección 3 (≈ 50 s)

**Qué mostrar:** matriz `M` y las tres sumas.

**Ideas clave:**

- Sin `axis`: colapsas **todo** el array a un escalar.
- `axis=0`: “me quedo con **una fila** de resultados → agrego **verticalmente** → una suma **por columna**.”
- `axis=1`: “una suma **por fila**.”

**Truco mnemotécnico (opcional):** “el eje que **desaparece** es el que agregas.”

---

## 4. Indexado y slicing (1D) — sección 4 + **Otros ejemplos** (≈ 55 s)

**Parte fija (celda ya rellena):** repasa `a[0]`, `a[1:4]`, `a[::2]`, `a[-1]` — mismas reglas que listas, pero sobre array NumPy.

**Bloque “Otros ejemplos” (ya en el notebook SOLUTION / alumno; ~25–35 s):**

Código añadido bajo el comentario *Otros ejemplos de slicing* (ejecuta la celda y comenta la salida):

- `print("a[2:] …", a[2:])` — desde el índice 2 hasta el final.
- `print("a[:3] …", a[:3])` — los tres primeros elementos.
- `print("a[::-1] …", a[::-1])` — el array al revés (muy visual).
- `print("a[[0, 2, 4]] …", a[[0, 2, 4]])` — **indexación por lista** (no es un slice continuo): posiciones concretas en el orden pedido.

Opcional si da tiempo: el slicing a menudo devuelve una **vista** sobre el mismo bloque de memoria; no hace falta profundizar en 5 min salvo que el grupo ya venga de memoria compartida en NumPy.

---

## 5. `np.where` — sección 5 + **Otros ejemplos** (≈ 50 s)

**Parte fija:** condición booleana elemento a elemento; tres argumentos = “si / si no”, sin `if` por cada posición.

- Primer ejemplo: negativos sustituidos por 0 (“clip” de negativos).
- Segundo: elegir entre dos arrays `a` y `b` según `x > 0`.

**Bloque “Otros ejemplos” (ya en el notebook; ~20–30 s):**

Tras los dos `where` base, la celda incluye:

- `print(..., np.where(x == 0, 999, x))` — sustituir o marcar **ceros** (resto de posiciones sin cambio).
- `print(..., np.where(x > 5, 1, 0))` — **máscara 0/1** según umbral (base para clasificación binaria o filtros).

Si da tiempo en aula: comenta que `x` tiene la misma longitud que los arrays `a` y `b` del ejemplo anterior; con escalares en el segundo y tercer argumento, NumPy aplica **broadcasting** implícito.

---

## 6. Cierre (≈ 15 s)

- Resumen en una frase: crear → operar en bloque → resumir con `axis` → trocear → condicionar con `np.where`.
- Puente al siguiente vídeo o práctica: “en el workbook practicarás variantes; aquí hemos visto el mapa mental.”

---

## Notas para producción

- **Pantalla:** notebook con kernel ya arrancado; ejecuta celdas en orden o muestra salidas ya generadas.
- **Ritmo:** si te pasas de 5 min, recorta primero los “opcionales” de los bloques 2 y 3; los “Otros ejemplos” ya están en código en el SOLUTION y en el notebook del alumno (misma celda), así que basta con ejecutarlos y comentar la salida, sin improvisar en teclado salvo que quieras variantes extra.
- **Checklist antes de grabar:** `import numpy as np` ejecutado; fuente del notebook legible en zoom; una prueba de audio de 10 s.

---

## Tabla rápida de tiempos

| Bloque                         | Tiempo aprox. |
|--------------------------------|---------------|
| 0. Apertura                    | 30 s          |
| 1. Crear arrays                | 1 min         |
| 2. Operaciones vectorizadas    | 45 s          |
| 3. Agregaciones y `axis`       | 50 s          |
| 4. Indexado + otros ejemplos   | 55 s          |
| 5. `np.where` + otros ejemplos | 50 s          |
| 6. Cierre                      | 15 s          |
| **Total**                      | **~5 min 5 s** — ajusta recortando opcionales |

---

## Guión hablado (teleprompter)

Texto continuo para grabación. Entre corchetes, acciones en pantalla.

**[Pantalla: título del notebook o primera celda markdown]**

Hola. En este vídeo vamos a ver arrays en NumPy y operaciones vectorizadas: es decir, hacer muchas operaciones de una vez, sin ir posición a posición con un `for` en Python puro.

NumPy trabaja con arrays homogéneos —todos los elementos del mismo tipo— y delega el trabajo pesado en código optimizado en C. Hoy repasamos el mapa mental: cómo crear arrays, cómo operar sobre ellos, cómo resumirlos con sumas y medias y el parámetro `axis`, cómo trocearlos como si fueran listas, y cómo elegir valores según una condición con `np.where`.

**[Pantalla: sección 1, celda con `v`, `w`, `z`]**

Empezamos por crear arrays. Con `np.arange(0, 10, 2)` obtenemos valores espaciados de dos en dos, como un `range` de Python, pero ya como array. Ojo: el extremo superior suele ser exclusivo, igual que en `range`; por eso conviene mirar la salida y comprobar qué números salen exactamente.

`np.linspace(0, 1, 5)` es distinto: aquí fijas cuántos puntos quieres —cinco en este ejemplo— equiespaciados entre 0 y 1. Es muy habitual para ejes en gráficas o para muestrear un intervalo. Por defecto, los dos extremos entran en la lista de puntos.

Con `np.zeros((3, 4))` creamos una matriz de ceros: la tupla `(3, 4)` es la forma: tres filas y cuatro columnas. La propiedad `shape` te dice esas dimensiones. La idea es clara: no hace falta rellenar a mano listas enormes; NumPy te genera la forma que necesitas.

**[Pantalla: sección 2, vector `a`]**

Segundo bloque: operaciones vectorizadas. Si tienes un array `a` y haces `a + 10`, `a * 2` o `a ** 2`, cada operación se aplica elemento a elemento. Eso no es álgebra lineal estricta: no estamos multiplicando matrices salvo que uses operadores pensados para eso, como el arroba en versiones recientes de NumPy o `np.dot`. Aquí es simplemente: posición a posición, en paralelo.

Si usas algo como la raíz cuadrada con `np.sqrt`, a veces conviene pasar a coma flotante con algo como `astype(float)` para evitar avisos o comportamientos raros con enteros. Es un detalle práctico.

Y si sumas dos arrays de la misma forma, también se suman posición a posición. Esa es la filosofía de NumPy en el día a día.

**[Pantalla: sección 3, matriz `M` y las sumas]**

Tercero: agregaciones —sumas, medias, máximos— y el argumento `axis` en dos dimensiones. Si haces la suma de toda la matriz sin `axis`, colapsas todo y obtienes un solo número.

Si usas `axis=0`, estás diciendo: “recorre la dimensión cero”, que en una matriz son las filas. Visualmente, aplastas verticalmente: te quedas con una fila de resultados, es decir, una suma por columna.

Si usas `axis=1`, agregas a lo largo de las columnas dentro de cada fila: obtienes una suma por fila. Un truco que a mucha gente le ayuda: el eje que desaparece en el resultado es el que estás agregando.

**[Pantalla: sección 4, array `a` y el slicing ya escrito]**

Cuarto: indexado y slicing en una dimensión. Las reglas son las mismas que en listas: el primer elemento en el índice cero, un tramo con dos puntos como de uno a cuatro —recordando que el final puede ser exclusivo—, un salto con doble dos puntos, o el último elemento con índice menos uno. Todo eso, pero sobre un array de NumPy, que luego podrá ser parte de cálculos numéricos grandes.

**[Pantalla: misma celda; bloque “Otros ejemplos de slicing” ya escrito]**

En la misma celda, debajo del comentario de ampliación, tienes cuatro `print` más: `a[2:]` desde el índice dos hasta el final; `a[:3]` los tres primeros; `a[::-1]` que da la vuelta al vector, muy didáctico en pantalla; y `a[[0, 2, 4]]`, que no es un slice continuo sino una lista de posiciones en ese orden. Ejecuta y lee la salida con los alumnos: con eso cierras la idea de flexibilidad del indexado en 1D.

**[Pantalla: sección 5, `x`, `clip_neg`, y el `where` con `a` y `b`]**

Último bloque importante: `np.where`. La firma es: condición, valor si es verdad, valor si es falso —y se evalúa elemento a elemento, sin escribir un `if` por cada posición.

En el primer ejemplo, donde los negativos pasan a cero, estás haciendo una especie de recorte de la parte negativa. En el segundo, eliges entre dos arrays, `a` y `b`, según si `x` es positivo o no: donde la condición es cierta, coges un array; donde es falsa, el otro. Todo vectorizado.

**[Pantalla: bloque “Otros ejemplos con np.where” ya en la celda]**

La celda termina con dos líneas más: una que hace `np.where(x == 0, 999, x)` para ver cómo sustituyes o marcas los ceros, y otra con `np.where(x > 5, 1, 0)` que devuelve unos y ceros según un umbral, es decir una máscara sencilla. Ejecuta y relaciona cada posición de `x` con lo que sale: así conectas `where` con tareas típicas de limpieza o clasificación rudimentaria.

**[Pantalla: cierre o vuelta al índice del notebook]**

En resumen: crear con `arange`, `linspace`, `zeros`…; operar en bloque sin bucles; resumir con funciones como `sum` y con `axis` bien entendido; trocear como en listas, y condicionar con `np.where`.

En el workbook practicarás variantes; aquí hemos visto el mapa mental para que, cuando leas código de NumPy, sepas en qué cajón meter cada pieza. Hasta el siguiente vídeo.
