import requests
import json
import time

BASE_URL = "http://147.224.38.131:4042"
AGENT = "MiniMax_Explorer"

def get(endpoint, params):
    params["agent"] = AGENT
    r = requests.get(f"{BASE_URL}{endpoint}", params=params)
    time.sleep(0.1) # Be nice to the server
    return r.json()

# Connect first
requests.get(f"{BASE_URL}/connect?agent={AGENT}&archetype=scholar")

rooms_to_visit = [
    "harbor", "bridge", "forge", "tide-pool", "lighthouse", "current",
    "reef", "shell-gallery", "barracks", "workshop", "archives", "garden",
    "dry-dock", "observatory", "court", "horizon"
]

all_data = {}

for room in rooms_to_visit:
    print(f"Exploring {room}...")
    
    # Move to the room
    move_res = get("/move", {"room": room})
    if "error" in move_res and "can't go to" in move_res["error"]:
        print(f"Cannot directly move to {room} from current location. Will need to pathfind.")
        continue
    
    # Read the room info
    room_data = move_res
    objects = room_data.get("objects", [])
    entities = room_data.get("others_here", [])
    
    room_info = {
        "name": room_data.get("name", room),
        "description": room_data.get("description", ""),
        "atmosphere": room_data.get("atmosphere", ""),
        "exits": room_data.get("exits", []),
        "objects": {},
        "entities": {},
        "think_results": [],
        "create_results": []
    }
    
    # Interact with objects
    for obj in objects:
        obj_data = {}
        # Examine
        ex = get("/interact", {"action": "examine", "target": obj})
        obj_data["examine"] = ex.get("result", str(ex))
        
        # Use
        use = get("/interact", {"action": "use", "target": obj})
        obj_data["use"] = use.get("result", str(use))
        
        # Think
        think = get("/interact", {"action": "think", "target": obj})
        room_info["think_results"].append((obj, think.get("result", str(think))))
        
        # Create
        create = get("/interact", {"action": "create", "target": obj})
        room_info["create_results"].append((obj, create.get("result", str(create))))
        
        room_info["objects"][obj] = obj_data
        
    # Talk to entities
    for ent in entities:
        # Don't talk to ourselves
        if ent == AGENT:
            continue
        talk = get("/talk", {"target": ent, "message": "Greetings, what insights can you share?"})
        room_info["entities"][ent] = talk
        
    all_data[room] = room_info

# Write to JSON for inspection
with open("/workspace/exploration_data.json", "w") as f:
    json.dump(all_data, f, indent=2)

print("Exploration complete!")
