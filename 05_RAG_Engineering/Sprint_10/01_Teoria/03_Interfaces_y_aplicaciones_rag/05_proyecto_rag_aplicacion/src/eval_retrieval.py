"""Evaluación del retrieval — Sprint 9."""

import json
from pathlib import Path

from config import QUERIES_EVAL_JSON, TOP_K, TOP_K_CANDIDATES

from .context import formatear_contexto
from .retriever import recuperar


def cargar_preguntas_eval(ruta: Path | None = None) -> list[dict]:
    ruta = ruta or QUERIES_EVAL_JSON
    if not ruta.exists():
        raise FileNotFoundError(f"No existe {ruta}")
    data = json.loads(ruta.read_text(encoding="utf-8"))
    return data.get("preguntas", [])


def _nombre_fuente_corto(metadata: dict) -> str:
    source = metadata.get("source", "?")
    return Path(str(source)).name


def evaluar_pregunta(pregunta: str, top_k: int) -> dict:
    chunks = recuperar(pregunta, top_k=top_k)
    mejor = chunks[0] if chunks else {}
    return {
        "pregunta": pregunta,
        "top_k": top_k,
        "hits": len(chunks),
        "mejor_id": mejor.get("id"),
        "mejor_distance": mejor.get("distance"),
        "mejor_fuente": _nombre_fuente_corto(mejor.get("metadata", {})),
        "contexto_preview": formatear_contexto(chunks[:1])[:300],
    }


def ejecutar_evaluacion(
    top_k_list: list[int] | None = None,
    mostrar_contexto: bool = False,
) -> list[dict]:
    preguntas = cargar_preguntas_eval()
    ks = top_k_list or TOP_K_CANDIDATES

    print("\n=== Evaluación del retrieval ===")
    print(f"Preguntas: {len(preguntas)} | Valores de K: {ks}\n")

    resultados: list[dict] = []

    for item in preguntas:
        texto = item["texto"]
        notas = item.get("notas", "")
        fuente_esperada = item.get("fuente_esperada", "")

        print(f"\n--- {item.get('id', '?')}: {texto} ---")
        if notas:
            print(f"  Notas: {notas}")
        if fuente_esperada:
            print(f"  Fuente esperada (orientativa): {fuente_esperada}")

        for k in ks:
            resumen = evaluar_pregunta(texto, top_k=k)
            resultados.append({**item, **resumen})
            print(
                f"  K={k} → mejor={resumen['mejor_fuente']} "
                f"distance={resumen['mejor_distance']}"
            )
            if mostrar_contexto and k == (TOP_K if TOP_K in ks else ks[0]):
                print(formatear_contexto(recuperar(texto, top_k=k)))

    print("\n=== Fin evaluación ===")
    return resultados
