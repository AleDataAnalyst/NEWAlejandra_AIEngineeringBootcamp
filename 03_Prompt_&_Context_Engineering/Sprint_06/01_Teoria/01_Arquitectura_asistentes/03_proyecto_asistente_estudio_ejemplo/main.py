# main.py — demo Smart Study Assistant (Assistant Engineering)

from copy import deepcopy
from pathlib import Path

from config import ASSISTANT_CONFIG_DEFAULT
from logic import crear_estado_demo, demo_seleccion_faq, procesar_turno

DATA_DIR = Path(__file__).parent / "data"


def imprimir_resultado(r: dict) -> None:
    status = r.get("status", "unknown").upper()
    print(f"[{status}] {r.get('mensaje', '')}")
    if r.get("status") == "error":
        for e in r.get("data", {}).get("errores", []):
            print(" -", e)
        return

    data = r.get("data", {})
    if "respuesta" in data:
        print(f"\n{data['respuesta'][:500]}\n")
        m = data.get("metricas", {})
        print(
            f"  perfil={data.get('perfil_activo')} | "
            f"{m.get('elapsed_ms')} ms | tokens={m.get('total_tokens')}"
        )
    elif "entry" in data:
        entry = data["entry"]
        print(f"  topic_id: {data.get('topic_id')}")
        print(f"  P: {entry.get('question')}")
        print(f"  R: {entry.get('answer', '')[:200]}...")


def demo_perfiles() -> None:
    print("=" * 60)
    print("1) Misma pregunta, distinto perfil del asistente")
    print("=" * 60)

    pregunta = "¿Qué es un asistente conversacional con LLM?"
    perfiles = ("junior", "senior", "mentor")

    for perfil in perfiles:
        config = deepcopy(ASSISTANT_CONFIG_DEFAULT)
        config["perfil_activo"] = perfil
        state = crear_estado_demo()
        print(f"\n--- Perfil: {perfil} ---")
        imprimir_resultado(procesar_turno(state, pregunta, assistant_config=config))


def demo_memoria() -> None:
    print("\n" + "=" * 60)
    print("2) Sesión con estado (¿cómo me llamo?)")
    print("=" * 60)

    state = crear_estado_demo()
    turnos = [
        "Me llamo Ana y estoy estudiando Assistant Engineering en el bootcamp.",
        "¿Qué piezas mínimas tiene la arquitectura de un asistente?",
        "¿Cómo me llamo y qué estoy estudiando?",
    ]

    for pregunta in turnos:
        print(f"\n--- Usuario: {pregunta}")
        imprimir_resultado(procesar_turno(state, pregunta))


def demo_faq() -> None:
    print("\n" + "=" * 60)
    print("3) Turno con FAQ seleccionada en Python")
    print("=" * 60)

    consulta = "No entiendo qué es un embedding, ¿me lo explicas?"
    print(f"\nConsulta: {consulta}")
    sel = demo_seleccion_faq(DATA_DIR / "faq.json", consulta)
    imprimir_resultado(sel)

    if sel["status"] != "ok":
        return

    faq_entry = [sel["data"]["entry"]]
    state = crear_estado_demo()
    print("\n--- Respuesta del asistente con contexto FAQ ---")
    imprimir_resultado(procesar_turno(state, consulta, faq_entries=faq_entry))


def main() -> None:
    demo_perfiles()
    demo_memoria()
    demo_faq()
    print("\nListo. Explora config.py, state.py, prompts.py y logic.py.")


if __name__ == "__main__":
    main()
