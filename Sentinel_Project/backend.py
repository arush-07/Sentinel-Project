import pathway as pw
import google.generativeai as genai
import os
import time

# --- CONFIGURATION ---
# ⚠️ IMPORTANT: Paste your NEW Google API Key here below
os.environ["GOOGLE_API_KEY"] = "AIzaSyAUUmulf2IJZw0LlopI5XoedpBh-F0PTw0"

genai.configure(api_key=os.environ["GOOGLE_API_KEY"])

# Use Gemini 2.5 Flash (or 1.5 Flash if 2.5 is unavailable in your region)
MODEL_NAME = 'gemini-2.5-flash' 
model = genai.GenerativeModel(MODEL_NAME)

# --- 1. DEFINE INPUT FORMAT (UPDATED FOR MAP) ---
# We added latitude and longitude so the Dashboard can plot them
class InputSchema(pw.Schema):
    report_text: str
    location: str
    timestamp: str
    latitude: float   # <--- NEW FIELD
    longitude: float  # <--- NEW FIELD

# --- 2. THE BRAIN (Gemini 2.5 Flash) ---
def agent_decision(report_text, location):
    try:
        # Prompt Engineering for the Agent
        prompt = f"""
        Act as an Emergency Dispatch Agent.
        Event: "{report_text}" at "{location}".
        
        Task:
        1. Classify SEVERITY (Low, Medium, Critical).
        2. Assign UNIT (Police, Fire, Ambulance, SWAT, None).
        3. Write a short Action Plan (max 10 words).
        
        Output format: SEVERITY | UNIT | PLAN
        (Example: Critical | Fire | Dispatch engine and evacuate area)
        """
        
        # Call Gemini
        response = model.generate_content(prompt)
        return response.text.strip()
    except Exception as e:
        return f"ERROR | NONE | System Fault: {str(e)}"

# --- 3. THE REAL-TIME PIPELINE ---
# Watch the folder for new files
input_stream = pw.io.fs.read(
    "./stream_data",
    format="json",
    schema=InputSchema,
    mode="streaming" 
)

# Apply the Agent decision AND pass through coordinates
processed_data = input_stream.select(
    timestamp=input_stream.timestamp,
    location=input_stream.location,
    report=input_stream.report_text,
    latitude=input_stream.latitude,   # <--- PASS TO OUTPUT
    longitude=input_stream.longitude, # <--- PASS TO OUTPUT
    # This 'apply' line sends data to Gemini
    ai_decision=pw.apply(agent_decision, input_stream.report_text, input_stream.location)
)

# --- 4. OUTPUT ---
# Write results to CSV for the dashboard to read
pw.io.csv.write(processed_data, "output.csv")

if __name__ == "__main__":
    print(f"✅ Sentinel Backend Active.")
    print(f"🧠 Model: {MODEL_NAME}")
    print("📍 Map Data: Enabled")
    print("👀 Watching ./stream_data/ for new reports...")
    pw.run()