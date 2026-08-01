# 🏋️ Workout — SQL y Bases de Datos

Recorrido guiado por SQL desde Python: conectar, consultar, filtrar, agregar, combinar tablas con JOINs y gestionar bases de datos.

---

## 📂 01_Introducción_a_SQL

| Notebook | Qué aprenderás |
|----------|-----------------|
| [03_Conectividad_Cursores.ipynb](./01_Introducción_a_SQL/03_Conectividad_Cursores.ipynb) | Conexión a una base SQLite con `sqlite3`, creación de un cursor, ejecución de queries (`execute`) y recuperación de resultados (`fetchone`, `fetchmany`, `fetchall`). Conversión de la salida a un DataFrame de pandas. |

---

## 📂 02_Queries

| Notebook | Qué aprenderás |
|----------|-----------------|
| [04_Modelo_Datos_Primeras_Queries.ipynb](./02_Queries/04_Modelo_Datos_Primeras_Queries.ipynb) | Tablas y schema de una base relacional, primeras queries con `SELECT`, selección de campos concretos, `LIMIT` y `DISTINCT`. |
| [05_WHERE.ipynb](./02_Queries/05_WHERE.ipynb) | Filtros con `WHERE`: condiciones numéricas, sobre campos de texto, filtros varios y combinaciones booleanas de condiciones. |
| [06_Agregacion_Agrupacion.ipynb](./02_Queries/06_Agregacion_Agrupacion.ipynb) | Ordenación con `ORDER BY`, funciones de agregación y agrupación de resultados con `GROUP BY`. |
| [07_Joins_Teoria.ipynb](./02_Queries/07_Joins_Teoria.ipynb) | Teoría de JOINs: LEFT (outer), RIGHT (outer), INNER, FULL OUTER y otros tipos. Cuándo usar cada uno. |
| [08_Join_Ejemplos_LEFT.ipynb](./02_Queries/08_Join_Ejemplos_LEFT.ipynb) | Ejemplos prácticos de LEFT JOIN, creación de VIEW y DROP, errores comunes al combinar tablas. |
| [09_Joins_Ejemplos_II.ipynb](./02_Queries/09_Joins_Ejemplos_II.ipynb) | Ejemplos prácticos de RIGHT JOIN, INNER JOIN y FULL JOIN. |

---

## 📂 03_Gestión_de_Bases_de_Datos

| Notebook | Qué aprenderás |
|----------|-----------------|
| [10_Gestion_BD.ipynb](./03_Gestión_de_Bases_de_Datos/10_Gestion_BD.ipynb) | Creación de bases de datos y tablas, inserción de registros con `INSERT`. |
| [11_Gestion_BDs_II.ipynb](./03_Gestión_de_Bases_de_Datos/11_Gestion_BDs_II.ipynb) | Actualización (`UPDATE`) y borrado (`DELETE`) de registros, borrado de columnas y de tablas completas. |

---

## 📎 Otros recursos

- `data/chinook.db` y `data/chinook_joins.db` — bases de datos SQLite de ejemplo (tienda de música) usadas en los notebooks de JOINs.
- `ppts/Procesado_Datos_Internos_P01_BBDD_Relacionales.pdf` y `ppts/Procesado_Datos_Internos_P02_SQL.pdf` — slides de apoyo teórico.
