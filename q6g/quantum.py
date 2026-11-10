"""Quantum core: pure-stdlib statevector simulator (1-12 qubits).

Honest scope: this is a classical simulation of a quantum computer.
No live QPU hardware is claimed or accessed.
"""
from __future__ import annotations

import cmath
import math
import random

MAX_QUBITS = 12


class QuantumCircuit:
    def __init__(self, n_qubits: int, seed: int = 42):
        if not 1 <= n_qubits <= MAX_QUBITS:
            raise ValueError(f"n_qubits must be 1..{MAX_QUBITS}")
        self.n = n_qubits
        self.size = 1 << n_qubits
        self.state = [0j] * self.size
        self.state[0] = 1.0 + 0j
        self.rng = random.Random(seed)

    # -- single-qubit gates -------------------------------------------------
    def _apply_single(self, qubit: int, m):
        step = 1 << qubit
        for base in range(0, self.size, step * 2):
            for off in range(step):
                i0 = base + off
                i1 = i0 + step
                a0, a1 = self.state[i0], self.state[i1]
                self.state[i0] = m[0][0] * a0 + m[0][1] * a1
                self.state[i1] = m[1][0] * a0 + m[1][1] * a1
        return self

    def h(self, q: int):
        s = 1 / math.sqrt(2)
        return self._apply_single(q, [[s, s], [s, -s]])

    def x(self, q: int):
        return self._apply_single(q, [[0, 1], [1, 0]])

    def y(self, q: int):
        return self._apply_single(q, [[0, -1j], [1j, 0]])

    def z(self, q: int):
        return self._apply_single(q, [[1, 0], [0, -1]])

    def s(self, q: int):
        return self._apply_single(q, [[1, 0], [0, 1j]])

    def rx(self, q: int, theta: float):
        c, s = math.cos(theta / 2), -1j * math.sin(theta / 2)
        return self._apply_single(q, [[c, s], [s, c]])

    def ry(self, q: int, theta: float):
        c, sn = math.cos(theta / 2), math.sin(theta / 2)
        return self._apply_single(q, [[c, -sn], [sn, c]])

    def rz(self, q: int, theta: float):
        return self._apply_single(
            q, [[cmath.exp(-1j * theta / 2), 0], [0, cmath.exp(1j * theta / 2)]]
        )

    # -- two-qubit gates ----------------------------------------------------
    def cnot(self, control: int, target: int):
        cs, ts = 1 << control, 1 << target
        for i in range(self.size):
            if (i & cs) and not (i & ts):
                j = i | ts
                self.state[i], self.state[j] = self.state[j], self.state[i]
        return self

    def cz(self, control: int, target: int):
        cs, ts = 1 << control, 1 << target
        for i in range(self.size):
            if (i & cs) and (i & ts):
                self.state[i] = -self.state[i]
        return self

    def swap(self, a: int, b: int):
        self.cnot(a, b).cnot(b, a).cnot(a, b)
        return self

    # -- measurement ----------------------------------------------------------
    def probabilities(self) -> list[float]:
        return [abs(a) ** 2 for a in self.state]

    def measure(self, qubit: int) -> int:
        step = 1 << qubit
        p1 = sum(abs(self.state[i]) ** 2 for i in range(self.size) if i & step)
        bit = 1 if self.rng.random() < p1 else 0
        norm = math.sqrt(p1 if bit else 1 - p1) or 1.0
        for i in range(self.size):
            if bool(i & step) != bool(bit):
                self.state[i] = 0j
            else:
                self.state[i] /= norm
        return bit

    def measure_all(self) -> int:
        probs = self.probabilities()
        r, acc = self.rng.random(), 0.0
        for i, p in enumerate(probs):
            acc += p
            if r <= acc:
                return i
        return self.size - 1


def bell_pair(seed: int = 42) -> QuantumCircuit:
    qc = QuantumCircuit(2, seed=seed)
    qc.h(0).cnot(0, 1)
    return qc


def ghz(n: int = 3, seed: int = 42) -> QuantumCircuit:
    qc = QuantumCircuit(n, seed=seed)
    qc.h(0)
    for q in range(1, n):
        qc.cnot(0, q)
    return qc


def teleport(bit_alpha: float = 0.6, seed: int = 7) -> dict:
    """Teleport one qubit state |psi> = alpha|0> + beta|1> to qubit 2.

    Returns the recovered amplitudes on qubit 2 after corrections.
    Deterministic statevector check (no sampling): the final state's
    qubit-2 reduced amplitudes must equal (alpha, beta) up to phase.
    """
    beta = math.sqrt(max(0.0, 1 - bit_alpha**2))
    qc = QuantumCircuit(3, seed=seed)
    # prepare |psi> on qubit 0 via RY: alpha=cos(t/2)
    theta = 2 * math.acos(bit_alpha)
    qc.ry(0, theta)
    qc.h(1).cnot(1, 2)          # Bell pair on 1-2
    qc.cnot(0, 1).h(0)          # Bell measurement basis change
    # Coherent form of the classical corrections: X on q2 controlled by
    # q1, Z on q2 controlled by q0. After these gates q2 disentangles
    # and holds |psi> exactly, whichever branch measurement would give.
    qc.cnot(1, 2).cz(0, 2)
    # Trace out q0/q1: recovered amplitude magnitudes on q2.
    p0 = sum(abs(a) ** 2 for i, a in enumerate(qc.state) if not (i & 4))
    p1 = sum(abs(a) ** 2 for i, a in enumerate(qc.state) if (i & 4))
    amp0, amp1 = math.sqrt(p0), math.sqrt(p1)
    return {
        "alpha_in": bit_alpha,
        "beta_in": round(beta, 6),
        "alpha_out": round(amp0, 6),
        "beta_out": round(amp1, 6),
        "fidelity": round(abs(bit_alpha * amp0 + beta * amp1), 6),
        "corrections": "X controlled by q1, Z controlled by q0 (coherent)",
    }


def grover(n_qubits: int = 4, marked: int = 11, iterations: int | None = None) -> dict:
    """Grover search: amplify `marked` among 2**n_qubits states."""
    if marked >= (1 << n_qubits):
        raise ValueError("marked out of range")
    if iterations is None:
        iterations = max(1, round(math.pi / 4 * math.sqrt(1 << n_qubits)))
    qc = QuantumCircuit(n_qubits, seed=1)
    for q in range(n_qubits):
        qc.h(q)
    for _ in range(iterations):
        # oracle: phase-flip marked state via multi-controlled Z (emulated)
        qc.state[marked] = -qc.state[marked]
        # diffusion: 2|s><s| - I applied directly on amplitudes
        mean = sum(qc.state) / qc.size
        qc.state = [2 * mean - a for a in qc.state]
    probs = qc.probabilities()
    best = max(range(qc.size), key=lambda i: probs[i])
    return {
        "n_qubits": n_qubits,
        "marked": marked,
        "iterations": iterations,
        "best": best,
        "success_probability": round(probs[marked], 4),
        "found": best == marked,
    }
