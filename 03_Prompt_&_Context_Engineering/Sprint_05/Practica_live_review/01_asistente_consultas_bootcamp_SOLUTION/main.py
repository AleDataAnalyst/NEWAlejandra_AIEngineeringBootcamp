"""main.py — Punto de entrada y demos de la práctica.

Qué hace este módulo:
  - Ejecuta las 3 demos cuando corres `python main.py`.
  - Imprime en consola los resultados con `imprimir_resultado()`.
  - Carga datos de `data/faq.json` y `data/consultas_ejemplo.json`.

Para qué sirve:
  - Probar si tu implementación cumple los criterios del README sin escribir tests extra.

Qué NO debes hacer aquí:
  - Reglas de negocio (validar, clasificar, chat) → van en `validators.py`, `logic.py`, etc.
  - Llamadas directas a Gemini → usa `gemini_client.py` desde `logic.py`.
"""

import json
from pathlib import Path

from context import cargar_faq

DATA_DIR = Path(__file__).parent / "data"


def imprimir_resultado(r: dict) -> None:
    status = r.get("status", "unknown").upper()
    print(f"[{status}] {r.get('mensaje', '')}")
    if r.get("status") == "error":
        for e in r.get("data", {}).get("errores", []):
            print("  -", e)
        return
    data = r.get("data", {})
    if "category" in data:
        print(f"  → {data.get('category')} / {data.get('priority')}: {data.get('summary')}")
    if "respuesta" in data:
        print(f"\n{data['respuesta'][:500]}\n")
        m = data.get("metricas", {})
        print(
            f"  métricas: {m.get('elapsed_ms')} ms | "
            f"in={m.get('prompt_tokens')} out={m.get('output_tokens')}"
        )
    if "topic_id" in data:
        entry = data.get("entry", {})
        print(f"  FAQ topic: {data.get('topic_id')}")
        print(f"  P: {entry.get('question', '')[:80]}...")


def demo_verificar_estructura() -> None:
    print("=" * 60)
    print("0) Verificación de estructura (sin API)")
    print("=" * 60)
    faq = cargar_faq(DATA_DIR / "faq.json")
    consultas = json.loads((DATA_DIR / "consultas_ejemplo.json").read_text(encoding="utf-8"))
    print(f"  FAQ cargado: {len(faq)} entradas")
    print(f"  Consultas ejemplo: {len(consultas)} registros")
    print("  Estructura OK.\n")


def demo_clasificar_consultas() -> None:
    from logic import clasificar_consulta

    print("=" * 60)
    print("1) Validación + clasificación JSON")
    print("=" * 60)
    consultas = json.loads((DATA_DIR / "consultas_ejemplo.json").read_text(encoding="utf-8"))
    for c in consultas:
        print(f"\n--- {c.get('nombre') or '(sin nombre)'} ---")
        imprimir_resultado(clasificar_consulta(c))


def demo_chat_con_contexto() -> None:
    from context import cargar_faq, seleccionar_faq
    from logic import demo_seleccion_faq, responder_chat
    from state import inicializar_estado

    print("\n" + "=" * 60)
    print("2) FAQ filtrado + chat con memoria")
    print("=" * 60)

    consulta_faq = "¿Qué es la live review del bootcamp?"
    print(f"\nSelección FAQ: {consulta_faq}")
    imprimir_resultado(demo_seleccion_faq(DATA_DIR / "faq.json", consulta_faq))

    state = inicializar_estado(
        {
            "name": "Ana",
            "email": "ana@ejemplo.com",
            "language": "español",
            "level": "junior",
        }
    )
    faq_path = DATA_DIR / "faq.json"

    turnos = [
        "Me llamo Ana y estudio el Sprint 5 del bootcamp.",
        "¿Cuándo son las clases en directo?",
        "¿Cómo me llamo y qué sprint estoy estudiando?",
    ]
    for pregunta in turnos:
        print(f"\n--- Usuario: {pregunta}")
        faq_sel = seleccionar_faq(cargar_faq(faq_path), pregunta, max_entradas=1)
        imprimir_resultado(responder_chat(state, pregunta, faq_sel))


def main() -> None:
    demo_verificar_estructura()
    try:
        demo_clasificar_consultas()
    except NotImplementedError as e:
        print(f"\n[PENDIENTE — clasificación] {e}\n")
    try:
        demo_chat_con_contexto()
    except NotImplementedError as e:
        print(f"\n[PENDIENTE — chat con contexto] {e}\n")
    print("Fin. Consulta README.md para criterios de aceptación.")


if __name__ == "__main__":
    main()
