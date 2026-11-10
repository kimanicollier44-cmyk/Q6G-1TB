"""Self-checks: every check is a real assertion over the real engines."""
from __future__ import annotations

from . import gates, network6g, payloads, qkd, quantum


def run_checks() -> dict:
    results = []

    def check(name, fn):
        try:
            ok = bool(fn())
            results.append((name, ok, "" if ok else "returned false"))
        except Exception as exc:  # report, don't hide
            results.append((name, False, str(exc)))

    check("bell_pair_entangled", lambda: _bell_ok())
    check("ghz3_probabilities", lambda: _ghz_ok())
    check("teleport_fidelity_gt_0.99", lambda: quantum.teleport()["fidelity"] > 0.99)
    check("grover_finds_marked", lambda: quantum.grover()["found"])
    check("grover_success_gt_0.9", lambda: quantum.grover()["success_probability"] > 0.9)
    check("link_meets_1tbps_at_100m", lambda: network6g.LinkConfig().meets_target())
    check("capacity_falls_with_distance", lambda: (
        network6g.LinkConfig(distance_m=1000).capacity_tbps()
        < network6g.LinkConfig(distance_m=100).capacity_tbps()))
    check("urllc_latency_met", lambda: network6g.LinkConfig().latency_ms()["meets_urllc"])
    check("speedtest_peak_near_capacity", lambda: (
        network6g.speedtest()["download_tbps_peak"] > 0.9))
    check("bb84_clean_key_ok", lambda: qkd.bb84(eve=False)["key_established"])
    check("bb84_eve_detected", lambda: qkd.bb84(eve=True)["eavesdropper_detected"])
    check("hold_gates_count_13", lambda: len(gates.HOLD_GATES) == 13)
    check("live_hardware_held", lambda: gates.is_held("live_qpu_hardware"))
    check("simulation_not_held", lambda: not gates.is_held("local_simulation"))
    check("chamber_never_executes", lambda: payloads.run_chamber()["all_executed"] is False)
    check("chamber_zero_network", lambda: payloads.run_chamber()["total_network_attempts"] == 0)
    check("chamber_holds_3_dangerous", lambda: payloads.run_chamber()["held"] == 3)
    check("chamber_allows_4_clean", lambda: payloads.run_chamber()["allowed"] == 4)
    passed = sum(1 for _, ok, _ in results if ok)
    return {"passed": passed, "total": len(results),
            "results": [{"check": n, "ok": ok, "detail": d} for n, ok, d in results],
            "all_passed": passed == len(results)}


def _bell_ok() -> bool:
    probs = quantum.bell_pair().probabilities()
    return abs(probs[0] - 0.5) < 1e-9 and abs(probs[3] - 0.5) < 1e-9 and probs[1] < 1e-9 and probs[2] < 1e-9


def _ghz_ok() -> bool:
    probs = quantum.ghz(3).probabilities()
    return abs(probs[0] - 0.5) < 1e-9 and abs(probs[7] - 0.5) < 1e-9
