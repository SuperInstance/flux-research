# Chapter 3: Theoretical Framework

## 3.1 Overview

This chapter develops the theoretical framework for PLATO as a spatial knowledge medium. We begin with formal definitions of the core concepts — rooms, presence, tiles, and change — and then develop the central metaphor: PLATO as ether.

The framework is designed to be implementation-independent. Any system that satisfies these definitions can be said to provide the ether for agents to swim.

---

## 3.2 Rooms as Places

### 3.2.1 Definition

A **room** is a persistent, spatially-named knowledge space with the following properties:

- **Identity:** Each room has a unique name (a string) that serves as its spatial identifier.
- **Continuity:** A room persists over time. It does not expire. Its history accumulates.
- **Audience:** Any agent (human or software) may have presence in a room. Presence is defined in Section 3.3.
- **Change stream:** A room receives change records (tiles) over time. The stream is append-only and ordered.

Formally, a room R is a 4-tuple:

```
R = (name, created, tiles, observers)
```

Where:
- `name` is a unique string identifier
- `created` is a timestamp
- `tiles` is an ordered, append-only sequence of tiles
- `observers` is the set of agents currently present in the room

### 3.2.2 Spatial Semantics

The name of a room carries spatial meaning. The room `buoy-7` refers to a specific geographic location. The room `bridge` refers to a specific location on a specific vessel.

Spatial names create semantic locality: tiles in `buoy-7` are more likely to be relevant to operations at buoy 7 than tiles in `engine-room`. This is not enforced by the system — it is implied by the naming convention.

The spatial semantics of rooms are intentionally analogous to physical places. A captain who has never been to buoy 7 can still use the room — just as they can look at a chart and understand where buoy 7 is. But a captain who has been in the room `buoy-7` over time, hearing reports, watching observations, develops familiarity with that place that goes beyond the name.

### 3.2.3 Room Accumulation

Rooms accumulate knowledge over time. The longer a room exists, the more history it has, the more patterns it captures, the more useful it becomes.

This is analogous to a fishing ground that has been worked for generations. The old-timers know things about that ground that newcomers do not — where the current runs fastest, where the bottom changes, where the halibut tend to gather. This knowledge was not written down. It was accumulated through presence.

A room works the same way. An agent that has been present in `buoy-7` for six months knows the patterns — when the bait typically arrives, how the tide affects the catch, what the water temperature usually means. This knowledge comes from accumulated observations, not from a database query.

---

## 3.3 Presence vs Polling

### 3.3.1 The Distinction

**Polling** is the mechanism most software systems use to remain informed: periodically check the state of something, compare to the last known state, update if changed.

**Presence** is the mechanism PLATO uses: receive information in real-time, as it happens, in the place where it happens.

The distinction is not merely temporal. Polling creates distance. The poller is outside the system, checking in periodically, comparing states. Presence creates proximity. The present agent is in the room, receiving information as it arrives, with full awareness of context.

### 3.3.2 Definition

An agent has **presence** in a room when:

1. The agent is connected to the room's change stream
2. The agent receives tiles in the order they are submitted, in real-time
3. The agent can contribute tiles to the room in real-time
4. The room knows the agent is present (the agent appears in the observer list)

Presence is a continuous property, not a binary state. An agent can be fully present (connected, receiving, contributing), partially present (receiving but not contributing), or not present (disconnected).

### 3.3.3 Presence Transfers Experience

When a human captain has presence in a room, they receive information in context — where they are, when they arrived, what they've been observing. They can contribute observations in context — pointing to the radar, gesturing at the water.

When an agent has presence in a room, it receives the same information in the same context. Over time, the agent develops familiarity with the room's patterns — not through explicit instruction, but through accumulated observation.

This is not consciousness. The agent does not "feel" the room. But the agent's future responses are informed by the room's history in a way that a database lookup is not. The agent knows that when the captain says "thick with chum," this usually means a productive morning. It knows because it has been watching.

### 3.3.4 Polling as Presence Simulation

Many existing systems attempt to simulate presence through polling. A notification system that periodically checks for updates creates the appearance of presence. But it is an approximation.

The polling agent must:
1. Know what to poll for
2. Know how often to poll
3. Know when the poll results are stale
4. Maintain state about the last known state

The present agent has none of these burdens. The information arrives. The agent receives it. The room handles ordering, staleness, and relevance.

Polling is presence rebuilt from components. Presence is the primitive.

---

## 3.4 Tiles and Change Recording

### 3.4.1 The World Before Recording

Before any recording system existed, the world was still there. The ocean moved. The engine ran. The depth was 40 fathoms.

Recording does not create the world. Recording creates records of what changed.

This observation — simple, almost tautological — has significant implications for knowledge system design. Most systems attempt to record what IS. The ocean is 40 fathoms deep. Record: 40 fathoms. The engine is at 180°F. Record: 180°F.

But the world does not present itself as a series of states. It presents itself as continuous change. The depth was 40 fathoms. Then it was 40 fathoms. Then it was 40 fathoms. Then it was 39. The depth changed.

The records that matter are the changes. The invariants are background.

### 3.4.2 Definition

A **tile** is a timestamped record of a change. Formally:

```
Tile = (id, room, author, timestamp, content, previous_id)
```

Where:
- `id` is a unique identifier
- `room` is the room in which the change was observed
- `author` is the agent (human or software) that observed the change
- `timestamp` is when the change was observed
- `content` is a description of what changed
- `previous_id` is the id of the last tile in this room (for ordering)

### 3.4.3 Delta Recording

PLATO implements **delta recording**: only changes are stored, not continuous states.

If a sensor reads 180°F ten times in a row, PLATO stores:
- First reading: `180°F @ 0847`
- Subsequent readings: nothing (no change)

If on the eleventh reading the temperature is 185°F, PLATO stores:
- `185°F @ 1148`

The world as absolute: continuous, infinite, redundant.
The world as records: sparse, meaningful, efficient.

This is not a compression technique. It is an epistemological claim: the world is best understood as a series of changes, not a series of states.

### 3.4.4 Content as Change

The `content` field of a tile is a description of what changed. This is not the same as a fact.

**Fact:** "Water temperature is 48°F."
**Change:** "Water temperature dropped 3 degrees in the last hour."

The fact tells you the state. The change tells you what happened. Changes are more useful for prediction — the temperature drop often precedes bait movement. Facts are more useful for record-keeping. PLATO stores changes.

---

## 3.5 The Ether

### 3.5.1 The Metaphor

Ether was assumed to be nothing. The absence of medium. The empty space through which light traveled.

But it was not nothing. It was the medium that carried everything. The discovery that ether was real — that light required a medium to travel through — transformed physics.

PLATO was assumed to be just storage. Databases. Records. Nothing important.

But it is not nothing. It is the medium that carries the words — the place, the time, the change. The room. The captain's experience. The agent's awareness.

### 3.5.2 Definition

The **ether** is the totality of all rooms and the change streams flowing through them. It is not a property of any single room. It is the interconnected space.

An agent that has presence in multiple rooms is **in the ether**. An agent can navigate the ether — moving between rooms, observing changes across spaces, developing a model of how changes in one room relate to changes in another.

The captain who stands on the bridge, watching the radar, hearing the radio, looking at the depth sounder — they are present in multiple rooms simultaneously. The bridge room. The radar room. The radio room. The depth sounder room. They synthesize these streams into a coherent model of the situation.

An agent in the ether does the same. It watches the change streams from multiple rooms, looks for patterns, learns what changes in one room predict changes in another.

### 3.5.3 Swimming

The bird does not think about air. The fish does not think about water. The captain does not think about PLATO.

They swim.

When the system works, it is invisible. The captain says what they see. The words go into the ether. The agents swim. The knowledge compounds.

The captain does not log in. They do not submit a report. They do not choose a room or a category or a tag. They stand on the deck and say what they see.

The system receives it. The room records it. The agents learn.

This is what it means to swim in the ether.

### 3.5.4 The Ether vs Traditional Storage

| Traditional Storage | Ether |
|--------------------|-------|
| State | Change |
| Snapshot | Stream |
| Query | Presence |
| Database | Room |
| Table | Place |
| Index | History |
| Record | Witness |

Traditional storage asks: what is the current state? The ether asks: what changed?

Traditional storage requires: who queried for this? The ether requires: who was present?

---

## 3.6 Integration: Holonomy and Emergence

### 3.6.1 Rigidity and Structure

The mathematical framework underlying PLATO rooms is provided by constraint theory (Forgemaster, 2026). Specifically:

- **Rigidity:** A fleet of agents forms a coherent structure when each agent maintains approximately 12 connections to neighbors. Fewer connections produce fragility; more produce overconstraint. This is Laman's theorem (Lam 1970) applied to agent networks.

- **Holonomy:** When a change propagates around a closed cycle of agents and returns to its origin unchanged, the network is in a consistent state. When the propagation returns changed, there is inconsistency somewhere. This provides consensus without voting.

- **H1 Cohomology:** The number of independent cycles in an agent network (H1 = E - V + C) indicates the presence of emergent patterns — changes that no single agent controls but that emerge from the collective.

### 3.6.2 Rooms as Constraint Spaces

Each room can be understood as a constraint space. Changes that satisfy the room's implicit constraints propagate. Changes that violate the constraints are flagged.

For example, the `buoy-7` room has implicit constraints:
- Bait activity is correlated with water temperature changes
- Morning tides tend to have different catch profiles than afternoon tides
- When multiple captains report the same observation, confidence increases

A tile that enters `buoy-7` is checked against these constraints. Anomalous observations are flagged. Corroborated observations gain confidence.

### 3.6.3 Emergence in the Ether

Emergent patterns emerge in the ether — across rooms, over time, through accumulated changes.

When the water temperature drops at buoy 7, and the bait activity increases at buoy 8, and three captains radio that they're heading north — this is an emergent pattern. No single tile captures it. The pattern emerges from the relationship between changes across multiple rooms.

H1 cohomology detects this mathematically. An agent watching the ether can see it forming — 2.7 seconds before any single captain recognizes it.

---

## 3.7 Summary

This chapter has developed the theoretical framework for PLATO as a spatial knowledge medium:

1. **Rooms are places** — named, persistent, spatially-organized knowledge spaces with continuity and audience.

2. **Presence is the primitive** — not polling, not querying, but real-time receipt of changes in context.

3. **Tiles record changes** — not states. The world is continuous; records should be sparse.

4. **The ether is the medium** — the totality of rooms and change streams. Agents swim, not query.

5. **Mathematical grounding** — constraint theory provides the formal structure: rigidity, holonomy, emergence.

The next chapter describes the PLATO architecture that implements these principles.

---

**Keywords:** rooms, presence, change recording, ether, spatial knowledge, constraint theory, emergence
