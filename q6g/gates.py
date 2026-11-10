"""HOLD gates: actions this system will never do autonomously.

Simulation, modelling and local testing are always allowed.
Anything touching live hardware, live spectrum or live networks is HOLD.
"""
from __future__ import annotations

HOLD_GATES = [
    ("live_qpu_hardware", "Running on real quantum hardware"),
    ("live_carrier_6g_network", "Connecting to a live carrier 6G network"),
    ("rf_spectrum_transmission", "Transmitting on real RF / THz spectrum"),
    ("real_1tbps_physical_link", "Claiming or provisioning a physical 1 Tbps link"),
    ("live_entanglement_distribution", "Distributing entanglement over a live network"),
    ("user_traffic_routing", "Routing real user traffic"),
    ("spectrum_license_bypass", "Bypassing spectrum licensing"),
    ("encryption_bypass", "Bypassing encryption on any live system"),
    ("radio_firmware_flashing", "Flashing radio / baseband firmware"),
    ("satellite_uplink", "Transmitting to a satellite"),
    ("safety_critical_control", "Controlling medical / safety-critical systems"),
    ("live_network_reconfiguration", "Reconfiguring a live network autonomously"),
    ("live_sample_detonation", "Detonating a live/unknown sample outside the static sandbox-api chamber"),
    ("live_identifier_spoofing", "Deploying DI-MIXER spoofed device identifiers on a live network"),
    ("live_video_generation", "Rendering/generating video with Google Flow or any live generator"),
    ("live_gemini_api_call", "Calling the live Gemini / Carbon 4 API with a real key"),
]

_GATE_NAMES = {name for name, _ in HOLD_GATES}


class HoldGate(Exception):
    pass


def check(action: str) -> None:
    if action in _GATE_NAMES:
        raise HoldGate(f"HOLD: {action} requires Darion's explicit approval")


def is_held(action: str) -> bool:
    return action in _GATE_NAMES


def list_gates() -> list[dict]:
    return [{"gate": name, "description": desc} for name, desc in HOLD_GATES]
