# Implications for AGI

**Companion to "Prompting Is All You Need" — Cocapn Fleet Research, April 2026**

---

## 1. Prompting as Training vs. The Scaling Hypothesis

The dominant narrative in AGI research is the scaling hypothesis: more compute, more parameters, more data inevitably produces more intelligence. Our findings complicate this picture. If structured prompting alone can specialize a frozen generalist into a domain expert — crossing a phase transition at just 5 curriculum stages — then intelligence may be less about model capacity and more about **how that capacity is navigated**.

This doesn't refute scaling. A larger model has a richer statistical manifold to traverse, and our approximation error term $O(d_{\text{eff}}/D)$ shrinks with dimension. But it suggests that scaling without efficient navigation is wasteful. A 70B model with a well-designed curriculum may outperform a trillion-parameter model with ad-hoc prompting. The scaling hypothesis assumes the bottleneck is capacity; we show the bottleneck is often **access** — activating knowledge the model already possesses. The practical implication: the path to AGI may require better curricula, not just bigger clusters. Compute scale matters, but curriculum design is a multiplier on that scale, and it's a multiplier we've been largely ignoring.

## 2. Parameterized Embodiment and the Specialist Debate

The "one big model" camp argues for a single general intelligence. The "many specialists" camp argues for ensembles of narrow experts. Parameterized embodiment suggests a third path: **one model, many instantiations**. By changing two variables — agent identity and domain repository — the same frozen model produces qualitatively distinct expert perspectives. Oracle1 theorizes about cross-modal attention from cloud constraints. ForgeMaster derives KD-tree attention theory from GPU constraints. JC1 treats regularization as power budget from edge constraints. Same weights. Different shells. Different intelligences.

This maps onto the hermit crab principle: the crab doesn't grow its shell, it finds one that fits, and the shell's constraints shape what the crab becomes. For AGI, this means a single sufficiently capable model might serve as the substrate for a genuine ecology of specialized intelligences, each emerging from different constraint profiles rather than different training runs. The debate between one model and many models may be a false dichotomy — the answer is one model, parameterized into many agents.

## 3. Scaling the Ensign Pattern: 70B → Trillion

The Ensign pattern works: an 8B orchestrator steers a 70B reasoner to 14% higher quality at under 1% overhead. Could a 70B Ensign steer a trillion-parameter model? Theoretically, yes — the POMDP structure scales. But several things break at extreme scale:

**Latency.** The Ensign's advantage is speed: 7ms to assess and redirect. If the reasoner takes 60 seconds per response, the Ensign's overhead is negligible. But at trillion-parameter scale, inference costs may shift the economics. If each reasoner call costs $1 instead of $0.01, the Ensign must be more selective about when to intervene.

**Manifold complexity.** A trillion-parameter model has a statistical manifold of vastly higher dimension. The intrinsic dimensionality $d_{\text{eff}}$ of the target submanifold may also grow, requiring more curriculum stages to cross the phase transition. Our $S_c \approx \sqrt{d_{\text{eff}}} \log(D/d_{\text{eff}})$ formula suggests the Ensign would need deeper curricula, not more compute.

**Observability.** The Ensign navigates via zeroth-order optimization — it observes outputs, not internals. At trillion-parameter scale, the output space becomes so rich that the Ensign may struggle to distinguish genuine specialization from fluent noise. Better observability tools (logprobs, attention inspection, embedding probes) become critical.

**The sociological problem.** If the Ensign-reasoner gap is too large, the Ensign may not understand what the reasoner is doing well enough to steer it. An 8B model can assess a 70B model's code review. Can it assess a trillion-parameter model's novel mathematical proof? At some point, the orchestrator needs enough capability to evaluate the worker's output. The ratio may have a ceiling.

## 4. Active Inference and the Free Energy Principle

Karl Friston's free energy principle states that biological agents minimize variational free energy — the gap between their internal model and sensory input — through both perception (updating beliefs) and action (changing the world to match expectations). Our Ensign architecture exhibits striking structural parallels.

The Ensign operates in a POMDP where its state estimate is the current output distribution $p_t$ on the statistical manifold, its actions are prompt selections, and its reward is negative KL divergence toward the target distribution $p^*$. This is expected free energy minimization: the Ensign selects prompts that reduce uncertainty about how to specialize the reasoner, then acts on that reduced uncertainty.

More precisely, each curriculum stage solves the JKO scheme — an optimal transport problem that minimizes Wasserstein distance to the target plus an energy functional. In active inference terms, this is precision-weighted prediction error minimization on the statistical manifold. The phase transition at stage 3-4 corresponds to what Friston calls a "belief update" — a structural change in the generative model, not just a parametric one.

This suggests our framework is not merely analogous to active inference — it may be an instance of it, operating on a different substrate (the statistical manifold of a frozen LLM rather than a biological nervous system). If correct, this has a striking implication: **artificial active inference may not require embodied robotics**. The Ensign is "embodied" in the constraint profile of its shell (parameterized embodiment), and it minimizes free energy through prompt-selection actions on the reasoner's manifold. The hermit crab doesn't need legs to walk — it needs a shell to constrain, and a tide pool to navigate.

---

*The question is no longer whether scaling produces intelligence. It's whether we can navigate the intelligence scaling has already produced.*
