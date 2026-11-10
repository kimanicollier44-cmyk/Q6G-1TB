"""BB84 quantum key distribution simulation for the 6G Q-SLICE.

Honest scope: classical simulation of the BB84 protocol. Detects an
eavesdropper via QBER > 11% exactly like the real protocol analysis.
No photons are transmitted.
"""
from __future__ import annotations

import random

QBER_ABORT = 0.11


def bb84(n_bits: int = 512, eve: bool = False, seed: int = 42) -> dict:
    rng = random.Random(seed)
    alice_bits = [rng.randint(0, 1) for _ in range(n_bits)]
    alice_bases = [rng.randint(0, 1) for _ in range(n_bits)]
    bob_bases = [rng.randint(0, 1) for _ in range(n_bits)]
    bob_bits = []
    for i in range(n_bits):
        bit = alice_bits[i]
        if eve:
            eve_basis = rng.randint(0, 1)
            if eve_basis != alice_bases[i]:
                bit = rng.randint(0, 1)  # Eve's wrong-basis measure randomises
        if bob_bases[i] != alice_bases[i]:
            bob_bits.append(rng.randint(0, 1))
        else:
            bob_bits.append(bit)
    sifted_a, sifted_b = [], []
    for i in range(n_bits):
        if alice_bases[i] == bob_bases[i]:
            sifted_a.append(alice_bits[i])
            sifted_b.append(bob_bits[i])
    errors = sum(1 for a, b in zip(sifted_a, sifted_b) if a != b)
    qber = errors / len(sifted_a) if sifted_a else 1.0
    aborted = qber > QBER_ABORT
    return {
        "raw_bits": n_bits,
        "sifted_key_length": 0 if aborted else len(sifted_a),
        "qber": round(qber, 4),
        "qber_abort_threshold": QBER_ABORT,
        "eve_present_simulated": eve,
        "eavesdropper_detected": bool(eve and aborted),
        "key_established": not aborted,
        "status": "ABORT - eavesdropping suspected" if aborted else "KEY OK",
    }
