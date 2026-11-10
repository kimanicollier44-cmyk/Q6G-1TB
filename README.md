![Q6G-1TB cover](assets/cover.png)

# 📡⚛️ Q6G-1TB — 6G 1 Tbps Internet Quantum Computer

**🌐 A 6G network that targets 1 terabit per second, guarded by a quantum computer, with a sandbox-api chamber checking every payload before it is studied — all in one pure-Python project.**

👨‍💻 By Darion Kellar · 📜 MIT License · 🐍 Python stdlib only, zero dependencies · 🏷️ v1.1.0

![Python](https://img.shields.io/badge/Python-3.12-3776AB?logo=python&logoColor=white)
![Docker](https://img.shields.io/badge/Docker-ready-2496ED?logo=docker&logoColor=white)
![License](https://img.shields.io/badge/License-MIT-green)
![Dependencies](https://img.shields.io/badge/dependencies-0-brightgreen)
![Version](https://img.shields.io/badge/version-1.1.0-blue)
![GitHub](https://img.shields.io/badge/GitHub-credkellar%2FQ6G--1TB-181717?logo=github)

---

## 🔄 Updated Workflows

Two workflows ship in `workflow-pack/` — paste each one into `.github/workflows/` on GitHub (the App cannot write workflow files, so this paste is the owner's step):

| Workflow | File to create | What it does |
|---|---|---|
| ✅ CI | `.github/workflows/ci.yml` | On every push + pull request: Python 3.12 → install pytest → `pytest tests/ -q` → `python main.py checks` |
| 🐳 Docker Publish | `.github/workflows/docker-publish.yml` | On push to `main`: Docker Hub login from secrets → build + push `credkellar/q6g-1tb:latest` |

Secrets needed (repo → Settings → Secrets → Actions): `DOCKERHUB_USERNAME`, `DOCKERHUB_TOKEN`.

[![CI](https://img.shields.io/badge/CI-pending%20paste-yellow)](https://github.com/credkellar/Q6G-1TB/actions/workflows/ci.yml)
[![Docker Publish](https://img.shields.io/badge/Docker%20Publish-pending%20paste-yellow)](https://github.com/credkellar/Q6G-1TB/actions/workflows/docker-publish.yml)

> ⚠️ **Honest badge note:** the two badges above are static on purpose. The real `badge.svg` URLs were checked live and return **404** until the workflow files are pasted and run for the first time — after that, swap these for the live workflow badges. Every other badge in this README was checked live: **HTTP 200**.

```mermaid
flowchart LR
    P[📤 Push to credkellar/Q6G-1TB] --> CI[✅ CI workflow<br/>pytest 15 + CHECKS 18/18]
    P --> DP[🐳 Docker Publish workflow]
    DP --> S{🔑 DOCKERHUB secrets set?}
    S -->|yes| HUB[🐳 credkellar/q6g-1tb:latest]
    S -->|no| HOLD[⛔ Publish waits for owner]
```

---

## 🧰 Tech Stack Badges & Full Architecture Tech Stack

![pytest](https://img.shields.io/badge/pytest-15%20passed-brightgreen)
![CHECKS](https://img.shields.io/badge/CHECKS-18%2F18-brightgreen)
![Quantum](https://img.shields.io/badge/quantum-12%20qubits-blueviolet)
![6G](https://img.shields.io/badge/6G-1%20Tbps%20modelled-cyan)
![HOLD gates](https://img.shields.io/badge/HOLD%20gates-13-red)
![sandbox-api](https://img.shields.io/badge/sandbox--api-merged-orange)

### 💻 Core Programming Languages & Core Systems
- 🐍 **Python 3.12** — the whole system, one language
- 📚 **Standard library only** — `cmath`, `math`, `random`, `hashlib`, `tempfile`, `argparse`, `json`; zero pip installs
- ⚛️ **Statevector quantum engine** — complex-amplitude simulation, 1–12 qubits

### ⛓️ Web3 & Infrastructure
- 🚫 **No blockchain** — honestly none; this is a network + quantum project
- 🔐 **BB84 quantum key distribution** — the security layer for the Q-SLICE
- 🧪 **sandbox-api chamber** — merged from Darion's own `credkellar/sandbox-api` line (8,393 pulls when first catalogued); the chamber code here is copied **verbatim** (sha256 `28b3365c…`) from his MonadDB-RE implementation of it

### ⚙️ Platform Support & Hardware Architecture
- 🖥️ **Any OS** that runs Python 3.12 (Linux, macOS, Windows, Termux)
- 📡 **Modelled radio** — 256-antenna massive MIMO, 8 streams, bands at 60 / 140 / 300 GHz (modelled, not physical hardware)
- 🐳 **Docker** — `python:3.12-slim`, non-root user

### ⚡ Low-Level Infrastructure & Performance
- 🧮 **Real link math** — Shannon capacity + free-space path loss, computed live on every report
- 🎯 **Deterministic seeds** — every simulation is reproducible run-to-run
- 🪶 **No heavy deps** — the full test suite runs in under a second

### 🔧 DevOps & Build Tools
- ✅ **GitHub Actions CI** — pytest + self-checks (paste step, see Updated Workflows)
- 🐳 **Docker Publish** — to Docker Hub `credkellar/q6g-1tb`
- 🧪 **pytest** — 15 tests · 🔎 **built-in CHECKS** — 18/18

### ☁️ Cloud Providers
- 🚫 **None required** — everything runs locally, offline
- 🧠 **Optional brain seat** — Muse via the Meta Model API (`MODEL_API_KEY`, names-only, advisory only, pay-as-you-go — never labelled free)

```mermaid
flowchart TD
    U[👤 User] --> MAIN[🚪 main.py CLI]
    MAIN --> Q[⚛️ quantum.py]
    MAIN --> N[📡 network6g.py]
    MAIN --> K[🔐 qkd.py]
    MAIN --> SB[🧪 payloads.py] --> SA[📦 sandbox_api.py<br/>verbatim chamber]
    MAIN --> C[🧠 council.py]
    MAIN --> G[⛔ gates.py]
    MAIN --> CH[🔎 checks.py]
    Q --> K
    C --> G
    CH --> Q
    CH --> N
    CH --> SB
```

---

## ❓ What is this about?

📖 This project is about the **next internet after 5G** — called **6G** — and the **quantum computers** that will help run and protect it.

Three ideas are joined into one machine:

1. 📡 **Speed** — a 6G link designed to reach **1 terabit per second** (1,000,000,000,000 bits every second).
2. ⚛️ **Quantum** — a quantum computer core that can hold many answers at once, teleport a quantum state, and search a haystack the fast quantum way.
3. 🛡️ **Safety** — quantum keys that reveal any spy, a sandbox chamber that studies payloads without ever running them, and hard HOLD gates on everything live.

⚠️ It is a **working simulation and model**, honestly labelled: real 6G is not commercially deployed yet, and no physical 1 Tbps link or live quantum hardware is claimed. The math, the quantum circuits, the key exchange, and the chamber all really run.

## 🎯 What this does?

Step by step, one `python main.py demo` run:

1. ⚛️ Builds a **Bell pair** — two qubits linked so measuring one fixes the other (probabilities 0.5 / 0 / 0 / 0.5).
2. 🌀 Builds a **GHZ state** — three qubits in one shared state.
3. ✨ **Teleports** a qubit state from qubit 0 to qubit 2 and measures the recovery: **fidelity 1.0**.
4. 🔍 Runs **Grover search** on 4 qubits and finds the marked state with **96.13%** success probability.
5. 📡 Computes the **6G link**: 24 GHz of aggregated bandwidth × 8 MIMO streams × Shannon efficiency at the modelled SNR → **1.10 Tbps at 100 m**.
6. ⏱️ Checks **latency**: 0.0703 ms total — inside the 0.1 ms URLLC++ target.
7. 🚀 Runs a **simulated speed test** (labelled simulated in its own output): ~1.04 Tbps average.
8. 🔐 Runs **BB84 QKD** twice — clean channel gets a key; with an eavesdropper the error rate jumps past 11% and the key **aborts**.
9. 🧪 Sends **7 payloads through the sandbox-api chamber** — 4 clean ones are allowed for static study, 3 dangerous ones (eval, socket, shell markers) are **held**, nothing is executed, network attempts = 0.
10. 🧠 Asks the **council**: Carbon 4 decides, Muse advises (authority: none), strictest wins.
11. ⛔ Confirms all **13 HOLD gates** are armed.

## ⚙️ How this works?

### 📡 The 1 Tbps math (derived, not typed)

`capacity = bandwidth × log2(1 + SNR) × MIMO streams × (1 − overhead)`

| Piece | Value |
|---|---|
| 📶 Aggregated bandwidth | 24 GHz (2 @ 60 GHz + 10 @ 140 GHz + 12 @ 300 GHz) |
| 🔀 MIMO streams | 8 |
| 📡 Antennas | 256 (beamforming gain ≈ 24.08 dB) |
| 📊 SNR @ 100 m | 20.25 dB (from free-space path loss `20·log10(d_km) + 20·log10(f_GHz) + 92.45`) |
| 🧮 Spectral efficiency | 6.74 bps/Hz/stream |
| ✂️ Overhead | 15% |
| 🏁 **Modelled capacity** | **1.10 Tbps ✅** |

Move the receiver to 1 km and the same formula drops below target — a test asserts that falloff, because that is the physics talking.

### ⚛️ The quantum core
A statevector of complex amplitudes. Gates (H, X, Y, Z, S, Rx, Ry, Rz, CNOT, CZ, SWAP) rewrite the amplitudes; measurement samples them. Teleportation uses the coherent form of the classical corrections (X controlled by qubit 1, Z controlled by qubit 0), so the recovered state can be checked exactly instead of statistically.

### 🔐 The quantum keys
BB84: Alice sends bits in random bases, Bob measures in random bases, they keep only the matching-basis bits. An eavesdropper must guess bases and corrupts about 25% of the sifted key — past the 11% abort line, so the key is thrown away and the spy is exposed.

### 🧪 The chamber
Every payload is data only. The chamber writes it to a throwaway folder, runs a static marker scan, records telemetry (sha256, bytes, FS diff, trace, budgets), and deletes the folder. It imports no socket machinery at all: network attempts are 0 **by design**, and sample code executed is always `False`.

### 🧠 The council
Carbon 4 is the DECIDER (risk ≥ 75 → HOLD, ≥ 40 → REVIEW, else ALLOW_SIM; thinking tiers 2048 / 8192 / 32768; it can only tighten). Muse is an advisor with authority **none** — its key is names-only (`MODEL_API_KEY`), the value is never printed or stored. Strictest outcome wins.

## 😎 Why is this is cool?

Because it takes three things people usually only draw on slides — 6G, 1 Tbps, and a quantum computer — and turns them into code you can run, measure, and break, in under a second, with nothing to install.

### 🔟 10 reasons why this is cool

1. 🏁 The **1 Tbps number is derived** from real formulas live — change the distance or antennas and it moves.
2. ✨ **Teleportation fidelity is measured** (1.0), not asserted — it failed at 0.96 during development and the circuit was fixed until the math closed.
3. 🔍 **Grover really amplifies** the marked state to 96.13% — quantum search, not a lookup.
4. 🕵️ **BB84 catches its spy the real way** — QBER past 11% aborts the key.
5. 🧪 The **sandbox-api chamber** studies payloads with executed = False and network = 0 on every single run, proven by tests.
6. 📉 **Capacity falloff with distance is a test**, not a hope — the model is not allowed to flatter itself.
7. 🏷️ The **speed test labels itself simulated** inside its own output — no fake flexing.
8. 🪶 **Zero dependencies** — the entire future internet runs on the Python standard library.
9. 🧠 The **advisor can never override the decider** — the council is built so advice cannot loosen a HOLD.
10. ⛔ **13 named HOLD gates** stand between this simulation and the live world — hardware, spectrum, carrier networks, all of it.

## 🧩 What problems this solves?

1. 🤷 **"6G" is mostly marketing slides.** → This gives it equations, defaults, and tests you can argue with.
2. 🔢 **Peak-speed claims are usually just typed.** → Here 1 Tbps falls out of bandwidth × Shannon × streams, and falls apart honestly at distance.
3. 🎓 **Quantum computing feels untouchable.** → Bell, GHZ, teleportation, and Grover run in ~180 lines of readable stdlib Python.
4. 🔓 **Future networks need new security.** → BB84 shows quantum keys that expose eavesdroppers by physics, not by trust.
5. 💣 **Studying unknown payloads is dangerous.** → The chamber analyses them as data only, in a throwaway folder, with budgets.
6. 🧪 **Demos hide their failures.** → CHECKS (18/18) and pytest (15) are part of the program, and the demo prints raw outputs.
7. 🏷️ **Simulations pretend to be measurements.** → Every output that is modelled or simulated says so in itself.
8. 📦 **Big installs kill curiosity.** → Zero dependencies: clone, run, done.
9. 🤖 **AI advisors get too much power in other systems.** → Here Muse advises and Carbon 4 decides; strictest wins, always.
10. 🌍 **One repo per idea fragments the work.** → Network, quantum, security, chamber, and council live behind **one** `main.py`.

### 🔟 10 solutions (the short list)

1. ✅ Formula-first link budget (Shannon + FSPL) instead of a typed headline number.
2. ✅ Distance-falloff test so the model cannot overclaim.
3. ✅ Statevector simulator with exact fidelity checks.
4. ✅ BB84 with a hard 11% QBER abort.
5. ✅ Static chamber: no execution, no sockets, step + time budgets, FS-diff telemetry.
6. ✅ Marker-scan triage: eval / socket / shell payloads are held automatically (3 of 7 demo payloads).
7. ✅ Deterministic seeds — every number in this README reproduces.
8. ✅ Self-labelling outputs: "modelled" and "simulated" travel with the data.
9. ✅ Council with tighten-only decider and a no-authority advisor.
10. ✅ 13 HOLD gates + a hold-demo that exits 2, so the boundary is testable too.

## 💾 How to install this? Step-by-step

1. 🐍 Install **Python 3.12** (any OS).
2. 📥 Clone the repo:
   ```bash
   git clone https://github.com/credkellar/Q6G-1TB.git
   cd Q6G-1TB
   ```
3. 🚀 Run the full demo — nothing to install first:
   ```bash
   python main.py demo
   ```
4. 🎛️ Or run one part at a time:
   ```bash
   python main.py quantum     # ⚛️ Bell / GHZ / teleport / Grover
   python main.py network     # 📡 1 Tbps link report + slices
   python main.py speedtest   # 🚀 simulated speed test
   python main.py qkd         # 🔐 BB84 clean vs eavesdropped
   python main.py sandbox     # 🧪 chamber triage of 7 payloads
   python main.py council     # 🧠 Carbon 4 + Muse
   python main.py checks      # 🔎 self-checks (CHECKS 18/18)
   python main.py hold-demo   # ⛔ HOLD gate fires, exit 2
   ```
5. 🧪 (Optional) Run the test suite:
   ```bash
   pip install pytest
   python -m pytest tests/ -q   # 15 passed
   ```
6. 🐳 (Optional) Run it in Docker:
   ```bash
   docker build -t q6g-1tb .
   docker run --rm q6g-1tb demo
   ```
7. 🔄 (Owner step) Paste `workflow-pack/ci.yml` and `workflow-pack/docker-publish.yml` into `.github/workflows/`, add the two Docker Hub secrets, and CI + publishing go live.
8. 🖼️ (Owner step) Upload `assets/cover.png` to the repo — binary files cannot ride the App push, so the cover is an upload step.

## 📋 Requirements?

- 🐍 **Python 3.12+** — required. Nothing else.
- 📦 **pip packages: none** for running. `pytest` only if you want the test suite.
- 🐳 **Docker: optional**, only for the container run.
- 🔑 **API keys: none** for the simulation. `MODEL_API_KEY` only names the optional Muse advisor seat; the system runs fully without it.
- 🌐 **Internet: not required** — every engine is local and deterministic.
- 💻 **Hardware: any** machine that runs Python — the quantum sim caps at 12 qubits so it stays light.

## 🧒 Explain in 5th grade English

Imagine the internet is a road for tiny cars that carry messages. 🚗

5G is a good road. This project draws a **super road** called 6G that is so wide, a **trillion** tiny cars can drive on it every second. That is what "1 Tbps" means — one trillion bits, every single second. 🏁

Next to the road is a special kind of computer called a **quantum computer**. A normal computer thinks about one answer at a time. A quantum computer can hold **many answers at once**, like holding a whole handful of keys and trying the right one super fast. ⚛️

The quantum computer also makes **magic keys** for locking messages. If a spy tries to peek at a magic key, the key breaks — so we always know someone peeked, and we throw that key away. 🔐

Before any new package is opened, it goes into a **glass box room** (the sandbox chamber). We look at it through the glass, take notes, and never, ever run it. If it looks dangerous, it stays in the box. 🧪

And there is a **rule keeper** (Carbon 4) and a **helper** (Muse). The helper can give ideas, but only the rule keeper makes decisions, and the keeper can only make rules *stricter*, never weaker. ⛔

None of this is plugged into the real world. It is a **model** — like a toy city that follows the real rules — so we can learn exactly how the real one should work. 🏙️

---

## 📜 Script-by-script — a mermaid flowchart for each script

### 🚪 `main.py` — the one entry point

```mermaid
flowchart TD
    A[python main.py] --> B{Command?}
    B -->|demo| D[⚛️ Quantum + 📡 Network + 🔐 QKD + 🧪 Chamber + 🧠 Council]
    B -->|quantum| Q[quantum.py]
    B -->|network / speedtest| N[network6g.py]
    B -->|qkd| K[qkd.py]
    B -->|sandbox| S[payloads.py]
    B -->|council| C[council.py]
    B -->|checks| CH[checks.py]
    B -->|hold-demo| H[gates.py → HOLD, exit 2]
```

### ⚛️ `q6g/quantum.py` — statevector quantum computer

```mermaid
flowchart TD
    A[QuantumCircuit n qubits] --> B[Apply gates<br/>H X Y Z S Rx Ry Rz CNOT CZ SWAP]
    B --> C{Program}
    C -->|bell_pair| D[0.5 / 0 / 0 / 0.5]
    C -->|ghz| E[Shared multi-qubit state]
    C -->|teleport| F[X by q1, Z by q0 corrections<br/>fidelity measured = 1.0]
    C -->|grover| G[Oracle + diffusion ×3<br/>marked state 96.13%]
    B --> H[probabilities / measure]
```

### 📡 `q6g/network6g.py` — the 6G 1 Tbps engine

```mermaid
flowchart TD
    A[LinkConfig<br/>24 GHz, 8 streams, 256 antennas] --> B[FSPL per band]
    B --> C[SNR at distance]
    C --> D[Shannon efficiency<br/>log2 of 1 + SNR]
    D --> E[Capacity = BW × eff × streams × 0.85]
    E --> F{≥ 1 Tbps?}
    F -->|100 m: 1.10 Tbps| G[✅ Target met, modelled]
    F -->|1 km| H[📉 Below target — physics]
    A --> I[Latency budget<br/>0.0703 ms vs 0.1 ms target]
    A --> J[Speed test<br/>seeded, labelled simulated]
```

### 🔐 `q6g/qkd.py` — BB84 quantum key distribution

```mermaid
flowchart TD
    A[Alice: random bits + bases] --> B[Bob: random bases]
    B --> C{Matching bases?}
    C -->|yes| D[Sifted key]
    C -->|no| E[Discard]
    F[🕵️ Eve guesses bases] -.->|corrupts ~25%| D
    D --> G{QBER > 11%?}
    G -->|no| H[✅ KEY OK]
    G -->|yes| I[⛔ ABORT — spy suspected]
```

### 📦 `q6g/sandbox_api.py` — the chamber (verbatim merge)

> Copied byte-for-byte from Darion's MonadDB-RE implementation of his `credkellar/sandbox-api` merge — sha256 `28b3365c0466027079a4985520840f6532d7d9a0c5b4239b840e561f06de54b0`, identical in both repos. Its own docstring states the provenance honestly: no public source repo exists for the Hub image, and this is the static, defensive version of its idea.

```mermaid
flowchart TD
    A[Sample bytes] --> B[Temp dir<br/>write sample as DATA]
    B --> C[analyse_fn runs statically]
    C --> D[Telemetry: sha256, bytes,<br/>FS diff, trace, budgets]
    D --> E[Report + telemetry]
    E --> F[Temp dir deleted]
    C -.->|never| X[🚫 No exec, no eval,<br/>no sockets — network 0]
```

### 🧪 `q6g/payloads.py` — payload triage through the chamber

```mermaid
flowchart TD
    A[7 payloads] --> B[detonate_static<br/>one fresh chamber each]
    B --> C[Marker scan:<br/>eval / exec / shell / socket / pipe / rm]
    C --> D{Danger markers?}
    D -->|none: 4 payloads| E[✅ ALLOW_STATIC_STUDY]
    D -->|found: 3 payloads| F[⛔ HOLD_IN_CHAMBER]
    E --> G[Summary: executed False,<br/>network attempts 0]
    F --> G
```

### 🧠 `q6g/council.py` — Carbon 4 DECIDER + Muse advisor

```mermaid
flowchart TD
    A[Request + risk score] --> B[Carbon 4 DECIDER]
    B --> C{risk}
    C -->|≥ 75| D[⛔ HOLD, tier 32768]
    C -->|≥ 40| E[🔎 REVIEW, tier 8192]
    C -->|< 40| F[✅ ALLOW_SIM, tier 2048]
    A --> G[Muse advisor<br/>authority: none]
    G -.->|advice only,<br/>can never loosen| D
    D --> H[Strictest wins]
    E --> H
    F --> H
```

### ⛔ `q6g/gates.py` — the 13 HOLD gates

```mermaid
flowchart TD
    A[Any action] --> B{On the HOLD list?}
    B -->|live QPU / carrier / spectrum /<br/>physical link / detonation / 8 more| C[⛔ HoldGate raised<br/>needs Darion's explicit approval]
    B -->|local simulation| D[✅ Allowed]
```

### 🔎 `q6g/checks.py` — self-checks (18/18)

```mermaid
flowchart TD
    A[run_checks] --> B[⚛️ Bell, GHZ, teleport, Grover ×2]
    A --> C[📡 1 Tbps @ 100 m, falloff, latency, speed test]
    A --> D[🔐 BB84 clean OK, Eve detected]
    A --> E[⛔ Gates = 13, live held, sim free]
    A --> F[🧪 Chamber never executes,<br/>network 0, holds 3, allows 4]
    B --> G[CHECKS passed / total]
    C --> G
    D --> G
    E --> G
    F --> G
```

### 🧪 `tests/test_q6g.py` — pytest suite (15 passed)

```mermaid
flowchart TD
    A[pytest tests/] --> B[4 quantum tests]
    A --> C[4 network tests]
    A --> D[2 QKD tests]
    A --> E[2 council + gates tests]
    A --> F[3 chamber tests]
    B --> G[15 passed]
    C --> G
    D --> G
    E --> G
    F --> G
```

---

## 🌐 Network slices

| Slice | 🎯 Use | 🚀 Peak | ⏱️ Latency |
|---|---|---|---|
| eMBB+ | XR, holographic media | 1 Tbps | 1 ms |
| URLLC++ | Industrial control, V2X | 10 Gbps | 0.1 ms |
| mMTC+ | Massive IoT (10M devices/km²) | 100 Mbps | 10 ms |
| Q-SLICE | Quantum-secured traffic | 1 Gbps key-managed | 1 ms |

## ⛔ HOLD gates (13)

🚫 Live QPU hardware · 🚫 live carrier 6G network · 🚫 RF/THz spectrum transmission · 🚫 claiming or provisioning a physical 1 Tbps link · 🚫 live entanglement distribution · 🚫 routing real user traffic · 🚫 spectrum-license bypass · 🚫 encryption bypass · 🚫 radio/baseband firmware flashing · 🚫 satellite uplink · 🚫 medical/safety-critical control · 🚫 live network reconfiguration · 🚫 detonating a live/unknown sample outside the static chamber.

## 🧪 Verified (actually run, not claimed)

- ✅ `python -m pytest tests/ -q` → **15 passed**
- ✅ `python main.py checks` → **CHECKS 18/18**, exit 0
- ✅ `python main.py hold-demo` → HOLD fires, exit 2
- ✅ `python main.py sandbox` → 7 payloads: **4 allowed / 3 held**, executed False, network 0
- 🏷️ Badges: 14 shields.io URLs checked live → **HTTP 200**; real workflow badge.svg URLs → 404 until the workflows are pasted (see Updated Workflows)
- 🐳 Docker: the Dockerfile is provided; the image build was **not** run on the build machine (no Docker there) — first build happens in the Docker Publish workflow

## 📁 Project structure

```
Q6G-1TB/
├── 🖼️ assets/
│   └── cover.png            README cover (owner upload step — binary)
├── 🚪 main.py               CLI entry point (demo/quantum/network/speedtest/qkd/sandbox/council/checks/hold-demo)
├── 📦 q6g/
│   ├── ⚛️ quantum.py        statevector simulator, teleportation, Grover
│   ├── 📡 network6g.py      bands, FSPL, Shannon capacity, slices, speed test
│   ├── 🔐 qkd.py            BB84 with eavesdropper detection
│   ├── 📦 sandbox_api.py    sandbox-api chamber, verbatim (sha256 28b3365c…)
│   ├── 🧪 payloads.py       7 payloads + marker-scan triage through the chamber
│   ├── 🧠 council.py        Carbon 4 DECIDER + Muse advisor (authority: none)
│   ├── ⛔ gates.py          13 HOLD gates
│   └── 🔎 checks.py         18 self-checks
├── 🧪 tests/
│   └── test_q6g.py          15 pytest tests
├── 🔄 workflow-pack/
│   ├── ci.yml               → paste to .github/workflows/ci.yml
│   └── docker-publish.yml   → paste to .github/workflows/docker-publish.yml
├── 🐳 Dockerfile            python:3.12-slim, non-root
├── 📜 LICENSE               MIT
└── 📖 README.md             this file
```

## ⚠️ Honest scope

Real 6G is **not** commercially deployed, no physical 1 Tbps link is measured or claimed, no quantum hardware is accessed, and the sandbox-api Hub image has no public source repo — its chamber here is Darion's own static implementation, copied verbatim from his MonadDB-RE project with provenance stated in its docstring. What *is* real: the link math, the quantum simulation, the BB84 protocol behaviour, the chamber telemetry, the tests, and the checks — all running, all reproducible, all labelled.
