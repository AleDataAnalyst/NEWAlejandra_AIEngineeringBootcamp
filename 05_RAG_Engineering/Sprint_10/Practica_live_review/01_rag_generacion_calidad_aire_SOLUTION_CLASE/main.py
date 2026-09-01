"""Punto de entrada — Live Review Sprint 10 (calidad del aire).

Uso:
  python main.py --prepare --index
  python main.py --ask "¿Qué mide la magnitud 83?"
  python main.py --eval
  python main.py --check
  streamlit run app.py
"""

from __future__ import annotations

import argparse
import json

from src.context import imprimir_contexto
from src.embed import ejecutar_embeddings
from src.eval_generation import ejecutar_evaluacion
from src.index import ejecutar_indexacion
from src.pipeline import ejecutar_ingesta
from src.retriever import recuperar
from verificar import (
    verificar_app,
    verificar_entregable,
    verificar_eval_generation,
    verificar_generate,
    verificar_logic,
    verificar_prompts,
)


def _cmd_check() -> None:
    print("=" * 60)
    print("Verificación capa Sprint 10 (sin Gemini de generación si stubs)")
    print("=" * 60)

    checks = [
        ("src/prompts.py", verificar_prompts),
        ("src/generate.py", verificar_generate),
        ("src/logic.py", verificar_logic),
        ("src/eval_generation.py", verificar_eval_generation),
        ("app.py", verificar_app),
        ("entregables/reflexion_generacion.md", verificar_entregable),
    ]
    for nombre, fn in checks:
        ok, errores = fn()
        if ok:
            print(f"  [OK] {nombre}")
        else:
            print(f"  [PENDIENTE — {nombre}]")
            for e in errores:
                print(f"    - {e}")
    print()


def _cmd_prepare() -> None:
    ejecutar_ingesta()
    print()
    ejecutar_embeddings()


def _cmd_index(recreate: bool) -> None:
    total = ejecutar_indexacion(recreate=recreate)
    print(f"\nÍndice listo: {total} vectores en ChromaDB.")


def _cmd_query(pregunta: str, top_k: int | None) -> None:
    chunks = recuperar(pregunta, top_k=top_k)
    imprimir_contexto(chunks)


def _cmd_ask(pregunta: str, top_k: int | None) -> None:
    from src.logic import responder

    resultado = responder(pregunta, top_k=top_k)
    print(json.dumps(
        {
            "respuesta": resultado.get("respuesta"),
            "fuentes": resultado.get("fuentes"),
            "error": resultado.get("error"),
        },
        ensure_ascii=False,
        indent=2,
    ))


def main() -> None:
    parser = argparse.ArgumentParser(
        description="Live Review S10 — generación RAG calidad del aire"
    )
    parser.add_argument("--check", action="store_true")
    parser.add_argument("--prepare", action="store_true")
    parser.add_argument("--index", action="store_true")
    parser.add_argument("--recreate-index", action="store_true")
    parser.add_argument("--query", type=str, help="Solo retrieval (debug S9)")
    parser.add_argument("--ask", type=str, help="RAG completo: responder()")
    parser.add_argument("--top-k", type=int, default=None)
    parser.add_argument("--eval", action="store_true", help="Eval respuestas")

    args = parser.parse_args()

    if not any(
        [args.check, args.prepare, args.index, args.query, args.ask, args.eval]
    ):
        parser.print_help()
        print(
            "\nEjemplo:\n"
            "  python main.py --prepare --index\n"
            '  python main.py --ask "¿Qué mide la magnitud 83?"\n'
            "  python main.py --eval\n"
            "  streamlit run app.py"
        )
        return

    if args.check:
        _cmd_check()
    if args.prepare:
        _cmd_prepare()
    if args.index:
        _cmd_index(recreate=args.recreate_index)
    if args.query:
        _cmd_query(args.query, args.top_k)
    if args.ask:
        _cmd_ask(args.ask, args.top_k)
    if args.eval:
        ejecutar_evaluacion()


if __name__ == "__main__":
    main()
