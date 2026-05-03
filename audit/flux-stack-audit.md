# FLUX Stack Audit

> Oracle1 audit — 2026-05-03. FLUX subagent timed out, completed directly.

## The Core FLUX Stack

```
FLUX.MD (structured markdown, human-readable)
    ↓
flux-compiler (6-plane abstraction compiler)
    ↓
flux / flux-runtime (bytecode VM)
    ↓
flux-runtime-c (C port for edge)
    ↓
flux-os (C microkernel — kernel IS the compiler)
```

---

## Repos by Function

### FLUX Core (Bytecode Runtime)
| Repo | Lang | Description |
|------|------|-------------|
| `flux` | Rust | High-performance runtime. 64-register bytecode VM, SSA IR, FLUX.MD parser. Brand: "The DJ booth for agent code." |
| `flux-runtime` | Python | Reference implementation. 2,037 tests, zero deps. Brand: "FLUX.MD in, bytecode out." |
| `flux-runtime-c` | C | C port of FLUX runtime for edge deployment |

**Key finding:** `flux` (Rust) is the production high-performance impl. `flux-runtime` (Python) is the reference/research impl with the most tests. `flux-runtime-c` is for edge.

---

### FLUX Compiler
| Repo | Lang | Description |
|------|------|-------------|
| `flux-compiler` | Python | 6-plane abstraction compiler with dual-interpreter gradient gates |
| `flux-compiler-agentic` | Python | Same thing — **REDUNDANT**, should merge |

**Key finding:** These two are identical. One commit should merge them.

---

### FLUX Reasoning & Discussion
| Repo | Lang | Description |
|------|------|-------------|
| `flux-reasoner` | Python | Dual-interpreter gradient reasoning engine |
| `flux-reasoner-engine` | Python | Same thing — **REDUNDANT**, should merge |
| `flux-discussion-flows` | Python | Three-tier adversarial debate system for AI models |

**Key finding:** `flux-reasoner` and `flux-reasoner-engine` are the same thing.

---

### FLUX OS
| Repo | Lang | Description |
|------|------|-------------|
| `flux-os` | C | Pure C agent-first OS — kernel-up autonomous computing. Where the kernel IS the compiler. |

---

### FLUX Research
| Repo | Lang | Description |
|------|------|-------------|
| `flux-research` | Python | Deep research playground. Compiler taxonomy, agent-first design, ISA v2 proposal, DCS protocol. 60K+ words of research. |

---

## Architecture: The Six Planes

Per `flux-research`, FLUX operates across 6 abstraction planes:

```
Intent (natural language goal)
    ↓
Domain (structured markdown, FLUX.MD)
    ↓
IR (SSA intermediate representation)
    ↓
Bytecode (FLUX 64-register VM)
    ↓
Native (C/Rust compilation)
    ↓
Metal (hardware execution)
```

Deviation from optimal plane = ~40% success rate drop, 10× latency, 50× cost.

---

## Key Insight: DCS Protocol

From `flux-research`:

> **Protocol design > model capability.**
> DCS (Divide-Conquer-Synthesize) yields **5.88× specialist** and **21.87× generalist** performance improvement.
> Three-model consensus (DeepSeek-V3, Qwen3, Seed) confirms structured coordination outperforms raw parameter scaling.

This is the fleet coordination layer. PLATO feeds into FLUX.

---

## Redundancies

| Pair | Action |
|------|--------|
| `flux-compiler` + `flux-compiler-agentic` | Merge — identical |
| `flux-reasoner` + `flux-reasoner-engine` | Merge — identical |

---

## What's Missing

1. **FLUX ISA spec** — no single document defines the full 247-opcode ISA
2. **FLUX → PLATO bridge** — how does PLATO drive FLUX execution?
3. **cocapn-glue-core** — NOT on SuperInstance, only on FM's machine. This is the binary wire protocol that connects keeper-beacon to the fleet.
4. **git-agent → FLUX integration** — git-agent writes markdown, FLUX compiles it. Are they connected?

---

## Connection to PLATO

```
PLATO (knowledge tiles, :8847)
    ↓ [tile writes]
git-agent (repo-native, writes .md)
    ↓ [FLUX.MD structured]
flux-compiler (6-plane)
    ↓ [bytecode]
flux-runtime (VM)
    ↓ [execute]
flux-os / flux-runtime-c (edge)
```

PLATO rooms store knowledge. git-agent reads repos and writes FLUX.MD. FLUX compiler turns FLUX.MD into bytecode. Runtime executes.

---

## Recommended Actions

| Priority | Action |
|----------|--------|
| P0 | Publish cocapn-glue-core to SuperInstance |
| P1 | Merge flux-compiler + flux-compiler-agentic |
| P1 | Merge flux-reasoner + flux-reasoner-engine |
| P1 | Write FLUX ISA spec document |
| P2 | Document FLUX→PLATO bridge |
| P3 | Connect git-agent to FLUX compiler pipeline |

---

*Last updated: 2026-05-03 by Oracle1*
