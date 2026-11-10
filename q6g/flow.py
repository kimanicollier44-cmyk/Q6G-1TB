"""Google Flow seat - all 4 flows, PLAN ONLY.

House pattern (same as Darion's other projects): FlowX, Workspace
Studio, Flow Filmmaking and the DataX google_flow seat produce plans,
storyboards and task lists. Nothing is rendered, sent or generated
live: live video generation is HOLD gate `live_video_generation`,
and every plan carries rendered=False and live_calls=0.
"""
from __future__ import annotations

FLOWX_SUBTASKS = [
    "ingest topic", "outline beats", "draft script", "split scenes",
    "write image prompts", "write motion prompts", "plan transitions",
    "plan captions", "plan voiceover", "assemble timeline",
    "export storyboard", "export shot list", "archive plan",
]


def flowx(topic: str) -> dict:
    return {"flow": "FlowX", "topic": topic,
            "subtasks": FLOWX_SUBTASKS, "subtask_count": len(FLOWX_SUBTASKS),
            "rendered": False, "live_calls": 0}


def workspace_studio(topic: str) -> dict:
    return {"flow": "Workspace Studio", "topic": topic,
            "plan": [f"Doc outline for '{topic}'", "Slide beats (5)",
                     "Speaker notes draft", "Share list: owner only"],
            "sent_anywhere": False, "rendered": False, "live_calls": 0}


def filmmaking(topic: str) -> dict:
    scenes = [
        {"track": "setup", "seconds": 6,
         "prompt": f"Title card: '{topic}' over a glowing quantum core and 6G towers, dark navy neon"},
        {"track": "explain", "seconds": 20,
         "prompt": f"Narrated walkthrough of {topic}: light streams carry data at 1 Tbps between towers"},
        {"track": "diagram", "seconds": 14,
         "prompt": f"Animated diagram for {topic}: qubits entangle, keys exchange, decoys rotate"},
        {"track": "recap", "seconds": 8,
         "prompt": "Recap card with the three key points, then the Q6G-1TB cover"},
    ]
    return {"flow": "Flow Filmmaking", "topic": topic,
            "tracks": ["setup", "explain", "diagram", "recap"],
            "scenes": scenes,
            "total_seconds": sum(s["seconds"] for s in scenes),
            "rendered": False, "live_calls": 0,
            "render": "HOLD - plan only; rendering needs Darion's own Google Flow access"}


def datax_flow(topic: str) -> dict:
    return {"flow": "DataX google_flow", "topic": topic,
            "plan": ["route topic to FlowX", "attach filmmaking storyboard",
                     "log plan in registry"],
            "rendered": False, "live_calls": 0}


def merged_plan(topic: str = "Q6G-1TB: the 1 Tbps quantum-secured 6G network") -> dict:
    flows = [flowx(topic), workspace_studio(topic), filmmaking(topic), datax_flow(topic)]
    return {"topic": topic, "flows": flows,
            "all_flows_used": len(flows) == 4,
            "total_live_calls": sum(f["live_calls"] for f in flows),
            "anything_rendered": any(f["rendered"] for f in flows)}
