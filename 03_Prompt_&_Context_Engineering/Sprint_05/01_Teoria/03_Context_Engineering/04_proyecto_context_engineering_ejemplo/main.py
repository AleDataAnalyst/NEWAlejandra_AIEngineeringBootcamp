# main.py — demo Smart Study Assistant (Context Engineering)

from pathlib import Path

from logic import (
    crear_estado_demo,
    demo_faq,
    faq_para_topic,
    responder_pregunta,
)

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
            f"  métricas: {m.get('elapsed_ms')} ms | "
            f"in={m.get('prompt_tokens')} out={m.get('output_tokens')} "
            f"total={m.get('total_tokens')} | modo={data.get('modo_contexto')}"
        )
        if data.get("resumen_actualizado"):
            print("  → resumen de sesión actualizado")
    elif "entry" in data:
        entry = data["entry"]
        print(f"  topic_id: {data.get('topic_id')}")
        print(f"  P: {entry.get('question')}")
        print(f"  R: {entry.get('answer', '')[:200]}...")


def demo_seleccion_faq() -> None:
    print("=" * 60)
    print("1) Selección de FAQ (sin meter todo el JSON en el prompt)")
    print("=" * 60)

    consulta = "No entiendo qué son los embeddings, ¿me lo explicas?"
    print(f"\nConsulta: {consulta}")
    imprimir_resultado(demo_faq(DATA_DIR / "faq.json", consulta))


def demo_chat_con_memoria() -> None:
    print("\n" + "=" * 60)
    print("2) Chat con perfil + historial reciente")
    print("=" * 60)

    state = crear_estado_demo()
    faq = faq_para_topic(DATA_DIR, "context_engineering")

    turnos = [
        "Me llamo Ana y estoy estudiando Context Engineering en el bootcamp.",
        "¿Qué debería tener en cuenta al construir contexto para un LLM?",
        "¿Cómo me llamo y qué estoy estudiando?",
    ]

    for pregunta in turnos:
        print(f"\n--- Usuario: {pregunta}")
        imprimir_resultado(responder_pregunta(state, pregunta, faq_entries=faq))


def demo_compresion_por_resumen() -> None:
    print("\n" + "=" * 60)
    print("3) Conversación larga → resumen + ventana")
    print("=" * 60)

    state = crear_estado_demo()
    faq = faq_para_topic(DATA_DIR, "tokens")

    turnos_extra = [
        "Explícame por qué importan los tokens en una app con LLM.",
        "Si mando todo el historial siempre, ¿qué problema hay?",
        "¿Qué estrategia simple puedo usar para no enviar todo?",
        "Resume en una frase la idea de presupuesto de contexto.",
        "¿Recuerdas mi nombre y mi tema de estudio?",
    ]

    for pregunta in turnos_extra:
        print(f"\n--- Usuario: {pregunta}")
        r = responder_pregunta(state, pregunta, faq_entries=faq)
        imprimir_resultado(r)
        if r.get("status") == "ok" and r["data"].get("summary"):
            print("  summary (extracto):", r["data"]["summary"][:180], "...")


def main() -> None:
    demo_seleccion_faq()
    demo_chat_con_memoria()
    demo_compresion_por_resumen()
    print("\nListo. Explora config.py, context.py, state.py y prompts.py.")


if __name__ == "__main__":
    main()
