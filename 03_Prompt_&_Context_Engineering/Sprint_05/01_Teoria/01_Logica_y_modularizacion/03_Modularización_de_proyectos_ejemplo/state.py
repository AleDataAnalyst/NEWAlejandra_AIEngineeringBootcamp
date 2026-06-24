# state.py — sesión en memoria (historial + operaciones)


def inicializar_estado() -> dict:
    return {
        "historial": [],
        "contadores": {},
        "ultima_accion": None,
    }


def guardar_si_ok(state: dict, datos: dict, resultado: dict) -> bool:
    """Solo añade al historial si la lógica devolvió status ok."""
    if resultado.get("status") != "ok":
        state["ultima_accion"] = "rechazado"
        return False

    entrada = {**datos, "procesado": resultado.get("data", {})}
    state["historial"].append(entrada)

    tipo = str(datos.get("tipo", "")).strip().lower()
    state["contadores"][tipo] = state["contadores"].get(tipo, 0) + 1
    state["ultima_accion"] = "guardado"
    return True


def listar_historial(state: dict) -> list[dict]:
    return list(state.get("historial", []))


def filtrar_por_tipo(state: dict, tipo: str) -> list[dict]:
    t = (tipo or "").strip().lower()
    return [
        r
        for r in state.get("historial", [])
        if str(r.get("tipo", "")).strip().lower() == t
    ]


def filtrar_prioridad_minima(state: dict, minimo: int) -> list[dict]:
    return [
        r
        for r in state.get("historial", [])
        if isinstance(r.get("prioridad"), int) and r["prioridad"] >= minimo
    ]


def contar_por_tipo(state: dict) -> dict:
    return dict(state.get("contadores", {}))


def vaciar_historial(state: dict) -> None:
    state["historial"].clear()
    state["contadores"].clear()
    state["ultima_accion"] = "vaciado"


def ultimos_n(state: dict, n: int = 3) -> list[dict]:
    historial = state.get("historial", [])
    return historial[-n:] if n > 0 else []
