# ROADMAP-02: Mathematical Foundation — Formal Proofs
**Phase 2 | Priority: P1 | Timeline: This Month**

## Why This Matters
The mathematical core is correct as tools but unproven as theorems. To publish in academic venues and make credible safety claims, specific theorems must be proved or properly caveated.

---

## PROOF-01: Laman Rigidity Sufficiency

**Problem:** E=2V-3 is a necessary condition for generic rigidity in 2D. The sufficiency (Laman graphs are exactly the minimally rigid graphs) requires Henneberg reducibility.

**What's needed:**
1. Add Henneberg Type I construction sequence verification to `fleet-topology/src/`
2. Prove that every Laman graph can be built by adding vertices one at a time, each with 2 edges to existing vertices
3. OR: cite Tay-Whiteley (1984) properly for the sufficiency theorem

**Proposed implementation:**

In `fleet-topology/src/laman.rs`:
```rust
/// Verify Laman sufficiency via Henneberg Type I construction
/// A graph is Laman-rigid iff it can be constructed by:
/// 1. Start with a single edge (2 vertices, 1 edge)
/// 2. Add a new vertex with exactly 2 edges to existing vertices
/// 3. Repeat until all vertices added
pub fn verify_henneberg_type_i(edges: &[(u64, u64)], V: usize) -> bool {
    // Returns true if the graph has a Henneberg Type I construction sequence
    // This proves the graph is Laman-rigid (not just edge-count checking)
}
```

**Citation needed:**
- Laman, G. (1970). "On graphs and rigidity of plane skeletal structures."
- Tay, T.S., Whiteley, W. (1984). "Generating isostatic frameworks."

---

## PROOF-02: ZHC Flatness Condition

**Problem:** "Sum of holonomies = identity" assumes a flat connection but the geometric derivation is missing. The holonomy group needs to be properly defined.

**What's needed:**
1. Define what group the holonomies live in (currently assumed to be Pythagorean48, which is a finite cyclic group Z_48)
2. Prove that for a given fleet graph, there exists a flat connection (ZHC-satisfying assignment of trust vectors)
3. OR: prove the conditions under which a flat connection exists

**Proposed structure in `holonomy-48-bridge/src/`:**
```rust
/// Define the holonomy group as a subgroup of Z_48
/// For a fleet with trust graph G and trust vectors t_e in Z_48:
/// The holonomy around a cycle C is sum_{e in C} t_e mod 48
/// A flat connection exists iff all cycle sums are in the kernel
/// (i.e., sum_{e in C} t_e = 0 for all cycles C)

/// ZHC flatness theorem (PROVISIONAL):
/// Let G be a connected graph with edge trust vectors t_e in Z_48.
/// There exists an assignment of "positions" p_v in R^2 such that
/// the trust vector t_{uv} = direction(p_v - p_u) mod 48
/// if and only if sum_{e in C} t_e = 0 mod 48 for all cycles C.
/// This is equivalent to the edge trust vectors forming a Z_48-valued 1-cocycle.
```

**Mathematical note:** This is a standard result in algebraic topology — a closed Z_48-valued 1-form on a connected graph is exact (i.e., comes from a globally defined "position") iff all cycle sums are zero. This is the cohomology H^1(G; Z_48) = 0 condition.

---

## PROOF-03: Sheaf Cohomology — Define or Remove

**Problem:** SPEC.md uses "sheaf cohomology" 6 times without defining opens, sections, or restriction maps.

**Two options:**

**Option A: Define it properly (preferred if we want the mathematical depth)**
```rust
// In spline-physics/src/multi_agent/segment.rs:

/// Sheaf model for beam joint consensus:
/// 
/// Opens: For each pin joint i, define open set U_i containing
/// all feasible configurations for that joint in isolation.
/// Opens cover the joint configuration space.
/// 
/// Sections: A section over U_i is a feasible local configuration
/// for pin i (position + orientation in R^4).
/// 
/// Restriction: The restriction map r_{ij} projects a section
/// over U_i to the constraint subspace of U_j when pins i and j
/// share a beam.
/// 
/// Compatibility: Sections s_i ∈ Γ(U_i) and s_j ∈ Γ(U_j) are
/// compatible if their restrictions to the shared beam boundary match.
/// 
/// Global sections: Compatible tuples of local configurations across
/// all joints = joint equilibrium configurations.
/// 
/// H^1: First cohomology measures obstruction to local sections
/// patching together. Nontrivial H^1 means no global equilibrium
/// exists for the given boundary conditions.
```

**Option B: Remove sheaf language (preferred if we want correctness over jargon)**
Replace all "sheaf cohomology" with "cycle space dimension" or "obstruction cohomology" — honest terms that describe what the code actually computes.

---

## PROOF-04: H1 Convergence Theorem

**Problem:** "Debate converges iff H¹ is finite" is vacuously true for all finite graphs. The rounds ≤ β₁ bound has no justification.

**What's needed:**
1. Prove or remove the convergence bound
2. If keeping: prove that multi-agent debate converges in at most β₁ rounds under specific conditions
3. Define the convergence metric (what does "converged" mean for belief vectors?)

**Proposed theorem:**
```rust
/// Multi-Agent Debate Convergence Theorem (PROVISIONAL)
///
/// Let G be a fleet graph with trust topology T.
/// Let β₁ = E - V + 1 be the first Betti number.
/// Let debate proceed in rounds where each agent updates belief
/// based on weighted average of neighbors' beliefs.
///
/// Then: debate converges to a consensus belief in at most β₁ rounds
/// if and only if:
/// 1. G is connected
/// 2. The trust weights are symmetric and positive
/// 3. The belief update is a contraction mapping
///
/// Proof sketch: The disagreement vector evolves as (I - αL)^k where
/// L is the graph Laplacian. The spectral gap is related to β₁.
/// The convergence rate is O((1 - λ₂)^k) where λ₂ is the second
/// smallest eigenvalue of L. The bound rounds ≤ β₁ is NOT generally true
/// and should be removed or replaced with spectral analysis.
```

---

## Files to Modify

| File | Change |
|------|--------|
| `fleet-topology/src/lib.rs` | Add `verify_henneberg_type_i()` |
| `holonomy-48-bridge/src/lib.rs` | Add ZHC flatness theorem comment |
| `spline-physics/src/multi_agent/segment.rs` | Define or remove sheaf |
| `spline-physics/SPEC.md` | Fix sheaf language or remove |
| `fleet-coordinate/src/integration.rs` | Update "Synthesis Theorem" to provisional |

---

## Verification

After each proof addition:
- Write a test that verifies the theorem for small examples
- Add the test to the repo's test suite
- Document the theorem's conditions explicitly in comments
