"""Comprobaciones ligeras — no gastan cuota Gemini."""

import inspect
import sys


def _funcion_pendiente(modulo, nombre: str) -> bool:
    fn = getattr(modulo, nombre, None)
    if fn is None or not inspect.isfunction(fn):
        return True
    try:
        codigo = inspect.getsource(fn)
    except OSError:
        codigo = ""
    return "NotImplementedError" in codigo


def main() -> int:
    ok = True

    try:
        import src.agent as mod
    except ImportError as exc:
        print(f"[FAIL] No se puede importar src.agent: {exc}")
        return 1

    for nombre in ("procesar_turno", "run_demo"):
        if _funcion_pendiente(mod, nombre):
            print(f"[FAIL] Implementa {nombre}() en src/agent.py")
            ok = False
        else:
            print(f"[OK] {nombre}")

    if not ok:
        return 1

    from src.state import crear_estado

    try:
        estado = mod.procesar_turno(crear_estado(""), "   ")
    except NotImplementedError:
        print("[FAIL] procesar_turno sigue sin implementar")
        return 1
    except Exception as exc:  # noqa: BLE001
        print(f"[FAIL] procesar_turno('') lanzó: {exc}")
        return 1

    if not isinstance(estado, dict) or not (estado.get("respuesta") or "").strip():
        print("[FAIL] mensaje vacío debería devolver dict con respuesta no vacía")
        return 1
    if estado.get("traza"):
        print("[FAIL] mensaje vacío no debería añadir traza (no hay llamada al LLM)")
        return 1

    print("[OK] mensaje vacío (sin LLM)")
    print("Todo [OK] — prueba también: python main.py  y  streamlit run app.py")
    return 0


if __name__ == "__main__":
    sys.exit(main())
