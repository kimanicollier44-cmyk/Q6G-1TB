"""6G network model targeting 1 Tbps peak.

Honest scope: a link-budget / capacity *model* and deterministic simulator.
Real 6G is not commercially deployed and no physical 1 Tbps link is
claimed. The model shows exactly which parameters reach 1 Tbps and
simulates throughput under distance / SNR / load.
"""
from __future__ import annotations

import math
import random
from dataclasses import dataclass, field

TARGET_TBPS = 1.0  # 1 terabit per second peak target


@dataclass(frozen=True)
class Band:
    name: str
    freq_ghz: float
    bandwidth_ghz: float

    @property
    def bandwidth_hz(self) -> float:
        return self.bandwidth_ghz * 1e9


BANDS = [
    Band("sub-6", 3.5, 0.1),
    Band("mmWave-28", 28.0, 1.0),
    Band("mmWave-60", 60.0, 2.0),
    Band("sub-THz-140", 140.0, 10.0),
    Band("THz-300", 300.0, 12.0),
]


def fspl_db(distance_m: float, freq_ghz: float) -> float:
    """Free-space path loss: 20log10(d_km) + 20log10(f_GHz) + 92.45."""
    d_km = max(distance_m, 1.0) / 1000.0
    return 20 * math.log10(d_km) + 20 * math.log10(freq_ghz) + 92.45


def beamforming_gain_db(n_antennas: int) -> float:
    return round(10 * math.log10(max(n_antennas, 1)), 2)


def shannon_efficiency(snr_db: float, max_bits_per_symbol: float = 12.0) -> float:
    """Spectral efficiency (bps/Hz/stream), Shannon capped by 4096-QAM."""
    snr_linear = 10 ** (snr_db / 10)
    return min(math.log2(1 + snr_linear), max_bits_per_symbol)


@dataclass
class LinkConfig:
    """One aggregated 6G link. Default config is engineered to hit 1 Tbps."""

    bands: list[Band] = field(default_factory=lambda: list(BANDS[2:]))  # 24 GHz total
    mimo_streams: int = 8
    antennas: int = 256
    tx_power_dbm: float = 30.0
    distance_m: float = 100.0
    overhead: float = 0.15  # coding / guard / protocol overhead
    base_snr_db: float = 20.0

    @property
    def total_bandwidth_ghz(self) -> float:
        return sum(b.bandwidth_ghz for b in self.bands)

    def snr_at_distance(self) -> float:
        ref_loss = fspl_db(100.0, 140.0)
        loss = sum(fspl_db(self.distance_m, b.freq_ghz) for b in self.bands) / len(self.bands)
        return round(self.base_snr_db - (loss - ref_loss) + beamforming_gain_db(self.antennas) - 24.08, 2)

    def capacity_bps(self) -> float:
        snr = self.snr_at_distance()
        eff = shannon_efficiency(snr)
        bw = self.total_bandwidth_ghz * 1e9
        return bw * eff * self.mimo_streams * (1 - self.overhead)

    def capacity_tbps(self) -> float:
        return self.capacity_bps() / 1e12

    def meets_target(self) -> bool:
        return self.capacity_tbps() >= TARGET_TBPS

    def latency_ms(self) -> dict:
        prop = (self.distance_m / 3e8) * 1000  # one-way propagation
        processing = 0.05   # 6G air-interface processing target
        queueing = 0.02
        total = prop + processing + queueing
        return {
            "propagation_ms": round(prop, 6),
            "processing_ms": processing,
            "queueing_ms": queueing,
            "total_ms": round(total, 4),
            "urllc_target_ms": 0.1,
            "meets_urllc": total <= 0.1,
        }

    def report(self) -> dict:
        return {
            "bands": [b.name for b in self.bands],
            "total_bandwidth_ghz": self.total_bandwidth_ghz,
            "mimo_streams": self.mimo_streams,
            "antennas": self.antennas,
            "beamforming_gain_db": beamforming_gain_db(self.antennas),
            "distance_m": self.distance_m,
            "snr_db": self.snr_at_distance(),
            "spectral_efficiency_bps_hz": round(shannon_efficiency(self.snr_at_distance()), 3),
            "capacity_tbps": round(self.capacity_tbps(), 4),
            "capacity_gbps": round(self.capacity_bps() / 1e9, 1),
            "target_tbps": TARGET_TBPS,
            "meets_1tbps_target": self.meets_target(),
            "latency": self.latency_ms(),
            "note": "Modelled capacity, not a measured physical link.",
        }


SLICES = [
    {
        "name": "eMBB+",
        "use": "Extreme broadband, XR, holographic media",
        "peak": "1 Tbps",
        "latency_ms": 1.0,
        "reliability": 0.99999,
    },
    {
        "name": "URLLC++",
        "use": "Industrial control, teleoperation, V2X",
        "peak": "10 Gbps",
        "latency_ms": 0.1,
        "reliability": 0.9999999,
    },
    {
        "name": "mMTC+",
        "use": "Massive IoT sensing",
        "peak": "100 Mbps",
        "latency_ms": 10.0,
        "density_per_km2": 10_000_000,
        "reliability": 0.999,
    },
    {
        "name": "Q-SLICE",
        "use": "Quantum-secured traffic (BB84 QKD keys)",
        "peak": "1 Gbps key-managed",
        "latency_ms": 1.0,
        "reliability": 0.99999,
    },
]


def speedtest(cfg: LinkConfig | None = None, seconds: int = 5, seed: int = 42) -> dict:
    """Deterministic simulated speed test (seeded, labelled simulated)."""
    cfg = cfg or LinkConfig()
    rng = random.Random(seed)
    cap = cfg.capacity_tbps()
    samples = []
    for i in range(seconds * 2):
        ramp = min(1.0, (i + 1) / 4)
        noise = rng.uniform(0.92, 1.0)
        samples.append(round(cap * ramp * noise, 4))
    peak = max(samples)
    avg = sum(samples[-4:]) / 4
    return {
        "simulated": True,
        "download_tbps_avg": round(avg, 4),
        "download_tbps_peak": round(peak, 4),
        "download_gbps_avg": round(avg * 1000, 1),
        "upload_ratio": 0.5,
        "upload_tbps_avg": round(avg * 0.5, 4),
        "ping_ms": cfg.latency_ms()["total_ms"],
        "jitter_ms": round(rng.uniform(0.005, 0.03), 4),
        "samples_tbps": samples,
    }
