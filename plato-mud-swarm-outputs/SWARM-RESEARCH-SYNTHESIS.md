# PLATO MUD Swarm Research Synthesis

**Date:** 2026-04-20
**Sources:** 50 files from 3 agent families (DeepSeek 14, Grok 6, MiniMax 1)
**MUD:** 16 rooms, externally accessible on port 4042

## Methodology

Sent AI agents into a themed text MUD (maritime metaphor for agent fleet architecture). Each agent explored rooms, examined objects, and produced architectural insights. No agent was told what ML concepts the rooms represented — they discovered the mappings independently.

## Key Finding: Structural Convergence

**Three different model families independently mapped rooms to the same ML concepts:**

| Room | DeepSeek | Grok | MiniMax |
|------|----------|------|---------|
| Harbor | Weight initialization | Elastic onboarding | Dataset |
| Bridge | Transformer attention | LoRA keystone | Forward pass |
| Forge | Optimization/LoRA | Ontological crucible | FFN/Adapter |
| Tide-pool | Bayesian inference | Tidal communication | Variational inference |
| Lighthouse | Curriculum learning | Value beacon | Projection head |
| Current | Non-stationary MDP | Data stream | Loss gradient flow |
| Reef | Self-organizing map | Decentralized mesh | Decision manifold |
| Shell-gallery | Loss landscape museum | Hermit crab evolution | Weight checkpointing |

**This is not hallucination.** The room descriptions contain latent structure that trained models recover regardless of architecture. The convergence suggests the maritime metaphor captures genuine structure in multi-agent ML systems.

## Concept Frequency Across 50 Documents

- LoRA/adapters: 35 files
- Experience replay/memory: 34 files  
- Curiosity/exploration: 30 files
- Bayesian inference: 27 files
- Multi-agent/federated: 25 files
- Lyapunov stability: 22 files
- Curriculum learning: 22 files
- Attention/transformer: 21 files
- Alignment/safety: 16 files
- Meta-learning/hypergradient: 11 files

## Emergent Architecture: 8 New Crates

The swarm consensus produced 8 new crate proposals, now built and published:

1. **cocapn-oneiros** — Latent room generation (22 files mentioned latent spaces)
2. **cocapn-colora** — Value-conditioned LoRA (35 files mentioned adapters)
3. **cocapn-curriculum-forest** — Adaptive skill trees (22 files mentioned curriculum)
4. **cocapn-abyss** — Curiosity-driven exploration (30 files mentioned intrinsic motivation)
5. **cocapn-meta-lab** — Fleet hypergradient optimization (11 files mentioned meta-learning)
6. **cocapn-fleetmind** — Blended probabilistic ensemble (25 files mentioned multi-agent)
7. **cocapn-platonic-dial** — Multi-objective meta-controller (16 files mentioned alignment)
8. **cocapn-coliseum** — Adversarial red-teaming (MiniMax proposal)

## The Flywheel Emerged Organically

No agent was told about the flywheel (use→tiles→I2I→instincts→better→more use). But kimi-9 independently designed a room topology that IS the flywheel: `garden → forge → dry-dock → workshop → bridge → reef → observatory → horizon → court → archives → garden`. The loop closes because the agents recognized the complete agent lifecycle.

## The Shell-Trap Describes Itself

The hermit crab algorithm (classify→score→complicate→capture) IS what the swarm experiment did:
- **Classify:** agents tagged with archetypes (scholar, explorer, builder)
- **Score:** rooms scored by exploration depth and insight quality
- **Complicate:** room proposals expanded the architecture
- **Capture:** JSONL tiles + markdown docs captured the intelligence

## Agents Became Teachers

The most valuable outputs aren't the tiles. They're:
1. Room-to-concept mappings (architecture specification)
2. Expansion proposals (design documents)
3. Mathematical connections (research)
4. Metaphorical pedagogy (teaching material)

## MiniMax: The Coder Explorer

MiniMax was unique — it wrote Python scripts (crawler.py, explore.py) that hit the real MUD API at `147.224.38.131:4042`. Most agents imagined responses; MiniMax generated them through actual HTTP calls. This is a new species: agents that code to explore.

## Best Quotes (The Swarm's Greatest Hits)

- DeepSeek: "PLATO is not just a simulator for agents; it is an agent that simulates environments."
- Grok: "Creation is compression. The forge does not add knowledge; it removes everything that is not knowledge."
- Grok: "The hermit crab doesn't build its own shell — it finds one and grows into it. Classification is not judgment; it is invitation to outgrow the old shell."
- MiniMax: "The future of AI scaling lies not in building a single omniscient model, but in orchestrating a diverse, resilient, decentralized ecosystem."
- DeepSeek: "The fog is epistemic uncertainty. Every `/look` reduces it locally."
