"""Comprobaciones ligeras — no gastan cuota Gemini (salvo que importes mal)."""

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

    # --- tools (dadas en S13) ---
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
        print("[FAIL] TOOL_REGISTRY incompleto")
        ok = False
    else:
        print("[OK] TOOL_REGISTRY")

    for nombre in ("validar_args", "ejecutar_tool"):
        if _funcion_pendiente(tools_mod, nombre):
            print(f"[FAIL] {nombre}()")
            ok = False
        else:
            print(f"[OK] {nombre}")

    # --- graph ---
    try:
        import src.graph as graph_mod
    except ImportError as exc:
        print(f"[FAIL] No se puede importar src.graph: {exc}")
        return 1

    for nombre in ("build_graph", "invoke_tools_loop", "_router", "_router_tras_tools"):
        if _funcion_pendiente(graph_mod, nombre):
            print(f"[FAIL] Completa {nombre}() en src/graph.py")
            ok = False
        else:
            print(f"[OK] {nombre}")

    if not _funcion_pendiente(graph_mod, "build_graph"):
        try:
            src = inspect.getsource(graph_mod.build_graph)
        except OSError:
            src = ""
        if "add_conditional_edges" not in src or "agent" not in src:
            print("[FAIL] build_graph debe cablear agent/tools con edges condicionales")
            ok = False
        else:
            print("[OK] build_graph (edges)")

    if not _funcion_pendiente(graph_mod, "invoke_tools_loop"):
        try:
            src = inspect.getsource(graph_mod.invoke_tools_loop)
        except OSError:
            src = ""
        if ".invoke(" not in src:
            print("[FAIL] invoke_tools_loop debe llamar app.invoke(...)")
            ok = False
        else:
            print("[OK] invoke_tools_loop (invoke)")

    # --- agent ---
    try:
        import src.agent as agent_mod
    except ImportError as exc:
        print(f"[FAIL] No se puede importar src.agent: {exc}")
        return 1

    for nombre in ("procesar_turno", "run_demo", "aprobar_plan"):
        if _funcion_pendiente(agent_mod, nombre):
            print(f"[FAIL] Implementa {nombre}() en src/agent.py")
            ok = False
        else:
            print(f"[OK] {nombre}")

    if not _funcion_pendiente(agent_mod, "procesar_turno"):
        try:
            src = inspect.getsource(agent_mod.procesar_turno)
        except OSError:
            src = ""
        if "invoke_tools_loop" not in src:
            print("[FAIL] procesar_turno debe llamar invoke_tools_loop (grafo)")
            ok = False
        else:
            print("[OK] procesar_turno usa grafo")

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
    print("Todo [OK] — prueba: python main.py  y  streamlit run app.py")
    return 0


if __name__ == "__main__":
    sys.exit(main())
