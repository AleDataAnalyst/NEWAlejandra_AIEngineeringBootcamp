"""
Autor: The Bridge
Descripción: Utilidades de texto para practicar módulos y docstrings.
"""


def normaliza_nombre(nombre):
    """
    Normaliza un nombre propio a formato 'Title Case' eliminando espacios extra.

    Args:
        nombre (str): nombre a normalizar

    Returns:
        str: nombre normalizado
    """
    if nombre is None:
        return ""
    # Colapsa espacios y aplica Title Case palabra a palabra
    partes = str(nombre).strip().split()
    return " ".join(p.title() for p in partes)


def cuenta_palabras(texto):
    """
    Cuenta cuántas palabras hay en un texto (separadas por espacios).

    Args:
        texto (str): texto de entrada

    Returns:
        int: número de palabras
    """
    if texto is None:
        return 0
    return len(str(texto).strip().split())


if __name__ == "__main__":
    print("Pruebas texto_utils.py")
    print(normaliza_nombre("   maría   del   mar "))
    print(cuenta_palabras("hola mundo desde python"))
