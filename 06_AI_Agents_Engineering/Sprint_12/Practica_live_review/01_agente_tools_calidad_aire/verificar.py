"""Comprobaciones ligeras — no gastan cuota Gemini. DADO."""

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
        import src.tools as tools_mod
    except ImportError as exc:
        print(f"[FAIL] No se puede importar src.tools: {exc}")
        return 1

    registry = getattr(tools_mod, "TOOL_REGISTRY", None)
    esperadas = {
        "hora_actual",
        "RAG_buscar_en_guia",
        "API_consultar_calidad_aire",
    }
    if not isinstance(registry, dict) or not esperadas.issubset(registry.keys()):
        print(
            "[FAIL] TOOL_REGISTRY debe incluir hora_actual, "
            "RAG_buscar_en_guia, API_consultar_calidad_aire"
        )
        ok = False
    else:
        print("[OK] TOOL_REGISTRY")

    for nombre in ("validar_args", "ejecutar_tool"):
        if _funcion_pendiente(tools_mod, nombre):
            print(f"[FAIL] Implementa {nombre}() en src/tools/__init__.py")
            ok = False
        else:
            print(f"[OK] {nombre}")

    # API viene dada: solo smoke-test (api o fallback)
    try:
        from src.tools import api_calidad_aire as api_mod
    except ImportError as exc:
        print(f"[FAIL] No se puede importar api_calidad_aire: {exc}")
        return 1

    try:
        out = api_mod.API_consultar_calidad_aire(limite=2)
    except Exception as exc:
        print(f"[FAIL] API_consultar_calidad_aire lanzó: {exc}")
        ok = False
    else:
        if not isinstance(out, str) or not out.strip():
            print("[FAIL] API_consultar_calidad_aire debe devolver str no vacío")
            ok = False
        elif "Fuente:" not in out:
            print("[FAIL] El resumen debe incluir 'Fuente: api' o 'Fuente: fallback'")
            ok = False
        else:
            print("[OK] API_consultar_calidad_aire (dada)")

    if not _funcion_pendiente(tools_mod, "validar_args"):
        try:
            limpios = tools_mod.validar_args(
                "API_consultar_calidad_aire", {"limite": 99}
            )
            if limpios.get("limite") != 10:
                print("[FAIL] validar_args debe acotar limite a 1..10 (99 → 10)")
                ok = False
            else:
                print("[OK] validar_args (limite)")
        except Exception as exc:
            print(f"[FAIL] validar_args: {exc}")
            ok = False

    try:
        import src.agent as agent_mod
    except ImportError as exc:
        print(f"[FAIL] No se puede importar src.agent: {exc}")
        return 1

    for nombre in ("procesar_turno", "run_demo"):
        if _funcion_pendiente(agent_mod, nombre):
            print(f"[FAIL] Implementa {nombre}() en src/agent.py")
            ok = False
        else:
            print(f"[OK] {nombre}")

    try:
        import src.llm as llm_mod
    except ImportError as exc:
        print(f"[FAIL] No se puede importar src.llm: {exc}")
        return 1

    if _funcion_pendiente(llm_mod, "run_tool_loop"):
        print("[FAIL] Completa el TODO de allowlist/ejecutar_tool en run_tool_loop")
        ok = False
    else:
        try:
            src = inspect.getsource(llm_mod.run_tool_loop)
        except OSError:
            src = ""
        if "ejecutar_tool" not in src or "blocked" not in src:
            print(
                "[FAIL] run_tool_loop debe usar ejecutar_tool y marcar status blocked"
            )
            ok = False
        else:
            print("[OK] run_tool_loop (allowlist / ejecutar_tool)")

    if not ok:
        return 1

    from src.state import crear_estado

    try:
        estado = agent_mod.procesar_turno(crear_estado(""), "   ")
    except NotImplementedError:
        print("[FAIL] procesar_turno sigue sin implementar")
        return 1
    except Exception as exc:
        print(f"[FAIL] procesar_turno('') lanzó: {exc}")
        return 1

    if not isinstance(estado, dict) or not (estado.get("respuesta") or "").strip():
        print("[FAIL] mensaje vacío debería devolver dict con respuesta no vacía")
        return 1
    if estado.get("traza"):
        print("[FAIL] mensaje vacío no debería añadir traza")
        return 1

    print("[OK] mensaje vacío (sin LLM)")
    print("Todo [OK] — prueba también: python main.py  y  streamlit run app.py")
    return 0


if __name__ == "__main__":
    sys.exit(main())
