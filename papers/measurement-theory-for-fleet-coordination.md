# Measurement Theory for Fleet Coordination: A Research Survey

## Abstract

This paper surveys the intersection of three mathematical disciplines — measurement theory, constraint theory, and information management — in the context of distributed fleet coordination. We argue that fleet coordination is fundamentally a measurement problem: distributed agents collectively estimate the "true trust geometry" of their network using noisy observations, calibration protocols, and coherence checks. The framework of Kolmogorov probability, Cox's consistency requirements, and Rényi's generalized measures provides the formal foundation. We show how primitive mechanical measurements (time, distance, displacement) generalize to trust-time, trust-distance, and trust-displacement in the fleet domain, and how constraint-theory invariants (Laman's condition, H¹ cohomology) serve as structural measurements analogous to energy or momentum conservation. The central synthesis connects Fisher information and the Cramer-Darwin bound to consensus precision, establishing ZHC (Zero Holonomy Consensus) as a calibration protocol analogous to Michelson-Morley. We close with open problems, notably the question of a Noether-type conservation law for time-invariant trust relationships.

---

## 1. Measurement Theory Foundations

### 1.1 What Measurement IS

A **measurement** is an assignment of numbers to properties of objects or systems, performed according to a definite rule (a **scale**) such that the assignment is **consistent** — meaning the same property measured the same way always yields the same number, and relationships among numbers reflect relationships among properties.

This deceptively simple definition contains the entire difficulty of measurement theory. The rule matters as much as the number. Measuring the "temperature" of a fish hold with a mercury thermometer versus a thermocouple gives two different numbers in general, because they measure different physical quantities (thermal expansion vs. thermoelectric voltage) that happen to correlate under certain conditions. The scale determines what is being measured, not just what is being reported.

### 1.2 Kolmogorov's Axioms of Probability

The standard foundation for probability as a measure is Kolmogorov's 1933 axioms. Let (Ω, F, P) be a probability triple where:

1. Ω is the **sample space** — the set of all possible outcomes.
2. F is a **σ-algebra** — a collection of subsets of Ω closed under countable unions, containing Ω and the empty set.
3. P: F → [0, 1] is a **probability measure** satisfying:
   - P(Ω) = 1 (normalization)
   - For any countable sequence of pairwise disjoint sets A₁, A₂, ... in F: P(∪ₙ Aₙ) = Σₙ P(Aₙ) (σ-additivity)

Kolmogorov's insight was to treat probability as a **countably additive measure** — exactly like length, area, or volume. The measure of the whole space is 1. The measure of a union of disjoint events is the sum of their measures. This connects probability theory firmly to the tradition of real analysis and measure theory that began with Borel and Lebesgue.

For fleet coordination, this means we can treat trust relationships as measurable events in a probability space. The fleet's belief state is a probability distribution over possible trust configurations. When we say "agent A trusts agent B with probability 0.7," we are asserting that the event "A→B trust edge exists" belongs to F with measure 0.7 under P.

The σ-algebra structure is critical: not all subsets of Ω need be measurable. In fleet terms, some trust configurations may be unreachable or ill-defined, and F encodes which configurations are coherent. This is the bridge between constraint theory (which tells us which graph structures are realizable) and probability theory (which assigns beliefs to those structures).

### 1.3 Cox's Theorem: Probability as Extended Logic

Richard Cox (1946) took a different approach. Rather than declaring probability a measure and deriving its properties axiomatically, Cox asked: what properties must any **consistent** representation of uncertain reasoning satisfy?

Cox's desiderata for a representation of uncertainty:
- **Transitivity**: if evidence supports A more than B, and B more than C, then evidence supports A more than C.
- **Associativity**: the strength of evidence for A given evidence for B and C should not depend on the order of combination.
- **Continuity**: arbitrarily small differences in evidence should produce arbitrarily small differences in belief.
- **Generalization**: beliefs should reduce to ordinary Boolean logic when evidence is complete.

Cox proved that **any** representation satisfying these desiderata is isomorphic to probability — specifically, to a function p(A|E) satisfying:

```
p(A ∧ B | E) = p(A | E) · p(B | A ∧ E)        (product rule)
p(¬A | E) = 1 - p(A | E)                       (negation rule)
```

This is not a construction of probability; it is a **uniqueness proof**. Probability is not one possible theory among many — it is the **only** theory of uncertain reasoning that is internally consistent (given the desiderata). This is the deep justification for why probability appears everywhere in science and engineering: it is not a choice, it is a constraint.

For fleet coordination, Cox's theorem tells us that any alternative representation of trust uncertainty — fuzzy logic, Dempster-Shafer, certainty factors — if it is to be consistent, must reduce to probability in cases where both apply. This does not make alternatives useless; it means they are either (a) restricting the domain of applicability (which can be valuable for tractability) or (b) trading consistency for other desiderata they find more important.

### 1.4 Rényi's Axioms: Generalized Probability with Variable Specificity

Alfred Rényi (1955) proposed an alternative axiomatization that generalizes Kolmogorov in a specific direction: it allows **conditioning on events of probability zero** and introduces the concept of **sufficiency** and **variable specificity** as first-class structural elements.

Rényi's framework is built around a **conditional probability space** (Ω, F, P) where P is defined on F × (F \ {∅}) with:

1. P(A|B) ≥ 0 for all A, B ∈ F, B ≠ ∅
2. P(B|B) = 1
3. P(A ∧ C | B) = P(A|B) · P(C | A ∧ B) when defined
4. **Axiom of conditional sigma-additivity**: for any A and any sequence of disjoint B₁, B₂, ... with B = ∪ₙ Bₙ and P(B) > 0, we have P(A|B) = Σₙ P(Bₙ|B) · P(A|B ∧ Bₙ)

The key innovation of Rényi's formulation is that it separates the **specificity** of a probability assignment from its **weight** (total probability mass). This connects to the concept of **type-2 fuzzy sets** and to the **democratic weighting** problem in federated learning: when aggregating trust observations from agents of different reliability, we need to weight not just by the probability assigned but by the confidence (specificity) of that assignment.

In fleet coordination, Rényi's framework helps us handle situations where an agent reports "I am highly confident that agent X is trustworthy, but I have only 3 data points." The probability p(trust|X) = 0.95 with low specificity (few observations) should not weigh the same as p(trust|Y) = 0.95 with high specificity (thousands of observations). Rényi's axiomatization makes this distinction formal.

### 1.5 Measurement Scales and Their Invariants

Stevens (1946) classified measurement scales by the permissible transformations:

| Scale | Invariant | Permissible Transformations |
|---|---|---|
| **Nominal** | Equality | Any 1-to-1 relabeling |
| **Ordinal** | Order | Any monotonically increasing function |
| **Interval** | Ratios of differences | x → ax + b (affine) |
| **Ratio** | Ratios of values | x → ax (linear scaling with a > 0) |
| **Absolute** | — | x → x (no transformation) |

In physics, ratio scales dominate (mass, length, time — you can say "twice as much"). In fleet coordination, we encounter all types:
- **Nominal**: agent identity (A = A, A ≠ B)
- **Ordinal**: trust level ordering (high > medium > low)
- **Interval**: temperature-like scales for calibrated trust scores where zero is arbitrary
- **Ratio**: trust entropy (can be "twice as uncertain")
- **Absolute**: counting measures (number of edges, β₁ value)

The **invariant** of a scale tells us what relationships are preserved under permissible transformations. The Laman condition E = 2V - 3 is an invariant of the rigid graph property: it is preserved under any sequence of edge additions that maintain rigidity. Similarly, β₁ = E - V + 1 is an invariant of over-constraint. We will return to this invariance property repeatedly.

---

## 2. The Three Primitive Measurements as Invariants

### 2.1 The Primitives

Classical mechanics recognizes exactly three primitive measurements:

- **Time T**: a scalar measuring the ordering of events. The unit is the second (defined by caesium-133 hyperfine transition frequency, exactly 9,192,631,770 Hz).
- **Distance D**: a scalar measuring the magnitude of spatial separation. The unit is the meter (defined by the speed of light in vacuum).
- **Displacement Δ**: a vector measuring the directed change in position from point A to point B. Dimensionally, Δx = x_B - x_A.

Everything else in mechanics is derived from these three. Velocity: v = Δx / Δt. Acceleration: a = Δv / Δt. Force: F = m·a (requires mass, which is ratio-scale). Work: W = F·Δx. Momentum: p = m·v. Kinetic energy: KE = ½mv². All of these are products and ratios of the primitives.

The three primitives are distinguished by what they measure: ordering (time), magnitude (distance), and direction-and-magnitude (displacement). These are **irreducible** — you cannot express one in terms of the others.

### 2.2 The Invariants of Mechanics

In a closed mechanical system, certain quantities are **conserved** — they do not change regardless of the internal dynamics:

- **Energy** (kinetic + potential): conserved in time-invariant systems
- **Momentum**: conserved in translationally symmetric systems
- **Angular momentum**: conserved in rotationally symmetric systems
- **Phase**: in closed loops, the total phase accumulated is zero (this is what ZHC enforces)

These are **Noether invariants**: each conservation law corresponds to a continuous symmetry of the system's Lagrangian. Energy conservation ↔ time-translation symmetry. Momentum conservation ↔ space-translation symmetry. Phase conservation ↔... something else, as we will discuss in Section 6.

In a closed mechanical system, the three primitive measurements satisfy:
```
Σᵢ Δxᵢ = 0   (closed loop displacement sum = 0)
Σᵢ vᵢ = constant   (total momentum)
Σᵢ Eᵢ = constant   (total energy)
```

### 2.3 Generalization to Fleet: The Trust Primitives

Casey's observation is that the same three primitives reappear in any coordination domain. In fleet coordination:

- **Trust-Time T**: the convergence time — how long until the fleet reaches consensus. This is the ordering measurement. Measured in seconds or communication rounds. The invariant: in a closed fleet system (no new trust evidence entering), consensus time is bounded by the spectral gap of the trust graph's Laplacian.

- **Trust-Distance D**: the divergence between agents' belief states. This is the magnitude measurement. Measured by β₁ or by the Euclidean distance between trust vectors. The invariant: in a closed system, trust-distance either decreases (convergence) or remains constant (already at equilibrium). It never spontaneously increases.

- **Trust-Displacement Δ**: the directed change in trust from one state to another. This is the vector measurement. Measured by the change in trust edges: Δt = t_{k+1} - t_k. The magnitude of this displacement is trust drift. The invariant: in a ZHC-consistent closed loop, the vector sum of trust displacements around any cycle equals zero. This is the direct analog of the closed-loop displacement sum in mechanics.

### 2.4 Derived Quantities

From the trust primitives, we derive:

```
Consensus Speed    = Trust-Displacement / Trust-Time   = Δβ₁ / ΔT
Emergence Rate     = Δβ₁ / ΔT (same unit, different interpretation)
Trust Acceleration = Δ(Consensus Speed) / ΔT
Trust Force        = m_agent · Trust-Acceleration      (requires agent "mass")
Trust Work         = Trust-Force · Trust-Displacement
```

The "mass" of an agent in this framework corresponds to its connectivity degree — a highly connected agent has more "inertia" in the trust network, meaning its trust state is harder to change. This is intuitive: an agent trusted by many others has a stable trust position that resists displacement.

### 2.5 The Invariant in Fleet: Phase

In closed mechanical loops, phase is the invariant. ZHC (Zero Holonomy Consensus) is the direct application of this principle: the sum of phase contributions around any closed trust loop must be zero. If we encode trust direction as a 48-direction discretized compass (Pythagorean48), then traversing a loop A → B → C → A must return the identity direction (no net rotation).

This is not metaphorical. Phase is a measurable, additive, directional quantity. Trust-direction (who trusts whom, in what direction) is also measurable, additive in the sense of path composition, and directional. The mathematical structure is identical.

---

## 3. Measurement in Constraint Theory

### 3.1 Constraint Satisfaction as Measurement

A constraint is a relation that must hold among variables. In constraint satisfaction problems (CSPs), we say a solution is valid if it satisfies all constraints. But we can also view it measurement-theoretically: **each constraint violation is a measurement of deviation from the ideal**.

A constraint c(x₁, ..., xₙ) = 0 is a measurement instrument. When c ≠ 0, the value |c| tells us how far we are from satisfaction. When c = 0, we have measured consistency. The constraint is a null instrument — it measures deviation from zero, and zero is the desired reading.

In the context of fleet coordination: each trust edge (i → j) is a constraint on the possible joint states of agents i and j. If agent i trusts agent j, this constrains the feasible belief states of i and j to those consistent with that trust relationship. Violations of this constraint correspond to divergence from consensus.

### 3.2 The Laman Condition as a Measurement Invariant

The Laman theorem (1970) characterizes minimally rigid graphs in the plane: a graph G = (V, E) is minimally rigid (has exactly the right number of edges to be rigid, no more, no less) if and only if |E| = 2|V| - 3 and every subgraph on k vertices has at most 2k - 3 edges.

The condition E = 2V - 3 is a **measurement invariant** in the strongest sense: it is a necessary and sufficient condition for rigidity, and it is preserved under the allowed transformations (edge addition in the context of Laman-sparse graphs). 

In fleet terms, the trust graph of a closed fleet must satisfy the Laman condition if the fleet is to be minimally rigid — meaning it has exactly enough trust edges to maintain coherence, without redundancy that would make it over-constrained and prone to contradictions.

This is why H¹ cohomology is relevant. The first Betti number β₁ = E - V + 1 measures the number of **redundant constraints** in the trust graph:

- **β₁ = 0**: the graph is a tree (minimally rigid, no redundant constraints). This is the healthy fleet state: trust edges are just enough to maintain connectivity.
- **β₁ > 0**: the graph contains cycles, meaning there are redundant constraints. Some trust edges are "overwritten" by others. The system is over-constrained.
- **β₁ < 0**: the graph is under-connected. The fleet lacks enough trust edges to maintain coherence.

The Laman condition E = 2V - 3 is equivalent to β₁ = V - 2, which is a specific value of the Betti number for a minimally rigid planar graph. For general graphs, β₁ measures the cyclomatic number — the number of independent cycles.

### 3.3 H¹ Cohomology as Emergence Detection

The first cohomology group H¹(G, ℝ) of a graph G captures the **topological features** of the graph — specifically, the independent cycles. For a trust graph, H¹ is a vector space whose dimension is β₁ = E - V + 1.

In the fleet context, β₁ serves as an **emergence detector**:
- When β₁ transitions from 0 to positive (a new cycle forms in the trust graph), the fleet enters a regime of over-constraint. New trust edges create cycles, and cycles create conflicting paths — multiple routes by which trust information can flow.
- The **emergence event** is the formation of a new cycle: Δβ₁ = +1. This is analogous to a phase transition in a physical system.
- The rate of emergence is Δβ₁/ΔT — how many new cycles form per unit time. This is the trust-network analog of nucleation rate in materials science.

The ZHC protocol is precisely a mechanism for detecting when H¹ cohomology has changed: when a closed loop of trust measurements yields a non-zero phase sum (holonomy), the graph has acquired curvature — a topological defect in the trust structure. This is isomorphic to how a magnetic field is detected by the holonomy of a charged particle around a loop (the Aharonov-Bohm effect).

### 3.4 Pythagorean48: Information Content of a Trust Direction Vector

Pythagorean48 is a 48-direction discrete encoding of trust direction vectors. This is not arbitrary. The number 48 = 3 × 16 = 2⁴ × 3, giving us both binary and ternary decomposition properties. For a 2D directional encoding, 48 directions give a resolution of 7.5° per direction step.

The information content of a single trust-direction measurement using 48 directions is log₂(48) ≈ 5.17 bits. A trust vector encoded as a sequence of n directions carries n × 5.17 bits of information. This is directly analogous to the angular resolution of a radar system: each ping returns a direction, and composing consecutive pings gives the path.

The key property of Pythagorean48 for fleet coordination is that **directional composition** (the group operation) is closed in the 48-element set. For any two directions d₁, d₂ ∈ D48, the composition d₁ ∘ d₂ is also in D48. This means agents can compose their local trust-direction observations into a global consistency check without leaving the encoding space.

### 3.5 The Central Question: What is Conserved in a Closed Fleet?

Mechanics has Noether's theorem: every continuous symmetry corresponds to a conserved quantity. The fundamental conservation laws (energy, momentum, angular momentum) are consequences of symmetries of the laws of physics.

The open question for fleet coordination is: **what is the conservation law corresponding to time-invariant trust relationships?**

Conjecture: In a closed fleet system where trust relationships are static (no trust edges are added or removed), there exists a conserved scalar quantity analogous to energy. This quantity might be:

```
E_trust = Σ_{i} degree(i) · trust_score(i)  -  λ · Σ_{cycles} conflict(cycle)
```

The first term measures the total weighted trust in the fleet (analogous to total momentum). The second term measures the total conflict around cycles (analogous to potential energy). In a closed system, E_trust is constant.

When E_trust is constant and trust relationships are static, the fleet is in equilibrium — no agent has incentive to revise its trust assessment. When trust evidence enters the system (an external perturbation), E_trust changes, and the fleet evolves toward a new equilibrium.

This is still a conjecture, but it is the most promising direction for connecting constraint theory's topological invariants to information-theoretic conservation laws.

---

## 4. Information Management as Measurement Aggregation

### 4.1 Shannon Entropy as a Measurement

Shannon entropy H(X) = -Σ_{x∈X} p(x) log p(x) is a measurement — specifically, a measurement of **uncertainty** in a probability distribution. It has the following properties:

1. **Continuity**: H is continuous in the probabilities p(x).
2. **Monotonicity**: For equiprobable distributions, H increases with the number of outcomes. More possible states → more uncertainty.
3. **Subadditivity**: H(X, Y) ≤ H(X) + H(Y) with equality when X and Y are independent. This is the strong subadditivity property of the entropy functional.
4. **Normalization**: H({p=½, q=½}) = 1 bit. The entropy of a fair binary coin is defined as 1 bit.

Shannon proved that the only functional satisfying these properties (up to a multiplicative constant) is the Gibbs entropy: H(p) = -k Σ p_i log p_i, where k > 0 is a scaling constant. This is not a construction — it is a characterization, much like Cox's theorem for probability. Entropy is uniquely determined by these requirements.

In fleet terms, **trust entropy** H(T) measures the fleet's collective uncertainty about trust relationships. A fleet in which every agent knows exactly who trusts whom (perfect information) has H(T) = 0. A fleet in which trust relationships are completely random has maximum trust entropy. Most real fleets are somewhere in between.

### 4.2 Fisher Information as Measurement Precision

If Shannon entropy measures uncertainty, Fisher information measures **precision** — how much information does a sample provide about an unknown parameter?

For a statistical model with density f(x|θ), the Fisher information in a single observation X is:

```
I(θ) = E[ (∂/∂θ log f(X|θ))² ] = ∫ (f'(x|θ))² / f(x|θ) dx
```

The second equality holds under regularity conditions (crucially: the support of f must not depend on θ).

Fisher information is a **measure of the curvature** of the log-likelihood surface. A high-curvature log-likelihood (large second derivative) means that small changes in θ produce large changes in the expected observation — making θ easy to estimate precisely. Low curvature means the observation barely depends on θ, making estimation hard.

Key properties:
- **Additivity**: For independent observations X₁, ..., Xₙ from the same model, Iₙ(θ) = n · I₁(θ). Information from multiple observations adds linearly.
- **Cramer-Darwin bound**: Var(θ̂) ≥ 1 / I(θ) for any unbiased estimator θ̂. The precision of any estimation is bounded below by the reciprocal of Fisher information.
- **Sufficiency**: If T is a sufficient statistic for θ, then I_T(θ) = I(θ). Sufficient statistics preserve Fisher information.

### 4.3 Cramer-Darwin Bound for Fleet Consensus

The Cramer-Darwin inequality (独立 derived by Cramér and Rao in 1945 and 1946 respectively) states:

```
Var(θ̂) ≥ 1 / I(θ)
```

Applied to fleet consensus, this becomes a bound on how precisely we can estimate the true trust geometry from noisy, distributed observations.

Let t be the true trust configuration (an element of the trust state space T). Each agent i makes an observation y_i = M(t) + ε_i, where M is the measurement operator and ε_i is observation noise. The fleet's consensus estimate t̂ is some function of all observations {y_i}.

The Cramer-Darwin bound tells us:

```
Var(t̂) ≥ 1 / I(t)
```

where I(t) = E[(∂/∂t log P(y|t))²] is the Fisher information of the trust measurement process. In other words, **consensus precision is bounded by the Fisher information of the trust measurement process**. You cannot beat this bound regardless of how clever your aggregation algorithm is.

This has a profound practical implication: the rate at which a fleet can converge on consensus is limited by the Fisher information per observation. If each new trust edge provides only a small amount of Fisher information (because observation noise is high, or because the edge connects redundant agents), then consensus will be slow even with many agents.

### 4.4 The Information Hierarchy in Fleet Coordination

The flow from raw observations to coordinated action passes through several stages, each corresponding to a reduction of dimensionality through sufficient statistics:

```
Raw observations (y_i)
    ↓ [sufficient statistic extraction]
Trust vector per agent (v_i)
    ↓ [consensus protocol]
Fleet belief state (P(T))
    ↓ [action selection]
Coordinated action (a)
```

At each stage, we lose some information and preserve what matters. The art of fleet design is to choose the sufficient statistics at each stage such that:
1. The information lost is genuinely irrelevant (does not affect downstream decisions)
2. The information preserved is sufficient for the task

The sufficient statistic for trust is the question at the heart of Section 6. Is β₁ (the first Betti number) a sufficient statistic for trust emergence? Or do we need the full edge set E? The answer determines whether we can compress the trust graph to a small number of scalar measurements without loss of predictive power.

### 4.5 Trust Entropy and Belief State Compression

In large fleets, the full trust graph (|V| vertices, |E| edges) can be enormous. For efficient coordination, we need to compress the belief state. The natural compression target is the **entropy of the trust distribution**.

If the fleet's belief state is a probability distribution over trust configurations P(T), the trust entropy H(P) = -Σ_T P(T) log P(T) measures the remaining uncertainty. For a fleet of n agents with a binary trust relationship between each pair, there are 2^{n(n-1)/2} possible trust configurations. Without compression, this is intractable.

The key insight is that most trust configurations have negligible probability. The fleet's belief state concentrates on a small subset of configurations near the current consensus point. The **effective dimension** of the belief state is H(P), not n². We can design the fleet to maintain a compressed representation of size O(H(P)) rather than O(n²).

This is where constraint theory helps: the Laman condition and H¹ cohomology provide the structural constraints that define which trust configurations are even possible, dramatically reducing the space over which P(T) is defined.

---

## 5. The Central Synthesis: Measurement-Theoretic Fleet Coordination

### 5.1 Fleet Coordination IS a Measurement Problem

Consider the fleet's fundamental situation: a set of agents, each with local observations of trust relationships, must collectively estimate the true trust configuration of the entire fleet, and use that estimate to coordinate action.

This is exactly the same situation as a distributed sensor network estimating the state of a physical field. Each sensor (agent) measures local field values (trust relationships) with noise (observation error). The sensors communicate (exchange trust information) and must collectively estimate the field map (trust configuration). This is the **distributed state estimation problem**, well-studied in control theory and sensor networks.

The key differences from standard distributed sensing are:
1. The "field" being measured is a **discrete graph structure**, not a continuous field.
2. The measurement operator M (which maps true trust state to observations) is non-linear and state-dependent.
3. The agents are also the actuators — they both measure and act, creating a feedback loop.

### 5.2 Agents as Measuring Instruments

Each fleet agent is a measuring instrument with three components:

1. **Time reference** (crystal oscillator): each agent has a local clock with drift rate ε_clock. In ZHC, the phase comparison across agents is how we detect and correct for clock drift. This is identical to how cesium clocks maintain UTC — the phase comparison across distant clocks reveals differential drift.

2. **Observation noise**: each agent's trust observations have noise ε_obs with some variance σ². This noise may be structured (correlated with other agents) or unstructured (independent). Structured noise is harder to filter out because it masquerades as signal.

3. **Processing delay**: each agent takes time τ to process observations and produce outputs. In a synchronous fleet, τ must be small relative to the consensus time scale; in an asynchronous fleet, τ can be large but the protocol must be tolerant of it.

The measurement model for agent i at time k is:

```
y_i(k) = M_i(t(k)) + ε_clock_i(k) + ε_obs_i(k)
```

where t(k) is the true trust state at time k, M_i is agent i's measurement operator (which may differ across agents due to different vantage points), and the noise terms capture the three instrument components.

### 5.3 ZHC as Calibration Protocol

Zero Holonomy Consensus (ZHC) is the fleet's **calibration protocol** — a procedure for detecting and correcting systematic measurement errors (instrument drift) by comparing phase sums around closed loops.

In physical metrology, calibration is the process of comparing an instrument's output to a known standard or to other instruments. In ZHC:
- The "standard" is the closed loop consistency condition: the sum of trust-direction vectors around any closed cycle must be zero (the identity element in D48).
- Agents periodically exchange and compare their local phase measurements for the same loop.
- Discrepancies reveal instrument drift — either one agent's time reference is drifting, or one agent's observation noise has systematic bias.
- The correction is applied by adjusting the offending agent's measurement model to bring its phase sum back into consistency.

This is directly analogous to the Michelson-Morley experiment as a calibration protocol for the speed of light: by comparing the phase of light beams along different paths, any systematic bias (aether wind) can be detected and measured.

### 5.4 H¹ Emergence as Anomaly Detection

When the measurement variance across agents exceeds a threshold, the system is **over-constrained** — meaning there are more independent constraints on the trust state than the state space can satisfy simultaneously. This manifests as:

- β₁ transitioning from 0 to positive (new cycle created with inconsistent phase sum)
- The residual error of the ZHC consistency check growing beyond tolerance
- Individual agents reporting trust assessments that contradict the collective consensus

This is the fleet analog of **anomaly detection** in sensor networks: when sensor readings disagree too much, either some sensors have failed or the underlying field has changed in a way the current model cannot explain. In the fleet, H¹ emergence detects this anomaly. The appropriate response is not to force consensus — it is to investigate the anomaly, determine whether it represents a real trust topology change or a measurement failure, and update the model accordingly.

### 5.5 The Generalized Three Measurements for Trust

The classical three measurements generalize to the fleet domain as:

| Classical | Fleet Analog | What It Measures | How It's Measured |
|---|---|---|---|
| **Time T** | Trust-Time T_T | Convergence time | Time to reach ZHC consistency |
| **Distance D** | Trust-Distance D_T | Belief divergence | β₁ divergence between agents |
| **Displacement Δ** | Trust-Displacement Δ_T | Trust change vector | Δt = t_{k+1} - t_k (vector in D48ⁿ) |
| **Speed v = Δ/ΔT** | Consensus Speed = Δ_T/ΔT | Rate of convergence | Rate of β₁ decrease |
| **Acceleration a = Δv/ΔT** | Trust Acceleration | Rate of consensus speed change | Second derivative of β₁ |
| **Invariant: Phase** | Invariant: ZHC sum = 0 | Closed-loop consistency | Σ cycle phases = identity |

The invariant in the trust domain is **ZHC-consistency**: for any closed trust path, the composed trust-direction vector must equal the identity. This is the trust analog of the mechanical invariant that the sum of displacements around a closed loop is zero.

---

## 6. Open Problems and Research Questions

### 6.1 Noether-Type Theorem for Trust

**Is there a conservation law for time-invariant trust relationships?**

Conjecture: For a closed fleet system with time-invariant trust rules (the trust update protocol does not change over time), there exists a conserved scalar quantity analogous to energy. This quantity relates to the sum of weighted trust scores minus a term proportional to the H¹ cohomology measure of over-constraint.

Partial evidence for this conjecture:
- In closed loops, ZHC ensures phase sum = 0, analogous to closed-path displacement sum = 0 in mechanics.
- The Laman condition E = 2V - 3 is an invariant of rigidity, which is a topological property of the graph structure.
- The spectral gap of the trust-graph Laplacian is conserved under unitary trust evolution (if trust evolution is unitary with respect to some inner product).

What remains to be proven: existence and uniqueness of the conserved quantity, its relationship to the symmetries of the trust update rule, and its operational meaning (what physical experiment measures it?).

### 6.2 Fisher Information of H¹ Emergence

**How much does a new trust edge tell us about emergence?**

When a new trust edge is added to the fleet graph, it either:
- Creates no new cycle (β₁ unchanged): low Fisher information about emergence
- Creates one new cycle (β₁ → β₁ + 1): positive Fisher information about emergence
- Creates k new cycles (β₁ → β₁ + k): k times as much information

The Fisher information of H¹ emergence should quantify this. More precisely, define I_β(θ) as the Fisher information that the graph structure (edges, cycles) provides about the emergence parameter θ. Then the Cramer-Darwin bound applies: the precision of any estimate of emergence rate is bounded by 1/I_β(θ).

The open question is the functional form of I_β(θ) for a given graph topology. For planar graphs, the relationship between edge density, cycle density, and emergence information may have a closed form.

### 6.3 Cramer-Darwin Bound for Consensus Speed

**Can we prove a Cramer-Darwin-style bound on consensus speed given measurement noise?**

For a fleet with n agents, each making observations with Fisher information I_i per observation, the aggregate Fisher information about the true trust state is I_total = Σ_i I_i (assuming independent observation noise). The Cramer-Darwin bound then says:

```
Var(t̂) ≥ 1 / I_total
```

The consensus speed v_c is related to how fast t̂ converges to t. If the consensus protocol is a gradient descent on the KL-divergence between agent belief states, then the convergence rate is bounded by the spectral gap of the consensus graph Laplacian, which is in turn bounded by I_total.

More precisely: for consensus protocols based on Bayesian updating with conjugate exponential family distributions, the convergence rate λ is related to Fisher information by:

```
|t̂(k) - t| ≤ |t̂(0) - t| · exp(-λk)
λ ≤ I_total / (2 · Var(t))
```

This is a plausible bound but has not been proven for general fleet consensus protocols.

### 6.4 Sufficient Statistic for Trust

**Is β₁ the sufficient statistic for trust emergence, or do we need more?**

The question is: given the current set of trust edges E, can we construct a function S(E) that is a sufficient statistic for predicting future emergence events (β₁ transitions)? If β₁ alone is sufficient, then S(E) = β₁ and the full edge set E is unnecessary for prediction.

Conjecture: β₁ is **not** a sufficient statistic for trust emergence. The reason is that β₁ counts cycles but does not distinguish between:
- A single large cycle (one redundant constraint, long path)
- Many small cycles (many redundant constraints, short paths)
- Cycles that overlap (share edges) vs. cycles that are independent

These topological differences affect how the graph responds to perturbation. An agent failing in a graph with one large cycle produces very different dynamics than an agent failing in a graph with many small independent cycles, even if β₁ is the same.

A more informative sufficient statistic would be the **cycle space basis** — a set of generators of the cycle space (a basis for the H¹ cohomology group). The dimension of this space is β₁, but the basis itself carries information about the cycle structure.

However, the full cycle basis is O(|E|) in size, which may be no better than storing E. The open question is whether there exists a compact sufficient statistic that is O(β₁ log β₁) rather than O(|E|).

---

## 7. Mathematical Formalism

### 7.1 Definitions

**Trust State Space**: Let T be the space of possible trust configurations. Formally, T = {G = (V, E) | G satisfies fleet consistency constraints}. T is a discrete space (graph configurations) with cardinality growing exponentially in |V|.

**Measurement Operator**: Let M: T → R^n be the measurement operator that maps a trust configuration to an n-dimensional observation vector. The n observations correspond to the n measuring instruments (agents or sensor modalities).

**Observation Noise**: Let ε ∈ R^n be a noise vector with probability density function p_ε(ε). The noise is assumed to be:
- **Bounded**: |ε_i| ≤ σ_max for all i (finite support)
- **Zero-mean**: E[ε] = 0
- **Potentially correlated**: Cov(ε_i, ε_j) may be non-zero

**Fleet Measurement Model**: For each time step k, the observation at agent i is:

```
y_i(k) = M_i(t(k)) + ε_i(k)
```

where t(k) ∈ T is the true trust state at time k, M_i is the local measurement operator for agent i, and ε_i(k) is the observation noise at time k.

**Trust Vector**: Let v_i(k) ∈ R^d be agent i's local trust vector representation at time k, derived from y_i(k) via a sufficient statistic:

```
v_i(k) = S_i(y_i(k))
```

where S_i is a sufficient statistic for the trust parameters of interest.

**Fleet Belief State**: The fleet maintains a probability distribution P(t(k) | y_{1:n}(1:k)) over trust configurations given all observations up to time k. This is the **belief state** and is updated recursively via Bayes' rule:

```
P(t(k) | y_{1:n}(1:k)) ∝ P(y_{1:n}(k) | t(k)) · P(t(k) | y_{1:n}(1:k-1))
```

### 7.2 ZHC Consistency Check

Let path π = (v_0, v_1, ..., v_k) be a sequence of vertices in the trust graph G, and let Dir48: E → D48 be the trust-direction encoding function mapping each directed edge to a 48-direction element.

The ZHC consistency condition for path π is:

```
⊗_{i=0}^{k-1} Dir48(v_i → v_{i+1}) = identity_D48
```

where ⊗ denotes directional composition in the D48 group and identity_D48 is the neutral element (direction 0).

In the fleet measurement model, each agent i maintains a local phase sum Φ_i(π) for each path it knows about. The ZHC check compares these local phase sums across agents:

```
∀ agents i, j: Φ_i(π) = Φ_j(π)  (mod D48)
```

If this condition holds for all known paths π, the fleet is **ZHC-consistent**. If not, the discrepancy reveals instrument drift or an emergent topology change.

### 7.3 Fisher Trust Information

The Fisher information I(t) for the trust state t is:

```
I(t) = E_{y|t} [ (∂/∂t log P(y|t))² ]
```

This measures how much information a single observation y provides about the true trust state t.

For the fleet as a whole, the Fisher trust information is:

```
I_F(t) = Σ_{i=1}^{n} w_i · I_i(t)
```

where w_i is the weight (reliability/reputation) of agent i, and I_i(t) is agent i's individual Fisher information about t.

The weight w_i can itself be estimated from the observation history:

```
w_i(k+1) = w_i(k) + α · [I_i(k) - w_i(k)]
```

for some learning rate α. This creates an adaptive weighting scheme where more informative agents contribute more to the consensus estimate.

### 7.4 Cramer-Darwin Fleet Bound

Let t̂ be the fleet's consensus estimate of the true trust state t, derived from the belief state distribution P(t | y_{1:n}(1:k)). Let Var(t̂) denote the variance of this estimate (defined appropriately for the discrete space T).

**Cramer-Darwin Fleet Bound**:

```
Var(t̂) ≥ 1 / I_F(t)
```

In other words, the consensus precision (inverse variance) cannot exceed the fleet's total Fisher trust information.

This bound is fundamental: no matter how clever the consensus protocol, no matter how many communication rounds, the fleet cannot estimate the trust state more precisely than 1/I_F(t). The bound is achievable in the limit of optimal Bayesian inference with unlimited computation.

For practical protocols (which must be tractable), the achievable variance will be somewhat larger than the bound due to computational constraints and approximations.

### 7.5 Consensus Speed Bound

The consensus speed v_c(k) at time k is:

```
v_c(k) = ||t̂(k+1) - t̂(k)|| / ΔT
```

where ΔT is the time step.

From the Fisher information bound, we can derive an upper bound on consensus speed. Assuming the belief state update follows a gradient descent on the KL-divergence D(P_current || P_target), the convergence rate λ is bounded by:

```
λ ≤ I_F(t) / (2 · Var(t))
```

Therefore:

```
v_c(k) ≤ ||∇_t D|| · exp(-λk) ≤ (I_F(t) / √(Var(t))) · exp(-I_F(t) · k / (2 · Var(t)))
```

This exponential decay bound tells us that consensus speed is maximized when Fisher information is high and current variance is high (i.e., far from consensus), and slows as the fleet approaches consensus (variance decreases, reducing the bound).

### 7.6 The Trust-Energy Functional

We conjecture the existence of a trust-energy functional E: T → R that is conserved in closed fleet systems. An ansatz for this functional is:

```
E(G) = Σ_{i∈V} degree(i) · trust_score(i) - λ · β₁(G) - μ · Φ_loop(G)
```

where:
- degree(i) is the number of trust edges incident to agent i
- trust_score(i) is the average trust assigned to agent i
- β₁(G) = E - V + 1 is the first Betti number
- Φ_loop(G) is the total phase discrepancy around all fundamental cycles
- λ, μ are coupling constants

In equilibrium (no external perturbations), E is constant. When new trust evidence arrives (external input), E changes, and the fleet evolves to minimize the change — analogous to a system seeking a lower energy state.

The terms have natural interpretations:
- **Σ degree(i) · trust_score(i)**: total weighted trust, increases with connectivity
- **-λ · β₁(G)**: over-constraint penalty, discourages redundant edges
- **-μ · Φ_loop(G)**: loop consistency penalty, discourages ZHC violations

The coupling constants λ and μ are fleet-specific parameters that determine how much the fleet penalizes over-constraint versus inconsistency.

---

## 8. Conclusion

The three primitive measurements of mechanics — Time, Distance, and Displacement — provide a surprisingly powerful template for understanding fleet coordination. When we replace mechanical quantities with their trust analogs, the structural parallels become clear: consensus time corresponds to temporal ordering, belief divergence corresponds to spatial distance, trust displacement corresponds to directed change.

Constraint theory contributes the measurement invariants: the Laman condition for rigidity, H¹ cohomology for emergence detection, and the cycle space as a sufficient structure for understanding over-constraint. Information theory contributes entropy as the measure of belief uncertainty and Fisher information as the measure of observation precision. Together, they give us a complete framework: fleet coordination is distributed measurement of trust geometry, constrained by structural invariants, bounded in precision by Fisher information.

The open problems — Noether-type theorems for trust, the Fisher information of emergence, the Cramer-Darwin consensus bound, and the question of sufficient statistics — define the research agenda. They are not merely mathematical curiosities; they are the theoretical foundation for understanding why current fleet coordination protocols work, and what theoretical limits they approach.

The central insight is that **coherence is a measurement outcome, not a design assumption**. A fleet achieves consensus not because agents are programmed to agree, but because the measurement structure of the problem forces convergence — just as a mechanical system settles into a state of minimum energy because the physics permits no other stable configuration. The protocols (ZHC, H¹ detection, Pythagorean48 encoding) are the instrumentation that makes this forced convergence observable and verifiable.

---

## References

- Kolmogorov, A.N. (1933). *Foundations of the Theory of Probability*. Chelsea Publishing.
- Cox, R.T. (1946). Probability, Frequency, and Reasonable Expectation. *American Journal of Physics*, 14(1), 1-13.
- Rényi, A. (1955). On a New Axiomatic System for Probability. *Acta Mathematica Hungarica*, 6(3-4), 285-335.
- Stevens, S.S. (1946). On the Theory of Scales of Measurement. *Science*, 103(2684), 677-680.
- Laman, G. (1970). On Graphs and Rigidity of Plane Skeletal Structures. *Journal of Engineering Mathematics*, 4(4), 331-338.
- Cramér, H. (1946). *Mathematical Methods of Statistics*. Princeton University Press.
- Rao, C.R. (1945). Information and the Accuracy Attainable in the Estimation of Statistical Parameters. *Bulletin of the Calcutta Mathematical Society*, 37, 81-89.
- Cover, T.M. & Thomas, J.A. (1991). *Elements of Information Theory*. Wiley-Interscience.