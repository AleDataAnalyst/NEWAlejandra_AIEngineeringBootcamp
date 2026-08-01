"""Punto de entrada — Live Review Sprint 08.

Tres demos al ejecutar python main.py:

  0) Verificación (sin API): load.py + entregables
  1) Ingesta → output/chunks.json
  2) Embeddings → output/embeddings.json (requiere GEMINI_API_KEY)
"""

from embed import ejecutar_embeddings
from pipeline import ejecutar_ingesta
from verificar import verificar_entregables, verificar_load


def _mostrar_muestra_embed(items: list[dict]) -> None:
    """Imprime dimensiones del primer vector para inspección rápida."""
    if not items:
        return
    vector = items[0]["vector"]
    print("\n--- Muestra embedding (chunk 0) ---")
    print(f"  Dimensiones: {len(vector)}")
    print(f"  Primeros 5 valores: {vector[:5]}")


def demo_verificar() -> bool:
    """Demo 0: comprueba load.py y entregables sin llamar a Gemini."""
    print("=" * 60)
    print("0) Verificación (sin API)")
    print("=" * 60)

    ok_load, err_load = verificar_load()
    if ok_load:
        print("  [OK] load.py (ingesta CSV meteorológico)")
    else:
        print("  [PENDIENTE — load.py]")
        for e in err_load:
            print(f"    - {e}")

    ok_ent, err_ent = verificar_entregables()
    if ok_ent:
        print("  [OK] entregables/ (estrategia + reflexión)")
    else:
        print("  [PENDIENTE — entregables] (Fase 2)")
        for e in err_ent:
            print(f"    - {e}")

    print()
    return ok_load


def demo_ingesta() -> bool:
    """Demo 1: pipeline completo hasta chunks.json."""
    print("=" * 60)
    print("1) Pipeline ingesta → output/chunks.json")
    print("=" * 60)

    ok_load, err_load = verificar_load()
    if not ok_load:
        print("[PENDIENTE — load.py] Completa load.py antes de la ingesta:")
        for e in err_load:
            print(f"  - {e}")
        print()
        return False

    ejecutar_ingesta()
    print()
    return True


def demo_embeddings() -> None:
    """Demo 2: genera embeddings.json (Fase 2)."""
    print("=" * 60)
    print("2) Embeddings Gemini → output/embeddings.json")
    print("=" * 60)

    ok_load, err_load = verificar_load()
    if not ok_load:
        print("[PENDIENTE — load.py] Completa load.py antes de embeddear:")
        for e in err_load:
            print(f"  - {e}")
        print()
        return

    items, _ruta = ejecutar_embeddings()
    _mostrar_muestra_embed(items)
    print("\nListo. Revisa output/chunks.json y output/embeddings.json")


def main() -> None:
    demo_verificar()
    if demo_ingesta():
        demo_embeddings()


if __name__ == "__main__":
    main()
