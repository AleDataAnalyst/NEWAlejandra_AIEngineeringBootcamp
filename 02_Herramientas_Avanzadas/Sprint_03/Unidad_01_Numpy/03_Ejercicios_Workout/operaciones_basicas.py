"""
Autor: The Bridge
Descripción: Módulo de operaciones básicas para practicar imports.
"""


def suma(a, b):
    """
    Suma dos números.

    Args:
        a (int | float): primer sumando
        b (int | float): segundo sumando

    Returns:
        int | float: resultado de a + b
    """
    return a + b


def resta(a, b):
    """
    Resta dos números.

    Args:
        a (int | float): minuendo
        b (int | float): sustraendo

    Returns:
        int | float: resultado de a - b
    """
    return a - b


def multiplica(a, b):
    """
    Multiplica dos números.

    Args:
        a (int | float): factor 1
        b (int | float): factor 2

    Returns:
        int | float: resultado de a * b
    """
    return a * b


def divide(a, b):
    """
    Divide dos números.

    Args:
        a (int | float): dividendo
        b (int | float): divisor

    Returns:
        float: resultado de a / b

    Raises:
        ZeroDivisionError: si b es 0
    """
    # Deja que ZeroDivisionError ocurra si b == 0
    return a / b


if __name__ == "__main__":
    # Pruebas rápidas (solo al ejecutar este fichero directamente)
    print("Pruebas operaciones_basicas.py")
    print("suma(3,5) ->", suma(3, 5))
    print("resta(10,4) ->", resta(10, 4))
    print("multiplica(6,7) ->", multiplica(6, 7))
    print("divide(8,2) ->", divide(8, 2))
