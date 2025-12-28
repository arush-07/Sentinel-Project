import json
import time
import random
import os

FOLDER = "stream_data"
if not os.path.exists(FOLDER):
    os.makedirs(FOLDER)

LOCATIONS = [
    {"name": "Central Metro Station", "lat": 12.9716, "lon": 77.5946}, 
    {"name": "Chemical Plant Sector 4", "lat": 12.9352, "lon": 77.6245},
    {"name": "North Avenue Park", "lat": 12.9784, "lon": 77.6408},
    {"name": "City Hospital", "lat": 12.9250, "lon": 77.5891},
    {"name": "Tech Park Main Gate", "lat": 12.9900, "lon": 77.6600}
]

SCENARIOS = [
    "Suspicious package found near entrance, ticking sound heard.",
    "A cat is stuck in a tree and meowing loudly.",
    "Massive explosion reported, yellow smoke rising, workers trapped.",
    "Minor traffic accident, no injuries, traffic blocked.",
    "Fire alarm triggered in server room, smoke visible."
]

print("🚨 Simulation Started: Generating events every 5 seconds...")

try:
    while True:
        loc = random.choice(LOCATIONS)
        event = {
            "timestamp": time.strftime("%H:%M:%S"),
            "location": loc["name"],
            "latitude": loc["lat"],
            "longitude": loc["lon"],
            "report_text": random.choice(SCENARIOS)
        }
        filename = f"report_{int(time.time())}.json"
        filepath = os.path.join(FOLDER, filename)
        with open(filepath, "w") as f:
            json.dump(event, f)
            f.write("\n")
            
        print(f" -> Generated: {event['report_text']} at {event['location']}")
        time.sleep(5)

except KeyboardInterrupt:
    print("\n🛑 Simulation Stopped.")