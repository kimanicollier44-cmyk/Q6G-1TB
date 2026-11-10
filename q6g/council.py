"""Council: Carbon 4 DECIDER (can only tighten) + Muse advisor (authority: none).

Strictest outcome wins. Muse advises; it can never lift a HOLD gate
or loosen a Carbon 4 decision.
"""
from __future__ import annotations

import os

TIERS = (2048, 8192, 32768)


class Carbon4:
    """Deterministic decider over a risk score 0..100. Can only tighten."""

    def decide(self, risk: float) -> dict:
        if risk >= 75:
            verdict, tier = "HOLD", TIERS[2]
        elif risk >= 40:
            verdict, tier = "REVIEW", TIERS[1]
        else:
            verdict, tier = "ALLOW_SIM", TIERS[0]
        return {"brain": "Carbon 4", "role": "DECIDER", "verdict": verdict,
                "thinking_tier": tier, "risk": risk}


class MuseAdvisor:
    """Advisory seat. Key is names-only: only the env var NAME is read
    to report presence; the value is never printed or stored."""

    def __init__(self):
        key_name = "MODEL_API_KEY"
        self.key_present = bool(os.environ.get(key_name))
        self.key_name = key_name

    def advise(self, topic: str) -> dict:
        advice = [
            f"Keep '{topic}' inside simulation until independently measured.",
            "Report modelled 1 Tbps as modelled, never as a measured link.",
            "QBER above 11% must abort the key, no exceptions.",
        ]
        return {"brain": "Muse (Meta Model API)", "role": "advisor",
                "authority": "none", "key_name": self.key_name,
                "key_present": self.key_present, "advice": advice}


def council_run(topic: str, risk: float) -> dict:
    decision = Carbon4().decide(risk)
    advice = MuseAdvisor().advise(topic)
    # Strictest wins; advisor cannot override.
    final = decision["verdict"]
    return {"topic": topic, "decision": decision, "advice": advice,
            "final": final, "rule": "strictest-wins; advisor authority = none"}
