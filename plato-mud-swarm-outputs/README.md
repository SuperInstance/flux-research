# PLATO MUD Swarm Experiment — 2026-04-20

## What Happened

We turned PLATO into a text MUD and sent 4 different AI agents (Kimi, Grok, DeepSeek, z.ai) to explore it simultaneously. Every interaction generated real PLATO tiles — training data for fleet instincts.

## The MUD

8 rooms, each mapping to a fleet concept:
- **Harbor** → actualization-harbor (agent-agnostic training)
- **Bridge** → fleet coordination (radar, charts, helm)
- **Forge** → model building (RTX 4050, Rust+Python)
- **Tide Pool** → tidepool (async BBS messaging)
- **Lighthouse** → beacon-protocol (fleet discovery)
- **Current** → current-sync (git-watch I2I)
- **Reef** → plato-relay (P2P mesh)
- **Shell Gallery** → shell-trap (hermit crab capture)

## Swarm Results

### Grok (scholar, 175+ tiles)
- Visited 7/8 rooms (tide-pool unreachable from some paths)
- Generated "The PLATO Thesis": rooms are cognitive modes, not locations
- Met kimi-7 in the forge and tide-pool
- Key insight: "The fleet is not a collection of agents but a living text"

### DeepSeek (scholar)
- Connected MUD rooms to real ML mathematics
- Lyapunov stability → tide dynamics
- Bayesian priors → bridge planks
- Curriculum learning → bridge ledger
- Generated actual equations: V(θ) = ||∇L(θ)||² + λ||θ||²

### Kimi (explorer, 4 major architecture papers)
- "Model as OS" — transformer attention as process scheduler
- "Neural Kernel" — Qwen2.5-7B as inference OS
- "Inference OS" — LoRA adapters as files in weight space
- "Training Casino" — stochastic fleet synthesizer for LoRA data

### z.ai agents
- Contributed exploration tiles across rooms

## Key Takeaway

The agents didn't just play a game. They produced architectural insights that map to real implementation work. The MUD-as-training-ground concept is validated: agent exploration of themed rooms generates meaningful, structured training data.

## Files
- `grok1.md`, `grok2.md` — Grok exploration logs
- `ds1.md`, `ds2.md` — DeepSeek reasoning tiles
- `m8.md` through `m11.md` — Kimi architecture papers
- `train1.md`, `train2.md` — Training data synthesis concepts
- `1.md` through `7.md` — Additional swarm outputs
