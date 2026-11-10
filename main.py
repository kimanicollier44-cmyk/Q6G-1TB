#!/usr/bin/env python3
"""Q6G-1TB - 6G 1 Tbps Internet Quantum Computer (simulation).

One entry point. Zero dependencies (Python stdlib only).

Usage:
  python main.py demo        # full run: quantum + 6G link + QKD + council
  python main.py quantum     # Bell / GHZ / teleport / Grover
  python main.py network     # 1 Tbps link report + network slices
  python main.py speedtest   # simulated speed test
  python main.py qkd         # BB84, clean vs eavesdropped
  python main.py sandbox     # sandbox-api chamber: payload triage
  python main.py council     # Carbon 4 DECIDER + Muse advisor
  python main.py checks      # self-checks (exit 0 only if all pass)
  python main.py hold-demo   # shows a HOLD gate firing (exit 2)
"""
from __future__ import annotations

import argparse
import json
import sys

from q6g import checks, council, gates, network6g, payloads, qkd, quantum


def _print(obj) -> None:
    print(json.dumps(obj, indent=2))


def cmd_demo(_args) -> int:
    print("== ⚛️ QUANTUM CORE ==")
    _print({
        "bell_probabilities": [round(p, 4) for p in quantum.bell_pair().probabilities()],
        "teleport": quantum.teleport(),
        "grover": quantum.grover(),
    })
    print("== 📡 6G 1 TBPS LINK (modelled) ==")
    _print(network6g.LinkConfig().report())
    print("== 🚀 SIMULATED SPEED TEST ==")
    _print(network6g.speedtest())
    print("== 🔐 BB84 QKD (Q-SLICE security) ==")
    _print({"clean": qkd.bb84(eve=False), "with_eve": qkd.bb84(eve=True)})
    print("== 🧪 SANDBOX-API CHAMBER ==")
    _print(payloads.run_chamber())
    print("== 🧠 COUNCIL ==")
    _print(council.council_run("live deployment", risk=90))
    print(f"⛔ HOLD gates armed: {len(gates.HOLD_GATES)}")
    return 0


def cmd_sandbox(_args) -> int:
    _print(payloads.run_chamber())
    return 0


def cmd_quantum(_args) -> int:
    _print({
        "bell_probabilities": [round(p, 4) for p in quantum.bell_pair().probabilities()],
        "ghz3_probabilities": [round(p, 4) for p in quantum.ghz(3).probabilities()],
        "teleport": quantum.teleport(),
        "grover_4q_marked_11": quantum.grover(),
    })
    return 0


def cmd_network(_args) -> int:
    _print({"link": network6g.LinkConfig().report(), "slices": network6g.SLICES})
    return 0


def cmd_speedtest(_args) -> int:
    _print(network6g.speedtest())
    return 0


def cmd_qkd(_args) -> int:
    _print({"clean": qkd.bb84(eve=False), "with_eve": qkd.bb84(eve=True)})
    return 0


def cmd_council(_args) -> int:
    _print({
        "simulation_request": council.council_run("run local simulation", risk=10),
        "live_request": council.council_run("connect live carrier network", risk=90),
    })
    return 0


def cmd_checks(_args) -> int:
    result = checks.run_checks()
    _print(result)
    print(f"CHECKS {result['passed']}/{result['total']}")
    return 0 if result["all_passed"] else 1


def cmd_hold_demo(_args) -> int:
    try:
        gates.check("live_qpu_hardware")
        print("NOT HELD (unexpected)")
        return 1
    except gates.HoldGate as exc:
        print(str(exc))
        return 2


def main(argv=None) -> int:
    parser = argparse.ArgumentParser(prog="q6g-1tb", description=__doc__)
    sub = parser.add_subparsers(dest="cmd")
    for name, fn in [
        ("demo", cmd_demo), ("quantum", cmd_quantum), ("network", cmd_network),
        ("speedtest", cmd_speedtest), ("qkd", cmd_qkd), ("sandbox", cmd_sandbox),
        ("council", cmd_council),
        ("checks", cmd_checks), ("hold-demo", cmd_hold_demo),
    ]:
        p = sub.add_parser(name)
        p.set_defaults(fn=fn)
    args = parser.parse_args(argv)
    if not getattr(args, "fn", None):
        return cmd_demo(args)
    return args.fn(args)


if __name__ == "__main__":
    sys.exit(main())
