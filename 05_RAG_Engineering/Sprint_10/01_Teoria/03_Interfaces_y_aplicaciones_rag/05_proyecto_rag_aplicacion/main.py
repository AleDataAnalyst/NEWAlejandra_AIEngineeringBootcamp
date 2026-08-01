"""Punto de entrada del pipeline RAG completo (S8 + S9 + S10).

Uso:
  python main.py --prepare              # ingesta + embeddings (S8)
  python main.py --index                # indexar en ChromaDB (S9)
  python main.py --prepare --index      # pipeline offline completo
  python main.py --query "pregunta"     # retrieval + contexto (S9)
  python main.py --ask "pregunta"       # RAG completo: respuesta generada (S10)
  python main.py --eval                 # evaluación del retrieval (S9)

App Streamlit: streamlit run app.py
"""

import argparse

from src.context import imprimir_contexto
from src.embed import ejecutar_embeddings
from src.eval_retrieval import ejecutar_evaluacion
from src.index import ejecutar_indexacion
from src.logic import responder
from src.pipeline import ejecutar_ingesta
from src.retriever import recuperar


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
    resultado = responder(pregunta, top_k=top_k)
    if resultado.get("error"):
        print(f"\n[ERROR] {resultado['error']}")
        if resultado.get("contexto"):
            print("\n--- Contexto (parcial) ---")
            print(resultado["contexto"])
        return

    print("\n--- Respuesta ---")
    print(resultado["respuesta"])
    if resultado.get("fuentes"):
        print("\n--- Fuentes ---")
        for fuente in resultado["fuentes"]:
            print(f"  - {fuente}")


def _cmd_eval() -> None:
    ejecutar_evaluacion()


def main() -> None:
    parser = argparse.ArgumentParser(
        description="RAG completo — agenda cultural Madrid (S8–S10)"
    )
    parser.add_argument("--prepare", action="store_true", help="Ingesta + embeddings")
    parser.add_argument("--index", action="store_true", help="Indexar en ChromaDB")
    parser.add_argument(
        "--recreate-index",
        action="store_true",
        help="Borrar y recrear la colección Chroma",
    )
    parser.add_argument("--query", type=str, help="Retrieval + contexto (S9)")
    parser.add_argument("--ask", type=str, help="RAG completo: respuesta generada (S10)")
    parser.add_argument("--top-k", type=int, default=None, help="Sobrescribe TOP_K")
    parser.add_argument("--eval", action="store_true", help="Evaluar retrieval")

    args = parser.parse_args()

    if not any([args.prepare, args.index, args.query, args.ask, args.eval]):
        parser.print_help()
        print(
            "\nEjemplo rápido:\n"
            "  python main.py --prepare --index\n"
            '  python main.py --ask "¿Hay cine gratuito en verano?"'
        )
        return

    if args.prepare:
        _cmd_prepare()
    if args.index:
        _cmd_index(recreate=args.recreate_index)
    if args.query:
        _cmd_query(args.query, args.top_k)
    if args.ask:
        _cmd_ask(args.ask, args.top_k)
    if args.eval:
        _cmd_eval()


if __name__ == "__main__":
    main()
