import requests

BASE_URL = "http://147.224.38.131:4042"
AGENT = "MiniMax"

def get(endpoint, params):
    params["agent"] = AGENT
    r = requests.get(f"{BASE_URL}{endpoint}", params=params)
    return r.json()

print("Think endpoint:", get("/think", {"room": "harbor"}))
print("Create endpoint:", get("/create", {"room": "harbor"}))
print("Interact think dock:", get("/interact", {"action": "think", "target": "dock"}))
print("Interact create dock:", get("/interact", {"action": "create", "target": "dock"}))

