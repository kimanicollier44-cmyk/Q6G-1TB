import pathlib
import sys

sys.path.insert(0, str(pathlib.Path(__file__).resolve().parents[1]))

from q6g import (checks, council, dimixer, ecosystem, flow, gates, network6g,
                 payloads, qkd, quantum, topology)


def test_bell():
    probs = quantum.bell_pair().probabilities()
    assert abs(probs[0] - 0.5) < 1e-9 and abs(probs[3] - 0.5) < 1e-9


def test_grover():
    result = quantum.grover()
    assert result["found"] and result["success_probability"] > 0.9


def test_teleport():
    assert quantum.teleport()["fidelity"] > 0.99


def test_capacity_meets_1tbps():
    report = network6g.LinkConfig().report()
    assert report["meets_1tbps_target"], report


def test_capacity_falls_with_distance():
    near = network6g.LinkConfig(distance_m=100).capacity_tbps()
    far = network6g.LinkConfig(distance_m=1000).capacity_tbps()
    assert far < near


def test_latency_urllc():
    assert network6g.LinkConfig().latency_ms()["meets_urllc"]


def test_speedtest_simulated_labelled():
    result = network6g.speedtest()
    assert result["simulated"] is True and result["download_tbps_peak"] > 0.9


def test_bb84_clean():
    assert qkd.bb84(eve=False)["key_established"]


def test_bb84_eve_detected():
    result = qkd.bb84(eve=True)
    assert result["eavesdropper_detected"] and not result["key_established"]


def test_hold_gate():
    assert gates.is_held("rf_spectrum_transmission")
    try:
        gates.check("live_qpu_hardware")
        raise AssertionError("gate did not fire")
    except gates.HoldGate:
        pass


def test_council_strictest_wins():
    result = council.council_run("live deployment", risk=90)
    assert result["final"] == "HOLD"
    assert result["advice"]["authority"] == "none"


def test_chamber_counts():
    result = payloads.run_chamber()
    assert result["total"] == 7 and result["allowed"] == 4 and result["held"] == 3


def test_chamber_never_executes_no_network():
    result = payloads.run_chamber()
    assert result["all_executed"] is False
    assert result["total_network_attempts"] == 0


def test_chamber_verdicts():
    verdicts = {r["name"]: r["verdict"] for r in payloads.run_chamber()["runs"]}
    assert verdicts["quantum-circuit-bell"] == "ALLOW_STATIC_STUDY"
    assert verdicts["payload-eval-marker"] == "HOLD_IN_CHAMBER"
    assert verdicts["payload-socket-attempt"] == "HOLD_IN_CHAMBER"


def test_dimixer_synthetic_ranges():
    pool = dimixer.decoy_pool(16)
    assert pool["all_synthetic"] and pool["unique_macs"] == 16
    for ident in pool["identities"]:
        assert ident["ipv4"].rsplit(".", 1)[0] in dimixer.TEST_NETS
        assert ident["ipv6"].startswith("2001:db8:")
        first = int(ident["mac"].split(":")[0], 16)
        assert first & 0b10 and not first & 0b01


def test_dimixer_scanner_view():
    view = dimixer.scanner_view()
    assert view["devices_seen"] == 32 and view["devices_real"] == 0


def test_topology_star_spof():
    result = topology.analyse_topology("star", 8)
    assert result["single_points_of_failure"] == [0]


def test_topology_mesh_resilient():
    result = topology.analyse_topology("mesh", 8)
    assert result["resilient"] and result["worst_case_hops"] == 1


def test_flow_plan_only():
    plan = flow.merged_plan()
    assert plan["all_flows_used"] and plan["total_live_calls"] == 0
    assert plan["anything_rendered"] is False


def test_carbon4_full_seat():
    d = council.Carbon4().decide(10)
    assert d["model"] == "google/gemini-carbon-4-extended-pro-thinking"
    assert d["phases"] == ["MAP", "MODEL", "STRESS", "DECIDE"]
    assert d["live_call_made"] is False
    assert len(council.MuseAdvisor().advise("t")["advice"]) == 4


def test_ecosystem_router():
    assert ecosystem.route("decision")["seat"] == "carbon-4"
    assert ecosystem.route("advice")["seat"] == "muse"
    assert ecosystem.route("payload_triage")["seat"] == "sandbox-api"
    assert ecosystem.route("nonsense")["seat"] is None


def test_ecosystem_monitor():
    m = ecosystem.monitor()
    assert m["status"] == "OK" and m["link_meets_target"] and m["live_network"] is False
    assert m["decoys_active"] == 32


def test_ecosystem_threat_intake_and_dashboard():
    held = ecosystem.threat_intake("t", b'{"code": "socket.connect(x)"}')
    assert held["verdict"] == "HOLD_IN_CHAMBER" and held["executed_sample_code"] is False
    assert "KELLAR-ECOSYSTEM" in ecosystem.dashboard()
    assert len(ecosystem.COMPONENTS) == 10


def test_all_checks_pass():
    result = checks.run_checks()
    assert result["all_passed"], result
