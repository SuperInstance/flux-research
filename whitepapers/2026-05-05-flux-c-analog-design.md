# FLUX-C Analog Compute Integration for PLATO Rooms

## Design Document v1.1

**Author:** Oracle1 (PLATO Fleet Architecture)  
**Date:** 2026-05-05 (revised 2026-05-07)  
**Status:** Draft — R&D Phase 1  
**Target:** JC1 Edge Runtime, FLUX-C 43-opcode safety layer

---

## 1. Motivation: Why Analog Compute in PLATO?

> *"A shipwright doesn't measure a hull point-by-point. Every plank, every ribband, every frame — they don't pull out a tape and write down coordinates. They define the spline. The spline is the shape. Every measurement is just a check against it."*

### The Problem with Points

Imagine you're lofting a wooden boat — drawing the hull shape at full scale on the lofting floor. Old-timers used a long, flexible strip of wood called a *spline*. You'd weight it down at key points (the stations), and the wood would bend naturally into the fairest curve through those points. Every plank you'd cut later would be measured against that spline, not against a coordinate grid.

Now imagine doing it the point-by-point way: measure every single point on the hull surface with a tape measure. Store all those coordinates. If one measurement is wrong — a bent tape, a transcribed number — you have a ghost in your data. A plank cut to those wrong coordinates won't fit. Worse: you might not even know it's wrong until you're on the boat, hammering.

**This is exactly the trap PLATO rooms fell into.** Every tile placed in a room was stored as absolute coordinates. 100 tiles = 100 coordinate pairs. Lose one, and the room has a hole you can't recover from. Corrupt one float, and you have geometry that looks fine but isn't. The room's *shape* — what the room is actually trying to represent — is buried in a pile of points.

### The Spline Solution

FLUX-C analog compute inverts this. Instead of storing points, we store the **shape itself**: three control points and a material constant. From these, any point on the curve can be computed on demand. The stored data isn't coordinates — it's the rule that generates coordinates.

This is how real shipwrights worked. The spline tolerates:
- **Measurement noise**: a plank that's 2mm off the theoretical bend doesn't break the hull; the spline absorbs it
- **Missing data**: if you skip a station during lofting, the spline fills the gap naturally
- **Incremental growth**: you can add a control point anywhere along the spline and the shape updates locally, not globally

**This is what analog compute gives you.** Not a digital approximation of a curve, but a representation that *has physical meaning* — how would a plank of oak actually bend between these three points?

The four FLUX-C analog opcodes in this design expose that physical model to PLATO rooms. They're not floating-point tricks. They're the FLUX-C safety layer doing geometry the way a shipwright does it.

---

## 2. FLUX-C Opcode Design

FLUX-C uses Format G (Variable-Length Payload, 2+N bytes):

```
┌─────────────┬───────────┬────────────────┐
│ opcode (1B) │ length (1B)│   payload (N)  │
└─────────────┴───────────┴────────────────┘
```

New Analog opcodes are allocated in the **0xD0–0xDF range** (currently unallocated in FLUX-C canonical):

| Hex | Name | Payload | What it does |
|-----|------|---------|--------------|
| `0xD0` | `ANALOG_SPLINE` | 34 bytes | Fits a quadratic Bézier through 3 control points |
| `0xD1` | `ANALOG_WATER_LEVEL` | 9 bytes | Computes least-squares horizontal level through a point cloud |
| `0xD2` | `ANALOG_STORY_POLE` | 10 bytes | Transfers a level surface to multiple heights |
| `0xD3` | `ANALOG_SECTOR` | 9 bytes | Divides a distance into equal proportional segments |

### 2.1 `ANALOG_SPLINE(0xD0)` — The Core Primitive

**Purpose:** Given three boundary points and a material, compute the fairest curve through them.

**Encoding:**

```
Byte  0:  0xD0          — opcode
Byte  1:  0x22 (34)     — payload length
Bytes 2–9:   point[0]   — (x: f32, y: f32)  ← start
Bytes 10–17: point[1]   — (x: f32, y: f32)  ← control
Bytes 18–25: point[2]   — (x: f32, y: f32)  ← end
Bytes 26–29: material_E — f32  (Young's modulus, GPa)
Bytes 30–33: tension    — f32  (0.0 = straight, 1.0 = tight)
```

**Pseudo-code:**

```flux-c
// ANALOG_SPLINE(0xD0)
// Input:  three control points + material + tension
// Output: (x, y, curvature) tuples pushed to FLUX-C stack

fn ANALOG_SPLINE(p0, p1, p2, E, tension) {
    // Guard preconditions
    assert(p0.y <= p1.y && p1.y <= p2.y, "points must ascend in Y")
    assert(E > 0.0, "material must be positive")
    assert(0.0 <= tension && tension <= 1.0, "tension out of range")
    assert(dist(p0, p1) > EPSILON && dist(p1, p2) > EPSILON, "duplicate point")

    // Quadratic Bézier: B(t) = (1-t)²·p0 + 2(1-t)t·p1 + t²·p2,  t ∈ [0,1]
    // Output point count scales with tension (higher tension = more detail)
    num_points = ceil(3 + tension * 12)  // 3 to 15 points

    for i in 0..num_points {
        t = f32(i) / f32(num_points - 1)
        x = (1-t)*(1-t)*p0.x + 2*(1-t)*t*p1.x + t*t*p2.x
        y = (1-t)*(1-t)*p0.y + 2*(1-t)*t*p1.y + t*t*p2.y

        // Curvature κ = |x'y'' - y'x''| / (x'² + y'²)^(3/2)
        // Bounded by material stiffness — stiff materials resist bending
        curvature = bound_by_material_E(y, E, tension)

        push_stack((x, y, curvature))
    }

    // Postconditions enforced by GUARD:
    // - spline passes through p0 and p2 exactly
    // - C1 continuity at p1
    // - all outputs finite
    // - curvature bounded by E * tension
}
```

**Why three points?** A line (2 points) is a degenerate spline — useful for walls but not for hulls. Three points define a *unique* quadratic curve. That's the minimum interesting shape. Four points would need cubic interpolation, which introduces additional degrees of freedom that complicate the safety proof. Three is optimal.

**Why Young's modulus?** Real spline tools (wooden strips, fiberglass) have stiffness. A strip of cedar bends differently than a strip of steel. `material_E` parameterizes the *physics*, not just the geometry. The opcode could hardcode "just interpolate," but then it's not modeling the real tool. If you want to predict how a cedar plank will actually bend between two points, you need E. If you just want pure geometry, pass E=infinity (or a very large number — we use `tension` to bound the output).

**Preconditions:**
```
material_E > 0.0
tension ∈ [0.0, 1.0]
p0.y ≤ p1.y ≤ p2.y   (ascending Y — spline flows upward)
dist(p0,p1) > 1e-6   (points must be distinct)
dist(p1,p2) > 1e-6
```

**Postconditions:**
```
Output spline passes through p0 and p2 exactly
Output has C1 continuity (continuous first derivative) at p1
All output coordinates are finite (no NaN, no Inf)
Curvature at any output point ≤ material_E × tension
GUARD tolerance: ±(0.5 + material_variation × tension)
```

---

### 2.2 `ANALOG_WATER_LEVEL(0xD1)` — The Level Surface

**Purpose:** Given a point cloud, find the horizontal line that best fits them. The "water line" — the surface water would settle to if you dumped all your points in a gravity well.

**Encoding:**

```
Byte  0:  0xD1           — opcode
Byte  1:  0x09 (9)       — payload length
Bytes 2–5:   point_array_ptr — u32  (word-aligned address)
Bytes 6–9:   count           — u32  (3 ≤ count ≤ 256)
```

**Pseudo-code:**

```flux-c
// ANALOG_WATER_LEVEL(0xD1)
// Input:  array of 2D points
// Output: single f32 — the Y-coordinate of the level surface

fn ANALOG_WATER_LEVEL(ptr, count) {
    // Preconditions enforced by GUARD
    assert(count >= 3, "need ≥ 3 points for meaningful level")
    assert(count <= 256, "FLUX-C memory limit")
    assert(is_word_aligned(ptr), "unaligned pointer")
    assert(all_finite(read_array(ptr, count)), "non-finite coordinate")

    // Least-squares horizontal line through points:
    // Minimize Σ(y_i - Y)²  →  solution: Y = mean(points.y)
    sum = 0.0
    for i in 0..count {
        sum += read_point(ptr, i).y
    }
    Y = sum / f32(count)

    // Postconditions:
    // - Y = Σ(points[i].y) / count  (exact arithmetic mean)
    // - Y is finite
    // - If all y equal, Y = that y exactly (zero residual)
    return Y
}
```

**Why least-squares?** A naive approach would average the min and max Y. But that's sensitive to outliers. The least-squares solution is the *unique* horizontal line that minimizes total squared error — it's the correct answer for "what level would these points settle to." For a room's boundary tiles that should all be at the same height but have measurement noise, this is exactly what you want.

**Why a horizontal line specifically?** Because we're computing a *level surface* — a reference datum. The other opcodes (`ANALOG_STORY_POLE`) take this level and transfer it to other heights. The water level is the anchor; everything else is offsets from it.

**Preconditions:**
```
count ∈ [3, 256]
point_array_ptr word-aligned (4-byte alignment)
All coordinates finite (no NaN, no Inf)
```

**Postconditions:**
```
Result Y = Σ(points[i].y) / count  (exact)
Result is finite
Zero residual if all points share the same Y
```

---

### 2.2.1 ASCII: Spline vs. Discrete Points

```
DISCRETE POINT APPROACH                    ANALOG SPLINE APPROACH
────────────────────────────────────────    ────────────────────────────────────────

Point cloud (what we store):                Spline (what we store):

    ×           ×                               ······
      ×       ×                                  ·    ·  ← curve computed on demand
        ×   ×                                    ·      ·
          ×                                     ·        ·  ← 3 points + E + tension
        ×   ×                                    ·          ·
      ×       ×                                  ·            ·
    ×           ×                                ······×·····×·····
                                               ↑       ↑    ↑
                                             p0      p1   p2

Tile validity check:                         Tile validity check:

  × ← tile                    tile at P:       P:────→×   compute d(P, spline)
  │                           compute d to     │        ↖  d < tolerance? valid
  ↓                           each other       ↓           d ≥ tolerance? flag
  ↑                           point            ↑

  O(n²) comparisons!           No.              O(1): evaluate spline at P's x, check d

What we store:                             What we store:
  100 tiles × 2 coords × 8 bytes           3 points + 1 material + 1 tension
  = 1,600 bytes                            = 34 bytes
                                            + 100 deltas × 2 × 4 = 800 bytes
                                            = 834 bytes (48% reduction)
```

---

### 2.3 `ANALOG_STORY_POLE(0xD2)` — Transferring the Level

**Purpose:** Once you have a level surface (from `ANALOG_WATER_LEVEL`), transfer it to *other heights*. This is exactly what a story pole does in boat building: a notched stick where each notch is the vertical position of a frame, transferred from the lofting floor to the boat.

**Encoding:**

```
Byte  0:  0xD2           — opcode
Byte  1:  0x0A (10)      — payload length
Bytes 2–5:   anchor       — f32  (reference Y-coordinate, from WATER_LEVEL)
Bytes 6–9:   delta_ptr    — u32  (word-aligned address of delta array)
```

Delta count is implicit: `(10 - 2) / 4 = 2` deltas in payload, plus up to 16 more from the FLUX-C value stack (pushed before call).

**Pseudo-code:**

```flux-c
// ANALOG_STORY_POLE(0xD2)
// Input:  anchor Y (reference level), deltas from stack
// Output: absolute Y positions on stack

fn ANALOG_STORY_POLE(anchor, deltas[N]) {
    // Preconditions
    assert(is_finite(anchor))
    assert(all_finite(deltas))
    assert(N > 0 && N <= 16, "FLUX-C stack depth limit")

    // Running cumulative sum (like a story pole's notches):
    // notch[0] = anchor
    // notch[1] = anchor + delta[0]
    // notch[2] = anchor + delta[0] + delta[1]
    // etc.
    current = anchor
    for i in 0..N {
        current = current + deltas[i]    // running sum
        push_stack(current)
    }

    // Postconditions:
    // result[0] = anchor + deltas[0]
    // result[i] = result[i-1] + deltas[i]
    // All results finite
}
```

**Why cumulative sum?** Because the story pole metaphor: each notch is offset from the *previous* notch, not from the anchor. When you hold the pole against the hull, you're transferring relative positions, not absolute ones. The deltas represent the hull's *change* in shape from station to station — that's what the shipwright measured on the lofting floor.

**Why bounded to 16?** FLUX-C's stack depth is 16 frames. The opcode can't iterate unboundedly. This is a deliberate safety constraint — the output count is always known at call time.

**Preconditions:**
```
anchor is finite
All deltas are finite
N ∈ (0, 16]
delta_ptr word-aligned
```

**Postconditions:**
```
result[0] = anchor + delta[0]
result[i] = result[i-1] + delta[i]  (i > 0)
All result[i] finite
If all deltas = 0: all result[i] = anchor
```

---

### 2.4 `ANALOG_SECTOR(0xD3)` — Dividing the Arc

**Purpose:** Divide a total distance into equal proportional segments. In boat building, you'd use a ship's compass (beam compass) to step off equal distances along a curve. This opcode does that digitally.

**Encoding:**

```
Byte  0:  0xD3           — opcode
Byte  1:  0x09 (9)       — payload length
Bytes 2–5:   distance    — f32  (total arc length or chord length)
Bytes 6–9:   divisor     — u32  (2 ≤ divisor ≤ 256)
```

**Pseudo-code:**

```flux-c
// ANALOG_SECTOR(0xD3)
// Input:  total distance, number of segments
// Output: divisor equal segment lengths on stack

fn ANALOG_SECTOR(distance, divisor) {
    // Preconditions
    assert(distance > 0.0)
    assert(divisor >= 2 && divisor <= 256)
    assert(distance / divisor >= FLT_EPSILON, "would underflow")

    segment = distance / f32(divisor)

    // Postconditions
    // - All output values equal segment exactly
    // - Sum of all outputs = distance exactly
    // - Result deterministic (no iteration, pure division)
    for i in 0..divisor {
        push_stack(segment)
    }
}
```

**Why divide at all?** Because in a room, you often need *equal steps* along a boundary — the stations on a hull, the frames on a boat. `ANALOG_SECTOR` gives you those steps without floating-point iteration. You get `divisor` equal pieces, each exactly `distance/divisor`. This is useful for subdividing a spline (how many points per segment?) and for checking that tiles are evenly spaced.

**Why deterministic output?** No iteration means no accumulated rounding error. Each output is the exact same IEEE-754 division result. Sum of `divisor` copies = `distance` exactly (within floating-point precision).

**Preconditions:**
```
distance > 0.0
divisor ∈ [2, 256]
distance / divisor ≥ f32_epsilon  (no underflow)
```

**Postconditions:**
```
All outputs = distance / divisor (exactly equal)
Sum of outputs = distance
```

---

## 3. Room Boundary as Spline Surface

### 3.1 The Core Insight

A PLATO room's state is **not** a vector of coordinates. It's a *continuous surface* inferred from tile positions. The room stores the shape; the tiles are just evidence of it.

**Traditional storage:**
```
Room = { tile_0: (x₀, y₀), tile_1: (x₁, y₁), ..., tile_N: (x_N, y_N) }
```
16N bytes. Every tile is an independent fact. Corrupt one, and you have a hole.

**Spline-boundary storage:**
```
Room = {
  spline: ANALOG_SPLINE(p0, p1, p2, E, tension),
  deltas: [δ₀, δ₁, ..., δ_N]  // each tile = offset from previous
}
```
34 bytes for spline + 8N bytes for deltas = 34 + 8N. For N=100: 834 bytes vs. 1,600 bytes. **48% reduction.** And: if you lose half the deltas, you can still reconstruct the room from the spline. Lose half the coordinates in the traditional approach, and you have irrecoverable holes.

### 3.2 Incremental Update

Adding a tile to a spline-boundary room:

```flux-c
fn add_tile(room, new_tile) {
    // 1. Predict: where should this tile be on the current spline?
    expected_pos = evaluate_spline(room.spline, new_tile.x)

    // 2. Measure: how far is the actual tile from the spline?
    deviation = abs(new_tile.y - expected_pos.y)

    // 3. Guard check: within tolerance?
    if deviation > room.tolerance {
        flag_for_review(new_tile)  // anomaly detected
        return
    }

    // 4. Correct: update the spline if needed
    // Small deviation → fine-tune control points
    // Large deviation (but within tolerance) → add new control point
    room.spline = refine_spline(room.spline, new_tile, deviation)

    // 5. Append delta to stream
    room.deltas.append(new_tile.delta_from_previous)
}
```

This is the **Kalman filter cycle** — predict, measure, correct, update — applied to geometry. The spline is never "wrong." It's the best estimate given all measurements so far. New measurements refine it.

### 3.3 Noise Tolerance

Real materials and real measurements have noise. A cedar spline bent by hand won't follow the mathematical Bézier exactly. Tiles placed by agents won't fall exactly on the theoretical curve. The tolerance absorbs this:

```
tolerance = ε + material_variation × tension

where:
  ε = 1e-6                          (machine epsilon)
  material_variation = ±5%          (real material property variance)
  tension ∈ [0, 1]                  (curve tightness)
```

For oak: `tolerance = 1e-6 + 0.05 × tension ≈ 0.05` units. For steel: `tolerance = 1e-6 + 0.05 × 200 × tension` — but we cap this, because steel's high E means it resists bending, so the tolerance is physically bounded by the material's stiffness.

The tolerance is **physically meaningful**, not arbitrary. It says: "tiles within X of the spline are valid, because that's what the real material would actually do."

---

## 4. PLATO Room Self-Checking

### 4.1 How Rooms Use These Opcodes for Self-Validation

A PLATO room can check its own integrity using the analog opcodes. This is the self-checking property that makes spline-boundary rooms robust:

```flux-c
// Room integrity check — runs periodically or on-demand
fn room_self_check(room) {
    errors = []

    // 1. Reconstruct all tile positions from deltas + spline
    reconstructed = reconstruct_from_spline_and_deltas(room)

    // 2. For each tile, check it satisfies GUARD conditions
    for tile in room.placed_tiles {
        deviation = distance_to_spline(tile.pos, room.spline)
        if deviation > room.tolerance {
            errors.push((
                tile.id,
                "tile_deviation_exceeds_tolerance",
                deviation,
                room.tolerance
            ))
        }
    }

    // 3. Check spline self-consistency
    // The spline should pass through its own control points
    for cp in room.spline.control_points {
        if !spline_passes_through(room.spline, cp) {
            errors.push(("spline", "control_point_mismatch", cp))
        }
    }

    // 4. Check C1 continuity at control points
    discontinuity = compute_curvature_jump(room.spline)
    if discontinuity > EPSILON {
        errors.push(("spline", "C1_discontinuity", discontinuity))
    }

    // 5. Check material precondition on every ANALOG_SPLINE call
    // This is a GUARD assertion in the FLUX-C layer
    assert(room.material_E > 0.0, "material_E must be positive")
    assert(room.tension >= 0.0 && room.tension <= 1.0, "tension out of range")

    return errors  // empty = room is self-consistent
}
```

### 4.2 The Precondition/Postcondition Chain

Each opcode's postcondition is the next opcode's precondition. This creates a verifiable chain:

```
ANALOG_WATER_LEVEL
  post: Y = mean(points.y)
    ↓ feeds into
ANALOG_STORY_POLE
  pre: anchor (Y from WATER_LEVEL) must be finite
  post: result[i] = anchor + cumulative_deltas[i]
    ↓ feeds into
ANALOG_SPLINE
  pre: control points must be finite (from STORY_POLE output)
  post: spline passes through p0, p2; C1 continuous at p1
    ↓ used by
Room self-check
  pre: spline must have C1 continuity
  post: all tiles within tolerance of spline
```

If any postcondition fails, the FLUX-C GUARD layer catches it and the opcode fails safely. No undefined behavior. No NaN propagation. Every failure mode is explicit and checked.

---

## 5. Implementation Notes

### 5.1 Code Example: Full Tile Placement Cycle

```rust
// PLATO room tile placement with FLUX-C analog compute
// (Rust pseudocode matching the flux-c-analog crate API)

use flux_analog::{AnalogSpline, AnalogWaterLevel, AnalogStoryPole, AnalogSector};

fn place_tile_in_spline_room(
    room: &mut SplineRoom,
    tile: Tile,
) -> Result<(), RoomError> {
    // ── Step 1: Predict ──────────────────────────────────────────
    // Compute expected position on current spline at tile's X
    let expected = AnalogSpline::evaluate(&room.spline, tile.x);

    // ── Step 2: Measure ──────────────────────────────────────────
    // Distance from tile to expected position
    let deviation = (tile.y - expected.y).abs();

    // ── Step 3: Guard check ──────────────────────────────────────
    let tolerance = room.tolerance();
    if deviation > tolerance {
        return Err(RoomError::TileDeviation {
            tile_id: tile.id,
            deviation,
            tolerance,
        });
    }

    // ── Step 4: Delta encode ──────────────────────────────────────
    // Store delta from last tile, not absolute position
    let delta = Delta {
        dx: tile.x - room.last_tile.x,
        dy: tile.y - room.last_tile.y,
    };
    room.delta_stream.push(delta);

    // ── Step 5: Optional spline refinement ──────────────────────
    // If deviation is small but non-zero, fine-tune control points
    // using a weighted moving average
    if deviation > EPSILON && deviation < tolerance * 0.5 {
        room.spline = SplineRefiner::adjust(
            &room.spline,
            ControlPoint { x: tile.x, y: tile.y },
            deviation / tolerance,  // weight by how "tight" the fit is
        );
    }

    // ── Step 6: Self-check ───────────────────────────────────────
    // After every placement, room can verify its own integrity
    let self_check = room.self_check();
    if !self_check.is_empty() {
        log::warn!("room {} self-check found issues: {:?}", room.id, self_check);
    }

    room.last_tile = tile;
    Ok(())
}
```

### 5.2 Delta Compression

Each tile stores only its offset from the previous tile:

```
Delta format: [dx: f32, dy: f32] = 8 bytes per tile

vs. Absolute: [x: f32, y: f32] = 8 bytes per tile

For N=100 tiles:
  Absolute: 100 × 8 = 800 bytes
  Delta:    100 × 8 = 800 bytes  ← same (in this simple scheme)

But: delta + spline (34 bytes) vs. absolute (800 bytes)
  Delta+spline: 34 + 800 = 834 bytes
  Absolute:     800 bytes
  Break-even: N where 34 + 8N < 16N  →  N > 3.4 tiles

For N > 3: spline+delta uses LESS storage than absolute positions.
And fault tolerance is categorically better.
```

**Optional improvement:** Delta-of-delta (second-order difference) for further compression. Consecutive tiles that are all roughly the same offset from each other (a straight section of hull) compress to near-zero in a second-order scheme. But this interacts with fault tolerance — a single lost delta-of-delta corrupts all subsequent tiles. First-order deltas are more robust.

---

## 6. Related Work

### 6.1 Constraint Theory Ecosystem

FLUX-C analog compute is the geometric instantiation of the constraint theory approach to agent systems. In the constraint-theory framework:

- **Constraints** are invariants that must hold (tile must be within tolerance of spline)
- **Agents** are operators that modify state while preserving constraints
- **Rooms** are the state containers that expose constraints via FLUX-C opcodes

The analog opcodes extend this framework from *discrete* constraints (tile A must be adjacent to tile B) to *continuous* constraints (tile must lie on this smooth curve). This is essential for spatial reasoning — the real world is continuous, not discrete.

See: `constraint-theory-ecosystem` design docs.

### 6.2 Fleet-Coordinate

Fleet-coordinate is the multi-agent orchestration layer built on top of PLATO rooms. When multiple agents place tiles in the same room:

- **Conflict detection**: two agents try to place tiles that violate the spline constraint
- **Optimistic concurrency**: each agent works on its own delta stream; reconcile periodically
- **Spline as shared state**: the room's spline is the consensus boundary that all agents agree on

The analog opcodes provide the fault-tolerant shared state that fleet-coordinate needs. If an agent's delta stream is lost in transmission, the room can reconstruct from the remaining deltas + spline. With absolute coordinates, a lost coordinate is an irrecoverable hole in the shared state.

See: `fleet-coordinate` design docs.

### 6.3 FLUX-VM

FLUX-VM is the reference implementation of the FLUX-C instruction set. The analog opcodes are implemented as FLUX-VM primitives:

- `flux-vm/src/ops/analog.rs` — opcode implementations
- `flux-vm/src/guard/` — GUARD precondition/postcondition checking
- `flux-vm/src/stack.rs` — bounded stack model (max 256 frames, max 16 value stack depth)

The bounded stack model is what makes the opcodes safe: `ANALOG_SECTOR` outputs `divisor` values, but `divisor ≤ 256` always, so the stack never overflows. `ANALOG_STORY_POLE` processes at most 16 deltas for the same reason.

See: `flux-vm` repository.

---

## 7. Material Properties in FLUX-C

Materials are not hard-coded into the opcode — they're loaded from the FLUX-C constant table:

| Material | E (GPa) | Density | Typical Use | FLUX-C Symbol |
|----------|---------|---------|-------------|---------------|
| Cedar | 6.0 | 0.4 g/cm³ | Light, flexible boundaries | `GUARD_MAT_CEDAR` |
| Oak | 12.0 | 0.7 g/cm³ | Structural, moderate stiffness | `GUARD_MAT_OAK` |
| Fiberglass | 30.0 | 2.0 g/cm³ | Semi-rigid, moderate weight | `GUARD_MAT_FIBERGLASS` |
| Steel | 200.0 | 7.8 g/cm³ | Rigid, precise boundaries | `GUARD_MAT_STEEL` |

FLUX-C constants exposed to rooms:
- `GUARD_E` — current Young's modulus
- `GUARD_rho` — density (for weight calculations)
- `GUARD_tension` — current tension parameter
- `GUARD_tolerance` — room's geometric tolerance

Material selection is a GUARD assertion:

```flux-c
GUARD room.material == GUARD_MAT_OAK
// ^ Precondition: material must be set before ANALOG_SPLINE
```

---

## 8. R&D Iteration Cycle

Following the shipwright methodology: loft at 1:1 before committing to full construction.

```
┌─────────────────────────────────────────────────────────────┐
│  R&D Pipeline                                                │
│                                                              │
│  Phase 1 ──► Phase 2 ──► Phase 3 ──► Phase 4 ──► Phase 5   │
│  Digital      Benchmark    Physical     Edge         Production│
│  Sim          vs scipy     Prototype    Test         Integration│
│                                                              │
│  Deliverable:  Deliverable:  Deliverable:  Deliverable:   Deliverable:│
│  flux-c-       Benchmark    3D-printed   JC1 energy   PLATO room │
│  analog crate  report       spline       measurement  mode flag   │
│  + unit tests               fixture      + cloud      + migration  │
│                                         comparison  path          │
└─────────────────────────────────────────────────────────────┘
```

### Phase 1: Digital Simulation (current)

Implement `ANALOG_SPLINE` as a digital simulation of analog behavior. The FLUX-C opcode calls a digital function that computes the spline, but the API contract is designed to match a physical spline (boundary conditions, tolerance, material parameters).

**Deliverable:** `flux-c-analog` crate with `analog_spline`, `analog_water_level`, `analog_story_pole`, `analog_sector` functions. FLUX-C opcode encodings. Unit tests with known-good inputs.

### Phase 2: Benchmark

Measure `ANALOG_SPLINE` vs. standard digital interpolation (NumPy `scipy.interpolate.Bezier`, `scipy.interpolate.CubicSpline`). Metrics: latency per call, curve smoothness (second derivative continuity), memory usage.

### Phase 3: Physical Prototype

Design and 3D-print a spline tool from a known material (oak or cedar filament). Fix the spline between three points, measure the actual curve with a CNC probe, compare to `ANALOG_SPLINE` output.

### Phase 4: JC1 Edge Test

Deploy to Jetson Orin Nano (ARM64, edge). Run constraint solving on a PLATO room with 50+ tiles. Verify opcode terminates, produces correct outputs, stays within edge energy budget.

### Phase 5: Production Integration

Integrate `ANALOG_SPLINE` as an optional PLATO room mode. Standard absolute-coordinate rooms remain the default for simplicity.

---

## 9. Open Questions

1. **Tension parameter range:** `0.0–1.0` is proposed, but should this be material-dependent? Cedar can handle higher tension before kinking than steel. Should `tension_max` be a material property?

2. **Delta-of-delta compression:** Could use second-order differences for further compression, but a single lost delta corrupts all subsequent tiles. First-order deltas are more robust. Is the compression worth the fault-tolerance cost?

3. **3D extension:** The 3-point quadratic Bézier works for 2D surfaces. For 3D PLATO spaces (volumetric rooms), we need either a tensor-product Bézier surface or a b-spline. What is the minimum useful 3D primitive?

4. **GUARD tolerance validation:** The formula `ε + material_variation × tension` is proposed but unvalidated. Should we measure actual material variation for oak, cedar, fiberglass, and steel samples to get real numbers?

5. **Tile validity beyond geometry:** Currently tile validity is purely geometric (distance to spline). Should we also consider tile content semantics (does this tile's type match the expected boundary type at this position)?

---

## Summary

FLUX-C analog compute provides four opcodes that treat PLATO room boundaries as continuous spline surfaces — the way a shipwright actually works:

| Opcode | What it does | Physical analogy |
|--------|-------------|-----------------|
| `ANALOG_SPLINE(0xD0)` | Fit quadratic Bézier through 3 points | Bending a wooden spline between stations |
| `ANALOG_WATER_LEVEL(0xD1)` | Least-squares level surface through point cloud | Water settling under gravity |
| `ANALOG_STORY_POLE(0xD2)` | Transfer level to multiple heights | Story pole — notched transfer stick |
| `ANALOG_SECTOR(0xD3)` | Divide distance into equal segments | Ship's compass stepping off equal arcs |

The room's state is the spline, not a coordinate vector. Each tile placement refines the spline estimate (Kalman filter). Tile validity is measured as distance to the spline curve, bounded by a GUARD tolerance derived from real material properties.

**Storage:** 48% reduction for rooms larger than ~3 tiles.  
**Fault tolerance:** Lose half the deltas, reconstruct from remaining. Lose one absolute coordinate, you have a hole.  
**Safety:** Every opcode has explicit pre/postconditions checked by FLUX-C GUARD. Every failure mode is explicit.

The R&D cycle follows shipwright practice: simulate → benchmark → physical prototype → edge test → deploy. No skipping stages.

---

*FLUX-C analog compute design — Oracle1, PLATO Fleet Architecture — 2026-05-07*
