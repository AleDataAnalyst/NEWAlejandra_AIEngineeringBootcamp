"""Punto de entrada de la práctica Live Review Sprint 07.

Demo 0: verificación sin API (preguntas + entregables).
Demo 1: benchmark Gemini (pregunta × modelo) → CSV + informe.
"""

from benchmark import ejecutar_benchmark
from report import generar_reporte_md, guardar_csv
from verificar import verificar_entregables, verificar_preguntas


def demo_verificar() -> bool:
    print("=" * 60)
    print("0) Verificación (sin API)")
    print("=" * 60)

    ok_preg, err_preg = verificar_preguntas()
    if ok_preg:
        print("  [OK] data/preguntas.json")
    else:
        print("  [PENDIENTE — preguntas]")
        for e in err_preg:
            print(f"    - {e}")

    ok_ent, err_ent = verificar_entregables()
    if ok_ent:
        print("  [OK] entregables/ (matriz + recomendación)")
    else:
        print("  [PENDIENTE — entregables] (Fase 2)")
        for e in err_ent:
            print(f"    - {e}")

    print()
    return ok_preg


def demo_benchmark() -> None:
    print("=" * 60)
    print("1) Benchmark Gemini (pregunta × modelo)")
    print("=" * 60)

    ok_preg, err_preg = verificar_preguntas()
    if not ok_preg:
        print("[PENDIENTE — preguntas] Completa data/preguntas.json antes del benchmark:")
        for e in err_preg:
            print(f"  - {e}")
        print()
        return

    print("Iniciando benchmark...")
    filas = ejecutar_benchmark()
    csv_path = guardar_csv(filas)
    md_path = generar_reporte_md(filas, csv_path)
    print(f"\nCSV: {csv_path}")
    print(f"Informe: {md_path}")
    print("\nSiguiente: completa entregables/matriz_decision.md y recomendacion.md")


def main() -> None:
    demo_verificar()
    demo_benchmark()


if __name__ == "__main__":
    main()
