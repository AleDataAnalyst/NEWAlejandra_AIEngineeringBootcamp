"""Punto de entrada del motor de búsqueda semántica (S8 + S9).

Une la preparación offline (ingesta, embeddings, indexación) con la
consulta interactiva y la evaluación.

Uso:
  python main.py --prepare              # ingesta + embeddings (S8)
  python main.py --index                # indexar en ChromaDB (S9)
  python main.py --prepare --index      # pipeline offline completo
  python main.py --query "pregunta"     # retrieval + contexto
  python main.py --eval                 # evaluación con preguntas fijas
"""

import argparse

from context import imprimir_contexto
from embed import ejecutar_embeddings
from eval_retrieval import ejecutar_evaluacion
from index import ejecutar_indexacion
from pipeline import ejecutar_ingesta
from retriever import recuperar


def _cmd_prepare() -> None:
    """Sprint 8: genera chunks.json y embeddings.json."""
    ejecutar_ingesta()
    print()
    ejecutar_embeddings()


def _cmd_index(recreate: bool) -> None:
    """Sprint 9: carga embeddings.json en ChromaDB."""
    total = ejecutar_indexacion(recreate=recreate)
    print(f"\nÍndice listo: {total} vectores en ChromaDB.")


def _cmd_query(pregunta: str, top_k: int | None) -> None:
    """Sprint 9: una pregunta → top-K chunks → contexto formateado."""
    chunks = recuperar(pregunta, top_k=top_k)
    imprimir_contexto(chunks)
    print("\n(Sprint 10: este contexto iría al prompt de Gemini.)")


def _cmd_eval() -> None:
    """Sprint 9: barrido de preguntas_eval.json con varios K."""
    ejecutar_evaluacion()


def main() -> None:
    parser = argparse.ArgumentParser(
        description="Motor de búsqueda semántica — agenda cultural Madrid"
    )
    parser.add_argument(
        "--prepare",
        action="store_true",
        help="Ingesta + embeddings (Sprint 8)",
    )
    parser.add_argument(
        "--index",
        action="store_true",
        help="Indexar embeddings.json en ChromaDB",
    )
    parser.add_argument(
        "--recreate-index",
        action="store_true",
        help="Borrar y recrear la colección Chroma antes de indexar",
    )
    parser.add_argument(
        "--query",
        type=str,
        help="Pregunta de prueba para retrieval",
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
        help="Evaluar retrieval con preguntas_eval.json",
    )

    args = parser.parse_args()

    if not any([args.prepare, args.index, args.query, args.eval]):
        parser.print_help()
        print(
            "\nEjemplo rápido:\n"
            "  python main.py --prepare --index\n"
            '  python main.py --query "¿Hay cine gratuito?"'
        )
        return

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
