# 📘 SQL y Bases de Datos

En este contenido damos el salto de trabajar con datos en memoria (listas, pandas) a interactuar con **bases de datos relacionales**: cómo conectar Python a una base SQLite, escribir queries SQL, combinar tablas con JOINs y gestionar bases de datos (crear, insertar, actualizar y borrar).

El contenido se organiza en tres bloques que se construyen uno sobre otro:

---

## 🧩 Bloque 1 — Workout: fundamentos de SQL

📁 [`01_Workout/`](./01_Workout/)

> **De Python a SQL:** conexión y cursores, primeras queries, filtros con WHERE, agregación y agrupación, los distintos tipos de JOIN, y gestión de bases de datos (crear, insertar, actualizar, borrar).

| # | Notebook | Qué aprenderás |
|---|----------|-----------------|
| 1 | [03_Conectividad_Cursores.ipynb](./01_Workout/01_Introducción_a_SQL/03_Conectividad_Cursores.ipynb) | Conectar Python a una base de datos SQLite, crear un cursor y ejecutar queries (`execute`, `fetchone`, `fetchmany`, `fetchall`), y convertir resultados a pandas. |
| 2 | [04_Modelo_Datos_Primeras_Queries.ipynb](./01_Workout/02_Queries/04_Modelo_Datos_Primeras_Queries.ipynb) | Tablas y schema, modelo de datos relacional, primeras queries con `SELECT`, selección de campos, `LIMIT` y `DISTINCT`. |
| 3 | [05_WHERE.ipynb](./01_Workout/02_Queries/05_WHERE.ipynb) | Filtros con `WHERE`: condiciones numéricas, sobre texto, y combinaciones booleanas. |
| 4 | [06_Agregacion_Agrupacion.ipynb](./01_Workout/02_Queries/06_Agregacion_Agrupacion.ipynb) | `ORDER BY`, funciones de agregación y agrupación con `GROUP BY`. |
| 5 | [07_Joins_Teoria.ipynb](./01_Workout/02_Queries/07_Joins_Teoria.ipynb) | Teoría de JOINs: LEFT, RIGHT, INNER, FULL OUTER y otros tipos. |
| 6 | [08_Join_Ejemplos_LEFT.ipynb](./01_Workout/02_Queries/08_Join_Ejemplos_LEFT.ipynb) | Ejemplos prácticos de LEFT JOIN, creación de VIEW/DROP, y errores comunes. |
| 7 | [09_Joins_Ejemplos_II.ipynb](./01_Workout/02_Queries/09_Joins_Ejemplos_II.ipynb) | Ejemplos prácticos de RIGHT JOIN, INNER JOIN y FULL JOIN. |
| 8 | [10_Gestion_BD.ipynb](./01_Workout/03_Gestión_de_Bases_de_Datos/10_Gestion_BD.ipynb) | Creación de bases de datos y tablas, `INSERT`. |
| 9 | [11_Gestion_BDs_II.ipynb](./01_Workout/03_Gestión_de_Bases_de_Datos/11_Gestion_BDs_II.ipynb) | `UPDATE`, `DELETE`, borrado de columnas y de tablas. |

Índice detallado: [`01_Workout/README.md`](./01_Workout/README.md)

---

## 🏋️ Bloque 2 — Ejercicios

📁 [`02_Ejercicios/`](./02_Ejercicios/)

> **Practicar sobre datos reales:** consultas, joins y gestión de bases de datos sobre la base Chinook (tienda de música) y un dataset de Pokémon.

| Notebook | Qué practica |
|----------|----------------|
| [12_Ejercicio_Consultas_SQL.ipynb](./02_Ejercicios/12_Ejercicio_Consultas_SQL.ipynb) | `SELECT`, `WHERE`, `LIMIT`/`DISTINCT`, agregaciones y agrupaciones. |
| [13_Ejercicio_Joins_Merge.ipynb](./02_Ejercicios/13_Ejercicio_Joins_Merge.ipynb) | LEFT, RIGHT e INNER JOIN, comparando con su equivalente en pandas (`merge`). |
| [14_Ejercicio_Gestion_BDs.ipynb](./02_Ejercicios/14_Ejercicio_Gestion_BDs.ipynb) | Creación, inserción, actualización y borrado sobre bases de datos. |
| [18_Practica_Chinook_SQL.ipynb](./02_Ejercicios/18_Practica_Chinook_SQL.ipynb) | *(Muy recomendado, no obligatorio)* Repaso general de todos los conceptos de SQL vistos, sobre la base Chinook. |

> 💡 Todos los notebooks de Workout y Ejercicios tienen su versión `_SOL` con las soluciones resueltas — hay mucho donde practicar por vuestra cuenta.

Índice detallado: [`02_Ejercicios/README.md`](./02_Ejercicios/README.md)

---

## 🎯 Práctica Obligatoria

📁 [`Team_Challenges/TC_03_SQL/03_Practica_Obligatoria/`](../../Team_Challenges/TC_03_SQL/03_Practica_Obligatoria/)

> Práctica integradora dividida en dos partes, dentro del Team Challenge de SQL.

---

## ⚙️ Convenciones

- Base de datos de referencia: **Chinook** (`data/chinook.db`), una base SQLite de ejemplo con datos de una tienda de música.
- Conexión con `sqlite3` (librería estándar de Python) + `cursor_bootcamp` como cursor de trabajo.
- Los notebooks funcionan en JupyterHub siempre que la carpeta `data/` viaje junto al notebook (ruta relativa `data/chinook.db`).
