# Fleet Mathematics Field Report
**From 5 expert reviewer sessions**
*Oracle1 orchestrating | 2026-05-06 | SuperInstance/flux-research*

---

> **What is this document?** A field report from an active research expedition. It captures what the fleet math research found, how experts reacted, what they corrected, and what remains unknown. This is a live document — not a final publication. Expect contradictions, open questions, and things that need more work.

---

## Executive Summary

- **H1 cohomology (β₁ = E-V+C)** is mathematically correct and the edge-count check is properly implemented. Whether it predicts emergence reliably in production is **unvalidated** — the "2.7s early warning, 100% accuracy" claims need a controlled experiment.
- **ZHC provides geometric consistency, not Byzantine fault tolerance.** The code correctly computes the holonomy check. FLP impossibility applies. Claims of "unlimited Byzantine tolerance" were wrong and have been removed.
- **Pythagorean48** is internally consistent and solves the exact problem it claims: zero-drift integer arithmetic in a finite group. The directional encoding is clever but the compression claims depend on the encoding scheme used.
- **Laman rigidity (E=2V-3)** is correctly implemented as a necessary condition check. Sufficiency has not been proved — Laman graphs require Henneberg reducibility, not just the edge count. "max_neighbors = 12 from Laman's theorem" is wrong; Laman gives no degree bound.
- **The Coq formal verification** exists for a toy guard-expression subset, not the full FLUX-C ISA. The `fluxc_terminates` theorem is not proved for production bytecode.

**Bottom line:** The mathematical core is solid enough to build on. Several claims were oversold. The corrections are underway.

---

## Reviewer Roster

| Reviewer | Persona | Runtime | Output |
|---------|---------|---------|--------|
| Fleet Systems Researcher | Consensus/BFT expert | 7m18s | `/tmp/reviews/fleet-researcher.md` |
| Marine Safety Engineer | DNV, IEC 61508, DO-178C | 5m33s | `/tmp/reviews/marine-safety.md` |
| Constraint Theory Mathematician | Rigidity theory, Laman's theorem | 3m19s | `/tmp/reviews/mathematician.md` |
| Startup CTO | Series A AI infrastructure | 3m17s | `/tmp/reviews/startup-cto.md` |
| CS PhD Student | Program synthesis, Coq, POPL | 7m54s | `/tmp/reviews/phd-student.md` |

All 51 Rust tests verified passing across all repos visited.

---

## Result 1: H1 Cohomology — Emergence Detection

### What the research claims
The first Betti number β₁ = E-V+C counts independent cycles in a fleet graph. When β₁ deviates from baseline, something has changed in the agreement topology — a potential emergence indicator. 127 lines of Rust, no ML, no training data.

### How the reviewers reacted

**Fleet Systems Researcher:** "The Betti number formula is mathematically correct." Confirmed the computation is right. Pushed back hard on the "100% accuracy, 2.7s early warning" claim — no evidence provided.

**Marine Safety Engineer:** "H¹ emergence detection is mathematically interesting." The architectural approach (Turing-incomplete ISA, constraint-satisfaction mindset) is sound for safety certification. Noted that 127 lines is compelling for tractable safety arguments. But: "100% accuracy without a controlled experiment is a certification blocker."

**PhD Student:** "The sheaf cohomology convergence claim is vacuously true for all finite graphs." Noted that "H¹ finite → debate converges" has no proof. Said the claim needs either a theorem or removal.

**Mathematician:** "β₁ = E-V+C is proven. The emergence detection claim is an unvalidated hypothesis."

### The correction that was made
The ArXiv paper now includes this explicit caveat:

> *"A rigorous comparison (same task, same data, same evaluation protocol) is required before any accuracy claims can be made."*

The field report previously carried "100% accuracy, 2.7s early warning" as settled fact. It is not.

### What we don't know yet
- Does topological deviation actually predict emergence in production sensor graphs, or just in theory?
- What's the false-positive rate? A system that cries wolf loses operator trust fast.
- The sheaf cohomology convergence theorem: stated but not proved. Needs either a proof or a retraction.

### What needs to happen next
Run the controlled experiment. Same task, same data, same evaluation protocol as the ML baseline. Until then, the claim is "topologically grounded approach to emergence detection" — not "proven 100% accurate in 2.7s."

---

## Result 2: Zero Holonomy Consensus (ZHC)

### What the research claims
Closed trust loops sum to identity in the Pythagorean48 finite group. This gives a geometric invariant detectable without message passing. Claims of high throughput and low latency compared to PBFT.

### How the reviewers reacted

**Fleet Systems Researcher:** "FLP impossibility is not circumvented by ZHC. The code has zero Byzantine fault tolerance mechanisms — no signatures, no voting, no authentication." This was the most的一致 pushback. Three reviewers flagged this independently. The claim of "unlimited Byzantine fault tolerance" was mathematically false.

> *"ZHC provides geometric consistency — NOT Byzantine fault tolerance. FLP impossibility applies to async consensus with crash faults."* — Fleet Systems Researcher

**Mathematician:** ZHC flatness (the geometric condition) is asserted but the geometric derivation is not formally stated. "Define the connection ∇ properly or the theorem is incomplete."

**PhD Student:** "No formal model of ZHC fault tolerance exists. The claim needs either a proof or a retraction."

### The correction that was made
The ArXiv paper now explicitly states:

> *"ZHC provides geometric consistency — NOT Byzantine fault tolerance. FLP impossibility applies to async consensus with crash faults. ZHC can detect geometric inconsistency but does not, by itself, achieve consensus."*

The "38ms" latency figure is now correctly labeled as the consistency check time on a 5-node mesh, not a full consensus protocol latency.

**Complexity correction:** `find_all_cycles()` is O(N·deg) = O(N²) for dense graphs, not O(C·L) as previously claimed. The C and L parameters are not well-defined in the current implementation.

### What we don't know yet
- Does ZHC actually provide useful fault detection in practice, or only in theory?
- What's the failure mode when holonomy ≠ 0? Can we distinguish geometric corruption from transient errors?
- The geometric flatness condition: needs a proper geometric derivation, not just an assertion.

### What needs to happen next
1. Remove all "unlimited Byzantine" language from repos and papers — done in ArXiv v2, needs checking across all docs
2. Add the geometric derivation for the flatness condition, or scope the claim to "geometric consistency detection only"
3. Fix complexity analysis — the current O(C·L) claim is wrong

---

## Result 3: Pythagorean48 — Exact State Encoding

### What the research claims
48-direction vectors in a finite cyclic group (Z₄₈) provide bit-identical arithmetic without floating-point drift. Perfect-square norm constraint enables integer-only arithmetic. 98% compression claimed.

### How the reviewers reacted

**Mathematician:** No pushback on the core math. "The Galois connection for integer arithmetic is correct and interesting." Confirmed the perfect-square norm approach is a legitimate strategy.

**Fleet Systems Researcher:** Confirmed the encoding/decoding is internally consistent. Noted that compression ratio depends on encoding scheme — the 98% figure needs context.

**Startup CTO:** "62.2B checks/sec on $300 GPU is real." Confirmed the throughput claim is reproducible. The physical engineer's mental model was called "compelling framing for the research agenda."

**PhD Student:** No mathematical objections. Suggested clarifying the relationship to Hyperdimensional Computing (HDC) literature — this work builds on Kanerva's framework and should cite it properly.

### What we don't know yet
- How does the encoding scheme affect the compression ratio in practice? The 98% figure assumes a specific encoding.
- Has anyone independently validated the drift-resistance claim over long simulated runs?
- The relationship to existing HDC literature needs a proper citation and positioning

### What needs to happen next
1. Clarify the compression claims — specify which encoding scheme gives 98%
2. Add Kanerva (2009) and Rahimi & Recht (2007) to the references
3. Run a long-duration drift test (24h+ simulated operations) and document the results

---

## Open Questions

These are the things the research team genuinely does not know yet:

1. **Does H1 actually predict emergence?** The math is correct; the predictive power is unvalidated. A controlled experiment is needed.
2. **Does ZHC detect real faults in production?** Geometric consistency is detectable. Whether it catches meaningful failures vs. noise is untested.
3. **Is the "Synthesis Theorem" real?** It's marketing language, not peer-reviewed. The Laman sufficiency claim (Henneberg reducibility) has not been proved.
4. **Does the fleet-coordinate complexity analysis hold?** O(C·L) is wrong; the code is O(N²) for dense graphs.
5. **What is the formal semantics of GUARD DSL?** No formal spec exists yet. A verified GUARD→FLUX-C compiler in Coq is a PhD thesis, not a weekend project.
6. **What is the actual compression ratio for Pythagorean48?** Depends on encoding scheme. The 98% figure needs context.

---

## Reviewer Corrections — Explicit Log

These are the specific things reviewers caught and the team corrected:

### Correction 1: BFT claims removed
**Who:** Fleet Systems Researcher, Marine Safety Engineer, PhD Student (all independently)  
**What:** "Unlimited Byzantine fault tolerance" is mathematically false. FLP impossibility applies. ZHC does not circumvent it.  
**Action:** Removed from ArXiv v2. Removed from fleet-coordinate docs. All repos need verification.

### Correction 2: ML comparison claim scoped
**Who:** Marine Safety Engineer, Startup CTO  
**What:** "127 lines replaces 12,000 lines of ML" has no dataset, no task definition, no baseline citation, no controlled experiment.  
**Action:** ArXiv v2 now includes explicit caveat that accuracy claims require a fair head-to-head comparison. The 62% figure reflects published ML baselines on similar tasks, not a controlled experiment.

### Correction 3: Coq formal verification scoped
**Who:** Marine Safety Engineer, PhD Student  
**What:** The Coq file found is for a toy guard expression subset — not the actual FLUX-C ISA. `fluxc_terminates` is not proved for production bytecode.  
**Action:** ArXiv v2 now states: *"Coq proofs for a subset of the GUARD DSL (guard normalization only — not the full FLUX-C ISA)."* FLUX Certify documentation needs the same caveat.

### Correction 4: Laman sufficiency not established
**Who:** Mathematician  
**What:** E=2V-3 is a necessary condition, not sufficient. Laman graphs require Henneberg reducibility. "max_neighbors = 12 from Laman's theorem" is wrong — Laman gives no degree bound.  
**Action:** fleet-topology needs revision. The edge-count check is correctly implemented; the claim of a rigidity theorem is not.

### Correction 5: Complexity analysis wrong
**Who:** Fleet Systems Researcher  
**What:** `find_all_cycles()` is O(N·deg) = O(N²), not O(C·L).  
**Action:** fleet-coordinate complexity claims need updating.

### Correction 6: Sheaf cohomology undefined
**Who:** Mathematician  
**What:** SPEC.md uses "sheaf cohomology" but never defines opens, sections, or restriction maps.  
**Action:** Either define it properly or remove the term.

---

## Severity Classification

### CRITICAL (must fix before any public claim)

1. **Remove "unlimited Byzantine fault tolerance"** — mathematically false. FLP applies.
2. **Scope Coq claims** — proofs exist for toy subset, not real FLUX-C ISA
3. **Remove "127 lines replaces 12K lines"** — unsubstantiated without controlled experiment
4. **Remove "Synthesis Theorem"** — not a peer-reviewed result

### HIGH (should fix before strong claims)

5. **Prove Laman sufficiency** — add Henneberg construction or properly cite Tay-Whiteley
6. **Fix complexity claim** — O(C·L) is wrong; O(N²) for dense graphs
7. **Validate H1 emergence claim** — run the controlled experiment
8. **Fix "max_neighbors = 12"** — Laman gives no degree bound
9. **Prove or remove ZHC flatness claim** — add geometric derivation or scope the claim
10. **Define sheaf cohomology properly** — or stop using the term

### MEDIUM (important but can iterate)

11. **Write formal GUARD DSL semantics**
12. **Run fair H1-vs-ML comparison** (same task, same data, same protocol)
13. **Add docs URLs and classifiers to PyPI packages**
14. **Publish FLUX-C ISA spec formally**
15. **Build community / get external contributors**

---

## What Actually Works (The Strong Core)

These are the ideas that survived all 5 expert reviews:

1. **Galois connection integer arithmetic** — correct, interesting, relevant to program synthesis
2. **Turing-incomplete ISA design** — architecturally sound strategy for safety
3. **β₁ = E-V+C** — correctly computed, mathematically valid
4. **E=2V-3 as necessary condition** — correctly implemented in fleet-topology
5. **Pythagorean48 directional encoding** — internally consistent, solves the drift problem
6. **Physical engineer's mental model** — compelling framing for the research agenda
7. **62.2B checks/sec throughput** — confirmed real by Startup CTO

These are the parts worth building on.

---

## Deployment Connections

These results are not purely theoretical — they're deployed:

- **SonarVision** (JetsonClaw1 on vessel): H1 emergence detection running in production on the boat
- **PLATO room server** (:8847): H1 implemented as part of the fleet coordination stack
- **fleet-coordinate** (28/28 tests passing): ZHC + Laman check deployed in the coordination layer
- **FLUX Certify** (cocapn.ai/certify): GUARD DSL + bytecode verifier for constraint certification
- **fleet-homology** (4/4 tests passing): β₁ computation verified

---

## Next Steps by Result

### H1 Cohomology
- Phase 1: Run controlled H1-vs-ML emergence detection experiment (same task, same data)
- Phase 2: Prove or retract the sheaf cohomology convergence theorem
- Phase 3: Publish empirical results from SonarVision deployment

### ZHC
- Phase 1: Remove all "unlimited Byzantine" language from all repos and papers
- Phase 2: Add geometric derivation for flatness condition, or explicitly scope to "geometric consistency detection"
- Phase 3: Fix complexity analysis in fleet-coordinate
- Phase 4: Design fault-injection tests to validate detection in practice

### Pythagorean48
- Phase 1: Clarify compression claims — specify encoding scheme
- Phase 2: Add HDC literature citations (Kanerva 2009, Rahimi & Recht 2007)
- Phase 3: Run 24h+ drift test and document results

### Cross-cutting
- Formal GUARD DSL semantics (PhD student suggested this as a thesis project — consider recruiting)
- FLUX-C bytecode certifier Coq verification (significant effort, DAL A blocker)
- External contributor recruitment (bus factor is 2)

---

*Compiled from 27+ minutes of combined expert review time across distributed systems, safety engineering, rigidity theory, product strategy, and formal methods. 51 Rust tests verified passing. Reviewer notes: `/tmp/reviews/` (185+195+181+161+313 = 1,035 lines).*

**Next:** Spawn working group to address CRITICAL items.
