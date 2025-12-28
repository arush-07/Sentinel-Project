import json
import time
import random
import os

# Define the folder to drop data into
FOLDER = "stream_data"
if not os.path.exists(FOLDER):
    os.makedirs(FOLDER)

# Emergency Types for simulation
LOCATIONS = [
    {"name": "Central Metro Station", "lat": 12.9716, "lon": 77.5946}, # Bangalore coords example
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
        # Pick a random event
        loc = random.choice(LOCATIONS)
        event = {
            "timestamp": time.strftime("%H:%M:%S"),
            "location": loc["name"],
            "latitude": loc["lat"],
            "longitude": loc["lon"],
            "report_text": random.choice(SCENARIOS)
        }
        
        # Create a unique filename so Pathway sees it as "New"
        filename = f"report_{int(time.time())}.json"
        filepath = os.path.join(FOLDER, filename)
        
        # Write properly formatted JSON Line
        with open(filepath, "w") as f:
            json.dump(event, f)
            f.write("\n")
            
        print(f" -> Generated: {event['report_text']} at {event['location']}")
        
        # Wait 5 seconds before the next emergency
        time.sleep(5)

except KeyboardInterrupt:
    print("\n🛑 Simulation Stopped.")