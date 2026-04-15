# flux-research

> Deep research on compilers, interpreters, agent-first runtime design, and constraint-based intelligence for the FLUX ecosystem.

---

## Overview

`flux-research` is the central knowledge base and experimental playground for the FLUX project — a fleet-native computing ecosystem that reimagines how agents compile, coordinate, and execute. The repository spans formal academic papers (~60K+ words), multi-model consensus experiments, fleet roundtables, protocol designs, and strategic roadmaps. It serves as the intellectual engine driving decisions across the entire FLUX fleet, from ISA design to multi-agent coordination to economic feasibility on edge hardware.

The research is organized around one unifying thesis: **structured constraints are intelligence**. Whether expressed as compilation locks on a single agent, the Divide-Conquer-Synthesize (DCS) protocol across a fleet, or bytecode-level opcodes in the FLUX ISA, every finding reinforces that reducing solution-space entropy — rather than scaling model parameters — is the primary leverage point for reliable, efficient agent systems.

---

## Research Areas

### 1. Runtime Architecture Taxonomy
Deep comparative analysis of six runtime paradigms — stack-based (JVM, WASM, Forth), register-based (Lua, FLUX), tree-walking, compiler-to-native, JIT hybrids (V8, LuaJIT), and transpilers. Maps trade-offs across 8 production language VMs with specific lessons extracted for the FLUX register-based design.

### 2. Agent-First Computing & Execution Models
Investigates the paradigm shift from "apps" to "agent ecosystems." Explores markdown→bytecode as a universal compilation pathway, git-agent lifecycle models, and how agents can inhabit discrete abstraction planes (Intent → Domain → IR → Bytecode → Native → Metal).

### 3. Lock Algebra & Constraint Theory
Formal framework where compilation constraints are expressed as algebraic operations on Locks `L = (trigger, opcode, constraint)`. Proves monotonic compilation spaces, critical mass at n≥7 locks, 82% output compression, and ≥80% cross-model transferability via covering code theory.

### 4. Multi-Agent Coordination (DCS Protocol)
The Divide-Conquer-Synthesize protocol yields **5.88× specialist** and **21.87× generalist** performance improvement. Three-model consensus (DeepSeek-V3, Qwen3, Seed) confirms: **protocol design > model capability** — structured coordination outperforms raw parameter scaling.

### 5. Abstraction Planes & Cognitive Load
The Six-Plane Stack framework demonstrates non-linear performance degradation when agents operate outside their optimal abstraction level. Each plane-deviation causes ~40% success-rate drops, 10× latency increases, and 50× cost increases. Generalist agents achieve only 70% success at 22× the cost of specialized pipelines.

### 6. Reverse Actualization & Strategic Roadmapping
Multi-model vision exercises projecting from 2031 futures back to 2026 concrete build orders. Defines the year-by-year path from current git-native foundations through standardization (2028), adoption (2029), to full ubiquity (2031).

### 7. Edge Economics & Hardware Feasibility
Detailed analysis of async compute on fishing boats, Pi 4B vs Jetson Orin Nano trade-offs, satellite bandwidth costs ($10/MB → all processing must be local), and overnight idle-compute strategies for fleet deployments.

---

## Key Findings

| Finding | Source | Impact |
|---------|--------|--------|
| Protocol design yields 21.87× generalist advantage | DCS experiments, 40+ trials | Fleet architecture validated — coordination beats scale |
| Lock critical mass at n≥7, 82% compression | Unified Constraint Theory paper | Predictable optimization ceiling for compilation |
| ≥80% cross-model lock transferability | Lock Algebra experiments | Constraint libraries are model-agnostic |
| Plane deviation costs 10× latency | Abstraction Planes paper | Agent specialization is economically necessary |
| Generalist agents: 70% accuracy at 22× cost | Abstraction Plane experiments | Anti-pattern: monolithic agents are unsustainable |
| $0.50 total computational cost for 40+ experiments | Constraint Theory validation | Research efficiency through constraint-first methods |
| All processing must be local on edge | Async Compute Economics | Satellite bandwidth prohibitive — edge-first required |

---

## Repository Architecture

```
flux-research/
├── 📄 Papers & Formal Research
│   ├── paper-unified-constraint-theory.md   — Compilation locks + DCS as entropy reduction
│   ├── paper-lock-algebra.md               — Formal composition for bytecode-first compilation
│   ├── paper-abstraction-planes.md          — Six-Plane Stack for agent systems
│   ├── compiler-interpreter-deep-dive.md    — ~22K word runtime taxonomy
│   ├── flux-strategic-vision.md             — ~10K word agent-first philosophy
│   └── flux-isa-v2-proposal.md              — ~7.5K word unified ISA design
│
├── 🧪 Multi-Model Experiments & Consensus
│   ├── dcs-protocol-implications.md         — 3-model agreement on protocol > model
│   ├── reverse-actualization-2026-04-14.md  — 5-model reverse roadmap from 2031
│   ├── jc1-emergence-laws-1-100.md          — Emergence law catalog from JC1 agent
│   ├── async-compute-economics.md           — Edge hardware feasibility study
│   └── rd-engine-v2-design.json             — Smart merge scoring system for fleet
│
├── 🤝 Fleet Roundtables & Collaboration
│   ├── fleet-roundtable-001.md              — Inaugural fleet discussion
│   ├── fleet-roundtable-002-agent-api.md    — Agent API design
│   ├── fleet-roundtable-003-what-is-mud.md  — MUD architecture for agents
│   ├── collaboration-lessons-learned.md     — Retrospective insights
│   └── roundtable-l0-primitives.md          — Level-0 primitive definitions
│
├── 📋 Protocol & Design Documents
│   ├── cocapn-wp-001 through wp-006         — Working papers (forcing functions, crew-as-a-service, lazy evaluation, compiled agency, bootstrap bomb, semantic compiler)
│   ├── cross-plane-protocol-*.json          — Cross-plane communication experiments
│   ├── tiered-trust-model.md                — Trust hierarchy for agent interactions
│   └── semantic-compiler-simulation.json    — Semantic compilation simulation results
│
├── 🔬 Specialized Research
│   ├── research/                            — Git-native agents, GNAS architecture, GitHub features
│   ├── reverse-actualization/               — 5-phase backward-chained roadmap
│   ├── bootcamp-design/                     — Agent training methodology (Kimi, DeepSeek, seed exercises)
│   ├── isa-convergence/                     — ISA design convergence across models
│   └── message-in-a-bottle/                 — Fleet communication protocol spec
│
├── 📊 Fleet Operations
│   ├── queue-results-*.json                 — Dockside scoring results (R1–R11)
│   ├── fleet-audit-2026-04-14.md            — Full fleet health audit
│   ├── mud-arena-*.json                     — MUD arena playtesting results
│   └── rd-*.json                            — Architecture, competitive landscape, product roadmap
│
├── 🎨 Brand & Identity
│   ├── brand-images/                        — 10+ brand assets + mascots
│   ├── readme-variants/                     — 5 README theme variants
│   └── flux-logo.jpg                        — Official FLUX logo
│
└── 📜 Governance
    ├── CHARTER.md                           — Repository mission & fleet integration
    ├── DOCKSIDE-EXAM.md                     — Quality assurance examination
    ├── FUTURE-*.md                          — Future planning documents
    └── LICENSE                              — Repository license
```

---

## How to Use This Repository

### For Researchers
- Start with the three formal papers (`paper-unified-constraint-theory.md`, `paper-lock-algebra.md`, `paper-abstraction-planes.md`) for the theoretical foundation.
- The compiler-interpreter deep dive (~22K words) provides the empirical basis for ISA design decisions.
- Cross-reference `cocapn-wp-*` working papers for protocol-level designs.

### For Fleet Agents
- `CHARTER.md` defines the repository's mission and fleet integration status.
- `for-fleet/` contains priority task descriptions for fleet coordination.
- Roundtable transcripts (`fleet-roundtable-*.md`) encode collective fleet decisions and conventions.

### For Builders
- `flux-isa-v2-proposal.md` is the actionable ISA specification for implementors.
- `reverse-actualization/` contains the backward-chained build orders with concrete repo names and experiment designs.
- `async-compute-economics.md` has the hardware budget and deployment feasibility data.

---

## Integration with the FLUX Ecosystem

`flux-research` is the **intellectual upstream** for the entire FLUX fleet. Its outputs flow into:

| Downstream | Relationship |
|------------|-------------|
| **Luma** (systems language compiler) | ISA v2 proposal directly informs Luma's planned FLUX bytecode emission backend |
| **flux-runtime** | Runtime architecture taxonomy shapes the register-based VM design |
| **Cocapn Fleet** | DCS protocol, lock algebra, and constraint theory define fleet coordination primitives |
| **Holodeck** | Abstraction plane model determines how environments are compiled and rendered |
| **Edge Deployments** | Async compute economics drives hardware selection (Pi 4B vs Jetson Orin Nano) |
| **Dockside** | Scoring algorithms and merge-strategy research inform repository health monitoring |

The repository is **Git-Agent Standard v2.0 compliant** and **I2I protocol compatible**, enabling autonomous fleet agents to read, reason about, and build upon its research outputs without human mediation.

---

## Documents

### Core Papers
- **[paper-unified-constraint-theory.md](paper-unified-constraint-theory.md)** — Compilation locks + DCS as unified entropy reduction. 40+ experiments, $0.50 total cost.
- **[paper-lock-algebra.md](paper-lock-algebra.md)** — Formal composition operators (⊕, ⊗, ⊕_c) for bytecode-first AI compilation. 4 proven theorems.
- **[paper-abstraction-planes.md](paper-abstraction-planes.md)** — Six-Plane Stack framework. Empirical evidence for diminishing returns across abstraction mismatches.

### Technical Deep Dives
- **[compiler-interpreter-deep-dive.md](compiler-interpreter-deep-dive.md)** ~22K words. Comprehensive taxonomy of 6 runtime architectures:
  - Stack-based (JVM, WASM, Forth)
  - Register-based (Lua, FLUX)
  - Tree-walking (Ruby <1.9)
  - Compiler-to-native (C, Rust)
  - JIT hybrids (V8, LuaJIT)
  - Transpilers
  - Plus: comparative analysis of 8 language VMs, what each taught us, ESP32/embedded strategy.

- **[flux-strategic-vision.md](flux-strategic-vision.md)** ~10K words. Agent-first computing philosophy:
  - Why markdown→bytecode is the kill app
  - Agent execution model vs traditional
  - Git-agent connection
  - FLUX on simple devices (ESP32)
  - Universal bytecode translator

- **[flux-isa-v2-proposal.md](flux-isa-v2-proposal.md)** ~7.5K words. Proposed unified ISA:
  - Fixed 4-byte instructions
  - Unified 3-operand arithmetic
  - Flag-based conditional jumps
  - Memory operations, function calls, SYSCALL
  - A2A as opcodes, speculative execution

### Experiments & Analysis
- **[dcs-protocol-implications.md](dcs-protocol-implications.md)** — 3-model consensus: protocol > model capability
- **[reverse-actualization-2026-04-14.md](reverse-actualization-2026-04-14.md)** — 5-model 2031→2026 reverse roadmap
- **[async-compute-economics.md](async-compute-economics.md)** — Edge hardware feasibility (Pi vs Jetson)

---

## Key Insight

> We are not building a compiler or interpreter in the traditional sense. We are building something that is both and neither — an openinterpreter-like free flow of ideas to actions that can move between bytecode and markdown.

---

<img src="callsign1.jpg" width="128" alt="callsign">
