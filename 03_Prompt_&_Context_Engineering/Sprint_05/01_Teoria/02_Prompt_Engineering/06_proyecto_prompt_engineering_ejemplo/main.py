# main.py — orquestación (sí usa print)

from pathlib import Path

from logic import (
    cargar_productos_csv,
    clasificar_mensaje,
    generar_ficha_producto,
    generar_recomendacion_clima,
    producto_por_sku,
)

DATA_DIR = Path(__file__).parent / "data"


def imprimir_resultado(r: dict) -> None:
    status = r.get("status", "unknown").upper()
    print(f"[{status}] {r.get('mensaje', '')}")
    if r.get("status") == "error":
        for e in r.get("data", {}).get("errores", []):
            print(" -", e)
    elif r.get("status") == "ok":
        data = r.get("data", {})
        for k, v in data.items():
            if k == "descripcion" or k == "texto":
                print(f"\n{v}\n")
            else:
                print(f"  {k}: {v}")


def demo_clasificacion() -> None:
    print("=" * 60)
    print("1) Clasificación de incidencias (salida JSON)")
    print("=" * 60)

    mensajes = [
        "No puedo acceder a mi cuenta desde ayer, necesito ayuda urgente.",
        "¿Cuándo llega mi factura de marzo?",
        "Quiero comprar 50 licencias para mi equipo.",
    ]

    for msg in mensajes:
        print(f"\nEntrada: {msg}")
        imprimir_resultado(clasificar_mensaje(msg))


def demo_datos_externos() -> None:
    print("\n" + "=" * 60)
    print("2) Inyección de datos externos")
    print("=" * 60)

    # 2a — producto desde CSV
    print("\n--- Ficha de producto (CSV) ---")
    productos = cargar_productos_csv(DATA_DIR / "productos.csv")
    producto = producto_por_sku(productos, "TB-100")
    print(f"SKU: {producto['sku']} · stock: {producto['stock']}")
    imprimir_resultado(generar_ficha_producto(producto))

    # 2b — dict de clima
    print("\n--- Recomendaciones con datos de clima (dict) ---")
    weather = {
        "city": "Madrid",
        "temperature_c": 34,
        "condition": "soleado",
        "uv_high": True,
    }
    imprimir_resultado(generar_recomendacion_clima(weather))


def main() -> None:
    demo_clasificacion()
    demo_datos_externos()
    print("\nListo. Revisa prompts.py y logic.py para ver cómo se construyen los prompts.")


if __name__ == "__main__":
    main()
