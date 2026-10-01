"""Tests de la ingesta (spec 000: RF-3 a RF-6). No llaman a ninguna API."""

import pandas as pd
from langchain_core.documents import Document

from src.chunk import fragmentar_documentos
from src.clean import limpiar_documentos, normalizar_texto
from src.load import fila_a_texto


def _fila(**campos) -> pd.Series:
    return pd.Series(campos)


def test_fila_csv_se_convierte_en_texto_legible():  # RF-3
    fila = _fila(
        TITULO="10 vidas",
        DESCRIPCION="Película de animación",
        **{
            "TITULO-ACTIVIDAD": "Cine de verano en Hortaleza",
            "NOMBRE-INSTALACION": "Parque de Villa Rosa",
            "DISTRITO-INSTALACION": "HORTALEZA",
            "FECHA": "2026-08-21 00:00:00.0",
            "HORA": "22:00",
            "GRATUITO": "1",
        },
    )
    texto = fila_a_texto(fila)
    assert texto.startswith("Evento: 10 vidas")
    assert "Distrito: HORTALEZA" in texto
    assert "Hora: 22:00" in texto
    assert "Gratuito: sí" in texto


def test_fila_de_pago_indica_gratuito_no():  # RF-3
    texto = fila_a_texto(_fila(TITULO="Concierto", GRATUITO="0"))
    assert "Gratuito: no" in texto


def test_fila_sin_titulo_se_descarta():  # RF-4
    assert fila_a_texto(_fila(TITULO=float("nan"), GRATUITO="1")) is None
    assert fila_a_texto(_fila(TITULO="   ", GRATUITO="1")) is None


def test_normalizar_texto_colapsa_saltos_y_espacios():  # RF-5
    assert normalizar_texto("Hola\r\n\n\n\nmundo   con   espacios ") == "Hola\n\nmundo con espacios"


def test_limpieza_descarta_documentos_vacios():  # RF-5
    docs = [Document(page_content="  \n\n "), Document(page_content="Texto", metadata={"source": "a.md"})]
    limpios = limpiar_documentos(docs)
    assert len(limpios) == 1
    assert limpios[0].metadata["source"] == "a.md"


def test_fragmentos_llevan_indice_y_tamano():  # RF-6
    doc = Document(page_content="palabra " * 400, metadata={"source": "guia.txt"})
    chunks = fragmentar_documentos([doc])
    assert len(chunks) > 1
    assert [c.metadata["chunk_index"] for c in chunks] == list(range(len(chunks)))
    assert all(c.metadata["chunk_size"] == len(c.page_content) for c in chunks)
    assert all(c.metadata["source"] == "guia.txt" for c in chunks)
