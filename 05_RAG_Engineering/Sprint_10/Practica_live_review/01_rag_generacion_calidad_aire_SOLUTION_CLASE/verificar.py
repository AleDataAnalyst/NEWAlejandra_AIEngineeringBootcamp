"""Comprobaciones --check de la capa Sprint 10."""

from __future__ import annotations

import inspect
import re
from pathlib import Path

from config import ENTREGABLES_DIR

_MARCADOR_TODO = re.compile(r"\bTODO\b", re.IGNORECASE)


def _funcion_pendiente(modulo, nombre: str) -> bool:
    fn = getattr(modulo, nombre, None)
    if fn is None or not inspect.isfunction(fn):
        return True
    try:
        codigo = inspect.getsource(fn)
    except OSError:
        codigo = ""
    return "NotImplementedError" in codigo


def verificar_prompts() -> tuple[bool, list[str]]:
    errores: list[str] = []
    try:
        import src.prompts as mod
    except ImportError as exc:
        return False, [str(exc)]
    if _funcion_pendiente(mod, "build_rag_prompt"):
        errores.append("Implementa build_rag_prompt() en src/prompts.py")
    return len(errores) == 0, errores


def verificar_generate() -> tuple[bool, list[str]]:
    errores: list[str] = []
    try:
        import src.generate as mod
    except ImportError as exc:
        return False, [str(exc)]
    if _funcion_pendiente(mod, "generar_respuesta"):
        errores.append("Implementa generar_respuesta() en src/generate.py")
    return len(errores) == 0, errores


def verificar_logic() -> tuple[bool, list[str]]:
    errores: list[str] = []
    try:
        import src.logic as mod
    except ImportError as exc:
        return False, [str(exc)]
    if _funcion_pendiente(mod, "responder"):
        errores.append("Implementa responder() en src/logic.py")
        return False, errores
    # Smoke: pregunta vacía no debe lanzar NotImplementedError
    try:
        r = mod.responder("   ")
        if not isinstance(r, dict) or not r.get("error"):
            errores.append(
                "responder('') debería devolver dict con clave error no vacía"
            )
    except NotImplementedError:
        errores.append("Implementa responder() en src/logic.py")
    except Exception as exc:  # noqa: BLE001
        errores.append(f"responder('') falló: {exc}")
    return len(errores) == 0, errores


def verificar_eval_generation() -> tuple[bool, list[str]]:
    errores: list[str] = []
    try:
        import src.eval_generation as mod
    except ImportError as exc:
        return False, [str(exc)]
    for nombre in ("evaluar_pregunta", "ejecutar_evaluacion"):
        if _funcion_pendiente(mod, nombre):
            errores.append(f"Implementa {nombre}() en src/eval_generation.py")
    return len(errores) == 0, errores


def verificar_app() -> tuple[bool, list[str]]:
    """app.py viene dado: solo comprobamos que sigue conectado a responder()."""
    app = Path(__file__).parent / "app.py"
    if not app.is_file():
        return False, ["Falta app.py"]
    texto = app.read_text(encoding="utf-8")
    if "from src.logic import responder" not in texto:
        return False, ["app.py debe importar responder desde src.logic (archivo dado)"]
    return True, []


def verificar_entregable() -> tuple[bool, list[str]]:
    errores: list[str] = []
    reflexion = ENTREGABLES_DIR / "reflexion_generacion.md"
    if not reflexion.is_file():
        return False, ["Falta entregables/reflexion_generacion.md"]
    texto = reflexion.read_text(encoding="utf-8")
    if _MARCADOR_TODO.search(texto):
        errores.append("Completa reflexion_generacion.md (quedan TODO)")
    if len(texto.strip()) < 350:
        errores.append("Añade más detalle al entregable (mín. ~350 caracteres)")
    return len(errores) == 0, errores
