"""Tests del contrato responder() (spec 000: RF-14, RF-15, RF-17).

Usan dobles de prueba: ni el retriever ni el LLM llaman a ninguna API.
"""

import pytest

import src.logic as logic


class Llamadas:
    def __init__(self):
        self.retriever = 0
        self.llm = 0


@pytest.fixture
def espia(monkeypatch):
    llamadas = Llamadas()

    def recuperar_falso(pregunta, top_k=None):
        llamadas.retriever += 1
        return [
            {"id": "chunk_1", "text": "Cine de verano gratuito en Hortaleza",
             "metadata": {"source": "data/agenda.csv"}, "distance": 0.2},
            {"id": "chunk_2", "text": "GRATUITO=1 significa gratis",
             "metadata": {"source": "data/faq_agenda_cultural.md"}, "distance": 0.3},
            {"id": "chunk_3", "text": "Más cine",
             "metadata": {"source": "data/agenda.csv"}, "distance": 0.35},
        ]

    def generar_falso(prompt):
        llamadas.llm += 1
        return "Sí, hay cine gratuito (agenda.csv)."

    monkeypatch.setattr(logic, "recuperar", recuperar_falso)
    monkeypatch.setattr(logic, "generar_respuesta", generar_falso)
    return llamadas


def test_pregunta_valida_devuelve_contrato_completo(espia):  # RF-17
    r = logic.responder("¿Hay cine gratuito en verano?")
    assert r["error"] is None
    assert r["respuesta"].startswith("Sí, hay cine")
    assert r["fuentes"] == ["agenda.csv", "faq_agenda_cultural.md"]
    assert len(r["chunks"]) == 3
    assert "--- Fragmento 1" in r["contexto"]
    assert espia.llm == 1


def test_pregunta_invalida_no_recupera_ni_llama_al_llm(espia):  # RF-14
    r = logic.responder("   ")
    assert r["error"]
    assert espia.retriever == 0 and espia.llm == 0


def test_sin_contexto_no_llama_al_llm(monkeypatch):  # RF-15
    llamadas = {"llm": 0}
    monkeypatch.setattr(logic, "recuperar", lambda pregunta, top_k=None: [])

    def generar_falso(prompt):
        llamadas["llm"] += 1
        return "no debería llamarse"

    monkeypatch.setattr(logic, "generar_respuesta", generar_falso)
    r = logic.responder("¿Hay cine gratuito en verano?")
    assert r["error"]
    assert llamadas["llm"] == 0
