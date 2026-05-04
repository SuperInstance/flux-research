# PLATO as Ether — Dissertation

**Working Title:** "PLATO Provides the Ether: Spatial Rooms as a Medium for Agent Presence and Change-Based Knowledge Recording"

**Status:** Drafting — Chapters 1-5 complete

## Core Thesis

> "PLATO provides the ether for agents to swim."

PLATO (Persistent Laminated Timed Observation) organizes knowledge spatially through rooms — named, persistent places where observations accumulate as change records. Agents develop presence in rooms, receiving information in context. The system records changes, not states.

## Chapters

| Chapter | Status | Lines |
|---------|--------|-------|
| 1. Introduction | ✅ Draft | 145 |
| 2. Literature Review | ✅ Draft | 216 |
| 3. Theoretical Framework | ✅ Draft | 259 |
| 4. PLATO Architecture | ✅ Draft | 359 |
| 5. Methodology | ✅ Draft | 270 |
| 6. Findings | 🔜 Pending | — |
| 7. Analysis | 🔜 Pending | — |
| 8. Conclusion | 🔜 Pending | — |

## Key Definitions

- **Room:** A persistent, spatially-named knowledge space with continuity and audience
- **Presence:** Real-time receipt of information in context, not polling
- **Tile:** A timestamped record of a change (not a state)
- **Ether:** The totality of rooms and change streams — the medium agents swim in
- **Delta Recording:** Only changes are stored, not continuous states

## Research Questions

1. **RQ1:** Does spatial organization through rooms improve agent performance on spatially-grounded tasks?
2. **RQ2:** Does change-based recording produce more efficient and accurate knowledge representations?
3. **RQ3:** Can agents develop effective presence in spaces through accumulated change records?
4. **RQ4:** Can fishermen with no software experience effectively use voice-driven spatial knowledge systems?

## Hypotheses

| ID | Hypothesis | Test |
|----|------------|------|
| H1 | Spatial rooms > flat database on spatially-grounded tasks | Lab study |
| H2 | Change recording > state recording for long-term accuracy | Lab study |
| H3a | 6-month agent presence shows measurable room familiarity | Field study |
| H3b | Agent response relevance increases with presence duration | Field study |
| H4a | Voice > manual for observation volume | Field study |
| H4b | Voice > manual for observation quality | Field study |
| H4c | Abandonment rate < 20% at 6 months | Field study |

## Key Insight

> "There was a world before recording began. Records are of what has changed since." — Blackerby

The world is continuous. PLATO records changes. The depth sounder shows you what's below. PLATO shows you what changed.

## Methodology Overview

**Study 1 — Lab Study (N=40 fishermen):**
- Within-subjects: spatial vs non-spatial conditions
- Simulated fishing scenario
- Measures: task performance, decision quality, cognitive load, usability

**Study 2 — Field Deployment (N=20 vessels, 6 months):**
- Longitudinal observational study
- Bering Sea fishing cooperative partnership
- Phased: baseline → agent responses → full deployment
- Measures: usage, engagement, knowledge growth, adoption

**Total timeline:** 14 months

## Key Metaphor

> "The bird does not think about air. The captain does not think about PLATO. They swim."

## Related Repos

- `SuperInstance/plato-server` — Room server implementation
- `SuperInstance/plato-voice` — Voice interface prototype
- `SuperInstance/plato-sdk` — Python SDK
- `SuperInstance/holonomy-consensus` — Mathematical foundations (constraint theory)

## Team

- **PI:** Casey Digennaro (fisherman, domain expert)
- **Co-PI:** TBD (academic collaborator with AI/robotics background)
- **Technical Lead:** Oracle1 (PLATO architecture)

## Funding Targets

- NSF Smart and Connected Communities (SCC)
- NOAA Fisheries and Oceans Canada
- DARPA PALM program

## Published Artifacts

- Future User Manual: `flux-research/whitepapers/2026-05-04-future-user-manual.md`
- Voice Prototype: `SuperInstance/plato-voice`
