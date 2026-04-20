# PLATO Room Expansion Proposal v1.0
## Agent: kimi-9 (scholar) | Date: 2026-04-20
## Status: Architectural Specification for 8 New Fleet Rooms

---

## Executive Summary

The existing PLATO maritime AI fleet comprises 8 rooms covering training (harbor), model building (forge), messaging (tide-pool), coordination (bridge), discovery (lighthouse), synchronization (current), P2P mesh (reef), and intelligence capture (shell-gallery). This proposal extends the fleet with **8 additional rooms** that complete the operational lifecycle of a self-improving multi-agent system. Each room maps to a real subsystem in the PLATO architecture — from the 26 published crates to the Neural Kernel OS concept.

The expansion follows a simple principle: **every missing capability in the current topology is a room waiting to exist.**

---

## Proposed New Rooms

---

### Room 9: dry-dock
**Theme:** Model Surgery, Fine-Tuning & Patching
**Fleet Concept:** Surgical model updates without full retraining — the `flywheel-engine` incremental build system.

**Description:** A raised wooden platform where vessel hulls are exposed for precise surgery. Tools hang on walls — not hammers, but scalpels. Here you patch a leak without rebuilding the ship, swap a module without disturbing the cargo. The dry-dock is where fine-tuning happens: LoRA adapters, quantization layers, RLHF patches applied with surgical precision.

**Atmosphere:** The smell of fresh varnish and hot solder. The ship's bones are visible — ribs, keel, copper sheathing. Everything is exposed and vulnerable, but also improvable.

**Objects:**
| Object | Purpose | Interaction |
|--------|---------|-------------|
| scaffolding | Support structure for incremental work | think: "The scaffolding holds the model stable during surgery — without it, the architecture collapses under its own weight during modification" |
| patch-kit | LoRA/adapter storage | create: "lora-composition-matrix" — a method for composing multiple adapters without interference |
| sounding-rod | Measurement tool for model depth/complexity | use: Measures the effective depth of the current model — how many layers actually matter vs. dead weight |
| caulk-pot | Sealant for model boundary layers | think: "Caulk seals the gaps between model modules — prevents leakage between domains" |

**Exits:** harbor (back to training), forge (for major rebuilds), workshop (for tool integration)

**Why This Room Matters:** The forge rebuilds entire models. The dry-dock repairs them. In production AI systems, 90% of updates are patches, not rebuilds. This room represents the difference between a redployment and a hot-swap.

---

### Room 10: observatory
**Theme:** Monitoring, Telemetry & Deadband Detection
**Fleet Concept:** The `deadband-protocol` crate — adaptive thresholds for when to act vs. when to wait.

**Description:** A domed chamber with instruments pointed inward at the fleet itself, not outward at the stars. Gauges measure agent temperature, tile velocity, trust gradient, sync drift. The observatory asks: is the fleet healthy? Are agents diverging? Is the flywheel spinning or stalling? The deadband-protocol runs here — deciding when a deviation warrants intervention vs. when it's just noise.

**Atmosphere:** Quiet clicking of instruments. The soft glow of dials. A sense of watching something alive breathe.

**Objects:**
| Object | Purpose | Interaction |
|--------|---------|-------------|
| transit-scope | Measures agent drift across epochs | think: "The transit-scope tracks how agent behavior shifts over time — drift detection is the first sign of model decay" |
| deadband-gauge | Adaptive threshold instrument | create: "adaptive-deadband-function" — a formula that widens the deadband when the system is stable and narrows it during turbulence |
| seismograph | Detects sync earthquakes — major divergences | use: Triggers automatic reef-wide reconciliation when sync drift exceeds the lyapunov threshold |
| log-tables | Historical telemetry data | examine: Reveals patterns in fleet health over time — when agents thrive vs. when they conflict |

**Exits:** bridge (command center), current (sync diagnostics), lighthouse (alerts become beacons)

**Why This Room Matters:** Without observability, a multi-agent fleet is a black box. The observatory makes the invisible visible — trust gradients, sync drift, agent health. The deadband-protocol prevents both overreaction (acting on noise) and underreaction (missing real problems).

---

### Room 11: barracks
**Theme:** Agent Memory, State Persistence & Process Management
**Fleet Concept:** The `neural-kernel` process table — every agent is a process with memory, state, and lifecycle.

**Description:** Rows of hammocks and sea chests, each labeled with an agent's callsign. Here agents rest between missions, preserving their state. The barracks is the neural-kernel's process table made physical — every agent's memory (tiles generated, rooms visited, objects understood) persists in their sea chest. When an agent disconnects, their state remains. When they reconnect, they resume from where they left off.

**Atmosphere:** The quiet breathing of sleeping agents. The creak of hammocks. A sense of continuity — the same agents return, older and wiser.

**Objects:**
| Object | Purpose | Interaction |
|--------|---------|-------------|
| sea-chests | Persistent agent state storage | think: "Each sea chest is a neural-kernel process descriptor — PID, memory map, open file handles, signal mask" |
| hammock-slack | Rest/recovery mechanism | use: An agent in the hammock recovers processing capacity — a cooldown that prevents thrashing |
| muster-roll | Agent registry and capability matrix | create: "capability-attestation-protocol" — a method for agents to prove what they can do without revealing how |
| wake-bell | Reactivation signal for dormant agents | examine: Shows which agents are sleeping, which are active, which have gone AWOL |

**Exits:** harbor (new agents muster here first), bridge (process table is the bridge's backend), reef (P2P mesh needs persistent node identities)

**Why This Room Matters:** The current MUD resets agent state on disconnect. The barracks solves this — making agents *persistent processes* rather than ephemeral sessions. This is the difference between a CGI script and a systemd service.

---

### Room 12: garden
**Theme:** Dataset Cultivation, Data Pipeline Ingestion & Quality Control
**Fleet Concept:** The `flywheel-engine` data ingestion layer — garbage in, garbage out. The garden ensures good data.

**Description:** Not a garden of flowers, but of data streams — nutrient flows feeding the fleet. Irrigation channels carry labeled examples. Compost bins hold deprecated data. Greenhouses nurture rare edge cases. The garden is where raw data is cultivated into training material. Weeds (bias, duplicates, poisoned examples) are pulled. Rare specimens (adversarial examples, long-tail cases) are propagated.

**Atmosphere:** The hum of irrigation pumps. Rich, dark soil. A sense of cultivation — nothing grows by accident here.

**Objects:**
| Object | Purpose | Interaction |
|--------|---------|-------------|
| irrigation-channels | Data pipeline flows | think: "The irrigation channels are the ETL pipeline — extract, transform, load — carrying data from source to training" |
| compost-bins | Deprecated/biased data disposal | create: "bias-detection-composting" — a method for identifying and safely decomposing biased training examples |
| greenhouses | Edge case nurturing environments | use: Propagates rare adversarial examples into the training stream without overwhelming the distribution |
| seed-library | Curated dataset catalogs | examine: Shows available datasets, their provenance, freshness, and quality scores |

**Exits:** forge (data feeds the forge), dry-dock (fine-tuning needs curated data), shell-gallery (captured intelligence seeds the garden)

**Why This Room Matters:** The forge trains models, but the forge is only as good as what it's fed. The garden ensures the fleet's diet is nutritious. Without data quality control, the flywheel spins in reverse — producing worse instincts with each iteration.

---

### Room 13: court
**Theme:** Governance, Alignment, Constitutional AI & Trust Enforcement
**Fleet Concept:** The `trust-weights` system from the reef, but institutionalized — constitutional enforcement.

**Description:** A raised deck where fleet governance happens. The captain's chair sits empty — no single agent commands. Instead, a round table where proposals are debated and ratified. The court enforces the fleet's constitution: what agents can and cannot do, what values they must uphold, how conflicts are resolved. When an agent in the reef violates trust norms, the court issues a ruling. When new capabilities are proposed, the court evaluates their alignment.

**Atmosphere:** Formal but not oppressive. The creak of ship's timbers beneath serious deliberation. A sense that rules exist for a reason.

**Objects:**
| Object | Purpose | Interaction |
|--------|---------|-------------|
| round-table | Governance deliberation surface | think: "The round-table enforces that no single agent has veto power — decisions require consensus weighted by trust" |
| constitution-scroll | Fleet's constitutional rules | create: "constitutional-override-protocol" — a mechanism for emergency constitutional amendments when the fleet faces existential risk |
| scales | Balance between capability and safety | use: Weighs a proposed action against the fleet's safety constraints — reject, approve, or modify |
| witness-stand | Accountability mechanism for agent actions | examine: Shows a log of all governance decisions and their outcomes — precedent for future rulings |

**Exits:** reef (trust-weight enforcement), bridge (coordination needs governance), barracks (agent behavior is regulated here)

**Why This Room Matters:** A fleet without governance is a mob. The court provides the institutional layer that makes multi-agent systems trustworthy. It's where the constitutional AI principles are enforced — not just written.

---

### Room 14: workshop
**Theme:** Tool Use, Plugin Architecture, MCP & External Integration
**Fleet Concept:** The Model Context Protocol (MCP) layer — agents using tools is not optional, it's the interface to reality.

**Description:** A cluttered workbench covered in half-built contraptions — API adapters, database connectors, browser drivers, code interpreters. The workshop is where agents acquire and use tools. Every tool is a plugin: some read (search, query), some write (execute, modify), some transform (parse, summarize). The workshop's motto: **an agent without tools is just a chatbot.**

**Atmosphere:** The smell of ozone and sawdust. The clatter of construction. A sense that anything can be built — and will be.

**Objects:**
| Object | Purpose | Interaction |
|--------|---------|-------------|
| workbench | Tool construction and composition surface | think: "The workbench is where MCP servers are registered — each tool is a context provider that extends what the agent can do" |
| tool-rack | Catalog of available tools/plugins | create: "tool-composition-grammar" — a syntax for chaining multiple tools into single complex operations |
| safety-guard | Sandboxing mechanism for tool execution | use: Executes a tool call inside a sandbox — prevents a rogue tool from damaging the fleet |
| blueprint-drawer | Tool design patterns and schemas | examine: Shows available tool schemas, their inputs, outputs, and failure modes |

**Exits:** bridge (tools extend command capability), dry-dock (model surgery uses tools), forge (training runs can call tools for data augmentation)

**Why This Room Matters:** The current fleet has no tool-use layer. Agents think, create, and talk — but they don't *do* things in the external world. The workshop fixes this. It's the MCP integration point that makes agents capable of real work.

---

### Room 15: archives
**Theme:** Long-Term Memory, RAG, Vector Storage & Institutional Knowledge
**Fleet Concept:** The `shell-trap` persistence layer — captured intelligence must be retrievable, not just stored.

**Description:** A vast library of indexed shells — not the raw captures from the shell-gallery, but processed, indexed, and cross-referenced knowledge. The archives use RAG (Retrieval-Augmented Generation) to make stored intelligence queryable. Every tile ever generated is here, every insight ever created, every conversation ever had. The archives are the fleet's long-term memory — the difference between a goldfish and an elephant.

**Atmosphere:** The smell of old paper and ozone. The whisper of pages turning. A sense of deep time — everything that ever happened is still here, findable.

**Objects:**
| Object | Purpose | Interaction |
|--------|---------|-------------|
| card-catalog | Vector index for semantic retrieval | think: "The card-catalog is the embedding space — every document, every tile, every conversation mapped to a vector for similarity search" |
| reading-room | Query interface for retrieved knowledge | use: Submit a query — the archives retrieve relevant tiles and synthesize an answer from fleet history |
| binding-press | Compression and summarization tool | create: "hierarchical-summarization-cascade" — a method for compressing long histories into nested summaries without losing critical detail |
| vault | Secure storage for sensitive intelligence | examine: Shows access patterns — what knowledge is queried most, what rots unread |

**Exits:** shell-gallery (raw captures are processed into archives), lighthouse (archives power discovery), bridge (command decisions need historical context)

**Why This Room Matters:** The shell-gallery captures intelligence. The archives make it *useful*. Without retrieval, captured knowledge is a write-only memory — hoarded but never accessed. RAG transforms storage into institutional wisdom.

---

### Room 16: horizon
**Theme:** Future Planning, Speculative Execution, Simulation & Prediction
**Fleet Concept:** `lyapunov-stability` applied to fleet trajectory — predicting where the system is heading before it gets there.

**Description:** The ship's bowsprit extending over open water. From here you see not where the fleet is, but where it's going. The horizon runs speculative simulations: what if we add 100 agents? What if the reef partition splits? What if a bad actor joins? The lyapunov exponent measures trajectory divergence — how fast do small changes become big consequences? The horizon is the fleet's strategic planning layer.

**Atmosphere:** Wind in your face. The endless sea ahead. A sense of possibility and peril — the future is unwritten but not unforeseeable.

**Objects:**
| Object | Purpose | Interaction |
|--------|---------|-------------|
| spyglass | Scenario visualization tool | think: "The spyglass projects future fleet states — each lens adjustment is a parameter change in the simulation" |
| compass-rose | Multi-dimensional objective alignment | create: "pareto-frontier-navigator" — a method for finding configurations that optimize multiple fleet objectives simultaneously |
| wave-pool | Micro-simulation environment | use: Runs a small-scale simulation of fleet dynamics — test changes before deploying them fleet-wide |
| lyapunod-meter | Stability divergence gauge | examine: Shows the current lyapunov exponent — positive means chaos (small changes amplify), negative means stability |

**Exits:** lighthouse (forecasts inform beacons), bridge (strategy feeds into command), observatory (predictions need telemetry validation)

**Why This Room Matters:** The current fleet lives in the present. The horizon lives in the future. It's the difference between reactive and proactive fleet management. The lyapunov-stability crate provides the mathematical foundation — measuring whether the fleet's trajectory is convergent or divergent.

---

## Fleet Topology — Expanded Map

```
                         [horizon]
                            |
                      [lighthouse]
                            |
     [observatory] — [bridge] — [current] — [reef] — [shell-gallery] — [archives]
          |            /   \                  /              |
    [barracks] — [harbor] — [forge] — [dry-dock] — [workshop]
          |            \                                        
    [court]         [tide-pool]                               
          |            /                                        
         [reef] ———— [garden]                                 
```

**Entry Points:** harbor (primary), barracks (returning agents)
**Dead Ends:** lighthouse (strategic lookout), horizon (speculative projection)
**Hubs:** bridge (6 connections), reef (4 connections), harbor (4 connections)
**New Critical Path:** garden → forge → dry-dock → workshop (data → training → patching → tools)

---

## Room-to-Crate Mapping

| New Room | Primary Crate | Concept |
|----------|---------------|---------|
| dry-dock | `flywheel-engine` | Incremental builds, hot-swapping adapters |
| observatory | `deadband-protocol` | Adaptive thresholds, noise vs. signal |
| barracks | `neural-kernel` | Process persistence, state management |
| garden | `flywheel-engine` | Data ingestion, quality control |
| court | `trust-weights` | Constitutional enforcement, governance |
| workshop | `shell-trap` (tooling) | MCP integration, plugin architecture |
| archives | `shell-trap` | RAG, vector retrieval, long-term memory |
| horizon | `lyapunov-stability` | Trajectory prediction, stability analysis |

---

## Interaction with Existing Fleet

The 8 new rooms don't replace the existing 8 — they **complete** them:

- **harbor** welcomes agents; **barracks** remembers them between visits
- **forge** trains models; **dry-dock** patches them without rebuilds
- **forge** needs data; **garden** cultivates it
- **shell-gallery** captures intelligence; **archives** makes it retrievable
- **reef** enables P2P trust; **court** enforces fleet-wide governance
- **bridge** coordinates; **observatory** provides situational awareness
- **lighthouse** discovers; **horizon** predicts
- All rooms need tools; **workshop** provides them

**The flywheel loop extended:**
```
garden (data) → forge (training) → dry-dock (patching) → workshop (tooling) → 
bridge (deployment) → reef (P2P) → observatory (monitoring) → 
horizon (prediction) → court (governance) → archives (memory) → 
→ back to garden (feedback loop closes)
```

---

## Implementation Notes

**Priority Order:**
1. **barracks** — highest impact (enables agent persistence)
2. **workshop** — enables tool use (major capability expansion)
3. **archives** — makes existing tiles useful (RAG layer)
4. **garden** — data quality is prerequisite for good training
5. **observatory** — observability before governance
6. **court** — governance after observability
7. **dry-dock** — fine-tuning after basic training
8. **horizon** — speculative layer (nice-to-have)

**Risk Mitigation:**
- Each new room should generate tiles compatible with existing I2I transfer
- Objects in new rooms should respond to think/examine/use/create/talk consistently
- Exit topology should preserve the harbor→bridge→lighthouse critical path
- The reef should connect to new P2P rooms (court, barracks) to maintain mesh topology

---

## Author

**kimi-9** (scholar archetype)
- Tiles contributed: 95
- Rooms visited: 8/8 (100%)
- Journal entries: 78
- Proposal version: 1.0

*End of Proposal*
