import os
import json
from typing import TypedDict, List
from pydantic import BaseModel
from google import genai
from google.genai import types
from qdrant_client import QdrantClient
from langgraph.graph import StateGraph, START, END

# ==========================================
# 1. CENTRAL GRAPH STATE
# ==========================================
class HealerState(TypedDict):
    raw_code_context: str
    target_file: str
    vulnerability_details: str
    critical_vulnerability_found: bool
    execution_log: str

# Structural validation schemas from Day 3
class AuditFinding(BaseModel):
    vulnerability_type: str
    severity: str
    file_path: str
    flawed_code: str
    explanation: str
    remediation: str

class CodebaseAuditReport(BaseModel):
    project_summary: str
    findings: List[AuditFinding]

# ==========================================
# 2. PHYSICAL OS TOOLS (The Agent's Hands)
# ==========================================
def write_secure_patch_tool(file_path: str, patched_code: str) -> str:
    """A highly specialized tool suitable for safely writing code patches to disk."""
    print(f"🛠️  [Executing Tool] Modifying file system asset: {file_path}")
    try:
        # Secure the directory path if it doesn't exist
        os.makedirs(os.path.dirname(file_path), exist_ok=True)
        
        # Overwrite the vulnerable file with clean, parameterized logic
        with open(file_path, "w") as f:
            f.write(patched_code.strip() + "\n")
        return f"SUCCESS: Successfully patched and secured {file_path}."
    except Exception as e:
        return f"FAILURE: Could not write patch to disk due to error: {str(e)}"

# ==========================================
# 3. GRAPH WORKER NODES
# ==========================================
def fetch_context_node(state: HealerState) -> HealerState:
    """Node 1: Pull context records from Qdrant."""
    print("📥 [Node: Fetch Context] Scanning local Qdrant vectors...")
    db_client = QdrantClient(host="localhost", port=6333)
    
    scroll_result, _ = db_client.scroll(
        collection_name="local_codebase",
        with_payload=True,
        limit=10
    )
    
    context_list = []
    for point in scroll_result:
        context_list.append(f"--- FILE: {point.payload['file_path']} ---\n{point.payload['text']}\n")
        
    return {
        "raw_code_context": "\n".join(context_list),
        "target_file": "",
        "vulnerability_details": "",
        "critical_vulnerability_found": False,
        "execution_log": ""
    }

def analyze_and_route_node(state: HealerState) -> HealerState:
    """Node 2: Structural analysis barrier via Gemini."""
    print("🧠 [Node: Analyze & Route] Querying Gemini logical engine...")
    ai_client = genai.Client()
    
    prompt = f"Audit this code context for security issues:\n{state['raw_code_context']}"
    
    response = ai_client.models.generate_content(
        model='gemini-2.5-flash',
        contents=prompt,
        config=types.GenerateContentConfig(
            response_mime_type="application/json",
            response_schema=CodebaseAuditReport,
            temperature=0.1
        ),
    )
    
    report_data = json.loads(response.text)
    findings = report_data.get('findings', [])
    
    # Locate critical vulnerabilities needing immediate mitigation
    critical_finding = next((f for f in findings if f['severity'].upper() == 'CRITICAL'), None)
    
    if critical_finding:
        print(f"⚠️  [Alert] Critical flaw discovered in {critical_finding['file_path']}! Diverting to repair stream.")
        return {
            "critical_vulnerability_found": True,
            "target_file": critical_finding['file_path'],
            "vulnerability_details": f"Type: {critical_finding['vulnerability_type']}\nExplanation: {critical_finding['explanation']}"
        }
    
    print("✅ No critical security threats detected. Ending workflow pipeline.")
    return {"critical_vulnerability_found": False}

def auto_heal_node(state: HealerState) -> HealerState:
    """Node 3: Autonomous patch engineering and execution tier."""
    print(f"🔥 [Node: Auto-Heal] Generating non-vulnerable codebase rewrite for {state['target_file']}...")
    ai_client = genai.Client()
    
    prompt = f"""
    You are an automated AppSec patching engineer. Your target file is: {state['target_file']}
    It suffers from the following critical flaw:
    {state['vulnerability_details']}
    
    Here is the full codebase context for reference:
    {state['raw_code_context']}
    
    Output the complete, corrected, and production-ready source code for ONLY the target file ({state['target_file']}).
    Do not use markdown code blocks like ```python, do not explain anything, do not include comments. 
    Output raw python code only.
    """
    
    response = ai_client.models.generate_content(
        model='gemini-2.5-flash',
        contents=prompt,
        config=types.GenerateContentConfig(temperature=0.1)
    )
    
    clean_code = response.text.replace("python", "").replace("```", "").strip()
    
    # Fire the physical file system tool
    tool_result = write_secure_patch_tool(
        file_path=state['target_file'],
        patched_code=clean_code
    )
    
    print(f"📦 [System Status] Tool Execution Result -> {tool_result}")
    return {"execution_log": tool_result}

# ==========================================
# 4. CONDITIONAL ROUTING RULES
# ==========================================
def healing_gate(state: HealerState):
    if state["critical_vulnerability_found"]:
        return "auto_heal"
    return END

# ==========================================
# 5. ASSEMBLING THE GRAPH RUNTIME
# ==========================================
builder = StateGraph(HealerState)

builder.add_node("fetch_context", fetch_context_node)
builder.add_node("analyze_and_route", analyze_and_route_node)
builder.add_node("auto_heal", auto_heal_node)

builder.add_edge(START, "fetch_context")
builder.add_edge("fetch_context", "analyze_and_route")

builder.add_conditional_edges(
    "analyze_and_route",
    healing_gate,
    {
        "auto_heal": "auto_heal",
        END: END
    }
)

builder.add_edge("auto_heal", END)
healer_workflow = builder.compile()

if __name__ == "__main__":
    print("🚀 Initializing Autonomous Self-Healing Graph Loop...")
    initial_state = {
        "raw_code_context": "",
        "target_file": "",
        "vulnerability_details": "",
        "critical_vulnerability_found": False,
        "execution_log": ""
    }
    
    final_state = healer_workflow.invoke(initial_state)
    print("\n🏁 [Self-Healing Process Complete]")