"""Evaluación del retrieval — Sprint 9 (Fase 3).

Objetivo didáctico
------------------
No basta con “parece que funciona”. Aquí barres un set fijo de preguntas
(queries/preguntas_eval.json) con varios valores de K y observas:
  - ¿Recupera la fuente esperada (FAQ vs CSV)?
  - ¿Cómo cambia el mejor hit al subir K?
  - ¿Qué pasa con una pregunta fuera de corpus (p. ej. capital de Francia)?

Esto es evaluación del RETRIEVAL (no del LLM). La reflexión escrita va en
entregables/reflexion_retrieval.md.

Funciones a completar:
  - evaluar_pregunta()
  - ejecutar_evaluacion()

Helpers ya dados:
  - cargar_preguntas_eval, _nombre_fuente_corto
  - recuperar() (Fase 2), formatear_contexto (context.py)

Prueba: python main.py --eval
"""

import json
from pathlib import Path

from config import QUERIES_EVAL_JSON, TOP_K, TOP_K_CANDIDATES
from context import formatear_contexto
from retriever import recuperar


def cargar_preguntas_eval(ruta: Path | None = None) -> list[dict]:
    """Lee el JSON con preguntas de prueba.

    Cada pregunta puede traer:
      - id, texto
      - fuente_esperada (orientativa: no es un test automático)
      - notas (pista pedagógica para el alumno)
    """
    ruta = ruta or QUERIES_EVAL_JSON
    if not ruta.exists():
        raise FileNotFoundError(f"No existe {ruta}")
    data = json.loads(ruta.read_text(encoding="utf-8"))
    return data.get("preguntas", [])


def _nombre_fuente_corto(metadata: dict) -> str:
    """Solo el nombre de fichero (más legible que la ruta completa)."""
    source = metadata.get("source", "?")
    return Path(str(source)).name


def evaluar_pregunta(pregunta: str, top_k: int) -> dict:
    """Una pregunta + un K → resumen del mejor hit y preview del contexto.

    Idea: encapsular “una corrida de retrieval” en un dict fácil de imprimir
    y de copiar a la reflexión.

    Nota: el “mejor” hit es el primero porque Chroma ya ordena por distancia.

    Pasos:
      1. chunks = recuperar(pregunta, top_k=top_k)
      2. mejor = chunks[0] si hay hits, si no {}
      3. return un dict con:
           pregunta, top_k, hits,
           mejor_id, mejor_distance, mejor_fuente,
           contexto_preview  (p. ej. formatear_contexto(chunks[:1])[:300])
    """
    # 1) Reutilizamos el retriever de la Fase 2 (misma ruta que --query)
    # 2) Chroma ya ordena por distancia → el primero es el “mejor” hit
    # 3) Dict resumen + preview corto para la reflexión
    raise NotImplementedError("Implementa evaluar_pregunta() en eval_retrieval.py")


def ejecutar_evaluacion(
    top_k_list: list[int] | None = None,
    mostrar_contexto: bool = False,
) -> list[dict]:
    """Barrido completo: todas las preguntas × varios valores de K.

    Por defecto usa TOP_K_CANDIDATES de config.py (típicamente [1, 3, 5]).

    Cómo usarlo en la reflexión:
      - Compara FAQ vs CSV en q1–q4.
      - Mira si K=5 mete ruido.
      - En la pregunta fuera de corpus, las distances suelen ser peores o
        muy parecidas entre sí (señal de “no hay evidencia”).

    Pasos:
      1. preguntas = cargar_preguntas_eval()
         ks = top_k_list or TOP_K_CANDIDATES
         Imprimir cabecera (nº de preguntas y valores de K).
      2. Para cada pregunta del JSON:
           - Imprimir id, texto, notas y fuente_esperada (si existen).
             fuente_esperada es orientativa: sirve para razonar, no para assert.
           - Para cada k en ks:
               resumen = evaluar_pregunta(texto, top_k=k)
               Loguear: K=… → mejor=… distance=…
               (Opcional) si mostrar_contexto, imprimir formatear_contexto(...)
      3. return la lista de resultados (útil si más adelante guardas un informe).
    """
    # 1) Cargar set fijo de preguntas y decidir qué K probar
    # 2) Por cada pregunta: contexto pedagógico + barrido de K
    # 3) Devolver resultados acumulados
    raise NotImplementedError("Implementa ejecutar_evaluacion() en eval_retrieval.py")
