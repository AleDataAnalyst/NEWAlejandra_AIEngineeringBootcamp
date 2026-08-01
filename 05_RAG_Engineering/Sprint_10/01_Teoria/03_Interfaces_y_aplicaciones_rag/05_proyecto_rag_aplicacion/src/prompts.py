"""Construcción del prompt RAG — Sprint 10.

Separa instrucciones fijas, contexto recuperado y pregunta del usuario.
"""

INSTRUCCIONES_RAG = """Eres un asistente que responde preguntas sobre la agenda cultural de Madrid.

Reglas:
- Responde ÚNICAMENTE con la información del contexto proporcionado.
- Si el contexto no contiene información suficiente, indícalo explícitamente.
- Cuando cites un hecho, menciona la fuente si aparece en el contexto.
- No inventes eventos, fechas ni datos que no estén en el contexto.
"""


def build_rag_prompt(contexto: str, pregunta: str) -> str:
    """Ensambla el prompt completo para el LLM."""
    return (
        f"{INSTRUCCIONES_RAG}\n\n"
        f"--- CONTEXTO RECUPERADO ---\n"
        f"{contexto.strip()}\n\n"
        f"--- PREGUNTA ---\n"
        f"{pregunta.strip()}\n\n"
        f"--- RESPUESTA ---"
    )
