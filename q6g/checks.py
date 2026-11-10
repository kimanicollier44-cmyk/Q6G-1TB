"""Self-checks: every check is a real assertion over the real engines."""
from __future__ import annotations

from . import (council, dimixer, ecosystem, flow, gates, network6g, payloads,
               qkd, quantum, topology)


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
    check("hold_gates_count_16", lambda: len(gates.HOLD_GATES) == 16)
    check("live_hardware_held", lambda: gates.is_held("live_qpu_hardware"))
    check("simulation_not_held", lambda: not gates.is_held("local_simulation"))
    check("chamber_never_executes", lambda: payloads.run_chamber()["all_executed"] is False)
    check("chamber_zero_network", lambda: payloads.run_chamber()["total_network_attempts"] == 0)
    check("chamber_holds_3_dangerous", lambda: payloads.run_chamber()["held"] == 3)
    check("chamber_allows_4_clean", lambda: payloads.run_chamber()["allowed"] == 4)
    check("dimixer_pool_all_synthetic", lambda: _dimixer_synthetic_ok())
    check("dimixer_scanner_sees_only_decoys", lambda: dimixer.scanner_view()["devices_real"] == 0)
    check("topology_star_spof_is_hub", lambda: topology.analyse_topology("star", 8)["single_points_of_failure"] == [0])
    check("topology_mesh_resilient", lambda: topology.analyse_topology("mesh", 8)["resilient"])
    check("flow_all_4_plan_only", lambda: _flow_ok())
    check("carbon4_full_seat_trace", lambda: _carbon_ok())
    check("ecosystem_router_decision_to_carbon", lambda: ecosystem.route("decision")["seat"] == "carbon-4")
    check("ecosystem_monitor_status_ok", lambda: ecosystem.monitor()["status"] == "OK")
    check("ecosystem_dashboard_and_registry", lambda: _ecosystem_ok())
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


def _dimixer_synthetic_ok() -> bool:
    pool = dimixer.decoy_pool(32)
    if not pool["all_synthetic"] or pool["transmitted"]:
        return False
    for ident in pool["identities"]:
        if not ident["ipv4"].rsplit(".", 1)[0] in dimixer.TEST_NETS:
            return False
        if not ident["ipv6"].startswith("2001:db8:"):
            return False
        first_octet = int(ident["mac"].split(":")[0], 16)
        if not (first_octet & 0b10) or (first_octet & 0b01):
            return False  # locally-administered bit must be set, multicast clear
    return True


def _flow_ok() -> bool:
    plan = flow.merged_plan()
    return plan["all_flows_used"] and plan["total_live_calls"] == 0 and not plan["anything_rendered"]


def _ecosystem_ok() -> bool:
    dash = ecosystem.dashboard()
    return ("KELLAR-ECOSYSTEM" in dash and len(ecosystem.COMPONENTS) == 10
            and ecosystem.threat_intake("t", b'{"code": "eval(x)"}')["verdict"] == "HOLD_IN_CHAMBER")


def _carbon_ok() -> bool:
    d = council.Carbon4().decide(90)
    return (d["phases"] == ["MAP", "MODEL", "STRESS", "DECIDE"]
            and d["verdict"] == "HOLD" and d["live_call_made"] is False
            and council.MuseAdvisor().advise("x")["authority"] == "none"
            and len(council.MuseAdvisor().advise("x")["advice"]) == 4)
