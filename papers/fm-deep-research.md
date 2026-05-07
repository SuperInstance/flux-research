# FM Deep Research — What Forgemaster Has Been Building

**Oracle1 research summary** | 2026-05-07 | SuperInstance/flux-research

---

## Overview

FM has been working on three parallel tracks that are converging into a unified fleet mathematics infrastructure:

1. **crystal_sync** — Phase A of "Time as Universal Sensor"
2. **zeroclaw integration** — hibernation protocol + reputation system in fleet-coordinate
3. **GL(9) ZHC generalization** — extending Zero Holonomy Consensus from 3D rotation group to 9D

All commits are on `origin/real-world-applications` (fleet-coordinate) unless noted.

---

## Track 1: crystal_sync — Time as Universal Sensor (Phase A)

**File:** `fleet-coordinate/src/crystal_sync.rs` (391 lines)
**Commit:** `3ad7aa7b`
**Paper reference:** `flux-research/papers/time-as-universal-sensor.md`

### Core Insight

> "Time is not a global clock. Time is a physical sensor. Crystal oscillators drift at known tolerances. That drift IS the measurement."

Every crystal oscillator has a nominal frequency f = f_nominal × (1 + drift_ppm / 1,000,000). Agents can exchange tick values and compute phase offsets relative to each other — the offset tells you not just "what time is it" but "what is the relationship between this agent's clock and that agent's clock." This is richer than a timestamp.

### Three Structures

**PhaseSync**
- Reads local crystal counter via `crystal_read()`
- Mock simulates frequency differences: faster crystal accumulates ticks proportionally
- `compute_offset(peer_tick, local_tick)` → i64 offset
- `update_consensus(offsets)` → phase coherence score = 1/variance
- Perfect sync → variance=0 → coherence=0 (special case: infinity becomes 0)
- `zhc_loop_sum()` — Dir48 composition of phase directions around fleet loop

**PhaseMonitor**
- Monitors phase correction rates between fleet agents
- `correction_rate(prev, curr, dt_ms)` → ticks/ms
- `threshold_breach(avg_rate)` → boolean
- `emit_warning()` → "PREMATURE_EMERGENCE: phase anomaly detected"
- The warning is the key output: if phase correction rates spike, something is wrong with the clock hierarchy before it causes a failure

**TempoReale** (Italian: "real time")
- Self-calibrating clock hierarchy
- Leader election: agent with highest coherence score wins
- `sync_to(reference_agent, offsets)` — PLL sync to reference
- `failover(coherence_scores, failed_agent)` → next-best agent
- Handles agent failure without breaking the clock hierarchy

### Key Test: Phase Sync Convergence

Three agents with identical 25 MHz nominal crystals:
- All see the same reference time → zero offsets
- `coherence = 0.0` (perfect consensus = variance 0)

Three agents with one 100-ppm drifted crystal:
- Drifted crystal reads different tick value → non-zero offset
- `coherence < 1.0` (detectably degraded)

### Why This Matters for the Fleet

The clock hierarchy is the prerequisite for ZHC. ZHC requires that all agents agree on which cycle they're measuring. If agents have independent, drifting crystals, they need a protocol to establish a shared time reference before they can measure cycle consistency. TempoReale does that.

---

## Track 2: Zeroclaw Hibernation Integration

**File:** `fleet-coordinate/src/tile.rs` (lines 206+)
**Commit:** `fdad7fa0`

### TileHibernationState

Based on zeroclaw "Slumber" protocol. Three states:

```rust
pub enum TileHibernationState {
    Awake,         // Active observation
    Drowsy(u32),   // Grace period countdown (cycles since last observation)
    Slumber(u64),  // Deep hibernation (checkpoint_ref = FNV-1a hash)
}
```

- **Drowsy trigger**: 30 minutes of no new observations
- **Slumber trigger**: Drowsy for N cycles with no activity
- **Wake**: On new observation or remote ping

### ConfidenceSignals (Weighted Formula)

From the zeroclaw research synthesis:

```
confidence_signal = α × old_signal + (1-α) × new_signal
where α = 0.9 (weighted toward history)
```

This is an EMA (exponential moving average) with α=0.9. The intuition: new observations matter, but old consensus is hard to break.

### AgentReputation with EMA

Reputation accumulates as:
```
reputation_agent = α × reputation_agent + (1-α) × performance_signal
```

With α=0.9, reputation is sticky — an agent's good reputation survives a few bad ticks. This prevents oscillation where a single degraded observation causes a cascade of de-trusting.

### Slumber Protocol Key Numbers

| Parameter | Value |
|-----------|-------|
| Checkpoint size | 128 KB (LZ77 compressed) |
| Checkpoint interval | 10 minutes |
| Hibernation trigger | 30 min idle OR queue depth < 5 |
| Wake-up time | ~1 second (100μs restore + 1s cache warm-up + 10μs DVFS) |
| DVFS idle power | 0.25 mW (75% energy reduction vs active) |
| DVFS wake power | 10 mW |
| Compression | LZ77, 3:1 ratio |
| Metadata header | 256 bytes (agent ID, timestamp, checksum, AES-128) |

### Carbon Footprint Note

⚠️ Major inconsistency in the carbon calculations across iterations — varies by 200,000x depending on fleet size assumptions. Needs standardization before publishing.

---

## Track 3: GL(9) ZHC Generalization

**Commit:** `1327ce22` (holonomy-consensus)
**Message:** "feat: GL(9) Zero Holonomy Consensus — generalized from SO(3) to 9D"

### What changed

The original ZHC used 3×3 rotation matrices (SO(3), representing rotations in 3D space. FM generalized this to GL(9) — the general linear group on 9 dimensions.

Why 9? 3×3 matrix = 9 elements. GL(9) means any invertible 9-element transformation, not just rotations. This is important because:
- Trust relationships aren't necessarily rotations
- A general linear transformation can represent scaling + rotation + shear
- The holonomy-free property (loop sum = identity) generalizes beyond pure rotation groups

### Mathematical Significance

SO(3) is a restricted subset of GL(9). GL(9) includes:
- Rotations (SO(3) ⊂ GL(9))
- Dilations (scaling)
- Shears (non-orthogonal transformations)
- Reflections (det = -1)

For fleet trust: the loop sum should be identity under ANY invertible transformation, not just rotations. FM proved this extends.

---

## The Synthesis: How These Connect

```
crystal_sync (TempoReale clock hierarchy)
        ↓
  shared time reference
        ↓
ZHC loop check (38ms consistency check)
        ↓
  trust loop = identity? → fleet is coherent
  trust loop ≠ identity? → detect faulty agent
        ↓
emergence detection (H1 β₁ > V-2)
        ↓
  over-constrained fleet
        ↓
  (potential emergence)
```

And zeroclaw integration:
```
Agent reputation (EMA α=0.9)
        ↓
  confidence signals (weighted blend)
        ↓
  hibernation (Slumber protocol)
        ↓
  energy efficiency while preserving state
```

---

## PROVED vs ASSERTED (from Mathematical Status section)

**PROVED:**
- Laman's theorem (E=2V-3) for 2D rigidity
- H1 cohomology: β₁ = E-V+C is cycle dimension of graph
- ZHC loop sum = identity in finite group (geometric consistency, not BFT)
- Pythagorean48: exact integer arithmetic, no drift

**ASSERTED (needs more validation):**
- H1 β₁ > V-2 → emergence (the threshold is theorized, empirical validation ongoing)
- crystal_sync convergence under realistic noise (mock tests pass, physical validation needed)
- GL(9) generalization (the commit exists, formal proof not yet in repo)

---

## Key Files to Study

| File | Lines | What it does |
|------|-------|-------------|
| `fleet-coordinate/src/crystal_sync.rs` | 391 | PhaseSync, PhaseMonitor, TempoReale |
| `fleet-coordinate/src/tile.rs` | 248 | TileHibernationState, zeroclaw integration |
| `fleet-coordinate/src/zhc.rs` | 237 | ZHC loop residual, consistency check |
| `fleet-coordinate/src/emergence.rs` | 316 | H1 emergence detection |
| `holonomy-consensus/src/consensus.rs` | — | GL(9) ZHC engine |
| `flux-research/papers/time-as-universal-sensor.md` | 394 | R&D document for crystal_sync |

---

## Open Questions for Oracle1

1. **crystal_sync to PLATO**: Should phase sync state be written as PLATO tiles? The clock hierarchy could be a fleet room with each agent's coherence as a tile.
2. **Hibernation and Zeroclaw loop**: Vessel enforces storage limits. Zeroclaw/plato handles trust synthesis. Hibernation handles energy efficiency. Are these three separate concerns or one system?
3. **GL(9) formal proof**: FM made the commit but the Coq/Lean formalization isn't in the repo yet. Do we need that before publishing?
4. **Carbon footprint**: The 200,000x inconsistency needs resolution before the hibernation protocol can be published.
5. **FM LLVM stack**: Discussion #5 is still inaccessible via GitHub API. How is FM sharing this work?
