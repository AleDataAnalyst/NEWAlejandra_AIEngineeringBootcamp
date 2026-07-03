# state.py — estado de sesión del asistente


def inicializar_estado(user_profile: dict | None = None) -> dict:
    return {
        "user_profile": user_profile or {},
        "messages": [],
        "turnos": 0,
    }


def append_user(state: dict, texto: str) -> None:
    state["messages"].append({"role": "user", "text": texto.strip()})


def append_assistant(state: dict, texto: str) -> None:
    state["messages"].append({"role": "assistant", "text": texto.strip()})
    state["turnos"] = state.get("turnos", 0) + 1


def ultimos_n(state: dict, n: int) -> list[dict]:
    msgs = state.get("messages", [])
    return msgs[-n:] if n > 0 else []


def actualizar_perfil_desde_mensaje(state: dict, mensaje: str) -> None:
    """Extracción didáctica (sin LLM) para demos de memoria."""
    msg = mensaje.lower()
    profile = state.setdefault("user_profile", {})

    if "me llamo" in msg:
        resto = mensaje.lower().split("me llamo", 1)[-1].strip().strip(".")
        if resto:
            profile["nombre"] = resto.split()[0].capitalize()

    if "estudio" in msg or "estudiando" in msg:
        for tema in ("assistant engineering", "context engineering", "prompt engineering"):
            if tema in msg:
                profile["tema_actual"] = tema.title()
                break
