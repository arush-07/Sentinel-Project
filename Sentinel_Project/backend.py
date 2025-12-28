import pathway as pw
import os
from typing import TypedDict, Literal
from langgraph.graph import StateGraph, END
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_core.messages import HumanMessage

load_dotenv()
genai.configure(api_key=os.getenv("GOOGLE_API_KEY")) # Load API key from .env

class AgentState(TypedDict):
    report_text: str
    location: str
    severity: str
    unit: str
    plan: str

# Initialize Gemini
llm = ChatGoogleGenerativeAI(
    model="gemini-2.5-flash",
    google_api_key=os.environ["GOOGLE_API_KEY"],
    temperature=0
)

def classify_node(state: AgentState):
    msg = f"Report: '{state['report_text']}' at '{state['location']}'. Classify SEVERITY as 'Low', 'Medium', or 'Critical'. Return ONLY the word."
    response = llm.invoke([HumanMessage(content=msg)])
    return {"severity": response.content.strip()}

def dispatch_node(state: AgentState):
    msg = f"Event Severity is {state['severity']}. Report: {state['report_text']}. Assign BEST UNIT (Police, Fire, SWAT, Ambulance) and a 5-word Action Plan."
    response = llm.invoke([HumanMessage(content=f"{msg}. Format: UNIT | PLAN")])

    try:
        parts = response.content.split("|")
        return {"unit": parts[0].strip(), "plan": parts[1].strip()}
    except:
        return {"unit": "General Patrol", "plan": "Investigate scene"}

def validate_node(state: AgentState):
    if "Critical" in state['severity'] and "None" in state['unit']:
        return {"unit": "SWAT + HAZMAT (Forced Override)", "plan": "Immediate deployment required"}
    return {} 

workflow = StateGraph(AgentState)
workflow.add_node("classify", classify_node)
workflow.add_node("dispatch", dispatch_node)
workflow.add_node("validate", validate_node)


workflow.set_entry_point("classify")
workflow.add_edge("classify", "dispatch")
workflow.add_edge("dispatch", "validate")
workflow.add_edge("validate", END)


app = workflow.compile()

class InputSchema(pw.Schema):
    report_text: str
    location: str
    timestamp: str
    latitude: float
    longitude: float

def agent_pipeline(report_text, location):
    try:
        inputs = {"report_text": report_text, "location": location}
        result = app.invoke(inputs)
        return f"{result['severity']} | {result['unit']} | {result['plan']}"
    except Exception as e:
        return f"ERROR | FAIL | {str(e)}"
input_stream = pw.io.fs.read(
    "./stream_data",
    format="json",
    schema=InputSchema,
    mode="streaming"
)

processed_data = input_stream.select(
    timestamp=input_stream.timestamp,
    location=input_stream.location,
    report=input_stream.report_text,
    latitude=input_stream.latitude,
    longitude=input_stream.longitude,
    ai_decision=pw.apply(agent_pipeline, input_stream.report_text, input_stream.location)
)
pw.io.csv.write(processed_data, "output.csv")
print("✅ Sentinel LangGraph Agent Running...")
pw.run()