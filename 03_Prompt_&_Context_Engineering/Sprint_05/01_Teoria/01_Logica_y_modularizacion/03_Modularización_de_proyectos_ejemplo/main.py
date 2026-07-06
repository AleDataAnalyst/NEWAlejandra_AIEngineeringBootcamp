# main.py — orquestación mínima (sí puede usar print)

from logic import procesar_registro
from state import (
    contar_por_tipo,
    filtrar_por_tipo,
    guardar_si_ok,
    inicializar_estado,
    listar_historial,
    ultimos_n,
)


def imprimir_respuesta(r: dict) -> None:
    status = r.get("status", "unknown").upper()
    mensaje = r.get("mensaje", "")
    print(f"[{status}] {mensaje}")

    if r.get("status") == "error":
        for e in r.get("data", {}).get("errores", []):
            print(" -", e)
    elif r.get("status") == "ok" and "mensaje_tarea" in r.get("data", {}):
        print("  →", r["data"]["mensaje_tarea"])


def main() -> None:
    state = inicializar_estado()

    casos = [
        {"nombre": "Ana", "codigo": "TKT-1234", "tipo": "summary", "prioridad": 3},
        {"nombre": "Luis", "codigo": "TKT-5678", "tipo": "qa", "prioridad": 5},
        {"nombre": "", "tipo": "resumen", "prioridad": "mucho"},
    ]

    for datos in casos:
        resultado = procesar_registro(datos)
        imprimir_respuesta(resultado)
        guardar_si_ok(state, datos, resultado)

    print("\n--- Historial (solo OK) ---")
    for i, reg in enumerate(listar_historial(state), start=1):
        print(
            f"  {i}. {reg.get('nombre')} · {reg.get('tipo')} · prioridad {reg.get('prioridad')}"
        )

    print("\n--- Solo tipo 'summary' ---")
    for reg in filtrar_por_tipo(state, "summary"):
        print(" ", reg.get("nombre"), reg.get("codigo"))

    print("\n--- Contadores por tipo ---", contar_por_tipo(state))
    print("--- Últimos 2 (borrador de contexto) ---", ultimos_n(state, 2))


if __name__ == "__main__":
    main()
