"""Punto de entrada — Live Review Sprint 09 (calidad del aire).

Uso:
  python main.py --prepare              # ingesta + embeddings (S8, dado)
  python main.py --index                # indexar en ChromaDB (Fase 1)
  python main.py --prepare --index      # pipeline offline completo
  python main.py --query "pregunta"     # retrieval + contexto (Fase 2)
  python main.py --eval                 # evaluación con preguntas fijas (Fase 3)
  python main.py --check                # verificación sin API
"""

import argparse

from context import imprimir_contexto
from embed import ejecutar_embeddings
from eval_retrieval import ejecutar_evaluacion
from index import ejecutar_indexacion
from pipeline import ejecutar_ingesta
from retriever import recuperar
from verificar import verificar_entregable, verificar_index, verificar_retriever, verificar_eval


def _cmd_check() -> None:
    print("=" * 60)
    print("Verificación (sin API de retrieval)")
    print("=" * 60)

    ok_i, err_i = verificar_index()
    if ok_i:
        print("  [OK] index.py")
    else:
        print("  [PENDIENTE — index.py]")
        for e in err_i:
            print(f"    - {e}")

    ok_r, err_r = verificar_retriever()
    if ok_r:
        print("  [OK] retriever.py")
    else:
        print("  [PENDIENTE — retriever.py]")
        for e in err_r:
            print(f"    - {e}")

    ok_e, err_e = verificar_eval()
    if ok_e:
        print("  [OK] eval_retrieval.py")
    else:
        print("  [PENDIENTE — eval_retrieval.py]")
        for e in err_e:
            print(f"    - {e}")

    ok_ent, err_ent = verificar_entregable()
    if ok_ent:
        print("  [OK] entregables/reflexion_retrieval.md")
    else:
        print("  [PENDIENTE — entregables]")
        for e in err_ent:
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
    print("\n(Sprint 10: este contexto iría al prompt de Gemini.)")


def _cmd_eval() -> None:
    ejecutar_evaluacion()


def main() -> None:
    parser = argparse.ArgumentParser(
        description="Live Review S9 — retrieval calidad del aire Madrid"
    )
    parser.add_argument(
        "--check",
        action="store_true",
        help="Verifica stubs / entregable (sin llamar a Gemini ni Chroma)",
    )
    parser.add_argument(
        "--prepare",
        action="store_true",
        help="Ingesta + embeddings (Sprint 8, código dado)",
    )
    parser.add_argument(
        "--index",
        action="store_true",
        help="Indexar embeddings.json en ChromaDB (Fase 1)",
    )
    parser.add_argument(
        "--recreate-index",
        action="store_true",
        help="Borrar y recrear la colección Chroma antes de indexar",
    )
    parser.add_argument(
        "--query",
        type=str,
        help="Pregunta de prueba para retrieval (Fase 2)",
    )
    parser.add_argument(
        "--top-k",
        type=int,
        default=None,
        help="Sobrescribe TOP_K de config.py",
    )
    parser.add_argument(
        "--eval",
        action="store_true",
        help="Evaluar retrieval con preguntas_eval.json (Fase 3)",
    )

    args = parser.parse_args()

    if not any([args.check, args.prepare, args.index, args.query, args.eval]):
        parser.print_help()
        print(
            "\nEjemplo rápido:\n"
            "  python main.py --check\n"
            "  python main.py --prepare --index\n"
            '  python main.py --query "¿Qué mide la magnitud 83?"\n'
            "  python main.py --eval"
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

    if args.eval:
        _cmd_eval()


if __name__ == "__main__":
    main()
