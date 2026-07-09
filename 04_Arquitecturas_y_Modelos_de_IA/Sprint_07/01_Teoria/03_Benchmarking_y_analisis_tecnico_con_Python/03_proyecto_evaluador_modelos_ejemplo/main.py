"""Punto de entrada del evaluador de modelos.

Orquesta el flujo completo: ejecuta el benchmark (pregunta × modelo),
guarda los resultados en CSV y genera un informe Markdown resumen.
Ejecutar con: python main.py
"""

from benchmark import ejecutar_benchmark
from report import generar_reporte_md, guardar_csv


def main() -> None:
    print("Iniciando benchmark (pregunta × modelo)...")
    filas = ejecutar_benchmark()
    csv_path = guardar_csv(filas)
    md_path = generar_reporte_md(filas, csv_path)
    print(f"\nCSV: {csv_path}")
    print(f"Informe: {md_path}")
    print("Listo. Ajusta MODELS y data/preguntas.json en config / data.")


if __name__ == "__main__":
    main()
