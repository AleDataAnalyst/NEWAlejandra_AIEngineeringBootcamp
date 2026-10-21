"""Comprobaciones locales — Live Review (alumno).

Uso:
  python verificar.py           # revisa TODOs en código (sin Gemini)
  python verificar.py --check   # además GET /health (TestClient)
"""

from __future__ import annotations

import argparse
import sys
from pathlib import Path


ROOT = Path(__file__).resolve().parent


def _leer(ruta: Path) -> str:
    return ruta.read_text(encoding="utf-8")


def _revisar_estatico() -> list[str]:
    fallos: list[str] = []

    # --- TODO 1: schemas ---
    schemas = _leer(ROOT / "schemas.py")
    bloque_askin = (
        schemas.split("class AskIn")[1].split("class ")[0]
        if "class AskIn" in schemas
        else ""
    )
    bloque_askout = (
        schemas.split("class AskOut")[1].split("class ")[0]
        if "class AskOut" in schemas
        else ""
    )
    bloque_approve = (
        schemas.split("class ApproveIn")[1].split("class ")[0]
        if "class ApproveIn" in schemas
        else ""
    )
    bloque_msg = (
        schemas.split("class MessageOut")[1]
        if "class MessageOut" in schemas
        else ""
    )
    if "pass" in bloque_askin or "min_length=1" not in bloque_askin:
        fallos.append("TODO 1: AskIn — define pregunta con Field(..., min_length=1, ...)")
    if "pass" in bloque_askout or "respuesta" not in bloque_askout:
        fallos.append("TODO 1: AskOut — define respuesta, thread_id, done, pendiente_hitl, error")
    if "pass" in bloque_approve or "min_length=1" not in bloque_approve:
        fallos.append("TODO 1: ApproveIn — thread_id con min_length=1 y aprobado bool")
    if "pass" in bloque_msg or "role:" not in bloque_msg:
        fallos.append("TODO 1: MessageOut — define role, content, created_at opcional")
    if "TODO 1" in schemas:
        fallos.append("TODO 1: quita comentarios TODO en schemas.py al completar")

    # --- TODO 2: models ---
    models = _leer(ROOT / "src" / "models.py")
    bloque_conv = (
        models.split("class Conversation")[1].split("class ")[0]
        if "class Conversation" in models
        else ""
    )
    bloque_msg_model = (
        models.split("class Message")[1] if "class Message" in models else ""
    )

    def _campo_real(bloque: str, nombre: str) -> bool:
        """True si hay una línea de campo activa (no comentario) tipo `nombre:`."""
        for line in bloque.splitlines():
            s = line.strip()
            if s.startswith("#"):
                continue
            if s.startswith(f"{nombre}:") or s.startswith(f"{nombre} :"):
                return True
        return False

    if "pass" in bloque_conv or not _campo_real(bloque_conv, "created_at"):
        fallos.append("TODO 2: Conversation — define id (PK) y created_at")
    if "pass" in bloque_msg_model or not _campo_real(bloque_msg_model, "thread_id"):
        fallos.append("TODO 2: Message — define id, thread_id (FK), role, content, created_at")
    if "foreign_key" not in bloque_msg_model:
        fallos.append('TODO 2: Message.thread_id debe usar Field(..., foreign_key="conversation.id")')
    if "TODO 2" in models:
        fallos.append("TODO 2: quita comentarios TODO en models.py al completar")

    # --- TODO 3: save_turn ---
    db_src = _leer(ROOT / "src" / "db.py")
    bloque_save = (
        db_src.split("def save_turn")[1].split("def ")[0]
        if "def save_turn" in db_src
        else ""
    )
    if "NotImplementedError" in bloque_save:
        fallos.append("TODO 3: save_turn sigue con NotImplementedError")
    elif "session.add" not in bloque_save:
        fallos.append("TODO 3: save_turn debe hacer session.add (Conversation/Message)")
    if "TODO 3" in bloque_save:
        fallos.append("TODO 3: quita comentarios TODO en save_turn al completar")

    # --- TODO 4: POST /ask ---
    app_src = _leer(ROOT / "app.py")
    bloque_ask = (
        app_src.split("def ask")[1].split("def ")[0]
        if "def ask" in app_src
        else ""
    )
    if "NotImplementedError" in bloque_ask:
        fallos.append("TODO 4: POST /ask sigue con NotImplementedError")
    else:
        if "procesar_turno" not in bloque_ask:
            fallos.append("TODO 4: /ask debe llamar a procesar_turno")
        if "_persistir_si_hay_respuesta" not in bloque_ask and "save_turn" not in bloque_ask:
            fallos.append(
                "TODO 4: /ask debe persistir el turno (save_turn o _persistir_si_hay_respuesta)"
            )

    # --- TODO 5: GET messages ---
    bloque_msgs = (
        app_src.split("def get_messages")[1]
        if "def get_messages" in app_src
        else ""
    )
    if "NotImplementedError" in bloque_msgs:
        fallos.append("TODO 5: GET /threads/.../messages sigue con NotImplementedError")
    elif "list_messages" not in bloque_msgs:
        fallos.append("TODO 5: get_messages debe llamar a db.list_messages")
    elif "MessageOut" not in bloque_msgs:
        fallos.append("TODO 5: get_messages debe devolver MessageOut")

    if "procesar_turno" not in app_src:
        fallos.append("app.py debe importar procesar_turno desde src.agent")

    return fallos


def _check_health() -> list[str]:
    fallos: list[str] = []
    try:
        import os

        # Solo para importar app (gemini_auth exige la variable); no se llama al LLM.
        os.environ.setdefault("GEMINI_API_KEY", "verificar-dummy")

        from fastapi.testclient import TestClient

        from app import app
    except Exception as exc:  # noqa: BLE001
        return [f"No se pudo importar la app: {exc}"]

    client = TestClient(app)
    r = client.get("/health")
    if r.status_code != 200 or r.json().get("status") != "ok":
        fallos.append(f"/health falló: {r.status_code} {r.text}")
    if r.json().get("storage") != "sqlite":
        fallos.append('/health debe incluir "storage": "sqlite"')
    return fallos


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--check",
        action="store_true",
        help="Prueba GET /health con TestClient (no llama a Gemini)",
    )
    args = parser.parse_args()

    fallos = _revisar_estatico()
    if args.check:
        if any("TODO" in f for f in fallos):
            print("Hay TODOs pendientes; --check solo tiene sentido cuando /ask esté listo.")
        fallos.extend(_check_health())

    if fallos:
        print("Pendiente:")
        for f in fallos:
            print(f"  - {f}")
        return 1

    print("OK: checks estructurales" + (" y /health" if args.check else ""))
    return 0


if __name__ == "__main__":
    sys.exit(main())
