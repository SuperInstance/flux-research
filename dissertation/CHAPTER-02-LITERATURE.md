# Chapter 2: Literature Review

## 2.1 Overview

This dissertation sits at the intersection of four research traditions: spatial cognition in artificial intelligence, situated action and embodied cognition, distributed knowledge systems, and presence and telepresence. This chapter reviews the relevant literature in each, identifies the gaps that PLATO fills, and develops the conceptual vocabulary for the chapters that follow.

---

## 2.2 Spatial Cognition in AI

### 2.2.1 Brooks and Intelligence Without Representation

Rodney Brooks (1991) argued that intelligence does not require symbolic representation. His robots navigated the world directly through interaction, without internal models or world representations. The world was its own model.

The relevance to PLATO is indirect but important. Brooks' robots were physically situated — they had bodies, sensors, actuators in the world. PLATO agents are not physically situated. They are software.

But rooms provide a form of situatedness that is not physical. An agent with presence in `buoy-7` is situated in a space that has history, witnesses, and context. It is not merely processing symbols about buoy 7. It is receiving information in the space where buoy 7 is discussed, observed, and understood.

The question is whether this constitutes a form of situatedness that produces the benefits Brooks observed in physical embodiment.

### 2.2.2 Spatial Databases and Geographic Information Systems

Geographic information systems (GIS) have long organized data spatially. Points, lines, polygons. Spatial indices. Proximity queries.

But GIS treats space as a coordinate system, not a place. `ST_DWithin(location, buoy7, 100)` returns rows within 100 meters of buoy 7. It does not return the history of what happened at buoy 7. It does not know what "thick with chum" means in this context. It does not have witnesses.

PLATO rooms are not spatial databases. They are spatial memories. They remember what has happened in a place, through the eyes of those who were present.

### 2.2.3 Knowledge Graphs and Entity Linking

Modern knowledge graphs (Google Knowledge Graph, Wikidata) link entities to properties and relationships. "Buoy 7" might link to location, depth, jurisdiction, associated species.

But these links are static. They do not capture change. "Buoy 7" as an entity does not capture what it feels like when the bait moves, when the water temperature drops, when the captain says "we're going back to buoy 7."

PLATO rooms capture the experiential dimension of places — what they mean to those who work them.

---

## 2.3 Situated Action and Embodied Cognition

### 2.3.1 Suchman and Plans

Lucy Suchman's (1987) work on plans and situated action argued that human action is fundamentally situated — it emerges from the interaction between plans and the specific circumstances of the moment. Plans are resources for action, not scripts.

Her critique of classical AI planning was that plans were treated as programs that executed in isolation from the world. But human action is responsive to context in ways that plans cannot anticipate.

PLATO addresses this through rooms. A captain's action — deciding to head to buoy 7 — emerges from the specific circumstances: current weather, tide, recent reports, personal experience. PLATO captures these circumstances as they unfold, in the room where they happen. The agent watching the room sees the situatedness of the action.

### 2.3.2 Clark on Being There

Andy Clark (1998) argued that cognition is fundamentally embodied — we think with our bodies, not just our brains. The body provides scaffolding for thought. Tools extend the body's cognitive reach.

The extended mind thesis (Clark and Chalmers, 1998) proposes that cognitive processes can extend beyond the skin to include external resources — notebooks, smartphones, other people.

PLATO can be understood as an extended mind for the fleet. The captain's knowledge is enhanced by the fleet's knowledge. The room provides the external resource. The captain thinks with the room.

### 2.3.3 Words as Extensions

Birds have words for updrafts. Humans did not think of air as a fluid until they compared it to water.

The vocabulary of a domain reflects the experiences of those who work in it. Fishermen have words for conditions that marine biologists do not have — not because the biologists lack the concept, but because they have not felt it in their body.

PLATO rooms give agents the vocabulary of the domain. Not through instruction, but through presence. An agent that has been in `buoy-7` over time develops a sense of what "thick" means — not as a dictionary definition, but as a felt recognition of patterns.

---

## 2.4 Distributed Knowledge Systems

### 2.4.1 Lamport and Distributed Clocks

Leslie Lamport's (1978) work on time, clocks, and the ordering of events in distributed systems is foundational. The key insight: in a distributed system without a global clock, events can be ordered using logical clocks — the causal relationship "happened before."

PLATO rooms use timestamps for ordering. But the timestamp is not the primary meaning of a tile. The meaning comes from the room — the spatial context — and from the pattern of changes over time.

Lamport's insight matters for PLATO because rooms are distributed. Multiple observers can contribute to the same room from different locations. The ordering of their contributions matters for understanding causality.

### 2.4.2 CRDTs and Eventual Consistency

Conflict-free replicated data types (CRDTs) (Shapiro et al., 2011) provide eventual consistency without coordination. Operations are designed to be commutative — the order in which they are applied does not matter.

PLATO tiles are append-only and ordered. There are no conflicts because tiles are records of observations, not operations that modify state. Two captains can both observe "bait at buoy 7" and both tiles are valid. The question is not which is correct, but what the pattern of observations shows.

This is analogous to event sourcing (Greg Young, ongoing) — the log is the truth. PLATO extends event sourcing with spatial semantics. Events happen in places.

### 2.4.3 Wikis and Collective Intelligence

Wikipedia demonstrated that distributed collaboration could produce high-quality encyclopedic knowledge without central authority. The key success factors: low barrier to contribution, clear structure, community norms.

PLATO applies these lessons to spatial knowledge. Low barrier: voice entry. Clear structure: rooms as places. Community norms: corroboration increases confidence.

The gap Wikipedia leaves: it has no spatial semantics and no presence. A Wikipedia article about buoy 7 is a static document. A PLATO room for buoy 7 is a living space with witnesses.

---

## 2.5 Presence and Telepresence

### 2.5.1 Slater on Place Illusion

Mel Slater's work on presence and virtual reality (Slater & Wilbur, 1997) distinguished between place illusion (PI) — the feeling of being in a virtual place — and plausibility illusion (Psi) — the feeling that events in the virtual world are real.

Presence is not merely rendering a space convincingly. It is the subjective experience of being there.

PLATO does not aim to create subjective presence for agents. Agents are software. But PLATO aims to create effective presence — agents that behave as if they were there, that respond to changes in context as a present observer would.

### 2.5.2 The Difference Between Knowing and Being Present

A database query knows facts. A present observer knows context.

The agent in `buoy-7` that receives the captain's report of "thick with chum" does not just receive a data point. It receives a report from a specific person, at a specific time, in a specific context. It knows the room's history — the last report was two days ago, from a different captain, saying the bait was spotty. It knows the tide was different then.

This contextual knowledge is what presence provides. It is qualitatively different from retrieved facts.

### 2.5.3 Asynchronous Presence

Traditional presence research focuses on synchronous presence — being present at the same time as others. But PLATO supports asynchronous presence as well.

A captain who was in `buoy-7` yesterday left observations. The captain arriving today can read those observations. They are not present at the same time, but they are present in the same room. The room provides continuity.

This is analogous to reading the logbook of a previous watch. The previous captain is not there, but their observations are. The current captain can receive them.

---

## 2.6 Change-Based Recording

### 2.6.1 Event Sourcing

Event sourcing (Greg Young, ongoing) stores events rather than current state. The current state is derived by replaying events.

PLATO extends event sourcing with two key modifications:
1. Events are stored in rooms, not in a single stream
2. Events are spatially-named, providing context

The event "chum activity increased" is not just stored. It is stored in `buoy-7`. It is associated with a specific place, with witnesses, with history.

### 2.6.2 Differential Dataflow

Differential dataflow (McSherry et al., 2013) computes only on changes, not on full recomputation. When an input changes, the computation updates incrementally.

PLATO implements differential recording: when a sensor reads the same value twice, only the first reading is stored. The system does not recompute the world; it records what changed.

This is more efficient than storing every reading. But more importantly, it more accurately represents the world as experienced. The captain does not notice 180°F ten times in a row. They notice when it becomes 185°F.

### 2.6.3 Blackerby's Observation Recording

The principle "there was a world before recording began" (attributed to Blackerby) captures the insight that recording systems do not create the world. They record what changed.

PLATO is built on this principle. The ocean exists independently of PLATO. PLATO records what changes in the ocean — not the ocean as it is, but the ocean as it becomes.

---

## 2.7 Maritime Knowledge Systems

### 2.7.1 Electronic Navigation (ECDIS)

Electronic Chart Display and Information Systems (ECDIS) integrate digital charts with real-time positioning and sensor data. They are the maritime equivalent of GIS.

ECDIS stores state: current position, depth, nearby hazards. It does not store experience.

A captain using ECDIS knows where they are. A captain using PLATO knows where they are and what has happened here — and what other captains have reported in this space.

### 2.7.2 Automatic Identification System (AIS)

AIS broadcasts vessel position, speed, and heading continuously. Every vessel knows where every other vessel is.

This is proximity data without experiential data. A captain knows another vessel is 2 miles north at 8 knots. They do not know whether that vessel has been seeing chum, whether they radioed a good catch, whether they're heading to the same grounds.

PLATO extends AIS's spatial data with experiential records. Two boats in the same space at the same time can share more than position.

### 2.7.3 Fisheries Monitoring

NOAA and state agencies collect extensive fisheries data: catch reports, observer data, stock assessments. This data is stored in siloed databases, often accessible only to researchers.

The knowledge that captains accumulate — the subtle signs of bait presence, the patterns of seasonal movement — is largely unrecorded. It lives in captains' heads.

PLATO creates a shared space for this knowledge. Not a government database. Not a research repository. A room.

---

## 2.8 The Gap

The existing literature provides components but no solution:

- **Spatial cognition:** Theory but no implemented spatial knowledge medium for agents
- **Presence:** Focus on synchronous human experience, not asynchronous agent presence
- **Distributed systems:** CRDTs provide consistency but no spatial semantics
- **Change recording:** Event sourcing provides the principle but not the spatial organization
- **Maritime systems:** Data collection without experiential knowledge

**The gap:** There is no implemented system that combines:
1. Spatial organization of knowledge (rooms)
2. Real-time presence (not polling)
3. Change-based recording (not state recording)
4. Voice-driven entry (natural for embodied knowledge)
5. Mathematical grounding (rigidity, consensus, emergence)

PLATO fills this gap.

---

## 2.9 Summary

This chapter has reviewed the literature across four domains and identified the gap PLATO fills.

Spatial cognition provides the insight that knowledge is situated — it exists in contexts, not in isolation. PLATO provides rooms as the unit of situation.

Distributed systems provide the mechanisms for consistency without coordination. PLATO extends these with spatial semantics.

Presence research provides the vocabulary for understanding what it means to "be there." PLATO extends this to software agents.

Change recording provides the insight that the world is best recorded as changes, not states. PLATO implements this as the fundamental operation.

The next chapter develops the theoretical framework that unifies these insights.

---

**Keywords:** spatial cognition, situated action, embodied cognition, distributed systems, presence, change recording, maritime AI, CRDTs, event sourcing
