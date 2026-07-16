"""Punto de entrada del pipeline RAG offline.

Flujo completo en un solo comando:
  data/ → ingesta (load, clean, chunk) → chunks.json
       → embeddings (Gemini API)       → embeddings.json

Uso:
  python main.py
"""

from embed import ejecutar_embeddings
from pipeline import ejecutar_ingesta


def _mostrar_muestra_embed(items: list[dict]) -> None:
    """Imprime dimensiones y primeros valores del vector del chunk 0.

    Entrada: items de embeddings.json (text + vector + metadata).
    """
    if not items:
        return
    vector = items[0]["vector"]
    print("\n--- Muestra embedding (chunk 0) ---")
    print(f"  Dimensiones: {len(vector)}")
    print(f"  Primeros 5 valores: {vector[:5]}")


def main() -> None:
    """Ejecuta ingesta + embeddings y muestra un resumen en consola."""
    # Paso 1: preparar fragmentos de texto
    ejecutar_ingesta()

    # Paso 2: convertir cada fragmento en un vector numérico
    print()
    items, _ruta_emb = ejecutar_embeddings()
    _mostrar_muestra_embed(items)

    print("\nListo. Revisa output/chunks.json y output/embeddings.json")
    print("Siguiente paso: indexar en una base vectorial.")


if __name__ == "__main__":
    main()
