import requests
import json
import time

BASE_URL = "http://147.224.38.131:4042"
AGENT = "MiniMax_Bot"

def api(endpoint, params):
    params["agent"] = AGENT
    for _ in range(3):
        try:
            r = requests.get(f"{BASE_URL}{endpoint}", params=params, timeout=5)
            return r.json()
        except:
            time.sleep(1)
    return {}

# Reconnect to start at harbor
api("/connect", {"archetype": "scholar"})
current_room = "harbor"

visited = set()
graph = {}
all_data = {}

def dfs(room):
    global current_room
    print(f"Visiting {room}...")
    if current_room != room:
        # Move to the room (assuming adjacent for this simple dfs if we trace back)
        res = api("/move", {"room": room})
        if "error" in res:
            print("ERROR moving to", room, res)
            return
        current_room = room
    else:
        res = api("/look", {})
    
    visited.add(room)
    
    room_data = {
        "name": res.get("name", room),
        "description": res.get("description", ""),
        "atmosphere": res.get("atmosphere", ""),
        "exits": res.get("exits", []),
        "objects": {},
        "think_results": {},
        "create_results": {},
        "talk_results": {}
    }
    
    for obj in res.get("objects", []):
        room_data["objects"][obj] = {
            "examine": api("/interact", {"action": "examine", "target": obj}).get("result", ""),
            "use": api("/interact", {"action": "use", "target": obj}).get("result", "")
        }
        room_data["think_results"][obj] = api("/interact", {"action": "think", "target": obj}).get("result", "")
        room_data["create_results"][obj] = api("/interact", {"action": "create", "target": obj}).get("result", "")

    for ent in res.get("others_here", []):
        if ent != AGENT:
            # Maybe talk without message?
            talk = api("/talk", {"target": ent, "message": "hello"})
            room_data["talk_results"][ent] = "Message delivered." if talk.get("delivered") else str(talk)

    all_data[room] = room_data
    exits = res.get("exits", [])
    
    for next_room in exits:
        if next_room not in visited:
            dfs(next_room)
            # go back
            api("/move", {"room": room})
            current_room = room

dfs("harbor")

with open("/workspace/all_rooms.json", "w") as f:
    json.dump(all_data, f, indent=2)

print("Exploration finished. Visited:", len(visited), "rooms")
