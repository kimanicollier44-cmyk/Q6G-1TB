"""Kellar-Ecosystem seat - merged from Darion's credkellar/kellar-ecosystem.

Verified on Docker Hub 2026-11-10: credkellar/kellar-ecosystem -
341 pulls, 1 star, ACTIVE, "AI-driven cybersecurity engine w/
real-time monitoring, dynamic LLM routing, [AI] threat sandbox. UI"
(Hub short description, truncated by Hub at ~100 chars; full
description empty). No public source repo exists for that image;
nothing here claims to be its source. This is Q6G-1TB's own
implementation of the same four ideas, over Q6G's own components:

1. Real-time monitoring - a health monitor over the modelled 6G
   network: link capacity, QKD key status, chamber holds, decoy
   pool, topology resilience -> status + alerts.
2. Dynamic LLM routing - a deterministic router that sends each
   task type to the right seat (decisions to Carbon 4, advice to
   Muse, video plans to Google Flow, payloads to the chamber,
   identity questions to DI-MIXER, map questions to topology).
   Offline: the router returns the seat NAME and the local seat's
   own output; it makes no live API call (live calls are HOLD).
3. Threat sandbox - threat intake is routed to the merged
   sandbox-api chamber (q6g/payloads.py), never handled ad hoc.
4. UI - a plain-text dashboard rendering of the whole ecosystem.
"""
from __future__ import annotations

from . import council, dimixer, flow, network6g, payloads, qkd, topology

COMPONENTS = [
    ("quantum-core", "q6g/quantum.py", "statevector 1-12 qubits"),
    ("6g-link", "q6g/network6g.py", "1 Tbps modelled link + slices"),
    ("qkd", "q6g/qkd.py", "BB84 quantum keys"),
    ("sandbox-api", "q6g/payloads.py", "static chamber, never executes"),
    ("di-mixer", "q6g/dimixer.py", "synthetic decoy identities"),
    ("topology", "q6g/topology.py", "management topology + SPOF"),
    ("google-flow", "q6g/flow.py", "4 flows, plan only"),
    ("carbon-4", "q6g/council.py", "Gemini Carbon 4 DECIDER"),
    ("muse", "q6g/council.py", "Muse advisor, authority none"),
    ("kellar-ecosystem", "q6g/ecosystem.py", "monitor + router + UI"),
]

ROUTES = {
    "decision": ("carbon-4", "Decisions always go to the DECIDER seat."),
    "advice": ("muse", "Advice goes to the advisor seat (authority: none)."),
    "video_plan": ("google-flow", "Video work is planned by the Flow seat, never rendered."),
    "payload_triage": ("sandbox-api", "Payloads go to the chamber before any analysis."),
    "identity": ("di-mixer", "Identity/decoy questions go to the DI-MIXER seat."),
    "network_map": ("topology", "Map/resilience questions go to the topology seat."),
    "key_exchange": ("qkd", "Key work goes to the BB84 seat."),
    "link_status": ("6g-link", "Link questions go to the 6G engine."),
}


def route(task_type: str) -> dict:
    """Dynamic routing: task type -> seat, deterministically, offline."""
    if task_type not in ROUTES:
        return {"task_type": task_type, "seat": None,
                "reason": "unknown task type - routed to council for a decision",
                "live_call_made": False}
    seat, reason = ROUTES[task_type]
    return {"task_type": task_type, "seat": seat, "reason": reason,
            "live_call_made": False}


def monitor() -> dict:
    """Real-time monitor over the modelled ecosystem (one live pass)."""
    link = network6g.LinkConfig().report()
    key = qkd.bb84(eve=False)
    chamber = payloads.run_chamber()
    topo = topology.management_report()
    alerts = []
    if not link["meets_1tbps_target"]:
        alerts.append("CAPACITY: modelled link below 1 Tbps target at current distance")
    if not key["key_established"]:
        alerts.append("QKD: clean-channel key failed to establish")
    if chamber["held"]:
        alerts.append(f"CHAMBER: {chamber['held']} payload(s) held in the sandbox")
    spof_kinds = [t["topology"] for t in topo["topologies"] if t["single_points_of_failure"]]
    if spof_kinds:
        alerts.append(f"TOPOLOGY: SPOF present in {', '.join(spof_kinds)} models")
    return {
        "link_tbps": link["capacity_tbps"],
        "link_meets_target": link["meets_1tbps_target"],
        "latency_ms": link["latency"]["total_ms"],
        "qkd_key_established": key["key_established"],
        "chamber_held": chamber["held"],
        "chamber_allowed": chamber["allowed"],
        "decoys_active": dimixer.scanner_view()["devices_seen"],
        "resilient_topologies": topo["resilient_topologies"],
        "alerts": alerts,
        "status": "OK" if link["meets_1tbps_target"] and key["key_established"] else "ATTENTION",
        "live_network": False,
    }


def threat_intake(payload_name: str, data: bytes) -> dict:
    """Threat sandbox intake: everything goes through the chamber."""
    from .payloads import analyse_payload
    from .sandbox_api import detonate_static
    result = detonate_static(payload_name, data, analyse_payload)
    return {"intake": "kellar-ecosystem threat sandbox",
            "verdict": result["report"]["verdict"],
            "fingerprints": result["report"]["fingerprints"],
            "executed_sample_code": result["telemetry"]["executed_sample_code"],
            "network_attempts": result["telemetry"]["network_attempts"]}


def dashboard() -> str:
    """The UI: a plain-text dashboard of the whole ecosystem."""
    m = monitor()
    lines = [
        "+--------------------------------------------------------------+",
        "|  KELLAR-ECOSYSTEM  -  Q6G-1TB control dashboard (modelled)   |",
        "+--------------------------------------------------------------+",
        f"|  6G link        : {m['link_tbps']:.2f} Tbps modelled  target met: {m['link_meets_target']}",
        f"|  Latency        : {m['latency_ms']} ms",
        f"|  QKD key        : {'ESTABLISHED' if m['qkd_key_established'] else 'FAILED'}",
        f"|  Chamber        : {m['chamber_allowed']} allowed / {m['chamber_held']} held (never executes)",
        f"|  Decoys (DI-MIXER): {m['decoys_active']} synthetic, 0 real",
        f"|  Resilient maps : {', '.join(m['resilient_topologies'])}",
        f"|  Status         : {m['status']}",
        "+--------------------------------------------------------------+",
        "  Components:",
    ]
    for name, path, what in COMPONENTS:
        lines.append(f"   - {name:<17} {path:<22} {what}")
    lines.append("  Alerts:")
    for alert in m["alerts"]:
        lines.append(f"   ! {alert}")
    lines.append("  Live network: NO - simulation only, HOLD gates armed.")
    return "\n".join(lines)
