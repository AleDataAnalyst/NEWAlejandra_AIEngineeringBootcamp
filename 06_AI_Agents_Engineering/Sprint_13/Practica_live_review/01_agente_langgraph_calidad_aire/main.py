"""CLI Live Review S13 — calidad del aire + LangGraph.

  python main.py
  python main.py --check
  python main.py --interactivo
  python main.py --sin-auto-aprobar
"""

from __future__ import annotations

import argparse
import json

import config
from src.agent import aprobar_plan, procesar_turno, run_demo
from src.state import crear_estado


def _interactivo(max_turns: int, max_steps: int) -> dict:
    estado = crear_estado("")
    print("Modo interactivo. Vacío o 'salir' para terminar.")
    print("Si hay plan pendiente: escribe 'aprobar' o 'rechazar'.\n")
    for _ in range(max_turns):
        if estado.get("pendiente_hitl"):
            print("HITL: plan pendiente. Escribe aprobar / rechazar")
            for item in estado.get("plan") or []:
                print(f"  - {item}")
        mensaje = input("Tú: ").strip()
        if not mensaje or mensaje.lower() in {"salir", "exit", "quit"}:
            break
        if mensaje.lower() in {"aprobar", "approve", "si", "sí", "yes"}:
            if estado.get("pendiente_hitl"):
                estado = aprobar_plan(estado, True)
            else:
                print("(No hay plan pendiente)")
                continue
        elif mensaje.lower() in {"rechazar", "reject", "no"}:
            if estado.get("pendiente_hitl"):
                estado = aprobar_plan(estado, False)
            else:
                print("(No hay plan pendiente)")
                continue
        else:
            estado = procesar_turno(estado, mensaje, max_steps=max_steps)
        print("Agente:", estado.get("respuesta") or "(sin respuesta)")
        if estado.get("plan"):
            print("Plan:", estado["plan"])
        print(
            "done:",
            estado.get("done"),
            "| hitl:",
            estado.get("pendiente_hitl"),
            "| error:",
            estado.get("error"),
        )
        print()
        if estado.get("done") or estado.get("error"):
            break
    return estado


def _resumen(estado: dict, max_turns: int, max_steps: int) -> None:
    traza = estado.get("traza") or []
    turnos = len(traza)
    ultimo_tools = []
    if traza:
        ultimo_tools = [
            t.get("tool") for t in (traza[-1].get("tools") or []) if t.get("tool")
        ]
    print("--- resumen ---")
    print(
        f"turnos: {turnos}/{max_turns} | done: {estado.get('done')} "
        f"| hitl: {estado.get('pendiente_hitl')} | error: {bool(estado.get('error'))}"
    )
    print(f"tools último turno: {ultimo_tools or '(ninguna)'}")
    print(f"max_steps config: {max_steps}")
    print("---------------")


def main() -> None:
    parser = argparse.ArgumentParser(description="LR S13 · aire + LangGraph")
    parser.add_argument("--check", action="store_true", help="verificar TODOs")
    parser.add_argument("--interactivo", action="store_true")
    parser.add_argument("--max-turns", type=int, default=config.MAX_TURNS_DEFAULT)
    parser.add_argument("--max-steps", type=int, default=config.MAX_STEPS_DEFAULT)
    parser.add_argument("--sin-auto-aprobar", action="store_true")
    args = parser.parse_args()

    if args.check:
        from verificar import main as check_main

        raise SystemExit(check_main())

    if args.interactivo:
        resultado = _interactivo(args.max_turns, args.max_steps)
    else:
        resultado = run_demo(
            max_turns=args.max_turns,
            max_steps=args.max_steps,
            auto_aprobar=not args.sin_auto_aprobar,
        )

    _resumen(resultado, args.max_turns, args.max_steps)
    print(json.dumps(resultado, ensure_ascii=False, indent=2, default=str))


if __name__ == "__main__":
    main()
