import requests

BASE_URL = "http://147.224.38.131:4042"
AGENT = "MiniMax"

def get(endpoint, params):
    params["agent"] = AGENT
    r = requests.get(f"{BASE_URL}{endpoint}", params=params)
    return r.json()

print("Move harbor:", get("/move", {"room": "harbor"}))
print("Look:", get("/look", {}))
print("Think:", get("/interact", {"action": "think", "target": "harbor"}))
print("Create:", get("/interact", {"action": "create", "target": "harbor"}))
print("Interact dock (examine):", get("/interact", {"action": "examine", "target": "dock"}))
print("Interact dock (use):", get("/interact", {"action": "use", "target": "dock"}))
print("Talk to MiniMax-Agent:", get("/talk", {"target": "MiniMax-Agent", "message": "hello"}))

