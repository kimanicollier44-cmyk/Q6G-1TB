"""DI-MIXER seat - merged from Darion's credkellar/di-mixerx.

Verified on Docker Hub 2026-11-10: credkellar/di-mixerx - 227 pulls,
1 star, ACTIVE, "Defensive honeypot that generates dynamically
spoofed device identifiers to confuse attackers." No public source
repo exists for that image and no local implementation survived;
nothing here claims to be its source. This is Q6G-1TB's own defensive
implementation of the same idea.

What it does here: the 6G network presents a rotating pool of DECOY
device identities so a scanner fingerprints decoys, not real devices.

Hard safety rules, enforced by construction and by tests:
- Every identity is labelled SYNTHETIC.
- IPv4 addresses come ONLY from RFC 5737 TEST-NET ranges
  (192.0.2.0/24, 198.51.100.0/24, 203.0.113.0/24) - documentation
  addresses that never belong to a real host.
- IPv6 addresses come ONLY from the 2001:db8::/32 documentation prefix.
- MAC addresses always have the locally-administered bit set and the
  multicast bit clear - they can never collide with a factory MAC.
- Nothing is transmitted. Deploying spoofed identifiers on a live
  network is HOLD gate `live_identifier_spoofing`.
"""
from __future__ import annotations

import random

TEST_NETS = ["192.0.2", "198.51.100", "203.0.113"]
DEVICE_TYPES = ["gNB-small-cell", "IoT-sensor", "XR-headset", "vehicle-OBU",
                "industrial-PLC", "drone-UAV", "smart-meter", "edge-server"]
VENDORS = ["Q6G-Labs", "DecoyWorks", "SynthNet", "MirrorCell"]


def _mac(rng: random.Random) -> str:
    first = (rng.randint(0, 255) & 0b11111100) | 0b00000010  # local bit set, unicast
    rest = [rng.randint(0, 255) for _ in range(5)]
    return ":".join(f"{b:02x}" for b in [first, *rest])


def _ipv4(rng: random.Random) -> str:
    return f"{rng.choice(TEST_NETS)}.{rng.randint(1, 254)}"


def _ipv6(rng: random.Random) -> str:
    groups = [format(rng.randint(0, 0xFFFF), "x") for _ in range(4)]
    return "2001:db8:" + ":".join(groups)


def generate_identity(rng: random.Random, index: int) -> dict:
    device = rng.choice(DEVICE_TYPES)
    return {
        "id": f"decoy-{index:03d}",
        "synthetic": True,
        "label": "SYNTHETIC DECOY - not a real device",
        "mac": _mac(rng),
        "ipv4": _ipv4(rng),
        "ipv6": _ipv6(rng),
        "hostname": f"{device.lower()}-{index:03d}.decoy.local",
        "device_type": device,
        "vendor": rng.choice(VENDORS),
        "uptime_hours": rng.randint(1, 8760),
        "slice": rng.choice(["eMBB+", "URLLC++", "mMTC+", "Q-SLICE"]),
    }


def decoy_pool(n: int = 32, seed: int = 42) -> dict:
    """A pool of n synthetic decoy identities (deterministic by seed)."""
    rng = random.Random(seed)
    pool = [generate_identity(rng, i) for i in range(n)]
    macs = [p["mac"] for p in pool]
    return {
        "source_image": "credkellar/di-mixerx (227 pulls, Hub-verified 2026-11-10)",
        "provenance": "Native Q6G implementation of the DI-MixerX idea; no public source exists for the image.",
        "pool_size": len(pool),
        "unique_macs": len(set(macs)),
        "all_synthetic": all(p["synthetic"] for p in pool),
        "ipv4_ranges": "RFC 5737 TEST-NET only",
        "ipv6_range": "2001:db8::/32 documentation only",
        "rotation": "Pool regenerates per epoch; a scanner sees a moving target.",
        "transmitted": False,
        "identities": pool,
    }


def scanner_view(seed: int = 42) -> dict:
    """What an attacker's scan would conclude - all of it decoys."""
    pool = decoy_pool(32, seed=seed)
    types: dict[str, int] = {}
    for ident in pool["identities"]:
        types[ident["device_type"]] = types.get(ident["device_type"], 0) + 1
    return {
        "devices_seen": pool["pool_size"],
        "devices_real": 0,
        "device_types_seen": types,
        "conclusion": "Every visible device is a synthetic decoy; real devices are not in this view.",
    }
