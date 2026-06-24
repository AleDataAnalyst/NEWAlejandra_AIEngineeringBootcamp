# state.py — estado de sesión del asistente de estudio


def inicializar_estado(user_profile: dict | None = None) -> dict:
    return {
        "user_profile": user_profile or {},
        "messages": [],  # historial completo: {"role": "user"|"model", "text": str}
        "summary": "",
        "turnos": 0,
    }


def append_user(state: dict, texto: str) -> None:
    state["messages"].append({"role": "user", "text": texto.strip()})


def append_model(state: dict, texto: str) -> None:
    state["messages"].append({"role": "model", "text": texto.strip()})
    state["turnos"] = state.get("turnos", 0) + 1


def ultimos_n(state: dict, n: int) -> list[dict]:
    msgs = state.get("messages", [])
    return msgs[-n:] if n > 0 else []


def historial_como_texto(state: dict) -> str:
    lines = []
    for msg in state.get("messages", []):
        lines.append(f"{msg.get('role', 'user')}: {msg.get('text', '')}")
    return "\n".join(lines)


def set_summary(state: dict, summary: str) -> None:
    state["summary"] = (summary or "").strip()
