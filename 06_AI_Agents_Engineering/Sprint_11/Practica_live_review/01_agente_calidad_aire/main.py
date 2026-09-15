"""CLI del agente calidad del aire.

Uso:
  python main.py
  python main.py --max-turns 2
  python main.py --interactivo
  python main.py --check
"""

import argparse
import json

import config
from src.agent import procesar_turno, run_demo
from src.state import crear_estado


def _interactivo(max_turns: int) -> dict:
    """Chat en terminal: el alumno escribe mensajes hasta max_turns / done / error."""
    estado = crear_estado("")
    print("Modo interactivo. Vacío o 'salir' para terminar.\n")
    for _ in range(max_turns):
        mensaje = input("Tú: ").strip()
        if not mensaje or mensaje.lower() in {"salir", "exit", "quit"}:
            break
        estado = procesar_turno(estado, mensaje)
        print("Agente:", estado.get("respuesta") or "(sin respuesta)")
        if estado.get("plan"):
            etiqueta = "Plan" if estado.get("done") else "Plan (borrador)"
            print(f"{etiqueta}:", estado["plan"])
        print("done:", estado.get("done"), "| error:", estado.get("error"))
        print()
        if estado.get("done") or estado.get("error"):
            break
    else:
        if not estado.get("done") and not estado.get("error"):
            aviso = "He parado por max_turns; esto es lo que llevo del plan."
            prev = (estado.get("respuesta") or "").strip()
            estado["respuesta"] = f"{prev}\n\n{aviso}".strip() if prev else aviso
    return estado


def _resumen(estado: dict, max_turns: int) -> None:
    """Print corto para ver límites sin bucear en el JSON."""
    traza = estado.get("traza") or []
    turnos = len(traza)

    if (
        not estado.get("done")
        and not estado.get("error")
        and turnos >= max_turns
    ):
        corte = f"max_turns ({max_turns})"
    elif estado.get("done"):
        corte = "ninguno (done=true)"
    elif estado.get("error"):
        corte = "error"
    else:
        corte = "ninguno"

    print("--- resumen ---")
    print(
        f"turnos: {turnos}/{max_turns} | done: {estado.get('done')} | "
        f"error: {bool(estado.get('error'))}"
    )
    print(f"corte: {corte}")
    print("---------------")


def main() -> None:
    parser = argparse.ArgumentParser(
        description="Agente calidad del aire"
    )
    parser.add_argument(
        "--interactivo",
        action="store_true",
        help="Chat por terminal turno a turno",
    )
    parser.add_argument("--max-turns", type=int, default=config.MAX_TURNS_DEFAULT)
    parser.add_argument(
        "--check",
        action="store_true",
        help="Comprueba que src/agent.py está implementado",
    )
    args = parser.parse_args()

    if args.check:
        from verificar import main as check_main

        raise SystemExit(check_main())

    if args.interactivo:
        resultado = _interactivo(args.max_turns)
    else:
        resultado = run_demo(max_turns=args.max_turns)

    _resumen(resultado, args.max_turns)
    print(json.dumps(resultado, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
