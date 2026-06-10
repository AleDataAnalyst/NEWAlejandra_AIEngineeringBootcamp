![imagen](../../assets/cabecera_python.png)

# Módulos: Creación y Manejo de Ficheros Python

## 1. Cómo crear un fichero para ejecutar con Python
Para crear un fichero Python, simplemente crea un archivo con la extensión `.py`. Por ejemplo, `mi_script.py`. Este archivo puede ejecutarse desde la terminal con el comando:

```bash
python mi_script.py
```

### Ejemplo:
```python
# mi_script.py
print("¡Hola, mundo!")
```

Ejecuta el archivo:
```bash
python mi_script.py
```

---

## 2. Estructura de un fichero Python.
Un fichero Python suele seguir esta estructura básica:

1. **Encabezado**: Comentarios iniciales con información del autor, fecha, y descripción.
2. **Importaciones**: Librerías necesarias.
3. **Definición de funciones y clases**.
4. **Bloque principal**: Código que se ejecuta al ejecutar el archivo directamente. Uso de la directiva `__main__`

### Ejemplo 1:
```python
# mi_script.py
"""
Autor: Tu Nombre
Fecha: 2023-10-01
Descripción: Ejemplo de estructura de un fichero Python.
"""

import math  # Importaciones

def calcular_area_circulo(radio):  # Definición de funciones
    return math.pi * radio ** 2

if __name__ == "__main__":  # Bloque principal
    print(calcular_area_circulo(5))
```

### Ejemplo 2:
Supongamos que tenemos un archivo llamado `calculadora.py` que define funciones matemáticas y también incluye un bloque `if __name__ == "__main__":` para pruebas:
```python
# calculadora.py
def suma(a, b):
    return a + b

def resta(a, b):
    return a - b

if __name__ == "__main__":
    print("Pruebas de la calculadora:")
    print(f"Suma: {suma(3, 5)}")  # Salida: Suma: 8
    print(f"Resta: {resta(10, 4)}")  # Salida: Resta: 6
```

**Archivo `main.py`:**
```python
from calculadora import suma, resta

if __name__ == "__main__":
    print("Usando la calculadora desde otro archivo:")
    print(f"Suma: {suma(7, 2)}")  # Salida: Suma: 9
    print(f"Resta: {resta(9, 3)}")  # Salida: Resta: 6
```

Ejecuta `main.py`:
```bash
python main.py
```

### Explicación de main:
El bloque `if __name__ == "__main__":` es una construcción común en Python que se utiliza para determinar si un archivo de Python está siendo ejecutado directamente o si está siendo importado como un módulo en otro archivo.

- Sirve para hacer control de flujo de ejecución del programa
- Lo primero que se ejecuta al lanzar un fichero`.py` es la función o funciones que especifiques dentro de `if __name__ == "__main__"`
- Cuando un archivo de Python se ejecuta directamente, la variable especial `__name__` toma el valor `"__main__"`.
- Si el archivo es importado como un módulo en otro script, la variable `__name__` toma el nombre del archivo (sin la extensión `.py`).
- Este bloque permite que cierto código solo se ejecute cuando el archivo es ejecutado directamente, y no cuando es importado.
- Evita que partes del código (como pruebas, ejemplos o lógica principal) se ejecuten al importar el archivo como módulo.
- Facilitar la reutilización del código en otros scripts o proyectos.

---

### Buenas prácticas con un fichero Python
- Usa nombres de variables y funciones descriptivos.
- Sigue las convenciones de estilo PEP 8.[Más info](https://peps.python.org/pep-0008/)
- Divide el código en funciones y módulos reutilizables.
- Documenta tu código con comentarios y docstrings.
- Usa el bloque `if __name__ == "__main__":` para evitar que el código se ejecute al importar el módulo.

---

## 3. Cómo hacer debugging de un fichero `.py`
1. Coloca puntos de interrupción (breakpoints) haciendo clic en el margen izquierdo del editor.
2. Abre la pestaña "Run and Debug" (`Ctrl + Shift + D` o `Cmd + Shift + D`).
3. Configura un archivo `launch.json` si es necesario.
4. Ejecuta el debugger.

---

## 4. Importar y exportar módulos
Puedes dividir tu código en varios módulos y reutilizarlos mediante `import`.

### Ejemplo:
**Archivo `operaciones.py`:**
```python
def suma(a, b):
    return a + b
```

**Archivo `main.py`:**
```python
from operaciones import suma

if __name__ == "__main__":
    print(suma(3, 5))
```

Ejecuta `main.py`:
```bash
python main.py
```

### Exportar módulos:
En Python, puedes exportar funciones, clases o variables definiéndolas en un archivo `.py` y luego importándolas en otros archivos. Esto permite organizar el código en módulos reutilizables y facilita su mantenimiento.

#### Ejemplo práctico:

1. **Definir un módulo (`mimodulo.py`):**
    ```python
    # mimodulo.py
    def saludar(nombre):
         return f"Hola, {nombre}!"

    class Persona:
         def __init__(self, nombre):
              self.nombre = nombre

         def presentar(self):
              return f"Soy {self.nombre}."
    ```

2. **Importar y usar el módulo en otro archivo (`main.py`):**
    ```python
    # main.py
    from mimodulo import saludar, Persona

    print(saludar("Mercedes"))  # Salida: Hola, Mercedes!

    persona = Persona("Andrés")
    print(persona.presentar())  # Salida: Soy Andrés.
    ```

De esta forma, puedes reutilizar el código definido en `mimodulo.py` en cualquier otro archivo de tu proyecto.
Para exportar funciones o clases, simplemente defínelas en un archivo `.py`. Luego, usa `import` para acceder a ellas desde otros archivos.

### Cómo importar un módulo/fichero y llamar a una función desde un archivo .ipynb

1. **Asegúrate de que el módulo o fichero esté en el mismo directorio**:
    - El archivo Python que deseas importar (por ejemplo, `mi_modulo.py`) debe estar en el mismo directorio que el archivo `.ipynb`. Si está en una ubicación diferente, asegúrate de proporcionar la ruta correcta.

2. **Importa el módulo o fichero**:
    - Usa la instrucción `import` para importar el módulo. Por ejemplo:
      ```python
      import mi_modulo
      ```
    - Si deseas importar una función específica del módulo, utiliza:
      ```python
      from mi_modulo import mi_funcion
      ```

3. **Llama a la función desde el módulo**:
    - Si importaste todo el módulo, llama a la función usando la notación de punto:
      ```python
      mi_modulo.mi_funcion()
      ```
    - Si importaste solo la función, puedes llamarla directamente:
      ```python
      mi_funcion()
      ```

4. **Recarga el módulo si haces cambios**:
    - Si realizas cambios en el archivo del módulo mientras trabajas en el notebook, usa el siguiente comando para recargarlo:
      ```python
      from importlib import reload
      reload(mi_modulo)
      ```

5. **Ejemplo práctico**:
    - Supongamos que tienes un archivo llamado `mi_modulo.py` con una función `saludar()`:
      ```python
      # mi_modulo.py
      def saludar():
            print("¡Hola desde mi_modulo!")
      ```
    - En tu notebook, puedes importar y usar la función de la siguiente manera:
      ```python
      import mi_modulo
      mi_modulo.saludar()
      ```
    - O bien:
      ```python
      from mi_modulo import saludar
      saludar()
      ```

## 5. Documentar funciones en Python

Documentar funciones es una buena práctica que facilita la comprensión y el mantenimiento del código. Para documentar una función, utiliza un **docstring**, que es una cadena de texto colocada justo debajo de la definición de la función.

### Ejemplo:
```python
def suma(a, b):
    """
    Suma dos números.

    Args:
        a (int or float): El primer número.
        b (int or float): El segundo número.

    Returns:
        int or float: La suma de los dos números.
    """
    return a + b
```

### Cómo acceder a la documentación:
Puedes acceder al docstring de una función utilizando la función `help()` o el atributo `__doc__`.

#### Ejemplo de uso:
```python
if __name__ == "__main__":
    print(suma(3, 5))  # Resultado: 8

    # Acceder al docstring
    help(suma)
    print(suma.__doc__)
```

#### Salida esperada:
```plaintext
Help on function suma in module __main__:

suma(a, b)
    Suma dos números.

    Args:
        a (int or float): El primer número.
        b (int or float): El segundo número.

    Returns:
        int or float: La suma de los dos números.

Suma dos números.

Args:
    a (int or float): El primer número.
    b (int or float): El segundo número.

Returns:
    int or float: La suma de los dos números.
```

### Ejecución:
Guarda el código en un archivo, por ejemplo, `documentar_funciones.py`, y ejecútalo desde la terminal:
```bash
python documentar_funciones.py
```

### Buenas prácticas:
- Usa un formato consistente para los docstrings, como [Google Style](https://google.github.io/styleguide/pyguide.html) o [Numpy Style](https://numpydoc.readthedocs.io/en/latest/format.html).
- Documenta todos los argumentos, valores de retorno y posibles excepciones.
- Mantén los docstrings claros y concisos.
- Usar herramientas como [`pydoc`](https://docs.python.org/3/library/pydoc.html) o [`Sphinx`](https://www.sphinx-doc.org/en/master/) para generar documentación automáticamente a partir de los docstrings. Te genera una web con HTML,CSS, JS con la documentación de tu proyecto.

### Más info
- [docstrings-python](https://www.datacamp.com/es/tutorial/docstrings-python)
- [crear-documentacion-con-pydoc](https://trifulcas.com/courses/programacion-en-pyhton/lessons/crear-documentacion-con-pydoc/)
- [A “How to” Guide for Sphinx + ReadTheDocs](https://sphinx-rtd-tutorial.readthedocs.io/en/latest/)
