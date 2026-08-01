"""Comprobaciones automáticas (demo 0) sin llamar a la API de Gemini."""

import inspect
import re

import pandas as pd

from config import DATA_DIR, ENTREGABLES_DIR, CSV_METEO

_MARCADOR_TODO = re.compile(r"\bTODO\b", re.IGNORECASE)


def _tiene_marcador_todo(texto: str) -> bool:
    return bool(_MARCADOR_TODO.search(texto))


def _funcion_pendiente(modulo, nombre: str) -> bool:
    """True si la función sigue con raise NotImplementedError."""
    fn = getattr(modulo, nombre, None)
    if fn is None or not inspect.isfunction(fn):
        return True
    try:
        codigo = inspect.getsource(fn)
    except OSError:
        codigo = ""
    return "NotImplementedError" in codigo


def verificar_load() -> tuple[bool, list[str]]:
    """Comprueba las funciones de ingesta en load.py con una fila real del CSV."""
    errores: list[str] = []

    try:
        import load as load_mod
    except ImportError as exc:
        return False, [f"No se pudo importar load.py: {exc}"]

    for nombre in ("nombre_magnitud", "fila_meteo_a_texto", "cargar_meteo_csv"):
        if _funcion_pendiente(load_mod, nombre):
            errores.append(f"Implementa {nombre}() en load.py")

    csv_path = DATA_DIR / CSV_METEO
    if not csv_path.is_file():
        errores.append(
            f"Falta {CSV_METEO} en data/. Comprueba que el corpus está en la carpeta data/."
        )
        return False, errores

    if errores:
        return False, errores

    # Prueba rápida con la primera fila del CSV
    try:
        df = pd.read_csv(csv_path, sep=";", nrows=1)
        fila = df.iloc[0]
        texto = load_mod.fila_meteo_a_texto(fila)
        if not texto or len(texto) < 80:
            errores.append(
                "fila_meteo_a_texto() debe devolver un texto legible con magnitud, fecha y horas"
            )
        if "magnitud" not in texto.lower() and "medición" not in texto.lower():
            errores.append("fila_meteo_a_texto() debería mencionar la magnitud o medición")
    except NotImplementedError:
        errores.append("Completa fila_meteo_a_texto() antes de continuar")
    except Exception as exc:
        errores.append(f"Error probando fila_meteo_a_texto(): {exc}")

    try:
        docs = load_mod.cargar_meteo_csv(csv_path)
        if len(docs) < 1:
            errores.append("cargar_meteo_csv() debe devolver al menos 1 Document")
        elif docs[0].metadata.get("tipo") != "meteo_medicion":
            errores.append("metadata['tipo'] debe ser 'meteo_medicion'")
    except NotImplementedError:
        errores.append("Completa cargar_meteo_csv() antes de continuar")
    except Exception as exc:
        errores.append(f"Error probando cargar_meteo_csv(): {exc}")

    return len(errores) == 0, errores


def verificar_entregables() -> tuple[bool, list[str]]:
    """Comprueba que los .md de entregables/ existen y no tienen TODO."""
    errores: list[str] = []
    estrategia = ENTREGABLES_DIR / "estrategia_chunking.md"
    reflexion = ENTREGABLES_DIR / "reflexion_pipeline.md"

    for path in (estrategia, reflexion):
        if not path.is_file():
            errores.append(f"Falta {path.name}")
            continue
        texto = path.read_text(encoding="utf-8")
        if _tiene_marcador_todo(texto):
            errores.append(f"Completa {path.name} (quedan marcadores TODO)")

    if estrategia.is_file():
        texto = estrategia.read_text(encoding="utf-8")
        if len(texto.strip()) < 350:
            errores.append("estrategia_chunking.md: añade más detalle (mín. ~350 caracteres)")

    if reflexion.is_file():
        texto = reflexion.read_text(encoding="utf-8")
        if len(texto.strip()) < 350:
            errores.append("reflexion_pipeline.md: añade más detalle (mín. ~350 caracteres)")

    return len(errores) == 0, errores
