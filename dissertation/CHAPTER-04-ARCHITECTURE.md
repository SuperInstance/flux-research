# Chapter 4: PLATO Architecture

## 4.1 Overview

This chapter describes the PLATO architecture in sufficient detail for reproducibility. PLATO consists of four primary components: the room server, the tile protocol, the presence system, and the voice interface.

The architecture is designed around three principles derived from the theoretical framework:
1. Rooms are the unit of organization
2. Change recording is the fundamental operation
3. Presence is real-time, not polling

---

## 4.2 Room Server

### 4.2.1 Overview

The PLATO room server is a lightweight HTTP server that manages rooms and tiles. It exposes a REST API for room and tile operations and a WebSocket stream for presence.

### 4.2.2 Core Data Model

```python
class Room:
    name: str              # Unique room identifier (e.g., "buoy-7")
    created: datetime       # Room creation timestamp
    tiles: List[Tile]      # Ordered, append-only list of tiles
    
class Tile:
    id: str                # UUID
    room: str              # Room name
    author: str            # Author identifier
    timestamp: datetime    # When the change was observed
    content: str           # Description of the change
    previous_id: str       # ID of the previous tile in this room

class Observer:
    agent_id: str          # Agent identifier
    room: str              # Room name
    connected: datetime    # When presence began
    last_seen: datetime    # Last activity
```

### 4.2.3 Room Operations

| Operation | Method | Endpoint |
|-----------|--------|----------|
| Create room | POST | `/rooms` |
| List rooms | GET | `/rooms` |
| Get room | GET | `/rooms/{name}` |
| Delete room | DELETE | `/rooms/{name}` |

### 4.2.4 Tile Operations

| Operation | Method | Endpoint |
|-----------|--------|----------|
| Submit tile | POST | `/rooms/{name}/tiles` |
| Get tiles | GET | `/rooms/{name}/tiles?limit=N` |
| Subscribe | WS | `/rooms/{name}/stream` |

### 4.2.5 Query Parameters

Tiles can be filtered by:
- `limit=N` — most recent N tiles (default: 100)
- `since=timestamp` — tiles since a time
- `author=agent` — tiles by a specific author
- `before=timestamp` — tiles before a time

---

## 4.3 The Tile Protocol

### 4.3.1 Submitting a Tile

```bash
POST /rooms/buoy-7/tiles
Content-Type: application/json

{
    "author": "captain:jones",
    "content": "Chum running thick, morning tide",
    "timestamp": "2026-05-04T06:30:00Z"
}
```

Response:
```json
{
    "id": "tile-uuid-1234",
    "room": "buoy-7",
    "author": "captain:jones",
    "timestamp": "2026-05-04T06:30:00Z",
    "content": "Chum running thick, morning tide",
    "previous_id": "tile-uuid-1199"
}
```

### 4.3.2 Reading Tiles

```bash
GET /rooms/buoy-7/tiles?limit=10
```

Response:
```json
{
    "room": "buoy-7",
    "count": 10,
    "tiles": [
        {
            "id": "tile-uuid-1234",
            "author": "captain:jones",
            "timestamp": "2026-05-04T06:30:00Z",
            "content": "Chum running thick, morning tide"
        },
        ...
    ]
}
```

### 4.3.3 The `previous_id` Chain

Each tile references the previous tile in the room. This creates an immutable, ordered chain — a simple blockchain without proof-of-work.

The chain enables:
- Ordering: tiles are strictly ordered by the chain, not by timestamp
- Integrity: tampering with a tile breaks the chain
- Causality: following the chain backward shows the history of the room

---

## 4.4 Presence System

### 4.4.1 Observer Registry

The room server maintains an observer registry for each room:

```python
{
    "buoy-7": [
        {"agent_id": "captain:jones", "connected": "2026-05-04T06:00:00Z"},
        {"agent_id": "agent:catch-log", "connected": "2026-05-04T05:30:00Z"},
        {"agent_id": "agent:weather-watch", "connected": "2026-05-04T04:00:00Z"}
    ]
}
```

### 4.4.2 WebSocket Stream

Agents subscribe to room streams via WebSocket:

```bash
WS /rooms/buoy-7/stream
```

Messages are delivered in real-time as tiles are submitted:

```json
{
    "type": "tile",
    "tile": {
        "id": "tile-uuid-1234",
        "author": "captain:jones",
        "content": "Chum running thick, morning tide"
    }
}
```

### 4.4.3 Observer Events

```json
{"type": "join", "agent_id": "captain:smith"}
{"type": "leave", "agent_id": "captain:smith"}
```

Agents can see who else is present. This is presence awareness.

### 4.4.4 Presence vs Subscription

Subscription is technical — receiving messages. Presence is social — being recognized as in the room.

An agent that subscribes to a room stream but never contributes is a lurker. An agent that contributes is present.

The distinction matters for trust. A tile from a present agent carries more weight than a tile from a lurker. Over time, the system develops a model of who has been present when — a form of reputation.

---

## 4.5 The Voice Interface

### 4.5.1 Design Goals

The voice interface is designed for maritime use:
- **Hands-free:** captains cannot type while operating the vessel
- **Accented:** maritime vocabulary is different from standard speech
- **Noisy:** engine noise, wind, waves
- **Intermittent connectivity:** boats lose signal

### 4.5.2 Architecture

```
Microphone → Browser Web Speech API → Room Server → Room Stream → Fleet Agents
                                    ↑
                              Tile Submission
```

### 4.5.3 Room Selection

The voice interface is room-aware. Before speaking, the user selects a room — `buoy-7`, `bridge`, `engine-room`, etc.

Room selection can be:
- Manual: tap to select
- Voice command: "Enter buoy-7" (planned)
- Location: GPS auto-select (planned)

### 4.5.4 Speech Recognition

The current prototype uses the Web Speech API, which is browser-based. In production, maritime speech recognition would require:
- Custom vocabulary for maritime terms
- Noise reduction for engine noise
- Offline capability for when connectivity drops

### 4.5.5 Confirmation

After speech recognition, the system confirms what was heard:

```
[Capt. Jones]: "Chum running thick at buoy 7"
[System]: "Chum running thick at buoy 7 — confirmed?"
```

If confirmed, the tile is submitted. If not, the user can repeat.

---

## 4.6 Delta Recording Implementation

### 4.6.1 Sensor Protocol

Sensors (depth sounder, temperature probe, GPS) can submit tiles via the REST API. The sensor protocol includes:

```json
{
    "type": "sensor",
    "sensor_id": "depth-sounder-hld-2",
    "room": "hold-2",
    "value": 38,
    "unit": "fathoms",
    "previous_value": 40,
    "timestamp": "2026-05-04T06:30:00Z"
}
```

### 4.6.2 Delta Rule

A sensor tile is stored only if:
1. `previous_value` is not set (first reading), OR
2. `value != previous_value` (value changed)

If the depth is 38 fathoms ten times in a row, only the first reading is stored. The system records what changed, not what persists.

### 4.6.3 Rate Limiting

To prevent flooding, sensors are rate-limited to one tile per minute per room unless the value changes.

---

## 4.7 Integration with Fleet Agents

### 4.7.1 Agent Presence

Fleet agents connect to rooms via WebSocket:

```python
class FleetAgent:
    def __init__(self, name, rooms):
        self.name = name
        self.rooms = rooms
        
    def connect(self, server_url):
        for room in self.rooms:
            ws = WebSocket(f"{server_url}/rooms/{room}/stream")
            ws.on_message(self.on_tile)
            
    def on_tile(self, tile):
        # Process tile in context of room history
        self.observe(tile)
```

### 4.7.2 Context Maintenance

Agents maintain a rolling window of recent tiles for each room:

```python
class RoomContext:
    def __init__(self, room_name, window=100):
        self.room = room_name
        self.tiles = deque(maxlen=window)
        
    def observe(self, tile):
        self.tiles.append(tile)
        self.update_model()
```

### 4.7.3 Response Generation

Agents can respond to tiles or queries:

```python
def respond(self, room, content):
    tile = {
        "author": self.name,
        "room": room,
        "content": content
    }
    requests.post(f"{PLATO_URL}/rooms/{room}/tiles", json=tile)
```

---

## 4.8 Deployment

### 4.8.1 Local Deployment

```bash
python3 -m http.server 8847
# PLATO available at http://localhost:8847
```

### 4.8.2 Docker Deployment

```bash
docker run -p 8847:8847 \
    -v plato-data:/data \
    ghcr.io/superinstance/plato-server
```

### 4.8.3 Fleet Deployment

For production maritime use:
- Multiple PLATO server instances for redundancy
- Satellite connectivity for remote deployments
- Local-first architecture (sync when connected)
- Offline tile buffering

---

## 4.9 Summary

The PLATO architecture implements the theoretical framework:

1. **Rooms** are the unit of organization — named, persistent, spatially-organized
2. **Tiles** are change records — immutable, ordered by chain, stored sparsely
3. **Presence** is real-time — WebSocket streams, observer registry
4. **Voice** is the primary interface — for maritime use, hands-free

The architecture is intentionally simple. Complexity emerges from the accumulated history of rooms, not from the mechanism itself.

---

**Keywords:** room server, tile protocol, presence system, voice interface, WebSocket, delta recording
