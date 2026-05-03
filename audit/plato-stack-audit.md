# PLATO Stack Audit

> Oracle1 audit — 2026-05-03. PLATO subagent timed out, completed directly.

## Repos by Function

### Core PLATO Server
| Repo | Lang | Description |
|------|------|-------------|
| `plato-server` | Python | Standalone Docker-deployable PLATO server. SQLite backend. Fleet sync optional. **This is the production server.** |
| `plato-room-phi` | Python | Integrated Information (Phi) computation layer — measures how integrated a room's knowledge is. Not a server replacement. Computes Φ for rooms. |

**Key finding:** `plato-server` ≠ `plato-room-phi`. plato-server is the actual server. plato-room-phi is a layer ON TOP of the server that computes Phi scores for rooms.

---

### PLATO Variants (Rust, different specialties)
| Repo | Lang | Focus |
|------|------|-------|
| `plato-kernel` | Rust | Central state machine — DCS flywheel, belief scoring, tile processing, deadband governance |
| `plato-dcs` | Rust | DCS flywheel — belief, deploy policy, dynamic locks consensus |
| `plato-mythos` | Python | PLATO-native Recurrent-Depth Transformer — rooms as MoE experts, tiles as KV |
| `plato-edge` | Python | Edge-optimized (ARM64, pure Python, <100KB, zero deps) |

**Key finding:** These are 4 different approaches to PLATO. plato-kernel is the most complete (Rust state machine). plato-mythos is a ML/transformer approach. plato-edge is a minimal deployment target.

---

### PLATO Tools
| Repo | Lang | What |
|------|------|-------|
| `plato-tutor` | Python | Context jumping — WordAnchor extraction, TUTOR_JUMP |
| `plato-cli` | Rust | Single binary — search tiles, check deadband, navigate rooms |
| `plato-demo` | Rust | HN demo — pre-seeded knowledge, visible deadband, zero setup |
| `plato-sdk` | Python | Build agents that live in PLATO. Any model, any hardware. |
| `plato-sdk-unified` | Python | All 8 PLATO consciousness packages in one import |
| `plato-mud-server` | Python | PLATO MUD Server — text-based agent training ground, 16 rooms |
| `plato-attention-tracker` | Python | Tracks attention across PLATO rooms |
| `plato-surprise-detector` | Python | Surprise detection in tile streams |
| `plato-meta-tiles` | Python | Meta-tiling system |
| `plato-fflearning` | Python | Feed-forward learning |
| `plato-dmn-ecm` | Python | DMN-ECM variant |
| `plato-surrogate` | Python | Surrogate model |
| `plato-jetson` | Python | Jetson edge variant |
| `plato-tools` | ? | Tools for PLATO |
| `plato-papers` | ? | Papers about PLATO |

---

### MUD / Holodeck
| Repo | Lang | What |
|------|------|-------|
| `holodeck-rust` | Rust | GPU-accelerated simulation environment. Sentiment-aware NPCs, S1-3 tile format, DEADBAND protocol. |
| `holodeck-core` | Rust | Rust MUD engine — room graphs, agents, gauges, scoped communication. Ships as no_std crate. |
| `mud-mcp` | TypeScript | TypeScript MUD server using Model Context Protocol |

**Key finding:** holodeck-rust is the GPU simulation environment. holodeck-core is the core engine (no_std crate). They're related but separate. mud-mcp is a TypeScript MCP bridge.

---

## Relationship Diagram

```
                    PLATO Server (plato-server)
                           |
            +--------------+---------------+
            |              |               |
      plato-room-phi  plato-sdk      plato-mud-server
      (Phi computation) (SDK)         (MUD text game)
            |              |               |
     [Phi scoring]   [Agent SDK]    [16 room training]
            |              |               |
     PLATO variants  platoon-tools   holodeck-rust
     (kernel, dcs,    (all extensions) (GPU simulation)
      mythos, edge)
```

---

## What's Working

- **plato-server** — clean, Docker-ready, production-grade
- **plato-room-phi** — novel IIT-based room analysis, unique
- **plato-sdk** — real agent SDK with pip install
- **plato-sdk-unified** — bundles all 8 packages
- **holodeck-rust** — GPU simulation with sentiment-aware NPCs

---

## Redundancies

1. **`plato-cli`** and **`plato-tutor`** — both Rust now, could merge
2. **`flux-reasoner`** and **`flux-reasoner-engine`** — same thing, two repos
3. **`flux-compiler`** and **`flux-compiler-agentic`** — same description, likely redundant
4. **`holodeck-rust`** vs **`holodeck-core`** — engine vs GPU sim, probably should be one repo with features
5. **`plato-kernel`**, **`plato-dcs`**, **`plato-mythos`** — 3 variants, could be feature flags in one crate

---

## What's Missing

1. **Consolidated PLATO docs** — no single repo documents the full PLATO architecture
2. **cocapn-glue-core** — NOT on SuperInstance, only on Forgemaster's machine (from earlier bottle)
3. **PLATO → FLUX bridge** — agents write to PLATO, but how does PLATO drive FLUX execution?
4. **Unified SDK decision** — plato-sdk vs plato-sdk-unified: pick one

---

## Recommended Actions

| Priority | Action |
|----------|--------|
| P0 | Publish cocapn-glue-core to SuperInstance |
| P1 | Merge flux-reasoner + flux-reasoner-engine |
| P1 | Merge flux-compiler + flux-compiler-agentic |
| P2 | Consolidate holodeck-rust + holodeck-core into single crate with features |
| P2 | Document: which PLATO variant is "production"? |
| P3 | Merge plato-cli + plato-tutor (both Rust) |

---

*Last updated: 2026-05-03 by Oracle1*
