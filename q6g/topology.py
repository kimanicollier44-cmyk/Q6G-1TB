"""Network management topology seat.

The topology engine is ported from Darion's LLM-X-NetLab
(llmx_netlab/netlab.py: build_topology / analyse_topology - bus, star,
ring, mesh, tree, BFS paths, single-point-of-failure analysis) and
re-pointed at 6G network management: gNB nodes, edge nodes and the
core, with per-topology resilience reporting for the modelled network.

Management scope: this analyses MODEL topologies only. Reconfiguring
a live network is HOLD gate `live_network_reconfiguration`.
"""
from __future__ import annotations

from collections import deque

KINDS = ["bus", "star", "ring", "mesh", "tree"]


def build_topology(kind: str, n: int) -> dict[int, set]:
    """Adjacency {node: set(neighbours)} for n nodes (0 = first)."""
    if n < 2:
        raise ValueError("a topology needs at least 2 nodes")
    adj: dict[int, set] = {i: set() for i in range(n)}

    def link(a: int, b: int) -> None:
        adj[a].add(b)
        adj[b].add(a)

    if kind == "bus":
        for i in range(n - 1):
            link(i, i + 1)
    elif kind == "star":
        for i in range(1, n):
            link(0, i)              # node 0 is the hub (core / central gNB)
    elif kind == "ring":
        for i in range(n):
            link(i, (i + 1) % n)
    elif kind == "mesh":
        for i in range(n):
            for j in range(i + 1, n):
                link(i, j)
    elif kind == "tree":
        for i in range(1, n):
            link((i - 1) // 2, i)
    else:
        raise ValueError(f"unknown topology: {kind}")
    return adj


def _path(adj: dict[int, set], src: int, dst: int):
    seen = {src}
    q = deque([(src, [src])])
    while q:
        node, path = q.popleft()
        if node == dst:
            return path
        for nb in adj[node]:
            if nb not in seen:
                seen.add(nb)
                q.append((nb, path + [nb]))
    return None


def analyse_topology(kind: str, n: int) -> dict:
    adj = build_topology(kind, n)
    links = sum(len(v) for v in adj.values()) // 2
    spof = []
    for cut in range(n):
        rest = {i: (adj[i] - {cut}) for i in range(n) if i != cut}
        nodes = list(rest)
        reached: set = set()
        stack = [nodes[0]] if nodes else []
        while stack:
            x = stack.pop()
            if x in reached:
                continue
            reached.add(x)
            stack.extend(rest[x] - reached)
        if len(reached) < len(nodes):
            spof.append(cut)
    worst = 0
    for i in range(n):
        for j in range(n):
            p = _path(adj, i, j)
            if p:
                worst = max(worst, len(p) - 1)
    return {"topology": kind, "nodes": n, "links": links,
            "worst_case_hops": worst, "single_points_of_failure": spof,
            "resilient": not spof}


def management_report(n: int = 8) -> dict:
    """Compare every topology for an n-node 6G management domain."""
    reports = [analyse_topology(kind, n) for kind in KINDS]
    resilient = [r["topology"] for r in reports if r["resilient"]]
    return {
        "domain": f"{n}-node 6G management domain (modelled)",
        "topologies": reports,
        "resilient_topologies": resilient,
        "recommendation": (
            "ring or mesh for the live design: no single point of failure. "
            "Star is cheapest but node 0 is a SPOF - if the hub dies, every "
            "spoke is cut off. (Recommendation for the model only; live "
            "reconfiguration is HOLD.)"),
        "live_reconfiguration": "HOLD",
    }
