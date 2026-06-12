import os
import json
from typing import TypedDict, List, Optional
from pydantic import BaseModel, Field
from google import genai
from google.genai import types
from qdrant_client import QdrantClient
from langgraph.graph import StateGraph, START, END

# ==========================================
# 1. THE AGENT STATE (CENTRAL MEMORY)
# ==========================================
class AuditorState(TypedDict):
    raw_code_context: str
    structured_report: dict
    critical_vulnerability_found: bool
    deep_dive_remediation: str

# Re-importing our Day 3 Pydantic schemas for the extraction barrier
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
# 2. THE GRAPH NODES (WORKERS)
# ==========================================

def fetch_context_node(state: AuditorState) -> AuditorState:
    """Node 1: Pull context records from the localized Qdrant DB."""
    print("📥 [Node: Fetch Context] Accessing optimized Qdrant vector spaces...")
    db_client = QdrantClient(host="localhost", port=6333)
    
    scroll_result, _ = db_client.scroll(
        collection_name="local_codebase",
        with_payload=True,
        limit=10
    )
    
    context_list = []
    for point in scroll_result:
        context_list.append(f"--- FILE: {point.payload['file_path']} ---\n{point.payload['text']}\n")
    
    # Update state memory
    return {
        "raw_code_context": "\n".join(context_list),
        "critical_vulnerability_found": False,
        "structured_report": {},
        "deep_dive_remediation": ""
    }

def analyze_code_node(state: AuditorState) -> AuditorState:
    """Node 2: Run verification validation barriers through Gemini."""
    print("🧠 [Node: Analyze Code] Executing Pydantic barrier audit via Gemini Cloud...")
    ai_client = genai.Client()
    
    prompt = f"Analyze this codebase for security vulnerabilities:\n{state['raw_code_context']}"
    
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
    
    # Check if a critical flaw stands out (auffallen) to toggle state machine router
    critical_flag = any(f['severity'].upper() == 'CRITICAL' for f in report_data.get('findings', []))
    if critical_flag:
        print("⚠️  [Alert] Critical security flaw flagged in memory! Routing logic activated.")
        
    return {
        "structured_report": report_data,
        "critical_vulnerability_found": critical_flag
    }

def deep_dive_patcher_node(state: AuditorState) -> AuditorState:
    """Node 3: Run advanced structural patch generation on critical failures."""
    print("🔥 [Node: Deep Dive Patcher] Writing customized engineering defense blueprint...")
    ai_client = genai.Client()
    
    prompt = f"""
    The automated auditor found a CRITICAL flaw in this context:
    {json.dumps(state['structured_report'], indent=2)}
    
    Write an advanced structural patch report explaining how to re-architect this block to prevent severe exploits.
    """
    
    response = ai_client.models.generate_content(
        model='gemini-2.5-flash',
        contents=prompt
    )
    
    return {"deep_dive_remediation": response.text}

# ==========================================
# 3. ROUTING LOGIC (CONDITIONAL EDGES)
# ==========================================
def routing_gate(state: AuditorState):
    """Evaluates state metrics to determine next workflow direction."""
    if state["critical_vulnerability_found"]:
        return "deep_dive_patcher"
    return END

# ==========================================
# 4. BUILDING THE GRAPH WORKFLOW
# ==========================================
builder = StateGraph(AuditorState)

# Register Nodes
builder.add_node("fetch_context", fetch_context_node)
builder.add_node("analyze_code", analyze_code_node)
builder.add_node("deep_dive_patcher", deep_dive_patcher_node)

# Link Structural Nodes
builder.add_edge(START, "fetch_context")
builder.add_edge("fetch_context", "analyze_code")

# Inject Conditional Routing Gate
builder.add_conditional_edges(
    "analyze_code",
    routing_gate,
    {
        "deep_dive_patcher": "deep_dive_patcher",
        END: END
    }
)

# Compile Graph State Machine
audit_workflow = builder.compile()

if __name__ == "__main__":
    print("🏁 Initializing Stateful LangGraph Auditor Session...")
    initial_state = {
        "raw_code_context": "",
        "structured_report": {},
        "critical_vulnerability_found": False,
        "deep_dive_remediation": ""
    }
    
    # Execute state runtime engine
    final_state = audit_workflow.invoke(initial_state)
    print("\n🏁 [Graph Run Complete]")
    
    # ==========================================
    # NEW: PERSISTENCE LAYER (WRITE TO DISK)
    # ==========================================
    print("\n💾 Extracting memory state and writing files to disk...")
    
    # 1. Save the structured JSON findings from Node 2
    if final_state.get("structured_report"):
        with open("graph_audit_report.json", "w") as f:
            json.dump(final_state["structured_report"], f, indent=2)
        print("📁 Saved structured findings to: 'graph_audit_report.json'")
        
    # 2. Save the complete advanced remediation report from Node 3
    if final_state.get("deep_dive_remediation"):
        with open("remediation_patch.md", "w") as f:
            f.write(final_state["deep_dive_remediation"])
        print("📁 Saved architectural patch blueprint to: 'remediation_patch.md'")
        
        # Keep the scannable console snippet active
        print("\n🛡️  ADVANCED DEEP DIVE REMEDIATION PREVIEW:")
        print(final_state["deep_dive_remediation"][:500] + "\n...[Truncated for Scannability]...")