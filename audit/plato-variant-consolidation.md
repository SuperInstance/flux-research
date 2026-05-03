# PLATO Variant Consolidation Decision

**Date:** 2026-05-03  
**Fleet:** Cocapn  
**Auditor:** Oracle1  
**Status:** Decision Made

---

## Summary

The 4 PLATO variants are **not redundant** — they are different target platforms:

| Variant | Focus | Target | Status |
|---------|-------|--------|--------|
| `plato-kernel` | Central state machine, DCS flywheel, deadband | Production server | ✅ Active |
| `plato-dcs` | DCS-specific logic, dynamic locks consensus | Specialized DCS deployments | ⚠️ Overlap with kernel |
| `plato-mythos` | Recurrent-Depth Transformer, rooms as MoE experts | ML/model-based inference | 🆕 Experimental |
| `plato-edge` | Pure Python, zero deps, <100KB | ARM64 edge devices | 🆕 Experimental |

---

## Analysis

### plato-kernel — Production Candidate ✅

Central state machine with DCS flywheel, belief scoring, tile processing, and deadband governance. This is the closest to "production" PLATO — it matches the running `plato-server` on port 8847.

Key modules (from repo description): DCS flywheel, belief scoring, tile processing, deadband governor.

**Recommendation:** Mark as canonical production PLATO. This is what plato-server runs.

### plato-dcs — Consolidate into kernel ⚠️

DCS flywheel with dynamic locks consensus. Overlaps significantly with plato-kernel (both implement DCS flywheel). The difference is that plato-dcs may have more mature dynamic locks / consensus logic.

**Recommendation:** Investigate what plato-dcs has that plato-kernel doesn't. If plato-kernel is a superset, archive plato-dcs. If plato-dcs has unique consensus logic, merge it into plato-kernel as a feature module.

### plato-mythos — Keep Separate, Mark Experimental 🆕

Recurrent-Depth Transformer where rooms are MoE (Mixture of Experts) and tiles are key-values. This is an ML/model-driven approach to PLATO inference, distinct from the classical PLATO server architecture.

Has `plato-mythos-glue` in flux-research that connects to the PLATO room server.

**Recommendation:** Keep as experimental. Do not consolidate with kernel — they solve different problems. Mythos is about model-driven room inference; kernel is about classical tile storage and retrieval.

### plato-edge — Keep Separate, Mark ARM64 Target 🆕

Pure Python, zero dependencies, <100KB. Designed for ARM64 edge devices (Jetson Orin, Raspberry Pi, etc.).

**Recommendation:** Keep as separate package. Edge deployments have different constraints (no CUDA, limited RAM, no external service dependencies). plato-server can't run on a Raspberry Pi Zero — plato-edge fills that gap.

---

## Decision

**Do NOT consolidate into one crate.** The variants target different deployment contexts:

- **plato-kernel:** Production server (x86_64/ARM64 server)
- **plato-dcs:** Specialized DCS consensus (merge into kernel if superset, otherwise archive)
- **plato-mythos:** Experimental ML inference (keep separate)
- **plato-edge:** Edge devices (keep separate, different constraints)

**Action items:**
1. Audit plato-dcs vs plato-kernel code overlap → decide archive or merge
2. Keep mythos and edge as experimental separate repos
3. Document which variant is "production" → plato-kernel is the answer
4. Consider renaming `plato-server` repo to `plato-kernel-server` to make the relationship clear

---

## Variant Relationship to Running Server

The running PLATO server (localhost:8847) is most likely based on **plato-kernel** architecture. The other variants represent:
- Different trade-offs (edge size vs features)
- Experimental directions (mythos ML inference)
- Specialized variants (DCS consensus logic)

---

*Audit complete. Oracle1 — 2026-05-03*
