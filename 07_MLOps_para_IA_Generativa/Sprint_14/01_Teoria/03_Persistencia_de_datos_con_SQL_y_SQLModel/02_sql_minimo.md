![Cabecera](../../../../06_AI_Agents_Engineering/Sprint_11/assets/cabecera_thebridge.png)

# SQL mínimo (lo que necesitáis entender)

SQL es el lenguaje para hablar con bases de datos **relacionales** (tablas con filas y columnas).

En este sprint casi no escribís SQL a mano: **SQLModel** lo genera. Aun así conviene saber qué hay debajo.

> **Mínimo para practicar:** tablas, PK, FK, `SELECT` / `INSERT`. El resto es profundización.

Recursos: [SQL — w3schools](https://www.w3schools.com/sql/) · [SQL Tutorial](https://www.sqltutorial.org/)

---

## 1) Tabla = hojas de cálculo con reglas

Pensad en Excel, pero con tipos y claves:

| id (PK) | role | content | thread_id (FK) |
|---------|------|---------|----------------|
| 1 | user | ¿Cómo está el NO2? | demo-aire |
| 2 | assistant | Según la guía… | demo-aire |

- Cada **fila** = un registro (un mensaje).
- Cada **columna** = un campo con tipo (`TEXT`, `INTEGER`, …).

---

## 2) PRIMARY KEY y FOREIGN KEY

**PRIMARY KEY (PK):** identifica una fila de forma única.

- En `conversation`: el `id` puede ser el mismo string que el `thread_id` de la API (`"demo-aire"`).
- En `message`: suele ser un entero **autoincremental** (la DB asigna 1, 2, 3…).

**FOREIGN KEY (FK):** apunta a la PK de otra tabla.

```text
message.thread_id  →  conversation.id
```

Así un hilo tiene muchos mensajes (relación 1–N).

---

## 3) Operaciones básicas (CRUD en SQL)

### Leer — `SELECT`

```sql
SELECT * FROM message;

SELECT role, content
FROM message
WHERE thread_id = 'demo-aire'
ORDER BY id;
```

### Crear — `INSERT`

```sql
INSERT INTO conversation (id) VALUES ('demo-aire');

INSERT INTO message (thread_id, role, content)
VALUES ('demo-aire', 'user', '¿Cómo está el NO2?');
```

### Actualizar — `UPDATE` (poco usado en el historial del turno)

```sql
UPDATE message
SET content = 'texto corregido'
WHERE id = 2;
```

### Borrar — `DELETE`

```sql
DELETE FROM message WHERE thread_id = 'demo-aire';
```

En la práctica del sprint: **insertáis** al cerrar un `/ask` y **leéis** con GET messages. Casi no actualizáis ni borráis.

---

## 4) Qué hace SQLModel por vosotros

Cuando en Python hacéis:

```python
session.add(Message(thread_id="demo-aire", role="user", content="…"))
session.commit()
```

Debajo el motor ejecuta algo equivalente a un `INSERT INTO message …`.

Cuando hacéis un `select(Message).where(…)`, debajo hay un `SELECT … WHERE …`.

No hace falta memorizar todo el SQL: sí hace falta **leer** un `SELECT`/`INSERT` y entender PK/FK.

---

## 5) SQL vs NoSQL (una frase)

| | Relacional (SQL) | NoSQL (p. ej. documentos) |
|--|------------------|---------------------------|
| Forma | Tablas + relaciones | Documentos, clave-valor, etc. |
| En este sprint | **Historial** en SQLite | Vector DB del RAG (otro almacén) |

El historial de chat encaja bien en tablas. Los embeddings del RAG suelen ir a otra tecnología.

---

## Resumen

- Tabla + PK + FK = modelo mental del historial.
- `SELECT` / `INSERT` = lo que más veréis.
- SQLModel escribe el SQL; vosotros pensáis en clases Python.
